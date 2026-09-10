# Deploy Chess Room on Dokploy

Online games require the Node server. Static hosting can run local chess only.

For the `simonfibiger/chess` application on branch `main`:

1. Set the Git **Build Path** to `/web` and save.
2. Set **Build Type** to **Dockerfile**, Dockerfile path `Dockerfile`, and Docker build context `.` (relative to `/web`). Save.
3. Add a persistent named volume called `chess-data`, mounted at `/data`. The server runs as Node's unprivileged user (UID 1000); the directory must be writable by that user. A new Docker named volume inherits the image directory permissions.
4. Keep **one replica**, on the server holding this volume. SQLite is local to that server.
5. Change the existing domain's **Container Port** to `3000`; keep path `/` and HTTPS enabled. Save.
6. Deploy. Logs should show `Chess Room listening on port 3000`. `/health` should return `{"ok":true}`.
7. Hard-refresh the site. Join `12345` on one device and the same code on another device or a private browser window. White joins first; Black joins second. Play a move on each device and refresh to check reconnection.

No build/install command, external database service, API key, or npm dependency is needed. The image runs Node 24 and uses its built-in SQLite module. Keep the volume when redeploying: it stores games and player credentials. Back up `/data` using a SQLite-aware backup or while the server is stopped.

The first two browsers joining a code occupy its seats. A third browser is rejected. The browser stores a random seat token, so rejoining on that browser restores the same color. Clearing browser storage loses that seat; use a new code for a new game. Codes are casual invitations, so choose one your friend knows rather than treating it as a private account password.

Moves are validated on the server, saved before acknowledging, and polled every 1.2 seconds. Stale or duplicate moves are rejected. Online undo/reset is disabled to prevent one player rewriting a shared game. Return to local mode and choose a new code for a rematch. Rooms expire after seven days without a move or join.

## Local development

With Node 24 or later, run `npm start` in `web`, then open `http://localhost:3000`. Games are saved to `web/data/chess.sqlite` (ignored by Git). Run `npm ci` then `npm test` for chess, server integration, and simulated two-client DOM checks. The DOM dependency is used only for tests; it is excluded from the Docker image.

The original `python server.py` launcher still supports local same-screen play. It does not provide the multiplayer API.

## Empty-board fix

The previous Static deployment served `.mjs` as `application/octet-stream`, which browsers refuse for JavaScript modules. The public modules now use `.js`, and the Node server explicitly serves them as `text/javascript`.
