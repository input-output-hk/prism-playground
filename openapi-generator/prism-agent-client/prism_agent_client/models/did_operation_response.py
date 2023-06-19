from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.did_operation_submission import DidOperationSubmission


T = TypeVar("T", bound="DIDOperationResponse")


@attr.s(auto_attribs=True)
class DIDOperationResponse:
    """
    Example:
        {'scheduledOperation': {'id': '98e6a4db10e58fcc011dd8def5ce99fd8b52af39e61e5fb436dc28259139818b', 'didRef':
            'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff'}}

    Attributes:
        scheduled_operation (DidOperationSubmission):  Example: {'id':
            '98e6a4db10e58fcc011dd8def5ce99fd8b52af39e61e5fb436dc28259139818b', 'didRef':
            'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff'}.
    """

    scheduled_operation: "DidOperationSubmission"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scheduled_operation = self.scheduled_operation.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scheduledOperation": scheduled_operation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.did_operation_submission import DidOperationSubmission

        d = src_dict.copy()
        scheduled_operation = DidOperationSubmission.from_dict(d.pop("scheduledOperation"))

        did_operation_response = cls(
            scheduled_operation=scheduled_operation,
        )

        did_operation_response.additional_properties = d
        return did_operation_response

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
