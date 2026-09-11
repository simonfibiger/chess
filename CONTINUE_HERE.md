# Where the Python project stopped

**Online update:** the later `feat: add Python backend for online chess rooms` commit adds server-authoritative online play inside `web/`. The two earlier checkpoints below remain intact. For current startup and hosting instructions, read `web/README.md`; the browser-version description below documents the earlier offline checkpoint.

The original desktop project is preserved exactly, including unfinished experiments and assets. No original files were changed for the browser version.

## Clearly separated Git checkpoints

1. **`5b7ff83fd5a8f3884bb2482fe52556297cefb77a` — `checkpoint: original Python chess before browser version`**
   This is the exact old-code snapshot, with the same Git tree as the original `64075c2011061d9f3ebf65f024c9f59026b35d0b` commit. The checkpoint intentionally changes no files; its commit message marks the handoff clearly.
2. **`feat: add browser chess in web without changing Python project`**
   This adds the independent browser game in `web/` and this guide. Everything outside those additions remains as it was at the old-code checkpoint.

On GitHub, open the checkpoint commit and choose **Browse files** to see precisely where desktop development stopped. To inspect it locally without changing your current checkout, run `git worktree add ../chess-python-checkpoint 5b7ff83fd5a8f3884bb2482fe52556297cefb77a`.

## Continue the original desktop game

The entry point is `code/main.py`, which opens `code/Menu.py`. `code/game_modes.py` contains the single-screen and local two-player modes; `code/game_state.py` owns Pygame state and clocks; `code/Piece.py` contains piece movement and rendering. Relative asset paths use `pictures/`, so launch from the repository root: `python code/main.py` with Pygame installed.

The original logic remains unchanged: it is coupled to Pygame and ends games by capturing kings. Do not confuse it with the standard-rule browser engine.

## Continue the browser game

Double-click `web/Start Chess.cmd`, or run `python web/server.py`. Python 3 is required; no Python packages are needed. The Python server serves the files locally. Legal-move logic runs in the browser using the bundled chess.js library; there is no Python chess API or online multiplayer backend.

- `web/dist/index.html`: page structure.
- `web/dist/style.css`: responsive board and interface styles.
- `web/dist/app.mjs`: board interactions and game state.
- `web/dist/chess.mjs`: bundled third-party chess rules library.
- `web/server.py`: local Python HTTP server and browser launcher.

The browser version reuses the original chess-piece artwork and offers two-player chess on one device, promotion, undo, board flipping, sound, and three board colors. Games are untimed and are not saved on reload.
