from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.purpose import Purpose

T = TypeVar("T", bound="ManagedDIDKeyTemplate")


@attr.s(auto_attribs=True)
class ManagedDIDKeyTemplate:
    """key-pair template to add to DID document.

    Example:
        {'purpose': 'authentication', 'id': 'key-1'}

    Attributes:
        id (str): Identifier of a verification material in the DID Document Example: key-1.
        purpose (Purpose): Purpose of the verification material in the DID Document Example: authentication.
    """

    id: str
    purpose: Purpose
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        purpose = self.purpose.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "purpose": purpose,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        purpose = Purpose(d.pop("purpose"))

        managed_did_key_template = cls(
            id=id,
            purpose=purpose,
        )

        managed_did_key_template.additional_properties = d
        return managed_did_key_template

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
