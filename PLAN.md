# Plan

Open items, worked through in this order. Accepted proposals from
`PROPOSALS.md` land here. Finished items are struck through with the date
and commit, e.g. `1. ~~**Item**~~ — done 2026-01-31 (`abc1234`).`

Taken over from the old `docs/ENHANCEMENT_PLAN.md` on 2026-10-24 (open
Phases 12–14; the done phases 0–11 are in `CHANGELOG.md` and git, see
D16). The old plan set no order between the Seven Hats and Phases 12–13;
the series comes first here because it was "next" there.

## Review fixes (2026-10-24, was P1–P12; D17)

Security and UX first, as asked.

1. ~~**Story names can't leave the sandbox**~~ — done 2026-10-24
   (`39f93e3`). Story id, host ids, file names, NPC and topic ids are
   checked on load.
2. ~~**Imported saves: safe sandbox names and mail ids**~~ — done
   2026-10-24 (`5897452`). No file count/size limit (optional, skipped).
3. ~~**Slot names checked everywhere**~~ — done 2026-10-24 (`4187e22`).
   New names must match `SLOT_NAME`; existing slots keep their names, only
   path-like ones are refused.
4. ~~**Self-host Pyodide**~~ — done 2026-10-24 (`c8c975f`). Plus a CSP.
5. ~~**Service worker only deletes its own caches**~~ — done 2026-10-24
   (`0b02f7d`).
6. ~~**Autosave on every scene change**~~ — done 2026-10-24 (`612bea1`).
   Plus `navigator.storage.persist()` when a new game starts.
7. ~~**Ctrl+C / Ctrl+D in the launcher exit cleanly**~~ — done 2026-10-24
   (`79985e1`).
8. ~~**Error messages say what to do next**~~ — done 2026-10-24
   (`b298086`).
9. ~~**`look` command and a "Previously…" recap**~~ — done 2026-10-24
   (`0e6feb3`).
10. ~~**Browser accessibility**~~ — done 2026-10-24 (`be16ecd`). Not yet
    checked with a real screen reader (Orca); dark/light is item 28.
11. ~~**Pin the CI tooling**~~ — done 2026-10-24 (`8a04826`).
    `requirements-ci.txt`.
12. ~~**Test the dependency floors**~~ — done 2026-10-24 (`9aee1f9`).
    Floors now `textual>=3.2`, `rich>=13.3.3`.

## The Seven Hats (series; story bible: `docs/seven-hats/STORYLINE.md`)

13. ~~**Series metadata**~~ — done 2026-09-27 (#46). `series`, `part`,
   `hat` and a per-story `version` in the manifest; story cards show "The
   Seven Hats · Part 1 · Black Hat".
14. ~~**Draft stories**~~ — done 2026-10-24 (#47). `draft: true` keeps
   unfinished stories out of the story lists.
15. **Part 1, Black (Vesper).** The owner writes the text (D15); Claude
   does `check_story`, tests and publishing. Runs on today's engine.
16. **Scope:** a terminal block's `scope: [hosts]` with
   `on_scope_violation: <scene>`. `scan`/`connect`/`ssh` against a host
   outside the scope sends the story there (or logs a violation that later
   gates endings), like the trace meter. Needed for White and for Blue's
   bounty terms.
17. **Engagement clock:** the trace meter with a label, e.g. `trace:
   {limit: 12, label: "hours left"}`, so a deadline doesn't read as
   "trace". Needed for Blue.
18. **Part 2, Blue (Ines).**
19. **Part 3, White (Theo).**
20. **Part 4, Gray (Kade).**
21. **Part 5, Green (Mika).**
22. **Part 6, Red (Rook).**
23. **Part 7, Purple (Noor).**

## More stories

24. **Story delivery independent of the game version** (D7): published
    stories are downloadable into the user stories folder (e.g.
    `sidechannel stories update`), each with its own `version` in its
    manifest. The browser needs none of this, since it deploys from
    `main`. Until this exists, terminal players get new stories only with
    a game release.
25. **User stories:** a stories folder in the user data directory (TUI),
    checked with `check_story` on load; loading a story zip in the
    browser.
26. `sidechannel new-story <id>`: a skeleton story that passes the
    checker.
27. **An author guide:** split the authoring half of the README into
    `docs/authoring.md`.

## Polish

28. Browser settings: text size and a light theme, remembered per browser.
29. Load progress: a percentage for the first ~13 MB download.
30. Optional: a German interface and stories.

Deferred: a story search/filter box, once there are many stories (D14).
