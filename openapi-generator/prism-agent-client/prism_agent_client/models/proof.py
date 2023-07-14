import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Proof")


@attr.s(auto_attribs=True)
class Proof:
    """A digital signature over the Credential Schema for the sake of asserting authorship. A piece of Metadata.

    Example:
        {'type': 'Ed25519Signature2018', 'created': datetime.datetime(2022, 3, 10, 12, 0, tzinfo=datetime.timezone.utc),
            'verificationMethod': 'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff#key-1',
            'proofPurpose': 'assertionMethod', 'proofValue': 'FiPfjknHikKmZ...', 'jws':
            'eyJhbGciOiJFZERTQSIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il0sImt0eSI6Ik...', 'domain': 'prims.atala.com'}

    Attributes:
        type (str): The type of cryptographic signature algorithm used to generate the proof. Example:
            Ed25519Signature2018.
        created (datetime.datetime): The date and time at which the proof was created, in UTC format. This field is used
            to ensure that the proof was generated before or at the same time as the credential schema itself. Example:
            2022-03-10 12:00:00+00:00.
        verification_method (str): The verification method used to generate the proof. This is usually a DID and key ID
            combination that can be used to look up the public key needed to verify the proof. Example:
            did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff#key-1.
        proof_purpose (str): The purpose of the proof (for example: `assertionMethod`). This indicates that the proof is
            being used to assert that the issuer really issued this credential schema instance. Example: assertionMethod.
        proof_value (str): The cryptographic signature value that was generated using the private key associated with
            the verification method, and which can be used to verify the proof. Example: FiPfjknHikKmZ....
        jws (str): The JSON Web Signature (JWS) that contains the proof information. Example:
            eyJhbGciOiJFZERTQSIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il0sImt0eSI6Ik....
        domain (Union[Unset, str]): It specifies the domain context within which the credential schema and proof are
            being used Example: prims.atala.com.
    """

    type: str
    created: datetime.datetime
    verification_method: str
    proof_purpose: str
    proof_value: str
    jws: str
    domain: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        created = self.created.isoformat()

        verification_method = self.verification_method
        proof_purpose = self.proof_purpose
        proof_value = self.proof_value
        jws = self.jws
        domain = self.domain

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "created": created,
                "verificationMethod": verification_method,
                "proofPurpose": proof_purpose,
                "proofValue": proof_value,
                "jws": jws,
            }
        )
        if domain is not UNSET:
            field_dict["domain"] = domain

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        created = isoparse(d.pop("created"))

        verification_method = d.pop("verificationMethod")

        proof_purpose = d.pop("proofPurpose")

        proof_value = d.pop("proofValue")

        jws = d.pop("jws")

        domain = d.pop("domain", UNSET)

        proof = cls(
            type=type,
            created=created,
            verification_method=verification_method,
            proof_purpose=proof_purpose,
            proof_value=proof_value,
            jws=jws,
            domain=domain,
        )

        proof.additional_properties = d
        return proof

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
