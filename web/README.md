# Chess Room — Python online multiplayer

Play on the same screen, or create a room and invite a friend on another device. The original Pygame project outside `web/` is unchanged.

## Start on Windows

Double-click `Start Chess.cmd`. The first run creates a virtual environment and installs the packages in `requirements.txt`, then starts the Python server on port 8765. Keep the terminal open.

Or run from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe server.py --host 0.0.0.0 --port 8765
```

## Two devices on the same Wi-Fi

1. Run the server on your computer.
2. Find that computer's private IPv4 address with `ipconfig` (for example `192.168.1.20`).
3. **On both devices**, open `http://192.168.1.20:8765`, substituting the actual address. Do not use `localhost` or `127.0.0.1` on the second device: those addresses refer to the device itself. Opening the private-IP address on the host also ensures the invite link has the correct address.
4. On the first device, click **Create online game**, then send the displayed invite link.
5. On the other device, open that link and click **Join invited game**. The creator is White; the guest is Black. Black sees a flipped board.

If Windows prompts, allow Python on your private network. Guest Wi-Fi/client isolation can prevent devices from reaching each other. The app does not change your firewall. Plain HTTP is intended for trusted local-network testing; internet hosting needs HTTPS.

## Next step: play over the internet

Deploy this **Python service and its `dist/` frontend together**, on a Python-capable host. The previous static Sites link does not run this backend and has not been updated with online play.

For your existing Dokploy setup, see [DEPLOY.md](DEPLOY.md). Select branch **python-online-backend**; `main` retains the independently added Node implementation. General deployment settings:

- Repository: `simonfibiger/chess`, root directory: `web`.
- Build/install command: `pip install -r requirements.txt`.
- Start command: `python server.py --host 0.0.0.0 --no-browser`.
- The server reads the host's `PORT` environment variable (default 8765).
- Set `CHESS_DB` to a path on a **persistent disk**, for example `/data/rooms.sqlite3`.
- Use **one running service instance** with its persistent disk. Multiple independent disks would produce different rooms; multi-instance hosting needs a shared database.
- Enable HTTPS on the hosting platform. Keep the frontend and `/api/` under the same domain; no CORS configuration is needed.
- Use `/api/health` for a health check.

Once deployed, open that public URL, create a room, and share its invite. No port forwarding on your home router is needed. Hosting has not been provisioned by this change.

## How it works

`server.py` uses Flask, Waitress, SQLite, and python-chess. **Python owns the board, checks turns, validates every move, and decides the result.** The browser uses the existing bundled chess.js library only to draw the board, display history, and highlight moves. Online moves appear after server acceptance. Clients poll once per second and automatically retry after network failures.

Each player receives a random credential stored in that browser's local storage; the server stores its hash. The invite contains only a random room ID, never the player's credential. The first guest to accept the invite takes the Black seat. Do not publish an invitation before your intended opponent joins. A third player cannot take an occupied seat.

Reload or reopen the same room URL **in the same browser and on the same host address** to resume your seat. Browser data deletion loses that seat's credential; start a new room if this happens. Games survive server restarts when the database is retained. Rooms expire seven days after creation; the server caps storage at 1,000 active rooms. This small personal-game backend does not implement accounts, matchmaking, clocks, resignations, spectators, or automatic seat replacement. For a widely advertised public service, add platform request limits and operational monitoring.

Online undo and local New game are disabled to prevent one player changing the other player's board. Use **Create online game** for another room; existing rooms remain available via their links. **Return to local board** exits online mode without deleting the saved game.

Draws are automatically declared on the third occurrence of a position or after 50 moves each without a pawn move/capture, matching the original browser version's convention rather than requiring draw claims.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_server.py
node check.mjs
# With the Python server running on port 8766:
node test_online.mjs http://127.0.0.1:8766
```

Tests cover two independent players, server-side move rejection, concurrent joins/moves, unauthorized access, game-over enforcement, en passant, persistence across application restarts, and static-file isolation. `check.mjs` covers the browser chess engine's special moves and assets. Browser visual testing is separate from these integration checks.

## Dependencies and attribution

The piece PNGs come from your original project. chess.js is bundled with its BSD license in `dist/CHESS-LICENSE.txt`. Python-chess is an external GPL-3.0-or-later dependency, installed through pip; its source and license are provided by that package. See [python-chess documentation](https://python-chess.readthedocs.io/en/stable/) and [Flask's Waitress deployment documentation](https://flask.palletsprojects.com/en/stable/deploying/waitress/).
