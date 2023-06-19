from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.options import Options
    from ..models.proof_request_aux import ProofRequestAux


T = TypeVar("T", bound="RequestPresentationInput")


@attr.s(auto_attribs=True)
class RequestPresentationInput:
    """
    Example:
        {'proofs': [{'schemaId': 'https://schema.org/Person', 'trustIssuers': ['trustIssuers', 'trustIssuers']},
            {'schemaId': 'https://schema.org/Person', 'trustIssuers': ['trustIssuers', 'trustIssuers']}], 'options':
            {'domain': 'https://example-verifier.com', 'challenge': '11c91493-01b3-4c4d-ac36-b336bab5bddf'}, 'connectionId':
            'bc528dc8-69f1-4c5a-a508-5f8019047900'}

    Attributes:
        connection_id (str): The unique identifier of an established connection between the verifier and the prover.
            Example: bc528dc8-69f1-4c5a-a508-5f8019047900.
        options (Union[Unset, Options]): The options to use when creating the proof presentation request (e.g., domain,
            challenge). Example: {'domain': 'https://example-verifier.com', 'challenge':
            '11c91493-01b3-4c4d-ac36-b336bab5bddf'}.
        proofs (Union[Unset, List['ProofRequestAux']]): The type of proofs requested in the context of this proof
            presentation request (e.g., VC schema, trusted issuers, etc.)
    """

    connection_id: str
    options: Union[Unset, "Options"] = UNSET
    proofs: Union[Unset, List["ProofRequestAux"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        connection_id = self.connection_id
        options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        proofs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.proofs, Unset):
            proofs = []
            for proofs_item_data in self.proofs:
                proofs_item = proofs_item_data.to_dict()

                proofs.append(proofs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connectionId": connection_id,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options
        if proofs is not UNSET:
            field_dict["proofs"] = proofs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.options import Options
        from ..models.proof_request_aux import ProofRequestAux

        d = src_dict.copy()
        connection_id = d.pop("connectionId")

        _options = d.pop("options", UNSET)
        options: Union[Unset, Options]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = Options.from_dict(_options)

        proofs = []
        _proofs = d.pop("proofs", UNSET)
        for proofs_item_data in _proofs or []:
            proofs_item = ProofRequestAux.from_dict(proofs_item_data)

            proofs.append(proofs_item)

        request_presentation_input = cls(
            connection_id=connection_id,
            options=options,
            proofs=proofs,
        )

        request_presentation_input.additional_properties = d
        return request_presentation_input

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
