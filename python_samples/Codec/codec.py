import os
import logging
from typing import Iterable, List
from google.protobuf import json_format

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from temporalio.api.common.v1 import Payload
from temporalio.converter import PayloadCodec, DefaultFailureConverterWithEncodedAttributes
from temporalio.exceptions import FailureError
from temporalio.api.failure.v1 import Failure

default_key = b"test-key-test-key-test-key-test!"
default_key_id = b"test-key-id"

class EncryptionCodec(PayloadCodec):
    def __init__(self, key_id: bytes = default_key_id, key: bytes = default_key) -> None:
        super().__init__()
        self.key_id = key_id
        self.encryptor = AESGCM(key)

    async def encode(self, payloads: Iterable[Payload]) -> List[Payload]:
        return [
            Payload(
                metadata={
                    "encoding": b"binary/encrypted",
                    "encryption_key_id": self.key_id,
                },
                data=self.encrypt(p.SerializeToString()),
            )
            for p in payloads
        ]

    async def encode_failure(self, failure: Failure) -> None:
        await super().encode_failure(failure)

        failure_size = len(failure.SerializeToString())
        log_level = (
            logging.ERROR if failure_size > 4 * 1024 else logging.WARN if failure_size > 2 * 1024 else logging.INFO
        )
        LOG.log(log_level, "Encoded failure is %d bytes: %s", failure_size, json_format.MessageToJson(failure))

    async def decode(self, payloads: Iterable[Payload]) -> List[Payload]:
        ret: List[Payload] = []
        for p in payloads:
            if p.metadata.get("encoding", b"").decode() != "binary/encrypted":
                ret.append(p)
                continue
            ret.append(Payload.FromString(self.decrypt(p.data)))
        return ret

    def encrypt(self, data: bytes) -> bytes:
        nonce = os.urandom(12)
        return nonce + self.encryptor.encrypt(nonce, data, None)

    def decrypt(self, data: bytes) -> bytes:
        return self.encryptor.decrypt(data[:12], data[12:], None)

# Set up logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
LOG.addHandler(handler)
