from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.did_document import DIDDocument
    from ..models.did_document_metadata import DIDDocumentMetadata
    from ..models.did_resolution_metadata import DIDResolutionMetadata


T = TypeVar("T", bound="DIDResolutionResult")


@attr.s(auto_attribs=True)
class DIDResolutionResult:
    """
    Attributes:
        context (str): The JSON-LD context for the DID resolution result. Example: https://w3id.org/did-resolution/v1.
        did_document_metadata (DIDDocumentMetadata): [DID document metadata](https://www.w3.org/TR/did-core/#did-
            document-metadata)
        did_resolution_metadata (DIDResolutionMetadata): [DID resolution metadata](https://www.w3.org/TR/did-core/#did-
            resolution-metadata)
        did_document (Union[Unset, DIDDocument]): A W3C compliant Prism DID document representation.
    """

    context: str
    did_document_metadata: "DIDDocumentMetadata"
    did_resolution_metadata: "DIDResolutionMetadata"
    did_document: Union[Unset, "DIDDocument"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        context = self.context
        did_document_metadata = self.did_document_metadata.to_dict()

        did_resolution_metadata = self.did_resolution_metadata.to_dict()

        did_document: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.did_document, Unset):
            did_document = self.did_document.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "@context": context,
                "didDocumentMetadata": did_document_metadata,
                "didResolutionMetadata": did_resolution_metadata,
            }
        )
        if did_document is not UNSET:
            field_dict["didDocument"] = did_document

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.did_document import DIDDocument
        from ..models.did_document_metadata import DIDDocumentMetadata
        from ..models.did_resolution_metadata import DIDResolutionMetadata

        d = src_dict.copy()
        context = d.pop("@context")

        did_document_metadata = DIDDocumentMetadata.from_dict(d.pop("didDocumentMetadata"))

        did_resolution_metadata = DIDResolutionMetadata.from_dict(d.pop("didResolutionMetadata"))

        _did_document = d.pop("didDocument", UNSET)
        did_document: Union[Unset, DIDDocument]
        if isinstance(_did_document, Unset):
            did_document = UNSET
        else:
            did_document = DIDDocument.from_dict(_did_document)

        did_resolution_result = cls(
            context=context,
            did_document_metadata=did_document_metadata,
            did_resolution_metadata=did_resolution_metadata,
            did_document=did_document,
        )

        did_resolution_result.additional_properties = d
        return did_resolution_result

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
