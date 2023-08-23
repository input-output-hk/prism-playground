## Schema Registry

The schema registry allows the creation and retrieval of schemas. Deleting schemas is not possible. Updates can be done by by creating a modified copy of the schema with an updated version


```python
import socket
import os
import time
import datetime
import base64
import uuid
import requests
import re
from pprint import pprint
from dotenv import load_dotenv
from typing import Any, Dict, Optional, Union, cast

from prism_agent_client import Client
from prism_agent_client.models import CredentialSchemaResponse
from prism_agent_client.models import CredentialSchemaInput
from prism_agent_client.models import ErrorResponse
from prism_agent_client.models import CreateManagedDidRequest, CreateManagedDIDResponse
from prism_agent_client.types import Response
from prism_agent_client.api.schema_registry import create_schema, get_schema_by_id, lookup_schemas_by_query
from prism_agent_client.api.did_registrar import post_did_registrar_dids
```

### Utilitary Functions


```python
def print_schema(schema):
    if hasattr(schema, "id"):
        print("id:", schema.id)
    print("name:", schema.name)
    print("version:", schema.version)
    print("author:", schema.author)
    print("authored:", schema.authored)
    print("tags:", schema.tags)
    print("description:", schema.description)
    
def print_schema_page(schema_page):
    for schema in schema_page.contents:
        print_schema(schema)
        print()

def to_canonical_did(long_form):
    pattern = r"did:prism:[a-fA-F0-9]{64}"
    match = re.search(pattern, long_form)
    
    if match:
        return match.group()
    else:
        return None
        
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

note: remember to update the file variables.env with the URLs and API keys provided to you.



```python
env_file = "../Playground/variables.env" if use_host_docker_internal() else "../Playground/variables-linux.env"
load_dotenv(env_file)

issuerApiKey = os.getenv('ISSUER_APIKEY')
issuerUrl = os.getenv('ISSUER_URL')

issuer_client = Client(base_url=issuerUrl, headers={"apiKey": issuerApiKey})

%xmode Minimal

preflight(issuerUrl, issuerApiKey)

%xmode Verbose
```

    Exception reporting mode: Minimal
    URL ok: http://host.docker.internal:8080/prism-agent
    Exception reporting mode: Verbose


### Create the Author

Create a DID to be used as a Schema author. It doesn't need to be a new DID but we will use a new one to keep the example self contianed.


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
did_author = to_canonical_did(post_did_registrar_dids.sync(client=issuer_client, json_body=did_request).long_form_did)

print(did_author)
```

    did:prism:be1035c1ee5374824986c3d66df64b30ee80eb6056871e458b8b332145903983


### Create Schema

Publish the new schema with attributes to the schema registry on behalf of Cloud Agent. Schema will be signed by the keys of Cloud Agent and issued by the DID that corresponds to it


```python

data = {
    "name": f"Driving License {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "version": f"1.0.0+{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}",
    "description": "Simple credential schema for the driving licence verifiable credential. This field is not a part of W3C specification",
    "type": "https://w3c-ccg.github.io/vc-json-schemas/schema/2.0/schema.json",
    "author": did_author,
    "schema": {
        "$id": "https://example.com/driving-license-1.0.0",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "description": "Driving License",
        "type": "object",
        "properties": {
            "credentialSubject": {
                "type": "object",
                "properties": {
                    "emailAddress": {
                        "type": "string",
                        "format": "email"
                    },
                    "givenName": {
                        "type": "string"
                    },
                    "familyName": {
                        "type": "string"
                    },
                    "dateOfIssuance": {
                        "type": "datetime"
                    },
                    "drivingLicenseID": {
                        "type": "string"
                    },
                    "drivingClass": {
                        "type": "integer"
                    },
                    "required": [
                        "emailAddress",
                        "familyName",
                        "dateOfIssuance",
                        "drivingLicenseID",
                        "drivingClass"
                    ],
                    "additionalProperties": True
                }
            }
        }
    },
    "tags": [
        "driving",
        "licence",
        "id"
    ]
}

credential_schema_input = CredentialSchemaInput.from_dict(data)
credential_schema: Response[Union[CredentialSchemaResponse, ErrorResponse]] = create_schema.sync(client=issuer_client, json_body=credential_schema_input)
print(credential_schema)
print_schema(credential_schema)
```

    CredentialSchemaResponse(guid='ae923355-b20a-3354-8fe5-14009901c44d', id='d8a7d661-51a4-457c-9067-cb2d80b2962e', name='Driving License 2023-08-23 23:14:22', version='1.0.0+2023-08-23-23-14-22', description='Simple credential schema for the driving licence verifiable credential. This field is not a part of W3C specification', type='https://w3c-ccg.github.io/vc-json-schemas/schema/2.0/schema.json', schema={'$id': 'https://example.com/driving-license-1.0.0', '$schema': 'https://json-schema.org/draft/2020-12/schema', 'description': 'Driving License', 'type': 'object', 'properties': {'credentialSubject': {'type': 'object', 'properties': {'emailAddress': {'type': 'string', 'format': 'email'}, 'givenName': {'type': 'string'}, 'familyName': {'type': 'string'}, 'dateOfIssuance': {'type': 'datetime'}, 'drivingLicenseID': {'type': 'string'}, 'drivingClass': {'type': 'integer'}, 'required': ['emailAddress', 'familyName', 'dateOfIssuance', 'drivingLicenseID', 'drivingClass'], 'additionalProperties': True}}}}, author='did:prism:be1035c1ee5374824986c3d66df64b30ee80eb6056871e458b8b332145903983', authored=datetime.datetime(2023, 8, 23, 23, 14, 22, 163441, tzinfo=tzutc()), kind='CredentialSchema', self_='/schema-registry/schemas/ae923355-b20a-3354-8fe5-14009901c44d', long_id='did:prism:be1035c1ee5374824986c3d66df64b30ee80eb6056871e458b8b332145903983/d8a7d661-51a4-457c-9067-cb2d80b2962e?version=1.0.0+2023-08-23-23-14-22', tags=['driving', 'licence', 'id'], proof=<prism_agent_client.types.Unset object at 0x7fd8c4268e50>, additional_properties={})
    id: d8a7d661-51a4-457c-9067-cb2d80b2962e
    name: Driving License 2023-08-23 23:14:22
    version: 1.0.0+2023-08-23-23-14-22
    author: did:prism:be1035c1ee5374824986c3d66df64b30ee80eb6056871e458b8b332145903983
    authored: 2023-08-23 23:14:22.163441+00:00
    tags: ['driving', 'licence', 'id']
    description: Simple credential schema for the driving licence verifiable credential. This field is not a part of W3C specification


### Lookup

Lookup schemas by `author`, `name`, `tags` parameters and control the pagination by `offset` and `limit` parameters


```python
schema_page = lookup_schemas_by_query.sync(client=issuer_client, tags=["driving"], limit=1)
print_schema_page(schema_page)
```

    id: d8a7d661-51a4-457c-9067-cb2d80b2962e
    name: Driving License 2023-08-23 23:14:22
    version: 1.0.0+2023-08-23-23-14-22
    author: did:prism:be1035c1ee5374824986c3d66df64b30ee80eb6056871e458b8b332145903983
    authored: 2023-08-23 23:14:22.163441+00:00
    tags: ['driving', 'licence', 'id']
    description: Simple credential schema for the driving licence verifiable credential. This field is not a part of W3C specification
    


### Fetch
Fetch the schema by the unique identifier. Verifiable Credential Schema in json format is returned.


```python
credential_schema = get_schema_by_id.sync(client=issuer_client, guid=credential_schema.guid)
print_schema(credential_schema)
```

    id: d8a7d661-51a4-457c-9067-cb2d80b2962e
    name: Driving License 2023-08-23 23:14:22
    version: 1.0.0+2023-08-23-23-14-22
    author: did:prism:be1035c1ee5374824986c3d66df64b30ee80eb6056871e458b8b332145903983
    authored: 2023-08-23 23:14:22.163441+00:00
    tags: ['driving', 'licence', 'id']
    description: Simple credential schema for the driving licence verifiable credential. This field is not a part of W3C specification

