class BaseHandler:

    async def execute(self, job):
        raise NotImplementedError