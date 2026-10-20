---
name: sre-capacity-and-system-design
description: Use when designing or reviewing a distributed system for scale and resilience — NALSD capacity math, load balancing, load shedding, retries, deadlines, graceful degradation, cascading failures, simplicity, and distributed consensus for critical state. Based on Google SRE practice.
---

# Capacity, Overload and Reliable System Design

Design with real numbers, survive the loss of your largest failure domain, and make every component degrade gracefully instead of collapsing under load.

## Overload and Cascading Failures

A cascading failure is one that grows by positive feedback: one part fails, its load moves to the rest, which then fails too. Most are driven by overload, so the defense is to make every service degrade gracefully instead of falling over.

### How cascades happen

- **Server overload** → slower responses → more concurrent requests → more memory/CPU → slower still.
- **Resource exhaustion**: CPU (queues grow), memory (GC thrash, OOM kills), threads, file descriptors, connection pools.
- **Retry amplification**: every layer retries, multiplying load on the struggling backend.
- **Crash loops / health-check churn**: overloaded tasks fail health checks, get removed, pushing more load onto survivors.
- **Slow startup / cold caches**: restarted tasks can't take full load yet.
- Triggers: traffic spikes, a lost cluster/zone, bad releases, cache flushes, batch jobs, a planned change that reduces capacity.

### Defenses (design time)

1. **Load-test to find the limit** and how the service fails beyond it. Know which resource runs out first. A service should keep serving at its capacity under excess load, not collapse.
2. **Load shedding**: reject excess requests early and cheaply (based on concurrent requests, queue length or CPU) with an explicit "overloaded" error. Keep queues short — a long queue just adds latency.
3. **Graceful degradation**: serve cheaper results (cached, partial, lower quality) when overloaded. Make degraded mode easy to trigger and test it regularly.
4. **Request criticality**: tag requests (e.g. critical-plus, critical, sheddable-plus, sheddable) and propagate the tag; shed least critical first. Batch and prefetch traffic should be sheddable.
5. **Retries done right**:
   - Exponential backoff with jitter.
   - Per-request retry cap (e.g. 3 attempts).
   - A **retry budget** per client (e.g. retries ≤ ~10% of requests); stop retrying when exceeded.
   - **Retry at one layer only**; lower layers return "overloaded, don't retry" so the error doesn't fan out.
6. **Deadlines**: every request carries a deadline, propagated (minus elapsed time) to downstream calls. Servers drop work whose deadline has already passed. Beware deadlines set far longer than useful.
7. **Client-side adaptive throttling**: clients track requests vs. accepted responses over a recent window and reject locally with probability ≈ max(0, (requests − K·accepts) / (requests + 1)), with K ≈ 2. This stops wasted work at the source when the backend is rejecting.
8. **Load balancing**: at the frontend, steer users by proximity and capacity (DNS, anycast, L7). In the datacenter, use subsetting (each client talks to a bounded subset of backends) and balancing on load signals (e.g. weighted round robin or least-loaded), not naive round robin.
9. **Capacity planning**: provision for peak plus headroom for losing your largest failure domain (N+2 is common); forecast organic growth and launches; autoscaling with sensible min/max, scaling on the right signal, and awareness that scaling a frontend can overload a backend.
10. **Avoid dangerous behaviors**: don't fail health checks just because you're busy; make startup fast and warm caches gradually; avoid synchronized clients (jitter cron and retries); test the full-cluster-loss scenario.

### Recovery playbook (during an overload incident)

1. **Stop the feedback loop first**: increase capacity if possible, but more importantly reduce load.
2. **Shed or block load**: drop sheddable/batch traffic, rate-limit or block the abusive or misbehaving client, turn on degraded mode.
3. **Stop retries amplifying** (disable client retries, raise backoff).
4. **Stop health-check churn** if it is killing tasks that could serve.
5. **Restart carefully** in stages, letting caches warm, rather than all at once.
6. **Add traffic back gradually**, watching saturation.
7. Afterwards: postmortem, with load test and degradation work as action items.

### Review checklist for a service

- [ ] Known capacity per task and per cluster, from load tests, with the limiting resource identified?
- [ ] Behavior beyond capacity tested — sheds instead of collapsing?
- [ ] Deadlines set and propagated; expired work dropped?
- [ ] Retries bounded per request and per client, at one layer, with backoff + jitter?
- [ ] Request criticality defined and used for shedding?
- [ ] Degraded mode exists and is exercised?
- [ ] Capacity covers peak with loss of the largest failure domain?
- [ ] Health checks distinguish "dead" from "busy"?

## Reliable System Design Review

### Non-abstract large system design (NALSD)

Design iteratively and make every design **concrete**: put real numbers on it and check it would fit on real machines and networks. An elegant abstract design that needs 10× the hardware you have is not a design.

#### Procedure

1. **Clarify requirements.** Users, operations (reads/writes), data size, request rate, latency and availability SLOs, consistency needs, growth over 1–3 years.
2. **Is it possible at all?** Sketch the simplest design ignoring scale (one machine). Does it meet functional requirements?
3. **Can we do better?** Improve the algorithm/data layout before adding machines (e.g. O(n) → O(log n), precompute, index).
4. **Make it scale.** Distribute: shard, replicate, cache, batch. For each component, calculate:
   - Peak QPS (incl. growth and a safety factor), per-request CPU, memory, disk and network cost.
   - Storage size including replication and indices.
   - Number of machines = max over resources of (demand ÷ per-machine capacity), plus headroom.
   - Latency budget across hops vs. the SLO.
   Use `references/estimation-cheatsheet.md` for back-of-envelope numbers.
5. **Make it reliable.** Place replicas across failure domains (machine, rack, zone, region); provision N+2 for the largest domain; decide degradation behavior when a component is lost.
6. **Iterate.** Re-run the numbers after each change; record assumptions so they can be checked against reality later (load tests, production metrics).

Output a bill of materials (machines/resources per component per region) and the assumptions behind it.

### Simplicity review

Complexity is the enemy of reliability. Distinguish **essential** complexity (inherent in the problem) from **accidental** complexity (from our solutions), and attack the latter.

Ask in review:
- Can the design be explained in a few sentences and a single diagram?
- Is every component, flag, and option needed now? Remove unused code and features ("negative lines of code" are a win).
- Are APIs minimal and hard to misuse? Are modules loosely coupled with clear ownership?
- Are releases small and frequent rather than large and rare?
- Is the system boring in the good sense — predictable, using well-understood technology?
- Track complexity over time (number of dependencies, config knobs, services); push back when it grows without need.

### Critical state and distributed consensus

For state that must be consistent across replicas (leader election, locks, configuration, metadata, queues that must not lose or duplicate work):

- Use a proven **consensus system** (Paxos/Raft-based: e.g. etcd, ZooKeeper, Spanner-like stores) instead of ad-hoc heartbeats or "whoever writes last wins". Heartbeat-based leader election suffers split-brain under network partitions.
- Understand the trade-off (CAP): under partition you choose between availability and consistency — for critical state, choose consistency.
- **Performance**: consensus needs a quorum round-trip per write; place replicas so a quorum is close together for latency, while still spread enough to survive the failure domains you care about. Typically 5 replicas tolerate 2 failures; 3 tolerate 1.
- Batch and pipeline proposals to increase throughput; serve reads from leader leases or followers only when stale reads are acceptable.
- **Monitor**: number of healthy replicas, leader changes, proposal latency, lagging replicas, quorum loss risk.
- Keep the consensus system small and dedicated; put bulk data elsewhere and store only pointers/metadata in it.

### Review checklist

- [ ] Requirements quantified (QPS, data size, SLOs, growth)?
- [ ] Capacity math shown per component, with assumptions written down?
- [ ] Failure domains identified; design survives loss of largest one at peak?
- [ ] Critical state handled by a consensus system, with replica placement justified?
- [ ] Degradation plan when a dependency fails?
- [ ] Accidental complexity challenged; the simplest workable design chosen?

## Sources

- SRE book ch. 19 Load Balancing at the Frontend — https://sre.google/sre-book/load-balancing-frontend/
- SRE book ch. 20 Load Balancing in the Datacenter — https://sre.google/sre-book/load-balancing-datacenter/
- SRE book ch. 21 Handling Overload — https://sre.google/sre-book/handling-overload/
- SRE book ch. 22 Addressing Cascading Failures — https://sre.google/sre-book/addressing-cascading-failures/
- Workbook ch. 11 Managing Load — https://sre.google/workbook/managing-load/
- SRE book ch. 9 Simplicity — https://sre.google/sre-book/simplicity/
- SRE book ch. 23 Managing Critical State: Distributed Consensus — https://sre.google/sre-book/managing-critical-state/
- SRE book ch. 2 The Production Environment at Google — https://sre.google/sre-book/production-environment/
- Workbook ch. 7 Simplicity — https://sre.google/workbook/simplicity/
- Workbook ch. 12 Introducing Non-Abstract Large System Design — https://sre.google/workbook/non-abstract-design/
