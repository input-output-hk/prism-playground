from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="HealthInfo")


@attr.s(auto_attribs=True)
class HealthInfo:
    """
    Example:
        {'version': '1.1.0'}

    Attributes:
        version (str): The semantic version number of the running service Example: 1.1.0.
    """

    version: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        version = d.pop("version")

        health_info = cls(
            version=version,
        )

        health_info.additional_properties = d
        return health_info

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
