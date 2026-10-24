# Plan

Open items, worked through in this order. Accepted proposals from
`PROPOSALS.md` land here. Finished items are struck through with the date
and commit, e.g. `1. ~~**Item**~~ — done 2026-01-31 (`abc1234`).`

Taken over from the old `docs/ENHANCEMENT_PLAN.md` on 2026-10-24 (open
Phases 12–14; the done phases 0–11 are in `CHANGELOG.md` and git, see
D16). The old plan set no order between the Seven Hats and Phases 12–13;
the series comes first here because it was "next" there.

## The Seven Hats (series; story bible: `docs/seven-hats/STORYLINE.md`)

1. ~~**Series metadata**~~ — done 2026-09-27 (#46). `series`, `part`,
   `hat` and a per-story `version` in the manifest; story cards show "The
   Seven Hats · Part 1 · Black Hat".
2. ~~**Draft stories**~~ — done 2026-10-24 (#47). `draft: true` keeps
   unfinished stories out of the story lists.
3. **Part 1, Black (Vesper).** The owner writes the text (D15); Claude
   does `check_story`, tests and publishing. Runs on today's engine.
4. **Scope:** a terminal block's `scope: [hosts]` with
   `on_scope_violation: <scene>`. `scan`/`connect`/`ssh` against a host
   outside the scope sends the story there (or logs a violation that later
   gates endings), like the trace meter. Needed for White and for Blue's
   bounty terms.
5. **Engagement clock:** the trace meter with a label, e.g. `trace:
   {limit: 12, label: "hours left"}`, so a deadline doesn't read as
   "trace". Needed for Blue.
6. **Part 2, Blue (Ines).**
7. **Part 3, White (Theo).**
8. **Part 4, Gray (Kade).**
9. **Part 5, Green (Mika).**
10. **Part 6, Red (Rook).**
11. **Part 7, Purple (Noor).**

## More stories

12. **Story delivery independent of the game version** (D7): published
    stories are downloadable into the user stories folder (e.g.
    `sidechannel stories update`), each with its own `version` in its
    manifest. The browser needs none of this, since it deploys from
    `main`. Until this exists, terminal players get new stories only with
    a game release.
13. **User stories:** a stories folder in the user data directory (TUI),
    checked with `check_story` on load; loading a story zip in the
    browser.
14. `sidechannel new-story <id>`: a skeleton story that passes the
    checker.
15. **An author guide:** split the authoring half of the README into
    `docs/authoring.md`.

## Polish

16. Browser settings: text size and a light theme, remembered per browser.
17. Load progress: a percentage for the first ~10 MB download.
18. Optional: a German interface and stories.

Deferred: a story search/filter box, once there are many stories (D14).
