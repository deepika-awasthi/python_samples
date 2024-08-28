import asyncio
import random
import traceback
from datetime import timedelta
from temporalio import activity, workflow
from temporalio.client import Client, WorkflowFailureError
from temporalio.worker import Worker 
from time import sleep
from concurrent.futures import ThreadPoolExecutor

# Asynchronous
@activity.defn
async def short_acty_async() -> None:
	delay = random.uniform(0.05, 0.15)
	print(f"async activity started..")
	await asyncio.sleep(delay)
	print("async activity completed..")

# Synchronous 
@activity.defn
def short_acty_sync() -> None:
	delay = random.uniform(0.05, 0.15)
	print(f"sync activity started..")
	sleep(delay)
	print("sync activity completed..")


# Workflow
@workflow.defn
class ShortActyWorkflow:
	@workflow.run
	async def run(self) -> None:
		start_now = workflow.now()
		run_for = timedelta(seconds=5)

		while workflow.now() - start_now < run_for:

			# run activity sequentially 

			await workflow.execute_activity(
				short_acty_async, start_to_close_timeout=timedelta(seconds=10)
			)
			await workflow.execute_activity(
				short_acty_sync, start_to_close_timeout=timedelta(seconds=10)
			)

# start worker and workflow


async def main():
    
    client = await Client.connect("localhost:7233")

    t_p_executor = ThreadPoolExecutor()

    async with Worker(
        client,
        task_queue="tq",
        workflows=[ShortActyWorkflow],
        activities=[short_acty_async, short_acty_sync],
        activity_executor=t_p_executor
    ):

    
        handle = await client.start_workflow(
            ShortActyWorkflow.run,
            id="wk_id",
            task_queue="tq"
        )

        print("Workflow started..")

        # sleep 2 sec, then cancel the workflow
        await asyncio.sleep(2)
        print("cancelling workflow...")
        await handle.cancel()

        # confirm cancellation
        try:
            await handle.result()
            raise RuntimeError("not cancelled")
        except WorkflowFailureError:
            print("cancelled properly")
            print("e: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())