import asyncio
import dataclasses
from datetime import timedelta

import temporalio.converter
from temporalio import workflow, activity
from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker

from codec import EncryptionCodec


@activity.defn
async def make_greeting(input: str) -> str:
    print(f"Invoking activity, attempt number {activity.info().attempt}")
    if activity.info().attempt == 1:
        raise ValueError("initial activity failure")
    return f"Hello, {input}.{activity.info().attempt}"

@workflow.defn(name="Workflow")
class CodecWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:

        return await workflow.execute_activity(
            make_greeting,
            "A" * 5436,
            start_to_close_timeout=timedelta(seconds=10),
        )
        # return f"Codec, {name}"


interrupt_event = asyncio.Event()


async def main():
    # Connect client
    client = await Client.connect(
        "localhost:7233",
        # Use the default converter, but change the codec
        data_converter=dataclasses.replace(
            temporalio.converter.default(), payload_codec=EncryptionCodec(), failure_converter_class=temporalio.converter.DefaultFailureConverterWithEncodedAttributes
        ),
    )

    with open("/Users/dawasthi/temporal/temporal-certs/ca.pem", "rb") as f:
        server_root_ca_cert = f.read()
        print(server_root_ca_cert)
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
        data_converter=dataclasses.replace(
            temporalio.converter.default(), payload_codec=EncryptionCodec(),
            failure_converter_class=temporalio.converter.DefaultFailureConverterWithEncodedAttributes
        ),
    )

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="encryption-task-queue",
        workflows=[CodecWorkflow],
        activities=[make_greeting],
    ):
        # Wait until interrupted
        print("Worker started, ctrl+c to exit")
        await interrupt_event.wait()
        print("Shutting down")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())