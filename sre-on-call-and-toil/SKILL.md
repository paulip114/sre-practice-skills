---
name: sre-on-call-and-toil
description: Use when designing on-call rotations and operational workload (page limits, interrupts, onboarding, team overload), measuring and eliminating toil with safe automation, or starting and growing an SRE practice in an organization. Based on Google SRE practice.
---

# On-Call, Toil and SRE Teams

Keep operational work bounded and shrinking so engineers spend most of their time on engineering, and build the team practices that sustain that.

## Sustainable On-Call and Operational Load

On-call works when pages are rare, meaningful and manageable, and the rest of the team's time goes to engineering that makes pages rarer.

### Targets to aim for

- **Ops work ≤ 50%** of the team's time (on-call, tickets, toil, manual operations). The rest is engineering. When ops exceeds this, redirect the overflow to the development team or pause launches until it's back under control.
- **On-call ≤ 25%** of any individual's time, which implies a rotation of roughly **8 people at one site, or 6 per site across two sites** for 24/7 primary + secondary coverage.
- **At most ~2 incidents per 12-hour shift** on average. Each real incident (handling, cleanup, postmortem) takes hours; more than that and quality drops. Zero for long stretches means skills atrophy — run drills.
- **Response time matches the SLO**: a tight SLO needs minutes-level acknowledgment; a loose one can tolerate longer.
- Multi-site rotations ("follow the sun") avoid night shifts but add handoff and communication cost.
- Compensate out-of-hours on-call (time off or pay) and cap it so it stays bounded.

### Rotation design checklist

- [ ] Primary and secondary, with clear rules for when secondary takes over.
- [ ] Escalation paths to developer on-call and dependency teams.
- [ ] Explicit handoff at shift change (open issues, ongoing incidents, risky pushes).
- [ ] Playbooks/runbooks linked from every alert.
- [ ] Every page reviewed weekly: was it actionable? duplicated? fixable by automation?
- [ ] Metrics tracked: pages/shift, incidents/shift, time-to-ack, out-of-hours pages, % pages with no action taken.

### Psychological safety under pressure

Stress pushes people toward fast, intuitive, unverified action. Counter it with: clear escalation (asking for help is expected, not a failure), written procedures, and a culture where on-callers are trusted to act and not blamed for reasonable decisions.

### Interrupts: separate them from project work

Interrupts include pages, tickets, and ongoing operational responsibilities (rollouts, flag changes, requests from other teams). Context switching destroys focus, so:

- **Assign one person to own interrupts** for the shift (tickets as well as pages), and protect everyone else's project time.
- The interrupt-holder does no project work that week; they work on reducing interrupts (fixing the causes of tickets, writing automation, improving docs).
- Hand over explicitly between interrupt-holders.
- If ticket volume needs more than one person, add a second dedicated person rather than spreading interrupts across the team.
- Review tickets regularly: recurring types are toil to eliminate (*Toil Reduction and Automation* below).

### Onboarding new on-callers

- Learn the system by layers: request path, then dependencies, then failure modes. Use past postmortems as reading.
- **Shadow** on-call, then **reverse-shadow** (newcomer leads, experienced person backs up).
- Run **"Wheel of Misfortune"** role-plays: a game master replays a past incident, the trainee responds using real tools/dashboards, then the team debriefs.
- Have trainees improve playbooks and dashboards as they learn — fresh eyes find gaps.
- Use checklists of knowledge areas; certify readiness explicitly before joining the rotation.

### Recovering from operational overload

Signs: constant firefighting, pages ignored, postmortems without follow-up, team morale low, ops > 50%. Overload can also be *perceived* — sudden changes in scope, unclear priorities or loss of autonomy can make a team feel overloaded even when measured load is moderate. Measure the load (tickets, pages, toil hours) and also ask the team; fix both the workload and the sources of uncertainty (clear priorities, explicit ownership, saying no to unplanned work).

Approach (often with an experienced SRE embedded for a few weeks):
1. **Learn the service and its context**; identify the biggest sources of stress (top pages, top ticket types, riskiest manual procedures).
2. **Stop the bleeding by fixing what's on fire**, but focus on reducing future work, not just doing today's.
3. **Introduce SLOs and an error budget policy** so reliability vs. velocity becomes a data-driven conversation (`sre-slos-and-error-budgets`).
4. Ensure **postmortems** are written and action items done.
5. **Rank toil and automate** the top items.
6. Leave behind written practices (on-call review, ticket review, postmortem process) so the team keeps improving.

## Toil Reduction and Automation

### What toil is

Toil is operational work that is:
- **Manual** — a human runs it.
- **Repetitive** — done again and again.
- **Automatable** — a machine could do it (or the need could be designed away).
- **Tactical** — interrupt-driven, reactive.
- **No enduring value** — the service is no better afterwards.
- **Scales with the service** — grows linearly with users, traffic or instances.

Not toil: overhead (meetings, HR), and engineering work that has lasting value, even if it's tedious. Some toil is unavoidable and even fine in small amounts; the problem is when it grows unchecked and crowds out engineering.

**Budget:** keep toil (plus other ops work) under ~50% of team time — see *Targets to aim for* above.

### Procedure

1. **Identify.** Sources: tickets by type, pages that needed a manual fix, runbook steps, requests from other teams, recurring calendar tasks, release/deploy steps. Ask the people doing it — they know.
2. **Measure.** For each item: frequency, time per occurrence, number of people involved, error rate when done manually, growth rate. Track total toil hours per week as a team metric. Short surveys or ticket-time tags are enough to start.
3. **Prioritize** by cost now × growth, risk of human error, and morale impact. Also weigh the engineering cost of the fix. Favor items that scale with growth.
4. **Choose the strongest remedy** (in order of preference):
   - **Eliminate** the need: change the system so the work disappears (e.g. self-healing, fix the bug that causes the ticket).
   - **Self-service**: let requesters do it safely themselves via a tool or API.
   - **Automate** end-to-end.
   - **Partially automate**: scripts that do the steps but still need a human to start or confirm.
   - **Document** a clear runbook (only as a stepping stone).
5. **Roll out incrementally** and measure toil before/after. Retire the old manual path.
6. **Re-evaluate** quarterly; new toil appears as systems grow.

### Automation maturity ladder

1. No automation — manual everything.
2. Externally maintained, system-specific scripts (one person's laptop).
3. Externally maintained, generic automation shared by the team.
4. Internally maintained, system-specific automation shipped with the service.
5. **Autonomous systems** that need no human intervention (the system manages itself: auto-repair, auto-scaling, auto-failover).

Aim to move up the ladder; the best automation is the system not needing it.

### Designing automation safely

Automation applies changes at machine speed, including mistakes, so build guard rails:
- **Idempotent** operations — safe to rerun after partial failure.
- **Validate inputs**; treat an empty or missing filter as an error, never as "everything".
- **Rate limits and blast-radius caps** — refuse to act on more than N targets or more than X% of a fleet at once.
- **Cross-check intent** with another source of truth before destructive actions (e.g. is this rack actually scheduled for decommission?).
- **Dry-run mode**, logging of every action, and an easy **kill switch**.
- Own it like production code: tests, review, monitoring, on-call.
- Keep humans able to understand and take over: automation that nobody understands erodes operational skill.

## Adopting SRE in an Organization

### What SRE is

SRE treats operations as a software engineering problem. Core tenets:
- Reliability targets are explicit (SLOs) and owned jointly with product; error budgets arbitrate between reliability and velocity.
- Ops work is capped (~50%); the rest goes to engineering that reduces future ops work.
- Toil is measured and eliminated; automation and self-healing are preferred.
- Failure is normal; learning from it is blameless and structured.
- Monitoring alerts humans only when action is needed.

**Relation to DevOps:** DevOps is a broad set of cultural principles (no silos, accept failure, gradual change, tooling and measurement). SRE is one concrete implementation of those principles, with specific practices and metrics. You can adopt SRE practices without a team called "SRE".

### Starting with no SRE team

Practices that work for any team and pay off quickly, roughly in order:
1. Define SLOs for one important service and agree an error budget policy (`sre-slos-and-error-budgets`, `sre-slos-and-error-budgets`).
2. Make alerts SLO-based and reduce noise (`sre-monitoring-and-alerting`).
3. Introduce blameless postmortems with tracked action items (`sre-postmortem`).
4. Measure toil and start automating the biggest items (*Toil Reduction and Automation* above).
5. Define incident roles and practise them (`sre-incident-response`).

### Team lifecycle

1. **Seed** — one or a few engineers apply SRE practices to a high-value service; prove value with measurable outcomes (fewer pages, SLOs met, faster releases).
2. **Form a team** — charter, scope, on-call rotation of sustainable size (*Rotation design checklist* above), explicit engagement model with dev teams (`sre-release-and-launch`).
3. **Grow and split** — as scope grows, split by service area or by platform vs. embedded; keep shared practices and tooling.
4. **Mature** — invest in platforms and frameworks that make services reliable by default, so expertise scales beyond headcount.

### Charter and engagement

Write a charter covering: mission, which services are in scope, what SRE does vs. what dev teams do, entry criteria for onboarding a service (PRR), exit criteria (when pager goes back to devs), and how priorities are set.

### Staffing and skills

- Hire for software engineering ability plus systems knowledge (networking, OS, distributed systems) and troubleshooting temperament.
- Mix backgrounds; pair experienced operators with strong coders.
- Keep a balance between project work and ops for everyone, to prevent burnout and keep skills current.

### Communication and collaboration

- **Weekly production meeting** per service: review pages and incidents since last meeting, upcoming changes and launches, SLO/budget status, outstanding postmortem action items, and toil/ticket trends. Rotate the chair; publish notes.
- Keep dev and SRE priorities visible to each other; joint planning for reliability work.
- Distributed teams: favor written communication, clear ownership, explicit handoffs, overlap hours for key meetings.

### Leading the change

- Start where pain is visible and measurable; show results with data before expanding.
- Get explicit leadership sponsorship for the error budget policy and for protecting engineering time.
- Change incrementally: one service, one practice at a time; adapt practices to your context rather than copying Google wholesale.
- Expect and address resistance: explain the "why", involve affected teams in designing processes, and celebrate early wins.
- Measure progress: SLO attainment, pages per shift, toil hours, postmortem action-item closure, deploy frequency, time to mitigate.

## Sources

- SRE book ch. 11 Being On-Call — https://sre.google/sre-book/being-on-call/
- SRE book ch. 28 Accelerating SREs to On-Call and Beyond — https://sre.google/sre-book/accelerating-sre-on-call/
- SRE book ch. 29 Dealing with Interrupts — https://sre.google/sre-book/dealing-with-interrupts/
- SRE book ch. 30 Embedding an SRE to Recover from Operational Overload — https://sre.google/sre-book/operational-overload/
- Workbook ch. 8 On-Call — https://sre.google/workbook/on-call/
- Workbook ch. 17 Identifying and Recovering from Overload (team overload) — https://sre.google/workbook/overload/
- SRE book ch. 5 Eliminating Toil — https://sre.google/sre-book/eliminating-toil/
- SRE book ch. 7 The Evolution of Automation at Google — https://sre.google/sre-book/automation-at-google/
- Workbook ch. 6 Eliminating Toil — https://sre.google/workbook/eliminating-toil/
- SRE book ch. 1 Introduction — https://sre.google/sre-book/introduction/
- SRE book ch. 31 Communication and Collaboration in SRE — https://sre.google/sre-book/communication-and-collaboration/
- SRE book ch. 33 Lessons Learned from Other Industries — https://sre.google/sre-book/lessons-learned/
- SRE book Appendix F Example Production Meeting Minutes — https://sre.google/sre-book/production-meeting/
- Workbook ch. 1 How SRE Relates to DevOps — https://sre.google/workbook/how-sre-relates/
- Workbook ch. 20 SRE Team Lifecycles — https://sre.google/workbook/team-lifecycles/
- Workbook ch. 21 Organizational Change Management in SRE — https://sre.google/workbook/organizational-change/
