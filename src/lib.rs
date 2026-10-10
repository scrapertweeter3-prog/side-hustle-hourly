//! True hourly rate math for side hustles.
//!
//! A gig's real hourly rate is net cash after platform cuts and costs,
//! divided by hours that include the unpaid admin around the paid ones.
//! These functions compute that rate and compare gigs on it.

/// Net cash a gig leaves after the platform cut and job costs.
///
/// ```
/// let net = side_hustle_hourly::net_cash(200.0, 0.15, 40.0);
/// assert!((net - 130.0).abs() < 1e-9);
/// ```
pub fn net_cash(gross: f64, platform_cut: f64, costs: f64) -> f64 {
    gross * (1.0 - platform_cut) - costs
}

/// True hourly rate: net cash over hours, with unpaid admin hours added
/// to the paid ones.
///
/// ```
/// let rate = side_hustle_hourly::hourly_rate(130.0, 5.0, 3.0);
/// assert!((rate - 16.25).abs() < 1e-9);
/// ```
pub fn hourly_rate(net: f64, paid_hours: f64, unpaid_hours: f64) -> f64 {
    if paid_hours + unpaid_hours <= 0.0 {
        return 0.0;
    }
    net / (paid_hours + unpaid_hours)
}

/// Effective hourly rate of the better gig and how much it wins by,
/// comparing two gigs on net and hours. Returns the winner's rate and
/// the per-hour gap.
///
/// ```
/// let (best, gap) = side_hustle_hourly::compare_gigs(16.25, 12.0);
/// assert!((best - 16.25).abs() < 1e-9);
/// assert!((gap - 4.25).abs() < 1e-9);
/// ```
pub fn compare_gigs(rate_a: f64, rate_b: f64) -> (f64, f64) {
    if rate_a >= rate_b {
        (rate_a, rate_a - rate_b)
    } else {
        (rate_b, rate_b - rate_a)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn cut_and_costs_land_before_hours() {
        assert!(net_cash(200.0, 0.15, 40.0) < 200.0 - 40.0);
    }

    #[test]
    fn admin_hours_push_the_rate_down() {
        assert!(hourly_rate(130.0, 5.0, 3.0) < hourly_rate(130.0, 5.0, 0.0));
    }

    #[test]
    fn zero_hours_do_not_divide() {
        assert!(hourly_rate(100.0, 0.0, 0.0) == 0.0);
    }
}
