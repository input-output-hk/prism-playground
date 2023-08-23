## Verification Policies

Verification policies are rules a verifier sets to specify what information they require from a holder to verify their identity or qualifications. They serve as a way for verifiers to communicate their verification requirements to holders and are used in the Present Proof protocol to construct proof requests.   

The PRISM Agent provides endpoints to create, update, fetch, lookup and delete verification policies. 
  
The policies attributes include:
- A unique ID
- A name
- Credential constraints. Composed by a credential schema identifier and a list of trusted issuers (Decentralized Identifiers)
  


```python
import socket
import os
import time
import datetime
import base64
import requests
from pprint import pprint
from dotenv import load_dotenv

from prism_agent_client import Client
from prism_agent_client.models import VerificationPolicy, VerificationPolicyInput, VerificationPolicyPage
from prism_agent_client.api.verification import create_verification_policy, delete_verification_policy_by_id, get_verification_policy_by_id
from prism_agent_client.api.verification import update_verification_policy, lookup_verification_policies_by_query
from prism_agent_client.types import Response

```

### Ultilitary functions


```python
def print_verification_policy(policy):
    print("id:", policy.id)
    print("name:", policy.name)
    print("created_at:", policy.created_at)
    print("updated_at:", policy.updated_at)
    print("constraints:", policy.constraints)
    
def print_verification_policy_page(verification_policy_page):
    for verification_policy in verification_policy_page.contents:
        print_verification_policy(verification_policy)
        print()
        
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

For this example we only need one client.

note: remember to update the file variables.env with the URLs and API keys provided to you.



```python
env_file = "../Playground/variables.env" if use_host_docker_internal() else "../Playground/variables-linux.env"
load_dotenv(env_file)

verifierApiKey = os.getenv('VERIFIER_APIKEY')
verifierUrl = os.getenv('VERIFIER_URL')

verifier_client = Client(base_url=verifierUrl, headers={"apiKey": verifierApiKey})

%xmode Minimal

preflight(verifierUrl, verifierApiKey)

%xmode Verbose
```

    Exception reporting mode: Minimal
    URL ok: http://host.docker.internal:9000/prism-agent
    Exception reporting mode: Verbose


### Create Verification Policy

We will create two policies, one for driver's licenses and one for education requirements.


```python
data = {
    "name": f"Driver license verificaion {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "description":"Verification Policy Example",
    "constraints": [
        {
            "schemaId": "drivers license",
            "trustedIssuers": [
                "did:prism:1234"
            ]
        }
    ]
}
verification_policy_input = VerificationPolicyInput.from_dict(data)
verification_policy : [VerificationPolicy] = create_verification_policy.sync(client=verifier_client, json_body=verification_policy_input)

print(f"Drivers License: {verification_policy.id}\n")
print_verification_policy(verification_policy)


data_2 = {
    "name": f"Education requirement {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "description":"Verification Policy Example 2",
    "constraints": [
        {
            "schemaId": "School diploma",
            "trustedIssuers": [
                "did:prism:5678", "did:prism:8765"
            ]
        },
        {
            "schemaId": "High School diploma",
            "trustedIssuers": [
                "did:prism:5678", "did:prism:8765"
            ]
        }
    ]
}

verification_policy_input_2 = VerificationPolicyInput.from_dict(data_2)
verification_policy_2 : [VerificationPolicy] = create_verification_policy.sync(client=verifier_client, json_body=verification_policy_input_2)

print(f"\nEducation Requirement: {verification_policy_2.id}\n")
print_verification_policy(verification_policy_2)
```

    Drivers License: e189e75f-4878-4ce8-b719-7703c43e9e79
    
    id: e189e75f-4878-4ce8-b719-7703c43e9e79
    name: Driver license verificaion 2023-08-23 23:14:51
    created_at: 2023-08-23 23:14:51.648170+00:00
    updated_at: 2023-08-23 23:14:51.648170+00:00
    constraints: [VerificationPolicyConstraint(schema_id='drivers license', trusted_issuers=['did:prism:1234'], additional_properties={})]
    
    Education Requirement: 25913a8f-e57a-49da-98cc-38b8f5bb21bc
    
    id: 25913a8f-e57a-49da-98cc-38b8f5bb21bc
    name: Education requirement 2023-08-23 23:14:51
    created_at: 2023-08-23 23:14:51.748950+00:00
    updated_at: 2023-08-23 23:14:51.748950+00:00
    constraints: [VerificationPolicyConstraint(schema_id='School diploma', trusted_issuers=['did:prism:5678', 'did:prism:8765'], additional_properties={}), VerificationPolicyConstraint(schema_id='High School diploma', trusted_issuers=['did:prism:5678', 'did:prism:8765'], additional_properties={})]


### Update Verification Policy

Next, we will update the driver's License verification policy by a trusted issuer.  


```python
data = {
    "name": f"Driver license verificaion {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "description":"Verification Policy Example",
    "constraints": [
        {
            "schemaId": "drivers license",
            "trustedIssuers": [
                "did:prism:1234",
                "did:prism:4321"
            ]
        }
    ]
}
verification_policy_input = VerificationPolicyInput.from_dict(data)
verification_policy : [VerificationPolicy] = update_verification_policy.sync(client=verifier_client, 
                                                                             id=verification_policy.id,
                                                                             nonce=verification_policy.nonce,
                                                                             json_body=verification_policy_input)
print_verification_policy(verification_policy)
```

    id: e189e75f-4878-4ce8-b719-7703c43e9e79
    name: Driver license verificaion 2023-08-23 23:14:51
    created_at: 2023-08-23 23:14:51.648170+00:00
    updated_at: 2023-08-23 23:14:51.790233+00:00
    constraints: [VerificationPolicyConstraint(schema_id='drivers license', trusted_issuers=['did:prism:1234', 'did:prism:4321'], additional_properties={})]


### Fetch

Get the verification policy by id


```python
verification_policy : [VerificationPolicy] = get_verification_policy_by_id.sync(client=verifier_client, id=verification_policy.id)
print_verification_policy(verification_policy)
```

    id: e189e75f-4878-4ce8-b719-7703c43e9e79
    name: Driver license verificaion 2023-08-23 23:14:51
    created_at: 2023-08-23 23:14:51.648170+00:00
    updated_at: 2023-08-23 23:14:51.790233+00:00
    constraints: [VerificationPolicyConstraint(schema_id='drivers license', trusted_issuers=['did:prism:1234', 'did:prism:4321'], additional_properties={})]


### Lookup

The lookup endpoint can be used to get a list of verification policies. The available filter is `name` and to control the pagination `offset` and `limit` parameters are available.        


```python
verification_policy_page : [verification_policy_page] = lookup_verification_policies_by_query.sync(client=verifier_client, 
                                                                                                   name=[verification_policy.name], 
                                                                                                   limit=1)
print_verification_policy_page(verification_policy_page)
```

    id: e189e75f-4878-4ce8-b719-7703c43e9e79
    name: Driver license verificaion 2023-08-23 23:14:51
    created_at: 2023-08-23 23:14:51.648170+00:00
    updated_at: 2023-08-23 23:14:51.790233+00:00
    constraints: [VerificationPolicyConstraint(schema_id='drivers license', trusted_issuers=['did:prism:1234', 'did:prism:4321'], additional_properties={})]
    


🚧 There is known issue with this feature. We are working on it. 🚧

### Delete

Verification policies can be deleted by `id`


```python
#verification_policy : [VerificationPolicy] = get_verification_policy_by_id.sync(client=verifier_client, id=verification_policy.id)
#print("Get by id before deletion:\n")
#print_verification_policy(verification_policy)

#delete_verification_policy_by_id.sync(client=verifier_client,nonce=verification_policy.nonce, id=verification_policy.id)
#response = get_verification_policy_by_id.sync(client=verifier_client, id=verification_policy.id)

#print(f"\nGet by id after deletion: {response.msg}")
```
