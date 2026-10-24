# Plan

Open items, worked through in this order. Accepted proposals from
`PROPOSALS.md` land here. Finished items are struck through with the date
and commit, e.g. `1. ~~**Item**~~ — done 2026-01-31 (`abc1234`).`

Taken over from the old `docs/ENHANCEMENT_PLAN.md` on 2026-10-24 (open
Phases 12–14; the done phases 0–11 are in `CHANGELOG.md` and git, see
D16). The old plan set no order between the Seven Hats and Phases 12–13;
the series comes first here because it was "next" there.

## Review fixes (2026-10-24, was P1–P12; D17)

Security and UX first, as asked. Items 1–3 share one name check.

1. **Story names can't leave the sandbox** (was P1). Filesystem entry
   names, host ids, mail message ids and the manifest `id` become path
   parts (`materialize_fs_node`, `Network.materialize`,
   `materialize_delivered_mail`, `save_slot_path`). Check them on load:
   one segment, no `/`, `\`, `..` or NUL, not empty; ids
   `[A-Za-z0-9_.-]+`. `materialize_fs_node` also refuses targets that
   resolve outside the host dir. `check_story` reports bad names; test
   with a hostile story. Must land before items 24/25.
2. **Imported saves: safe sandbox names and mail ids** (was P2).
   `savefile._validated` allows only `[A-Za-z0-9_.-]` segments, checks the
   resolved target is inside the sandbox, and checks `email_queue[].id`
   like item 1. Optionally limit file count/size.
3. **Slot names checked everywhere** (was P3): `SLOT_NAME` enforced in
   `save_slot_path`, with a clear CLI error for `--slot`/`select_slot`.
4. **Self-host Pyodide** (was P4, option a). `web/build.py` downloads a
   pinned Pyodide release, checks its sha256 and ships the core files on
   Pages; `app.js`/`sw.js` load them from the site. Add a CSP `<meta>`
   (`default-src 'self'`, `'wasm-unsafe-eval'`, whatever else Pyodide
   needs -- test it).
5. **Service worker only deletes its own caches** (was P5): keys starting
   with `sidechannel-` (rename the Pyodide cache to `sidechannel-pyodide-…`).
   The generic IDBFS name `/saves` stays; note it as a known limit.
6. **Autosave on every scene change** (was P6, option a), in both
   frontends. Plus `navigator.storage.persist()` at boot in the browser,
   with a short "export to keep your saves" hint if it's refused.
7. **Ctrl+C / Ctrl+D in the launcher exit cleanly** (was P7): no
   traceback, exit code 130; `q` quits the pickers.
8. **Error messages say what to do next** (was P8): unknown story → close
   matches / `--list`; browser boot failure → network/content blocker
   hint; "internal error" → your last save is safe, Save & exit.
9. **`look` command and a "Previously…" recap** (was P9): reprints the
   current scene's text (`MANUAL` entry, not traced); continuing a slot
   shows the last few journal entries above the scene.
10. **Browser accessibility** (was P10): only new scene text/command output
    is announced (one live region, not both logs), `role="log"` on the
    panes, keyboard shortcuts to focus story/terminal; dark/light goes into
    item 28. Check with Orca.
11. **Pin the CI tooling** (was P11): pytest/ruff/mypy and build/twine
    versions in a file Dependabot updates.
12. **Test the dependency floors** (was P12): a CI job with the lowest
    allowed versions; raise the floors to what passes.

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
