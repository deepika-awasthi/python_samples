
import asyncio
from temporalio.client import Client
from client import TemporalClient
from workflow import HelloWorkflow


async def main():
    
    #different sdk-client for workflow and worker
    client = await Client.connect("localhost:7233")

    # only single python-sdk-client for worker and workflow
    # client = await TemporalClient().get_client()



    # adding delay with timer 

    # await asyncio.sleep(30)

    result = await client.execute_workflow(
        HelloWorkflow.run,
        "temporal_python_sdk",
        id="hello_workflow_id",
        task_queue="hello_workflow_tq"
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())