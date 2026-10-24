# Side Channel

Instructions for anyone working on this repo: people and AI agents of any
kind (Claude Code, Codex, Gemini CLI, Copilot, …). Claude Code reads this
file through `CLAUDE.md`. Only lasting knowledge goes here. Where things
stand right now goes in `STATUS.md`.

## Goal

A terminal hacking thriller: a hacker-themed text adventure with a fake
terminal, played in a terminal (a full-screen Textual app, `pipx install
sidechannel`) or in the browser (https://derd1ngs.github.io/sidechannel/,
the same Python engine in Pyodide). The game ships with stories written in
YAML; the README documents playing and story authoring. The story series
"The Seven Hats" has its own story bible, `docs/seven-hats/STORYLINE.md`.

## Context

- Python package `sidechannel/`: `engine/` (pure game logic), `tui.py`
  (Textual frontend), `main.py` (pre-flight picker), `tools/check_story.py`,
  `stories/`. Browser frontend in `web/`. Layout details: README,
  "Project layout".
- Repo: `derd1ngs/sidechannel` on GitHub; CI in `.github/workflows/`
  (`tests.yml`, `pages.yml`, `release.yml`).

## Resume here

1. `AGENTS.md` (this file): goal, conventions
2. `STATUS.md`: where things stand, what was last done, what's blocked
3. `PLAN.md`: open items, in order

## Document roles

Every file has one role. Each fact has one home; other files link to it
instead of repeating it.

| Role | Files | Rule |
|---|---|---|
| Deliverable | the code, stories, `README.md`, `docs/seven-hats/STORYLINE.md` (the series' story bible) | Current state only. No history, no to-dos, no "changed on …". |
| Decision | `DECISIONS.md` | Append-only log. Each entry: what was decided, why, alternatives. A changed decision gets a new entry that supersedes the old one. |
| Change | `CHANGELOG.md` + git commits | What changed, for a reader of the deliverable. |
| Work | `PLAN.md`, `PROPOSALS.md`, `STATUS.md` | Tasks and state. Never inside a deliverable. |
| Instructions | `AGENTS.md` (+ `CLAUDE.md` for Claude-only notes) | Lasting conventions. No status. |

## Proposals, then the plan

Changes nobody has decided on yet (review findings, ideas, follow-ups
noticed during a task) go into `PROPOSALS.md`, not straight into the plan
or the deliverable:

- One numbered entry per proposal (P1, P2, …): the problem (with file or
  section), the proposal, rough effort (S/M/L), and an empty `Decision:`
  line (yes / no / later / yes, but …). Alternatives as (a)/(b).
- Numbers stay stable while the file exists; new ones get the next number.
- After review: accepted entries move into `PLAN.md` as open items (with
  the reviewer's changes), rejected ones are dropped (record the rejection
  in `DECISIONS.md` if the reason is worth keeping), `later` ones stay.
  Delete `PROPOSALS.md` once it's empty.
- Don't implement a proposal before it is accepted. Something the owner
  asked for directly doesn't need this round trip.

## Reviews

`reviews/` holds review briefs. To run one: "follow
`reviews/<brief>.md`". Findings go into `PROPOSALS.md`.

## Setup

- A `.venv` created before the project directory was moved/renamed is broken
  (`.venv/bin/pytest: bad interpreter`, `No module named 'sidechannel'`
  outside the repo): it hardcodes its absolute path. `./setup.sh` detects
  this and recreates it; then `.venv/bin/pip install -e ".[test,lint]"` for
  the dev tools.
- The repo was renamed TerminalGames -> sidechannel (2026-09-27). On another
  machine's older checkout: `git remote set-url origin <url ending in
  sidechannel.git>` (GitHub redirects meanwhile), then `./setup.sh` to swap
  the old `sidechannel` command for `sidechannel`.

## Before calling a change done

- CI (`.github/workflows/tests.yml`) runs pytest plus `ruff check .`,
  `ruff format --check .` and `mypy sidechannel` -- run all four before
  calling a change done.
- Browser build: to check a change, run `python web/build.py`, then
  `python -m http.server -d _site 8765`, then `web/e2e/e2e.mjs` (see README;
  CI's `web-e2e` job runs the same script).

## PRs and CI

- `main` is branch-protected and requires PR branches to be up to date: when
  a PR is "BEHIND" (e.g. after merging the lower PR of a stack), run
  `gh api -X PUT repos/derd1ngs/sidechannel/pulls/<N>/update-branch`, wait
  for CI, then `gh pr merge <N> --merge`. That API call is refused (403, no
  `workflow` scope) when `main` changed a file under `.github/workflows/`:
  then `git merge origin/main` locally and `git push` instead, or for a
  Dependabot PR comment `@dependabot rebase`.
- `gh run view <run> --log` can come back empty; fetch a job's log via REST
  instead: `gh api repos/derd1ngs/sidechannel/actions/jobs/<job-id>/logs`
  (job ids: `gh api .../actions/runs/<run>/jobs -q '.jobs[] | .name, .id'`).

## Engine and packaging

- `sidechannel/engine/` and `web_bridge.py` must stay importable with only
  PyYAML (the browser build runs them in Pyodide) -- enforced by
  `tests/test_engine_is_ui_free.py`.
- When running Pyodide under Node, pass `unpackArchive` a
  `new Uint8Array(buf).buffer` -- a Node `Buffer` fails with "Unknown typed
  array type".
- The editable install from `setup.sh` hides packaging mistakes: any new
  non-`.py` file under `sidechannel/` (story YAML, data) must be listed in
  `[tool.setuptools.package-data]` in `pyproject.toml`, or a real install
  silently lacks it. CI's `package` job (wheel -> clean venv -> run outside
  the repo) catches this.
- A new shell command (`@command` in `engine/shell.py`) needs a `MANUAL`
  entry (a test enforces it) and, if it touches a host, a place in
  `TRACED_COMMANDS` -- otherwise it slips past scenes' trace meters. Adding a
  command can also change completion results that tests pin.
- Saves are versioned (`SAVE_VERSION` in `engine/state.py`, see D6 in
  `DECISIONS.md`). A new GameState field with a default needs nothing; any
  change `from_dict`'s defaults can't absorb (a renamed or restructured
  field) must bump `SAVE_VERSION` and add a `_MIGRATIONS` step, with a test
  that loads an old-shaped save.

## Tests and screenshots

- TUI tests: `App.run_test()` defaults to an 80x24 screen, so modals and
  forms must fit it (a click outside raises `OutOfBounds`). A pane that a
  scene change hid renders no lines, so assert on recorded
  `log_terminal`/`log_text` calls rather than reading that pane.
- To look at the TUI: `app.save_screenshot(filename=..., path=...)` inside
  `run_test(size=(80, 24))` writes an SVG; Playwright's Firefox can open it
  via `file://` and screenshot it to PNG.
- Offline e2e in Playwright's Firefox: `context.setOffline(true)` is
  unusable -- Firefox either serves its HTTP cache (the test passes even with
  a broken service worker) or refuses the reload (`NS_ERROR_OFFLINE`). Cut
  the network with `context.route("**/*", r => r.abort())` instead: routing
  also disables the HTTP cache, so only the service worker can serve.
- Favicons: `web/favicon.svg` is the source; the PNGs come from
  `web/e2e/make-icons.mjs` (rasterized through an in-page canvas -- this
  Playwright Firefox can't take transparent or SVG-element screenshots:
  "Not implemented").

## Names and releases

- Names: the game is "Side Channel" -- PyPI distribution, command, GitHub
  repo and import package are all `sidechannel` (site:
  derd1ngs.github.io/sidechannel/; the package was `terminalgames` until
  after 1.0.0). Exported browser saves keep the format tag
  `terminalgames-save` so older exports still import (D3, D4).
- The version lives only in `sidechannel/__init__.py` (pyproject reads it
  dynamically); a release is a `vX.Y.Z` tag matching it
  (`.github/workflows/release.yml` checks that). Build locally with
  `build`/`twine` in a scratch venv, never the project venv.
- New or revised stories don't change the game's version number (D7):
  release only for engine or player-facing code changes, and log story
  changes in the changelog's "Stories" section.

## Local environment (kompjuda)

Quirks of one machine (Ubuntu 24.04), needed by any agent working there:

- `gh pr edit` and `gh pr view` fail with gh 2.45 ("Projects (classic) is
  being deprecated"). Change a PR's base with
  `gh api -X PATCH repos/derd1ngs/sidechannel/pulls/<N> -f base=main`; read
  a PR with `gh api repos/derd1ngs/sidechannel/pulls/<N> -q '.state,
  .mergeable_state'`.
- That gh also has no `--json` on `gh pr checks`, and its tab-separated
  output breaks `awk '{print $2}'` on names like `test (3.10)`: read results
  with `gh pr checks <N> | cut -f1,2`.
- There's no Chrome, so the browser e2e and screenshots use Playwright's
  Firefox.
- The remote must be `git@ghderd1ngs:derd1ngs/sidechannel.git`: the
  `ghderd1ngs` host in `~/.ssh/config` uses the `derd1ngs` key. Plain
  `git@github.com:` (what `gh repo clone` sets) logs in as `treihs`, and
  pushes are denied. Check with `ssh -T git@ghderd1ngs` → "Hi derd1ngs!".

## End of a work session

1. `STATUS.md`: what was done, where things stand, what's next or blocked.
2. `PLAN.md`: strike through finished items (with date and commit).
3. `DECISIONS.md`: add an entry for every decision made (including
   accepted or rejected proposals that matter later).
   `CHANGELOG.md`: add an entry if something a reader would notice changed.
4. Check that no to-dos or status notes leaked into deliverables.
5. Commit.
