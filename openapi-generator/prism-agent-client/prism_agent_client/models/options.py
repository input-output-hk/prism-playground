from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="Options")


@attr.s(auto_attribs=True)
class Options:
    """The options to use when creating the proof presentation request (e.g., domain, challenge).

    Example:
        {'domain': 'https://example-verifier.com', 'challenge': '11c91493-01b3-4c4d-ac36-b336bab5bddf'}

    Attributes:
        challenge (str): The challenge should be a randomly generated string. Example:
            11c91493-01b3-4c4d-ac36-b336bab5bddf.
        domain (str): The domain value can be any string or URI. Example: https://example-verifier.com.
    """

    challenge: str
    domain: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        challenge = self.challenge
        domain = self.domain

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "challenge": challenge,
                "domain": domain,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        challenge = d.pop("challenge")

        domain = d.pop("domain")

        options = cls(
            challenge=challenge,
            domain=domain,
        )

        options.additional_properties = d
        return options

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
