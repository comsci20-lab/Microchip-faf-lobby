# Project rules
Never commit credentials. Preserve FAF lobby host authority and existing RequestColor/SetColor messages. Respect occupied colours, Ready state, observers and organiser locks. Keep lobby overlays compatible with faf-re append-only loading. Test using `python tests/test_lobby_colours.py`. Do not claim live verification without an actual multiplayer check.
For lobby UI changes, check new controls against all neighboring visible controls, including Presets/Unit Manager and host/guest variants, at supported UI scales before release. Anchoring below a control is not proof that the space is free.

