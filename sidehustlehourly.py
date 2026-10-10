#!/usr/bin/env python3
"""sidehustlehourly.py - true hourly rate math for side gigs: net cash after
platform cut and job costs, divided by hours that include the unpaid ones,
with a two-gig comparison.

The app shows the gross. The rate that decides whether a gig is worth your
evening is what lands after the cut and costs, over every hour the work
actually takes, including the ones nobody clocks. This tool runs that
arithmetic and prints the rate next to minimum wage so the number lands
next to something real.

Stdlib only. Exit codes: 0 first gig wins or no comparison, 1 first gig
loses, 2 usage error (bad numbers).
"""

import argparse
import json
import sys

MIN_WAGE = 7.25  # US federal, printed as context only


def _positive(text):
    try:
        val = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a number: {text!r}")
    if val < 0:
        raise argparse.ArgumentTypeError(f"must be >= 0, got {val}")
    return val


def net_cash(gross, cut, costs):
    return gross * (1.0 - cut) - costs


def hourly_rate(net, paid, unpaid):
    hours = paid + unpaid
    return net / hours if hours > 0 else 0.0


def main():
    p = argparse.ArgumentParser(description="true hourly rate for a side gig")
    p.add_argument("--gross", type=_positive, required=True, help="gross payout")
    p.add_argument("--cut", type=_positive, default=0.0, help="platform cut, 0.20 = 20%%")
    p.add_argument("--costs", type=_positive, default=0.0, help="job costs (gas, supplies)")
    p.add_argument("--paid", type=_positive, required=True, help="paid hours")
    p.add_argument("--unpaid", type=_positive, default=0.0, help="unpaid admin/wait hours")
    p.add_argument("--min-wage", type=_positive, default=MIN_WAGE, help="minimum wage for context")
    p.add_argument("--alt-gross", type=_positive, help="second gig gross (comparison)")
    p.add_argument("--alt-cut", type=_positive, default=0.0)
    p.add_argument("--alt-costs", type=_positive, default=0.0)
    p.add_argument("--alt-paid", type=_positive)
    p.add_argument("--alt-unpaid", type=_positive, default=0.0)
    p.add_argument("--json", action="store_true", help="machine output")
    args = p.parse_args()

    if not 0.0 <= args.cut <= 1.0:
        p.error("--cut must be between 0 and 1")
    if args.alt_gross or args.alt_paid:
        if not (args.alt_gross and args.alt_paid):
            p.error("--alt-gross and --alt-paid go together")
        if not 0.0 <= args.alt_cut <= 1.0:
            p.error("--alt-cut must be between 0 and 1")

    net = net_cash(args.gross, args.cut, args.costs)
    rate = hourly_rate(net, args.paid, args.unpaid)

    out = {
        "net_cash": round(net, 2),
        "hours": round(args.paid + args.unpaid, 2),
        "true_hourly": round(rate, 2),
        "minimum_wage": args.min_wage,
    }

    cmp_exit = 0
    if args.alt_gross:
        alt_net = net_cash(args.alt_gross, args.alt_cut, args.alt_costs)
        alt_rate = hourly_rate(alt_net, args.alt_paid, args.alt_unpaid)
        out["alt_true_hourly"] = round(alt_rate, 2)
        out["winner"] = "A" if rate >= alt_rate else "B"
        out["gap_per_hour"] = round(abs(rate - alt_rate), 2)
        if rate < alt_rate:
            cmp_exit = 1

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print("== true hourly rate")
        print(f"Net cash              {out['net_cash']:>9.2f}")
        print(f"Hours (paid + unpaid) {out['hours']:>9.1f}")
        rate_line = f"True hourly rate      {out['true_hourly']:>9.2f}"
        if args.min_wage > 0:
            rate_line += f"  (minimum wage: ${args.min_wage:.2f})"
        print(rate_line)
        if args.alt_gross:
            print(f"Alt gig true rate     {out['alt_true_hourly']:>9.2f}")
            print(f"Winner: Gig {out['winner']}, by ${out['gap_per_hour']:.2f}/hr")

    sys.exit(cmp_exit if not args.json else 0)


if __name__ == "__main__":
    main()
