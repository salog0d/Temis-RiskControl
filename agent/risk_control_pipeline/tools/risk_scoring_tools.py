import math
from typing import Optional


def score_amount_deviation(
    transaction_amount: float,
    historical_mean: float,
    historical_std: float,
) -> dict:
    """
    Scores how anomalous the transaction amount is versus the user's historical spending
    pattern using a z-score method.

    Args:
        transaction_amount: The current transaction amount.
        historical_mean: User's historical mean transaction amount.
        historical_std: User's historical standard deviation of transaction amounts.

    Returns:
        dict with 'score' (0.0=normal, 1.0=highly anomalous) and 'detail'.
    """
    if historical_std <= 0:
        return {"score": 0.0, "detail": "Insufficient historical data (std=0)."}
    z = abs(transaction_amount - historical_mean) / historical_std
    score = round(min(1.0, z / 4.0), 4)
    return {
        "score": score,
        "detail": (
            f"z_score={z:.2f}; "
            f"amount={transaction_amount:.2f}, "
            f"mean={historical_mean:.2f}, "
            f"std={historical_std:.2f}"
        ),
    }


def score_velocity(
    transaction_count_in_window: int,
    window_minutes: int,
    baseline_rate_per_hour: float,
) -> dict:
    """
    Scores velocity risk: how many transactions occurred in a time window compared to
    the user's baseline rate. A 10x spike maps to score 1.0.

    Args:
        transaction_count_in_window: Number of transactions in the observation window.
        window_minutes: Length of the observation window in minutes.
        baseline_rate_per_hour: User's normal hourly transaction rate.

    Returns:
        dict with 'score' (0.0=normal, 1.0=extreme velocity) and 'detail'.
    """
    expected = max(baseline_rate_per_hour * (window_minutes / 60.0), 1.0)
    ratio = transaction_count_in_window / expected
    score = round(min(1.0, (ratio - 1.0) / 9.0), 4) if ratio > 1.0 else 0.0
    return {
        "score": score,
        "detail": (
            f"count={transaction_count_in_window}, "
            f"expected={expected:.2f}, "
            f"ratio={ratio:.2f}"
        ),
    }


def score_device_trust(
    is_known_device: bool,
    device_age_days: int,
    fraud_flags_count: int,
) -> dict:
    """
    Scores device trust based on prior recognition, device age, and associated fraud flags.
    Unknown devices receive a base score of 0.6; fraud flags add additional penalty.

    Args:
        is_known_device: Whether the device has been seen before for this user.
        device_age_days: Days since the device was first seen (0 = brand new).
        fraud_flags_count: Number of fraud flags linked to this device.

    Returns:
        dict with 'score' (0.0=trusted, 1.0=suspicious) and 'detail'.
    """
    if not is_known_device:
        base = 0.60
    elif device_age_days < 7:
        base = 0.35
    else:
        base = 0.0

    flag_penalty = min(0.40, fraud_flags_count * 0.20)
    score = round(min(1.0, base + flag_penalty), 4)
    return {
        "score": score,
        "detail": (
            f"known={is_known_device}, "
            f"age_days={device_age_days}, "
            f"fraud_flags={fraud_flags_count}"
        ),
    }


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))


def score_geolocation_anomaly(
    prev_latitude: float,
    prev_longitude: float,
    current_latitude: float,
    current_longitude: float,
    time_delta_minutes: float,
) -> dict:
    """
    Detects impossible travel by computing the required speed between consecutive
    transaction locations. Commercial flights reach ~900 km/h; exceeding that is
    physically impossible and maps to score 1.0.

    Args:
        prev_latitude: Latitude of the previous transaction location.
        prev_longitude: Longitude of the previous transaction location.
        current_latitude: Latitude of the current transaction location.
        current_longitude: Longitude of the current transaction location.
        time_delta_minutes: Minutes elapsed between the two events.

    Returns:
        dict with 'score' (0.0=plausible, 1.0=impossible travel) and 'detail'.
    """
    distance_km = _haversine_km(
        prev_latitude, prev_longitude, current_latitude, current_longitude
    )

    if distance_km < 1.0:
        return {"score": 0.0, "detail": f"distance={distance_km:.2f} km — same location."}

    if time_delta_minutes <= 0:
        return {
            "score": 1.0,
            "detail": f"Impossible: distance={distance_km:.2f} km in 0 minutes.",
        }

    speed_kmh = distance_km / (time_delta_minutes / 60.0)
    score = round(min(1.0, speed_kmh / 900.0), 4)
    return {
        "score": score,
        "detail": (
            f"distance={distance_km:.1f} km, "
            f"time={time_delta_minutes:.1f} min, "
            f"implied_speed={speed_kmh:.1f} km/h"
        ),
    }


def score_new_beneficiaries(
    new_beneficiaries_in_window: int,
    window_hours: float,
    baseline_new_per_day: float,
) -> dict:
    """
    Scores the risk from unusual spikes in new destination account registrations.
    Adding 5x more beneficiaries than the user's baseline within a window maps to 1.0.

    Args:
        new_beneficiaries_in_window: New destination accounts added in the window.
        window_hours: Duration of the observation window in hours.
        baseline_new_per_day: User's typical rate of new beneficiary additions per day.

    Returns:
        dict with 'score' (0.0=normal, 1.0=suspicious spike) and 'detail'.
    """
    MAX_RATIO = 5.0
    expected = max(baseline_new_per_day * (window_hours / 24.0), 0.5)
    ratio = new_beneficiaries_in_window / expected
    score = round(min(1.0, (ratio - 1.0) / (MAX_RATIO - 1.0)), 4) if ratio > 1.0 else 0.0
    return {
        "score": score,
        "detail": (
            f"new_beneficiaries={new_beneficiaries_in_window}, "
            f"expected={expected:.2f}, "
            f"ratio={ratio:.2f}"
        ),
    }


def score_account_takeover_signals(
    password_changed_hours_ago: Optional[float],
    email_changed_hours_ago: Optional[float],
    two_fa_changed_hours_ago: Optional[float],
    recent_otp_failures: int,
) -> dict:
    """
    Scores account takeover (ATO) risk based on recent sensitive account changes and
    OTP failures. Changes within the last 24 hours are weighted by recency.

    Args:
        password_changed_hours_ago: Hours since last password change (None = no recent change).
        email_changed_hours_ago: Hours since last email change (None = no recent change).
        two_fa_changed_hours_ago: Hours since last 2FA method change (None = no recent change).
        recent_otp_failures: OTP failure count in the past hour.

    Returns:
        dict with 'score' (0.0=no signals, 1.0=strong ATO indicators) and 'detail'.
    """
    total = 0.0
    signals = []

    for label, hours_ago, weight in [
        ("password_change", password_changed_hours_ago, 0.30),
        ("email_change", email_changed_hours_ago, 0.35),
        ("2fa_change", two_fa_changed_hours_ago, 0.45),
    ]:
        if hours_ago is not None and hours_ago <= 24:
            recency = 1.0 - (hours_ago / 24.0)
            contribution = weight * recency
            total += contribution
            signals.append(f"{label}={hours_ago:.1f}h_ago(+{contribution:.2f})")

    otp_contribution = min(0.40, recent_otp_failures * 0.15)
    if otp_contribution > 0:
        total += otp_contribution
        signals.append(f"otp_failures={recent_otp_failures}(+{otp_contribution:.2f})")

    score = round(min(1.0, total), 4)
    return {
        "score": score,
        "detail": "; ".join(signals) if signals else "No ATO signals detected.",
    }


def score_ip_network_risk(
    is_vpn: bool,
    is_tor: bool,
    is_blacklisted: bool,
    provider_risk_score: float = 0.0,
) -> dict:
    """
    Scores IP/network risk based on VPN, TOR, and blacklist status combined with
    an optional external provider risk score. The maximum of all signals is used.

    Args:
        is_vpn: Whether the IP is a known VPN exit node.
        is_tor: Whether the IP is a TOR exit node.
        is_blacklisted: Whether the IP appears on a known fraud/abuse blacklist.
        provider_risk_score: External IP risk score (0.0–1.0) from a risk intelligence provider.

    Returns:
        dict with 'score' (0.0=clean, 1.0=high risk) and 'detail'.
    """
    flags = []
    max_score = max(0.0, min(1.0, provider_risk_score))

    if is_tor:
        max_score = max(max_score, 0.95)
        flags.append("TOR")
    if is_blacklisted:
        max_score = max(max_score, 0.85)
        flags.append("BLACKLISTED")
    if is_vpn:
        max_score = max(max_score, 0.60)
        flags.append("VPN")

    score = round(max_score, 4)
    detail = (
        f"flags=[{', '.join(flags)}], provider_score={provider_risk_score:.2f}"
        if flags
        else f"Clean IP, provider_score={provider_risk_score:.2f}"
    )
    return {"score": score, "detail": detail}


def score_network_connectivity(
    fraud_network_degree: int,
    connected_flagged_accounts: int,
) -> dict:
    """
    Scores risk based on the account's proximity to known fraud accounts in the
    transaction graph. Degree 0 means directly transacting with a fraud account.

    Args:
        fraud_network_degree: Graph distance to nearest known fraud account
                              (0=direct, 1=one hop, 2=two hops, -1=no connection).
        connected_flagged_accounts: Number of flagged accounts in the user's network.

    Returns:
        dict with 'score' (0.0=no connection, 1.0=direct fraud network member) and 'detail'.
    """
    if fraud_network_degree < 0 and connected_flagged_accounts == 0:
        return {"score": 0.0, "detail": "No proximity to fraud accounts in network."}

    degree_scores = {0: 0.90, 1: 0.65, 2: 0.35}
    degree_score = degree_scores.get(fraud_network_degree, 0.0)
    flagged_contribution = min(0.50, connected_flagged_accounts * 0.10)
    score = round(min(1.0, degree_score + flagged_contribution * (1.0 - degree_score)), 4)
    return {
        "score": score,
        "detail": (
            f"fraud_network_degree={fraud_network_degree}, "
            f"connected_flagged={connected_flagged_accounts}"
        ),
    }


def score_behavioral_deviation(
    hour_of_day_deviation: float,
    channel_deviation: float,
    interaction_pattern_deviation: float,
) -> dict:
    """
    Scores behavioral deviation: how much the current session differs from the user's
    historical patterns across time-of-day, channel, and interaction style.
    Each input must be pre-normalized to [0.0, 1.0].

    Args:
        hour_of_day_deviation: Unusualness of the transaction hour (0.0–1.0).
        channel_deviation: Unusualness of the channel or device type (0.0–1.0).
        interaction_pattern_deviation: Unusualness of session behavior such as
                                       navigation speed or click patterns (0.0–1.0).

    Returns:
        dict with 'score' (0.0=typical, 1.0=highly atypical) and 'detail'.
    """
    weights = [0.30, 0.35, 0.35]
    values = [
        max(0.0, min(1.0, hour_of_day_deviation)),
        max(0.0, min(1.0, channel_deviation)),
        max(0.0, min(1.0, interaction_pattern_deviation)),
    ]
    score = round(sum(w * v for w, v in zip(weights, values)), 4)
    return {
        "score": score,
        "detail": (
            f"hour_deviation={values[0]:.2f}, "
            f"channel_deviation={values[1]:.2f}, "
            f"interaction_deviation={values[2]:.2f}"
        ),
    }


def compute_aggregate_risk_score(
    amount_deviation_score: float,
    velocity_score: float,
    device_trust_score: float,
    geolocation_anomaly_score: float,
    new_beneficiaries_score: float,
    account_takeover_score: float,
    ip_network_risk_score: float,
    network_connectivity_score: float,
    behavioral_deviation_score: float,
) -> dict:
    """
    Combines all individual fraud signal scores into a single aggregate risk score (0.0–1.0)
    using a weighted average. Signals with stronger predictive power receive higher weights.

    Weight distribution (total = 1.0):
      geolocation_anomaly   0.15
      account_takeover      0.15
      velocity              0.12
      device_trust          0.12
      amount_deviation      0.10
      new_beneficiaries     0.10
      ip_network_risk       0.10
      network_connectivity  0.08
      behavioral_deviation  0.08

    Args:
        amount_deviation_score: Score from score_amount_deviation (0.0–1.0).
        velocity_score: Score from score_velocity (0.0–1.0).
        device_trust_score: Score from score_device_trust (0.0–1.0).
        geolocation_anomaly_score: Score from score_geolocation_anomaly (0.0–1.0).
        new_beneficiaries_score: Score from score_new_beneficiaries (0.0–1.0).
        account_takeover_score: Score from score_account_takeover_signals (0.0–1.0).
        ip_network_risk_score: Score from score_ip_network_risk (0.0–1.0).
        network_connectivity_score: Score from score_network_connectivity (0.0–1.0).
        behavioral_deviation_score: Score from score_behavioral_deviation (0.0–1.0).

    Returns:
        dict with 'aggregate_score' (0.0–1.0), 'risk_level', and 'signal_breakdown'.
    """
    WEIGHTS = {
        "amount_deviation": 0.10,
        "velocity": 0.12,
        "device_trust": 0.12,
        "geolocation_anomaly": 0.15,
        "new_beneficiaries": 0.10,
        "account_takeover": 0.15,
        "ip_network_risk": 0.10,
        "network_connectivity": 0.08,
        "behavioral_deviation": 0.08,
    }

    scores = {
        "amount_deviation": amount_deviation_score,
        "velocity": velocity_score,
        "device_trust": device_trust_score,
        "geolocation_anomaly": geolocation_anomaly_score,
        "new_beneficiaries": new_beneficiaries_score,
        "account_takeover": account_takeover_score,
        "ip_network_risk": ip_network_risk_score,
        "network_connectivity": network_connectivity_score,
        "behavioral_deviation": behavioral_deviation_score,
    }

    aggregate = round(
        min(1.0, max(0.0, sum(WEIGHTS[k] * v for k, v in scores.items()))), 4
    )

    if aggregate < 0.30:
        risk_level = "low"
    elif aggregate < 0.55:
        risk_level = "medium"
    elif aggregate < 0.75:
        risk_level = "high"
    else:
        risk_level = "critical"

    return {
        "aggregate_score": aggregate,
        "risk_level": risk_level,
        "signal_breakdown": {k: round(v, 4) for k, v in scores.items()},
    }
