from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.connection import Connection


T = TypeVar("T", bound="ConnectionsPage")


@attr.s(auto_attribs=True)
class ConnectionsPage:
    """
    Attributes:
        kind (str):  Example: ConnectionsPage.
        self_ (str):  Example: /prism-agent/connections?offset=10&limit=10.
        page_of (str):
        contents (Union[Unset, List['Connection']]):
        next_ (Union[Unset, str]):  Example: /prism-agent/connections?offset=20&limit=10.
        previous (Union[Unset, str]):  Example: /prism-agent/connections?offset=0&limit=10.
    """

    kind: str
    self_: str
    page_of: str
    contents: Union[Unset, List["Connection"]] = UNSET
    next_: Union[Unset, str] = UNSET
    previous: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind
        self_ = self.self_
        page_of = self.page_of
        contents: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.contents, Unset):
            contents = []
            for contents_item_data in self.contents:
                contents_item = contents_item_data.to_dict()

                contents.append(contents_item)

        next_ = self.next_
        previous = self.previous

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "self": self_,
                "pageOf": page_of,
            }
        )
        if contents is not UNSET:
            field_dict["contents"] = contents
        if next_ is not UNSET:
            field_dict["next"] = next_
        if previous is not UNSET:
            field_dict["previous"] = previous

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.connection import Connection

        d = src_dict.copy()
        kind = d.pop("kind")

        self_ = d.pop("self")

        page_of = d.pop("pageOf")

        contents = []
        _contents = d.pop("contents", UNSET)
        for contents_item_data in _contents or []:
            contents_item = Connection.from_dict(contents_item_data)

            contents.append(contents_item)

        next_ = d.pop("next", UNSET)

        previous = d.pop("previous", UNSET)

        connections_page = cls(
            kind=kind,
            self_=self_,
            page_of=page_of,
            contents=contents,
            next_=next_,
            previous=previous,
        )

        connections_page.additional_properties = d
        return connections_page

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
