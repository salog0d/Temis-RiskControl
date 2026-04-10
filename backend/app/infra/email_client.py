import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

_TEMPLATES: dict[str, dict[str, str]] = {
    "fraud_alert": {
        "subject": "Alerta de seguridad: actividad sospechosa detectada",
        "body_html": """
<p>Hola,</p>
<p>Detectamos actividad inusual en tu cuenta y <strong>hemos bloqueado la transacción</strong>
como medida de protección.</p>
<p><strong>Motivo:</strong> {reason}</p>
<p>Si reconoces esta actividad, comunícate con soporte. Si no fuiste tú, cambia tu
contraseña de inmediato.</p>
<p>Equipo de Seguridad — Temis</p>
""",
    },
    "challenge_required": {
        "subject": "Verificación requerida para continuar",
        "body_html": """
<p>Hola,</p>
<p>Tu transacción requiere una verificación adicional antes de poder procesarse.</p>
<p><strong>Motivo:</strong> {reason}</p>
<p><strong>Método de verificación:</strong> {challenge_method}</p>
<p>Si no iniciaste esta operación, ignora este mensaje y considera cambiar tu contraseña.</p>
<p>Equipo de Seguridad — Temis</p>
""",
    },
    "account_blocked": {
        "subject": "Tu cuenta ha sido suspendida temporalmente",
        "body_html": """
<p>Hola,</p>
<p>Por tu seguridad, <strong>hemos suspendido tu cuenta</strong> y cerrado todas tus sesiones
activas.</p>
<p><strong>Motivo:</strong> {reason}</p>
<p>Para reactivar tu cuenta comunícate con nuestro equipo de soporte adjuntando
una identificación oficial.</p>
<p>Equipo de Seguridad — Temis</p>
""",
    },
    "rate_limited": {
        "subject": "Límite temporal aplicado a tus transacciones",
        "body_html": """
<p>Hola,</p>
<p>Detectamos un patrón inusual de actividad y hemos aplicado un <strong>límite temporal</strong>
en las transacciones de tu cuenta.</p>
<p><strong>Motivo:</strong> {reason}</p>
<p>El límite se levantará automáticamente una vez que el período de evaluación concluya.
Si tienes preguntas, contáctanos.</p>
<p>Equipo de Seguridad — Temis</p>
""",
    },
}

_CHALLENGE_METHOD_LABELS = {
    "otp_sms": "Código OTP por SMS",
    "otp_email": "Código OTP por correo electrónico",
    "biometric": "Verificación biométrica",
}


def _build_message(
    recipient: str,
    incident_type: str,
    reason: str,
    challenge_method: str | None,
) -> MIMEMultipart:
    template = _TEMPLATES.get(incident_type, _TEMPLATES["fraud_alert"])

    body = template["body_html"].format(
        reason=reason,
        challenge_method=_CHALLENGE_METHOD_LABELS.get(challenge_method or "", challenge_method or "N/A"),
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = template["subject"]
    msg["From"] = settings.smtp_from_address
    msg["To"] = recipient
    msg.attach(MIMEText(body, "html", "utf-8"))
    return msg


def _send_sync(recipient: str, incident_type: str, reason: str, challenge_method: str | None) -> None:
    msg = _build_message(recipient, incident_type, reason, challenge_method)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        if settings.smtp_use_tls:
            server.starttls()
        if settings.smtp_username and settings.smtp_password:
            server.login(settings.smtp_username, settings.smtp_password)
        server.sendmail(settings.smtp_from_address, [recipient], msg.as_string())


async def send_email(
    recipient: str,
    incident_type: str,
    reason: str,
    challenge_method: str | None = None,
) -> None:
    """
    Sends a security incident email to the given address.
    Runs the blocking smtplib call in a thread to avoid blocking the event loop.
    """
    await asyncio.to_thread(_send_sync, recipient, incident_type, reason, challenge_method)
