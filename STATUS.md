# Status

<!-- Overwritten at the end of every work session. Current state only: the
history lives in CHANGELOG.md and git. -->

**As of:** 2026-10-24

## Where things stand

Side Channel 1.0.1 (2026-09-27) is the latest release, on PyPI and in the
browser. `main` has unreleased engine work since then (see `CHANGELOG.md`,
Unreleased), including the twelve security/UX review fixes (`PLAN.md`
items 1–12, D17; PR #53, merged 2026-10-24). The Seven Hats storyline is
agreed (`docs/seven-hats/STORYLINE.md`); no story of the series is written
yet.

## Last session

- Security and user-view review (`reviews/security.md`,
  `reviews/user_view.md`): P1–P12, all accepted, moved to `PLAN.md`
  items 1–12, done and merged (#53). Highlights: story and save names
  can't leave the sandbox, Pyodide self-hosted with a CSP, autosave on every
  scene change, `look`, screen reader fixes, pinned CI tools, real
  dependency floors.
- All four local checks, `check_story --all` and the browser e2e pass.

## Next

- Part 1 of The Seven Hats (`PLAN.md` item 15): the owner writes it.
- After that, a release: the unreleased changes include player-facing
  fixes and new dependency floors.

## Blocked / waiting on

- Part 1's text: waiting on the owner (D15).
- A screen reader check of the browser game (Orca) — not done yet.
- Dependabot PR #49 (Playwright 1.63.0 → 1.64.1), open since 2026-10-20.
