from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ManagedDID")


@attr.s(auto_attribs=True)
class ManagedDID:
    """
    Example:
        {'longFormDid': 'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff:Cr4BCrsBElsKBmF1dGgt
            MRAEQk8KCXNlY3AyNTZrMRIg0opTuxu-zt6aRbT1tPniG4eu4CYsQPM3rrLzvzNiNgwaIIFTnyT2N4U7qCQ78qtWC3-p0el6Hvv8qxG5uuEw-WgM
            ElwKB21hc3RlcjAQAUJPCglzZWNwMjU2azESIKhBU0eCOO6Vinz_8vhtFSAhYYqrkEXC8PHGxkuIUev8GiAydFHLXb7c22A1Uj_PR21NZp6BCDQq
            Nq2xd244txRgsQ', 'did': 'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff', 'status':
            'CREATED'}

    Attributes:
        did (str): A managed DID Example: did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff.
        status (str): A status indicating a publication state of a DID in the wallet (e.g. PUBLICATION_PENDING,
            PUBLISHED).
            Does not represent DID a full lifecyle (e.g. deactivated, recovered, updated). Example: CREATED.
        long_form_did (Union[Unset, str]): A long-form DID. Mandatory when status is not PUBLISHED and optional when
            status is PUBLISHED Example: did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff:Cr4BCrsB
            ElsKBmF1dGgtMRAEQk8KCXNlY3AyNTZrMRIg0opTuxu-
            zt6aRbT1tPniG4eu4CYsQPM3rrLzvzNiNgwaIIFTnyT2N4U7qCQ78qtWC3-p0el6Hvv8qxG5uuEw-WgMElwKB21hc3RlcjAQAUJPCglzZWNwMjU2
            azESIKhBU0eCOO6Vinz_8vhtFSAhYYqrkEXC8PHGxkuIUev8GiAydFHLXb7c22A1Uj_PR21NZp6BCDQqNq2xd244txRgsQ.
    """

    did: str
    status: str
    long_form_did: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        did = self.did
        status = self.status
        long_form_did = self.long_form_did

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "did": did,
                "status": status,
            }
        )
        if long_form_did is not UNSET:
            field_dict["longFormDid"] = long_form_did

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        did = d.pop("did")

        status = d.pop("status")

        long_form_did = d.pop("longFormDid", UNSET)

        managed_did = cls(
            did=did,
            status=status,
            long_form_did=long_form_did,
        )

        managed_did.additional_properties = d
        return managed_did

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
