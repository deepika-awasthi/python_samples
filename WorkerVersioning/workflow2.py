from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import start, startwithtimestamp


@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self)-> None:
        if workflow.patched("my-patch"):
            self._result = await workflow.execute_activity(
                startwithtimestamp,
                args=["deepika","hello"],
                schedule_to_close_timeout=timedelta(minutes=5),
            )
        else:
            self._result = await workflow.execute_activity(
                start,
                "hello",
                schedule_to_close_timeout=timedelta(minutes=5),
            )

    @workflow.query
    def result(self)-> str:
        return self._result