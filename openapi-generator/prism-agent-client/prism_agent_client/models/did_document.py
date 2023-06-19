from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.service import Service
    from ..models.verification_method import VerificationMethod


T = TypeVar("T", bound="DIDDocument")


@attr.s(auto_attribs=True)
class DIDDocument:
    """A W3C compliant Prism DID document representation.

    Attributes:
        id (str): [DID subject](https://www.w3.org/TR/did-core/#did-subject).
            The value must match the DID that was given to the resolver. Example:
            did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff.
        context (Union[Unset, List[str]]): The JSON-LD context for the DID resolution result.
        controller (Union[Unset, str]): [DID controller](https://www.w3.org/TR/did-core/#did-controller) Example:
            did:prism:4a5b5cf0a513e83b598bbea25cd6196746747f361a73ef77068268bc9bd732ff.
        verification_method (Union[Unset, List['VerificationMethod']]):
        authentication (Union[Unset, List[str]]):
        assertion_method (Union[Unset, List[str]]):
        key_agreement (Union[Unset, List[str]]):
        capability_invocation (Union[Unset, List[str]]):
        capability_delegation (Union[Unset, List[str]]):
        service (Union[Unset, List['Service']]):
    """

    id: str
    context: Union[Unset, List[str]] = UNSET
    controller: Union[Unset, str] = UNSET
    verification_method: Union[Unset, List["VerificationMethod"]] = UNSET
    authentication: Union[Unset, List[str]] = UNSET
    assertion_method: Union[Unset, List[str]] = UNSET
    key_agreement: Union[Unset, List[str]] = UNSET
    capability_invocation: Union[Unset, List[str]] = UNSET
    capability_delegation: Union[Unset, List[str]] = UNSET
    service: Union[Unset, List["Service"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        context: Union[Unset, List[str]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context

        controller = self.controller
        verification_method: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.verification_method, Unset):
            verification_method = []
            for verification_method_item_data in self.verification_method:
                verification_method_item = verification_method_item_data.to_dict()

                verification_method.append(verification_method_item)

        authentication: Union[Unset, List[str]] = UNSET
        if not isinstance(self.authentication, Unset):
            authentication = self.authentication

        assertion_method: Union[Unset, List[str]] = UNSET
        if not isinstance(self.assertion_method, Unset):
            assertion_method = self.assertion_method

        key_agreement: Union[Unset, List[str]] = UNSET
        if not isinstance(self.key_agreement, Unset):
            key_agreement = self.key_agreement

        capability_invocation: Union[Unset, List[str]] = UNSET
        if not isinstance(self.capability_invocation, Unset):
            capability_invocation = self.capability_invocation

        capability_delegation: Union[Unset, List[str]] = UNSET
        if not isinstance(self.capability_delegation, Unset):
            capability_delegation = self.capability_delegation

        service: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.service, Unset):
            service = []
            for service_item_data in self.service:
                service_item = service_item_data.to_dict()

                service.append(service_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if context is not UNSET:
            field_dict["@context"] = context
        if controller is not UNSET:
            field_dict["controller"] = controller
        if verification_method is not UNSET:
            field_dict["verificationMethod"] = verification_method
        if authentication is not UNSET:
            field_dict["authentication"] = authentication
        if assertion_method is not UNSET:
            field_dict["assertionMethod"] = assertion_method
        if key_agreement is not UNSET:
            field_dict["keyAgreement"] = key_agreement
        if capability_invocation is not UNSET:
            field_dict["capabilityInvocation"] = capability_invocation
        if capability_delegation is not UNSET:
            field_dict["capabilityDelegation"] = capability_delegation
        if service is not UNSET:
            field_dict["service"] = service

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.service import Service
        from ..models.verification_method import VerificationMethod

        d = src_dict.copy()
        id = d.pop("id")

        context = cast(List[str], d.pop("@context", UNSET))

        controller = d.pop("controller", UNSET)

        verification_method = []
        _verification_method = d.pop("verificationMethod", UNSET)
        for verification_method_item_data in _verification_method or []:
            verification_method_item = VerificationMethod.from_dict(verification_method_item_data)

            verification_method.append(verification_method_item)

        authentication = cast(List[str], d.pop("authentication", UNSET))

        assertion_method = cast(List[str], d.pop("assertionMethod", UNSET))

        key_agreement = cast(List[str], d.pop("keyAgreement", UNSET))

        capability_invocation = cast(List[str], d.pop("capabilityInvocation", UNSET))

        capability_delegation = cast(List[str], d.pop("capabilityDelegation", UNSET))

        service = []
        _service = d.pop("service", UNSET)
        for service_item_data in _service or []:
            service_item = Service.from_dict(service_item_data)

            service.append(service_item)

        did_document = cls(
            id=id,
            context=context,
            controller=controller,
            verification_method=verification_method,
            authentication=authentication,
            assertion_method=assertion_method,
            key_agreement=key_agreement,
            capability_invocation=capability_invocation,
            capability_delegation=capability_delegation,
            service=service,
        )

        did_document.additional_properties = d
        return did_document

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
