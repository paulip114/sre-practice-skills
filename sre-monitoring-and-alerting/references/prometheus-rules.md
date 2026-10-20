# Prometheus rule templates (multiwindow, multi-burn-rate)

Replace `myjob`, metric names and `0.001` (= 1 − SLO for 99.9%).

## Recording rules

```yaml
groups:
  - name: slo-recording
    rules:
      # Repeat for each window: 5m, 30m, 1h, 2h, 6h, 1d, 3d
      - record: job:slo_errors_per_request:ratio_rate5m
        expr: |
          sum(rate(slo_errors_total[5m])) by (job)
          /
          sum(rate(slo_requests_total[5m])) by (job)
      - record: job:slo_errors_per_request:ratio_rate1h
        expr: |
          sum(rate(slo_errors_total[1h])) by (job)
          /
          sum(rate(slo_requests_total[1h])) by (job)
      # ... 30m, 2h, 6h, 1d, 3d
```

Long windows (3d) are expensive to compute from raw series; consider building them from
shorter recorded rates, or use a tool that generates these rules (e.g. Sloth, Pyrra) from an
SLO spec.

## Alerting rules

```yaml
groups:
  - name: slo-alerts
    rules:
      - alert: ErrorBudgetBurnFast
        expr: |
          (
            job:slo_errors_per_request:ratio_rate1h{job="myjob"} > (14.4 * 0.001)
            and
            job:slo_errors_per_request:ratio_rate5m{job="myjob"} > (14.4 * 0.001)
          )
          or
          (
            job:slo_errors_per_request:ratio_rate6h{job="myjob"} > (6 * 0.001)
            and
            job:slo_errors_per_request:ratio_rate30m{job="myjob"} > (6 * 0.001)
          )
        labels:
          severity: page
        annotations:
          summary: "{{ $labels.job }} is burning error budget fast"
          runbook: "<link>"

      - alert: ErrorBudgetBurnSlow
        expr: |
          (
            job:slo_errors_per_request:ratio_rate1d{job="myjob"} > (3 * 0.001)
            and
            job:slo_errors_per_request:ratio_rate2h{job="myjob"} > (3 * 0.001)
          )
          or
          (
            job:slo_errors_per_request:ratio_rate3d{job="myjob"} > (1 * 0.001)
            and
            job:slo_errors_per_request:ratio_rate6h{job="myjob"} > (1 * 0.001)
          )
        labels:
          severity: ticket
```

Configure Alertmanager inhibition so `ErrorBudgetBurnFast` suppresses `ErrorBudgetBurnSlow`
for the same job.

## Latency SLOs

Same shape: define `slo_errors` as "requests slower than threshold" (e.g. total minus the
`le` bucket at the threshold) and reuse the rules.
