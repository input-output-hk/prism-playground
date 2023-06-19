from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.presentation_status import PresentationStatus
from ...types import Response


def _get_kwargs(
    presentation_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/present-proof/presentations/{presentationId}".format(client.base_url, presentationId=presentation_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[ErrorResponse, PresentationStatus]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PresentationStatus.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[ErrorResponse, PresentationStatus]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    presentation_id: str,
    *,
    client: Client,
) -> Response[Union[ErrorResponse, PresentationStatus]]:
    """Gets an existing proof presentation record by its unique identifier. More information on the error
    can be found in the response body.

     Returns an existing presentation record by id.

    Args:
        presentation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, PresentationStatus]]
    """

    kwargs = _get_kwargs(
        presentation_id=presentation_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    presentation_id: str,
    *,
    client: Client,
) -> Optional[Union[ErrorResponse, PresentationStatus]]:
    """Gets an existing proof presentation record by its unique identifier. More information on the error
    can be found in the response body.

     Returns an existing presentation record by id.

    Args:
        presentation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, PresentationStatus]
    """

    return sync_detailed(
        presentation_id=presentation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    presentation_id: str,
    *,
    client: Client,
) -> Response[Union[ErrorResponse, PresentationStatus]]:
    """Gets an existing proof presentation record by its unique identifier. More information on the error
    can be found in the response body.

     Returns an existing presentation record by id.

    Args:
        presentation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, PresentationStatus]]
    """

    kwargs = _get_kwargs(
        presentation_id=presentation_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    presentation_id: str,
    *,
    client: Client,
) -> Optional[Union[ErrorResponse, PresentationStatus]]:
    """Gets an existing proof presentation record by its unique identifier. More information on the error
    can be found in the response body.

     Returns an existing presentation record by id.

    Args:
        presentation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, PresentationStatus]
    """

    return (
        await asyncio_detailed(
            presentation_id=presentation_id,
            client=client,
        )
    ).parsed
