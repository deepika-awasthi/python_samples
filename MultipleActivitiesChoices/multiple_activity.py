import asyncio
from dataclasses import dataclass
from datetime import timedelta
from enum import IntEnum
from typing import List

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker



@activity.defn
async def eat_apples(fruit: str) -> str:
    return f"Eating apples!! "


@activity.defn
async def eat_bananas(fruit: str) -> str:
    return f"Eating bananas!! "


@activity.defn
async def eat_cherries(fruit: str) -> str:
    return f"Eating cherries!! "


@activity.defn
async def eat_oranges(fruit: str) -> str:
    return f"Eating oranges!! "


@workflow.defn
class PurchaseFruitsWorkflow:
    @workflow.run
    async def run(self, list: List[str]) -> str:
    	ordered: List[str] = []
    	for s in list:
    		if s == 'APPLE':
    			ordered.append(
    				await workflow.execute_activity(
    						eat_apples,
    						"APPLE",
    						start_to_close_timeout=timedelta(seconds=5)
    					)
    				)
    		elif s == 'BANANAS':
    			ordered.append(
    				await workflow.execute_activity(
    						eat_bananas,
    						"BANANAS",
    						start_to_close_timeout=timedelta(seconds=5)
    					)
    				)
    		elif s == 'CHERRIES':
    			ordered.append(
    				await workflow.execute_activity(
    						eat_cherries,
    						"CHERRIES",
    						start_to_close_timeout=timedelta(seconds=5)
    					)
    				)
    		elif s == 'ORANGES':
    			ordered.append(
    				await workflow.execute_activity(
    						eat_oranges,
    						"ORANGES",
    						start_to_close_timeout=timedelta(seconds=5)
    					)
    				)
    		else:
    			raise ValueError(f"Unrecognized fruit: {s}")

    	return "".join(ordered)



async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="hello-activity-choice-task-queue",
        workflows=[PurchaseFruitsWorkflow],
        activities=[eat_apples, eat_bananas, eat_cherries, eat_oranges],
    ):

        result = await client.execute_workflow(
            PurchaseFruitsWorkflow.run,
                [
                    "APPLE",
                    "BANANAS",
                    "CHERRIES",
                    "ORANGES"
                ]
            ,
            id="hello-activity-choice-workflow-id",
            task_queue="hello-activity-choice-task-queue",
        )
        print(f"Order result: {result}")


if __name__ == "__main__":
    asyncio.run(main())

