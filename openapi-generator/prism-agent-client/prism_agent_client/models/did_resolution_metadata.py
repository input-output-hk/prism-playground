from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DIDResolutionMetadata")


@attr.s(auto_attribs=True)
class DIDResolutionMetadata:
    """[DID resolution metadata](https://www.w3.org/TR/did-core/#did-resolution-metadata)

    Attributes:
        error (Union[Unset, str]): Resolution error constant according to [DID spec
            registries](https://www.w3.org/TR/did-spec-registries/#error) Example: invalidDid.
        error_message (Union[Unset, str]): Resolution error message Example: The initialState does not match the suffix.
        content_type (Union[Unset, str]): The media type of the returned DID document Example: application/did+ld+json.
    """

    error: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    content_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        error = self.error
        error_message = self.error_message
        content_type = self.content_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if content_type is not UNSET:
            field_dict["contentType"] = content_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        error = d.pop("error", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        content_type = d.pop("contentType", UNSET)

        did_resolution_metadata = cls(
            error=error,
            error_message=error_message,
            content_type=content_type,
        )

        did_resolution_metadata.additional_properties = d
        return did_resolution_metadata

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
