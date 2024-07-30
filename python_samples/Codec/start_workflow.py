import asyncio
import dataclasses

import temporalio.converter
from temporalio.client import Client, TLSConfig

from codec import EncryptionCodec
from start_worker import CodecWorkflow


async def main():
    # Connect client
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
    print(client)
    # client = await Client.connect(
    #     "localhost:7233",
    #     # Use the default converter, but change the codec
    #     data_converter=dataclasses.replace(
    #         temporalio.converter.default(), payload_codec=EncryptionCodec(),
    #         failure_converter_class=temporalio.converter.DefaultFailureConverterWithEncodedAttributes
    #     ),
    # )

    # Run workflow
    result = await client.execute_workflow(
        CodecWorkflow.run,
        "A" * 43,
        id=f"encryption-workflow-id",
        task_queue="encryption-task-queue",
    )
    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())