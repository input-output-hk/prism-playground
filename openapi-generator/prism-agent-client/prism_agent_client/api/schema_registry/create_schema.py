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
    *,
    client: Client,
    json_body: CredentialSchemaInput,
) -> Dict[str, Any]:
    url = "{}/schema-registry/schemas".format(client.base_url)

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
) -> Optional[Union[CredentialSchemaResponse, ErrorResponse]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CredentialSchemaResponse.from_dict(response.json())

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
    *,
    client: Client,
    json_body: CredentialSchemaInput,
) -> Response[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Publish new schema to the schema registry

     Create the new credential schema record with metadata and internal JSON Schema on behalf of Cloud
    Agent. The credential schema will be signed by the keys of Cloud Agent and issued by the DID that
    corresponds to it.

    Args:
        json_body (CredentialSchemaInput):  Example: {'schema': {'$id': 'driving-license-1.0',
            '$schema': 'https://json-schema.org/draft/2020-12/schema', 'description': 'Driving
            License', 'type': 'object', 'properties': {'credentialSubject': {'type': 'object',
            'properties': {'emailAddress': {'type': 'string', 'format': 'email'}, 'givenName':
            {'type': 'string'}, 'familyName': {'type': 'string'}, 'dateOfIssuance': {'type':
            'datetime'}, 'drivingLicenseID': {'type': 'string'}, 'drivingClass': {'type': 'integer'},
            'required': ['emailAddress', 'familyName', 'dateOfIssuance', 'drivingLicenseID',
            'drivingClass'], 'additionalProperties': True}}}}, 'author':
            'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff', 'name':
            'DrivingLicense', 'description': 'Simple credential schema for the driving licence
            verifiable credential.', 'type': 'https://w3c-ccg.github.io/vc-json-
            schemas/schema/2.0/schema.json', 'version': '1.0.0', 'tags': ['tags', 'tags']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialSchemaResponse, ErrorResponse]]
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
    json_body: CredentialSchemaInput,
) -> Optional[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Publish new schema to the schema registry

     Create the new credential schema record with metadata and internal JSON Schema on behalf of Cloud
    Agent. The credential schema will be signed by the keys of Cloud Agent and issued by the DID that
    corresponds to it.

    Args:
        json_body (CredentialSchemaInput):  Example: {'schema': {'$id': 'driving-license-1.0',
            '$schema': 'https://json-schema.org/draft/2020-12/schema', 'description': 'Driving
            License', 'type': 'object', 'properties': {'credentialSubject': {'type': 'object',
            'properties': {'emailAddress': {'type': 'string', 'format': 'email'}, 'givenName':
            {'type': 'string'}, 'familyName': {'type': 'string'}, 'dateOfIssuance': {'type':
            'datetime'}, 'drivingLicenseID': {'type': 'string'}, 'drivingClass': {'type': 'integer'},
            'required': ['emailAddress', 'familyName', 'dateOfIssuance', 'drivingLicenseID',
            'drivingClass'], 'additionalProperties': True}}}}, 'author':
            'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff', 'name':
            'DrivingLicense', 'description': 'Simple credential schema for the driving licence
            verifiable credential.', 'type': 'https://w3c-ccg.github.io/vc-json-
            schemas/schema/2.0/schema.json', 'version': '1.0.0', 'tags': ['tags', 'tags']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialSchemaResponse, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: CredentialSchemaInput,
) -> Response[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Publish new schema to the schema registry

     Create the new credential schema record with metadata and internal JSON Schema on behalf of Cloud
    Agent. The credential schema will be signed by the keys of Cloud Agent and issued by the DID that
    corresponds to it.

    Args:
        json_body (CredentialSchemaInput):  Example: {'schema': {'$id': 'driving-license-1.0',
            '$schema': 'https://json-schema.org/draft/2020-12/schema', 'description': 'Driving
            License', 'type': 'object', 'properties': {'credentialSubject': {'type': 'object',
            'properties': {'emailAddress': {'type': 'string', 'format': 'email'}, 'givenName':
            {'type': 'string'}, 'familyName': {'type': 'string'}, 'dateOfIssuance': {'type':
            'datetime'}, 'drivingLicenseID': {'type': 'string'}, 'drivingClass': {'type': 'integer'},
            'required': ['emailAddress', 'familyName', 'dateOfIssuance', 'drivingLicenseID',
            'drivingClass'], 'additionalProperties': True}}}}, 'author':
            'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff', 'name':
            'DrivingLicense', 'description': 'Simple credential schema for the driving licence
            verifiable credential.', 'type': 'https://w3c-ccg.github.io/vc-json-
            schemas/schema/2.0/schema.json', 'version': '1.0.0', 'tags': ['tags', 'tags']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialSchemaResponse, ErrorResponse]]
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
    json_body: CredentialSchemaInput,
) -> Optional[Union[CredentialSchemaResponse, ErrorResponse]]:
    """Publish new schema to the schema registry

     Create the new credential schema record with metadata and internal JSON Schema on behalf of Cloud
    Agent. The credential schema will be signed by the keys of Cloud Agent and issued by the DID that
    corresponds to it.

    Args:
        json_body (CredentialSchemaInput):  Example: {'schema': {'$id': 'driving-license-1.0',
            '$schema': 'https://json-schema.org/draft/2020-12/schema', 'description': 'Driving
            License', 'type': 'object', 'properties': {'credentialSubject': {'type': 'object',
            'properties': {'emailAddress': {'type': 'string', 'format': 'email'}, 'givenName':
            {'type': 'string'}, 'familyName': {'type': 'string'}, 'dateOfIssuance': {'type':
            'datetime'}, 'drivingLicenseID': {'type': 'string'}, 'drivingClass': {'type': 'integer'},
            'required': ['emailAddress', 'familyName', 'dateOfIssuance', 'drivingLicenseID',
            'drivingClass'], 'additionalProperties': True}}}}, 'author':
            'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff', 'name':
            'DrivingLicense', 'description': 'Simple credential schema for the driving licence
            verifiable credential.', 'type': 'https://w3c-ccg.github.io/vc-json-
            schemas/schema/2.0/schema.json', 'version': '1.0.0', 'tags': ['tags', 'tags']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialSchemaResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
