from twilio.http.async_http_client import AsyncTwilioHttpClient
from twilio.rest import Client

from app.config import notification_settings


class SMSService:
    def __init__(self):
        self.client: Client | None = None

    def setup(self):
        self.client = Client(
            notification_settings.TWILIO_SID,
            notification_settings.TWILIO_AUTH_TOKEN,
            http_client=AsyncTwilioHttpClient(),
        )

    async def shutdown(self):
        if self.client:
            await self.client.http_client.close()

    async def send(self, to: str, body: str):
        await self.client.messages.create_async(
            from_=notification_settings.TWILIO_NUMBER,
            to=to,
            body=body,
        )


sms_service = SMSService()
