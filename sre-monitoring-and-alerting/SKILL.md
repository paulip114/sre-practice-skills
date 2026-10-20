---
name: sre-monitoring-and-alerting
description: Use when designing or reviewing monitoring, dashboards and alerts — golden signals, white-box vs black-box, alert hygiene, and turning SLOs into multiwindow multi-burn-rate alerts (with Prometheus templates and a burn-rate calculator). Based on Google SRE practice.
---

# Monitoring and Alerting

Monitoring answers what is broken and why. Page humans only when the error budget is under real threat; everything else is a ticket or a dashboard.

## Monitoring Design

Monitoring exists to answer two questions: **what is broken** (symptom) and **why** (cause). Build it so that a human is only interrupted for the first, and can find the second quickly.

### Principles

- **Alert on symptoms, investigate with causes.** Users feel "checkout is slow", not "DB CPU is 90%". Page on user-visible symptoms (ideally SLO burn — see *Alerting on SLOs* below); keep cause metrics for dashboards and debugging.
- **Every page must be urgent, actionable, and need human judgment.** If a script could respond, automate it. If it can wait until morning, it's a ticket. If nobody acts on it, delete it.
- **Keep it simple.** Rules that rarely fire, signals nobody looks at, and clever heuristics rot. Prefer a small set of well-understood signals and remove what isn't used (review quarterly).
- **Black-box + white-box.** Black-box probes show what users see right now (and catch problems that never reach your servers). White-box metrics show internals and imminent problems. You need both.
- **Measure distributions, not averages.** Use histograms/percentiles for latency; averages hide the tail. Choose bucket boundaries that match SLO thresholds.

### The four golden signals (request-serving systems)

| Signal | What to measure | Watch for |
|---|---|---|
| Latency | Time to serve, **separately for successes and errors** | Fast errors hide in blended averages; slow errors are worse than fast ones |
| Traffic | Demand: requests/s, sessions, transactions, bytes | Sudden drops can mean an upstream outage, not good news |
| Errors | Rate of failed requests: explicit (5xx), implicit (wrong content), policy (slower than promised) | Some errors are only visible end-to-end |
| Saturation | How full the most constrained resource is (CPU, memory, I/O, threads, queue depth, connection pools) | Latency increase is often the earliest sign; predict "full in N hours" |

For pipelines add freshness, throughput and backlog; for storage add durability and capacity headroom.

### Design procedure

1. **Start from SLIs** (`sre-slos-and-error-budgets`). Those become the top of every dashboard and the source of pages.
2. **Instrument the golden signals** at each tier (load balancer, service, critical dependencies). Label by endpoint/request class, response code, and version so you can slice by release.
3. **Add saturation metrics** for the resource that runs out first. Know what that is from load tests (`sre-capacity-and-system-design`).
4. **Add black-box probes** for each critical user journey, from outside your network.
5. **Decide metrics vs logs vs traces.** Metrics for things you alert on and trend (cheap, aggregated). Logs for per-event detail and forensic debugging. Traces for latency breakdown across services. Don't page from log scraping if a metric can carry the signal.
6. **Build dashboards in layers:**
   - Service overview: SLIs + budget remaining, golden signals, current release version.
   - Dependency view: each critical dependency's latency/errors as seen from the caller.
   - Resource view: saturation per component.
   Annotate deploys, config pushes and incidents on graphs.
7. **Write alert rules with**: a clear name, severity (page/ticket), the user impact in the description, and a runbook link with first diagnostic steps.
8. **Test the monitoring.** Verify alerts fire by injecting failures in staging or by unit-testing rules. Monitor the monitoring (a dead-man's-switch alert that fires when the pipeline stops sending).

### Alert hygiene checklist

For every existing page:
- [ ] Did it detect something users would notice (or will soon)?
- [ ] Was action required immediately, and did a human need to decide what to do?
- [ ] Has it fired spuriously in the last quarter? How often was it ignored?
- [ ] Does it duplicate another alert for the same symptom?
- [ ] Does its runbook exist and still match reality?

Anything failing these: convert to ticket, automate the response, merge, or delete. Track pages per shift as a health metric (`sre-on-call-and-toil`).

### Anti-patterns

- Paging on every cause metric "just in case".
- Static thresholds copied from another service without understanding.
- Dashboards with dozens of graphs and no ordering by importance.
- Monitoring that depends on the system it monitors (same cluster, same network path).
- Long `for:` durations used to hide flapping instead of fixing the signal.

## Alerting on SLOs

Page a human only when the error budget is under real threat. Everything else is a ticket or a dashboard.

### Judge any alerting strategy on four properties

- **Precision** — share of alerts that were significant.
- **Recall** — share of significant events that alerted.
- **Detection time** — how fast it fires.
- **Reset time** — how long it keeps firing after recovery.

A "significant event" means it consumed a meaningful fraction of the error budget.

### Why the simple options fail

| Approach | Problem |
|---|---|
| Alert when the short-window (e.g. 10 min) error rate ≥ SLO threshold | Poor precision: can fire many times a day while the SLO is still met |
| Same threshold, long window (e.g. 36 h) | Good precision, but it keeps firing for hours after the problem is fixed and is expensive to compute |
| Short window + `for:` duration | Detection time ignores severity (a total outage waits as long as a tiny one); a flapping signal resets the timer and may never fire. **Don't use durations for SLO alerts.** |
| Single burn-rate alert (e.g. 14.4× over 1h) | Good precision and detection, but misses slower burns that still exhaust the budget |

### Recommended: multiwindow, multi-burn-rate

**Burn rate** = observed error ratio ÷ (1 − SLO). Burn rate 1 spends exactly the whole budget over the window; burn rate 1,000 on a 99.9%/30-day SLO spends it in ~43 minutes.

Starting configuration for a 30-day window (scale thresholds by your SLO):

| Severity | Long window | Short window | Burn rate | Budget consumed when it fires |
|---|---|---|---|---|
| Page | 1 h | 5 min | 14.4 | 2% |
| Page | 6 h | 30 min | 6 | 5% |
| Ticket | 3 d | 6 h | 1 | 10% |

- Fire only when **both** long and short windows exceed the threshold. The long window gives precision; the short window (≈1/12 of the long) makes it stop firing soon after recovery.
- Threshold for each row = `burn_rate × (1 − SLO)`.
- Burn rate for "X% of budget in window W" over period P = `X × P / W`. (2% of 30 days in 1 h → 0.02 × 720 = 14.4.)
- Add alert suppression/inhibition so one big outage doesn't produce three notifications.
- Pages and tickets are the only alert outputs that ask a human to act; route the ticket row to a queue, not a pager.

Rule templates: `references/prometheus-rules.md`. Calculator: `scripts/burn_rate.py`.

### Special cases

**Low-traffic services** — one failure out of a handful of requests looks like a 1,000× burn. Options, usually combined:
- Generate synthetic traffic with probers (but synthetic success can mask real-user failure).
- Aggregate related low-traffic services that share failure domains into one alerting group.
- Make the product tolerate single failures (client retries with exponential backoff and jitter, queued/deferred execution).
- Reconsider whether the SLO or window is right if a single failure really doesn't merit a page.

**Very loose SLOs (e.g. 90%)** — a total 1-hour outage may never reach "2% of budget in 1h"; recompute thresholds so achievable outages can still fire.

**Very tight SLOs (e.g. 99.999%)** — a full outage burns the monthly budget in under a minute, faster than alerting can react. Defend these with design: progressive rollouts (a 1% canary stretches the time-to-exhaustion 100×), automated rollback, isolation. See `sre-release-and-launch`.

### Alerting at scale

Don't hand-tune windows and burn rates per service. Pick one parameter set and apply it everywhere. Group request types into a few classes with shared targets, e.g.:

| Class | Example | Availability | Latency |
|---|---|---|---|
| CRITICAL | login, payment | 99.99% | tight |
| HIGH_FAST | interactive core features | 99.9% | tight |
| HIGH_SLOW | reports, exports | 99.9% | relaxed |
| LOW | background polling | 99% | none |
| NO_SLO | dark launches, alpha | none | none |

### Reviewing existing alerts

For each alert ask: Is it tied to user-visible impact (symptom) or to an internal cause? Does it require immediate human action? What did responders actually do the last N times? Delete or downgrade anything that is routinely ignored or auto-resolves. See also *Alert hygiene checklist* above and `sre-on-call-and-toil`.

## Sources

- SRE book ch. 6 Monitoring Distributed Systems — https://sre.google/sre-book/monitoring-distributed-systems/
- SRE book ch. 10 Practical Alerting — https://sre.google/sre-book/practical-alerting/
- Workbook ch. 4 Monitoring — https://sre.google/workbook/monitoring/
- Workbook ch. 5 Alerting on SLOs — https://sre.google/workbook/alerting-on-slos/
