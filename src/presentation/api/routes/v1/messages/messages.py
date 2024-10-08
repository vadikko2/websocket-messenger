import logging
import typing
import uuid

import cqrs
import fastapi
from fastapi import status
from fastapi_app.exception_handlers import registry

from domain import messages
from presentation import dependencies
from service import exceptions
from service.requests.messages import (
    delete_message as delete_message_request,
    apply_message as apply_message_request,
)

router = fastapi.APIRouter(prefix="", tags=["Messages"])

logger = logging.getLogger(__name__)


@router.put(
    "/receive",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=registry.get_exception_responses(
        exceptions.ChatNotFound,
        exceptions.MessageNotFound,
        exceptions.ChangeStatusAccessDonated,
    ),
)
async def apply_message_receive(
    message_id: uuid.UUID,
    account_id: typing.Text = fastapi.Depends(dependencies.get_account_id),
    mediator: cqrs.RequestMediator = fastapi.Depends(
        dependency=dependencies.request_mediator_factory,
    ),
) -> fastapi.Response:
    """
    # Apply message as received
    """
    await mediator.send(
        apply_message_request.ApplyMessage(
            applier=account_id,
            message_id=message_id,
            status=messages.MessageStatus.RECEIVED,
        ),
    )
    return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/read",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=registry.get_exception_responses(
        exceptions.ChatNotFound,
        exceptions.MessageNotFound,
        exceptions.ChangeStatusAccessDonated,
    ),
)
async def apply_message_read(
    message_id: uuid.UUID,
    account_id: typing.Text = fastapi.Depends(dependencies.get_account_id),
    mediator: cqrs.RequestMediator = fastapi.Depends(
        dependency=dependencies.request_mediator_factory,
    ),
) -> fastapi.Response:
    """
    # Apply message as read
    """
    await mediator.send(
        apply_message_request.ApplyMessage(
            applier=account_id,
            message_id=message_id,
            status=messages.MessageStatus.READ,
        ),
    )
    return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=registry.get_exception_responses(
        exceptions.ChatNotFound,
        exceptions.MessageNotFound,
        exceptions.ChangeStatusAccessDonated,
    ),
)
async def delete_message(
    message_id: uuid.UUID,
    account_id: typing.Text = fastapi.Depends(dependencies.get_account_id),
    mediator: cqrs.RequestMediator = fastapi.Depends(
        dependency=dependencies.request_mediator_factory,
    ),
) -> fastapi.Response:
    """
    # Deletes message
    """
    await mediator.send(
        delete_message_request.DeleteMessage(
            message_id=message_id,
            deleter=account_id,
        ),
    )
    return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)
