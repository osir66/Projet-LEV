---
name: feedback-modification-scope
description: User wants targeted changes, not broad rewrites — ask before modifying multiple things at once
metadata:
  type: feedback
---

Prefer small, surgical changes over broad rewrites. When the user asks to add something, add it — don't also refactor surrounding code or remove things that seem unused.

**Why:** User explicitly said "je ne suis pas fan que tu modifies tout comme ça" after I rewrote the count functions and removed an import without being asked.

**How to apply:** If the task is "add function X", only add function X. Don't clean up nearby code, remove imports, or rename things unless explicitly asked.
