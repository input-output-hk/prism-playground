## Present proof

Presenting a proof involves establishing a connection between the issuer and the holder, which is done by following the process outlined in `Example 01 - Connections`. Once the connection is established, the verifier will prepare and send a proof request, which creates a presentation record on both the verifier's and holder's agents. The holder will then retrieve the list of presentations, find the one they wish to accept, and notify the verifier of their acceptance. The accept proof message contains an id of a credential stored in the Holders Agent. Finally, the Verifier will receive the proof from the holder, completing the process.

Note: the terminology "proof request" and "presentation request" may be used interchangeably 

### ⚠️ Important Note 
Please run *Example 03 - Issue Credential* before continuing with this example. 


```python
#🚨 Run this code cell to import requirements in the Kernel
import socket
import os
import time
import datetime
import base64
import jwt
import json
import requests
from pprint import pprint
from dotenv import load_dotenv

from prism_agent_client import Client
from prism_agent_client.types import Response, Unset
from prism_agent_client.models import Connection,ConnectionInvitation,CreateConnectionRequest,AcceptConnectionInvitationRequest
from prism_agent_client.models import PresentationStatus, ErrorResponse, Proof, ProofRequestAux, PublicKeyJwk, RequestPresentationInput, RequestPresentationOutput, RequestPresentationAction, RequestPresentationActionAction
from prism_agent_client.models import IssueCredentialRecord, CreateIssueCredentialRecordRequest, IssueCredentialRecordPage
from prism_agent_client.models import DIDDocumentMetadata, DIDOperationResponse, DidOperationSubmission, Service  
from prism_agent_client.api.connections_management import get_connections,get_connection,create_connection,accept_connection_invitation
from prism_agent_client.api.issue_credentials_protocol import get_credential_record, get_credential_records, create_credential_offer,accept_credential_offer,issue_credential
from prism_agent_client.api.present_proof import get_presentation, get_all_presentation, request_presentation, update_presentation
from prism_agent_client.api.did import get_did

```

### Ultilitary functions


```python
def get_invitation_str(connection):
    parts = connection.invitation.invitation_url.split("=")
    return parts[1]

def find_proof_request_by_state(client, state):
    proof_requests: Response[PresentationStatus] = get_all_presentation.sync(client=client)
    for proof_request in proof_requests.contents:
        if(proof_request.status == state):
            return proof_request
    return None 

def find_proof_requests_by_state(client, state):
    proof_requests: Response[PresentationStatus] = get_all_presentation.sync(client=client)
    matching_proof_requests = [] 

    for proof_request in proof_requests.contents:
        if proof_request.status == state:
            matching_proof_requests.append(proof_request)

    return matching_proof_requests  


def find_credential(client):
    credential_records: Response[IssueCredentialRecordPage] = get_credential_records.sync(client=client)
    for offer in credential_records.contents:
        if not (type(offer.jwt_credential) is Unset):
            return offer
    return None 

def print_proof_request(proof_request):
    if hasattr(proof_request, "presentation_id"):
        print(f"presentation_id: {proof_request.presentation_id}")
    if hasattr(proof_request, "status"):
        print(f"status:          {proof_request.status}")
    if hasattr(proof_request, "connection_id"):
        print(f"connection_id:   {proof_request.connection_id}")
        
def print_proof_requests(proof_requests):
    for proof_request in proof_requests:
        print_proof_request(proof_request)

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

We will create two separate clients, one for the Verifier and one for the Holder, in order to establish a connection between the two.

⚠️ Remember to update the file variables.env with the URLs and API keys provided to you.



```python
env_file = "../Playground/variables.env" if use_host_docker_internal() else "../Playground/variables-linux.env"
load_dotenv(env_file)

verifierApiKey = os.getenv('VERIFIER_APIKEY')
verifierUrl = os.getenv('VERIFIER_URL')

holderApiKey = os.getenv('HOLDER_APIKEY')
holderUrl = os.getenv('HOLDER_URL')

verifier_client = Client(base_url=verifierUrl, headers={"apiKey": verifierApiKey})
verifier_client_did_doc = Client(base_url=verifierUrl, headers={"apiKey": verifierApiKey, "accept":"application/did+ld+json"})
holder_client = Client(base_url=holderUrl, headers={"apiKey": holderApiKey})

%xmode Minimal

preflight(verifierUrl, verifierApiKey)
preflight(holderUrl, holderApiKey)

%xmode Verbose
```

    Exception reporting mode: Minimal
    URL ok: http://host.docker.internal:9000/prism-agent
    URL ok: http://host.docker.internal:8090/prism-agent
    Exception reporting mode: Verbose


### Create connection

ℹ️ For details on this see "Example 01 - Connections"


```python
print("Please wait...")

conn_request = CreateConnectionRequest()
conn_request.label = f'Present proof {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
verifier_connection: Response[Connection] =  create_connection.sync(client=verifier_client,json_body=conn_request)

invitation = get_invitation_str(verifier_connection)

accept_conn_request = AcceptConnectionInvitationRequest(invitation)
holder_connection: Response[ConnectionInvitation] =  accept_connection_invitation.sync(client=holder_client,json_body=accept_conn_request)

verifier_connection: Response[Connection] = get_connection.sync(client=verifier_client,connection_id=verifier_connection.connection_id)
holder_connection: Response[Connection] = get_connection.sync(client=holder_client,connection_id=holder_connection.connection_id)

while (verifier_connection.state != 'ConnectionResponseSent' or 
       not(holder_connection.state == 'ConnectionResponseReceived' or holder_connection.state == 'ConnectionRequestSent')):
    verifier_connection: Response[Connection] = get_connection.sync(client=verifier_client,connection_id=verifier_connection.connection_id)
    holder_connection: Response[Connection] = get_connection.sync(client=holder_client,connection_id=holder_connection.connection_id)
    print("Verifier State: {} / Holder State: {} \n".format(verifier_connection.state,holder_connection.state))
    time.sleep(1)
    
print("Connection established between verifier and Holder!")
print("\nVerifier connection:\n")
print_connection(verifier_connection)
print("\nHolder connection:\n")
print_connection(holder_connection)
```

    Please wait...
    Verifier State: InvitationGenerated / Holder State: ConnectionRequestPending 
    
    Verifier State: InvitationGenerated / Holder State: ConnectionRequestPending 
    
    Verifier State: ConnectionResponsePending / Holder State: ConnectionRequestPending 
    
    Verifier State: ConnectionResponsePending / Holder State: ConnectionRequestPending 
    
    Verifier State: ConnectionResponsePending / Holder State: ConnectionResponseReceived 
    
    Verifier State: ConnectionResponsePending / Holder State: ConnectionResponseReceived 
    
    Verifier State: ConnectionResponseSent / Holder State: ConnectionResponseReceived 
    
    Connection established between verifier and Holder!
    
    Verifier connection:
    
    connection_id: 8c7b94c3-0baf-4b46-956e-f7d4af2b73f4
    state:         ConnectionResponseSent
    label:         Present proof 2023-08-23 23:09:31
    my_did:        did:peer:2.Ez6LShB4Fr6Her9SQp4jtbP3HprWsApnNiebtQkHm4DAwEdgH.Vz6Mkum79zkmChJwDLSt1ZrictuizS23zVtK27AbeE4oDDR1Q.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjkwMDAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    their_did:     did:peer:2.Ez6LSijWkHNM53tymhgi4FbxKVBcL5jeua7GGVpCnsvCYwyPW.Vz6MkeWpwdioTYjEb5jaDanRHtR8kPCViiBG66BHQqpA5oX3W.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwOTAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    created_at:    2023-08-23 23:09:31.378177+00:00
    
    Holder connection:
    
    connection_id: 9ff1cb9d-610f-4d5e-a2c1-ec6174c2aedd
    state:         ConnectionResponseReceived
    label:         <prism_agent_client.types.Unset object at 0x7f37b4f6c090>
    my_did:        did:peer:2.Ez6LSijWkHNM53tymhgi4FbxKVBcL5jeua7GGVpCnsvCYwyPW.Vz6MkeWpwdioTYjEb5jaDanRHtR8kPCViiBG66BHQqpA5oX3W.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwOTAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    their_did:     did:peer:2.Ez6LShB4Fr6Her9SQp4jtbP3HprWsApnNiebtQkHm4DAwEdgH.Vz6Mkum79zkmChJwDLSt1ZrictuizS23zVtK27AbeE4oDDR1Q.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjkwMDAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    created_at:    2023-08-23 23:09:31.412416+00:00


### Verifier - Create proof request
The Verifier prepares the proof request, it uses the `connection_id` of the connection with the Holder to define where to send the request. The `proofs` describe the credential requested 


```python
data = {
    "description":"Request presentation of credential",
    "connectionId": verifier_connection.connection_id,
    "options":{
        "challenge": "11c91493-01b3-4c4d-ac36-b336bab5bddf",
        "domain": "https://example-verifier.com"
    },
    "proofs":[
        {
            "schemaId": "https://schema.org/Person",
            "trustIssuers": [
                "did:web:atalaprism.io/users/testUser"
            ]
        }
    ]
}

proof_request = RequestPresentationInput.from_dict(data)
```

### Verifier - Send proof request

The Verifier sends the proof request. This action creates the presentation record in the Verifier side and sends the request to the Holder using the connection


```python
verifier_proof_request: Response[RequestPresentationInput] = request_presentation.sync(client=verifier_client, json_body=proof_request)
print("\nVerifier proof request:\n")
print_proof_request(verifier_proof_request)
```

    
    Verifier proof request:
    
    presentation_id: 2411274e-bac6-42bd-8cad-b764a62bbf98


### Holder - Wait for proof request

The Holder waits to receive the request


```python
print("Please wait...")

holder_proof_requests = find_proof_requests_by_state(holder_client, "RequestReceived")

while(holder_proof_requests == []):
    holder_proof_requests = find_proof_requests_by_state(holder_client, "RequestReceived")
    time.sleep(1)

print("\nHolder proof requests:\n")
print_proof_requests(holder_proof_requests)
```

    Please wait...
    
    Holder proof requests:
    
    presentation_id: f6b2c0e5-12c1-49fb-941a-4433fc1c33da
    status:          RequestReceived
    connection_id:   <prism_agent_client.types.Unset object at 0x7f37b4f6c090>


### Holder - Accept proof request

The Holder accepts the proof request by updating the presentation record with the action `REQUEST_ACCEPT`. The update also provides the `proof_id` corresponding to the credential used to fulfill the proof request.

⚠️ The program will prompt for a credential `record_id`. Provide the one obtained at the last step of *Example 03 - Issue Credential*  
To make it easier we will automatically load the `record_id` from *Example 03 - Issue Credential* with `%store -r holder_credential_record`

**Note: `record_id` and `proof_id` refer to the same value**


```python
# retrieve holder credential record_id from Example 03 - Issue Credential notebook
%store -r holder_credential_record

def valid_credential(client, record_id):
    credential_record = get_credential_record.sync(client=client, record_id=record_id)
    print(credential_record)
    if credential_record is None:
        return False
    elif type(credential_record.jwt_credential) is Unset:
        return False
    else:
        return True

while True:
    # credential_record_id = input("\nprovide a credential record_id").strip()
    credential_record_id = holder_credential_record.record_id
    if credential_record_id == "":
        print(f"\n🚨 The provided credential record is not valid. Please create a credential on this agent {holderUrl} to proceed")
    elif(valid_credential(holder_client, credential_record_id)):
        print(f"\n✅ Credential record is correct: {credential_record_id}")
        break
    else:
        print(f"\n🚨 The provided credential is not valid. Please create a credential on this agent {holderUrl} to proceed")

action = RequestPresentationAction(action=RequestPresentationActionAction.REQUEST_ACCEPT, proof_id=[credential_record_id])


for holder_proof_request in holder_proof_requests:
    update_presentation.sync(client=holder_client, json_body=action, presentation_id=holder_proof_request.presentation_id)

    print("\nHolder proof request:\n")
    print(holder_proof_request.presentation_id)

```

    IssueCredentialRecord(record_id='5e39c9e3-faf4-45e0-b5e6-df1002c00427', thid='5a53a986-2d83-404b-9a01-08c8c07f962c', claims={'firstname': 'James', 'lastname': 'Smith', 'birthdate': '01/01/2000'}, created_at=datetime.datetime(2023, 8, 23, 23, 3, 50, 899432, tzinfo=tzutc()), role='Holder', protocol_state='CredentialReceived', subject_id='did:prism:aef3909689155b840c0ff54bfd765bddcda3034f0a5870e1d94e610d8a2fd063', validity_period=<prism_agent_client.types.Unset object at 0x7f37b4f6c090>, automatic_issuance=<prism_agent_client.types.Unset object at 0x7f37b4f6c090>, updated_at=datetime.datetime(2023, 8, 23, 23, 4, 1, 119231, tzinfo=tzutc()), jwt_credential='ZXlKaGJHY2lPaUpGVXpJMU5rc2lmUS5leUpwYzNNaU9pSmthV1E2Y0hKcGMyMDZPREUwTm1NeE5EZGxObU01Wm1abE5HUmhOMk0yWmpJelpESTBNV00yTURabFlURmpOekl6WXpZMFpETmtPRFkxWTJNNU5XUTBPRGd3TjJNNE5EVTNNVHBEY2xGQ1EzSkZRa1ZxWjB0Q1IzUnNaVlJGVVVKRmIzVkRaMng2V2xkT2QwMXFWVEpoZWtWVFNWRk9kMWh6YTNRdGFFeEllblZIYjBoeFZrMUlZblZXZGpKNWRtRlRjMUpIWm5vemN6SkVUbmhYYURrd1VrazBRMmRTY2xwWWEzbEZRVXBMVEdkdlNtTXlWbXBqUkVreFRtMXplRVZwUlVSb2MyUnpRazQyTlcxbE1HWldNbWxYZWw4M1IzaEhOVEpMZDJsUmQydDZTMDFhYkVOWU5VOUNUbXRuVTA5M2IwaGlWMFo2WkVkV2VVMUNRVUpUYVRSTFExaE9iRmt6UVhsT1ZGcHlUVkpKYUVFeWVEZG1iQzF6UWw4eldFeG1XV0ZIWTNGNlMxcFNNRzlsWkV4VFprbzVWVU55YzFaclFVOWpiemxXSWl3aWMzVmlJam9pWkdsa09uQnlhWE50T21GbFpqTTVNRGsyT0RreE5UVmlPRFF3WXpCbVpqVTBZbVprTnpZMVltUmtZMlJoTXpBek5HWXdZVFU0TnpCbE1XUTVOR1UyTVRCa09HRXlabVF3TmpNNlEzSlJRa055UlVKRmFtZExRa2QwYkdWVVJWRkNSVzkxUTJkc2VscFhUbmROYWxVeVlYcEZVMGxSVEVOa2RUWkpVeTFWV25CcFVHNXVSRXhwVG1OV1ptbzRZM1p5WjNCUk5sWmZXVkZ4T0RKd0xUVklNVkpKTkVOblVuSmFXR3Q1UlVGS1MweG5iMHBqTWxacVkwUkpNVTV0YzNoRmFVVkROVjlzZGpSS2VYbGFkbTUxWlZwUmVHa3lPVkpXV1hwNFptMU9NbFpVVDJwc1VHZHBlVU50UjBkb1oxTlBkMjlJWWxkR2VtUkhWbmxOUWtGQ1UyazBTME5ZVG14Wk0wRjVUbFJhY2sxU1NXaEJiakpNTnpWNGNuZFdMWFJrZUVoSlZ6VkplbXhwZFRaTE1FcHhiRGhvY1hoV1JIVjNia1ZGUlVsR1F5SXNJbTVpWmlJNk1UWTVNamd6TVRnek9Dd2laWGh3SWpveE5qa3lPRE0xTkRNNExDSjJZeUk2ZXlKamNtVmtaVzUwYVdGc1UzVmlhbVZqZENJNmV5Sm1hWEp6ZEc1aGJXVWlPaUpLWVcxbGN5SXNJbUpwY25Sb1pHRjBaU0k2SWpBeFhDOHdNVnd2TWpBd01DSXNJbWxrSWpvaVpHbGtPbkJ5YVhOdE9tRmxaak01TURrMk9Ea3hOVFZpT0RRd1l6Qm1aalUwWW1aa056WTFZbVJrWTJSaE16QXpOR1l3WVRVNE56QmxNV1E1TkdVMk1UQmtPR0V5Wm1Rd05qTTZRM0pSUWtOeVJVSkZhbWRMUWtkMGJHVlVSVkZDUlc5MVEyZHNlbHBYVG5kTmFsVXlZWHBGVTBsUlRFTmtkVFpKVXkxVlduQnBVRzV1UkV4cFRtTldabW80WTNaeVozQlJObFpmV1ZGeE9ESndMVFZJTVZKSk5FTm5VbkphV0d0NVJVRktTMHhuYjBwak1sWnFZMFJKTVU1dGMzaEZhVVZETlY5c2RqUktlWGxhZG01MVpWcFJlR2t5T1ZKV1dYcDRabTFPTWxaVVQycHNVR2RwZVVOdFIwZG9aMU5QZDI5SVlsZEdlbVJIVm5sTlFrRkNVMmswUzBOWVRteFpNMEY1VGxSYWNrMVNTV2hCYmpKTU56VjRjbmRXTFhSa2VFaEpWelZKZW14cGRUWkxNRXB4YkRob2NYaFdSSFYzYmtWRlJVbEdReUlzSW14aGMzUnVZVzFsSWpvaVUyMXBkR2dpZlN3aWRIbHdaU0k2V3lKV1pYSnBabWxoWW14bFEzSmxaR1Z1ZEdsaGJDSmRMQ0pBWTI5dWRHVjRkQ0k2V3lKb2RIUndjenBjTDF3dmQzZDNMbmN6TG05eVoxd3ZNakF4T0Z3dlkzSmxaR1Z1ZEdsaGJITmNMM1l4SWwxOWZRLmRwdmVocm5UazFaWk1RR21SeHZkT2xsdWs5ZEdHbW44QnFqQzRkdkFEbjJYaGNldkl2MEhvSDdqU2RpTE16WVU0MkNfbFpFR3pCVTNDaVVMVmpPTzBB', issuing_did=<prism_agent_client.types.Unset object at 0x7f37b4f6c090>, additional_properties={})
    
    ✅ Credential record is correct: 5e39c9e3-faf4-45e0-b5e6-df1002c00427
    
    Holder proof request:
    
    f6b2c0e5-12c1-49fb-941a-4433fc1c33da


### Verifier - Wait for verification

The Verifier waits for the proof. Once received, it updates the status of the presentation and gets the verifiable presentation data.   
ℹ️ Note the status of the presentation after this step is `PresentationVerified`


```python
print("Please wait...")

verifier_proof_request: Response[PresentationStatus] = get_presentation.sync(client=verifier_client, presentation_id=verifier_proof_request.presentation_id)

print(f"Verifier presentation: {verifier_proof_request.presentation_id}")
print(f"Holder presentation:   {holder_proof_request.presentation_id}\n")
while(verifier_proof_request.status != "PresentationVerified"):
    verifier_proof_request: Response[PresentationStatus] = get_presentation.sync(client=verifier_client, presentation_id=verifier_proof_request.presentation_id)
    holder_proof_request: Response[PresentationStatus] = get_presentation.sync(client=holder_client, presentation_id=holder_proof_request.presentation_id)
    print("Verifier State: {} / Holder State: {}".format(verifier_proof_request.status,holder_proof_request.status))
    time.sleep(1)
    
print_proof_request(verifier_proof_request)
```

    Please wait...
    Verifier presentation: 2411274e-bac6-42bd-8cad-b764a62bbf98
    Holder presentation:   f6b2c0e5-12c1-49fb-941a-4433fc1c33da
    
    Verifier State: RequestPending / Holder State: PresentationPending
    Verifier State: RequestSent / Holder State: PresentationPending
    Verifier State: RequestSent / Holder State: PresentationGenerated
    Verifier State: RequestSent / Holder State: PresentationGenerated
    Verifier State: PresentationReceived / Holder State: PresentationGenerated
    Verifier State: PresentationVerified / Holder State: PresentationGenerated
    presentation_id: 2411274e-bac6-42bd-8cad-b764a62bbf98
    status:          PresentationVerified
    connection_id:   8c7b94c3-0baf-4b46-956e-f7d4af2b73f4


### Verifier - Check the presentation

The website https://jwt.io/ can be used to decode the verifiable presentation.


```python
verifier_proof_request.data[0]
```




    'eyJhbGciOiJFUzI1NksifQ.eyJpc3MiOiJkaWQ6cHJpc206YWVmMzkwOTY4OTE1NWI4NDBjMGZmNTRiZmQ3NjViZGRjZGEzMDM0ZjBhNTg3MGUxZDk0ZTYxMGQ4YTJmZDA2MzpDclFCQ3JFQkVqZ0tCR3RsZVRFUUJFb3VDZ2x6WldOd01qVTJhekVTSVFMQ2R1NklTLVVacGlQbm5ETGlOY1ZmajhjdnJncFE2Vl9ZUXE4MnAtNUgxUkk0Q2dSclpYa3lFQUpLTGdvSmMyVmpjREkxTm1zeEVpRUM1X2x2NEp5eVp2bnVlWlF4aTI5UlZZenhmbU4yVlRPamxQZ2l5Q21HR2hnU093b0hiV0Z6ZEdWeU1CQUJTaTRLQ1hObFkzQXlOVFpyTVJJaEFuMkw3NXhyd1YtdGR4SElXNUl6bGl1NkswSnFsOGhxeFZEdXduRUVFSUZDIiwiYXVkIjoiaHR0cHM6XC9cL2V4YW1wbGUtdmVyaWZpZXIuY29tIiwidnAiOnsidHlwZSI6WyJWZXJpZmlhYmxlUHJlc2VudGF0aW9uIl0sIkBjb250ZXh0IjpbImh0dHBzOlwvXC93d3cudzMub3JnXC8yMDE4XC9wcmVzZW50YXRpb25zXC92MSJdLCJ2ZXJpZmlhYmxlQ3JlZGVudGlhbCI6WyJleUpoYkdjaU9pSkZVekkxTmtzaWZRLmV5SnBjM01pT2lKa2FXUTZjSEpwYzIwNk9ERTBObU14TkRkbE5tTTVabVpsTkdSaE4yTTJaakl6WkRJME1XTTJNRFpsWVRGak56SXpZelkwWkROa09EWTFZMk01TldRME9EZ3dOMk00TkRVM01UcERjbEZDUTNKRlFrVnFaMHRDUjNSc1pWUkZVVUpGYjNWRFoyeDZXbGRPZDAxcVZUSmhla1ZUU1ZGT2QxaHphM1F0YUV4SWVuVkhiMGh4VmsxSVluVldkako1ZG1GVGMxSkhabm96Y3pKRVRuaFhhRGt3VWtrMFEyZFNjbHBZYTNsRlFVcExUR2R2U21NeVZtcGpSRWt4VG0xemVFVnBSVVJvYzJSelFrNDJOVzFsTUdaV01tbFhlbDgzUjNoSE5USkxkMmxSZDJ0NlMwMWFiRU5ZTlU5Q1RtdG5VMDkzYjBoaVYwWjZaRWRXZVUxQ1FVSlRhVFJMUTFoT2JGa3pRWGxPVkZweVRWSkphRUV5ZURkbWJDMXpRbDh6V0V4bVdXRkhZM0Y2UzFwU01HOWxaRXhUWmtvNVZVTnljMVpyUVU5amJ6bFdJaXdpYzNWaUlqb2laR2xrT25CeWFYTnRPbUZsWmpNNU1EazJPRGt4TlRWaU9EUXdZekJtWmpVMFltWmtOelkxWW1Sa1kyUmhNekF6TkdZd1lUVTROekJsTVdRNU5HVTJNVEJrT0dFeVptUXdOak02UTNKUlFrTnlSVUpGYW1kTFFrZDBiR1ZVUlZGQ1JXOTFRMmRzZWxwWFRuZE5hbFV5WVhwRlUwbFJURU5rZFRaSlV5MVZXbkJwVUc1dVJFeHBUbU5XWm1vNFkzWnlaM0JSTmxaZldWRnhPREp3TFRWSU1WSkpORU5uVW5KYVdHdDVSVUZLUzB4bmIwcGpNbFpxWTBSSk1VNXRjM2hGYVVWRE5WOXNkalJLZVhsYWRtNTFaVnBSZUdreU9WSldXWHA0Wm0xT01sWlVUMnBzVUdkcGVVTnRSMGRvWjFOUGQyOUlZbGRHZW1SSFZubE5Ra0ZDVTJrMFMwTllUbXhaTTBGNVRsUmFjazFTU1doQmJqSk1OelY0Y25kV0xYUmtlRWhKVnpWSmVteHBkVFpMTUVweGJEaG9jWGhXUkhWM2JrVkZSVWxHUXlJc0ltNWlaaUk2TVRZNU1qZ3pNVGd6T0N3aVpYaHdJam94TmpreU9ETTFORE00TENKMll5STZleUpqY21Wa1pXNTBhV0ZzVTNWaWFtVmpkQ0k2ZXlKbWFYSnpkRzVoYldVaU9pSktZVzFsY3lJc0ltSnBjblJvWkdGMFpTSTZJakF4WEM4d01Wd3ZNakF3TUNJc0ltbGtJam9pWkdsa09uQnlhWE50T21GbFpqTTVNRGsyT0RreE5UVmlPRFF3WXpCbVpqVTBZbVprTnpZMVltUmtZMlJoTXpBek5HWXdZVFU0TnpCbE1XUTVOR1UyTVRCa09HRXlabVF3TmpNNlEzSlJRa055UlVKRmFtZExRa2QwYkdWVVJWRkNSVzkxUTJkc2VscFhUbmROYWxVeVlYcEZVMGxSVEVOa2RUWkpVeTFWV25CcFVHNXVSRXhwVG1OV1ptbzRZM1p5WjNCUk5sWmZXVkZ4T0RKd0xUVklNVkpKTkVOblVuSmFXR3Q1UlVGS1MweG5iMHBqTWxacVkwUkpNVTV0YzNoRmFVVkROVjlzZGpSS2VYbGFkbTUxWlZwUmVHa3lPVkpXV1hwNFptMU9NbFpVVDJwc1VHZHBlVU50UjBkb1oxTlBkMjlJWWxkR2VtUkhWbmxOUWtGQ1UyazBTME5ZVG14Wk0wRjVUbFJhY2sxU1NXaEJiakpNTnpWNGNuZFdMWFJrZUVoSlZ6VkplbXhwZFRaTE1FcHhiRGhvY1hoV1JIVjNia1ZGUlVsR1F5SXNJbXhoYzNSdVlXMWxJam9pVTIxcGRHZ2lmU3dpZEhsd1pTSTZXeUpXWlhKcFptbGhZbXhsUTNKbFpHVnVkR2xoYkNKZExDSkFZMjl1ZEdWNGRDSTZXeUpvZEhSd2N6cGNMMXd2ZDNkM0xuY3pMbTl5WjF3dk1qQXhPRnd2WTNKbFpHVnVkR2xoYkhOY0wzWXhJbDE5ZlEuZHB2ZWhyblRrMVpaTVFHbVJ4dmRPbGx1azlkR0dtbjhCcWpDNGR2QURuMlhoY2V2SXYwSG9IN2pTZGlMTXpZVTQyQ19sWkVHekJVM0NpVUxWak9PMEEiXX0sIm5vbmNlIjoiMTFjOTE0OTMtMDFiMy00YzRkLWFjMzYtYjMzNmJhYjViZGRmIn0.Ud4UzCDhCMFAmCRqC_Z-3_-ITUU5dO6v_cX--xy4nNTcc6bcDxH-xZqE6wxIqPPL3LTp6M1wcC4xu2WhLrNmJA'



### Decode verifiable presentation

As an alternative to the website https://jwt.io/ below you will find the code to perform the verifiable presentation decoding programmatically:

#### Unverified Decoding


```python
try:
    jwt_vp_decoded_id_token = jwt.decode(verifier_proof_request.data[0], options={"verify_signature": False})
    # print(jwt_decoded_id_token)
    print(json.dumps(jwt_vp_decoded_id_token, indent=2))
except (jwt.ExpiredSignatureError, jwt.InvalidAudienceError) as e:
    print("[ERROR]", e)
```

    {
      "iss": "did:prism:aef3909689155b840c0ff54bfd765bddcda3034f0a5870e1d94e610d8a2fd063:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQLCdu6IS-UZpiPnnDLiNcVfj8cvrgpQ6V_YQq82p-5H1RI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEC5_lv4JyyZvnueZQxi29RVYzxfmN2VTOjlPgiyCmGGhgSOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhAn2L75xrwV-tdxHIW5Izliu6K0Jql8hqxVDuwnEEEIFC",
      "aud": "https://example-verifier.com",
      "vp": {
        "type": [
          "VerifiablePresentation"
        ],
        "@context": [
          "https://www.w3.org/2018/presentations/v1"
        ],
        "verifiableCredential": [
          "eyJhbGciOiJFUzI1NksifQ.eyJpc3MiOiJkaWQ6cHJpc206ODE0NmMxNDdlNmM5ZmZlNGRhN2M2ZjIzZDI0MWM2MDZlYTFjNzIzYzY0ZDNkODY1Y2M5NWQ0ODgwN2M4NDU3MTpDclFCQ3JFQkVqZ0tCR3RsZVRFUUJFb3VDZ2x6WldOd01qVTJhekVTSVFOd1hza3QtaExIenVHb0hxVk1IYnVWdjJ5dmFTc1JHZnozczJETnhXaDkwUkk0Q2dSclpYa3lFQUpLTGdvSmMyVmpjREkxTm1zeEVpRURoc2RzQk42NW1lMGZWMmlXel83R3hHNTJLd2lRd2t6S01abENYNU9CTmtnU093b0hiV0Z6ZEdWeU1CQUJTaTRLQ1hObFkzQXlOVFpyTVJJaEEyeDdmbC1zQl8zWExmWWFHY3F6S1pSMG9lZExTZko5VUNyc1ZrQU9jbzlWIiwic3ViIjoiZGlkOnByaXNtOmFlZjM5MDk2ODkxNTViODQwYzBmZjU0YmZkNzY1YmRkY2RhMzAzNGYwYTU4NzBlMWQ5NGU2MTBkOGEyZmQwNjM6Q3JRQkNyRUJFamdLQkd0bGVURVFCRW91Q2dselpXTndNalUyYXpFU0lRTENkdTZJUy1VWnBpUG5uRExpTmNWZmo4Y3ZyZ3BRNlZfWVFxODJwLTVIMVJJNENnUnJaWGt5RUFKS0xnb0pjMlZqY0RJMU5tc3hFaUVDNV9sdjRKeXladm51ZVpReGkyOVJWWXp4Zm1OMlZUT2psUGdpeUNtR0doZ1NPd29IYldGemRHVnlNQkFCU2k0S0NYTmxZM0F5TlRack1SSWhBbjJMNzV4cndWLXRkeEhJVzVJemxpdTZLMEpxbDhocXhWRHV3bkVFRUlGQyIsIm5iZiI6MTY5MjgzMTgzOCwiZXhwIjoxNjkyODM1NDM4LCJ2YyI6eyJjcmVkZW50aWFsU3ViamVjdCI6eyJmaXJzdG5hbWUiOiJKYW1lcyIsImJpcnRoZGF0ZSI6IjAxXC8wMVwvMjAwMCIsImlkIjoiZGlkOnByaXNtOmFlZjM5MDk2ODkxNTViODQwYzBmZjU0YmZkNzY1YmRkY2RhMzAzNGYwYTU4NzBlMWQ5NGU2MTBkOGEyZmQwNjM6Q3JRQkNyRUJFamdLQkd0bGVURVFCRW91Q2dselpXTndNalUyYXpFU0lRTENkdTZJUy1VWnBpUG5uRExpTmNWZmo4Y3ZyZ3BRNlZfWVFxODJwLTVIMVJJNENnUnJaWGt5RUFKS0xnb0pjMlZqY0RJMU5tc3hFaUVDNV9sdjRKeXladm51ZVpReGkyOVJWWXp4Zm1OMlZUT2psUGdpeUNtR0doZ1NPd29IYldGemRHVnlNQkFCU2k0S0NYTmxZM0F5TlRack1SSWhBbjJMNzV4cndWLXRkeEhJVzVJemxpdTZLMEpxbDhocXhWRHV3bkVFRUlGQyIsImxhc3RuYW1lIjoiU21pdGgifSwidHlwZSI6WyJWZXJpZmlhYmxlQ3JlZGVudGlhbCJdLCJAY29udGV4dCI6WyJodHRwczpcL1wvd3d3LnczLm9yZ1wvMjAxOFwvY3JlZGVudGlhbHNcL3YxIl19fQ.dpvehrnTk1ZZMQGmRxvdOlluk9dGGmn8BqjC4dvADn2XhcevIv0HoH7jSdiLMzYU42C_lZEGzBU3CiULVjOO0A"
        ]
      },
      "nonce": "11c91493-01b3-4c4d-ac36-b336bab5bddf"
    }


### Decode Verifiable Credential 

#### Unverified Decoding


```python
try:
    jwt_vc_decoded_id_token = jwt.decode(jwt_vp_decoded_id_token['vp']['verifiableCredential'][0], options={"verify_signature": False})
    # print(jwt_decoded_id_token)
    print(json.dumps(jwt_vc_decoded_id_token, indent=2))
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


#### Verified Decoding of Verifiable Credential

##### Resolve issuer DID


```python
did = None

while (did is None):
    try:
        did = get_did.sync(client=verifier_client_did_doc, did_ref=jwt_vc_decoded_id_token['iss'])
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
    jwt_decoded_id_token = jwt.decode(jwt_vp_decoded_id_token['vp']['verifiableCredential'][0], key = issuer_pubKey, algorithms=["ES256K"])
    # print(jwt_decoded_id_token)
    print(json.dumps(jwt_decoded_id_token, indent=2))
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
jwt_tampered_id_token = jwt_vp_decoded_id_token['vp']['verifiableCredential'][0] + 'x'

try:
    jwt_tampered_decoded_id_token = jwt.decode(jwt_tampered_id_token, key = issuer_pubKey, algorithms=["ES256K"])
    # print(jwt_decoded_id_token)
    # print(json.dumps(jwt_tampered_decoded_id_token, indent=2))
except (jwt.ExpiredSignatureError, jwt.InvalidAudienceError, jwt.InvalidSignatureError) as e:
    print("[ERROR]", e)
```

    [ERROR] Signature verification failed

