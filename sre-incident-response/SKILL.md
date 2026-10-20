---
name: sre-incident-response
description: Use during or when preparing for a production incident — declaring it, incident command roles, the live incident document, status updates, mitigation, handoff, drills — and when systematically diagnosing a production problem. Based on Google's IMAG / Incident Command System practice.
---

# Incident Response and Troubleshooting

Manage the incident (people, communication, control) and resolve it (mitigate first, then diagnose systematically).

## Incident Response

Resolve the incident (mitigate impact, restore service) **and** manage it (coordinate people, keep everyone informed). Most incidents that spiral do so because of management failures, not technical ones.

### The 3Cs

- **Coordinate** the response effort.
- **Communicate** among responders, to the organization, and to users.
- **Control** the response: one clear line of command; no freelancing.

Common failure modes to guard against: the on-call is so deep in the technical problem that nobody manages; nobody knows what others are doing; well-meaning people make uncoordinated changes that make things worse.

### When to declare an incident

Declare early. It is cheap to close a small incident and expensive to organize a big one hours late. Declare if **any** is true:

- A second team is needed to fix it.
- The problem is visible to users/customers.
- It is still unsolved after about an hour of focused work.

Teams should keep their own written criteria based on past outages and known high-risk areas.

### Roles

| Role | Responsibilities |
|---|---|
| **Incident Commander (IC)** | Holds the overall picture; assigns roles; makes decisions; removes blockers. Holds every role not yet delegated. Does not get lost in debugging. |
| **Operations Lead (OL)** | Leads hands-on mitigation. **The ops team is the only group that changes production during the incident.** |
| **Communications Lead (CL)** | Public face of the response: periodic updates to stakeholders and users, answers inquiries, keeps the incident doc current. |
| **Planning** (larger incidents) | Files bugs, tracks deviations from normal state to undo later, arranges handoffs and staffing. |

The person who declares is IC by default. Roles can be delegated recursively; if anyone is overloaded they ask for more people and create sub-teams.

### Running the incident

1. **Declare** in the agreed channel; name the IC.
2. **Open the live incident state document** (`references/incident-state-doc-template.md`). IC's most important job is keeping it accurate; most important info at the top.
3. **Assess impact**: who/what is affected, since when, how badly, is it growing.
4. **Mitigate first, root-cause later.** Users care that errors stop, not that you understand why. Reach for **generic mitigations** as soon as you know *where* the problem is, even if you don't know *what* it is:
   - Roll back the latest release or config push.
   - Drain traffic away from a bad zone/cluster/region.
   - Disable the new feature via flag.
   - Add capacity / shed low-priority load.
   - Block an abusive client.
   Record every change in the doc so it can be reverted. Preserve evidence (logs, core dumps) where feasible.
5. **Communicate on a cadence** (e.g. every 30–60 min for major incidents, even if "no change"). Use pre-written templates. Say clearly when the incident is over — silence is read as "still broken".
6. **Re-evaluate periodically**: is the current approach still the best one? Should we escalate or switch tack?
7. **Hand off explicitly.** When the IC changes (shift end, fatigue, or someone more experienced arrives), brief the new IC, say "you are now the incident commander", wait for explicit acknowledgment, and announce the change.
8. **Close**: confirm recovery with metrics, declare resolved, assign a postmortem owner (`sre-postmortem`).

Responders should watch their own state: if you're panicking or exhausted, ask for help or rotate out. Rotate long-incident responders every few hours.

### Preparing beforehand

- Write and socialize the incident process (roles, criteria, channel) before it's needed.
- Agree on **one** communication channel (chat room + bridge) and practise using it. Don't host it on infrastructure that might be the thing that's down.
- Keep a **contact list** of on-calls and escalation paths for every team you depend on.
- Prepare 2–3 **status update templates** and know who approves external communications.
- Build generic mitigation tooling (one-command rollback, drain, feature kill switches) **in calm times**; review past postmortems to find which ones would have helped.
- **Practise:** role-play past incidents ("Wheel of Misfortune"), run disaster-recovery tests, and use the incident framework for ordinary multi-team operations so it stays familiar. Rotate who plays IC.

## Effective Troubleshooting

Treat debugging as applied scientific method: observe, hypothesize, test, repeat — while keeping the service alive.

### The loop

1. **Problem report.** Write down: expected behavior, actual behavior, how to reproduce if possible, when it started, scope. Vague reports ("it's slow") must be sharpened first.
2. **Triage.** Judge severity. If users are hurting, **stop the bleeding first** (rollback, drain, shed load — see *Running the incident* above) before deep diagnosis. Preserve evidence when you can (logs, snapshots, a held-out instance).
3. **Examine.** Look at what the system is telling you:
   - Golden-signal dashboards for the service and its dependencies.
   - Logs and traces for failing requests; compare with a succeeding one.
   - Introspection endpoints (status pages, current config, version, health).
   - Recent changes: deploys, config pushes, flag flips, traffic shifts, dependency changes. Correlating the start time with a change is often the fastest lead.
4. **Diagnose.** Form hypotheses that explain *all* the observations. Narrow the search space:
   - **Simplify and reduce** — can you reproduce with a smaller input, one instance, one request?
   - **Divide and conquer / bisect** — test the middle of the request path (or the commit range) and halve the search each step.
   - **Ask "what, where, why"** — what is the system doing, where are resources going, why is it doing that.
   - **What touched it last?** — systems tend to stay working until something changes.
5. **Test and treat.** Design tests that can *disprove* a hypothesis. Prefer tests with mutually exclusive outcomes. Consider side effects: a test that adds logging or load can change behavior. Record every test and result.
6. **Cure.** Once the cause is confirmed, fix it, verify, and record the findings for the postmortem (`sre-postmortem`).

### Traps to avoid

- **Looking at irrelevant symptoms** or misreading metrics — understand what a graph actually measures before trusting it.
- **Not knowing how to change the system** or its inputs to test a hypothesis safely.
- **Favoring far-fetched theories** over simple ones; remember common causes are common.
- **Chasing coincidences** — correlation in time is a lead, not a proof. Other services may share the symptom for unrelated reasons.
- **Anchoring** on the first hypothesis; actively list alternatives and look for evidence against your favorite.
- **Changing several things at once** — you won't know which one mattered, and you may stack new problems.
- **Freelance changes during an incident** — coordinate through the ops lead.

### Make systems easier to debug (do this ahead of time)

- Consistent structured logging with request IDs propagated across services; adjustable log verbosity at runtime.
- Distributed tracing on critical paths.
- Introspection endpoints showing version, config, dependency health, and recent errors.
- Tools that diff current vs last-known-good config/version.
- Write down useful diagnostic queries and playbook steps after each investigation.

### Output when asked to help debug

Return: a sharpened problem statement, the evidence reviewed, a ranked list of hypotheses with the test that would confirm or refute each, recommended immediate mitigation if users are affected, and what to record for the postmortem.

## Sources

- SRE book ch. 13 Emergency Response — https://sre.google/sre-book/emergency-response/
- SRE book ch. 14 Managing Incidents — https://sre.google/sre-book/managing-incidents/
- SRE book Appendix C Example Incident State Document — https://sre.google/sre-book/incident-document/
- Workbook ch. 9 Incident Response — https://sre.google/workbook/incident-response/
- SRE book ch. 12 Effective Troubleshooting — https://sre.google/sre-book/effective-troubleshooting/
- SRE book ch. 6 Monitoring Distributed Systems — https://sre.google/sre-book/monitoring-distributed-systems/
