import asyncio
from temporalio.client import Client
from models import TransferToHumanCSSkillParamsAndArgs, TransferToHumanCSSkillArgs, TransferToHumanCSSkillParams, LlmProviders
from workflow import TransferToHumanCSSkill


async def start_workflow():
    client = await Client.connect("localhost:7233")
    
    # Define workflow parameters and arguments
    skill_args = TransferToHumanCSSkillArgs(
        account_id="account",
        conversation_id="conv",
        chat_history="Sample chat history",
        time_para_receber="some-time",
        locale="en-US"
    )
    
    skill_params = TransferToHumanCSSkillParams()
    
    skill_data = TransferToHumanCSSkillParamsAndArgs(
        flavoredSkillId="some-id",
        organization_slug="some-slug",
        secrets={"key": "secret-value"},
        llm_provider=LlmProviders.OPENAI,
        args=skill_args,
        params=skill_params
    )
    
    # Start the workflow
    result = await client.start_workflow(
        TransferToHumanCSSkill.run,
        skill_data,  # Workflow input
        id="id",
        task_queue="tq"
    )
    
    print(f"Workflow started with result: {result}")

if __name__ == "__main__":
    asyncio.run(start_workflow())
