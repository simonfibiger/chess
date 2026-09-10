# Chess Room

A two-player browser chess game: play on the same screen or join a friend online with a five-digit room code.

The original Python project is unchanged. This version uses the bundled BSD-licensed chess.js 1.4.0 library for standard legal moves, check/checkmate, stalemate, castling, en passant, promotion, and draw detection. It automatically ends games on threefold repetition or the 50-move rule. Online games use a Node 24 server and SQLite to save moves and enforce turns; browsers poll for updates every 1.2 seconds. There is no computer opponent or clock.

## Play online

Run `npm start` with Node 24+ installed, then open `http://localhost:3000`. Enter the same five-digit code on two devices: the first joins as White, the second as Black. Refreshing restores your seat in the same browser. A third player cannot join an occupied room. Online undo and reset are disabled; choose a new code for another game. Room data is retained for seven days without a move or join. Browser storage must remain available to restore a seat after refresh.

For the hosted site, follow [Dokploy deployment settings](DEPLOY.md), including its persistent `/data` volume. Static hosting supports same-screen play only.

## Run locally

Double-click `Start Chess.cmd` on Windows. Keep its terminal open while playing. Or run `python server.py` in this folder. The local Python server opens the browser after binding successfully. If port 8765 is occupied, use `python server.py --port 8766`. The server only serves the application; chess rules run in JavaScript.

Click a piece and a highlighted destination. Keyboard users can Tab into the board, navigate with arrow keys, and use Enter or Space to select and move. Escape clears selection; F flips the board. Promotion lets you choose all four piece types. Undo removes one half-move; New game asks before clearing a played game.

All assets and the rules library are bundled locally. No external runtime services are required. See `dist/CHESS-LICENSE.txt` for the rules library license; piece artwork was supplied by the original project.

## Validation

Run `npm ci` then `npm test`. Tests check chess rules, assets, room pairing, seat authentication, turn enforcement, duplicate requests, room isolation, checkmate, JavaScript MIME types, and persistence through a server restart. DOM tests also check board rendering, local controls, and two clients syncing moves and reconnecting. These are simulated DOM checks, not visual browser tests. Optional WebMCP read/move tools are feature-detected; no supported WebMCP validation context was available, so these experimental tools were not verified.
