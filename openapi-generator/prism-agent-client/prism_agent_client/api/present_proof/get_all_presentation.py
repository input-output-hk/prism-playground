from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.presentation_status_page import PresentationStatusPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    thid: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/present-proof/presentations".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["offset"] = offset

    params["limit"] = limit

    params["thid"] = thid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[ErrorResponse, PresentationStatusPage]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PresentationStatusPage.from_dict(response.json())

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


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, PresentationStatusPage]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    thid: Union[Unset, None, str] = UNSET,
) -> Response[Union[ErrorResponse, PresentationStatusPage]]:
    """Gets the list of proof presentation records.

     list of presentation statuses

    Args:
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        thid (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, PresentationStatusPage]]
    """

    kwargs = _get_kwargs(
        client=client,
        offset=offset,
        limit=limit,
        thid=thid,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    thid: Union[Unset, None, str] = UNSET,
) -> Optional[Union[ErrorResponse, PresentationStatusPage]]:
    """Gets the list of proof presentation records.

     list of presentation statuses

    Args:
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        thid (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, PresentationStatusPage]
    """

    return sync_detailed(
        client=client,
        offset=offset,
        limit=limit,
        thid=thid,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    thid: Union[Unset, None, str] = UNSET,
) -> Response[Union[ErrorResponse, PresentationStatusPage]]:
    """Gets the list of proof presentation records.

     list of presentation statuses

    Args:
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        thid (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, PresentationStatusPage]]
    """

    kwargs = _get_kwargs(
        client=client,
        offset=offset,
        limit=limit,
        thid=thid,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    thid: Union[Unset, None, str] = UNSET,
) -> Optional[Union[ErrorResponse, PresentationStatusPage]]:
    """Gets the list of proof presentation records.

     list of presentation statuses

    Args:
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        thid (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, PresentationStatusPage]
    """

    return (
        await asyncio_detailed(
            client=client,
            offset=offset,
            limit=limit,
            thid=thid,
        )
    ).parsed
