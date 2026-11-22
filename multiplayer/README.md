# Multiplayer migration

This directory is the isolated multiplayer track. The current launcher remains
the single-player fallback until this track can start a real networked match.

## Decision

Use the Xash3D FWGS browser networking stack that supports browser WebRTC, with
a compatible dedicated game server. Do not treat publishing the HTML/WASM files
as hosting a match: those files are only the player client. The game server
owns the match and must run continuously somewhere reachable by the players.

The known working reference architecture is `webxash3d-fwgs` plus its
`cs-web-server` image. Its browser client connects to the server through a
WebSocket signaling endpoint and sends game traffic over WebRTC/UDP. A server
can run on a rented host or a player's machine; it does not have to run on the
project author's PC.

## Compatibility constraint

The existing page uses `xash3d-fwgs@0.0.4` and `cs16-client@0.0.2`, with the
old Emscripten dynamic-library layout. That runtime does not provide the
WebRTC multiplayer path. The reference stack uses the newer `xash3d-fwgs`
`1.2.x` and `cs16-client` `0.1.x` packages and a matching server. Swapping only
the CDN version numbers is unsafe because the module layout and startup API
changed.

CS 1.1 content and bot behavior must be checked against the newer client and
server separately. Bot commands must execute on the authoritative server, so
the target is a match where human clients and server-side bots can occupy both
teams. A multiplayer UI that only starts a local listen server does not meet
the requirement.

## Rollout

1. Preserve the existing single-player page and its content unchanged.
2. Build a parallel browser client against the WebRTC-capable runtime and
   verify it loads this project's CS 1.1 assets.
3. Add a matching dedicated-server deployment with configurable map, player
   slots, and bot quota/team placement.
4. Connect two browser clients, then verify bot + player team compositions.
5. Port the existing launcher, trainer, navigation prompt, and skin importer
   only after the networked game path works. Keep the single-player fallback.

## Current state

- The legacy page is preserved at `legacy-index.snapshot.html` with a matching
  SHA-256 copy of the current root `index.html`.
- No multiplayer client or dedicated server has been wired in yet.
- Docker is not installed in the current workspace, so local server startup is
  unavailable until a host/runtime is provisioned.
