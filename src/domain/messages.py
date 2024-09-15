import datetime
import enum
import logging
import typing
import uuid

import cqrs
import pydantic

from domain import (
    attachments as attachment_entities,
    events,
    exceptions,
    reactions as reaction_entities,
)

logger = logging.getLogger(__name__)

TOTAL_EMOJI_NUMBER = 12
EMOJI_PER_REACTOR = 3


class MessageStatus(enum.IntEnum):
    """
    Message statuses
    """

    SENT = 1
    RECEIVED = 2
    READ = 4
    DELETED = 5


class Message(pydantic.BaseModel):
    """
    Message entity
    """

    chat_id: uuid.UUID = pydantic.Field(frozen=True)
    message_id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4, frozen=True)

    sender: typing.Text = pydantic.Field(frozen=True)

    reply_to: typing.Optional[uuid.UUID] = pydantic.Field(default=None, frozen=True)

    content: typing.Text = pydantic.Field(frozen=True)
    attachments: typing.List[attachment_entities.Attachment] = pydantic.Field(
        default_factory=list,
        max_length=5,
        frozen=True,
    )
    reactions: typing.List[reaction_entities.Reaction] = pydantic.Field(
        default_factory=list,
        max_length=TOTAL_EMOJI_NUMBER,
    )
    status: MessageStatus = pydantic.Field(default=MessageStatus.SENT)

    created: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now,
        frozen=True,
    )
    updated: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now,
    )

    event_list: typing.List[cqrs.DomainEvent] = pydantic.Field(default_factory=list)

    def receive(self, receiver: typing.Text) -> None:
        self.status = MessageStatus.RECEIVED
        self.updated = datetime.datetime.now()
        logger.debug(f"Message {self.message_id} received by {receiver}")
        self.event_list.append(
            events.MessageReceived(
                chat_id=self.chat_id,
                message_id=self.message_id,
                receiver_id=receiver,
            ),
        )

    def read(self, reader: typing.Text) -> None:
        self.status = MessageStatus.READ
        self.updated = datetime.datetime.now()
        logger.debug(f"Message {self.message_id} read by {reader}")
        self.event_list.append(
            events.MessageRead(
                chat_id=self.chat_id,
                message_id=self.message_id,
                reader_id=reader,
            ),
        )

    def delete(self) -> None:
        if self.status == MessageStatus.DELETED:
            logger.debug(f"Message {self.message_id} already deleted")
            return

        self.status = MessageStatus.DELETED
        self.updated = datetime.datetime.now()
        logger.debug(f"Message {self.message_id} deleted")
        self.event_list.append(
            events.MessageDeleted(chat_id=self.chat_id, message_id=self.message_id),
        )

    def _get_reactions_per_reactor(self, reactor: typing.Text) -> int:
        """
        Returns number of reactions per reactor
        """
        return len(
            [reaction for reaction in self.reactions if reaction.reactor == reactor],
        )

    def react(self, reaction: reaction_entities.Reaction) -> None:
        """
        Reacts to message
        """
        if len(self.reactions) == TOTAL_EMOJI_NUMBER:
            raise exceptions.TooManyReactions(
                reactor=reaction.reactor,
                reaction_id=reaction.reaction_id,
                message_id=self.message_id,
            )

        if self._get_reactions_per_reactor(reaction.reactor) == EMOJI_PER_REACTOR:
            raise exceptions.TooManyReactions(
                reactor=reaction.reactor,
                reaction_id=reaction.reaction_id,
                message_id=self.message_id,
            )

        self.reactions.append(reaction)
        logger.debug(
            f"Message {self.message_id} reacted by {reaction.reactor} with {reaction.emoji}",
        )
        self.event_list.append(
            events.NewReactionAdded(
                reaction_id=reaction.reaction_id,
                reactor=reaction.reactor,
                message_id=self.message_id,
                emoji=reaction.emoji,
            ),
        )

    def unreact(self, reaction: reaction_entities.Reaction) -> None:
        """
        Unreacts from message
        """
        self.reactions.remove(reaction)
        logger.debug(
            f"Message {self.message_id} unreacted by {reaction.reactor} with {reaction.emoji}",
        )

    def get_events(self) -> typing.List[cqrs.DomainEvent]:
        """
        Returns new domain events
        """
        new_events = []
        while self.event_list:
            new_events.append(self.event_list.pop())
        return new_events

    def __hash__(self):
        return hash(self.message_id)
