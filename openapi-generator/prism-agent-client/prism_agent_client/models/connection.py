import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.connection_role import ConnectionRole
from ..models.connection_state import ConnectionState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.connection_invitation import ConnectionInvitation


T = TypeVar("T", bound="Connection")


@attr.s(auto_attribs=True)
class Connection:
    """
    Example:
        {'createdAt': datetime.datetime(2022, 3, 10, 12, 0, tzinfo=datetime.timezone.utc), 'theirDid': 'did:peer:67890',
            'role': 'Inviter', 'invitation': {'invitationUrl': 'https://my.domain.com/path?_oob=eyJAaWQiOiIzZmE4NWY2NC01NzE3
            LTQ1NjItYjNmYy0yYzk2M2Y2NmFmYTYiLCJAdHlwZSI6Imh0dHBzOi8vZGlkY29tbS5vcmcvbXktZmFtaWx5LzEuMC9teS1tZXNzYWdlLXR5cGUi
            LCJkaWQiOiJXZ1d4cXp0ck5vb0c5MlJYdnhTVFd2IiwiaW1hZ2VVcmwiOiJodHRwOi8vMTkyLjE2OC41Ni4xMDEvaW1nL2xvZ28uanBnIiwibGFi
            ZWwiOiJCb2IiLCJyZWNpcGllbnRLZXlzIjpbIkgzQzJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInJvdXRpbmdL
            ZXlzIjpbIkgzQzJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInNlcnZpY2VFbmRwb2ludCI6Imh0dHA6Ly8xOTIu
            MTY4LjU2LjEwMTo4MDIwIn0=', 'from': 'did:peer:1234457', 'id': '0527aea1-d131-3948-a34d-03af39aba8b4', 'type':
            'https://didcomm.org/out-of-band/2.0/invitation'}, 'kind': 'Connection', 'connectionId':
            '0527aea1-d131-3948-a34d-03af39aba8b4', 'self': 'https://atala-prism-products.io/connections/ABCD-1234',
            'label': 'Peter', 'myDid': 'did:peer:12345', 'state': 'InvitationGenerated', 'updatedAt':
            datetime.datetime(2022, 3, 10, 12, 0, tzinfo=datetime.timezone.utc)}

    Attributes:
        connection_id (str): The unique identifier of the connection. Example: 0527aea1-d131-3948-a34d-03af39aba8b4.
        role (ConnectionRole): The role played by the Prism agent in the connection flow. Example: Inviter.
        state (ConnectionState): The current state of the connection protocol execution. Example: InvitationGenerated.
        invitation (ConnectionInvitation): The invitation for this connection Example: {'invitationUrl': 'https://my.dom
            ain.com/path?_oob=eyJAaWQiOiIzZmE4NWY2NC01NzE3LTQ1NjItYjNmYy0yYzk2M2Y2NmFmYTYiLCJAdHlwZSI6Imh0dHBzOi8vZGlkY29tbS
            5vcmcvbXktZmFtaWx5LzEuMC9teS1tZXNzYWdlLXR5cGUiLCJkaWQiOiJXZ1d4cXp0ck5vb0c5MlJYdnhTVFd2IiwiaW1hZ2VVcmwiOiJodHRwOi
            8vMTkyLjE2OC41Ni4xMDEvaW1nL2xvZ28uanBnIiwibGFiZWwiOiJCb2IiLCJyZWNpcGllbnRLZXlzIjpbIkgzQzJBVnZMTXY2Z21NTmFtM3VWQW
            pacGZrY0pDd0R3blpuNnozd1htcVBWIl0sInJvdXRpbmdLZXlzIjpbIkgzQzJBVnZMTXY2Z21NTmFtM3VWQWpacGZrY0pDd0R3blpuNnozd1htcV
            BWIl0sInNlcnZpY2VFbmRwb2ludCI6Imh0dHA6Ly8xOTIuMTY4LjU2LjEwMTo4MDIwIn0=', 'from': 'did:peer:1234457', 'id':
            '0527aea1-d131-3948-a34d-03af39aba8b4', 'type': 'https://didcomm.org/out-of-band/2.0/invitation'}.
        created_at (datetime.datetime): The date and time the connection record was created. Example: 2022-03-10
            12:00:00+00:00.
        self_ (str): The reference to the connection resource. Example: https://atala-prism-
            products.io/connections/ABCD-1234.
        kind (str): The type of object returned. In this case a `Connection`. Example: Connection.
        label (Union[Unset, str]): A human readable alias for the connection. Example: Peter.
        my_did (Union[Unset, str]): The DID representing me as the inviter or invitee in this specific connection.
            Example: did:peer:12345.
        their_did (Union[Unset, str]): The DID representing the other peer as the an inviter or invitee in this specific
            connection. Example: did:peer:67890.
        updated_at (Union[Unset, datetime.datetime]): The date and time the connection record was last updated. Example:
            2022-03-10 12:00:00+00:00.
    """

    connection_id: str
    role: ConnectionRole
    state: ConnectionState
    invitation: "ConnectionInvitation"
    created_at: datetime.datetime
    self_: str
    kind: str
    label: Union[Unset, str] = UNSET
    my_did: Union[Unset, str] = UNSET
    their_did: Union[Unset, str] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        connection_id = self.connection_id
        role = self.role.value

        state = self.state.value

        invitation = self.invitation.to_dict()

        created_at = self.created_at.isoformat()

        self_ = self.self_
        kind = self.kind
        label = self.label
        my_did = self.my_did
        their_did = self.their_did
        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connectionId": connection_id,
                "role": role,
                "state": state,
                "invitation": invitation,
                "createdAt": created_at,
                "self": self_,
                "kind": kind,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if my_did is not UNSET:
            field_dict["myDid"] = my_did
        if their_did is not UNSET:
            field_dict["theirDid"] = their_did
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.connection_invitation import ConnectionInvitation

        d = src_dict.copy()
        connection_id = d.pop("connectionId")

        role = ConnectionRole(d.pop("role"))

        state = ConnectionState(d.pop("state"))

        invitation = ConnectionInvitation.from_dict(d.pop("invitation"))

        created_at = isoparse(d.pop("createdAt"))

        self_ = d.pop("self")

        kind = d.pop("kind")

        label = d.pop("label", UNSET)

        my_did = d.pop("myDid", UNSET)

        their_did = d.pop("theirDid", UNSET)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        connection = cls(
            connection_id=connection_id,
            role=role,
            state=state,
            invitation=invitation,
            created_at=created_at,
            self_=self_,
            kind=kind,
            label=label,
            my_did=my_did,
            their_did=their_did,
            updated_at=updated_at,
        )

        connection.additional_properties = d
        return connection

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
