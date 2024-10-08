import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import timedelta

# import sentry_sdk
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from interceptor import SentryInterceptor

with workflow.unsafe.imports_passed_through():
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

@dataclass
class ComposeGreetingInput:
    greeting: str
    name: str


@activity.defn
async def compose_greeting(input: ComposeGreetingInput) -> str:
    activity.logger.info("Running activity with parameter %s" % input)
    return f"{input.greeting}, {input.name}!"


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        workflow.logger.info("Running workflow with parameter %s" % name)
        return await workflow.execute_activity(
            compose_greeting,
            ComposeGreetingInput("Hello", name),
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():

    # Initialize the Sentry SDK
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
    )

    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    worker = Worker(
        client,
        task_queue="sentry-task-queue",
        workflows=[GreetingWorkflow],
        activities=[compose_greeting],
        interceptors=[
            SentryInterceptor(
                activity_error_deny_list=[], 
                workflow_error_deny_list=[], 
            )
        ],
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
