from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="VerificationPolicyConstraint")


@attr.s(auto_attribs=True)
class VerificationPolicyConstraint:
    """
    Example:
        {'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'}

    Attributes:
        schema_id (str):
        trusted_issuers (Union[Unset, List[str]]):
    """

    schema_id: str
    trusted_issuers: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
        trusted_issuers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.trusted_issuers, Unset):
            trusted_issuers = self.trusted_issuers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schemaId": schema_id,
            }
        )
        if trusted_issuers is not UNSET:
            field_dict["trustedIssuers"] = trusted_issuers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        schema_id = d.pop("schemaId")

        trusted_issuers = cast(List[str], d.pop("trustedIssuers", UNSET))

        verification_policy_constraint = cls(
            schema_id=schema_id,
            trusted_issuers=trusted_issuers,
        )

        verification_policy_constraint.additional_properties = d
        return verification_policy_constraint

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
