from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DidOperationSubmission")


@attr.s(auto_attribs=True)
class DidOperationSubmission:
    """
    Example:
        {'id': '98e6a4db10e58fcc011dd8def5ce99fd8b52af39e61e5fb436dc28259139818b', 'didRef':
            'did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff'}

    Attributes:
        id (str): A scheduled operation ID Example: 98e6a4db10e58fcc011dd8def5ce99fd8b52af39e61e5fb436dc28259139818b.
        did_ref (str): A DID affected by the scheduled operation Example:
            did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff.
    """

    id: str
    did_ref: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        did_ref = self.did_ref

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "didRef": did_ref,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        did_ref = d.pop("didRef")

        did_operation_submission = cls(
            id=id,
            did_ref=did_ref,
        )

        did_operation_submission.additional_properties = d
        return did_operation_submission

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
