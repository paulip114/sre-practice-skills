# SLO document template

```markdown
# <Service> SLO

| | |
|---|---|
| Status | Draft / Approved |
| Authors | |
| Reviewers (technical accuracy) | |
| Approvers (business decision) | |
| Approved on | YYYY-MM-DD |
| Next review | YYYY-MM-DD (monthly while new, then quarterly) |

## Service overview
Two or three sentences: what it does, who the users are, main dependencies.

## SLIs and SLOs

| Category | SLI specification | SLI implementation (source, query) | SLO | Window |
|---|---|---|---|---|
| Availability | | | 99.x% | 4w rolling |
| Latency | % of requests < T1 | | 90% | 4w rolling |
| Latency | % of requests < T2 | | 99% | 4w rolling |

Known blind spots of each implementation: …

## Rationale
Where the numbers came from (observed baseline, user research, business need, or ad hoc —
say so explicitly if ad hoc).

## Error budget
- Budget = 1 − SLO, measured over the window above.
- Expected volume: ~N events per window → ~X allowed bad events.
- What counts against the budget (incl. dependency failures? planned maintenance?).
- Link to the error budget policy.

## Clarifications and caveats
- Which requests are excluded as invalid, and why.
- Aspirational SLOs that are tracked but not enforced.
```
