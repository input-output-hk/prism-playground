from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.did_operation_response import DIDOperationResponse
from ...models.error_response import ErrorResponse
from ...models.update_managed_did_request import UpdateManagedDIDRequest
from ...types import Response


def _get_kwargs(
    did_ref: str,
    *,
    client: Client,
    json_body: UpdateManagedDIDRequest,
) -> Dict[str, Any]:
    url = "{}/did-registrar/dids/{didRef}/updates".format(client.base_url, didRef=did_ref)

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[DIDOperationResponse, ErrorResponse]]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = DIDOperationResponse.from_dict(response.json())

        return response_202
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[DIDOperationResponse, ErrorResponse]]:
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
    json_body: UpdateManagedDIDRequest,
) -> Response[Union[DIDOperationResponse, ErrorResponse]]:
    """Update DID in Prism Agent's wallet and post update operation to the VDR

     Update DID in Prism Agent's wallet and post update operation to the VDR.
    This endpoint updates the DID document from the last confirmed operation.
    Submitting multiple update operations without waiting for confirmation will result in
    some operations being rejected as only one operation is allowed to be appended to the last confirmed
    operation.

    Args:
        did_ref (str):
        json_body (UpdateManagedDIDRequest):  Example: {'actions': [{'actionType': None,
            'removeKey': {'id': 'id'}, 'removeService': {'id': 'id'}, 'addService': {'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type':
            'LinkedDomains'}, 'updateService': {'id': 'service-1', 'serviceEndpoint':
            ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, 'addKey': {'purpose':
            'authentication', 'id': 'key-1'}}, {'actionType': None, 'removeKey': {'id': 'id'},
            'removeService': {'id': 'id'}, 'addService': {'id': 'service-1', 'serviceEndpoint':
            ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, 'updateService': {'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type':
            'LinkedDomains'}, 'addKey': {'purpose': 'authentication', 'id': 'key-1'}}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DIDOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        did_ref=did_ref,
        client=client,
        json_body=json_body,
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
    json_body: UpdateManagedDIDRequest,
) -> Optional[Union[DIDOperationResponse, ErrorResponse]]:
    """Update DID in Prism Agent's wallet and post update operation to the VDR

     Update DID in Prism Agent's wallet and post update operation to the VDR.
    This endpoint updates the DID document from the last confirmed operation.
    Submitting multiple update operations without waiting for confirmation will result in
    some operations being rejected as only one operation is allowed to be appended to the last confirmed
    operation.

    Args:
        did_ref (str):
        json_body (UpdateManagedDIDRequest):  Example: {'actions': [{'actionType': None,
            'removeKey': {'id': 'id'}, 'removeService': {'id': 'id'}, 'addService': {'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type':
            'LinkedDomains'}, 'updateService': {'id': 'service-1', 'serviceEndpoint':
            ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, 'addKey': {'purpose':
            'authentication', 'id': 'key-1'}}, {'actionType': None, 'removeKey': {'id': 'id'},
            'removeService': {'id': 'id'}, 'addService': {'id': 'service-1', 'serviceEndpoint':
            ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, 'updateService': {'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type':
            'LinkedDomains'}, 'addKey': {'purpose': 'authentication', 'id': 'key-1'}}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DIDOperationResponse, ErrorResponse]
    """

    return sync_detailed(
        did_ref=did_ref,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    did_ref: str,
    *,
    client: Client,
    json_body: UpdateManagedDIDRequest,
) -> Response[Union[DIDOperationResponse, ErrorResponse]]:
    """Update DID in Prism Agent's wallet and post update operation to the VDR

     Update DID in Prism Agent's wallet and post update operation to the VDR.
    This endpoint updates the DID document from the last confirmed operation.
    Submitting multiple update operations without waiting for confirmation will result in
    some operations being rejected as only one operation is allowed to be appended to the last confirmed
    operation.

    Args:
        did_ref (str):
        json_body (UpdateManagedDIDRequest):  Example: {'actions': [{'actionType': None,
            'removeKey': {'id': 'id'}, 'removeService': {'id': 'id'}, 'addService': {'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type':
            'LinkedDomains'}, 'updateService': {'id': 'service-1', 'serviceEndpoint':
            ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, 'addKey': {'purpose':
            'authentication', 'id': 'key-1'}}, {'actionType': None, 'removeKey': {'id': 'id'},
            'removeService': {'id': 'id'}, 'addService': {'id': 'service-1', 'serviceEndpoint':
            ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, 'updateService': {'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type':
            'LinkedDomains'}, 'addKey': {'purpose': 'authentication', 'id': 'key-1'}}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DIDOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        did_ref=did_ref,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    did_ref: str,
    *,
    client: Client,
    json_body: UpdateManagedDIDRequest,
) -> Optional[Union[DIDOperationResponse, ErrorResponse]]:
    """Update DID in Prism Agent's wallet and post update operation to the VDR

     Update DID in Prism Agent's wallet and post update operation to the VDR.
    This endpoint updates the DID document from the last confirmed operation.
    Submitting multiple update operations without waiting for confirmation will result in
    some operations being rejected as only one operation is allowed to be appended to the last confirmed
    operation.

    Args:
        did_ref (str):
        json_body (UpdateManagedDIDRequest):  Example: {'actions': [{'actionType': None,
            'removeKey': {'id': 'id'}, 'removeService': {'id': 'id'}, 'addService': {'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type':
            'LinkedDomains'}, 'updateService': {'id': 'service-1', 'serviceEndpoint':
            ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, 'addKey': {'purpose':
            'authentication', 'id': 'key-1'}}, {'actionType': None, 'removeKey': {'id': 'id'},
            'removeService': {'id': 'id'}, 'addService': {'id': 'service-1', 'serviceEndpoint':
            ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, 'updateService': {'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type':
            'LinkedDomains'}, 'addKey': {'purpose': 'authentication', 'id': 'key-1'}}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DIDOperationResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            did_ref=did_ref,
            client=client,
            json_body=json_body,
        )
    ).parsed
