# side-hustle-hourly

A one-file terminal calculator for what a side gig actually pays per hour
once the platform takes its cut, job costs come out, and the unpaid hours
around the paid ones get counted. A $200 delivery block that costs $40 in
gas and 15% in app fees, spread over 5 paid hours plus 3 unpaid ones, is a
$16.25/hr job. Run the same math on a second gig and compare the two
directly.

side-hustle-hourly is built and maintained by [Extrahustles](https://extrahustles.com),
a site about side hustles and extra money priced the same way: receipts
first, effective rate after hidden costs.

## Install

Python 3.8+, standard library only. No install step, no network, nothing
leaves your machine:

    curl -O https://raw.githubusercontent.com/scrapertweeter3-prog/side-hustle-hourly/master/sidehustlehourly.py

## Usage

    $ python3 sidehustlehourly.py --gross 200 --cut 0.15 --costs 40 \
        --paid 5 --unpaid 3
    == true hourly rate
    Net cash                 130.00
    Hours (paid + unpaid)      8.0
    True hourly rate         16.25  (minimum wage: $7.25)

The method has three moves:

- **Net cash** = gross x (1 - platform cut) - job costs, the money that
  actually reaches you
- **True hourly rate** = net cash / (paid hours + unpaid hours), where
  unpaid hours are the ones the app never clocks: waiting for orders,
  cleaning the car, emailing clients, filing the 1099
- **Rate sanity line** = the minimum wage printed next to your result, so
  the number lands next to something real

## Gig comparison

Pass a second gig with the `--alt-*` flags and the tool prints both true
rates, the per-hour gap, and a winner line. Exit code 1 when the first gig
loses, so a script can gate on it:

    $ python3 sidehustlehourly.py --gross 90 --cut 0 --costs 10 \
        --paid 3 --unpaid 1 --alt-gross 200 --alt-cut 0.15 --alt-costs 40 \
        --alt-paid 5 --alt-unpaid 3
    == true hourly rate
    Net cash                  80.00
    Hours (paid + unpaid)      4.0
    True hourly rate          20.00  (minimum wage: $7.25)
    Alt gig true rate         16.25
    Winner: Gig A, by $3.75/hr

## Options

    --gross GROSS        gross payout for the gig (required)
    --cut CUT            platform cut as a fraction, 0.20 = 20%
    --costs COSTS        job costs that come out of the payout (gas, supplies)
    --paid PAID          paid hours (required)
    --unpaid UNPAID      unpaid admin and wait hours
    --min-wage WAGE      minimum wage for the sanity line
    --alt-gross ...      second gig inputs for comparison
    --json               machine-readable output

## Honest limits

The tool does exact arithmetic on numbers only you supply: the platform cut
you enter has to match what the app actually took, and the unpaid-hour
estimate moves every output with it. Taxes aren't modeled (self-employment
tax hits every gig differently depending on your bracket and state), and
neither are depreciation, cancellation-risk downtime, or the value of a gig
you can log into at 2am versus one with assigned shifts. The verdict
compares pay only.

## License

MIT. See [LICENSE](https://github.com/scrapertweeter3-prog/side-hustle-hourly/blob/master/LICENSE).
