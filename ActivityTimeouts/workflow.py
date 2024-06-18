from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import your_activity, YourParams


@workflow.defn
class yourWorkflow:
    @workflow.run
    async def run(self, greeting:str) -> list[str]:
        activity_timeout_result = await workflow.execute_activity(
            your_activity,
            YourParams(greeting, "Activity Timeout option"),
            start_to_close_timeout=timedelta(seconds=10),
            )

        await asyncio.sleep(10)

        activity_result = await workflow.execute_activity(
            your_activity,
            YourParams(greeting, "Retry Policy options"),
            start_to_close_timeout=timedelta(seconds=10),
            # Retry Policy
            retry_policy=RetryPolicy(
                backoff_coefficient=2.0,
                maximum_attempts=5,
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=2),
                # non_retryable_error_types=["ValueError"],
            ),
        )

        return activity_timeout_result, activity_result