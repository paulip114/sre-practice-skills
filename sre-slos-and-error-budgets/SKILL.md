---
name: sre-slos-and-error-budgets
description: Use when defining, reviewing or refining SLIs and SLOs, writing or applying an error budget policy (release freezes, reliability prioritization, escalation), or quantifying incidents and projects in error-budget terms. Based on Google SRE practice.
---

# SLOs and Error Budgets

Define what "reliable enough" means for users, then agree in advance what the organization does when the service falls short.

## SLO Design

Design service level indicators (SLIs) and objectives (SLOs) that track what users experience, and that the organization will actually use to make decisions.

### Core ideas

- An SLO is a target for "reliable enough". Above it, nearly all users are satisfied; below it, they start to complain or leave.
- **100% is never the target.** Every extra nine costs more and is worth less to users, dependencies between you and the user add their own failures, and a 100% goal leaves no room for change, which is the main source of outages.
- Express every SLI as **good events / valid events**, a ratio between 0% and 100%. Then error budget = 100% − SLO, and one set of tooling (numerator, denominator, threshold) works for every SLI.
- Separate the **SLI specification** (what matters to the user, e.g. "home page loads in < 100 ms") from the **SLI implementation** (where and how it is measured). One spec can have several implementations that trade off fidelity, coverage and cost.
- SLOs need an **owner empowered to trade velocity for reliability** — usually the product owner.

### Procedure

1. **Scope.** Pick one application. Name the users whose happiness you are optimizing.
2. **Map the system.** Sketch components, request flow, data flow and critical dependencies. Classify each component as *request-driven*, *pipeline* or *storage* (see `references/sli-menu.md`).
3. **List critical user journeys** (e.g. search → add to cart → checkout). These are what SLIs should ultimately represent.
4. **Choose SLI specs.** At most ~5 SLI types for the service. Use multiple thresholds for latency-like SLIs so you cover both the typical case and the tail (e.g. 90% < 100 ms *and* 99% < 400 ms).
5. **Choose implementations.** Start with the cheapest data that exists (logs or load-balancer metrics) over probers or client instrumentation that would take weeks. Prefer measuring as close to the user as is practical, and note what each source misses (e.g. server logs miss requests that never arrive).
6. **Set starter targets.** If nothing better is known, measure recent performance and round *down* to a manageable figure (e.g. two significant figures for availability, a coarse step for latency). Don't lock yourself into today's accidental excellence, but remember users come to expect whatever you deliver.
7. **Pick a window.** Default: a **4-week rolling window** (whole weeks keep weekend counts constant), with weekly summaries for prioritization and quarterly reports for planning. Use calendar windows only where business planning needs them.
8. **Compute the budget** in absolute terms (allowed bad events per window) so people can reason in "this outage cost 13% of our budget".
9. **Get agreement from three parties:** product (target is good enough for users), development (will act when budget runs out), operations (defensible without heroics or excessive toil). If any party won't sign, iterate on the SLI/SLO — don't ship an SLO without teeth.
10. **Document** it using `references/slo-document-template.md`, including the rationale and whether numbers are observational or ad hoc. Review monthly at first, quarterly once stable.
11. **Pair with** an error budget policy (*Error Budget Policy* below) and burn-rate alerts (`sre-monitoring-and-alerting`).

### Iterating on an existing SLO

Collect a cheap signal of user happiness (support tickets, manually detected outages, forum posts, surveys). Then compare it with budget burn:

- Real user pain that never dented the budget → poor **recall**: tighten the SLO or move/broaden the SLI implementation.
- Budget burn with no user pain → poor **precision**: loosen the SLO or fix the SLI.
- If moving the threshold either way gives too many false positives or negatives, the *implementation* is the problem, not the number.
- Need a tighter target than you can meet today? Track it as an **aspirational SLO** that the error budget policy explicitly does not enforce.

Use this matrix to decide what to do next:

| SLO | Toil | Users happy? | Action |
|---|---|---|---|
| Met | Low | Yes | Ship faster / relax release process, or move SRE effort elsewhere |
| Met | Low | No | Tighten SLO |
| Met | High | Yes | Reduce false-positive alerting or temporarily loosen SLO; fix product / automate mitigation |
| Met | High | No | Tighten SLO |
| Missed | Low | Yes | Loosen SLO |
| Missed | Low | No | Make alerting more sensitive |
| Missed | High | Yes | Loosen SLO |
| Missed | High | No | Offload toil; fix product / automate mitigation |

### Advanced patterns

- **Bucket requests** by importance or expected responsiveness (e.g. premium vs free tier; interactive vs bulk export) and give each bucket its own SLO, rather than one SLO per endpoint.
- **Dependencies:** a component on the critical path of a high-value journey needs an SLO at least as strict as that journey. Don't multiply availabilities as if redundant copies were independent — shared dependencies and control planes break that math.
- **Don't** confuse SLOs with SLAs: an SLA is a contractual promise with penalties and should be looser than the internal SLO.

### Output

When asked to design SLOs, produce: the component classification, a table of SLI specs → implementations (with known blind spots), proposed targets with rationale, window, budget in absolute numbers, and a filled SLO document.

## Error Budget Policy

An SLO only changes behavior if the organization has agreed in advance what it will do when the budget runs low. The error budget policy is that agreement.

### Core ideas

- **Error budget = 1 − SLO** over the SLO window. A 99.9% SLO on 1M requests in four weeks allows ~1,000 bad requests.
- The budget is a shared currency between product velocity and reliability. While budget remains, teams may take risk (launch, experiment). When it's gone, risk-reduction takes priority.
- The policy must be written down and **approved by product, development and SRE/operations before it is needed**. Getting that sign-off is also a test of whether the SLO is right (see step 9 of *SLO Design*).
- Enforcement is not punishment; it is the pre-agreed way to restore stability.
- Budget is an approximation of user pain. One long outage, several short ones and a steady low error rate can cost the same budget but feel different to users — use judgment at the edges.

### Writing a policy

Use `references/policy-template.md`. It must cover:

1. **Goals and non-goals** — protect users from repeated misses; give permission to ship while in budget. Not a tool to punish teams or to aim for zero errors.
2. **SLO miss policy** — what happens when the budget is exhausted over the window. Typical: halt all changes except urgent fixes (high-priority bugs, security) until back within SLO; reliability bugs take top priority; optionally the whole dev team works on reliability.
3. **What counts.** Decide in advance, and write down:
   - Service's own bugs or procedural errors → enforce the freeze.
   - Failures of company-wide infrastructure or another team's dependency → choose between "freeze anyway" (better for users) or "don't freeze, but escalate to the dependency". Record the choice.
   - Errors that were miscategorized and later found → may retroactively trigger the policy.
4. **Outage policy (single-incident thresholds)** — e.g. any single incident that consumes more than a set share of the window's budget (20% is a common starting point) requires a postmortem with at least one top-priority action item; a recurring class of outage consuming a large share over a quarter requires a planned project to fix it.
5. **Escalation path** — who arbitrates if teams disagree about the calculation or about whether the action is appropriate (usually a named senior leader).
6. **Exit criteria** — e.g. back within SLO over the window, plus the main contributing causes addressed.
7. **Authors, reviewers, approvers, approval and next-review dates.**

### Applying the policy

When budget is burning, work through:

1. **How much has been used, and by what?** Rank incidents in the window by budget consumed. Example: a bad release that caused 14k errors against a 110k budget used ~13%.
2. **Is the policy triggered?** Compare against the thresholds in the policy, not against how anyone feels.
3. **Who owns the cause?** Apply the dependency rule written in the policy.
4. **Act** — freeze, re-prioritize, schedule postmortems — and announce it to stakeholders with the numbers.
5. **Track exit criteria** and lift the freeze explicitly.

### Using budget for prioritization

- Estimate expected budget cost per year of each failure class (frequency × budget per occurrence). Fix the most expensive class first. E.g. two or three bad releases per year can cost far more budget than a once-in-five-years hardware failure, so automated rollback beats a replicated database.
- Consistently under-spending budget with low toil and happy users → relax release controls, ship faster, or move reliability effort to services that need it.
- **Aspirational SLOs** can be measured alongside the real one; the policy should state they don't trigger enforcement.
- Only experiment with deliberately degrading the service (e.g. added latency to measure user sensitivity) when there is clearly budget to spare, and be careful interpreting the results.

## Sources

- SRE book ch. 3 Embracing Risk — https://sre.google/sre-book/embracing-risk/
- SRE book ch. 4 Service Level Objectives — https://sre.google/sre-book/service-level-objectives/
- Workbook ch. 2 Implementing SLOs — https://sre.google/workbook/implementing-slos/
- Workbook ch. 3 SLO Engineering Case Studies — https://sre.google/workbook/slo-engineering-case-studies/
- Workbook Appendix A Example SLO Document — https://sre.google/workbook/slo-document/
- Workbook ch. 2 Implementing SLOs (Establishing an Error Budget Policy; Decision Making) — https://sre.google/workbook/implementing-slos/
- Workbook Appendix B Example Error Budget Policy — https://sre.google/workbook/error-budget-policy/
