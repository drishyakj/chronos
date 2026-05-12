from app.job_handlers.telegram_handler import TelegramHandler


JOB_HANDLERS = {
    "TELEGRAM_MESSAGE": TelegramHandler()
}


class JobExecutor:

    @staticmethod
    async def execute(job):

        handler = JOB_HANDLERS.get(job.job_type)

        if not handler:
            raise Exception("Unsupported job type")

        return await handler.execute(job)