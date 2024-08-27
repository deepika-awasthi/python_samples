import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from workflow import TransferToHumanCSSkill, sample_activity


async def main():
	# Create a Temporal client
    client = await Client.connect("localhost:7233")

    # Create and run a worker for the TransferToHumanCSSkill workflow
    worker = Worker(
        client,
        task_queue="tq",
        workflows=[TransferToHumanCSSkill],
        activities=[sample_activity],
    )

    # Run the worker until interrupted
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
    
