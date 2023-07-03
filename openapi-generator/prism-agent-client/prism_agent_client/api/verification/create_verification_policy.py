from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.verification_policy import VerificationPolicy
from ...models.verification_policy_input import VerificationPolicyInput
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: VerificationPolicyInput,
) -> Dict[str, Any]:
    url = "{}/verification/policies".format(client.base_url)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[ErrorResponse, VerificationPolicy]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = VerificationPolicy.from_dict(response.json())

        return response_201
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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[ErrorResponse, VerificationPolicy]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: VerificationPolicyInput,
) -> Response[Union[ErrorResponse, VerificationPolicy]]:
    """Create the new verification policy

     Create the new verification policy

    Args:
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
    json_body: VerificationPolicyInput,
) -> Optional[Union[ErrorResponse, VerificationPolicy]]:
    """Create the new verification policy

     Create the new verification policy

    Args:
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
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: VerificationPolicyInput,
) -> Response[Union[ErrorResponse, VerificationPolicy]]:
    """Create the new verification policy

     Create the new verification policy

    Args:
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
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: VerificationPolicyInput,
) -> Optional[Union[ErrorResponse, VerificationPolicy]]:
    """Create the new verification policy

     Create the new verification policy

    Args:
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
            client=client,
            json_body=json_body,
        )
    ).parsed
