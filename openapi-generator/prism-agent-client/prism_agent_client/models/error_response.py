from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorResponse")


@attr.s(auto_attribs=True)
class ErrorResponse:
    """
    Attributes:
        status (int): The HTTP status code for this occurrence of the problem. Example: 200.
        type (str): A URI reference that identifies the problem type. Example: https://example.org/doc/#model-
            MalformedEmail/.
        title (str): A short, human-readable summary of the problem type. It does not change from occurrence to
            occurrence of the problem. Example: Malformed email.
        instance (str): A URI reference that identifies the specific occurrence of the problem. It may or may not yield
            further information if dereferenced. Example: The received '{}à!è@!.b}' email does not conform to the email
            format.
        detail (Union[Unset, str]): A human-readable explanation specific to this occurrence of the problem. Example:
            The received '{}à!è@!.b}' email does not conform to the email format.
    """

    status: int
    type: str
    title: str
    instance: str
    detail: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        type = self.type
        title = self.title
        instance = self.instance
        detail = self.detail

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "type": type,
                "title": title,
                "instance": instance,
            }
        )
        if detail is not UNSET:
            field_dict["detail"] = detail

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status")

        type = d.pop("type")

        title = d.pop("title")

        instance = d.pop("instance")

        detail = d.pop("detail", UNSET)

        error_response = cls(
            status=status,
            type=type,
            title=title,
            instance=instance,
            detail=detail,
        )

        error_response.additional_properties = d
        return error_response

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
