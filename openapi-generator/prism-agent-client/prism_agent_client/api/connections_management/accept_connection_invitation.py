from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.accept_connection_invitation_request import AcceptConnectionInvitationRequest
from ...models.connection import Connection
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: AcceptConnectionInvitationRequest,
) -> Dict[str, Any]:
    url = "{}/connection-invitations".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Connection, ErrorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Connection.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Connection, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: AcceptConnectionInvitationRequest,
) -> Response[Union[Connection, ErrorResponse]]:
    """Accepts an Out of Band invitation.


    Accepts an [Out of Band 2.0](https://identity.foundation/didcomm-messaging/spec/v2.0/#out-of-band-
    messages) invitation, generates a new Peer DID,
    and submits a Connection Request to the inviter.
    It returns a connection object in `ConnectionRequestPending` state, until the Connection Request is
    eventually sent to the inviter by the prism-agent's background process. The connection object state
    will then automatically move to `ConnectionRequestSent`.

    Args:
        json_body (AcceptConnectionInvitationRequest):  Example: {'invitation': 'eyJAaWQiOiIzZmE4N
            WY2NC01NzE3LTQ1NjItYjNmYy0yYzk2M2Y2NmFmYTYiLCJAdHlwZSI6Imh0dHBzOi8vZGlkY29tbS5vcmcvbXktZmF
            taWx5LzEuMC9teS1tZXNzYWdlLXR5cGUiLCJkaWQiOiJXZ1d4cXp0ck5vb0c5MlJYdnhTVFd2IiwiaW1hZ2VVcmwiO
            iJodHRwOi8vMTkyLjE2OC41Ni4xMDEvaW1nL2xvZ28uanBnIiwibGFiZWwiOiJCb2IiLCJyZWNpcGllbnRLZXlzIjp
            bIkgzQzJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInJvdXRpbmdLZXlzIjpbIkgzQ
            zJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInNlcnZpY2VFbmRwb2ludCI6Imh0dHA
            6Ly8xOTIuMTY4LjU2LjEwMTo4MDIwIn0='}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Connection, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: AcceptConnectionInvitationRequest,
) -> Optional[Union[Connection, ErrorResponse]]:
    """Accepts an Out of Band invitation.


    Accepts an [Out of Band 2.0](https://identity.foundation/didcomm-messaging/spec/v2.0/#out-of-band-
    messages) invitation, generates a new Peer DID,
    and submits a Connection Request to the inviter.
    It returns a connection object in `ConnectionRequestPending` state, until the Connection Request is
    eventually sent to the inviter by the prism-agent's background process. The connection object state
    will then automatically move to `ConnectionRequestSent`.

    Args:
        json_body (AcceptConnectionInvitationRequest):  Example: {'invitation': 'eyJAaWQiOiIzZmE4N
            WY2NC01NzE3LTQ1NjItYjNmYy0yYzk2M2Y2NmFmYTYiLCJAdHlwZSI6Imh0dHBzOi8vZGlkY29tbS5vcmcvbXktZmF
            taWx5LzEuMC9teS1tZXNzYWdlLXR5cGUiLCJkaWQiOiJXZ1d4cXp0ck5vb0c5MlJYdnhTVFd2IiwiaW1hZ2VVcmwiO
            iJodHRwOi8vMTkyLjE2OC41Ni4xMDEvaW1nL2xvZ28uanBnIiwibGFiZWwiOiJCb2IiLCJyZWNpcGllbnRLZXlzIjp
            bIkgzQzJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInJvdXRpbmdLZXlzIjpbIkgzQ
            zJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInNlcnZpY2VFbmRwb2ludCI6Imh0dHA
            6Ly8xOTIuMTY4LjU2LjEwMTo4MDIwIn0='}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Connection, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: AcceptConnectionInvitationRequest,
) -> Response[Union[Connection, ErrorResponse]]:
    """Accepts an Out of Band invitation.


    Accepts an [Out of Band 2.0](https://identity.foundation/didcomm-messaging/spec/v2.0/#out-of-band-
    messages) invitation, generates a new Peer DID,
    and submits a Connection Request to the inviter.
    It returns a connection object in `ConnectionRequestPending` state, until the Connection Request is
    eventually sent to the inviter by the prism-agent's background process. The connection object state
    will then automatically move to `ConnectionRequestSent`.

    Args:
        json_body (AcceptConnectionInvitationRequest):  Example: {'invitation': 'eyJAaWQiOiIzZmE4N
            WY2NC01NzE3LTQ1NjItYjNmYy0yYzk2M2Y2NmFmYTYiLCJAdHlwZSI6Imh0dHBzOi8vZGlkY29tbS5vcmcvbXktZmF
            taWx5LzEuMC9teS1tZXNzYWdlLXR5cGUiLCJkaWQiOiJXZ1d4cXp0ck5vb0c5MlJYdnhTVFd2IiwiaW1hZ2VVcmwiO
            iJodHRwOi8vMTkyLjE2OC41Ni4xMDEvaW1nL2xvZ28uanBnIiwibGFiZWwiOiJCb2IiLCJyZWNpcGllbnRLZXlzIjp
            bIkgzQzJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInJvdXRpbmdLZXlzIjpbIkgzQ
            zJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInNlcnZpY2VFbmRwb2ludCI6Imh0dHA
            6Ly8xOTIuMTY4LjU2LjEwMTo4MDIwIn0='}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Connection, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: AcceptConnectionInvitationRequest,
) -> Optional[Union[Connection, ErrorResponse]]:
    """Accepts an Out of Band invitation.


    Accepts an [Out of Band 2.0](https://identity.foundation/didcomm-messaging/spec/v2.0/#out-of-band-
    messages) invitation, generates a new Peer DID,
    and submits a Connection Request to the inviter.
    It returns a connection object in `ConnectionRequestPending` state, until the Connection Request is
    eventually sent to the inviter by the prism-agent's background process. The connection object state
    will then automatically move to `ConnectionRequestSent`.

    Args:
        json_body (AcceptConnectionInvitationRequest):  Example: {'invitation': 'eyJAaWQiOiIzZmE4N
            WY2NC01NzE3LTQ1NjItYjNmYy0yYzk2M2Y2NmFmYTYiLCJAdHlwZSI6Imh0dHBzOi8vZGlkY29tbS5vcmcvbXktZmF
            taWx5LzEuMC9teS1tZXNzYWdlLXR5cGUiLCJkaWQiOiJXZ1d4cXp0ck5vb0c5MlJYdnhTVFd2IiwiaW1hZ2VVcmwiO
            iJodHRwOi8vMTkyLjE2OC41Ni4xMDEvaW1nL2xvZ28uanBnIiwibGFiZWwiOiJCb2IiLCJyZWNpcGllbnRLZXlzIjp
            bIkgzQzJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInJvdXRpbmdLZXlzIjpbIkgzQ
            zJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInNlcnZpY2VFbmRwb2ludCI6Imh0dHA
            6Ly8xOTIuMTY4LjU2LjEwMTo4MDIwIn0='}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Connection, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
