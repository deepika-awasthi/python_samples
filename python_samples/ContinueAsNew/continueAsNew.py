import asyncio
import logging

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker


@workflow.defn
class NewWorkflow:
    @workflow.run
    async def run(self, count: int) -> None:
        if count == 5:
            return
        workflow.logger.info("Running new workflow every time %s", count)
        await asyncio.sleep(1)
        workflow.continue_as_new(count + 1)


async def main():
    
    logging.basicConfig(level=logging.INFO)

    # Start client
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="continueasnewtq",
        workflows=[NewWorkflow],
    ):

        await client.execute_workflow(
            NewWorkflow.run,
            0,
            id="continueasnewwfid",
            task_queue="continueasnewtq",
        )


if __name__ == "__main__":
    asyncio.run(main())
