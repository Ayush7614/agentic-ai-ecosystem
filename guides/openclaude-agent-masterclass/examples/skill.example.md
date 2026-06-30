---
name: repo-smoke-test
description: Run lint and tests before claiming a task is done
maxSteps: 12
---

When finishing a coding task, always run the project's test and lint commands.
Report stdout. Do not declare success until both pass.
