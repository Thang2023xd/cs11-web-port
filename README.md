# Counter-Strike 1.1 Web Port

A browser launcher for the CS 1.1 game files, using Xash3D FWGS and WebAssembly.

## Run locally

Serve this folder from a local web server (for example, `python -m http.server 8000`) and open `http://localhost:8000`. The browser needs WebAssembly and WebGL 2.

The game installation and generated asset archives are intentionally excluded from Git. When the launcher asks for game data, select a locally owned `valve.zip`. The launcher can also load `assets.zip` and `pak0.pak` when those files are present beside `index.html` locally.

## Publish the launcher with GitHub Pages

Push this repository to GitHub, then open **Settings → Pages** and choose **GitHub Actions** as the build and deployment source. The workflow deploys `index.html` on each push to `main`.

The published page contains the launcher code, not the game installation. Each player must provide their own game data through the launcher's file picker. Do not add `CS11/`, `valve.zip`, `assets.zip`, or `pak0.pak` to a public repository or Pages deployment unless you have redistribution rights for those files.

## Navigation files

Use **Bot navigation sync** in the launcher to import `.nav` files and export saved maps as a ZIP. Transfer that ZIP to another device and import it there; each browser keeps its own navigation cache.

## Multiplayer status

The `multiplayer/` directory documents the separate multiplayer migration track. Publishing the browser client on GitHub Pages does not host a game server; see `multiplayer/README.md` for the current architecture notes.
