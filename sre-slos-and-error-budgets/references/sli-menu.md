# SLI menu by component type

Pick from here, then write each as `good events / valid events`.

## Request-driven (APIs, web frontends, RPC services)

| SLI | Good event | Notes |
|---|---|---|
| Availability | Request got a successful response (e.g. not 5xx; decide explicitly how to treat 4xx, 429, timeouts) | Exclude requests that are invalid by design, not ones that failed |
| Latency | Request completed faster than threshold T | Use 2+ thresholds (e.g. p90-ish and p99-ish) to cover the tail |
| Quality | Response served without degradation | Only needed if the service degrades gracefully (fallback content, partial results) |

## Pipeline (batch jobs, streaming processors, ETL)

| SLI | Good event | Notes |
|---|---|---|
| Freshness | Data read/served was updated within threshold T | Best counted at read time, weighted by how often users look at it |
| Correctness | Output record had the correct value | Measure with known-answer test inputs or an independent (slower) checker on a sample |
| Coverage | Batch: job processed ≥ expected volume. Streaming: record processed within window | Can miss records the pipeline never learned about |

## Storage

| SLI | Good event | Notes |
|---|---|---|
| Durability | Previously written record can be read back | Watch out: users care about *the data they want now*, which may be a tiny slice of the total |
| Availability / latency | As for request-driven, on read and write paths separately | |

## Where to measure (closest to user = best fidelity, usually most cost)

1. Application server logs/metrics — cheap; miss requests that never reach the server.
2. Load balancer metrics — usually already exists; closer to the user.
3. Black-box probers — catch network/edge failures; synthetic, limited coverage.
4. Client-side instrumentation — truest picture; needs code and its own telemetry pipeline.

Start with whatever already exists; move closer to the user when you find gaps.

## Prometheus-style examples

```promql
# Availability over 7d
sum(rate(http_requests_total{job="api",code!~"5.."}[7d]))
/
sum(rate(http_requests_total{job="api"}[7d]))

# Latency SLI: fraction of requests under 450ms (needs a histogram bucket at 0.45)
sum(rate(http_request_duration_seconds_bucket{job="api",le="0.45"}[7d]))
/
sum(rate(http_request_duration_seconds_count{job="api"}[7d]))
```

Counting slow requests directly is more accurate than reading them off histogram buckets; make sure bucket boundaries match your thresholds.
