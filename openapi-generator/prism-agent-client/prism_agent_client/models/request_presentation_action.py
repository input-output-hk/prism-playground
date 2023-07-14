from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.request_presentation_action_action import RequestPresentationActionAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestPresentationAction")


@attr.s(auto_attribs=True)
class RequestPresentationAction:
    """
    Example:
        {'action': 'request-accept', 'proofId': ['proofId', 'proofId']}

    Attributes:
        action (RequestPresentationActionAction): The action to perform on the proof presentation record. Example:
            request-accept.
        proof_id (Union[Unset, List[str]]): The unique identifier of the issue credential record - and hence VC - to use
            as the prover accepts the presentation request. Only applicable on the prover side when the action is `request-
            accept`.
    """

    action: RequestPresentationActionAction
    proof_id: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action = self.action.value

        proof_id: Union[Unset, List[str]] = UNSET
        if not isinstance(self.proof_id, Unset):
            proof_id = self.proof_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
            }
        )
        if proof_id is not UNSET:
            field_dict["proofId"] = proof_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action = RequestPresentationActionAction(d.pop("action"))

        proof_id = cast(List[str], d.pop("proofId", UNSET))

        request_presentation_action = cls(
            action=action,
            proof_id=proof_id,
        )

        request_presentation_action.additional_properties = d
        return request_presentation_action

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
