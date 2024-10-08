import typing
import uuid

import cqrs
import pydantic

from domain import messages as messages_entity


class GetMessages(cqrs.Request):
    chat_id: uuid.UUID
    account: typing.Text
    messages_limit: pydantic.NonNegativeInt
    latest_message_id: typing.Optional[uuid.UUID] = None


class Messages(cqrs.Response):
    messages: typing.List[messages_entity.Message] = pydantic.Field(
        default_factory=list,
    )
