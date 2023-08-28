from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DIDDocumentMetadata")


@attr.s(auto_attribs=True)
class DIDDocumentMetadata:
    """[DID document metadata](https://www.w3.org/TR/did-core/#did-document-metadata)

    Attributes:
        deactivated (Union[Unset, bool]): If a DID has been deactivated, DID document metadata MUST include this
            property with the boolean value true. If a DID has not been deactivated, this property is OPTIONAL, but if
            included, MUST have the boolean value false.
        canonical_id (Union[Unset, str]):
            A DID in canonical form.
            If a DID is in long form and has been published, DID document metadata MUST contain a `canonicalId`` property
            with the short form DID as its value.
            If a DID in short form or has not been published, DID document metadata MUST NOT contain a `canonicalId`
            property.
             Example: did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff.
        version_id (Union[Unset, str]):
            DID document metadata MUST contain a versionId property with the hash of the AtalaOperation contained in the
            latest valid SignedAtalaOperation that created the DID or changed the DID's internal state.
             Example: 4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff.
        created (Union[Unset, str]): The timestamp of the Cardano block that contained the first valid
            SignedAtalaOperation with a CreateDIDOperation that created the DID. Example: 2023-02-04 13:52:10+00:00.
        updated (Union[Unset, str]): The timestamp of the Cardano block that contained the latest valid
            SignedAtalaOperation that changed the DID's internal state. Example: 2023-02-04 13:52:10+00:00.
    """

    deactivated: Union[Unset, bool] = UNSET
    canonical_id: Union[Unset, str] = UNSET
    version_id: Union[Unset, str] = UNSET
    created: Union[Unset, str] = UNSET
    updated: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        deactivated = self.deactivated
        canonical_id = self.canonical_id
        version_id = self.version_id
        created = self.created
        updated = self.updated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deactivated is not UNSET:
            field_dict["deactivated"] = deactivated
        if canonical_id is not UNSET:
            field_dict["canonicalId"] = canonical_id
        if version_id is not UNSET:
            field_dict["versionId"] = version_id
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        deactivated = d.pop("deactivated", UNSET)

        canonical_id = d.pop("canonicalId", UNSET)

        version_id = d.pop("versionId", UNSET)

        created = d.pop("created", UNSET)

        updated = d.pop("updated", UNSET)

        did_document_metadata = cls(
            deactivated=deactivated,
            canonical_id=canonical_id,
            version_id=version_id,
            created=created,
            updated=updated,
        )

        did_document_metadata.additional_properties = d
        return did_document_metadata

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
