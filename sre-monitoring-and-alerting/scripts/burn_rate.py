#!/usr/bin/env python3
"""Burn-rate calculator for SLO alerting.

Examples:
  # Thresholds for the recommended table at 99.9% over 30 days
  python3 burn_rate.py --slo 99.9 --period-days 30

  # Custom rows: "<budget %>:<long window hours>:<severity>"
  python3 burn_rate.py --slo 99.95 --period-days 28 --row 2:1:page --row 5:6:page --row 10:72:ticket

  # How long until a given error rate exhausts the budget?
  python3 burn_rate.py --slo 99.9 --period-days 30 --error-rate 1.5
"""
import argparse

DEFAULT_ROWS = [(2.0, 1.0, "page"), (5.0, 6.0, "page"), (10.0, 72.0, "ticket")]


def fmt_duration(hours: float) -> str:
    if hours < 1 / 60:
        return f"{hours * 3600:.0f}s"
    if hours < 1:
        return f"{hours * 60:.1f}m"
    if hours < 48:
        return f"{hours:.1f}h"
    return f"{hours / 24:.1f}d"


def parse_row(text: str):
    budget, window, severity = text.split(":")
    return float(budget), float(window), severity


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--slo", type=float, required=True, help="SLO in percent, e.g. 99.9")
    p.add_argument("--period-days", type=float, default=30, help="SLO window in days")
    p.add_argument("--row", action="append", type=parse_row, help="budget%%:long_window_hours:severity")
    p.add_argument("--error-rate", type=float, help="observed error rate in percent")
    a = p.parse_args()

    budget_ratio = 1 - a.slo / 100
    period_h = a.period_days * 24
    if budget_ratio <= 0:
        raise SystemExit("SLO must be below 100%")

    print(f"SLO {a.slo}% over {a.period_days:g} days -> error budget {budget_ratio * 100:.4g}%")
    print(f"A 100% outage exhausts the budget in {fmt_duration(budget_ratio * period_h)}\n")

    rows = a.row or DEFAULT_ROWS
    print(f"{'severity':<8} {'budget':>7} {'long':>7} {'short':>7} {'burn':>7} {'threshold':>11}")
    for budget_pct, long_h, sev in rows:
        burn = (budget_pct / 100) * period_h / long_h
        threshold = burn * budget_ratio
        short_h = long_h / 12
        warn = "  (unreachable: > 100% errors)" if threshold > 1 else ""
        print(f"{sev:<8} {budget_pct:>6g}% {fmt_duration(long_h):>7} {fmt_duration(short_h):>7} "
              f"{burn:>7.3g} {threshold * 100:>10.4g}%{warn}")

    if a.error_rate is not None:
        burn = (a.error_rate / 100) / budget_ratio
        print(f"\nError rate {a.error_rate}% = burn rate {burn:.3g}; "
              f"budget exhausted in {fmt_duration(period_h / burn) if burn > 0 else 'never'}")


if __name__ == "__main__":
    main()
