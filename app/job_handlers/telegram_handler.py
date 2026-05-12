import requests

from app.job_handlers.base_handler import BaseHandler

from app.core.config import TELEGRAM_BOT_TOKEN


class TelegramHandler(BaseHandler):

    async def execute(self, job):

        payload = job.payload

        url = (
            f"https://api.telegram.org/"
            f"bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        )

        response = requests.post(
            url,
            json={
                "chat_id": payload["chat_id"],
                "text": payload["message"]
            }
        )

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()