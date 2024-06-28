import asyncio
from datetime import timedelta
from temporalio.client import Client
from converter import new_data_converter
import attrs
from worker import TestTypeHintWorkflow

@attrs.define
class my_attrs:
    test:str
    check:str


async def main():
    client = await Client.connect("localhost:7233", data_converter=new_data_converter)
    inpus = my_attrs(
        test="hints",
        check="types"
    )
    result = await client.execute_workflow(
        TestTypeHintWorkflow.run,
        inpus,
        id="test",
        task_queue="my-task-queue",
    )
    print(f"Workflow result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
