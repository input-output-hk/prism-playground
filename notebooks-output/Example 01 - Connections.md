# Create a connection

Establishing a connection between two peers, the Inviter and Invitee, begins with the Inviter creating an out-of-band (oob) invitation. This invitation contains all the necessary information for the Invitee to connect with the Inviter. Once the invitation is created, it must be handed to the Invitee in some way, such as through email, messaging or QR code. Once the Invitee receives the invitation, they must accept it to proceed with the connection. Finally, with the invitation accepted, the connection is established, allowing the two peers to communicate and share data.

This example presents the steps required to connect an Inviter and an Invitee.


```python
#🚨 Run this code cell to import requirements in the Kernel
import socket
import os
import datetime
import time
import requests
from pprint import pprint
from dotenv import load_dotenv

from prism_agent_client import Client
from prism_agent_client.models import Connection, ConnectionsPage, ConnectionInvitation,CreateConnectionRequest,AcceptConnectionInvitationRequest
from prism_agent_client.api.connections_management import get_connections,get_connection,create_connection,accept_connection_invitation
from prism_agent_client.types import Response
```

### Utilitary functions


```python
def get_invitation_str(connection):
    parts = connection.invitation.invitation_url.split("=")
    return parts[1]

def print_connection(connection):
    print(f"connection_id: {connection.connection_id}")
    print(f"state:         {connection.state}")
    print(f"label:         {connection.label}")
    print(f"my_did:        {connection.my_did}")
    print(f"their_did:     {connection.their_did}")
    print(f"created_at:    {connection.created_at}")
    print(f"OOB Invitation: {get_invitation_str(connection)}")
    
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

To start, we will create two separate clients, one for the inviter and one for the invitee, to establish a connection. The roles of the inviter and invitee may overlap with the traditional holder, prover, issuer, and verifier relationships. In some cases, the inviter may also be an issuer or verifier, while the invitee may have the role of a holder or prover. This flexibility allows for different scenarios and use cases to be supported within the same flow.

⚠️ Remember to update the file variables.env with the URLs and API keys provided to you.



```python
env_file = "../Playground/variables.env" if use_host_docker_internal() else "../Playground/variables-linux.env"
load_dotenv(env_file)

inviterApiKey = os.getenv('ISSUER_APIKEY')
inviterUrl = os.getenv('ISSUER_URL')

inviteeApiKey = os.getenv('HOLDER_APIKEY')
inviteeUrl = os.getenv('HOLDER_URL')

inviter_client = Client(base_url=inviterUrl, headers={"apiKey": inviterApiKey})
invitee_client = Client(base_url=inviteeUrl, headers={"apiKey": inviteeApiKey})

%xmode Minimal

preflight(inviterUrl, inviterApiKey)
preflight(inviteeUrl, inviteeApiKey)

%xmode Verbose
```

    Exception reporting mode: Minimal
    URL ok: http://host.docker.internal:8080/prism-agent
    URL ok: http://host.docker.internal:8090/prism-agent
    Exception reporting mode: Verbose


### Inviter - Create the invitation

The Inviter creates an invitation with a `create_connection` request. The only parameter required is a `label` to identify the connection with a human-readable format. 

The connection state, at the Inviter, will be set to `InvitationGenerated`


```python
conn_request = CreateConnectionRequest()
conn_request.label = f'Connect {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
inviter_connection: Response[Connection] =  create_connection.sync(client=inviter_client,json_body=conn_request)

invitation = get_invitation_str(inviter_connection)
print_connection(inviter_connection)
```

    connection_id: a743702a-13cc-4026-b35e-4ce4a426d636
    state:         InvitationGenerated
    label:         Connect 2023-08-23 22:54:37
    my_did:        <prism_agent_client.types.Unset object at 0x7fa0a81e5510>
    their_did:     <prism_agent_client.types.Unset object at 0x7fa0a81e5510>
    created_at:    2023-08-23 22:54:38.020040+00:00
    OOB Invitation: eyJpZCI6ImE3NDM3MDJhLTEzY2MtNDAyNi1iMzVlLTRjZTRhNDI2ZDYzNiIsInR5cGUiOiJodHRwczovL2RpZGNvbW0ub3JnL291dC1vZi1iYW5kLzIuMC9pbnZpdGF0aW9uIiwiZnJvbSI6ImRpZDpwZWVyOjIuRXo2TFNlS0JFdmdtUnE3UVNFNDN3d2o3RDd2QlV5d1VZU3RRbnpQMU54dXhQb1QxTS5WejZNa3ZpcFpjNUx4TXRtcW1yVUZ3aU1BaERIUmRDdVE3Z1hqTGg3eGFpRDlqNXY3LlNleUowSWpvaVpHMGlMQ0p6SWpvaWFIUjBjRG92TDJodmMzUXVaRzlqYTJWeUxtbHVkR1Z5Ym1Gc09qZ3dPREF2Wkdsa1kyOXRiU0lzSW5JaU9sdGRMQ0poSWpwYkltUnBaR052YlcwdmRqSWlYWDAiLCJib2R5Ijp7ImdvYWxfY29kZSI6ImlvLmF0YWxhcHJpc20uY29ubmVjdCIsImdvYWwiOiJFc3RhYmxpc2ggYSB0cnVzdCBjb25uZWN0aW9uIGJldHdlZW4gdHdvIHBlZXJzIHVzaW5nIHRoZSBwcm90b2NvbCAnaHR0cHM6Ly9hdGFsYXByaXNtLmlvL21lcmN1cnkvY29ubmVjdGlvbnMvMS4wL3JlcXVlc3QnIiwiYWNjZXB0IjpbXX19


### Invitee - Accept the invitation 

When the Inviter creates the invitation, there is no connection on the Invitee side, which is why the invitation is shared out of band. Here we conveniently use a variable to pass the invitation to the Invitee with the `accept_connection_invitation` request.

The PRISM Agent does the process to establish the connection automatically, so it may not be possible to track all the protocol steps. They progress as described below:

**Invitee:** `ConnectionRequestPending` --> `ConnectionRequestSent` --> `ConnectionResponseReceived`

**Inviter:** `InvitationGenerated` --> `ConnectionResponsePending` --> `ConnectionResponseSent`

After the next code block is executed, the connection will be established.

>**Note -** if the while loop gets stuck replace:  
>```while (inviter_connection.state != 'ConnectionResponseSent' or invitee_connection.state != 'ConnectionResponseReceived'):```    
>    with:  
>```while (inviter_connection.state != 'ConnectionResponseSent' or not(invitee_connection.state == 'ConnectionResponseReceived' or invitee_connection.state == 'ConnectionRequestSent')):```  


```python
print("Please wait...")

accept_conn_request = AcceptConnectionInvitationRequest(invitation)
invitee_connection: Response[ConnectionInvitation] =  accept_connection_invitation.sync(client=invitee_client,json_body=accept_conn_request)

while (inviter_connection.state != 'ConnectionResponseSent' or invitee_connection.state != 'ConnectionResponseReceived'):
    inviter_connection: Response[Connection] = get_connection.sync(client=inviter_client,connection_id=inviter_connection.connection_id)
    invitee_connection: Response[Connection] = get_connection.sync(client=invitee_client,connection_id=invitee_connection.connection_id)
    print("Inviter State: {} / Invitee State: {} \n".format(inviter_connection.state,invitee_connection.state))
    time.sleep(1)
    
print("Connection established between Issuer and Holder!")
```

    Please wait...
    Inviter State: InvitationGenerated / Invitee State: ConnectionRequestPending 
    
    Inviter State: ConnectionResponsePending / Invitee State: ConnectionRequestPending 
    
    Inviter State: ConnectionResponsePending / Invitee State: ConnectionRequestPending 
    
    Inviter State: ConnectionResponsePending / Invitee State: ConnectionResponseReceived 
    
    Inviter State: ConnectionResponsePending / Invitee State: ConnectionResponseReceived 
    
    Inviter State: ConnectionResponseSent / Invitee State: ConnectionResponseReceived 
    
    Connection established between Issuer and Holder!


### Inviter - Check connection

The details of the connection on the Inviter side are as presented below:


```python
inviter_connection: Response[Connection] =  get_connection.sync(client=inviter_client,connection_id=inviter_connection.connection_id)
print_connection(inviter_connection)
```

    connection_id: a743702a-13cc-4026-b35e-4ce4a426d636
    state:         ConnectionResponseSent
    label:         Connect 2023-08-23 22:54:37
    my_did:        did:peer:2.Ez6LSeKBEvgmRq7QSE43wwj7D7vBUywUYStQnzP1NxuxPoT1M.Vz6MkvipZc5LxMtmqmrUFwiMAhDHRdCuQ7gXjLh7xaiD9j5v7.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwODAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    their_did:     did:peer:2.Ez6LSbwrTHMTf9aPrsaRk3smrPtgjbwvYC4KTJrdDH8VhJRZ9.Vz6MksBfxPUGDAjapmqqq3LW67rkgsLAQvtemQyor4NoTrgBg.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwOTAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    created_at:    2023-08-23 22:54:38.020040+00:00
    OOB Invitation: eyJpZCI6ImE3NDM3MDJhLTEzY2MtNDAyNi1iMzVlLTRjZTRhNDI2ZDYzNiIsInR5cGUiOiJodHRwczovL2RpZGNvbW0ub3JnL291dC1vZi1iYW5kLzIuMC9pbnZpdGF0aW9uIiwiZnJvbSI6ImRpZDpwZWVyOjIuRXo2TFNlS0JFdmdtUnE3UVNFNDN3d2o3RDd2QlV5d1VZU3RRbnpQMU54dXhQb1QxTS5WejZNa3ZpcFpjNUx4TXRtcW1yVUZ3aU1BaERIUmRDdVE3Z1hqTGg3eGFpRDlqNXY3LlNleUowSWpvaVpHMGlMQ0p6SWpvaWFIUjBjRG92TDJodmMzUXVaRzlqYTJWeUxtbHVkR1Z5Ym1Gc09qZ3dPREF2Wkdsa1kyOXRiU0lzSW5JaU9sdGRMQ0poSWpwYkltUnBaR052YlcwdmRqSWlYWDAiLCJib2R5Ijp7ImdvYWxfY29kZSI6ImlvLmF0YWxhcHJpc20uY29ubmVjdCIsImdvYWwiOiJFc3RhYmxpc2ggYSB0cnVzdCBjb25uZWN0aW9uIGJldHdlZW4gdHdvIHBlZXJzIHVzaW5nIHRoZSBwcm90b2NvbCAnaHR0cHM6Ly9hdGFsYXByaXNtLmlvL21lcmN1cnkvY29ubmVjdGlvbnMvMS4wL3JlcXVlc3QnIiwiYWNjZXB0IjpbXX19


### Invitee - Check connection

The details of the connection on the Invitee side are as presented below:


```python
invitee_connection: Response[Connection] =  get_connection.sync(client=invitee_client,connection_id=invitee_connection.connection_id)
print_connection(invitee_connection)
```

    connection_id: 13960cfd-b3b9-4e9e-a732-b2ee4737b82d
    state:         ConnectionResponseReceived
    label:         <prism_agent_client.types.Unset object at 0x7fa0a81e5510>
    my_did:        did:peer:2.Ez6LSbwrTHMTf9aPrsaRk3smrPtgjbwvYC4KTJrdDH8VhJRZ9.Vz6MksBfxPUGDAjapmqqq3LW67rkgsLAQvtemQyor4NoTrgBg.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwOTAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    their_did:     did:peer:2.Ez6LSeKBEvgmRq7QSE43wwj7D7vBUywUYStQnzP1NxuxPoT1M.Vz6MkvipZc5LxMtmqmrUFwiMAhDHRdCuQ7gXjLh7xaiD9j5v7.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwODAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0
    created_at:    2023-08-23 22:54:41.585223+00:00
    OOB Invitation: eyJpZCI6ImE3NDM3MDJhLTEzY2MtNDAyNi1iMzVlLTRjZTRhNDI2ZDYzNiIsInR5cGUiOiJodHRwczovL2RpZGNvbW0ub3JnL291dC1vZi1iYW5kLzIuMC9pbnZpdGF0aW9uIiwiZnJvbSI6ImRpZDpwZWVyOjIuRXo2TFNlS0JFdmdtUnE3UVNFNDN3d2o3RDd2QlV5d1VZU3RRbnpQMU54dXhQb1QxTS5WejZNa3ZpcFpjNUx4TXRtcW1yVUZ3aU1BaERIUmRDdVE3Z1hqTGg3eGFpRDlqNXY3LlNleUowSWpvaVpHMGlMQ0p6SWpvaWFIUjBjRG92TDJodmMzUXVaRzlqYTJWeUxtbHVkR1Z5Ym1Gc09qZ3dPREF2Wkdsa1kyOXRiU0lzSW5JaU9sdGRMQ0poSWpwYkltUnBaR052YlcwdmRqSWlYWDAiLCJib2R5Ijp7ImdvYWxfY29kZSI6ImlvLmF0YWxhcHJpc20uY29ubmVjdCIsImdvYWwiOiJFc3RhYmxpc2ggYSB0cnVzdCBjb25uZWN0aW9uIGJldHdlZW4gdHdvIHBlZXJzIHVzaW5nIHRoZSBwcm90b2NvbCAnaHR0cHM6Ly9hdGFsYXByaXNtLmlvL21lcmN1cnkvY29ubmVjdGlvbnMvMS4wL3JlcXVlc3QnIiwiYWNjZXB0IjpbXX19


### List all connections

The request `get_connections` retrieves the lists of connections. (only printing the first 3)


```python
inviter_connections: Response[ConnectionsPage] = get_connections.sync(client=inviter_client)
invitee_connections: Response[ConnectionsPage] = get_connections.sync(client=invitee_client)

print("Inviter connections")
print("-------------------\n")
pprint(f"{inviter_connections.contents[0:3]}")
print("\nInvitee connections")
print("-------------------\n")
pprint(f"{invitee_connections.contents[0:3]}")
```

    Inviter connections
    -------------------
    
    ("[Connection(connection_id='a743702a-13cc-4026-b35e-4ce4a426d636', "
     "thid='a743702a-13cc-4026-b35e-4ce4a426d636', role=<ConnectionRole.INVITER: "
     "'Inviter'>, state=<ConnectionState.CONNECTIONRESPONSESENT: "
     "'ConnectionResponseSent'>, "
     "invitation=ConnectionInvitation(id='a743702a-13cc-4026-b35e-4ce4a426d636', "
     "type='https://didcomm.org/out-of-band/2.0/invitation', "
     "from_='did:peer:2.Ez6LSeKBEvgmRq7QSE43wwj7D7vBUywUYStQnzP1NxuxPoT1M.Vz6MkvipZc5LxMtmqmrUFwiMAhDHRdCuQ7gXjLh7xaiD9j5v7.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwODAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0', "
     "invitation_url='https://my.domain.com/path?_oob=eyJpZCI6ImE3NDM3MDJhLTEzY2MtNDAyNi1iMzVlLTRjZTRhNDI2ZDYzNiIsInR5cGUiOiJodHRwczovL2RpZGNvbW0ub3JnL291dC1vZi1iYW5kLzIuMC9pbnZpdGF0aW9uIiwiZnJvbSI6ImRpZDpwZWVyOjIuRXo2TFNlS0JFdmdtUnE3UVNFNDN3d2o3RDd2QlV5d1VZU3RRbnpQMU54dXhQb1QxTS5WejZNa3ZpcFpjNUx4TXRtcW1yVUZ3aU1BaERIUmRDdVE3Z1hqTGg3eGFpRDlqNXY3LlNleUowSWpvaVpHMGlMQ0p6SWpvaWFIUjBjRG92TDJodmMzUXVaRzlqYTJWeUxtbHVkR1Z5Ym1Gc09qZ3dPREF2Wkdsa1kyOXRiU0lzSW5JaU9sdGRMQ0poSWpwYkltUnBaR052YlcwdmRqSWlYWDAiLCJib2R5Ijp7ImdvYWxfY29kZSI6ImlvLmF0YWxhcHJpc20uY29ubmVjdCIsImdvYWwiOiJFc3RhYmxpc2ggYSB0cnVzdCBjb25uZWN0aW9uIGJldHdlZW4gdHdvIHBlZXJzIHVzaW5nIHRoZSBwcm90b2NvbCAnaHR0cHM6Ly9hdGFsYXByaXNtLmlvL21lcmN1cnkvY29ubmVjdGlvbnMvMS4wL3JlcXVlc3QnIiwiYWNjZXB0IjpbXX19', "
     'additional_properties={}), created_at=datetime.datetime(2023, 8, 23, 22, 54, '
     "38, 20040, tzinfo=tzutc()), self_='a743702a-13cc-4026-b35e-4ce4a426d636', "
     "kind='Connection', label='Connect 2023-08-23 22:54:37', "
     "my_did='did:peer:2.Ez6LSeKBEvgmRq7QSE43wwj7D7vBUywUYStQnzP1NxuxPoT1M.Vz6MkvipZc5LxMtmqmrUFwiMAhDHRdCuQ7gXjLh7xaiD9j5v7.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwODAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0', "
     "their_did='did:peer:2.Ez6LSbwrTHMTf9aPrsaRk3smrPtgjbwvYC4KTJrdDH8VhJRZ9.Vz6MksBfxPUGDAjapmqqq3LW67rkgsLAQvtemQyor4NoTrgBg.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwOTAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0', "
     'updated_at=datetime.datetime(2023, 8, 23, 22, 54, 46, 478275, '
     'tzinfo=tzutc()), additional_properties={})]')
    
    Invitee connections
    -------------------
    
    ("[Connection(connection_id='13960cfd-b3b9-4e9e-a732-b2ee4737b82d', "
     "thid='a743702a-13cc-4026-b35e-4ce4a426d636', role=<ConnectionRole.INVITEE: "
     "'Invitee'>, state=<ConnectionState.CONNECTIONRESPONSERECEIVED: "
     "'ConnectionResponseReceived'>, "
     "invitation=ConnectionInvitation(id='a743702a-13cc-4026-b35e-4ce4a426d636', "
     "type='https://didcomm.org/out-of-band/2.0/invitation', "
     "from_='did:peer:2.Ez6LSeKBEvgmRq7QSE43wwj7D7vBUywUYStQnzP1NxuxPoT1M.Vz6MkvipZc5LxMtmqmrUFwiMAhDHRdCuQ7gXjLh7xaiD9j5v7.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwODAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0', "
     "invitation_url='https://my.domain.com/path?_oob=eyJpZCI6ImE3NDM3MDJhLTEzY2MtNDAyNi1iMzVlLTRjZTRhNDI2ZDYzNiIsInR5cGUiOiJodHRwczovL2RpZGNvbW0ub3JnL291dC1vZi1iYW5kLzIuMC9pbnZpdGF0aW9uIiwiZnJvbSI6ImRpZDpwZWVyOjIuRXo2TFNlS0JFdmdtUnE3UVNFNDN3d2o3RDd2QlV5d1VZU3RRbnpQMU54dXhQb1QxTS5WejZNa3ZpcFpjNUx4TXRtcW1yVUZ3aU1BaERIUmRDdVE3Z1hqTGg3eGFpRDlqNXY3LlNleUowSWpvaVpHMGlMQ0p6SWpvaWFIUjBjRG92TDJodmMzUXVaRzlqYTJWeUxtbHVkR1Z5Ym1Gc09qZ3dPREF2Wkdsa1kyOXRiU0lzSW5JaU9sdGRMQ0poSWpwYkltUnBaR052YlcwdmRqSWlYWDAiLCJib2R5Ijp7ImdvYWxfY29kZSI6ImlvLmF0YWxhcHJpc20uY29ubmVjdCIsImdvYWwiOiJFc3RhYmxpc2ggYSB0cnVzdCBjb25uZWN0aW9uIGJldHdlZW4gdHdvIHBlZXJzIHVzaW5nIHRoZSBwcm90b2NvbCAnaHR0cHM6Ly9hdGFsYXByaXNtLmlvL21lcmN1cnkvY29ubmVjdGlvbnMvMS4wL3JlcXVlc3QnIiwiYWNjZXB0IjpbXX19', "
     'additional_properties={}), created_at=datetime.datetime(2023, 8, 23, 22, 54, '
     "41, 585223, tzinfo=tzutc()), self_='13960cfd-b3b9-4e9e-a732-b2ee4737b82d', "
     "kind='Connection', label=<prism_agent_client.types.Unset object at "
     '0x7fa0a81e5510>, '
     "my_did='did:peer:2.Ez6LSbwrTHMTf9aPrsaRk3smrPtgjbwvYC4KTJrdDH8VhJRZ9.Vz6MksBfxPUGDAjapmqqq3LW67rkgsLAQvtemQyor4NoTrgBg.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwOTAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0', "
     "their_did='did:peer:2.Ez6LSeKBEvgmRq7QSE43wwj7D7vBUywUYStQnzP1NxuxPoT1M.Vz6MkvipZc5LxMtmqmrUFwiMAhDHRdCuQ7gXjLh7xaiD9j5v7.SeyJ0IjoiZG0iLCJzIjoiaHR0cDovL2hvc3QuZG9ja2VyLmludGVybmFsOjgwODAvZGlkY29tbSIsInIiOltdLCJhIjpbImRpZGNvbW0vdjIiXX0', "
     'updated_at=datetime.datetime(2023, 8, 23, 22, 54, 44, 445279, '
     'tzinfo=tzutc()), additional_properties={})]')



```python

```
