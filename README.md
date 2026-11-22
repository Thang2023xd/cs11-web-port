# Counter-Strike 1.1 Web Port

A browser launcher for the CS 1.1 game files, using Xash3D FWGS and WebAssembly.

## Run locally

Serve this folder from a local web server (for example, `python -m http.server 8000`) and open `http://localhost:8000`. The browser needs WebAssembly and WebGL 2.

The game installation and generated asset archives are intentionally excluded from Git. When the launcher asks for game data, select a locally owned `valve.zip`. The launcher can also load `assets.zip` and `pak0.pak` when those files are present beside `index.html` locally.

## Create `valve.zip`

Install Python 3, then download `makezip.py` and `split_assets.py` from this repository. Open PowerShell in the folder where you saved the scripts. The game folder you pass must contain `valve/` and `cstrike/` directly. Run the scripts **in order** because the second one reads the ZIP created by the first:

```powershell
py .\makezip.py "D:\Games\Counter-Strike 1.1"
py .\split_assets.py .\valve.zip
```

Replace `D:\Games\Counter-Strike 1.1` with the actual game folder. The first command creates `valve.zip` beside the scripts; the second creates `assets.zip` and `pak0.pak` beside that ZIP. If Python's `py` launcher is unavailable, use `python` in both commands instead. If the scripts are placed inside the game folder itself, run `py .\makezip.py` without the game-folder argument, then `py .\split_assets.py`.

## Publish the launcher with GitHub Pages

Push this repository to GitHub, then open **Settings → Pages** and choose **GitHub Actions** as the build and deployment source. The workflow deploys `index.html` on each push to `main`.

The published page contains the launcher code, not the game installation. Each player must provide their own game data through the launcher's file picker. Do not add `CS11/`, `valve.zip`, `assets.zip`, or `pak0.pak` to a public repository or Pages deployment unless you have redistribution rights for those files.

## Navigation files

Use **Bot navigation sync** in the launcher to import `.nav` files and export saved maps as a ZIP. Transfer that ZIP to another device and import it there; each browser keeps its own navigation cache.

## Multiplayer status

The `multiplayer/` directory documents the separate multiplayer migration track. Publishing the browser client on GitHub Pages does not host a game server; see `multiplayer/README.md` for the current architecture notes.
