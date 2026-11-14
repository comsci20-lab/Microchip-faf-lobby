# Microchip faf lobby

Lobby extensions collected from Microchip faf-re:
- Ranked preferred colours (1, 2, 3), configurable with **Colour preferences** in the lobby. Defaults: yellow, blue, green.
- Immediately requests the highest available preference on lobby updates, including when another player releases yellow. Occupied human and AI colours are excluded. If every preference is occupied, keeps the current colour.
- Uses FAF RequestColor / SetColor and host authority; no speculative local colour changes. Repeated requests for an unchanged roster are suppressed after rejection. Ready players, observers, single-player and organiser-controlled lobbies are left alone. Changes resume when unready/seated.
- Connection diagnostics / lag test and extra checksum toggle.
- Lobby ready sound and Windows taskbar alert (optional UI mod).
- Offline lobby/chat translation (optional UI mod; requires native translator and language packs).
- Existing organiser-controlled lobby locks and refused-launch recovery.

## Install
Requires an existing compatible **faf-re** engine with append-only `/fafengine` hooks. These are not ordinary standalone FAF vault mods. Close the game, back up your FAF `bin_x64/fafengine` folder, then copy `data/fafengine` into `bin_x64/fafengine`. Copy the optional `mods` folders into your FAF user mods directory and enable them in FAF. The colour feature is built into the engine overlay and does not require a mod toggle. Preferences are saved in the active FAF player profile.

This repository contains the lobby overlays and optional lobby-related mods, not the native engine or offline translation models. Obtain the compatible engine from the existing faf-re project. Do not replace FAF downloaded `lua.nx2` archives.

## Validation
Run `python tests/test_lobby_colours.py` from this folder (Python with lupa). Tests exercise the Lua 5.1 colour-selection code using mocked FAF state. Live multiplayer / rendered UI validation remains required.
