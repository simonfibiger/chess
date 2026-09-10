import { createServer } from 'node:http';
import { DatabaseSync } from 'node:sqlite';
import { mkdirSync, readFileSync } from 'node:fs';
import { resolve, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { randomBytes, createHash } from 'node:crypto';
import { Chess } from './dist/chess.js';

const root = dirname(fileURLToPath(import.meta.url));
const hash = token => createHash('sha256').update(token).digest('hex');
const fail = (status, message) => { throw Object.assign(new Error(message), { status }); };

export function createChessServer({ dataDir = process.env.DATA_DIR || resolve(root, 'data') } = {}) {
  mkdirSync(dataDir, { recursive: true });
  const db = new DatabaseSync(resolve(dataDir, 'chess.sqlite'));
  db.exec(`PRAGMA journal_mode=WAL;
    CREATE TABLE IF NOT EXISTS rooms (
      pin TEXT PRIMARY KEY, white TEXT NOT NULL, black TEXT,
      moves TEXT NOT NULL DEFAULT '[]', version INTEGER NOT NULL DEFAULT 0,
      updated INTEGER NOT NULL
    );`);
  const get = db.prepare('SELECT * FROM rooms WHERE pin = ?');
  const limits = new Map();
  const limiter = setInterval(() => limits.clear(), 60000);
  limiter.unref();
  function authorize(room, req) {
    const token = req.headers.authorization?.replace(/^Bearer /, '') || '';
    const digest = hash(token);
    if (digest === room.white) return 'w';
    if (digest === room.black) return 'b';
    fail(401, 'Rejoin this room from the browser you used to join.');
  }
  function snapshot(room, color) {
    return { pin: room.pin, color, ready: Boolean(room.black), moves: JSON.parse(room.moves), version: room.version };
  }
  const server = createServer(async (req, res) => {
    const send = (status, body) => {
      res.writeHead(status, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
      res.end(JSON.stringify(body));
    };
    try {
      const url = new URL(req.url, 'http://localhost');
      if (url.pathname === '/health') return send(200, { ok: true });
      if (url.pathname.startsWith('/api/')) {
        // Do not accept cross-site mutations, even if a token is supplied.
        if (req.headers.origin && new URL(req.headers.origin).host !== req.headers.host) fail(403, 'Use this site to join and play.');
        const match = /^\/api\/rooms\/(\d{5})(?:\/(join|moves))?$/.exec(url.pathname);
        if (!match) fail(404, 'Use a five-digit room code.');
        const [, pin, action] = match;
        let body = {};
        if (req.method === 'POST') {
          let raw = '';
          for await (const chunk of req) {
            raw += chunk;
            if (Buffer.byteLength(raw) > 2048) fail(413, 'Request is too large.');
          }
          try { body = JSON.parse(raw || '{}'); } catch { fail(400, 'Invalid request.'); }
          if (!body || typeof body !== 'object' || Array.isArray(body)) fail(400, 'Invalid request.');
        }
        if (action === 'join' && req.method === 'POST') {
          const ip = req.socket.remoteAddress;
          const count = (limits.get(ip) || 0) + 1;
          limits.set(ip, count);
          if (count > 120) fail(429, 'Too many attempts. Please wait a minute.');
          // Codes become available again after seven days without a move or join.
          db.prepare('DELETE FROM rooms WHERE updated < ?').run(Date.now() - 7 * 86400000);
          let room = get.get(pin);
          if (room && req.headers.authorization) {
            const color = authorize(room, req);
            db.prepare('UPDATE rooms SET updated = ? WHERE pin = ?').run(Date.now(), pin);
            return send(200, snapshot(room, color));
          }
          if (room?.black) fail(409, 'This room already has two players. Try a different code.');
          const token = randomBytes(32).toString('hex');
          const color = room ? 'b' : 'w';
          if (!room) db.prepare('INSERT INTO rooms (pin, white, updated) VALUES (?, ?, ?)').run(pin, hash(token), Date.now());
          else db.prepare('UPDATE rooms SET black = ?, version = version + 1, updated = ? WHERE pin = ?').run(hash(token), Date.now(), pin);
          room = get.get(pin);
          return send(200, { ...snapshot(room, color), token });
        }
        const room = get.get(pin);
        if (!room) fail(404, 'This room has expired. Join a new room.');
        const color = authorize(room, req);
        if (!action && req.method === 'GET') return send(200, snapshot(room, color));
        if (action === 'moves' && req.method === 'POST') {
          if (!room.black) fail(409, 'Waiting for the second player.');
          if (body.version !== room.version) fail(409, 'The board changed. Syncing the latest moves.');
          const game = new Chess();
          for (const move of JSON.parse(room.moves)) game.move(move);
          if (game.isGameOver()) fail(409, 'This game has ended. Join a new code to play again.');
          if (game.turn() !== color) fail(403, 'Wait for your turn.');
          if (!/^[a-h][1-8]$/.test(body.from) || !/^[a-h][1-8]$/.test(body.to) || !['q','r','b','n'].includes(body.promotion || 'q')) fail(400, 'Invalid move.');
          try { game.move({ from: body.from, to: body.to, promotion: body.promotion || 'q' }); }
          catch { fail(400, 'That move is not legal.'); }
          db.prepare('UPDATE rooms SET moves = ?, version = version + 1, updated = ? WHERE pin = ?')
            .run(JSON.stringify(game.history()), Date.now(), pin);
          return send(200, snapshot(get.get(pin), color));
        }
        fail(405, 'Method not allowed.');
      }
      if (!['GET', 'HEAD'].includes(req.method)) fail(405, 'Method not allowed.');
      const path = decodeURIComponent(url.pathname);
      // Only explicitly public files are served; the database is outside dist.
      if (!/^\/(?:index\.html|style\.css|app\.js|chess\.js|CHESS-LICENSE\.txt|assets\/[\w ()-]+\.png)?$/.test(path)) fail(404, 'Not found.');
      const file = resolve(root, 'dist', path === '/' ? 'index.html' : path.slice(1));
      let content;
      try { content = readFileSync(file); } catch { fail(404, 'Not found.'); }
      const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.png': 'image/png', '.txt': 'text/plain; charset=utf-8' };
      res.writeHead(200, { 'Content-Type': types[extname(file)], 'Cache-Control': 'no-cache', 'X-Content-Type-Options': 'nosniff' });
      res.end(req.method === 'HEAD' ? undefined : content);
    } catch (error) {
      if (!error.status) console.error(error);
      if (!res.headersSent) send(error.status || 500, error.status ? { error: error.message } : { error: 'Server error. Please try again.' });
    }
  });
  server.on('close', () => { clearInterval(limiter); db.close(); });
  return server;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const server = createChessServer();
  server.listen(Number(process.env.PORT || 3000), '0.0.0.0', () => console.log(`Chess Room listening on port ${server.address().port}`));
  for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => server.close(() => process.exit(0)));
}
