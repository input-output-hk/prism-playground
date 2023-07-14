from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.credential_schema_response_page import CredentialSchemaResponsePage
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    author: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    version: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    order: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/schema-registry/schemas".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["author"] = author

    params["name"] = name

    params["version"] = version

    params["tags"] = tags

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
) -> Optional[Union[CredentialSchemaResponsePage, ErrorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CredentialSchemaResponsePage.from_dict(response.json())

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
) -> Response[Union[CredentialSchemaResponsePage, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    author: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    version: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    order: Union[Unset, None, str] = UNSET,
) -> Response[Union[CredentialSchemaResponsePage, ErrorResponse]]:
    """Lookup schemas by indexed fields

     Lookup schemas by `author`, `name`, `tags` parameters and control the pagination by `offset` and
    `limit` parameters

    Args:
        author (Union[Unset, None, str]):
        name (Union[Unset, None, str]):
        version (Union[Unset, None, str]):
        tags (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialSchemaResponsePage, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        author=author,
        name=name,
        version=version,
        tags=tags,
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
    author: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    version: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    order: Union[Unset, None, str] = UNSET,
) -> Optional[Union[CredentialSchemaResponsePage, ErrorResponse]]:
    """Lookup schemas by indexed fields

     Lookup schemas by `author`, `name`, `tags` parameters and control the pagination by `offset` and
    `limit` parameters

    Args:
        author (Union[Unset, None, str]):
        name (Union[Unset, None, str]):
        version (Union[Unset, None, str]):
        tags (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialSchemaResponsePage, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        author=author,
        name=name,
        version=version,
        tags=tags,
        offset=offset,
        limit=limit,
        order=order,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    author: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    version: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    order: Union[Unset, None, str] = UNSET,
) -> Response[Union[CredentialSchemaResponsePage, ErrorResponse]]:
    """Lookup schemas by indexed fields

     Lookup schemas by `author`, `name`, `tags` parameters and control the pagination by `offset` and
    `limit` parameters

    Args:
        author (Union[Unset, None, str]):
        name (Union[Unset, None, str]):
        version (Union[Unset, None, str]):
        tags (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialSchemaResponsePage, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        author=author,
        name=name,
        version=version,
        tags=tags,
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
    author: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    version: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    order: Union[Unset, None, str] = UNSET,
) -> Optional[Union[CredentialSchemaResponsePage, ErrorResponse]]:
    """Lookup schemas by indexed fields

     Lookup schemas by `author`, `name`, `tags` parameters and control the pagination by `offset` and
    `limit` parameters

    Args:
        author (Union[Unset, None, str]):
        name (Union[Unset, None, str]):
        version (Union[Unset, None, str]):
        tags (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        order (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialSchemaResponsePage, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            author=author,
            name=name,
            version=version,
            tags=tags,
            offset=offset,
            limit=limit,
            order=order,
        )
    ).parsed
