import os
from typing import Iterable, List

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from temporalio.api.common.v1 import Payload
from temporalio.converter import PayloadCodec


default_key = b"test-key-test-key-test-key-test!"
default_key_id = b"test-key-id"

class EncryptionCodec(PayloadCodec):
	def __init__(self, key_id: str = default_key_id, key: bytes = default_key) -> None:
		super().__init__()
		self.key_id = key_id 
		self.encryptor = AESGCM(key)

	async def encode(self, payloads : Iterable[Payload]) -> List[Payload]:

		return[
			Payload(
				metadata={
					"encoding": b"binary/encrypted",
					"encryption_key_id": b"cHJvamVjdHMvcHJvZHVjdGlvbi1mY2RmMDc4ZC9sb2NhdGlvbnMvZ2xvYmFsL2tleVJpbmdzL3RlbXBvcmFsL2NyeXB0b0tleXMvdGVtcG9yYWwtY29kZWM="
				},
				data=self.encrypt(p.SerializeToString()),
			)
			for p in payloads
		]

	async def decode(self, payloads : Iterable[Payload]) -> List[Payload]:
		ret : List[Payload] = []
		for p in payloads:
			if p.metadata.get("encoding", b"").decode() != "binary/encrypted":
				ret.append(p)
				continue

			# key_id = p.metadata.get(encryption-key-id, b"").decode()
			# if key_id != self.key_id:
			# 	raise ValueError(
			# 			f"Unrecognized key ID {key_id}. Current key ID is {self.key_id}."
			# 		)
			ret.append(Payload.FromString(self.decrypt(p.data)))
		return ret


	def encrypt(self, data: bytes) -> bytes:
		nonce = os.urandom(12)
		return nonce + self.encryptor.encrypt(nonce, data, None)

	def decrypt(self, data: bytes) -> bytes:
		return self.encryptor.decrypt(data[:12], data[12:], None)