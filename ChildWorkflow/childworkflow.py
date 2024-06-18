import asyncio
from dataclasses import dataclass

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class Greet:
    msg: str
    name: str


@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, input: Greet) -> str:
        return f"{input.msg}, {input.name}!"


@workflow.defn
class GreetWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_child_workflow(
            HelloWorkflow.run,
            Greet("Hello", name),
            id="child-workflow",
        )


async def main():
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="parent-workflow",
        workflows=[GreetWorkflow, HelloWorkflow],
    ):
        result = await client.execute_workflow(
            GreetWorkflow.run,
            "World",
            id="parent-workflow",
            task_queue="parent-workflow",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
