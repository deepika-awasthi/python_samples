# workflow.py
from temporalio import workflow, activity
from models import TransferToHumanCSSkillParamsAndArgs
from datetime import timedelta
from temporalio.common import RetryPolicy



@workflow.defn
class TransferToHumanCSSkill:
    @workflow.run
    async def run(self, skill_data: TransferToHumanCSSkillParamsAndArgs):
        args = skill_data.args

        # Log the initial workflow execution details
        print(f"Running workflow for account {args.account_id} with conversation {args.conversation_id}")

        # Define the activity's retry policy
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            backoff_coefficient=2.0,
            maximum_attempts=3
        )

        # Execute the sample activity
        result = await workflow.execute_activity(
            sample_activity,  # Activity function to execute
            args.chat_history,  # Argument to pass to the activity
            start_to_close_timeout=timedelta(seconds=10),  # Activity timeout
            retry_policy=retry_policy  # Optional retry policy
        )

        # Log the result of the activity
        print(f"Activity result: {result}")

        # Return the result (optional)
        return result
    

@activity.defn
async def sample_activity(param: str) -> str:
    return f"Processed: {param}"