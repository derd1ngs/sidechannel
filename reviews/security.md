# Review brief: security

**Purpose:** Can someone misuse this project, or does it leak anything it
shouldn't?

**Scope:** Code, configuration, scripts, CI files and dependency
manifests. Out of scope: hosting and infrastructure outside the repo,
unless the repo configures it.

**Steps:**
1. Secrets: keys, tokens, passwords or private URLs in the code, config,
   history (`git log -p` for removed ones) or example files.
2. Authentication and authorization: who can do what, and is it checked
   on every path, not just the obvious one?
3. Input handling: every place outside input enters (user input, files,
   network, environment). Look for injection (shell, SQL, HTML, path),
   missing validation and unsafe deserialization.
4. Dependencies: outdated or unmaintained packages, unpinned versions,
   anything fetched at runtime.
5. Logging and data: personal data or secrets written to logs, error
   messages or analytics.

**Output:** see `README.md`.
