---
name: sre-postmortem
description: Use when writing, reviewing or improving a blameless postmortem — structuring the document, quantifying impact, separating trigger from root causes, writing concrete action items, removing blameful language, or building postmortem culture and follow-up tracking. Based on Google SRE practice.
---

# Blameless Postmortems

A postmortem is a written record of an incident: its impact, what was done, its root causes and contributing factors, and the follow-up that prevents recurrence. Its value is proportional to what people learn from it and what changes because of it.

## When one is required

Agree triggers in advance. Typical:
- User-visible downtime or degradation beyond a threshold.
- Data loss of any kind.
- On-call intervention such as a rollback or traffic reroute.
- Resolution time above a threshold.
- Monitoring failure (humans found it, not alerts).
- A single incident consuming a large share of error budget (per `sre-slos-and-error-budgets`).
- Anyone may request one for any event.

## Blamelessness

Assume everyone acted reasonably with the information and tools they had. Focus on **what** in the system allowed the failure, not **who**.

- Don't name individuals as the cause; describe the action and the conditions that made it possible ("the workflow was rerun manually; the tool had no guard against repeat execution").
- No loaded or emotional language ("careless", "ridiculous", "can't believe we survived"). Replace adjectives with data.
- Action items fix systems and processes, not people. "Train people to be more careful" is not a fix; a guard rail is.
- If leadership slips into blame, redirect to "what warning signs existed and why were they missed?"

## Procedure

1. **Assign one owner** (plus collaborators) as soon as the incident closes. Include everyone who participated in writing it.
2. **Pull the facts** from the incident state doc, chat logs, graphs, deploy history. Build the timeline in UTC.
3. **Quantify impact** with numbers: duration, affected users/requests/% of traffic, latency, revenue/budget impact, team cost. An estimate with its method stated beats no number.
4. **Analyse causes.** Separate the **trigger** (what set it off) from **root causes and contributing factors** (latent conditions that let the trigger cause damage — missing validation, no rate limit, unsafe default, monitoring gap). Keep asking why until you reach things you can change. Expect several contributing causes.
5. **Lessons learned**: what went well, what went poorly, where we got lucky (luck marks a hidden risk).
6. **Action items** — see criteria below. Group them by theme for large incidents.
7. **Review** with the checklist below; senior engineers review high-impact postmortems.
8. **Publish within about a week**, widely by default (whole engineering org; customers when appropriate). Delay lets memory fade and lets others fill the silence.
9. **Track action items to closure** in the normal bug tracker and review completion rates.

Template: `references/postmortem-template.md`.

## Action item criteria

Each action item must have:
- **One owner** and a **tracking ticket**.
- A **priority** — not all the same. At least one top-priority item for any user-affecting outage.
- A **verifiable end state**: "Alert when > X% of machines leave the pool within 10 min", not "improve alerting".
- A **type**, with a balance across types — not only mitigations:
  - *Prevent* — stop this class from happening (input validation, safety checks, idempotency).
  - *Mitigate* — reduce blast radius or duration (rate limits, kill switch, smaller rollouts).
  - *Detect* — find it sooner (new alert, probe).
  - *Repair / Investigate / Process* as needed.

## Review checklist

- [ ] Readable by someone outside the team (background + glossary for jargon)?
- [ ] Impact quantified, with sources linked?
- [ ] Trigger and root causes both identified, at sufficient depth?
- [ ] Timeline complete, with detection and mitigation times?
- [ ] Action items meet the criteria above, vetted by the service's tech lead?
- [ ] Blameless language throughout?
- [ ] Single owner, status, dates, sharing list filled in?
- [ ] Shared beyond the team?

## Building the culture

- Reward closing action items, not just writing documents.
- Celebrate good postmortems (reading clubs, weekly outage summaries, cross-team reviews).
- Use past postmortems for training (re-enact them as role-play drills).
- Add machine-readable metadata (services, trigger type, detection method, durations) so trends can be analysed across postmortems.
- Warning signs: people avoid being "involved", postmortems are late or shallow, the same incident recurs (are action items closing? is velocity trumping fixes?).

## Sources

- SRE book ch. 15 Postmortem Culture — https://sre.google/sre-book/postmortem-culture/
- SRE book Appendix D Example Postmortem — https://sre.google/sre-book/example-postmortem/
- SRE book ch. 16 Tracking Outages — https://sre.google/sre-book/tracking-outages/
- Workbook ch. 10 Postmortem Culture — https://sre.google/workbook/postmortem-culture/
- Workbook Appendix C Results of Postmortem Analysis — https://sre.google/workbook/postmortem-analysis/
