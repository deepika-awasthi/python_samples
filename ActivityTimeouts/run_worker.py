import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from activities import your_activity
from workflow import yourWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="your-task-queue",
        workflows=[yourWorkflow],
        activities=[your_activity],
    )
    

if __name__ == "__main__":
    asyncio.run(main())