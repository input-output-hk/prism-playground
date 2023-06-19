from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AcceptCredentialOfferRequest")


@attr.s(auto_attribs=True)
class AcceptCredentialOfferRequest:
    """
    Example:
        {'subjectId': 'did:prism:3bb0505d13fcb04d28a48234edb27b0d4e6d7e18a81e2c1abab58f3bbc21ce6f'}

    Attributes:
        subject_id (str): The short-form subject Prism DID to which the verifiable credential should be issued. Example:
            did:prism:3bb0505d13fcb04d28a48234edb27b0d4e6d7e18a81e2c1abab58f3bbc21ce6f.
    """

    subject_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subject_id = self.subject_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subjectId": subject_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subject_id = d.pop("subjectId")

        accept_credential_offer_request = cls(
            subject_id=subject_id,
        )

        accept_credential_offer_request.additional_properties = d
        return accept_credential_offer_request

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
