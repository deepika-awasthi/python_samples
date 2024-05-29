
import asyncio
from temporalio.client import Client
from workflow import HelloWorkflow

async def main():
    client = await Client.connect("localhost:7233")

    print(f"Client: {client}")
    
    result = await client.execute_workflow(
        HelloWorkflow.run,
        "temporal_python_sdk",
        id="hello_workflow_id",
        task_queue="hello_workflow_tq"
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())