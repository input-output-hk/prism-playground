from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.verification_policy_page import VerificationPolicyPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    order: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/verification/policies".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["name"] = name

    params["offset"] = offset

    params["limit"] = limit

    params["order"] = order

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
) -> Optional[Union[ErrorResponse, VerificationPolicyPage]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = VerificationPolicyPage.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, VerificationPolicyPage]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    order: Union[Unset, None, str] = UNSET,
) -> Response[Union[ErrorResponse, VerificationPolicyPage]]:
    """Lookup verification policies by query

     Lookup verification policies by `name`, and control the pagination by `offset` and `limit`
    parameters

    Args:
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, VerificationPolicyPage]]
    """

    kwargs = _get_kwargs(
        client=client,
        name=name,
        offset=offset,
        limit=limit,
        order=order,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    order: Union[Unset, None, str] = UNSET,
) -> Optional[Union[ErrorResponse, VerificationPolicyPage]]:
    """Lookup verification policies by query

     Lookup verification policies by `name`, and control the pagination by `offset` and `limit`
    parameters

    Args:
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, VerificationPolicyPage]
    """

    return sync_detailed(
        client=client,
        name=name,
        offset=offset,
        limit=limit,
        order=order,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    order: Union[Unset, None, str] = UNSET,
) -> Response[Union[ErrorResponse, VerificationPolicyPage]]:
    """Lookup verification policies by query

     Lookup verification policies by `name`, and control the pagination by `offset` and `limit`
    parameters

    Args:
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, VerificationPolicyPage]]
    """

    kwargs = _get_kwargs(
        client=client,
        name=name,
        offset=offset,
        limit=limit,
        order=order,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    order: Union[Unset, None, str] = UNSET,
) -> Optional[Union[ErrorResponse, VerificationPolicyPage]]:
    """Lookup verification policies by query

     Lookup verification policies by `name`, and control the pagination by `offset` and `limit`
    parameters

    Args:
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, VerificationPolicyPage]
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            offset=offset,
            limit=limit,
            order=order,
        )
    ).parsed
