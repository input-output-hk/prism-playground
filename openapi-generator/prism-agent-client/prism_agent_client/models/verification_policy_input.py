from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.verification_policy_constraint import VerificationPolicyConstraint


T = TypeVar("T", bound="VerificationPolicyInput")


@attr.s(auto_attribs=True)
class VerificationPolicyInput:
    """
    Attributes:
        name (str):
        description (str):
        id (Union[Unset, str]):
        constraints (Union[Unset, List['VerificationPolicyConstraint']]):
    """

    name: str
    description: str
    id: Union[Unset, str] = UNSET
    constraints: Union[Unset, List["VerificationPolicyConstraint"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        id = self.id
        constraints: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.constraints, Unset):
            constraints = []
            for constraints_item_data in self.constraints:
                constraints_item = constraints_item_data.to_dict()

                constraints.append(constraints_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if constraints is not UNSET:
            field_dict["constraints"] = constraints

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.verification_policy_constraint import VerificationPolicyConstraint

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        id = d.pop("id", UNSET)

        constraints = []
        _constraints = d.pop("constraints", UNSET)
        for constraints_item_data in _constraints or []:
            constraints_item = VerificationPolicyConstraint.from_dict(constraints_item_data)

            constraints.append(constraints_item)

        verification_policy_input = cls(
            name=name,
            description=description,
            id=id,
            constraints=constraints,
        )

        verification_policy_input.additional_properties = d
        return verification_policy_input

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
