import argparse
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflow1 import MyWorkflow

from activities import start, startwithtimestamp


interrupt_event = asyncio.Event()

async def main():
    parser = argparse.ArgumentParser(description="worker started running.....")
    parser.add_argument(
        "--workflow",
        help="Which workflow. Can be 'initial', 'patched', 'patch-deprecated', or 'patch-complete'",
        required=True,
        )
    args=parser.parse_args()
    if args.workflow == "initial":
        from workflow1 import MyWorkflow
    elif args.workflow == "patched":
        from workflow2 import MyWorkflow
    elif args.workflow == "patch-deprecated":
        from workflow3 import MyWorkflow
    elif args.workflow == "patch-complete":
        from workflow4 import MyWorkflow
    else:
        raise RuntimeError("Unrecognized workflow")

    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="patching-task-queue",
        workflows=[MyWorkflow],
        activities=[start, startwithtimestamp],
    ):
        # Wait until interrupted
        print("Worker started")
        await interrupt_event.wait()
        print("Shutting down")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())