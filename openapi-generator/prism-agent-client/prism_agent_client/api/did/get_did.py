from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.did_document import DIDDocument
from ...types import Response


def _get_kwargs(
    did_ref: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/dids/{didRef}".format(client.base_url, didRef=did_ref)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[DIDDocument]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DIDDocument.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = DIDDocument.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DIDDocument.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.NOT_ACCEPTABLE:
        response_406 = DIDDocument.from_dict(response.json())

        return response_406
    if response.status_code == HTTPStatus.GONE:
        response_410 = DIDDocument.from_dict(response.json())

        return response_410
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = DIDDocument.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = DIDDocument.from_dict(response.json())

        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[DIDDocument]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    did_ref: str,
    *,
    client: Client,
) -> Response[DIDDocument]:
    """Resolve Prism DID to a W3C representation

     Resolve Prism DID to a W3C DID document representation.
    The response can be the [DID resolution result](https://w3c-ccg.github.io/did-resolution/#did-
    resolution-result)
    or [DID document representation](https://www.w3.org/TR/did-core/#representations) depending on the
    `Accept` request header.
    The response is implemented according to [resolver HTTP binding](https://w3c-ccg.github.io/did-
    resolution/#bindings-https) in the DID resolution spec.

    Args:
        did_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DIDDocument]
    """

    kwargs = _get_kwargs(
        did_ref=did_ref,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    did_ref: str,
    *,
    client: Client,
) -> Optional[DIDDocument]:
    """Resolve Prism DID to a W3C representation

     Resolve Prism DID to a W3C DID document representation.
    The response can be the [DID resolution result](https://w3c-ccg.github.io/did-resolution/#did-
    resolution-result)
    or [DID document representation](https://www.w3.org/TR/did-core/#representations) depending on the
    `Accept` request header.
    The response is implemented according to [resolver HTTP binding](https://w3c-ccg.github.io/did-
    resolution/#bindings-https) in the DID resolution spec.

    Args:
        did_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DIDDocument
    """

    return sync_detailed(
        did_ref=did_ref,
        client=client,
    ).parsed


async def asyncio_detailed(
    did_ref: str,
    *,
    client: Client,
) -> Response[DIDDocument]:
    """Resolve Prism DID to a W3C representation

     Resolve Prism DID to a W3C DID document representation.
    The response can be the [DID resolution result](https://w3c-ccg.github.io/did-resolution/#did-
    resolution-result)
    or [DID document representation](https://www.w3.org/TR/did-core/#representations) depending on the
    `Accept` request header.
    The response is implemented according to [resolver HTTP binding](https://w3c-ccg.github.io/did-
    resolution/#bindings-https) in the DID resolution spec.

    Args:
        did_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DIDDocument]
    """

    kwargs = _get_kwargs(
        did_ref=did_ref,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    did_ref: str,
    *,
    client: Client,
) -> Optional[DIDDocument]:
    """Resolve Prism DID to a W3C representation

     Resolve Prism DID to a W3C DID document representation.
    The response can be the [DID resolution result](https://w3c-ccg.github.io/did-resolution/#did-
    resolution-result)
    or [DID document representation](https://www.w3.org/TR/did-core/#representations) depending on the
    `Accept` request header.
    The response is implemented according to [resolver HTTP binding](https://w3c-ccg.github.io/did-
    resolution/#bindings-https) in the DID resolution spec.

    Args:
        did_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DIDDocument
    """

    return (
        await asyncio_detailed(
            did_ref=did_ref,
            client=client,
        )
    ).parsed
