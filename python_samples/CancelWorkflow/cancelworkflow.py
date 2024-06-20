import asyncio
import traceback
from datetime import timedelta
from typing import NoReturn

from temporalio import activity, workflow
from temporalio.client import Client, WorkflowFailureError
from temporalio.worker import Worker


@activity.defn
async def nevercomplete() -> NoReturn:
    #Heartbeat is how cancellation is delivered from the server.
    try:
        while True:
            print("Heartbeating activity")
            activity.heartbeat()
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Activity cancelled")
        raise


@activity.defn
async def cleanup() -> None:
    print("Executing cleanup activity")


@workflow.defn
class CancellationWorkflow:
    @workflow.run
    async def run(self) -> None:
        try:
            await workflow.execute_activity(
                nevercomplete,
                start_to_close_timeout=timedelta(seconds=1000),
                heartbeat_timeout=timedelta(seconds=2),
            )
        finally:
            await workflow.execute_activity(
                cleanup, start_to_close_timeout=timedelta(seconds=5)
            )


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="cancellationtq",
        workflows=[CancellationWorkflow],
        activities=[nevercomplete, cleanup],
    ):

        handle = await client.start_workflow(
            CancellationWorkflow.run,
            id="cancellationtq",
            task_queue="cancellationtq",
        )

        await asyncio.sleep(2)

        # cancel the activity
        await handle.cancel()

        try:
            await handle.result()
            raise RuntimeError("Should not succeed")
        except WorkflowFailureError:
            print("Got expected exception: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
