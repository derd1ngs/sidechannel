# Changelog

Changes a player or story author would notice. Newest first. Format based
on [Keep a Changelog](https://keepachangelog.com/). Append-only: correct an
old entry with a new one. Decisions and their reasons go in `DECISIONS.md`;
link to an entry (`D3`) where a change carries one out. Story releases go
under a "Stories" heading, not under a game version (D7).

## Unreleased

- New `look` command: shows the current scene's text again. Continuing a
  save starts with a short "Previously:" recap of your latest journal
  entries.
- Error messages say what to do next: an unknown story name suggests the
  closest match and `sidechannel --list`; a failed browser start says to
  check the connection (or that the browser lacks WebAssembly); an
  unexpected error during play says the game is saved up to the last scene
  change and to reload.
- Terminal launcher: `q` quits the story and slot pickers, and Ctrl+C or
  Ctrl+D at a prompt exits quietly instead of printing a Python traceback.
- Autosave on every scene change, not just at a new chapter: closing the
  browser tab or a crash costs at most the current scene (D17). The browser
  also asks to keep its saves (persistent storage) when a new game starts,
  and suggests exporting if it refuses.
- Browser: the Python runtime (Pyodide) is now served by the game's own site,
  checked against its published hash at build time, and a
  Content-Security-Policy keeps the page from loading anything else. The page
  no longer contacts a CDN (D17).
- Terminal: new save slots follow the browser's naming rule (letters,
  digits, `_` and `-`); a name like `../x` or `a/b` is refused instead of
  writing outside the saves folder. Existing slots keep working.
- Story files are checked for names that would leave the save folder: the
  story id, host ids, file names, NPC and topic ids may only use letters,
  digits, `_`, `-` and `.`. `check_story` reports any that don't, instead of
  crashing on a broken `network.yaml` or `npcs.yaml`.
- Draft stories: `draft: true` in a manifest keeps a story out of the story
  lists while it's being written. Authors can still launch it directly, or
  list drafts in the browser with `?drafts=1`. A test keeps `TODO(author)`
  placeholders out of published stories.
- Stories can belong to a series: manifests take `series`, `part` and `hat`,
  and the story list shows e.g. "The Seven Hats · Part 1 · Black Hat".
  Manifests also take a per-story `version`, since new or revised stories
  don't change the game's version.
- Saves carry a format version (`save_version`), so future versions can
  migrate them. A save from a newer version of the game is refused with a
  clear "update the game" message instead of misbehaving.
- Reaching an ending saves the slot, so it shows the finished run rather than
  an earlier save.
- Story lists show each story's publishing date, a one-line description,
  its size and the endings you've found, newest first. The browser pages
  them six at a time, and the terminal picker nine at a time (`n`/`p`), with
  titles instead of folder names. Story manifests take optional `published`
  and `description` fields.

## 1.0.1 -- 2026-09-27

- The browser version has a favicon: a green prompt and an amber cursor
  (SVG, plus PNGs for older browsers and iOS home screens).
- The Python package is now `sidechannel`, matching the game's name. It was
  `terminalgames`, the project's original name. The `sidechannel` command is
  unchanged, and save files exported from the browser still import.

## 1.0.0 -- 2026-09-27

First release, on PyPI as `sidechannel`: the game is now called **Side
Channel** (it started out as "TerminalGames"). Everything below is new since
the 0.1.0 prototype.

### Stories
- **Zero Day** (3 chapters, 6 endings): the in-fiction tutorial.
- **Dead Drop** (1 chapter, 4 endings): pipes, `ssh`, a runbook puzzle.
- **Night Shift** (1 chapter, 4 endings): hidden files, tool grants and a
  trace meter.
- Every puzzle scene has progressively revealed `hint`s.

### Playing
- A browser version with nothing to install
  (https://derd1ngs.github.io/sidechannel/). It runs the same Python engine
  in Pyodide, works offline after the first visit, has on-screen Tab and
  history buttons on phones, and can export and import save files.
- The terminal version is a full-screen Textual app with Tab completion,
  command history, Ctrl+S, and a `mail compose` form.
- An endings gallery per story, across all save slots.
- Shell: `ssh` logins, pipes into `grep`, `head`/`tail`, `find`, `ls -a`,
  `history`, `clear`, `man`, `status`, `journal <category>`, `hint`.

### Story authoring
- New story features:
  - `requires` combinators (`all`/`any`/`not`);
  - `tool.<id>` grants;
  - `ordered_commands` procedure puzzles;
  - trace meters (`trace: {limit, on_trace}`);
  - per-scene `hints`.
- Strict loading: typos and invalid values in any story file are errors,
  with a did-you-mean hint.
- `check_story` checks every scene and ending is reachable, lints
  references across files, and exports the scene graph as Mermaid
  (`--graph`).

### Fixes
- Installed copies (not just checkouts) now ship the stories and save to
  the user data directory.
- A save whose scene was removed by a story edit now offers a restart
  instead of crashing.
