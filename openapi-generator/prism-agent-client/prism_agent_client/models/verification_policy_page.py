from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.verification_policy import VerificationPolicy


T = TypeVar("T", bound="VerificationPolicyPage")


@attr.s(auto_attribs=True)
class VerificationPolicyPage:
    """
    Example:
        {'pageOf': 'pageOf', 'next': 'next', 'previous': 'previous', 'contents': [{'createdAt': datetime.datetime(2000,
            1, 23, 4, 56, 7, tzinfo=datetime.timezone.utc), 'kind': 'kind', 'name': 'name', 'self': 'self', 'description':
            'description', 'id': '046b6c7f-0b8a-43b9-b35d-6489e6daee91', 'nonce': 0, 'constraints': [{'trustedIssuers':
            ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'}, {'trustedIssuers': ['trustedIssuers',
            'trustedIssuers'], 'schemaId': 'schemaId'}], 'updatedAt': datetime.datetime(2000, 1, 23, 4, 56, 7,
            tzinfo=datetime.timezone.utc)}, {'createdAt': datetime.datetime(2000, 1, 23, 4, 56, 7,
            tzinfo=datetime.timezone.utc), 'kind': 'kind', 'name': 'name', 'self': 'self', 'description': 'description',
            'id': '046b6c7f-0b8a-43b9-b35d-6489e6daee91', 'nonce': 0, 'constraints': [{'trustedIssuers': ['trustedIssuers',
            'trustedIssuers'], 'schemaId': 'schemaId'}, {'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId':
            'schemaId'}], 'updatedAt': datetime.datetime(2000, 1, 23, 4, 56, 7, tzinfo=datetime.timezone.utc)}], 'kind':
            'kind', 'self': 'self'}

    Attributes:
        self_ (str):
        kind (str):
        page_of (str):
        next_ (Union[Unset, str]):
        previous (Union[Unset, str]):
        contents (Union[Unset, List['VerificationPolicy']]):
    """

    self_: str
    kind: str
    page_of: str
    next_: Union[Unset, str] = UNSET
    previous: Union[Unset, str] = UNSET
    contents: Union[Unset, List["VerificationPolicy"]] = UNSET
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
        from ..models.verification_policy import VerificationPolicy

        d = src_dict.copy()
        self_ = d.pop("self")

        kind = d.pop("kind")

        page_of = d.pop("pageOf")

        next_ = d.pop("next", UNSET)

        previous = d.pop("previous", UNSET)

        contents = []
        _contents = d.pop("contents", UNSET)
        for contents_item_data in _contents or []:
            contents_item = VerificationPolicy.from_dict(contents_item_data)

            contents.append(contents_item)

        verification_policy_page = cls(
            self_=self_,
            kind=kind,
            page_of=page_of,
            next_=next_,
            previous=previous,
            contents=contents,
        )

        verification_policy_page.additional_properties = d
        return verification_policy_page

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
