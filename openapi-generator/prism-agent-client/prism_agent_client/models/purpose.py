from enum import Enum


class Purpose(str, Enum):
    ASSERTIONMETHOD = "assertionMethod"
    AUTHENTICATION = "authentication"
    CAPABILITYDELEGATION = "capabilityDelegation"
    CAPABILITYINVOCATION = "capabilityInvocation"
    KEYAGREEMENT = "keyAgreement"

    def __str__(self) -> str:
        return str(self.value)
