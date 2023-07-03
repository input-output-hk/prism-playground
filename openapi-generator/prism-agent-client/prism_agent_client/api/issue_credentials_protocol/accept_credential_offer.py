from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.accept_credential_offer_request import AcceptCredentialOfferRequest
from ...models.error_response import ErrorResponse
from ...models.issue_credential_record import IssueCredentialRecord
from ...types import Response


def _get_kwargs(
    record_id: str,
    *,
    client: Client,
    json_body: AcceptCredentialOfferRequest,
) -> Dict[str, Any]:
    url = "{}/issue-credentials/records/{recordId}/accept-offer".format(client.base_url, recordId=record_id)

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
) -> Optional[Union[ErrorResponse, IssueCredentialRecord]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = IssueCredentialRecord.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, IssueCredentialRecord]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    record_id: str,
    *,
    client: Client,
    json_body: AcceptCredentialOfferRequest,
) -> Response[Union[ErrorResponse, IssueCredentialRecord]]:
    """As a holder, accepts a credential offer received from an issuer.

     Accepts a credential offer received from a VC issuer and sends back a credential request.

    Args:
        record_id (str):
        json_body (AcceptCredentialOfferRequest):  Example: {'subjectId':
            'did:prism:3bb0505d13fcb04d28a48234edb27b0d4e6d7e18a81e2c1abab58f3bbc21ce6f'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, IssueCredentialRecord]]
    """

    kwargs = _get_kwargs(
        record_id=record_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    record_id: str,
    *,
    client: Client,
    json_body: AcceptCredentialOfferRequest,
) -> Optional[Union[ErrorResponse, IssueCredentialRecord]]:
    """As a holder, accepts a credential offer received from an issuer.

     Accepts a credential offer received from a VC issuer and sends back a credential request.

    Args:
        record_id (str):
        json_body (AcceptCredentialOfferRequest):  Example: {'subjectId':
            'did:prism:3bb0505d13fcb04d28a48234edb27b0d4e6d7e18a81e2c1abab58f3bbc21ce6f'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, IssueCredentialRecord]
    """

    return sync_detailed(
        record_id=record_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    record_id: str,
    *,
    client: Client,
    json_body: AcceptCredentialOfferRequest,
) -> Response[Union[ErrorResponse, IssueCredentialRecord]]:
    """As a holder, accepts a credential offer received from an issuer.

     Accepts a credential offer received from a VC issuer and sends back a credential request.

    Args:
        record_id (str):
        json_body (AcceptCredentialOfferRequest):  Example: {'subjectId':
            'did:prism:3bb0505d13fcb04d28a48234edb27b0d4e6d7e18a81e2c1abab58f3bbc21ce6f'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, IssueCredentialRecord]]
    """

    kwargs = _get_kwargs(
        record_id=record_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    record_id: str,
    *,
    client: Client,
    json_body: AcceptCredentialOfferRequest,
) -> Optional[Union[ErrorResponse, IssueCredentialRecord]]:
    """As a holder, accepts a credential offer received from an issuer.

     Accepts a credential offer received from a VC issuer and sends back a credential request.

    Args:
        record_id (str):
        json_body (AcceptCredentialOfferRequest):  Example: {'subjectId':
            'did:prism:3bb0505d13fcb04d28a48234edb27b0d4e6d7e18a81e2c1abab58f3bbc21ce6f'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, IssueCredentialRecord]
    """

    return (
        await asyncio_detailed(
            record_id=record_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
