from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.issue_credential_record import IssueCredentialRecord


T = TypeVar("T", bound="IssueCredentialRecordPage")


@attr.s(auto_attribs=True)
class IssueCredentialRecordPage:
    """
    Example:
        {'pageOf': '/prism-agent/schema-registry/schemas', 'next': '/prism-agent/schema-
            registry/schemas?skip=20&limit=10', 'previous': '/prism-agent/schema-registry/schemas?skip=0&limit=10',
            'contents': [{'validityPeriod': 3600.0, 'recordId': '80d612dc-0ded-4ac9-90b4-1b8eabb04545', 'createdAt':
            datetime.datetime(2023, 6, 13, 17, 43, 4, 562064, tzinfo=datetime.timezone.utc), 'issuingDID':
            'did:prism:issuerofverifiablecredentials', 'role': 'Issuer', 'jwtCredential': 'jwtCredential', 'claims':
            '(firstname,Alice)', 'automaticIssuance': True, 'subjectId': 'did:prism:subjectofverifiablecredentials',
            'updatedAt': datetime.datetime(2000, 1, 23, 4, 56, 7, tzinfo=datetime.timezone.utc), 'protocolState':
            'OfferPending'}, {'validityPeriod': 3600.0, 'recordId': '80d612dc-0ded-4ac9-90b4-1b8eabb04545', 'createdAt':
            datetime.datetime(2023, 6, 13, 17, 43, 4, 562064, tzinfo=datetime.timezone.utc), 'issuingDID':
            'did:prism:issuerofverifiablecredentials', 'role': 'Issuer', 'jwtCredential': 'jwtCredential', 'claims':
            '(firstname,Alice)', 'automaticIssuance': True, 'subjectId': 'did:prism:subjectofverifiablecredentials',
            'updatedAt': datetime.datetime(2000, 1, 23, 4, 56, 7, tzinfo=datetime.timezone.utc), 'protocolState':
            'OfferPending'}], 'kind': '/prism-agent/schema-registry/schemas?skip=10&limit=10', 'self': '/prism-agent/schema-
            registry/schemas?skip=10&limit=10'}

    Attributes:
        self_ (str): A string field containing the URL of the current API endpoint Example: /prism-agent/schema-
            registry/schemas?skip=10&limit=10.
        kind (str): A string field containing the URL of the current API endpoint Example: /prism-agent/schema-
            registry/schemas?skip=10&limit=10.
        page_of (str): A string field indicating the type of resource that the contents field contains Example: /prism-
            agent/schema-registry/schemas.
        next_ (Union[Unset, str]): An optional string field containing the URL of the next page of results. If the API
            response does not contain any more pages, this field should be set to None. Example: /prism-agent/schema-
            registry/schemas?skip=20&limit=10.
        previous (Union[Unset, str]): An optional string field containing the URL of the previous page of results. If
            the API response is the first page of results, this field should be set to None. Example: /prism-agent/schema-
            registry/schemas?skip=0&limit=10.
        contents (Union[Unset, List['IssueCredentialRecord']]): A sequence of IssueCredentialRecord objects representing
            the list of credential records that the API response contains
    """

    self_: str
    kind: str
    page_of: str
    next_: Union[Unset, str] = UNSET
    previous: Union[Unset, str] = UNSET
    contents: Union[Unset, List["IssueCredentialRecord"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        kind = self.kind
        page_of = self.page_of
        next_ = self.next_
        previous = self.previous
        contents: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.contents, Unset):
            contents = []
            for contents_item_data in self.contents:
                contents_item = contents_item_data.to_dict()

                contents.append(contents_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "self": self_,
                "kind": kind,
                "pageOf": page_of,
            }
        )
        if next_ is not UNSET:
            field_dict["next"] = next_
        if previous is not UNSET:
            field_dict["previous"] = previous
        if contents is not UNSET:
            field_dict["contents"] = contents

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.issue_credential_record import IssueCredentialRecord

        d = src_dict.copy()
        self_ = d.pop("self")

        kind = d.pop("kind")

        page_of = d.pop("pageOf")

        next_ = d.pop("next", UNSET)

        previous = d.pop("previous", UNSET)

        contents = []
        _contents = d.pop("contents", UNSET)
        for contents_item_data in _contents or []:
            contents_item = IssueCredentialRecord.from_dict(contents_item_data)

            contents.append(contents_item)

        issue_credential_record_page = cls(
            self_=self_,
            kind=kind,
            page_of=page_of,
            next_=next_,
            previous=previous,
            contents=contents,
        )

        issue_credential_record_page.additional_properties = d
        return issue_credential_record_page

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
