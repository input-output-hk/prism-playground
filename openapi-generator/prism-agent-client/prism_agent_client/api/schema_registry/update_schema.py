from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.credential_schema_input import CredentialSchemaInput
from ...models.credential_schema_response import CredentialSchemaResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    author: str,
    id: str,
    *,
    client: Client,
    json_body: CredentialSchemaInput,
) -> Dict[str, Any]:
    url = "{}/schema-registry/{author}/{id}".format(client.base_url, author=author, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
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
    author: str,
    id: str,
    *,
    client: Client,
    json_body: CredentialSchemaInput,
) -> Response[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Publish the new version of the credential schema to the schema registry

     Publish the new version of the credential schema record with metadata and internal JSON Schema on
    behalf of Cloud Agent. The credential schema will be signed by the keys of Cloud Agent and issued by
    the DID that corresponds to it.

    Args:
        author (str):
        id (str):
        json_body (CredentialSchemaInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialSchemaResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        author=author,
        id=id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    author: str,
    id: str,
    *,
    client: Client,
    json_body: CredentialSchemaInput,
) -> Optional[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Publish the new version of the credential schema to the schema registry

     Publish the new version of the credential schema record with metadata and internal JSON Schema on
    behalf of Cloud Agent. The credential schema will be signed by the keys of Cloud Agent and issued by
    the DID that corresponds to it.

    Args:
        author (str):
        id (str):
        json_body (CredentialSchemaInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialSchemaResponse, ErrorResponse]
    """

    return sync_detailed(
        author=author,
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    author: str,
    id: str,
    *,
    client: Client,
    json_body: CredentialSchemaInput,
) -> Response[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Publish the new version of the credential schema to the schema registry

     Publish the new version of the credential schema record with metadata and internal JSON Schema on
    behalf of Cloud Agent. The credential schema will be signed by the keys of Cloud Agent and issued by
    the DID that corresponds to it.

    Args:
        author (str):
        id (str):
        json_body (CredentialSchemaInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialSchemaResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        author=author,
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    author: str,
    id: str,
    *,
    client: Client,
    json_body: CredentialSchemaInput,
) -> Optional[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Publish the new version of the credential schema to the schema registry

     Publish the new version of the credential schema record with metadata and internal JSON Schema on
    behalf of Cloud Agent. The credential schema will be signed by the keys of Cloud Agent and issued by
    the DID that corresponds to it.

    Args:
        author (str):
        id (str):
        json_body (CredentialSchemaInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialSchemaResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            author=author,
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
