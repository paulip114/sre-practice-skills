---
name: sre-data-reliability
description: Use when designing, operating or reviewing data pipelines, scheduled/cron jobs, backups and restores, or data integrity protections — pipeline SLOs, idempotency, handling stragglers and hot spots, distributed cron, defense in depth against data loss, and recovery testing. Based on Google SRE practice.
---

# Data Pipelines, Scheduled Jobs and Data Integrity

## Data integrity: what users need is restores, not backups

Users judge you by whether their data is there and correct when they ask for it. A backup that has never been restored is a hope, not a plan.

### Threat model

Data loss comes from many combinations of:
- **Root cause**: user error, application bugs, operator/automation error, infrastructure failure, malicious action, migration bugs.
- **Scope**: wide (many entities) vs. narrow (one user/object).
- **Rate**: sudden (big bang) vs. slow and creeping (a bug corrupting a little data each day for months).

Slow, creeping corruption is the most dangerous: by the time it's noticed, it's in every recent backup and replica.

### Defense in depth

1. **First layer — soft deletion / undo**: deleted data goes to a trash/tombstone state for a retention period (days to weeks) before purge; users and support can undo. Protects against user and application errors.
2. **Second layer — backups and recovery**: versioned backups with retention long enough to catch slow corruption, stored in a separate failure domain and administrative domain (so the same bug or operator mistake can't delete both). Replication is **not** a backup — it faithfully replicates corruption and deletes.
3. **Third layer — early detection**: continuous **out-of-band validation** that checks data invariants (referential integrity, counts, checksums, business rules) and alerts on drift. Detection time is what bounds how far back you need to restore.

### Recovery

- Define **RPO** (how much data loss is tolerable) and **RTO** (how fast you must recover) per dataset, and design backups to meet them.
- **Test restores continuously** and automatically, end to end, from real backups; measure time to restore. Alert when a restore test fails.
- Support **partial/point restores** (one user, one table, one time range), not just "restore everything".
- Keep tooling and runbooks for recovery as production-grade as serving code.

## Data pipelines

### Design

- Prefer **continuous/streaming or frequent small batches** over huge periodic batches when freshness matters; big periodic jobs create load spikes ("thundering herds") and long recovery after failure.
- Make every stage **idempotent** and re-runnable; write outputs atomically (write then rename/commit).
- Define pipeline SLOs: **freshness**, **correctness**, **coverage/completeness**, and end-to-end latency (`sre-slos-and-error-budgets`).
- Handle **stragglers and hot spots**: split work into many small shards, rebalance dynamically, avoid skewed keys.
- **Schema changes and migrations**: versioned schemas, backward/forward compatible readers, dual-writes and backfills staged and verified.
- Isolate pipelines by priority so a large low-priority backfill can't starve a critical job.
- Plan dependencies: know upstream sources, their SLOs, and what happens when they are late or bad; validate inputs and quarantine bad records instead of failing whole runs or silently passing garbage.

### Operating

- Monitor: freshness/lag at each stage, throughput, backlog, error/quarantine counts, data quality checks.
- Alert on SLO (e.g. "data older than X for > Y% of reads"), not on every task failure.
- Keep runbooks for: reprocessing a time range, skipping/quarantining poison inputs, backfills, and rolling back a bad output version.
- Canary pipeline code and config changes on a subset of data and compare output against the previous version before full rollout.

## Distributed cron / scheduled jobs

- Run the scheduler itself redundantly with leader election via a consensus system, so one machine's failure doesn't skip or double-run jobs.
- Persist launch state durably: record intent **before** launching and success **after**, so a new leader can tell whether a job ran.
- Make jobs **idempotent** or have them check for prior completion; decide explicitly whether a missed run should be skipped or run late, and whether a double run is acceptable.
- **Spread start times** (jitter, hashed minutes) to avoid everyone running at :00 and overloading shared systems.
- Monitor for missed runs, overruns (job still running at next start), and failures.

## Review checklist

- [ ] RPO/RTO defined per dataset; backups meet them?
- [ ] Backups in separate failure + administrative domain; retention covers slow corruption?
- [ ] Soft-delete / undo for user-facing deletions?
- [ ] Automated, end-to-end restore tests with alerting?
- [ ] Out-of-band data validation running?
- [ ] Pipeline stages idempotent, atomic outputs, freshness/correctness SLOs?
- [ ] Scheduled jobs survive scheduler failure without skipping or double-running?

## Sources

- SRE book ch. 24 Distributed Periodic Scheduling with Cron — https://sre.google/sre-book/distributed-periodic-scheduling/
- SRE book ch. 25 Data Processing Pipelines — https://sre.google/sre-book/data-processing-pipelines/
- SRE book ch. 26 Data Integrity — https://sre.google/sre-book/data-integrity/
- Workbook ch. 13 Data Processing Pipelines — https://sre.google/workbook/data-processing/
