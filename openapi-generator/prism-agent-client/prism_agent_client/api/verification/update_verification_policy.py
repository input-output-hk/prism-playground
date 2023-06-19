from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.verification_policy import VerificationPolicy
from ...models.verification_policy_input import VerificationPolicyInput
from ...types import UNSET, Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: VerificationPolicyInput,
    nonce: int,
) -> Dict[str, Any]:
    url = "{}/verification/policies/{id}".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["nonce"] = nonce

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[ErrorResponse, VerificationPolicy]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = VerificationPolicy.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[ErrorResponse, VerificationPolicy]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
    json_body: VerificationPolicyInput,
    nonce: int,
) -> Response[Union[ErrorResponse, VerificationPolicy]]:
    """Update the verification policy object by id

     Update the verification policy entry

    Args:
        id (str):
        nonce (int):
        json_body (VerificationPolicyInput):  Example: {'name': 'name', 'description':
            'description', 'id': '046b6c7f-0b8a-43b9-b35d-6489e6daee91', 'constraints':
            [{'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'},
            {'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, VerificationPolicy]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
        nonce=nonce,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Client,
    json_body: VerificationPolicyInput,
    nonce: int,
) -> Optional[Union[ErrorResponse, VerificationPolicy]]:
    """Update the verification policy object by id

     Update the verification policy entry

    Args:
        id (str):
        nonce (int):
        json_body (VerificationPolicyInput):  Example: {'name': 'name', 'description':
            'description', 'id': '046b6c7f-0b8a-43b9-b35d-6489e6daee91', 'constraints':
            [{'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'},
            {'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, VerificationPolicy]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
        nonce=nonce,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: VerificationPolicyInput,
    nonce: int,
) -> Response[Union[ErrorResponse, VerificationPolicy]]:
    """Update the verification policy object by id

     Update the verification policy entry

    Args:
        id (str):
        nonce (int):
        json_body (VerificationPolicyInput):  Example: {'name': 'name', 'description':
            'description', 'id': '046b6c7f-0b8a-43b9-b35d-6489e6daee91', 'constraints':
            [{'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'},
            {'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, VerificationPolicy]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
        nonce=nonce,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: VerificationPolicyInput,
    nonce: int,
) -> Optional[Union[ErrorResponse, VerificationPolicy]]:
    """Update the verification policy object by id

     Update the verification policy entry

    Args:
        id (str):
        nonce (int):
        json_body (VerificationPolicyInput):  Example: {'name': 'name', 'description':
            'description', 'id': '046b6c7f-0b8a-43b9-b35d-6489e6daee91', 'constraints':
            [{'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'},
            {'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, VerificationPolicy]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
            nonce=nonce,
        )
    ).parsed
