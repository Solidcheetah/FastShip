from asgiref.sync import async_to_sync
from celery import Celery
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from twilio.rest import Client as TwilioClient

from app.config import settings, notification_settings
from app.utils import TEMPLATE_DIR

fast_mail = FastMail(
    ConnectionConfig(
        **notification_settings.model_dump(
            exclude=["TWILIO_SID", "TWILIO_AUTH_TOKEN", "TWILIO_NUMBER"]
        ),
        TEMPLATE_FOLDER=TEMPLATE_DIR,
    )
)

_send_message = async_to_sync(fast_mail.send_message)

app = Celery(
    "api_tasks",
    broker=settings.REDIS_URL(9),
    backend=settings.REDIS_URL(9),
)
client = TwilioClient(
    notification_settings.TWILIO_SID,
    notification_settings.TWILIO_AUTH_TOKEN,
)


@app.task
def send_email(
    recipients: list[str],
    subject: str,
    body: str,
):
    _send_message(
        message=MessageSchema(
            recipients=recipients,
            subject=subject,
            body=body,
            subtype=MessageType.plain,
        ),
    )


@app.task
def send_email_with_template(
    recipients: list[str],
    subject: str,
    context: dict,
    template_name: str,
):
    _send_message(
        message=MessageSchema(
            recipients=recipients,
            subject=subject,
            template_body=context,
            subtype=MessageType.html,
        ),
        template_name=template_name,
    )


@app.task
def send_sms(to: str, body: str):

    client.messages.create(
        to=to,
        from_=notification_settings.TWILIO_NUMBER,
        body=body,
    )
