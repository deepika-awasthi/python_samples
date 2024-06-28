import json
import attrs
from typing import Any, Optional, Type, List

# from pydantic.json import pydantic_encoder
from temporalio.api.common.v1 import Payload
from temporalio.converter import (
    JSONPlainPayloadConverter,
    DataConverter
)


class AttrsPayloadConverter(JSONPlainPayloadConverter):
    """Pydantic JSON payload converter.

    This extends the :py:class:`JSONPlainPayloadConverter` to override
    :py:meth:`to_payload` using the Pydantic encoder.
    """

    def to_payloads(self, value: Any) -> Optional[Payload]:
        if attrs.has(value):
            return Payload(
                metadata={
                    "encoding": self.encoding.encode(),
                },
                data=encoding.dumps(value).encode(),
            )
        return super().to_payload(value)

    def from_payloads(self, payload: Payload, type_hint: Optional[Type] = None) -> Any:
        if (
            payload.metadata.get("encoding") == self.encoding.encode()
            and type_hint is not None
            and attrs.has(type_hint)
        ):
            return type_hint(**json.loads(payload.data.decode()))
        elif "type_hint" in payload.metadata:
            type_name = payload.metadata["type_hint"].decode()
            for cls in attrs._config._class_registry:
                if cls.__name__ == type_name:
                    return cls(**json.loads(payload.data.decode()))
        return super().from_payload(payload, type_hint)


new_data_converter = DataConverter(
    payload_converter_class=AttrsPayloadConverter
)
