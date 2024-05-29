import asyncio
from temporalio.worker import Worker
from temporalio.client import Client
from workflow import HelloWorkflow
from activity import hello_activity
from client import TemporalClient

async def main():
	client = await Client.connect("localhost:7233")

	# client = await TemporalClient().get_client()

	worker = Worker(
			client,
			workflows = [HelloWorkflow],
			activities = [hello_activity],
			task_queue="hello_workflow_tq"
		)
	await worker.run()

if __name__ == "__main__":
	asyncio.run(main())