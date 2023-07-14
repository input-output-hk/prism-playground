from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="RequestPresentationOutput")


@attr.s(auto_attribs=True)
class RequestPresentationOutput:
    """
    Example:
        {'presentationId': '11c91493-01b3-4c4d-ac36-b336bab5bddf'}

    Attributes:
        presentation_id (str): Ref to the id on the presentation (db ref) Example: 11c91493-01b3-4c4d-ac36-b336bab5bddf.
    """

    presentation_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        presentation_id = self.presentation_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "presentationId": presentation_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        presentation_id = d.pop("presentationId")

        request_presentation_output = cls(
            presentation_id=presentation_id,
        )

        request_presentation_output.additional_properties = d
        return request_presentation_output

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
