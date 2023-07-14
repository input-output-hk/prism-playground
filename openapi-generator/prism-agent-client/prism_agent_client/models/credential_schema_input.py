from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CredentialSchemaInput")


@attr.s(auto_attribs=True)
class CredentialSchemaInput:
    """
    Example:
        {'schema': {'$id': 'driving-license-1.0', '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'description': 'Driving License', 'type': 'object', 'properties': {'credentialSubject': {'type': 'object',
            'properties': {'emailAddress': {'type': 'string', 'format': 'email'}, 'givenName': {'type': 'string'},
            'familyName': {'type': 'string'}, 'dateOfIssuance': {'type': 'datetime'}, 'drivingLicenseID': {'type':
            'string'}, 'drivingClass': {'type': 'integer'}, 'required': ['emailAddress', 'familyName', 'dateOfIssuance',
            'drivingLicenseID', 'drivingClass'], 'additionalProperties': True}}}}, 'author':
            'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff', 'name': 'DrivingLicense',
            'description': 'Simple credential schema for the driving licence verifiable credential.', 'type':
            'https://w3c-ccg.github.io/vc-json-schemas/schema/2.0/schema.json', 'version': '1.0.0', 'tags': ['tags',
            'tags']}

    Attributes:
        name (str): A human-readable name for the credential schema. A piece of Metadata. Example: DrivingLicense.
        version (str): Denotes the revision of a given Credential Schema. It should follow semantic version convention
            to describe the impact of the schema evolution. Example: 1.0.0.
        type (str): This field resolves to a JSON schema with details about the schema metadata that applies to the
            schema. A piece of Metadata. Example: https://w3c-ccg.github.io/vc-json-schemas/schema/2.0/schema.json.
        schema (Any): Valid JSON Schema where the Credential Schema data fields are defined. A piece of Metadata
            Example: {'$id': 'driving-license-1.0', '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'description': 'Driving License', 'type': 'object', 'properties': {'credentialSubject': {'type': 'object',
            'properties': {'emailAddress': {'type': 'string', 'format': 'email'}, 'givenName': {'type': 'string'},
            'familyName': {'type': 'string'}, 'dateOfIssuance': {'type': 'datetime'}, 'drivingLicenseID': {'type':
            'string'}, 'drivingClass': {'type': 'integer'}, 'required': ['emailAddress', 'familyName', 'dateOfIssuance',
            'drivingLicenseID', 'drivingClass'], 'additionalProperties': True}}}}.
        author (str): DID of the identity which authored the credential schema. A piece of Metadata. Example:
            did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff.
        description (Union[Unset, str]): A human-readable description of the credential schema Example: Simple
            credential schema for the driving licence verifiable credential..
        tags (Union[Unset, List[str]]): Tokens that allow to lookup and filter the credential schema records.
    """

    name: str
    version: str
    type: str
    schema: Any
    author: str
    description: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        version = self.version
        type = self.type
        schema = self.schema
        author = self.author
        description = self.description
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "version": version,
                "type": type,
                "schema": schema,
                "author": author,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        version = d.pop("version")

        type = d.pop("type")

        schema = d.pop("schema")

        author = d.pop("author")

        description = d.pop("description", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        credential_schema_input = cls(
            name=name,
            version=version,
            type=type,
            schema=schema,
            author=author,
            description=description,
            tags=tags,
        )

        credential_schema_input.additional_properties = d
        return credential_schema_input

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
