from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.arr import Arr
    from ..models.bool_ import Bool
    from ..models.null import Null
    from ..models.num import Num
    from ..models.obj import Obj
    from ..models.str_ import Str


T = TypeVar("T", bound="UpdateManagedDIDServiceAction")


@attr.s(auto_attribs=True)
class UpdateManagedDIDServiceAction:
    """A patch to existing Service. 'type' and 'serviceEndpoint' cannot both be empty.

    Example:
        {'id': 'service-1', 'serviceEndpoint': 'https://example.com', 'type': 'LinkedDomains'}

    Attributes:
        id (str): The id of the service to update Example: service-1.
        type (Union[List[str], Unset, str]): The type of the service Example: LinkedDomains.
        service_endpoint (Union['Arr', 'Bool', 'Null', 'Num', 'Obj', 'Str', Unset]): The service endpoint. Can contain
            multiple possible values as described in the [Create DID operation] Example: https://example.com.
    """

    id: str
    type: Union[List[str], Unset, str] = UNSET
    service_endpoint: Union["Arr", "Bool", "Null", "Num", "Obj", "Str", Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.arr import Arr
        from ..models.bool_ import Bool
        from ..models.null import Null
        from ..models.num import Num
        from ..models.obj import Obj

        id = self.id
        type: Union[List[str], Unset, str]
        if isinstance(self.type, Unset):
            type = UNSET

        elif isinstance(self.type, list):
            type = self.type

        else:
            type = self.type

        service_endpoint: Union[Dict[str, Any], Unset]
        if isinstance(self.service_endpoint, Unset):
            service_endpoint = UNSET

        elif isinstance(self.service_endpoint, Arr):
            service_endpoint = self.service_endpoint.to_dict()

        elif isinstance(self.service_endpoint, Bool):
            service_endpoint = self.service_endpoint.to_dict()

        elif isinstance(self.service_endpoint, Null):
            service_endpoint = self.service_endpoint.to_dict()

        elif isinstance(self.service_endpoint, Num):
            service_endpoint = self.service_endpoint.to_dict()

        elif isinstance(self.service_endpoint, Obj):
            service_endpoint = self.service_endpoint.to_dict()

        else:
            service_endpoint = self.service_endpoint.to_dict()

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
        from ..models.arr import Arr
        from ..models.bool_ import Bool
        from ..models.null import Null
        from ..models.num import Num
        from ..models.obj import Obj
        from ..models.str_ import Str

        d = src_dict.copy()
        id = d.pop("id")

        def _parse_type(data: object) -> Union[List[str], Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_update_managed_did_service_action_type_type_0 = cast(List[str], data)

                return componentsschemas_update_managed_did_service_action_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], Unset, str], data)

        type = _parse_type(d.pop("type", UNSET))

        def _parse_service_endpoint(data: object) -> Union["Arr", "Bool", "Null", "Num", "Obj", "Str", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_json_type_0 = Arr.from_dict(data)

                return componentsschemas_json_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_json_type_1 = Bool.from_dict(data)

                return componentsschemas_json_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_json_type_2 = Null.from_dict(data)

                return componentsschemas_json_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_json_type_3 = Num.from_dict(data)

                return componentsschemas_json_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_json_type_4 = Obj.from_dict(data)

                return componentsschemas_json_type_4
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_json_type_5 = Str.from_dict(data)

            return componentsschemas_json_type_5

        service_endpoint = _parse_service_endpoint(d.pop("serviceEndpoint", UNSET))

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
