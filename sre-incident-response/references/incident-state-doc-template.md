# Live incident state document

Keep the top section current; append to the log below. Times in UTC.

```markdown
# Incident: <short title>   [ACTIVE | MITIGATED | RESOLVED]

**Summary (2–3 lines, always current):**
What is broken, who is affected, current status of mitigation.

| | |
|---|---|
| Declared | YYYY-MM-DD HH:MM UTC by <name> |
| Severity | |
| Incident Commander | <name> (since HH:MM) |
| Ops Lead | |
| Comms Lead | |
| Planning | |
| Channel / bridge | <link> |
| Next status update due | HH:MM UTC |

## Impact
- Users/services affected:
- Start time (first bad signal):
- Scope (regions, % of traffic, customers):
- Error budget consumed so far (approx):

## Current hypotheses
| Hypothesis | Evidence for | Evidence against | Owner | Status |
|---|---|---|---|---|

## Ruled out
- …

## Mitigations / changes made to production
| Time | Who | Change | Result | Needs revert later? |
|---|---|---|---|---|

## Open action items during incident
- [ ] <task> — owner

## Status updates sent
- HH:MM — to <audience> — <one line>

## Timeline (append-only)
- HH:MM — <event / observation / decision>

## Handoffs
- HH:MM — IC <old> → <new>, acknowledged.
```
