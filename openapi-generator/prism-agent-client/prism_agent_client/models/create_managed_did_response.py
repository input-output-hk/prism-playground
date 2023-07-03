from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="CreateManagedDIDResponse")


@attr.s(auto_attribs=True)
class CreateManagedDIDResponse:
    """
    Example:
        {'longFormDid': 'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff:Cr4BCrsBElsKBmF1dGgt
            MRAEQk8KCXNlY3AyNTZrMRIg0opTuxu-zt6aRbT1tPniG4eu4CYsQPM3rrLzvzNiNgwaIIFTnyT2N4U7qCQ78qtWC3-p0el6Hvv8qxG5uuEw-WgM
            ElwKB21hc3RlcjAQAUJPCglzZWNwMjU2azESIKhBU0eCOO6Vinz_8vhtFSAhYYqrkEXC8PHGxkuIUev8GiAydFHLXb7c22A1Uj_PR21NZp6BCDQq
            Nq2xd244txRgsQ'}

    Attributes:
        long_form_did (str): A long-form DID for the created DID Example: did:prism:4a5b5cf0a513e83b598bbea25cd619674674
            7f361a73ef77068268bc9bd732ff:Cr4BCrsBElsKBmF1dGgtMRAEQk8KCXNlY3AyNTZrMRIg0opTuxu-
            zt6aRbT1tPniG4eu4CYsQPM3rrLzvzNiNgwaIIFTnyT2N4U7qCQ78qtWC3-p0el6Hvv8qxG5uuEw-WgMElwKB21hc3RlcjAQAUJPCglzZWNwMjU2
            azESIKhBU0eCOO6Vinz_8vhtFSAhYYqrkEXC8PHGxkuIUev8GiAydFHLXb7c22A1Uj_PR21NZp6BCDQqNq2xd244txRgsQ.
    """

    long_form_did: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        long_form_did = self.long_form_did

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "longFormDid": long_form_did,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        long_form_did = d.pop("longFormDid")

        create_managed_did_response = cls(
            long_form_did=long_form_did,
        )

        create_managed_did_response.additional_properties = d
        return create_managed_did_response

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
