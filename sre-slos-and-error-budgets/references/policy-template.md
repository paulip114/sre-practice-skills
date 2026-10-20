# Error budget policy template

```markdown
# <Service> Error Budget Policy

| | |
|---|---|
| Authors | |
| Reviewers | |
| Approvers | Product owner, Dev lead, SRE/Ops lead |
| Approved on | YYYY-MM-DD |
| Next review | YYYY-MM-DD |

## Service overview
One paragraph of context. Link the SLO document.

## Goals
- Protect users from repeated SLO misses.
- Give the team an explicit incentive to balance reliability with feature work.

## Non-goals
- Punishing teams for missing SLOs.
- Driving errors to zero; the budget exists to be spent on change.

## SLO miss policy
If the service has exceeded its error budget over the preceding <window>:
- All changes and releases stop except: <P0 bug fixes, security fixes, changes that improve reliability>.
- Reliability work takes priority over feature work until the service is back within SLO
  and <exit criteria>.
- <Optional: the whole team works on reliability until exit criteria are met.>

Causes that trigger the freeze:
- A bug or procedural error in this service.
- <Decide:> failure of a dependency owned by another team → [freeze anyway | no freeze; escalate].
- Errors later found to have been miscategorized.

Causes that do not trigger the freeze:
- <e.g. company-wide infrastructure outage that has its own postmortem>
- <e.g. load beyond the published capacity contract>

## Outage policy
- Any single incident consuming more than <20>% of the window's budget → postmortem with at
  least one top-priority action item addressing the root cause.
- Any single class of outage consuming more than <20>% of budget over a quarter → a planned
  project in the next quarter's plan.

## Escalation
Disagreements about the calculation or the actions go to <named role>, who decides.

## Background (optional)
Short explanation of SLOs and error budgets for readers new to them.
```
