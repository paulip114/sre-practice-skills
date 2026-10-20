# Back-of-envelope estimation cheatsheet

Orders of magnitude only — always replace with measured numbers for your hardware.

## Time
- 1 day ≈ 86,400 s ≈ 10^5 s; 1 month ≈ 2.6 × 10^6 s; 1 year ≈ 3.15 × 10^7 s.
- 1M requests/day ≈ 12 QPS average. Peak is often 2–3× average (check your diurnal curve).

## Latency (approximate)
| Operation | Time |
|---|---|
| Main memory reference | ~100 ns |
| Read 1 MB sequentially from memory | ~10s of µs |
| Round trip within a datacenter | ~0.5 ms |
| SSD random read | ~0.1 ms |
| Read 1 MB sequentially from SSD | ~1 ms |
| HDD seek | ~10 ms |
| Read 1 MB sequentially from HDD | ~5–20 ms |
| Round trip within a continent | ~20–80 ms |
| Round trip intercontinental | ~100–200 ms |

## Throughput (per machine, rough)
- 10 Gbps NIC ≈ 1.25 GB/s; 25 Gbps ≈ 3 GB/s (plan to use well under line rate).
- HDD ≈ 100–200 MB/s sequential, ~100–200 random IOPS.
- SSD ≈ 0.5–3+ GB/s, 10^4–10^6 IOPS depending on type.

## Availability (downtime allowed)
| SLO | per 30 days | per year |
|---|---|---|
| 99% | 7.2 h | 3.65 d |
| 99.5% | 3.6 h | 1.83 d |
| 99.9% | 43.2 min | 8.77 h |
| 99.95% | 21.6 min | 4.38 h |
| 99.99% | 4.32 min | 52.6 min |
| 99.999% | 25.9 s | 5.26 min |

## Sizing formula
```
machines_for_resource = peak_demand_for_resource / (per_machine_capacity × target_utilization)
machines = max over CPU, memory, disk, network, IOPS
total    = machines × (1 + headroom) and enough to survive losing the largest failure domain
```

Write down every assumption next to the number it produced.
