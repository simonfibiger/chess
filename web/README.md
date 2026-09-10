# Chess Room

A two-player, same-screen browser chess game using the piece PNGs from `C:\programing\chess\pictures\actual\pieces`.

The original Python project is unchanged. Its movement code is tightly coupled to Pygame rendering and currently ends games by capturing a king. This version uses the bundled BSD-licensed chess.js 1.4.0 library for standard legal moves, check/checkmate, stalemate, castling, en passant, promotion, and draw detection. It automatically ends games on threefold repetition or the 50-move rule. There is no Python backend, computer opponent, online multiplayer, clock, or saved-game persistence.

## Run locally

Double-click `Start Chess.cmd` on Windows. Keep its terminal open while playing. Or run `python server.py` in this folder. The local Python server opens the browser after binding successfully. If port 8765 is occupied, use `python server.py --port 8766`. The server only serves the application; chess rules run in JavaScript.

Click a piece and a highlighted destination. Keyboard users can Tab into the board, navigate with arrow keys, and use Enter or Space to select and move. Escape clears selection; F flips the board. Promotion lets you choose all four piece types. Undo removes one half-move; New game asks before clearing a played game.

All assets and the rules library are bundled locally. No external runtime services are required. See `dist/CHESS-LICENSE.txt` for the rules library license; piece artwork was supplied by the original project.

## Validation

`node check.mjs` checks chess rule scenarios and local assets. JavaScript syntax and the local HTTP response were also checked. Optional WebMCP read/move tools are feature-detected; no supported WebMCP validation context was available, so these experimental tools were not verified. Browser interaction and visual testing have not been performed.
