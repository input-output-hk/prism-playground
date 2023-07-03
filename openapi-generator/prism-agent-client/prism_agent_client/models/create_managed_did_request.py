from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.create_managed_did_request_document_template import CreateManagedDidRequestDocumentTemplate


T = TypeVar("T", bound="CreateManagedDidRequest")


@attr.s(auto_attribs=True)
class CreateManagedDidRequest:
    """
    Example:
        {'documentTemplate': {'publicKeys': [{'purpose': 'authentication', 'id': 'key-1'}, {'purpose': 'authentication',
            'id': 'key-1'}], 'services': [{'id': 'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'],
            'type': 'LinkedDomains'}, {'id': 'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type':
            'LinkedDomains'}]}}

    Attributes:
        document_template (CreateManagedDidRequestDocumentTemplate):  Example: {'publicKeys': [{'purpose':
            'authentication', 'id': 'key-1'}, {'purpose': 'authentication', 'id': 'key-1'}], 'services': [{'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, {'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}]}.
    """

    document_template: "CreateManagedDidRequestDocumentTemplate"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        document_template = self.document_template.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "documentTemplate": document_template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_managed_did_request_document_template import CreateManagedDidRequestDocumentTemplate

        d = src_dict.copy()
        document_template = CreateManagedDidRequestDocumentTemplate.from_dict(d.pop("documentTemplate"))

        create_managed_did_request = cls(
            document_template=document_template,
        )

        create_managed_did_request.additional_properties = d
        return create_managed_did_request

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
