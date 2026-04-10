from typing import Optional

from pydantic import BaseModel, Field


class AmountHistorySchema(BaseModel):
    mean: float = Field(..., description="User's historical mean transaction amount")
    std: float = Field(..., description="User's historical standard deviation of amounts")


class VelocitySchema(BaseModel):
    count_in_window: int = Field(..., description="Transaction count in the observation window")
    window_minutes: int = Field(default=60, description="Window length in minutes")
    baseline_rate_per_hour: float = Field(default=1.0, description="User's normal hourly rate")


class DeviceSchema(BaseModel):
    device_id: str
    is_known: bool = Field(..., description="Whether the device has been seen before")
    age_days: int = Field(default=0, description="Days since device was first seen")
    fraud_flags_count: int = Field(default=0, description="Fraud flags linked to the device")


class GeolocationSchema(BaseModel):
    latitude: float
    longitude: float
    prev_latitude: Optional[float] = Field(default=None, description="Previous transaction latitude")
    prev_longitude: Optional[float] = Field(default=None, description="Previous transaction longitude")
    time_delta_minutes: Optional[float] = Field(
        default=None, description="Minutes since previous transaction"
    )


class BeneficiarySchema(BaseModel):
    new_count_in_window: int = Field(default=0, description="New destination accounts added recently")
    window_hours: float = Field(default=24.0, description="Observation window in hours")
    baseline_new_per_day: float = Field(default=1.0, description="User's typical daily new beneficiaries")


class AccountChangesSchema(BaseModel):
    password_changed_hours_ago: Optional[float] = Field(
        default=None, description="Hours since password change (None = no recent change)"
    )
    email_changed_hours_ago: Optional[float] = Field(
        default=None, description="Hours since email change (None = no recent change)"
    )
    two_fa_changed_hours_ago: Optional[float] = Field(
        default=None, description="Hours since 2FA change (None = no recent change)"
    )
    recent_otp_failures: int = Field(default=0, description="OTP failures in the last hour")


class IpSchema(BaseModel):
    address: str
    is_vpn: bool = False
    is_tor: bool = False
    is_blacklisted: bool = False
    provider_risk_score: float = Field(default=0.0, ge=0.0, le=1.0)


class NetworkSchema(BaseModel):
    fraud_network_degree: int = Field(
        default=-1,
        description="Graph distance to nearest fraud account (-1 = no connection)",
    )
    connected_flagged_accounts: int = Field(
        default=0, description="Flagged accounts in user's transaction network"
    )


class BehaviorSchema(BaseModel):
    hour_of_day_deviation: float = Field(default=0.0, ge=0.0, le=1.0)
    channel_deviation: float = Field(default=0.0, ge=0.0, le=1.0)
    interaction_pattern_deviation: float = Field(default=0.0, ge=0.0, le=1.0)


class TransactionEventRequest(BaseModel):
    transaction_id: str
    user_id: str
    account_id: str
    amount: float
    currency: str = "MXN"
    timestamp: str

    amount_history: AmountHistorySchema
    velocity: VelocitySchema
    device: DeviceSchema
    geolocation: GeolocationSchema
    beneficiaries: BeneficiarySchema
    account_changes: AccountChangesSchema
    ip: IpSchema
    network: NetworkSchema
    behavior: BehaviorSchema


class WebhookResponse(BaseModel):
    transaction_id: str
    status: str
    message: str
