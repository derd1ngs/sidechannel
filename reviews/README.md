# Review briefs

A brief tells any reviewer (a person or any AI model) how to review this
project from one perspective. Run one with: "follow `reviews/<brief>.md`".

## Brief format

Each brief has these sections:

- **Purpose:** the one question this review answers.
- **Scope:** which files or parts to look at, and what's out of scope.
- **Steps:** what to check, in order.
- **Output:** always the same (below).

## Output (all briefs)

- Findings go into `PROPOSALS.md` as new numbered entries, in that file's
  format (problem with file/section, proposal, effort S/M/L, empty
  `Decision:`).
- Start the batch with one line: brief name, date, reviewer (for an AI:
  the model name).
- Only verified findings. Mark anything uncertain as such.
- No changes to the project itself. The review only proposes.
