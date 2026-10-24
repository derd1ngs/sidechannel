# Decisions

Decision log: what was decided, why, and what else was considered.
Append-only, newest at the bottom, numbers never reused. To change a
decision, add a new entry that supersedes the old one, and add
"Superseded by Dn" to the old entry's status line. Never rewrite an old
entry's text.

Where an entry came from a proposal, name it (e.g. "was P4").

D1–D15 were backfilled on 2026-10-24 from `docs/ENHANCEMENT_PLAN.md`,
`docs/seven-hats/STORYLINE.md`, `CLAUDE.md` and the git history; their
dates are when the decision first appears in git.

---

## D1 — Skip the `textual serve` preview, go straight to a static browser version

**Date:** 2026-09-26 · **Status:** active

**Context:** Two ways to play in a browser: serve the existing TUI through
`textual-serve` (old Phase 2), or a static site on GitHub Pages running the
engine in Pyodide (old Phase 3).

**Decision:** Phase 2 was skipped; Phase 3 was built.

**Why:** The `textual serve` route needs a running Python process per
visitor, isn't suitable for public hosting, and two tabs on one save slot
clobber each other.

**Alternatives considered:** `textual serve` as a LAN-only preview first.

---

## D2 — Save download/import after the browser version, not with it

**Date:** 2026-09-26 · **Status:** active

**Context:** The browser version stores saves per browser.

**Decision:** Exporting and importing save files shipped as a follow-up to
the browser version.

**Why:** Reason not recorded.

**Alternatives considered:** None recorded.

---

## D3 — Exported browser saves keep the `terminalgames-save` format tag

**Date:** 2026-09-26 · **Status:** active

**Context:** The project was renamed from TerminalGames to Side Channel
(D4).

**Decision:** The format tag in exported save files stays
`terminalgames-save`.

**Why:** Older exports still import.

**Alternatives considered:** None recorded.

---

## D4 — The game is called Side Channel; everything is `sidechannel`

**Date:** 2026-09-27 · **Status:** active

**Context:** Publishing to PyPI as `terminalgames` clashed with the
existing `terminal-games` project.

**Decision:** The game is "Side Channel". The PyPI distribution, command,
GitHub repo and (from 1.0.1) the import package are `sidechannel`; the
site is `derd1ngs.github.io/sidechannel/`.

**Why:** The owner chose a distinct name over a suffixed one.

**Alternatives considered:** Keeping the name with a suffix.

---

## D5 — License GPL-3.0-or-later

**Date:** 2026-09-27 · **Status:** active

**Context:** Needed for the PyPI release.

**Decision:** `GPL-3.0-or-later`.

**Why:** The owner's decision; reason not recorded.

**Alternatives considered:** None recorded.

---

## D6 — Saves carry a format version; a newer save is refused

**Date:** 2026-09-27 · **Status:** active

**Context:** Save files had no version, so a format change would break old
saves silently.

**Decision:** Saves carry `save_version`, older ones are migrated
(`_MIGRATIONS`), and a save from a newer game is refused with an "update
the game" message.

**Why:** Future versions can migrate saves, and an older game never
misreads or overwrites a newer save.

**Alternatives considered:** None recorded.

---

## D7 — New or revised stories don't change the game's version

**Date:** 2026-09-27 · **Status:** active

**Context:** Stories are released one at a time (D12).

**Decision:** Bump `__version__` and tag a release only for engine or
player-facing code changes. Each story carries its own `version` in its
manifest, and story changes are logged in the changelog's "Stories"
section, not under a game version. Stories go live in the browser on
merge; installed copies get them with the next game release, or through
story delivery once that exists (`PLAN.md`).

**Why:** Story releases are independent of the engine.

**Alternatives considered:** A game release per story.

---

## D8 — The Seven Hats is one shared scenario

**Date:** 2026-09-27 · **Status:** active

**Context:** A series of seven stories, one per hacker "hat".

**Decision:** One long scenario (the Brackwater/TrackNet incident) in
which the hats join at different times; each story still stands alone.

**Why:** Reason not recorded beyond the "one incident, seven points of
view" concept.

**Alternatives considered:** Seven independent stories.

---

## D9 — The black hat is in the series, and starts long before the others

**Date:** 2026-09-27 · **Status:** active

**Context:** Whether to include an attacker's point of view.

**Decision:** Yes: Vesper is hired on day -120, with an audition job and
months of research before the others appear. Unauthorized hats always
meet consequences (`docs/seven-hats/STORYLINE.md`, content guidelines).

**Why:** Reason not recorded.

**Alternatives considered:** Leaving the black hat out.

---

## D10 — Release order C: the attacker first

**Date:** 2026-09-27 · **Status:** active

**Context:** Which hat's story comes out first.

**Decision:** Part 1 Black, then Blue, White, Gray, Green, Red, and
Purple last. Part numbers follow the release order.

**Why:** The attacker's story first, then "the other side of the story" in
the order its characters enter. Purple is last because its epilogue closes
the series.

**Alternatives considered:** Blue + White first (the authorized pair, the
original suggestion).

---

## D11 — The company is Brackwater Terminals

**Date:** 2026-09-27 · **Status:** active

**Context:** The first draft's company was "Meridian Freight".

**Decision:** Brackwater Terminals. All other names stay.

**Why:** "Meridian Freight" is a real company. Names are checked against
real companies before use.

**Alternatives considered:** None recorded.

---

## D12 — Each Seven Hats story is released separately

**Date:** 2026-09-27 · **Status:** active

**Context:** Release the series at once or story by story.

**Decision:** Each story is released on its own.

**Why:** Reason not recorded.

**Alternatives considered:** Releasing the series together.

---

## D13 — Vesper's three endings, with a cliffhanger

**Date:** 2026-09-27 · **Status:** active

**Context:** How Part 1 ends.

**Decision:** Three endings: caught, escaped, and an unclear cliffhanger.

**Why:** The cliffhanger is kept as a hook for a sequel ("The Seven Hats
II").

**Alternatives considered:** None recorded.

---

## D14 — Story search/filter waits until there are many stories

**Date:** 2026-09-27 · **Status:** active

**Context:** Story cards and pagination were built (old Phase 10).

**Decision:** A search/filter box is deferred.

**Why:** It only matters once there are many stories.

**Alternatives considered:** Building it with the story cards.

---

## D15 — The owner writes Part 1's text

**Date:** 2026-09-27 · **Status:** active

**Context:** Writing The Seven Hats Part 1 (the black hat's story).

**Decision:** The owner writes that story's text. Claude handles the
engine, validation (`check_story`), tests and publishing, and can write
the other hats' stories. Unfinished stories use `draft: true`.

**Why:** Claude's attempts to write its content, even a placeholder
skeleton, were repeatedly stopped by a safety check.

**Alternatives considered:** None recorded.

---

## D16 — Adopt the document roles layout

**Date:** 2026-10-24 · **Status:** active

**Context:** Instructions sat in a file only Claude reads, and the
enhancement plan mixed plan, history, status and decisions. (was P1–P7)

**Decision:** Tool-neutral instructions in `AGENTS.md` (`CLAUDE.md` =
`@AGENTS.md` + Claude-only notes, machine-specific notes in `AGENTS.md`
under "Local environment"); decisions here; open work in `PLAN.md`; status
in `STATUS.md`; `docs/ENHANCEMENT_PLAN.md` removed, its done phases
deleted rather than archived (`CHANGELOG.md` and git hold them);
`STORYLINE.md` is the story bible only; review briefs in `reviews/`.

**Why:** Any model or person can resume from `AGENTS.md` → `STATUS.md` →
`PLAN.md`, and each fact has one home.

**Alternatives considered:** Machine notes in claude-dotfiles' Claude-only
machine file (P1 b); an archive copy of the done phases (P3 b).

---

## D17 — Review fixes go first; self-hosted Pyodide; autosave per scene

**Date:** 2026-10-24 · **Status:** active

**Context:** Security and user-view review (was P1–P12), all accepted.

**Decision:** The twelve fixes come first in `PLAN.md`, ahead of the
series. Pyodide is self-hosted on Pages, pinned and hash-checked at build
time (was P4 a). Progress is saved on every scene change, in both
frontends (was P6 a).

**Why:** The owner asked for security and UX first. Self-hosting removes
the third-party runtime fetch entirely instead of checking it. A save per
scene change covers lost tabs and killed phone tabs at the cost of one
small JSON write.

**Alternatives considered:** Keep the CDN with an integrity-checked
import map and hash checks in the service worker (P4 b); also saving on
`visibilitychange`/`pagehide` for progress within a scene (P6 b).
