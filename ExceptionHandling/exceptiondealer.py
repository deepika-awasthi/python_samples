import asyncio
import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import NoReturn, Optional

from temporalio import activity, workflow
from temporalio.client import Client, WorkflowFailureError
from temporalio.common import RetryPolicy
from temporalio.exceptions import FailureError
from temporalio.worker import Worker


@dataclass
class CoffeeContents:
    content1: str
    content2: str


@activity.defn
async def make_coffee(input: CoffeeContents) -> NoReturn:
    raise RuntimeError(f"Greeting exception: {input.content1}, {input.content2}!")


@workflow.defn
class CoffeeWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            make_coffee,
            CoffeeContents("Milk", "GroundedCoffee"),
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="exceptiontq",
        workflows=[CoffeeWorkflow],
        activities=[make_coffee],
    ):

        try:
            await client.execute_workflow(
                CoffeeWorkflow.run,
                "COFFEE MACHINE",
                id="exceptiontq",
                task_queue="exceptiontq",
            )
        except WorkflowFailureError as err:
            append_temporal_stack(err)
            logging.exception("Got workflow failure")


def append_temporal_stack(exc: Optional[BaseException]) -> None:
    while exc:
        if (
            isinstance(exc, FailureError)
            and exc.failure
            and exc.failure.stack_trace
            and len(exc.args) == 1
            and "\nStack:\n" not in exc.args[0]
        ):
            exc.args = (f"{exc}\nStack:\n{exc.failure.stack_trace.rstrip()}",)
        exc = exc.__cause__


if __name__ == "__main__":
    asyncio.run(main())
