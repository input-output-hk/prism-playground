from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateIssueCredentialRecordRequest")


@attr.s(auto_attribs=True)
class CreateIssueCredentialRecordRequest:
    """
    Attributes:
        claims (Any): The claims that will be associated with the issued verifiable credential. Example:
            (firstname,Alice).
        issuing_did (str): The issuer DID of the verifiable credential object. Example:
            did:prism:issuerofverifiablecredentials.
        connection_id (str): The unique identifier of a DIDComm connection that already exists between the issuer and
            the holder, and that will be used to execute the issue credential protocol.
        validity_period (Union[Unset, float]): The validity period in seconds of the verifiable credential that will be
            issued. Example: 3600.0.
        schema_id (Union[Unset, str]): The unique identifier of the schema used for this credential offer. Example:
            https://agent-host.com/prism-agent/schema-registry/schemas/d9569cec-c81e-4779-aa86-0d5994d82676.
        automatic_issuance (Union[Unset, bool]): Specifies whether or not the credential should be automatically
            generated and issued when receiving the `CredentialRequest` from the holder. If set to `false`, a manual
            approval by the issuer via API call will be required for the VC to be issued. Example: True.
    """

    claims: Any
    issuing_did: str
    connection_id: str
    validity_period: Union[Unset, float] = UNSET
    schema_id: Union[Unset, str] = UNSET
    automatic_issuance: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        claims = self.claims
        issuing_did = self.issuing_did
        connection_id = self.connection_id
        validity_period = self.validity_period
        schema_id = self.schema_id
        automatic_issuance = self.automatic_issuance

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "claims": claims,
                "issuingDID": issuing_did,
                "connectionId": connection_id,
            }
        )
        if validity_period is not UNSET:
            field_dict["validityPeriod"] = validity_period
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id
        if automatic_issuance is not UNSET:
            field_dict["automaticIssuance"] = automatic_issuance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        claims = d.pop("claims")

        issuing_did = d.pop("issuingDID")

        connection_id = d.pop("connectionId")

        validity_period = d.pop("validityPeriod", UNSET)

        schema_id = d.pop("schemaId", UNSET)

        automatic_issuance = d.pop("automaticIssuance", UNSET)

        create_issue_credential_record_request = cls(
            claims=claims,
            issuing_did=issuing_did,
            connection_id=connection_id,
            validity_period=validity_period,
            schema_id=schema_id,
            automatic_issuance=automatic_issuance,
        )

        create_issue_credential_record_request.additional_properties = d
        return create_issue_credential_record_request

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
