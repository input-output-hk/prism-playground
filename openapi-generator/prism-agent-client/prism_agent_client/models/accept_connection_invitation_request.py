from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AcceptConnectionInvitationRequest")


@attr.s(auto_attribs=True)
class AcceptConnectionInvitationRequest:
    """
    Example:
        {'invitation': 'eyJAaWQiOiIzZmE4NWY2NC01NzE3LTQ1NjItYjNmYy0yYzk2M2Y2NmFmYTYiLCJAdHlwZSI6Imh0dHBzOi8vZGlkY29tbS5v
            cmcvbXktZmFtaWx5LzEuMC9teS1tZXNzYWdlLXR5cGUiLCJkaWQiOiJXZ1d4cXp0ck5vb0c5MlJYdnhTVFd2IiwiaW1hZ2VVcmwiOiJodHRwOi8v
            MTkyLjE2OC41Ni4xMDEvaW1nL2xvZ28uanBnIiwibGFiZWwiOiJCb2IiLCJyZWNpcGllbnRLZXlzIjpbIkgzQzJBVnZMTXY2Z21NTmFtM3VWQWpa
            cGZrY0pDd0R3blpuNnozd1htcVBWIl0sInJvdXRpbmdLZXlzIjpbIkgzQzJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBW
            Il0sInNlcnZpY2VFbmRwb2ludCI6Imh0dHA6Ly8xOTIuMTY4LjU2LjEwMTo4MDIwIn0='}

    Attributes:
        invitation (str): The base64-encoded raw invitation. Example: eyJAaWQiOiIzZmE4NWY2NC01NzE3LTQ1NjItYjNmYy0yYzk2M2
            Y2NmFmYTYiLCJAdHlwZSI6Imh0dHBzOi8vZGlkY29tbS5vcmcvbXktZmFtaWx5LzEuMC9teS1tZXNzYWdlLXR5cGUiLCJkaWQiOiJXZ1d4cXp0ck
            5vb0c5MlJYdnhTVFd2IiwiaW1hZ2VVcmwiOiJodHRwOi8vMTkyLjE2OC41Ni4xMDEvaW1nL2xvZ28uanBnIiwibGFiZWwiOiJCb2IiLCJyZWNpcG
            llbnRLZXlzIjpbIkgzQzJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInJvdXRpbmdLZXlzIjpbIkgzQzJBVnZMTX
            Y2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInNlcnZpY2VFbmRwb2ludCI6Imh0dHA6Ly8xOTIuMTY4LjU2LjEwMTo4MDIwIn
            0=.
    """

    invitation: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        invitation = self.invitation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "invitation": invitation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        invitation = d.pop("invitation")

        accept_connection_invitation_request = cls(
            invitation=invitation,
        )

        accept_connection_invitation_request.additional_properties = d
        return accept_connection_invitation_request

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
