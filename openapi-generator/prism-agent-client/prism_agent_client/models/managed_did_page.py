from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.managed_did import ManagedDID


T = TypeVar("T", bound="ManagedDIDPage")


@attr.s(auto_attribs=True)
class ManagedDIDPage:
    """
    Example:
        {'pageOf': 'pageOf', 'next': 'next', 'previous': 'previous', 'contents': [{'longFormDid': 'did:prism:4a5b5cf0a51
            3e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff:Cr4BCrsBElsKBmF1dGgtMRAEQk8KCXNlY3AyNTZrMRIg0opTuxu-
            zt6aRbT1tPniG4eu4CYsQPM3rrLzvzNiNgwaIIFTnyT2N4U7qCQ78qtWC3-p0el6Hvv8qxG5uuEw-WgMElwKB21hc3RlcjAQAUJPCglzZWNwMjU2
            azESIKhBU0eCOO6Vinz_8vhtFSAhYYqrkEXC8PHGxkuIUev8GiAydFHLXb7c22A1Uj_PR21NZp6BCDQqNq2xd244txRgsQ', 'did':
            'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff', 'status': 'CREATED'},
            {'longFormDid': 'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff:Cr4BCrsBElsKBmF1dGgt
            MRAEQk8KCXNlY3AyNTZrMRIg0opTuxu-zt6aRbT1tPniG4eu4CYsQPM3rrLzvzNiNgwaIIFTnyT2N4U7qCQ78qtWC3-p0el6Hvv8qxG5uuEw-WgM
            ElwKB21hc3RlcjAQAUJPCglzZWNwMjU2azESIKhBU0eCOO6Vinz_8vhtFSAhYYqrkEXC8PHGxkuIUev8GiAydFHLXb7c22A1Uj_PR21NZp6BCDQq
            Nq2xd244txRgsQ', 'did': 'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff', 'status':
            'CREATED'}], 'kind': 'kind', 'self': 'self'}

    Attributes:
        self_ (str):
        kind (str):
        page_of (str):
        next_ (Union[Unset, str]):
        previous (Union[Unset, str]):
        contents (Union[Unset, List['ManagedDID']]):
    """

    self_: str
    kind: str
    page_of: str
    next_: Union[Unset, str] = UNSET
    previous: Union[Unset, str] = UNSET
    contents: Union[Unset, List["ManagedDID"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        kind = self.kind
        page_of = self.page_of
        next_ = self.next_
        previous = self.previous
        contents: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.contents, Unset):
            contents = []
            for contents_item_data in self.contents:
                contents_item = contents_item_data.to_dict()

                contents.append(contents_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "self": self_,
                "kind": kind,
                "pageOf": page_of,
            }
        )
        if next_ is not UNSET:
            field_dict["next"] = next_
        if previous is not UNSET:
            field_dict["previous"] = previous
        if contents is not UNSET:
            field_dict["contents"] = contents

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.managed_did import ManagedDID

        d = src_dict.copy()
        self_ = d.pop("self")

        kind = d.pop("kind")

        page_of = d.pop("pageOf")

        next_ = d.pop("next", UNSET)

        previous = d.pop("previous", UNSET)

        contents = []
        _contents = d.pop("contents", UNSET)
        for contents_item_data in _contents or []:
            contents_item = ManagedDID.from_dict(contents_item_data)

            contents.append(contents_item)

        managed_did_page = cls(
            self_=self_,
            kind=kind,
            page_of=page_of,
            next_=next_,
            previous=previous,
            contents=contents,
        )

        managed_did_page.additional_properties = d
        return managed_did_page

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
