from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_managed_did_request_action import UpdateManagedDIDRequestAction


T = TypeVar("T", bound="UpdateManagedDIDRequest")


@attr.s(auto_attribs=True)
class UpdateManagedDIDRequest:
    """
    Example:
        {'actions': [{'actionType': None, 'removeKey': {'id': 'id'}, 'removeService': {'id': 'id'}, 'addService': {'id':
            'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'},
            'updateService': {'id': 'service-1', 'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type':
            'LinkedDomains'}, 'addKey': {'purpose': 'authentication', 'id': 'key-1'}}, {'actionType': None, 'removeKey':
            {'id': 'id'}, 'removeService': {'id': 'id'}, 'addService': {'id': 'service-1', 'serviceEndpoint':
            ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, 'updateService': {'id': 'service-1',
            'serviceEndpoint': ['serviceEndpoint', 'serviceEndpoint'], 'type': 'LinkedDomains'}, 'addKey': {'purpose':
            'authentication', 'id': 'key-1'}}]}

    Attributes:
        actions (Union[Unset, List['UpdateManagedDIDRequestAction']]):
    """

    actions: Union[Unset, List["UpdateManagedDIDRequestAction"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        actions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()

                actions.append(actions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if actions is not UNSET:
            field_dict["actions"] = actions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_managed_did_request_action import UpdateManagedDIDRequestAction

        d = src_dict.copy()
        actions = []
        _actions = d.pop("actions", UNSET)
        for actions_item_data in _actions or []:
            actions_item = UpdateManagedDIDRequestAction.from_dict(actions_item_data)

            actions.append(actions_item)

        update_managed_did_request = cls(
            actions=actions,
        )

        update_managed_did_request.additional_properties = d
        return update_managed_did_request

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
