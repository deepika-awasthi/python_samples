from temporalio import workflow
from datetime import timedelta
from welcome_msg import WelcomeMessage
from activity import hello_activity


@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        workflow.logger.info("Running workflow with parameter %s" % name)
        return await workflow.execute_activity(
            hello_activity,
            WelcomeMessage("Hello", name),
            start_to_close_timeout=timedelta(seconds=10),
        )

