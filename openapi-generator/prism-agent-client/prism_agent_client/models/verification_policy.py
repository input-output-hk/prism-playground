import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.verification_policy_constraint import VerificationPolicyConstraint


T = TypeVar("T", bound="VerificationPolicy")


@attr.s(auto_attribs=True)
class VerificationPolicy:
    """
    Example:
        {'createdAt': datetime.datetime(2000, 1, 23, 4, 56, 7, tzinfo=datetime.timezone.utc), 'kind': 'kind', 'name':
            'name', 'self': 'self', 'description': 'description', 'id': '046b6c7f-0b8a-43b9-b35d-6489e6daee91', 'nonce': 0,
            'constraints': [{'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'},
            {'trustedIssuers': ['trustedIssuers', 'trustedIssuers'], 'schemaId': 'schemaId'}], 'updatedAt':
            datetime.datetime(2000, 1, 23, 4, 56, 7, tzinfo=datetime.timezone.utc)}

    Attributes:
        self_ (str):
        kind (str):
        id (str):
        nonce (int):
        name (str):
        description (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        constraints (Union[Unset, List['VerificationPolicyConstraint']]):
    """

    self_: str
    kind: str
    id: str
    nonce: int
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    constraints: Union[Unset, List["VerificationPolicyConstraint"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        kind = self.kind
        id = self.id
        nonce = self.nonce
        name = self.name
        description = self.description
        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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
                "self": self_,
                "kind": kind,
                "id": id,
                "nonce": nonce,
                "name": name,
                "description": description,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if constraints is not UNSET:
            field_dict["constraints"] = constraints

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.verification_policy_constraint import VerificationPolicyConstraint

        d = src_dict.copy()
        self_ = d.pop("self")

        kind = d.pop("kind")

        id = d.pop("id")

        nonce = d.pop("nonce")

        name = d.pop("name")

        description = d.pop("description")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        constraints = []
        _constraints = d.pop("constraints", UNSET)
        for constraints_item_data in _constraints or []:
            constraints_item = VerificationPolicyConstraint.from_dict(constraints_item_data)

            constraints.append(constraints_item)

        verification_policy = cls(
            self_=self_,
            kind=kind,
            id=id,
            nonce=nonce,
            name=name,
            description=description,
            created_at=created_at,
            updated_at=updated_at,
            constraints=constraints,
        )

        verification_policy.additional_properties = d
        return verification_policy

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
