#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Temis RiskControl — End-to-End Test Runner
# Sends the 4 demo payloads against the running backend and prints results.
#
# Usage:
#   chmod +x scripts/run_tests.sh
#   ./scripts/run_tests.sh [BASE_URL]
#
# BASE_URL defaults to http://localhost:8000
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
ENDPOINT="$BASE_URL/api/webhook/transaction"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

print_header() {
  echo ""
  echo -e "${CYAN}${BOLD}══════════════════════════════════════════════════════${RESET}"
  echo -e "${CYAN}${BOLD}  $1${RESET}"
  echo -e "${CYAN}${BOLD}══════════════════════════════════════════════════════${RESET}"
}

send_case() {
  local label="$1"
  local expected="$2"
  local payload="$3"

  echo ""
  echo -e "${BOLD}▶ $label${RESET}"
  echo -e "  Esperado : ${YELLOW}${expected}${RESET}"

  response=$(curl -s -w "\n%{http_code}" -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d "$payload")

  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | head -n -1)

  if [ "$http_code" = "202" ]; then
    echo -e "  HTTP     : ${GREEN}${http_code} Accepted${RESET}"
    echo -e "  Response : $(echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body")"
  else
    echo -e "  HTTP     : ${RED}${http_code}${RESET}"
    echo -e "  Response : $(echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body")"
  fi
}

# ── Health check ──────────────────────────────────────────────────────────────
print_header "Health Check"
health=$(curl -s "$BASE_URL/api/health")
echo -e "  $health"

# ── Caso 1: carlos.mendoza — riesgo bajo ─────────────────────────────────────
print_header "CASO 1 — carlos.mendoza@gmail.com | Riesgo BAJO"
send_case "Transacción normal, dispositivo conocido (iPad Air), monto consistente" \
  "APPROVE" \
  '{
    "transaction_id": "demo-carlos-01",
    "user_id": "4100d9bb-40b3-4195-af31-ef24cdd7ce4b",
    "account_id": "7af4865e-a7a3-49f1-a491-e3cae43ebdf3",
    "amount": 9500.00,
    "currency": "MXN",
    "timestamp": "2026-04-10T14:30:00Z",
    "amount_history": { "mean": 11007.0, "std": 5800.0 },
    "velocity": { "count_in_window": 1, "window_minutes": 60, "baseline_rate_per_hour": 1.0 },
    "device": { "device_id": "4d21cf55-410f-4457-9f9f-68da86204415", "is_known": true, "age_days": 210, "fraud_flags_count": 0 },
    "geolocation": { "latitude": 19.4326, "longitude": -99.1332 },
    "beneficiaries": { "new_count_in_window": 0, "window_hours": 24.0, "baseline_new_per_day": 0.5 },
    "account_changes": { "recent_otp_failures": 0 },
    "ip": { "address": "189.203.10.55", "is_vpn": false, "is_tor": false, "is_blacklisted": false, "provider_risk_score": 0.04 },
    "network": { "fraud_network_degree": -1, "connected_flagged_accounts": 0 },
    "behavior": { "hour_of_day_deviation": 0.05, "channel_deviation": 0.0, "interaction_pattern_deviation": 0.08 }
  }'

# ── Caso 2: ana.garcia — riesgo medio ────────────────────────────────────────
print_header "CASO 2 — ana.garcia@hotmail.com | Riesgo MEDIO"
send_case "Monto 4x historial a las 3am, nuevos beneficiarios" \
  "CHALLENGE" \
  '{
    "transaction_id": "demo-ana-01",
    "user_id": "77d8afdb-44ab-49cd-b7ce-0503129f0985",
    "account_id": "5addeb22-3269-493d-8fdb-28d5af2a3f36",
    "amount": 42000.00,
    "currency": "MXN",
    "timestamp": "2026-04-10T03:12:00Z",
    "amount_history": { "mean": 10932.0, "std": 6700.0 },
    "velocity": { "count_in_window": 4, "window_minutes": 60, "baseline_rate_per_hour": 1.0 },
    "device": { "device_id": "f5f6aa4b-5aac-4e92-826d-9c5ff5b1b8df", "is_known": true, "age_days": 95, "fraud_flags_count": 0 },
    "geolocation": { "latitude": 25.6866, "longitude": -100.3161 },
    "beneficiaries": { "new_count_in_window": 2, "window_hours": 24.0, "baseline_new_per_day": 0.5 },
    "account_changes": { "recent_otp_failures": 1 },
    "ip": { "address": "201.145.88.20", "is_vpn": false, "is_tor": false, "is_blacklisted": false, "provider_risk_score": 0.18 },
    "network": { "fraud_network_degree": -1, "connected_flagged_accounts": 0 },
    "behavior": { "hour_of_day_deviation": 0.82, "channel_deviation": 0.3, "interaction_pattern_deviation": 0.35 }
  }'

# ── Caso 3: andres.gomez — riesgo crítico ────────────────────────────────────
print_header "CASO 3 — andres.gomez@hotmail.com | Riesgo CRÍTICO"
send_case "Viaje imposible Monterrey→Madrid en 25 min, IP Tor+blacklist, cuenta comprometida" \
  "DECLINE + FREEZE" \
  '{
    "transaction_id": "demo-andres-01",
    "user_id": "ca584053-066e-449a-a302-835d72f01a27",
    "account_id": "e4885055-0492-4d58-8b67-447590a4eccb",
    "amount": 95000.00,
    "currency": "MXN",
    "timestamp": "2026-04-10T04:45:00Z",
    "amount_history": { "mean": 8853.0, "std": 4200.0 },
    "velocity": { "count_in_window": 7, "window_minutes": 60, "baseline_rate_per_hour": 1.0 },
    "device": { "device_id": "a0f6e6a6-e3cf-458e-9a24-d7e78a97e0c5", "is_known": false, "age_days": 0, "fraud_flags_count": 3 },
    "geolocation": {
      "latitude": 40.4168, "longitude": -3.7038,
      "prev_latitude": 25.6866, "prev_longitude": -100.3161,
      "time_delta_minutes": 25
    },
    "beneficiaries": { "new_count_in_window": 4, "window_hours": 24.0, "baseline_new_per_day": 0.5 },
    "account_changes": {
      "password_changed_hours_ago": 2.0,
      "email_changed_hours_ago": 1.5,
      "recent_otp_failures": 5
    },
    "ip": { "address": "185.220.101.5", "is_vpn": true, "is_tor": true, "is_blacklisted": true, "provider_risk_score": 0.97 },
    "network": { "fraud_network_degree": 1, "connected_flagged_accounts": 3 },
    "behavior": { "hour_of_day_deviation": 0.95, "channel_deviation": 0.91, "interaction_pattern_deviation": 0.96 }
  }'

# ── Caso 4: diego.medina — falso positivo ────────────────────────────────────
print_header "CASO 4 — diego.medina@protonmail.com | Falso Positivo"
send_case "Monto alto pero historial lo justifica, Huawei P60 conocido (320 días)" \
  "APPROVE" \
  '{
    "transaction_id": "demo-diego-01",
    "user_id": "2ae78762-c223-4891-97a7-d4e0b1298927",
    "account_id": "2199ce2f-6252-4ce9-add0-a12d3f60d8b5",
    "amount": 16000.00,
    "currency": "MXN",
    "timestamp": "2026-04-10T11:00:00Z",
    "amount_history": { "mean": 11043.0, "std": 5500.0 },
    "velocity": { "count_in_window": 1, "window_minutes": 60, "baseline_rate_per_hour": 1.0 },
    "device": { "device_id": "7e59b2db-3780-46ae-a8b1-ee1c5e069a7f", "is_known": true, "age_days": 320, "fraud_flags_count": 0 },
    "geolocation": { "latitude": 19.4326, "longitude": -99.1332 },
    "beneficiaries": { "new_count_in_window": 0, "window_hours": 24.0, "baseline_new_per_day": 0.5 },
    "account_changes": { "recent_otp_failures": 0 },
    "ip": { "address": "187.190.44.12", "is_vpn": false, "is_tor": false, "is_blacklisted": false, "provider_risk_score": 0.03 },
    "network": { "fraud_network_degree": -1, "connected_flagged_accounts": 0 },
    "behavior": { "hour_of_day_deviation": 0.06, "channel_deviation": 0.04, "interaction_pattern_deviation": 0.05 }
  }'

echo ""
echo -e "${GREEN}${BOLD}══════════════════════════════════════════════════════${RESET}"
echo -e "${GREEN}${BOLD}  Tests completados — revisa los logs del agente:${RESET}"
echo -e "${GREEN}${BOLD}  docker-compose logs agent --tail=50${RESET}"
echo -e "${GREEN}${BOLD}══════════════════════════════════════════════════════${RESET}"
echo ""
