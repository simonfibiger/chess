# Deploy the Python version on Dokploy

This branch is `python-online-backend`. GitHub `main` independently received commit `356e64e` with a Node/PIN implementation while this Python backend was being built. That work has not been overwritten. This branch offers the requested Python backend and invite-link interface; it does not migrate rooms or player tokens from the Node version.

In the existing `simonfibiger/chess` Dokploy application:

1. Select branch **python-online-backend**.
2. Set Git **Build Path** to `/web`.
3. Select **Dockerfile** build type, Dockerfile path `Dockerfile`, and build context `.` relative to `/web`.
4. Keep one replica. Mount a persistent volume at `/data`, writable by UID **1000**. The Python database is `/data/rooms.sqlite3`; any existing Node database with a different filename stays separate.
5. Set the domain's container port to **3000**, path `/`, with HTTPS enabled.
6. Deploy. Verify `/api/health` returns `{"ok":true}`.
7. Open the public URL on device one, click **Create online game**, and send the invite link. On device two, open the link and click **Join invited game**. Try one move each and reload to verify reconnection.

The Dockerfile installs requirements and runs Waitress as an unprivileged user. No API keys are needed. Back up the volume before switching an existing service; retain it across redeployments. To return to the Node/PIN version, select `main` and use that branch's deployment instructions.

The Python application and live local transport were tested on Windows. A Docker build and deployment have not been run here. Deployment is the next user step, not something this commit has performed.
