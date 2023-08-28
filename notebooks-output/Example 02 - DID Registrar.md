## DID Registrar

The DID Registrar contains endpoints to create and manage PRISM DIDs. In this scenatio the keys are managed by PRISM Agent.


```python
#🚨 Run this code cell to import requirements in the Kernel
import socket
import os
import time
import datetime
import base64
import uuid
import requests
from pprint import pprint
from dotenv import load_dotenv
from typing import Any, Dict, Optional, Union, cast

from prism_agent_client import Client
from prism_agent_client.models import ErrorResponse
from prism_agent_client.types import Response, Unset
from prism_agent_client.models import CreateManagedDidRequestDocumentTemplate, CreateManagedDidRequest, CreateManagedDIDResponse

from prism_agent_client.models import UpdateManagedDIDRequest
from prism_agent_client.models import DIDDocumentMetadata, DIDOperationResponse, DidOperationSubmission, DIDDocument, Service, DIDResolutionResult  
from prism_agent_client.api.did_registrar import get_did_registrar_dids, get_did_registrar_dids_didref, post_did_registrar_dids, post_did_registrar_dids_didref_publications, post_did_registrar_dids_didref_updates, post_did_registrar_dids_didref_deactivations
from prism_agent_client.api.did import get_did
```

### Utilitary functions


```python
def print_did_operation_response(did_operation_response):
    if hasattr(did_operation_response, "scheduled_operation"):
        scheduled_operation = did_operation_response.scheduled_operation
        if hasattr(scheduled_operation, "id"):
            print("Scheduled operation ID:", scheduled_operation.id)
        if hasattr(scheduled_operation, "did_ref"):
            print("Scheduled operation DID reference:", scheduled_operation.did_ref)
        if hasattr(scheduled_operation, "additional_properties"):
            print("Scheduled operation additional properties:", scheduled_operation.additional_properties)
    if hasattr(did_operation_response, "additional_properties"):
        print("DID operation response additional properties:", did_operation_response.additional_properties)

def print_list_managed_did_response_inner(list_managed_did_response_inner):
    if hasattr(list_managed_did_response_inner, "did"):
        print("DID:", list_managed_did_response_inner.did)
    if hasattr(list_managed_did_response_inner, "status"):
        print("Status:", list_managed_did_response_inner.status)
    if hasattr(list_managed_did_response_inner, "long_form_did"):
        print("Long form DID:", list_managed_did_response_inner.long_form_did)
    if hasattr(list_managed_did_response_inner, "additional_properties"):
        print("Additional properties:", list_managed_did_response_inner.additional_properties)

def print_did_list(list_managed_did_response_inner_list):
    for list in list_managed_did_response_inner_list:
        print_list_managed_did_response_inner(list)
        print()
        
def print_did_operation_response(did_operation_response):
    if hasattr(did_operation_response, "scheduled_operation"):
        print("Scheduled Operation:")
        print("  ID:", did_operation_response.scheduled_operation.id)
        print("  DID Reference:", did_operation_response.scheduled_operation.did_ref)
        if hasattr(did_operation_response.scheduled_operation, "additional_properties"):
            print("  Additional Properties:", did_operation_response.scheduled_operation.additional_properties)
    if hasattr(did_operation_response, "additional_properties"):
        print("Additional Properties:", did_operation_response.additional_properties)
        
        
def print_did_response(did_response):
    #did = did_response.did
    print("DID ID: ", did.id)
    print("Controller: ", did.controller)
    print("Verification Methods: ")
    for ver_method in did.verification_method:
        print("\tID: ", ver_method.id)
        print("\tType: ", ver_method.type)
        print("\tController: ", ver_method.controller)
        print("\tPublic Key JWK: ", ver_method.public_key_jwk)
    print("Authentication: ")
    for auth in did.authentication:
        print("\t", auth)
    print("Assertion Method: ")
    for assert_method in did.assertion_method:
        print("\t", assert_method)
    print("Key Agreement: ")
    for key_agreement in did.key_agreement:
        print("\tType: ", key_agreement.type)
        print("\tURI: ", key_agreement.uri)
    print("Capability Invocation: ")
    for capability_invocation in did.capability_invocation:
        print("\t", capability_invocation)
    print("Capability Delegation: ")
    for capability_delegation in did.capability_delegation:
        print("\t", capability_delegation)
    print("Services: ")
    for service in did.service:
        print("\tID: ", service.id)
        print("\tType: ", service.type)
        print("\tService Endpoint: ", service.service_endpoint)

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

For this example we only need one Client.

⚠️ Remember to update the file variables.env with the URLs and API keys provided to you.



```python
env_file = "../Playground/variables.env" if use_host_docker_internal() else "../Playground/variables-linux.env"
load_dotenv(env_file)

issuerApiKey = os.getenv('ISSUER_APIKEY')
issuerUrl = os.getenv('ISSUER_URL')

issuer_client         = Client(base_url=issuerUrl, headers={"apiKey": issuerApiKey})
issuer_client_did_doc = Client(base_url=issuerUrl, headers={"apiKey": issuerApiKey, "accept":"application/did+ld+json"})

%xmode Minimal

preflight(issuerUrl, issuerApiKey)

%xmode Verbose
```

    Exception reporting mode: Minimal
    URL ok: http://host.docker.internal:8080/prism-agent
    Exception reporting mode: Verbose


### Create unpublished DID

The following code uses `create_managed_did` to create and store an unpublished DID inside PRISM Agent's DB. In this scenario, the PRISM Agent manages the keys of the DID. Once the DID is created, it can be published to the VDR using the publications endpoint.

The possible values for key purposes are: `authentication`, `assertionMethod`, `keyAgreement`, `capabilityInvocation`, `capabilityDelegation`

For services type, the only value allowed is: `LinkedDomains` 


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
    ],
    "services": [ ]
  }
}

did_request = CreateManagedDidRequest.from_dict(data)
did: Response[CreateManagedDIDResponse] = post_did_registrar_dids.sync(client=issuer_client, json_body=did_request)

print(did.long_form_did)
```

    did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207:CrQBCrEBEjgKBGtleTEQBEouCglzZWNwMjU2azESIQNKpn2HqKQE8Du1xcWPbt5sFxqayDWUUzXKn6t_YmUiMhI4CgRrZXkyEAJKLgoJc2VjcDI1NmsxEiEDHnudsg4K9eIVmqlwoKIvV6mbmevTplkGVQye7WOtt68SOwoHbWFzdGVyMBABSi4KCXNlY3AyNTZrMRIhA7V1ba1nuHVxbmtdQJckF-b1OatDnlvZzXEBXDdN4sjl


### Publish DID 
The request `publish_managed_did` is used to Publish the DID into the VDR. It requires the DID identifier as input.


```python

operation_response : (DIDOperationResponse) = post_did_registrar_dids_didref_publications.sync(client=issuer_client, did_ref=did.long_form_did)
print_did_operation_response(operation_response)
```

    Scheduled Operation:
      ID: 26d270a2088ce01c58b54b4982a3d0f0573f10af3af425ebccc36652503b9ef2
      DID Reference: did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
      Additional Properties: {}
    Additional Properties: {}


### DID Resolver

To resolve a PRISM DID the request `get_did` is available. It requires the DID identifier as a parameter. 

It takes some time for the DID to be published, so we use a delay loop to wait until the publication is completed.


```python
print("Please wait...")
did = None

while (did is None):
    try:
        did = get_did.sync(client=issuer_client_did_doc, did_ref=operation_response.scheduled_operation.did_ref)
    except Exception as e:
        print("Please wait...")
        time.sleep(10)

print(did)
print_did_response(did)
```

    Please wait...
    Please wait...
    DIDDocument(id='did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207', context=['https://www.w3.org/ns/did/v1', 'https://w3id.org/security/suites/jws-2020/v1'], controller='did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207', verification_method=[VerificationMethod(id='did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key1', type='JsonWebKey2020', controller='did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207', public_key_jwk=PublicKeyJwk(kty='EC', crv='secp256k1', x='SqZ9h6ikBPA7tcXFj27ebBcamsg1lFM1yp-rf2JlIjI', y='t69gqUbbGpXJH1263V21JgrWrOJMN-qOwO3mDFvECUk', additional_properties={}), additional_properties={}), VerificationMethod(id='did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key2', type='JsonWebKey2020', controller='did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207', public_key_jwk=PublicKeyJwk(kty='EC', crv='secp256k1', x='Hnudsg4K9eIVmqlwoKIvV6mbmevTplkGVQye7WOtt68', y='mT-bm1SMdFljRFkq26UKGbgujo5LHrLCbkBv1_G7FhM', additional_properties={}), additional_properties={})], authentication=['did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key1'], assertion_method=['did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key2'], key_agreement=[], capability_invocation=[], capability_delegation=[], service=[], additional_properties={})
    DID ID:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
    Controller:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
    Verification Methods: 
    	ID:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key1
    	Type:  JsonWebKey2020
    	Controller:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
    	Public Key JWK:  PublicKeyJwk(kty='EC', crv='secp256k1', x='SqZ9h6ikBPA7tcXFj27ebBcamsg1lFM1yp-rf2JlIjI', y='t69gqUbbGpXJH1263V21JgrWrOJMN-qOwO3mDFvECUk', additional_properties={})
    	ID:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key2
    	Type:  JsonWebKey2020
    	Controller:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
    	Public Key JWK:  PublicKeyJwk(kty='EC', crv='secp256k1', x='Hnudsg4K9eIVmqlwoKIvV6mbmevTplkGVQye7WOtt68', y='mT-bm1SMdFljRFkq26UKGbgujo5LHrLCbkBv1_G7FhM', additional_properties={})
    Authentication: 
    	 did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key1
    Assertion Method: 
    	 did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key2
    Key Agreement: 
    Capability Invocation: 
    Capability Delegation: 
    Services: 


### DID Update

To Update a DID, the PRISM Agent provides the `update_managed_did` endpoint. It updates the DID in PRISM Agent's DB and posts the update operation to the VDR. This endpoint updates the DID document from the last confirmed operation. Submitting multiple update operations without waiting for confirmation will result in some operations being rejected, as only one operation can be appended from the last confirmed operation.

The values for `actionType` are `ADD_KEY`, `REMOVE_KEY`, `ADD_SERVICE`, `REMOVE_SERVICE`, `UPDATE_SERVICE`


```python
data = {
    "actions": [
        {
            "actionType": "ADD_KEY",
            "addKey": {
                "id": "key3",
                "purpose": "authentication"
            }
        },
        {
            "actionType": "REMOVE_KEY",
            "removeKey": {
                "id": "key1"
            }
        }
    ]
}

did_update_request = UpdateManagedDIDRequest.from_dict(data)

update_response : [DIDOperationResponse] = post_did_registrar_dids_didref_updates.sync(client=issuer_client, 
                                                                   did_ref=operation_response.scheduled_operation.did_ref, 
                                                                   json_body=did_update_request)

print_did_operation_response(update_response)
```

    Scheduled Operation:
      ID: 0d2418637ec5498a8d9be062e925d551fcf7650f3c8894623245b2afa23aba42
      DID Reference: did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
      Additional Properties: {}
    Additional Properties: {}


**🚨Wait for a few minutes until the DID is updated and run the code below**


```python
did = get_did.sync(client=issuer_client_did_doc, did_ref=operation_response.scheduled_operation.did_ref)
    
print_did_response(did)
```

    DID ID:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
    Controller:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
    Verification Methods: 
    	ID:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key2
    	Type:  JsonWebKey2020
    	Controller:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
    	Public Key JWK:  PublicKeyJwk(kty='EC', crv='secp256k1', x='Hnudsg4K9eIVmqlwoKIvV6mbmevTplkGVQye7WOtt68', y='mT-bm1SMdFljRFkq26UKGbgujo5LHrLCbkBv1_G7FhM', additional_properties={})
    	ID:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key3
    	Type:  JsonWebKey2020
    	Controller:  did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
    	Public Key JWK:  PublicKeyJwk(kty='EC', crv='secp256k1', x='uX8MfM7U6KIkw8wdpppom75e2_E7slPmAmIpokgAyyw', y='sq5rGFJuzElX81jYc99glbrN924qkjPH_wjrAWgVqQM', additional_properties={})
    Authentication: 
    	 did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key3
    Assertion Method: 
    	 did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207#key2
    Key Agreement: 
    Capability Invocation: 
    Capability Delegation: 
    Services: 


### DID Deactivation

To deactivate DID and post deactivate operation to blockchain use `deactivate_managed_did`.


```python
deactivation_response = None
while (deactivation_response is None):
    try: 
        deactivation_response: [DIDOperationResponse] = post_did_registrar_dids_didref_deactivations.sync(client=issuer_client, did_ref=operation_response.scheduled_operation.did_ref)
        print_did_operation_response(deactivation_response) 
    except Exception as e:
        print("Please wait...")
        time.sleep(10)
```

    Scheduled Operation:
      ID: 0549514445df9906590b3f3fb8be5a4c48d3c9cdc5173344e44b33a60214d5a1
      DID Reference: did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
      Additional Properties: {}
    Additional Properties: {}


**🚨Wait for a few minutes until the DID is deactivated. And run the code below**


```python
#did = get_did.sync(client=issuer_client_did_doc, did_ref=operation_response.scheduled_operation.did_ref)
#print_did_response(did)
print("ℹ️ We have identified an issue with the get_did function in this example. Until we fix the problem, run the following curl command in a terminal and check the DID has the attribute `deactivated: true`\n")
print(f"curl --location 'localhost:8080/prism-agent/dids/{operation_response.scheduled_operation.did_ref}' --header 'Accept: application/ld+json; profile=https://w3id.org/did-resolution' --header 'apikey: {issuerApiKey}'")
```

    ℹ️ We have identified an issue with the get_did function in this example. Until we fix the problem, run the following curl command in a terminal and check the DID has the attribute `deactivated: true`
    
    curl --location 'localhost:8080/prism-agent/dids/did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207' --header 'Accept: application/ld+json; profile=https://w3id.org/did-resolution' --header 'apikey: kxr9i@6XgKBUxe%O'


The output will look like this:

```json
{
    "@context":"https://w3id.org/did-resolution/v1",
    "didDocumentMetadata":{
        "deactivated":true,
        "versionId":"3045805fc0a06714a07cae03653f0e4bf30c8cbc637f2a81c5ea08e13c4fc990",
        "created":"2023-08-23T22:56:05Z",
        "updated":"2023-08-23T22:57:05Z"},
    "didResolutionMetadata":{
        "contentType":"application/ld+json; profile=https://w3id.org/did-resolution"
    }
}
```

### List DIDs

To List all DIDs stored in the PRISM Agent DB use `list_managed_did`.


```python
did_list = get_did_registrar_dids.sync(client=issuer_client)
print_did_list(did_list.contents[:3])
```

    DID: did:prism:3a640a5228c4bc3225e539d656ba30d44301bd834a6848f054777a6e62dcd207
    Status: PUBLISHED
    Long form DID: <prism_agent_client.types.Unset object at 0x7fd7901eac10>
    Additional properties: {}
    



```python

```
