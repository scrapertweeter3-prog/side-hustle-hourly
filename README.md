# Side-hustle-hourly - true hourly rate math for side gigs

A terminal calculator for what a side gig actually pays per hour once the
platform takes its cut, the job costs come out, and the unpaid hours around
the paid ones get counted. A $200 delivery block that costs $40 in gas and
15% in app fees, spread over 5 paid hours plus 3 unpaid waiting and
maintenance hours, is a $16.25/hr job. Run the same math on a second gig
and compare.

Python 3.8+, standard library only. No install, no network, nothing leaves
your machine.

## The method

- **Net cash** = gross x (1 - platform cut) - job costs, the money that
  actually reaches you
- **True hourly rate** = net cash / (paid hours + unpaid hours), where
  unpaid hours are the ones the app doesn't clock: waiting for orders,
  cleaning the car, emailing clients, filing the 1099
- **Gig comparison** = both gigs on true hourly rate, and the per-hour gap
  between them
- **Rate sanity line** = your state's minimum wage printed next to your
  result, so the number lands next to something real

## Usage

```
$ python3 sidehustlehourly.py --gross 200 --cut 0.15 --costs 40 \
    --paid 5 --unpaid 3
== true hourly rate
Net cash                 130.00
Hours (paid + unpaid)      8.0
True hourly rate         16.25  (minimum wage: $7.25)

$ python3 sidehustlehourly.py --gross 90 --cut 0 --costs 10 \
    --paid 3 --unpaid 1 --alt-gross 200 --alt-cut 0.15 --alt-costs 40 \
    --alt-paid 5 --alt-unpaid 3
== true hourly rate
Net cash                  80.00
Hours (paid + unpaid)       4.0
True hourly rate          20.00  (minimum wage: $7.25)
Alt gig true rate         16.25
Winner: Gig A, by $3.75/hr
```

Exit code 1 when the first gig loses the comparison, so a script can gate
it. `--json` for machine output.

## Honest limits

The tool does exact arithmetic on numbers only you supply: the platform
cut you enter has to match what the app actually took, and the unpaid-hour
estimate moves every output with it. Taxes aren't modeled (self-employment
tax hits every gig differently depending on your bracket and state);
neither are depreciation on your car, cancellation-risk downtime, or the
value of a gig you can log into at 2am versus one with assigned shifts.
The verdict compares pay only.

## Related

The same true-hourly-rate audit applied to real gig apps, ranked by payout
speed: https://extrahustles.com/gigs/apps-that-pay-daily-ranked-by-payout-speed/
When a gig's margin comes from bank bonuses instead of the work itself:
https://extrahustles.com/passive/bank-account-churning-side-income/
More hourly-rate breakdowns: https://extrahustles.com/

## License

MIT
