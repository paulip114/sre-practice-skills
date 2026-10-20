# Postmortem template

```markdown
# Postmortem: <title describing what happened, not who>

| | |
|---|---|
| Incident date | YYYY-MM-DD HH:MM–HH:MM UTC |
| Owner | <one person> |
| Collaborators | |
| Status | Draft / In review / Final |
| Shared with | <default: all engineering> |
| Published | YYYY-MM-DD |
| Incident doc | <link> |

## Executive summary
**Impact:** one or two sentences with numbers.
**Root cause:** one or two sentences, systemic, blameless.

## Impact
- Duration (user-visible):
- Users / requests / % traffic affected:
- Latency or quality degradation:
- Data loss (if any):
- Error budget consumed:
- Revenue / customer / support impact:
- Team cost (people-hours, pages):
Explain how each number was estimated; link the source graphs/queries.

## Detection
How was it detected (alert, customer report, engineer noticed)? Time from start to detection.

## Background and glossary (optional)
Context and terms needed by readers outside the team.

## Trigger
What change or event set it off.

## Root causes and contributing factors
Latent conditions that allowed the trigger to cause this impact. Expect several.

## Resolution and recovery
What was done to mitigate and recover, and why it worked. Time to mitigate.

## Timeline (UTC)
| Time | Event |
|---|---|

## Lessons learned
### What went well
### What went poorly
### Where we got lucky

## Action items
| Action item | Type (prevent/mitigate/detect/repair/investigate/process) | Priority | Owner | Ticket |
|---|---|---|---|---|

## Supporting material
Graphs, log excerpts, chat log links.
```
