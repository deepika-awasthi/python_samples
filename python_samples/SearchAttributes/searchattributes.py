import asyncio

from temporalio import workflow
from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker


@workflow.defn
class SearchAttributesWorkflow:
    @workflow.run
    async def run(self) -> None:
        # Wait a couple seconds, then alter the keyword search attribute
        await asyncio.sleep(2)
        workflow.upsert_search_attributes({"testSA": ["new-value-1", "new-value-2"]})


async def main():

    with open("/Users/dawasthi/temporal/temporal-certs/client.pem", "rb") as f:
        client_cert = f.read()
        print(client_cert)
    #client-private-key.pem
    with open("/Users/dawasthi/temporal/temporal-certs/client.key", "rb") as f:
        client_private_key = f.read()
        print(client_private_key)
    client = await Client.connect(
        "deepika-test-namespace.a2dd6.tmprl.cloud:7233",
        namespace="deepika-test-namespace.a2dd6",
        tls=TLSConfig(
            client_cert=client_cert,
            client_private_key=client_private_key,
            # domain=domain, # TLS domain
            # server_root_ca_cert=server_root_ca_cert, # ROOT CA to validate the server cert
        ),
    )

    # Start client
    # client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="search-attributes-task-queue",
        workflows=[SearchAttributesWorkflow],
    ):

        # While the worker is running, use the client to start the workflow.
        # Note, in many production setups, the client would be in a completely
        # separate process from the worker.
        handle = await client.start_workflow(
            SearchAttributesWorkflow.run,
            id="search-attributes-workflow-id",
            task_queue="search-attributes-task-queue",
            # Start with default set of search attributes
            search_attributes={"testSA": ["old-value-1"]},
        )

        # Show search attributes before and after a few seconds
        # await asyncio.sleep(3)
        print(
            "First search attribute values: ",
            (await handle.describe()).search_attributes.get("testSA"),
        )
        await asyncio.sleep(3)
        print(
            "Second search attribute values: ",
            (await handle.describe()).search_attributes.get("testSA"),
        )


if __name__ == "__main__":
    asyncio.run(main())
