from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateManagedDIDServiceAction")


@attr.s(auto_attribs=True)
class UpdateManagedDIDServiceAction:
    """A patch to existing Service. 'type' and 'serviceEndpoint' cannot both be empty.

    Example:
        {'id': 'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}

    Attributes:
        id (str): The id of the service to update Example: service-1.
        type (Union[Unset, str]): The type of the service Example: LinkedDomains.
        service_endpoint (Union[Unset, List[str]]):
    """

    id: str
    type: Union[Unset, str] = UNSET
    service_endpoint: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type = self.type
        service_endpoint: Union[Unset, List[str]] = UNSET
        if not isinstance(self.service_endpoint, Unset):
            service_endpoint = self.service_endpoint

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if service_endpoint is not UNSET:
            field_dict["serviceEndpoint"] = service_endpoint

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        type = d.pop("type", UNSET)

        service_endpoint = cast(List[str], d.pop("serviceEndpoint", UNSET))

        update_managed_did_service_action = cls(
            id=id,
            type=type,
            service_endpoint=service_endpoint,
        )

        update_managed_did_service_action.additional_properties = d
        return update_managed_did_service_action

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
