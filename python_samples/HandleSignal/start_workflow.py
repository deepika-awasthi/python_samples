import asyncio
from temporalio.client import Client
from signalwf import MySignalWorkflow


async def main():
	client = await Client.connect("localhost:7233")
	handle = await client.start_workflow(
			MySignalWorkflow.run,
			id="my-signal-workflow",
			task_queue="signal_tq",
		)

	print("after handle")
	await handle.signal(MySignalWorkflow.submit_pending_task, "task-1")
	await handle.signal(MySignalWorkflow.submit_pending_task, "task-2")
	await handle.signal(MySignalWorkflow.submit_pending_task, "task-3")
	await handle.signal("my tests signal", "task-4")

	asyncio.sleep(20)
	await handle.signal(MySignalWorkflow.exit)
	result = await handle.result()

	print(result)


if __name__=="__main__":
	asyncio.run(main())