# Agent operating manual — map, not encyclopedia (~100 lines max)

## Read first (in order)
1. `feature_list.json` — pick ONE unfinished feature
2. `claude-progress.md` — last session handoff
3. `docs/ARCHITECTURE.md` — where code lives
4. Run `./init.sh` before any edits

## Scope rules
- Work on **one feature** until `passes: true` in feature_list
- Do not rewrite the feature list to hide unfinished work
- Do not declare done without verification evidence

## Verification (required before "done")
```bash
npm test && npm run lint && npm run typecheck
```
All must exit 0. Paste summary in progress log.

## Session wrap-up
- Update `claude-progress.md` (what changed, what's broken)
- Update `feature_list.json` only with evidence
- Commit when safe to resume next session

## Progressive disclosure
Deep docs live under `docs/` — read on demand, not all at startup.
