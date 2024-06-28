import logging
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
from converter import new_data_converter
import attrs
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)

@attrs.define
class my_attrs:
    test:str
    check:str

@activity.defn
async def test_type_activity(input: my_attrs) -> my_attrs:
    activity.logger.info("test activity...!!}")
    return input

@workflow.defn
class TestTypeHintWorkflow:
    @workflow.run
    async def run(self, input: my_attrs) -> my_attrs:
        return await workflow.execute_activity(
            test_type_activity, input, start_to_close_timeout=timedelta(seconds=10), result_type=my_attrs
        )

async def main():
    client = await Client.connect("localhost:7233", data_converter=new_data_converter)
    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[TestTypeHintWorkflow],
        activities=[test_type_activity]
    )
    await worker.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
