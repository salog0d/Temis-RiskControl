-- ─────────────────────────────────────────────────────────────────────────────
-- Temis RiskControl — Database Schema
-- PostgreSQL 16
--
-- Tabla de creación ordenada por dependencias (sin forward references).
-- Las tablas con FK apuntan a tablas ya definidas arriba.
-- ─────────────────────────────────────────────────────────────────────────────

-- ── Extensions ───────────────────────────────────────────────────────────────

CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- gen_random_uuid()

-- ── Core: usuario ────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS usuario (
    id                           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    email                        VARCHAR     NOT NULL UNIQUE,
    telefono                     VARCHAR,
    status                       VARCHAR     NOT NULL DEFAULT 'active',
    last_login                   TIMESTAMPTZ,
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now(),
    -- Enforcement fields (populated by Action Engine)
    sessions_invalidated_at      TIMESTAMPTZ,
    transaction_rate_limited_until TIMESTAMPTZ,
    transaction_rate_limit_max   INTEGER
);

-- ── Core: cuenta ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS cuenta (
    id          UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID            NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    balance     NUMERIC(18, 2)  NOT NULL DEFAULT 0.00,
    currency    VARCHAR         NOT NULL,
    status      VARCHAR         NOT NULL DEFAULT 'active'
);

-- ── Core: dispositivo ────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS dispositivo (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID        NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    fingerprint VARCHAR     NOT NULL,
    trusted     BOOLEAN     NOT NULL DEFAULT FALSE,
    first_seen  TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ── Core: transaccion ────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS transaccion (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID            NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    from_account_id UUID            REFERENCES cuenta(id) ON DELETE SET NULL,
    to_account      VARCHAR         NOT NULL,
    amount          NUMERIC(18, 2)  NOT NULL,
    currency        VARCHAR         NOT NULL,
    status          VARCHAR         NOT NULL DEFAULT 'pending',
    ip              VARCHAR,
    device_id       UUID            REFERENCES dispositivo(id) ON DELETE SET NULL,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- ── Core: beneficiario ───────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS beneficiario (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID        NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    account_number  VARCHAR     NOT NULL,
    bank_name       VARCHAR     NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ── Risk & Fraud: risk_assessment ────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS risk_assessment (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id  UUID            NOT NULL REFERENCES transaccion(id) ON DELETE CASCADE,
    risk_score      NUMERIC(10, 4),
    risk_level      VARCHAR,
    decision        VARCHAR,
    reason          JSONB,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- ── Risk & Fraud: risk_feature ───────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS risk_feature (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id      UUID            NOT NULL REFERENCES transaccion(id) ON DELETE CASCADE,
    velocity_1m         INTEGER,
    velocity_1h         INTEGER,
    amount_zscore       NUMERIC(10, 4),
    device_trust_score  NUMERIC(10, 4),
    geo_distance_km     NUMERIC(10, 2),
    new_beneficiary     BOOLEAN,
    ip_risk_score       NUMERIC(10, 4),
    behavioral_score    NUMERIC(10, 4),
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- ── Risk & Fraud: fraud_action ───────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS fraud_action (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id  UUID        NOT NULL REFERENCES transaccion(id) ON DELETE CASCADE,
    action_type     VARCHAR     NOT NULL,
    status          VARCHAR     NOT NULL DEFAULT 'pending',
    executed_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ── Auth & Security: sesion ──────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS sesion (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID        NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    device_id   UUID        REFERENCES dispositivo(id) ON DELETE SET NULL,
    ip          VARCHAR     NOT NULL,
    country     VARCHAR,
    city        VARCHAR,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    ended_at    TIMESTAMPTZ
);

-- ── Auth & Security: otp_challenge ───────────────────────────────────────────

CREATE TABLE IF NOT EXISTS otp_challenge (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID        NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    transaction_id  UUID        REFERENCES transaccion(id) ON DELETE SET NULL,
    code_hash       VARCHAR     NOT NULL,
    channel         VARCHAR     NOT NULL,
    status          VARCHAR     NOT NULL DEFAULT 'pending',
    attempts        INTEGER     NOT NULL DEFAULT 0,
    max_attempts    INTEGER     NOT NULL DEFAULT 3,
    expires_at      TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    verified_at     TIMESTAMPTZ
);

-- ── Auth & Security: token_blacklist ─────────────────────────────────────────

CREATE TABLE IF NOT EXISTS token_blacklist (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID        REFERENCES usuario(id) ON DELETE SET NULL,
    token_jti   VARCHAR     NOT NULL UNIQUE,
    expires_at  TIMESTAMPTZ NOT NULL,
    reason      VARCHAR,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ── Auth & Security: security_event ─────────────────────────────────────────

CREATE TABLE IF NOT EXISTS security_event (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID        NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    type        VARCHAR     NOT NULL,
    metadata    JSONB,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ── Audit: audit_log ─────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS audit_log (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID        REFERENCES usuario(id) ON DELETE SET NULL,
    transaction_id  UUID        REFERENCES transaccion(id) ON DELETE SET NULL,
    action          VARCHAR     NOT NULL,
    resource        VARCHAR     NOT NULL,
    details         JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ── Infra: ip_reputation ─────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ip_reputation (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    ip              VARCHAR         NOT NULL UNIQUE,
    risk_score      NUMERIC(10, 4),
    status          VARCHAR         NOT NULL DEFAULT 'unknown',
    failed_attempts INTEGER         NOT NULL DEFAULT 0,
    last_seen       TIMESTAMPTZ,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- ── Indexes ──────────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_cuenta_user_id          ON cuenta(user_id);
CREATE INDEX IF NOT EXISTS idx_dispositivo_user_id     ON dispositivo(user_id);
CREATE INDEX IF NOT EXISTS idx_transaccion_user_id     ON transaccion(user_id);
CREATE INDEX IF NOT EXISTS idx_transaccion_created_at  ON transaccion(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_beneficiario_user_id    ON beneficiario(user_id);
CREATE INDEX IF NOT EXISTS idx_risk_assessment_txn     ON risk_assessment(transaction_id);
CREATE INDEX IF NOT EXISTS idx_risk_feature_txn        ON risk_feature(transaction_id);
CREATE INDEX IF NOT EXISTS idx_fraud_action_txn        ON fraud_action(transaction_id);
CREATE INDEX IF NOT EXISTS idx_sesion_user_id          ON sesion(user_id);
CREATE INDEX IF NOT EXISTS idx_otp_challenge_user_id   ON otp_challenge(user_id);
CREATE INDEX IF NOT EXISTS idx_security_event_user_id  ON security_event(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id       ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at    ON audit_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ip_reputation_ip        ON ip_reputation(ip);
