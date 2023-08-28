from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

if TYPE_CHECKING:
    from ..models.arr import Arr
    from ..models.bool_ import Bool
    from ..models.null import Null
    from ..models.num import Num
    from ..models.obj import Obj
    from ..models.str_ import Str


T = TypeVar("T", bound="Service")


@attr.s(auto_attribs=True)
class Service:
    """A service expressed in the DID document. https://www.w3.org/TR/did-core/#services

    Example:
        {'id': 'service-1', 'serviceEndpoint': 'https://example.com', 'type': 'Single(LinkedDomains)'}

    Attributes:
        id (str): The id of the service.
            Requires a URI fragment when use in create / update DID.
            Returns the full ID (with DID prefix) when resolving DID Example: service-1.
        type (Union[List[str], str]): Service type. Can contain multiple possible values as described in the [Create DID
            operation](https://github.com/input-output-hk/prism-did-method-spec/blob/main/w3c-spec/PRISM-method.md#create-
            did) under the construction section. Example: Single(LinkedDomains).
        service_endpoint (Union['Arr', 'Bool', 'Null', 'Num', 'Obj', 'Str']): The service endpoint. Can contain multiple
            possible values as described in the [Create DID operation] Example: https://example.com.
    """

    id: str
    type: Union[List[str], str]
    service_endpoint: Union["Arr", "Bool", "Null", "Num", "Obj", "Str"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.arr import Arr
        from ..models.bool_ import Bool
        from ..models.null import Null
        from ..models.num import Num
        from ..models.obj import Obj

        id = self.id
        type: Union[List[str], str]

        if isinstance(self.type, list):
            type = self.type

        else:
            type = self.type

        service_endpoint: Dict[str, Any]

        if isinstance(self.service_endpoint, Arr):
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
                "type": type,
                "serviceEndpoint": service_endpoint,
            }
        )

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

        def _parse_type(data: object) -> Union[List[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_service_type_type_0 = cast(List[str], data)

                return componentsschemas_service_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], str], data)

        type = _parse_type(d.pop("type"))

        def _parse_service_endpoint(data: object) -> Union["Arr", "Bool", "Null", "Num", "Obj", "Str"]:
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

        service_endpoint = _parse_service_endpoint(d.pop("serviceEndpoint"))

        service = cls(
            id=id,
            type=type,
            service_endpoint=service_endpoint,
        )

        service.additional_properties = d
        return service

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
