## Issue Credential

Issuing a credential involves establishing a connection between the issuer and the holder, which is done by following the process outlined in `Example 01 - Connections`. Once the connection is established, the issuer will prepare and send a credential offer, which creates an issue record on both the issuer's and holder's agents. The holder will then retrieve the list of issue records, find the one they wish to accept, and notify the issuer of their acceptance. Finally, the issuer will issue the credential to the holder, completing the process.

This example presents the steps required to issue a credential using Atala PRISM Agents.


```python
#🚨 Run this code cell to import requirements in the Kernel
import socket
import os
import time
import datetime
import base64
import json
import jwt
import re
import requests
from pprint import pprint
from dotenv import load_dotenv
from termcolor import colored,cprint

from prism_agent_client import Client
from prism_agent_client.types import Response
from prism_agent_client.models import ErrorResponse
from prism_agent_client.models import Connection, ConnectionInvitation, CreateConnectionRequest, AcceptConnectionInvitationRequest, AcceptCredentialOfferRequest
from prism_agent_client.models import IssueCredentialRecord, CreateIssueCredentialRecordRequest, IssueCredentialRecordPage
from prism_agent_client.models import CreateManagedDidRequest, CreateManagedDIDResponse
from prism_agent_client.models import DIDOperationResponse, Service   

from prism_agent_client.api.connections_management import get_connection,create_connection,accept_connection_invitation
from prism_agent_client.api.issue_credentials_protocol import get_credential_record, get_credential_records, create_credential_offer,accept_credential_offer,issue_credential
from prism_agent_client.api.did_registrar import get_did_registrar_dids, post_did_registrar_dids, post_did_registrar_dids_didref_publications
from prism_agent_client.api.did import get_did
```

### Ultilitary functions


```python
def get_invitation_str(connection):
    parts = connection.invitation.invitation_url.split("=")
    return parts[1]

def find_credential_record_by_state(client, state):
    credential_records: Response[IssueCredentialRecordPage] = get_credential_records.sync(client=client)

    for offer in credential_records.contents:
        if(offer.protocol_state == state):
            return offer
    return None 

def to_canonical_did(long_form):
    pattern = r"did:prism:[a-fA-F0-9]{64}"
    match = re.search(pattern, long_form)
    
    if match:
        return match.group()
    else:
        return None

def print_credential_record(credential_record):
    print(f"record_id:          {credential_record.record_id}")
    print(f"subject_id:         {credential_record.subject_id}")
    print(f"role:               {credential_record.role}")
    print(f"protocol_state:     {credential_record.protocol_state}")
    print(f"created_at:         {credential_record.created_at}")
    print(f"updated_at:         {credential_record.updated_at}")
    
def print_connection(connection):
    print(f"connection_id: {connection.connection_id}")
    print(f"state:         {connection.state}")
    print(f"label:         {connection.label}")
    print(f"my_did:        {connection.my_did}")
    print(f"their_did:     {connection.their_did}")
    print(f"created_at:    {connection.created_at}")
    
troubleshooting_message = f'''
🚨 An issue occurred while attempting to interact with the PRISM Agent 🚨

- Check that the PRISM Agent you are trying to connect to is up and running, and that it is listening on the correct port. 
  You can try to connect to the Agent using a different tool to confirm that it is available. 
  (e.g. `curl --location '<host:port>/prism-agent/connections' --header 'apiKey: <key>'`) 
- Check if there are any network issues preventing the Notebook from connecting to the Agent. This can include firewalls, 
  proxies, and other network configurations.
- Ensure that the Agent URL is correct, and that the correct API Keys are provided in the variables.env file.
- If none of the above solutions work, check the logs of the Agent container to see if there are any more specific error 
  messages that can help diagnose the issue.'''

def preflight(url, api_key):
    try:
        endpoint = f'{url}/connections'
        headers = {'apiKey': api_key}
        response = requests.get(endpoint, headers=headers, timeout=15)
        if response.status_code == 200:
            print(f"URL ok: {url}")
        else:
            raise Exception(f"URL: {response.url} code: {response.status_code} content: {response.text}")
    except Exception as Ex:
        raise Exception(f'{troubleshooting_message}\n\nURL: {url}\nAPI Key: {api_key != ""}')

def use_host_docker_internal():
    try:
        socket.gethostbyname("host.docker.internal")
        return True
    except socket.gaierror: 
        return False
```

### Client instances

We will create two clients, one for the Issuer and one for the Holder, to establish a connection and perform the issue credential process.

⚠️ Remember to update the file variables.env with the URLs and API keys provided to you.



```python
env_file = "../Playground/variables.env" if use_host_docker_internal() else "../Playground/variables-linux.env"
load_dotenv(env_file)

issuerApiKey = os.getenv('ISSUER_APIKEY')
issuerUrl = os.getenv('ISSUER_URL')

holderApiKey = os.getenv('HOLDER_APIKEY')
holderUrl = os.getenv('HOLDER_URL')

issuer_client = Client(base_url=issuerUrl, headers={"apiKey": issuerApiKey})
issuer_client_did_doc = Client(base_url=issuerUrl, headers={"apiKey": issuerApiKey, "accept":"application/did+ld+json"})
holder_client = Client(base_url=holderUrl, headers={"apiKey": holderApiKey})
holder_client_did_doc = Client(base_url=holderUrl, headers={"apiKey": holderApiKey, "accept":"application/did+ld+json"})

%xmode Minimal

preflight(issuerUrl, issuerApiKey)
preflight(holderUrl, holderApiKey)

%xmode Verbose
```

    Exception reporting mode: Minimal
    URL ok: http://host.docker.internal:8080/prism-agent
    URL ok: http://host.docker.internal:8090/prism-agent
    Exception reporting mode: Verbose


### Create connection

ℹ️ For details on this see "Example 01 - Connections"


```python
print("Please wait...")

conn_request = CreateConnectionRequest()
conn_request.label = f'Issue credential {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
issuer_connection: Response[Connection] =  create_connection.sync(client=issuer_client,json_body=conn_request)

invitation = get_invitation_str(issuer_connection)

accept_conn_request = AcceptConnectionInvitationRequest(invitation)
holder_connection: Response[ConnectionInvitation] =  accept_connection_invitation.sync(client=holder_client,json_body=accept_conn_request)


issuer_connection: Response[Connection] = get_connection.sync(client=issuer_client,connection_id=issuer_connection.connection_id)
holder_connection: Response[Connection] = get_connection.sync(client=holder_client,connection_id=holder_connection.connection_id)

print(f"Issuer connection: {issuer_connection.connection_id}")
print(f"Holder connection: {holder_connection.connection_id}\n")

while (issuer_connection.state != 'ConnectionResponseSent' or 
       not(holder_connection.state == 'ConnectionResponseReceived' or holder_connection.state == 'ConnectionRequestSent')):
    issuer_connection: Response[Connection] = get_connection.sync(client=issuer_client,connection_id=issuer_connection.connection_id)
    holder_connection: Response[Connection] = get_connection.sync(client=holder_client,connection_id=holder_connection.connection_id)
    print("Issuer State: {} / Holder State: {}".format(issuer_connection.state,holder_connection.state))
    time.sleep(1)
    
print("Connection established between Issuer and Holder!")
print("\nIssuer connection:\n")
print_connection(issuer_connection)
print("\nHolder connection:\n")
print_connection(holder_connection)
```

    Please wait...
    Issuer connection: 8f2ce609-49d8-4d6a-aac8-539e4073da8b
    Holder connection: 2cfbcecb-10ad-4f91-a702-aa87e86279ef
    
    Issuer State: InvitationGenerated / Holder State: ConnectionRequestPending
    Issuer State: ConnectionResponsePending / Holder State: ConnectionRequestPending
    Issuer State: ConnectionResponsePending / Holder State: ConnectionRequestPending
    Issuer State: ConnectionResponsePending / Holder State: ConnectionResponseReceived
    Issuer State: ConnectionResponsePending / Holder State: ConnectionResponseReceived
    Issuer State: ConnectionResponseSent / Holder State: ConnectionResponseReceived
    Connection established between Issuer and Holder!
    
    Issuer connection:
    
    connection_id: 8f2ce609-49d8-4d6a-aac8-539e4073da8b
    state:         ConnectionResponseSent
    label:         Issue credential 2023-08-23 23:03:24
    my_did:        did:peer:2.Ez6LSpMwQJRZJgVNkrPvfWkZEnxMLg2E1ZAXhajmnHsnsEcwf.Vz6MkvN6gBDCCpcKcxKnHw2VT2UcxVGFRrPS8mvtyVYm16txh.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwODAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    their_did:     did:peer:2.Ez6LSq6abnz99QdaMbeyYfsLos8pbx13MNh72nFiH43VXaj5d.Vz6MkjAksrFwydvDcD24amzerwZ6cwdnNsaV7EQmhq2GnHW25.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwOTAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    created_at:    2023-08-23 23:03:24.130833+00:00
    
    Holder connection:
    
    connection_id: 2cfbcecb-10ad-4f91-a702-aa87e86279ef
    state:         ConnectionResponseReceived
    label:         <prism_agent_client.types.Unset object at 0x7fecd8d94710>
    my_did:        did:peer:2.Ez6LSq6abnz99QdaMbeyYfsLos8pbx13MNh72nFiH43VXaj5d.Vz6MkjAksrFwydvDcD24amzerwZ6cwdnNsaV7EQmhq2GnHW25.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwOTAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    their_did:     did:peer:2.Ez6LSpMwQJRZJgVNkrPvfWkZEnxMLg2E1ZAXhajmnHsnsEcwf.Vz6MkvN6gBDCCpcKcxKnHw2VT2UcxVGFRrPS8mvtyVYm16txh.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwODAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    created_at:    2023-08-23 23:03:24.151026+00:00


### Holder - Create an unpublished did:prism 

To issue a verifiable credential, the Holder must provide the credential subject to the Issuer. The credential subject is a DID identifier. We will use a long-form `did:prism` in this example. So the next step is to create an unpublished `did` on the Holder side. It is required to have a key with `purpose` equal to `assertionMethod` in the DID Document template.

ℹ️ For details on creating an unpublished `did` see "Example 02 - DID Registrar"


```python
data = { 
    "documentTemplate": {
        "publicKeys": [
            {
                "id": "key1",
                "purpose": "authentication"
            },
            {
                "id": "key2",
                "purpose": "assertionMethod"
            }
        ]
    }
}

did_request = CreateManagedDidRequest.from_dict(data)
subject_did: Response[CreateManagedDIDResponse] = post_did_registrar_dids.sync(client=holder_client, json_body=did_request)

print(f"Subject did (credential subject): {subject_did.long_form_did}")
```

    Subject did (credential subject): did:prism:aef3909689155b840c0ff54bfd765bddcda3034f0a5870e1d94e610d8a2fd063:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQLCdu6IS-UZpiPnnDLiNcVfj8cvrgpQ6V_YQq82p-5H1RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEC5_lv4JyyZvnueZQxi29RVYzxfmN2VTOjlPgiyCmGGhgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhAn2L75xrwV-tdxHIW5Izliu6K0Jql8hqxVDuwnEEEIFC


### Issuer - Create and publish a did:prism 

To issue a verifiable credential, the Issuer must provide the issuing DID. The issuing DID is a DID identifier. We will use a canonical-form `did:prism` in this example. So the next step is to create and publish a `did` on the Issuer side. It is required to have a key with `purpose` equal to `assertionMethod` in the DID Document template.

ℹ️ For details on creating and publishing a `did` see "Example 02 - DID Registrar"


```python
# Reusing the same did documentTemplate
issuing_did: Response[CreateManagedDIDResponse] = post_did_registrar_dids.sync(client=issuer_client, json_body=did_request)

print(f"Issuing did: {issuing_did.long_form_did}")

operation_response : (DIDOperationResponse) = post_did_registrar_dids_didref_publications.sync(client=issuer_client, did_ref=issuing_did.long_form_did)

print("Please wait...")

issuing_did = None

while (issuing_did is None):
    try:
        issuing_did = get_did.sync(client=issuer_client_did_doc, did_ref=operation_response.scheduled_operation.did_ref)
    except Exception as e:
        print("Please wait...")
        time.sleep(10)
    
print(f"Issuing did published: {issuing_did.id}")

```

    Issuing did: did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V
    Please wait...
    Please wait...
    Please wait...
    Issuing did published: did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571


### Issuer - Create credential claim

Now that we have the DIDs ready, the next step is for the Issuer to create the credential claim object. The credential claim contains the attributes that will be part of the verifiable credential.


```python
credential_claims = {
        "firstname": 'James',
        "lastname": 'Smith',
        "birthdate": '01/01/2000'
      }

#credential_claims = IssueCredentialRecordClaims().from_dict(data)
```

### Issuer - Send credential offer

Following, the Issuer creates a `CreateIssueCredentialRecordRequest`. It contains the `subject_id`, the `claims` and other metadata. This object is passed to the `create_credential_offer` endpoint.
The `create_credential_offer` call creates an `IssueCredentialRecord` on the issuer side, it also sends the credential offer to the Holder.


```python
credential_offer = CreateIssueCredentialRecordRequest(issuing_did=issuing_did.id,
                                                      claims=credential_claims, 
                                                      connection_id=issuer_connection.connection_id,
                                                      validity_period=3600, 
                                                      automatic_issuance=False)

issuer_credential_record: Response[IssueCredentialRecord] = create_credential_offer.sync(client=issuer_client,json_body=credential_offer)

print("\nIssuer credential record:\n")
print_credential_record(issuer_credential_record)
```

    
    Issuer credential record:
    
    record_id:          06fdc5b2-2753-4dca-8291-2c9d42ae8121
    subject_id:         <prism_agent_client.types.Unset object at 0x7fecd8d94710>
    role:               Issuer
    protocol_state:     OfferPending
    created_at:         2023-08-23 23:03:50.803209+00:00
    updated_at:         <prism_agent_client.types.Unset object at 0x7fecd8d94710>


### Holder - Wait for credential offer

The Holder waits to receive the credential offer. When received, it will show up in the Holder's credential records list as a new entry with `protocol_state` equal to `OfferReceived`. The code below waits until a credential offer is received and takes the corresponding credential_record.


```python
holder_credential_record = find_credential_record_by_state(holder_client, "OfferReceived")

while(holder_credential_record == None):
    holder_credential_record = find_credential_record_by_state(holder_client, "OfferReceived")
    time.sleep(1)
    
print("\nHolder credential record:\n")
print_credential_record(holder_credential_record)
```

    
    Holder credential record:
    
    record_id:          5e39c9e3-faf4-45e0-b5e6-df1002c00427
    subject_id:         <prism_agent_client.types.Unset object at 0x7fecd8d94710>
    role:               Holder
    protocol_state:     OfferReceived
    created_at:         2023-08-23 23:03:50.899432+00:00
    updated_at:         <prism_agent_client.types.Unset object at 0x7fecd8d94710>


### Holder - Accept credential offer

Now the Holder uses the `accept_credential_offer` endpoint to accept the credential offer. It must provide the `record_id` of the offer. Accepting the credential offer tells the Issuer that the credential can be issued.


```python
accept_credential = AcceptCredentialOfferRequest(subject_id=to_canonical_did(subject_did.long_form_did))

holder_credential_record: Response[IssueCredentialRecord] = accept_credential_offer.sync(client=holder_client, record_id=holder_credential_record.record_id, json_body=accept_credential)
print("\nHolder credential record:\n")
print_credential_record(holder_credential_record)
```

    
    Holder credential record:
    
    record_id:          5e39c9e3-faf4-45e0-b5e6-df1002c00427
    subject_id:         did:prism:aef3909689155b840c0ff54bfd765bddcda3034f0a5870e1d94e610d8a2fd063
    role:               Holder
    protocol_state:     RequestPending
    created_at:         2023-08-23 23:03:50.899432+00:00
    updated_at:         2023-08-23 23:03:52.942277+00:00


### Issuer - Wait for credential request

The Issuer waits to receive the credential request. When received, the credential record state will change to `RequestReceived` in the Issuer's credential records list. The code below waits until a credential request is received and takes the corresponding credential_record.


```python
print("Please wait...")

issuer_credential_record = get_credential_record.sync(client=issuer_client, record_id=issuer_credential_record.record_id)

print(f"Issuer credential record: {issuer_credential_record.record_id}")
print(f"Holder credential record: {holder_credential_record.record_id}\n")

while(issuer_credential_record.protocol_state != "RequestReceived"):
    issuer_credential_record = get_credential_record.sync(client=issuer_client, record_id=issuer_credential_record.record_id)
    holder_credential_record = get_credential_record.sync(client=holder_client, record_id=holder_credential_record.record_id)
    print(f"Issuer state: {issuer_credential_record.protocol_state} / Holder State: {holder_credential_record.protocol_state}")
    time.sleep(1)
    
print("\nIssuer credential record:\n")
print_credential_record(issuer_credential_record)
```

    Please wait...
    Issuer credential record: 06fdc5b2-2753-4dca-8291-2c9d42ae8121
    Holder credential record: 5e39c9e3-faf4-45e0-b5e6-df1002c00427
    
    Issuer state: OfferSent / Holder State: RequestPending
    Issuer state: OfferSent / Holder State: RequestPending
    Issuer state: OfferSent / Holder State: RequestGenerated
    Issuer state: OfferSent / Holder State: RequestGenerated
    Issuer state: RequestReceived / Holder State: RequestGenerated
    
    Issuer credential record:
    
    record_id:          06fdc5b2-2753-4dca-8291-2c9d42ae8121
    subject_id:         <prism_agent_client.types.Unset object at 0x7fecd8d94710>
    role:               Issuer
    protocol_state:     RequestReceived
    created_at:         2023-08-23 23:03:50.803209+00:00
    updated_at:         2023-08-23 23:03:56.774537+00:00


### Issuer - Accept credential request (issue credential to holder)

The Issuer uses the `issue_credential` endpoint to issue the credential. It must provide the `record_id`. When issued the record state changes to `CredentialSent` and the credential is send to the Holder.


```python
issuer_credential_record: Response[IssueCredentialRecord] = issue_credential.sync(client=issuer_client, record_id=issuer_credential_record.record_id)
print("\nIssuer credential record:\n")
print_credential_record(issuer_credential_record)
```

    
    Issuer credential record:
    
    record_id:          06fdc5b2-2753-4dca-8291-2c9d42ae8121
    subject_id:         <prism_agent_client.types.Unset object at 0x7fecd8d94710>
    role:               Issuer
    protocol_state:     CredentialPending
    created_at:         2023-08-23 23:03:50.803209+00:00
    updated_at:         2023-08-23 23:03:58.157599+00:00


### Holder - Wait for credential

The Holder waits to receive the credential. When received, it will be added to the Holder's credential record and the `protocol_state` will be updated to `CredentialReceived`. The code below waits until a credential is received.


```python
print("Please wait...")

holder_credential_record = get_credential_record.sync(client=holder_client, record_id=holder_credential_record.record_id)

print(f"Issuer credential record: {issuer_credential_record.record_id}")
print(f"Holder credential record: {holder_credential_record.record_id}\n")

while(holder_credential_record.protocol_state != "CredentialReceived"):
    issuer_credential_record = get_credential_record.sync(client=issuer_client, record_id=issuer_credential_record.record_id)
    holder_credential_record = get_credential_record.sync(client=holder_client, record_id=holder_credential_record.record_id)
    print(f"Issuer state: {issuer_credential_record.protocol_state} / Holder State: {holder_credential_record.protocol_state}")
    time.sleep(1)

print("\nHolder credential record:\n")
print_credential_record(holder_credential_record)
```

    Please wait...
    Issuer credential record: 06fdc5b2-2753-4dca-8291-2c9d42ae8121
    Holder credential record: 5e39c9e3-faf4-45e0-b5e6-df1002c00427
    
    Issuer state: CredentialPending / Holder State: RequestGenerated
    Issuer state: CredentialGenerated / Holder State: RequestSent
    Issuer state: CredentialGenerated / Holder State: RequestSent
    Issuer state: CredentialGenerated / Holder State: CredentialReceived
    
    Holder credential record:
    
    record_id:          5e39c9e3-faf4-45e0-b5e6-df1002c00427
    subject_id:         did:prism:aef3909689155b840c0ff54bfd765bddcda3034f0a5870e1d94e610d8a2fd063
    role:               Holder
    protocol_state:     CredentialReceived
    created_at:         2023-08-23 23:03:50.899432+00:00
    updated_at:         2023-08-23 23:04:01.119231+00:00


### JWT Credential

The JWT Credential is available in the holder credential record. The website https://jwt.io/ can be used to decode the credential.


```python
print(base64.b64decode(holder_credential_record.jwt_credential).decode())
```

    eyJhbGciOiJFUzI1NksifQ.eyJpc3MiOiJkaWQ6cHJpc206ODE0NmMxNDdlNmM5ZmZlNGRhN2M2ZjIzZDI0MWM2MDZlYTFjNzIzYzY0ZDNkODY1Y2M5NWQ0ODgwN2M4NDU3MTpDclFCQ3JFQkVqZ0tCR3RsZVRFUUJFb3VDZ2x6WldOd01qVTJhekVTSVFOd1hza3QtaExIenVHb0hxVk1IYnVWdjJ5dmFTc1JHZnozczJETnhXaDkwUkk0Q2dSclpYa3lFQUpLTGdvSmMyVmpjREkxTm1zeEVpRURoc2RzQk42NW1lMGZWMmlXel83R3hHNTJLd2lRd2t6S01abENYNU9CTmtnU093b0hiV0Z6ZEdWeU1CQUJTaTRLQ1hObFkzQXlOVFpyTVJJaEEyeDdmbC1zQl8zWExmWWFHY3F6S1pSMG9lZExTZko5VUNyc1ZrQU9jbzlWIiwic3ViIjoiZGlkOnByaXNtOmFlZjM5MDk2ODkxNTViODQwYzBmZjU0YmZkNzY1YmRkY2RhMzAzNGYwYTU4NzBlMWQ5NGU2MTBkOGEyZmQwNjM6Q3JRQkNyRUJFamdLQkd0bGVURVFCRW91Q2dselpXTndNalUyYXpFU0lRTENkdTZJUy1VWnBpUG5uRExpTmNWZmo4Y3ZyZ3BRNlZfWVFxODJwLTVIMVJJNENnUnJaWGt5RUFKS0xnb0pjMlZqY0RJMU5tc3hFaUVDNV9sdjRKeXladm51ZVpReGkyOVJWWXp4Zm1OMlZUT2psUGdpeUNtR0doZ1NPd29IYldGemRHVnlNQkFCU2k0S0NYTmxZM0F5TlRack1SSWhBbjJMNzV4cndWLXRkeEhJVzVJemxpdTZLMEpxbDhocXhWRHV3bkVFRUlGQyIsIm5iZiI6MTY5MjgzMTgzOCwiZXhwIjoxNjkyODM1NDM4LCJ2YyI6eyJjcmVkZW50aWFsU3ViamVjdCI6eyJmaXJzdG5hbWUiOiJKYW1lcyIsImJpcnRoZGF0ZSI6IjAxXC8wMVwvMjAwMCIsImlkIjoiZGlkOnByaXNtOmFlZjM5MDk2ODkxNTViODQwYzBmZjU0YmZkNzY1YmRkY2RhMzAzNGYwYTU4NzBlMWQ5NGU2MTBkOGEyZmQwNjM6Q3JRQkNyRUJFamdLQkd0bGVURVFCRW91Q2dselpXTndNalUyYXpFU0lRTENkdTZJUy1VWnBpUG5uRExpTmNWZmo4Y3ZyZ3BRNlZfWVFxODJwLTVIMVJJNENnUnJaWGt5RUFKS0xnb0pjMlZqY0RJMU5tc3hFaUVDNV9sdjRKeXladm51ZVpReGkyOVJWWXp4Zm1OMlZUT2psUGdpeUNtR0doZ1NPd29IYldGemRHVnlNQkFCU2k0S0NYTmxZM0F5TlRack1SSWhBbjJMNzV4cndWLXRkeEhJVzVJemxpdTZLMEpxbDhocXhWRHV3bkVFRUlGQyIsImxhc3RuYW1lIjoiU21pdGgifSwidHlwZSI6WyJWZXJpZmlhYmxlQ3JlZGVudGlhbCJdLCJAY29udGV4dCI6WyJodHRwczpcL1wvd3d3LnczLm9yZ1wvMjAxOFwvY3JlZGVudGlhbHNcL3YxIl19fQ.dpvehrnTk1ZZMQGmRxvdOlluk9dGGmn8BqjC4dvADn2XhcevIv0HoH7jSdiLMzYU42C_lZEGzBU3CiULVjOO0A


### ⚠️ Important Note
Keep the Holder credential record identifier at hand, it will be needed to run the next example:


```python
print(f"\nHolder credential record_id: {holder_credential_record.record_id}\n")
%store holder_credential_record
```

    
    Holder credential record_id: 5e39c9e3-faf4-45e0-b5e6-df1002c00427
    
    Stored 'holder_credential_record' (IssueCredentialRecord)


### Decode verifiable credential

As an alternative to the website https://jwt.io/ below you will find the code to perform the verifiable credential decoding programmatically:

#### Unverified Decoding


```python
try:
    jwt_decoded_id_token = jwt.decode(base64.b64decode(holder_credential_record.jwt_credential).decode(), options={"verify_signature": False})
    # print(jwt_decoded_id_token)
    print(json.dumps(jwt_decoded_id_token, indent=2))
except (jwt.ExpiredSignatureError, jwt.InvalidAudienceError) as e:
    print("[ERROR]", e)
```

    {
      "iss": "did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V",
      "sub": "did:prism:aef3909689155b840c0ff54bfd765bddcda3034f0a5870e1d94e610d8a2fd063:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQLCdu6IS-UZpiPnnDLiNcVfj8cvrgpQ6V_YQq82p-5H1RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEC5_lv4JyyZvnueZQxi29RVYzxfmN2VTOjlPgiyCmGGhgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhAn2L75xrwV-tdxHIW5Izliu6K0Jql8hqxVDuwnEEEIFC",
      "nbf": 1692831838,
      "exp": 1692835438,
      "vc": {
        "credentialSubject": {
          "firstname": "James",
          "birthdate": "01/01/2000",
          "id": "did:prism:aef3909689155b840c0ff54bfd765bddcda3034f0a5870e1d94e610d8a2fd063:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQLCdu6IS-UZpiPnnDLiNcVfj8cvrgpQ6V_YQq82p-5H1RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEC5_lv4JyyZvnueZQxi29RVYzxfmN2VTOjlPgiyCmGGhgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhAn2L75xrwV-tdxHIW5Izliu6K0Jql8hqxVDuwnEEEIFC",
          "lastname": "Smith"
        },
        "type": [
          "VerifiableCredential"
        ],
        "@context": [
          "https://www.w3.org/2018/credentials/v1"
        ]
      }
    }


#### Verified Decoding

##### Resolve Issuer DID


```python
did = None
while (did is None):
    try:
        did = get_did.sync(client=holder_client_did_doc, did_ref=jwt_decoded_id_token['iss'])
    except Exception as e:
        print("Please wait...")
        time.sleep(10)

print(did.to_dict())
```

    {'id': 'did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V', '@context': ['https://www.w3.org/ns/did/v1', 'https://w3id.org/security/suites/jws-2020/v1'], 'controller': 'did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V', 'verificationMethod': [{'id': 'did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V#key1', 'type': 'JsonWebKey2020', 'controller': 'did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V', 'publicKeyJwk': {'kty': 'EC', 'crv': 'secp256k1', 'x': 'cF7JLfoSx87hqB6lTB27lb9sr2krERn897NgzcVofdE', 'y': 'pQsBOs7dzC3Mk4HBvz6L7FVoULtcngsoqwczonodbjc'}}, {'id': 'did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V#key2', 'type': 'JsonWebKey2020', 'controller': 'did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V', 'publicKeyJwk': {'kty': 'EC', 'crv': 'secp256k1', 'x': 'hsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkg', 'y': '1MfsCfGuDNAShgNn_joNdElkLISpR6gnUfd_RrhVaMU'}}], 'authentication': ['did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V#key1'], 'assertionMethod': ['did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V#key2'], 'keyAgreement': [], 'capabilityInvocation': [], 'capabilityDelegation': [], 'service': []}


##### Extract assertion public JWK


```python
for verification_method in did.verification_method:
    if verification_method.id == did.assertion_method[0]:
        print('Issuer KeyId\n',verification_method.id)
        print('Issuer KeyId JWK\n',verification_method.public_key_jwk)
        issuer_jwk = verification_method.public_key_jwk

issuer_pubKey = jwt.algorithms.ECAlgorithm.from_jwk(json.dumps(issuer_jwk.to_dict()))
```

    Issuer KeyId
     did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V#key2
    Issuer KeyId JWK
     PublicKeyJwk(kty='EC', crv='secp256k1', x='hsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkg', y='1MfsCfGuDNAShgNn_joNdElkLISpR6gnUfd_RrhVaMU', additional_properties={})


##### Verify Verifiable Credential against resolved Issuer DID and associated authentication public JWK


```python
try:
    jwt_verified_decoded_id_token = jwt.decode(base64.b64decode(holder_credential_record.jwt_credential).decode(), key = issuer_pubKey, algorithms=["ES256K"])
    # print(jwt_decoded_id_token)
    print(json.dumps(jwt_verified_decoded_id_token, indent=2))
    print("JWT Signature Verification Successful!")
except (jwt.ExpiredSignatureError, jwt.InvalidAudienceError) as e:
    print("[ERROR]", e)
```

    {
      "iss": "did:prism:8146c147e6c9ffe4da7c6f23d241c606ea1c723c64d3d865cc95d48807c84571:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNwXskt-hLHzuGoHqVMHbuVv2yvaSsRGfz3s2DNxWh90RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDhsdsBN65me0fV2iWz_7GxG52KwiQwkzKMZlCX5OBNkgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA2x7fl-sB_3XLfYaGcqzKZR0oedLSfJ9UCrsVkAOco9V",
      "sub": "did:prism:aef3909689155b840c0ff54bfd765bddcda3034f0a5870e1d94e610d8a2fd063:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQLCdu6IS-UZpiPnnDLiNcVfj8cvrgpQ6V_YQq82p-5H1RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEC5_lv4JyyZvnueZQxi29RVYzxfmN2VTOjlPgiyCmGGhgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhAn2L75xrwV-tdxHIW5Izliu6K0Jql8hqxVDuwnEEEIFC",
      "nbf": 1692831838,
      "exp": 1692835438,
      "vc": {
        "credentialSubject": {
          "firstname": "James",
          "birthdate": "01/01/2000",
          "id": "did:prism:aef3909689155b840c0ff54bfd765bddcda3034f0a5870e1d94e610d8a2fd063:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQLCdu6IS-UZpiPnnDLiNcVfj8cvrgpQ6V_YQq82p-5H1RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEC5_lv4JyyZvnueZQxi29RVYzxfmN2VTOjlPgiyCmGGhgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhAn2L75xrwV-tdxHIW5Izliu6K0Jql8hqxVDuwnEEEIFC",
          "lastname": "Smith"
        },
        "type": [
          "VerifiableCredential"
        ],
        "@context": [
          "https://www.w3.org/2018/credentials/v1"
        ]
      }
    }
    JWT Signature Verification Successful!


##### Verify verifiable credential (with modification) against resolved Issuer DID and associated authentication public JWK
> NOTE!! This should fail as we tampered with the verifiable credential


```python
jwt_tampered_id_token = base64.b64decode(holder_credential_record.jwt_credential).decode() + 'x'

try:
    jwt_tampered_decoded_id_token = jwt.decode(jwt_tampered_id_token, key = issuer_pubKey, algorithms=["ES256K"])
    # print(jwt_decoded_id_token)
    # print(json.dumps(jwt_tampered_decoded_id_token, indent=2))
except (jwt.ExpiredSignatureError, jwt.InvalidAudienceError, jwt.InvalidSignatureError) as e:
    print("[ERROR]", e)
```

    [ERROR] Signature verification failed



```python

```


```python

```
