import asyncio

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker


@workflow.defn
class SearchWorkflow:
    @workflow.run
    async def run(self) -> None:
        # Wait a couple seconds, then alter the keyword search attribute
        await asyncio.sleep(2)
        workflow.upsert_search_attributes({"CustomKeywordField1": ["new-value"]})
        #workflow.upsert_search_attributes({"CustomKeywordField2": ["new-value-1"]})


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="custom-search-attributes-task-queue",
        workflows=[SearchWorkflow],
    ):

        # While the worker is running, use the client to start the workflow.
        # Note, in many production setups, the client would be in a completely
        # separate process from the worker.
        handle = await client.start_workflow(
            SearchWorkflow.run,
            id="custom-search-attributes-workflow-id",
            task_queue="custom-search-attributes-task-queue",
            # Start with default set of search attributes
            search_attributes={"CustomKeywordField1": ["old-value"]},
        )

        # Show search attributes before and after a few seconds
        print(
            "First search attribute values: ",
            (await handle.describe()).search_attributes.get("CustomKeywordField1"),
        )
        await asyncio.sleep(3)
        print(
            "Second search attribute values: ",
            (await handle.describe()).search_attributes.get("CustomKeywordField1"),
        )


if __name__ == "__main__":
    asyncio.run(main())
