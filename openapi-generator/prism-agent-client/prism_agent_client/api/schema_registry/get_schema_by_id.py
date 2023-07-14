from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.credential_schema_response import CredentialSchemaResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    guid: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/schema-registry/schemas/{guid}".format(client.base_url, guid=guid)

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[CredentialSchemaResponse, ErrorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CredentialSchemaResponse.from_dict(response.json())

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


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[CredentialSchemaResponse, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    guid: str,
    *,
    client: Client,
) -> Response[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Fetch the schema from the registry by `guid`

     Fetch the credential schema by the unique identifier

    Args:
        guid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialSchemaResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        guid=guid,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    guid: str,
    *,
    client: Client,
) -> Optional[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Fetch the schema from the registry by `guid`

     Fetch the credential schema by the unique identifier

    Args:
        guid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialSchemaResponse, ErrorResponse]
    """

    return sync_detailed(
        guid=guid,
        client=client,
    ).parsed


async def asyncio_detailed(
    guid: str,
    *,
    client: Client,
) -> Response[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Fetch the schema from the registry by `guid`

     Fetch the credential schema by the unique identifier

    Args:
        guid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialSchemaResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        guid=guid,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    guid: str,
    *,
    client: Client,
) -> Optional[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Fetch the schema from the registry by `guid`

     Fetch the credential schema by the unique identifier

    Args:
        guid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialSchemaResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            guid=guid,
            client=client,
        )
    ).parsed
