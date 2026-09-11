"""Authoritative two-player chess rooms, persisted in SQLite."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
import time
from urllib.parse import urlsplit
import webbrowser
from contextlib import contextmanager
import chess
from flask import Flask, jsonify, request, send_from_directory, abort
from werkzeug.exceptions import HTTPException

ROOT = Path(__file__).resolve().parent

def digest(token):
    return hashlib.sha256(token.encode()).hexdigest()

def result_for(board):
    outcome = board.outcome()
    if outcome:
        return outcome.result(), outcome.termination.name.lower()
    if board.is_repetition(3):
        return '1/2-1/2', 'threefold_repetition'
    if board.halfmove_clock >= 100:
        return '1/2-1/2', 'fifty_moves'
    return None, None

def create_app(database=None):
    app = Flask(__name__, static_folder=None)
    app.config['MAX_CONTENT_LENGTH'] = 4096
    path = Path(database or os.environ.get('CHESS_DB', ROOT / 'data' / 'rooms.sqlite3'))
    path.parent.mkdir(parents=True, exist_ok=True)
    @contextmanager
    def connect():
        db = sqlite3.connect(path, timeout=15)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()
    with connect() as db:
        db.execute('PRAGMA journal_mode=WAL')
        db.execute('''CREATE TABLE IF NOT EXISTS rooms (
            id TEXT PRIMARY KEY, white TEXT NOT NULL, black TEXT,
            moves TEXT NOT NULL DEFAULT '[]', version INTEGER NOT NULL DEFAULT 0,
            created REAL NOT NULL)''')
    def fail(message, status):
        abort(status, description=message)
    def payload():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            fail('Send a JSON object.', 400)
        return data
    def room(db, room_id):
        row = db.execute('SELECT * FROM rooms WHERE id=?', (room_id,)).fetchone()
        if row is None or row['created'] < time.time() - 7 * 86400:
            fail('This room has expired or does not exist. Create a new game.', 404)
        return row
    def seat(row):
        header = request.headers.get('Authorization', '')
        if not header.startswith('Bearer ') or len(header) > 200:
            fail('Reopen this room in the browser where you joined.', 401)
        hashed = digest(header[7:])
        for name, color in [('white', 'w'), ('black', 'b')]:
            if row[name] and secrets.compare_digest(row[name], hashed):
                return color
        fail('This player credential does not belong to this room.', 403)
    def board_for(row):
        board = chess.Board()
        for uci in json.loads(row['moves']):
            board.push_uci(uci)
        return board
    def state(row, color):
        board = board_for(row)
        result, reason = result_for(board)
        return dict(room=row['id'], color=color, ready=bool(row['black']),
                    version=row['version'], moves=json.loads(row['moves']),
                    fen=board.fen(), turn='w' if board.turn else 'b', result=result, reason=reason)
    @app.before_request
    def same_origin():
        if request.method == 'POST':
            origin = request.headers.get('Origin')
            if origin and urlsplit(origin).netloc != request.host:
                fail('Open the game and its API on the same host.', 403)
    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Cache-Control'] = 'no-store' if request.path.startswith('/api/') else 'no-cache'
        return response
    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(error=error.description), error.code
    @app.get('/api/health')
    def health():
        return jsonify(ok=True)
    @app.post('/api/rooms')
    def create_room():
        payload()
        room_id, token = secrets.token_urlsafe(12), secrets.token_urlsafe(32)
        with connect() as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('DELETE FROM rooms WHERE created < ?', (time.time() - 7 * 86400,))
            if db.execute('SELECT count(*) FROM rooms').fetchone()[0] >= 1000:
                fail('The server has reached its room limit. Try again later.', 503)
            db.execute('INSERT INTO rooms(id,white,created) VALUES(?,?,?)', (room_id, digest(token), time.time()))
            response = state(room(db, room_id), 'w')
        return jsonify(**response, token=token), 201
    @app.post('/api/rooms/<room_id>/join')
    def join(room_id):
        payload()
        with connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = room(db, room_id)
            if row['black']:
                fail('This room already has two players.', 409)
            token = secrets.token_urlsafe(32)
            db.execute('UPDATE rooms SET black=?,version=version+1 WHERE id=?', (digest(token), room_id))
            response = state(room(db, room_id), 'b')
        return jsonify(**response, token=token)
    @app.get('/api/rooms/<room_id>')
    def read_room(room_id):
        with connect() as db:
            row = room(db, room_id)
            return jsonify(state(row, seat(row)))
    @app.post('/api/rooms/<room_id>/moves')
    def move(room_id):
        data = payload()
        uci, version = data.get('move'), data.get('version')
        if not isinstance(uci, str) or not re.fullmatch('[a-h][1-8][a-h][1-8][qrbn]?', uci) or type(version) is not int:
            fail('Provide a UCI move and the current integer version.', 400)
        with connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = room(db, room_id)
            color = seat(row)
            if not row['black']:
                fail('Wait for the other player to join.', 409)
            if row['version'] != version:
                fail('The board changed. Reconnect and try again.', 409)
            board = board_for(row)
            if result_for(board)[0]:
                fail('This game has ended.', 409)
            if color != ('w' if board.turn else 'b'):
                fail('It is the other player\'s turn.', 403)
            try:
                proposed = chess.Move.from_uci(uci)
            except ValueError:
                fail('That move is not legal.', 400)
            if proposed not in board.legal_moves:
                fail('That move is not legal.', 400)
            moves = json.loads(row['moves']) + [uci]
            db.execute('UPDATE rooms SET moves=?,version=version+1 WHERE id=?', (json.dumps(moves), room_id))
            response = state(room(db, room_id), color)
        return jsonify(response)
    @app.get('/')
    def index():
        return send_from_directory(ROOT / 'dist', 'index.html')
    @app.get('/<path:filename>')
    def asset(filename):
        response = send_from_directory(ROOT / 'dist', filename)
        if filename.endswith(('.js', '.mjs')):
            response.mimetype = 'text/javascript'
        return response
    return app

def main():
    from waitress import serve
    parser = argparse.ArgumentParser(description='Start online Chess Room')
    parser.add_argument('--host', default=os.environ.get('HOST', '127.0.0.1'))
    parser.add_argument('--port', type=int, default=int(os.environ.get('PORT', '8765')))
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    app = create_app()
    url = f'http://{"127.0.0.1" if args.host == "0.0.0.0" else args.host}:{args.port}/'
    print(f'Chess Room: {url}\nKeep this server running while playing.', flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    serve(app, host=args.host, port=args.port, threads=8)

if __name__ == '__main__':
    main()
