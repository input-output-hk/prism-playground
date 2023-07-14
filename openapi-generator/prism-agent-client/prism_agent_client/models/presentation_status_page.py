from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.presentation_status import PresentationStatus


T = TypeVar("T", bound="PresentationStatusPage")


@attr.s(auto_attribs=True)
class PresentationStatusPage:
    """
    Example:
        {'pageOf': '1', 'next': '', 'previous': '', 'contents': [{'presentationId':
            '3c6d9fa5-d277-431e-a6cb-d3956e47e610', 'data': ['data', 'data'], 'proofs': [{'schemaId':
            'https://schema.org/Person', 'trustIssuers': ['trustIssuers', 'trustIssuers']}, {'schemaId':
            'https://schema.org/Person', 'trustIssuers': ['trustIssuers', 'trustIssuers']}], 'connectionId':
            'bc528dc8-69f1-4c5a-a508-5f8019047900', 'status': 'RequestPending'}, {'presentationId':
            '3c6d9fa5-d277-431e-a6cb-d3956e47e610', 'data': ['data', 'data'], 'proofs': [{'schemaId':
            'https://schema.org/Person', 'trustIssuers': ['trustIssuers', 'trustIssuers']}, {'schemaId':
            'https://schema.org/Person', 'trustIssuers': ['trustIssuers', 'trustIssuers']}], 'connectionId':
            'bc528dc8-69f1-4c5a-a508-5f8019047900', 'status': 'RequestPending'}], 'kind': 'Collection', 'self': '/present-
            proof/presentations'}

    Attributes:
        self_ (str): The reference to the presentation collection itself. Example: /present-proof/presentations.
        kind (str): The type of object returned. In this case a `Collection`. Example: Collection.
        page_of (str): Page number within the context of paginated response. Example: 1.
        contents (Union[Unset, List['PresentationStatus']]): A sequence of Presentation objects.
        next_ (Union[Unset, str]): URL of the next page (if available)
        previous (Union[Unset, str]): URL of the previous page (if available)
    """

    self_: str
    kind: str
    page_of: str
    contents: Union[Unset, List["PresentationStatus"]] = UNSET
    next_: Union[Unset, str] = UNSET
    previous: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        kind = self.kind
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
                "self": self_,
                "kind": kind,
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
        from ..models.presentation_status import PresentationStatus

        d = src_dict.copy()
        self_ = d.pop("self")

        kind = d.pop("kind")

        page_of = d.pop("pageOf")

        contents = []
        _contents = d.pop("contents", UNSET)
        for contents_item_data in _contents or []:
            contents_item = PresentationStatus.from_dict(contents_item_data)

            contents.append(contents_item)

        next_ = d.pop("next", UNSET)

        previous = d.pop("previous", UNSET)

        presentation_status_page = cls(
            self_=self_,
            kind=kind,
            page_of=page_of,
            contents=contents,
            next_=next_,
            previous=previous,
        )

        presentation_status_page.additional_properties = d
        return presentation_status_page

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
