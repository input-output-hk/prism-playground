# Prism V2 Playground  

This repo contains a Jupyter Notebook that runs from a docker container.  
It's an easy way to interact with the PRISM Agent APIs via python jupyter-notebook.  
It also includes scripts to run local Prism Agents. The default script will start/stop three Prism Agents for the various actors (`issuer`,`holder`, `verifier`) used as part the Prism Playground.  

## Prerequisites 
Install and start [Docker Desktop](https://www.docker.com/products/docker-desktop/) and `docker-compose` in your local machine and ensure you have an active internet connection.  
To start the Prism Playground you can use the commands below to start and stop the Jupyter Notebook server and Prism Agents.

## Quick Start Guide
### 1. Run Prism Playground and Local Prism Agents
```bash
cd <path>/prism_v2_playground

# Copy sample.env to .env
cp sample.env .env

# Set your Github PAT in the `.env` file
> NOTE: Your Github PAT should have `read-packages` access
ATALA_PRISM_SECRET_READ_ACCESS_TOKEN=<your Github PAT>

# Load env file variables
source .env
 
# Login to ghcr
echo $ATALA_PRISM_SECRET_READ_ACCESS_TOKEN | docker login ghcr.io -u atala-dev --password-stdin

# Starting the Jupyter Notebook Server (Prism Playground)
docker compose up --build -d

# Starting the local Prism Agents.
./run_agents.sh
```
### 2a. Access the Prism Playground Jupyter Notebooks
The default password is `Prismv2`    
This is the default location to access the Prism Playground notebooks:

```bash
http://127.0.0.1:8888/
```

### 2b. Access the Prism Agent Swagger API
This is the default location to access the Prism Agent Swagger API:
> NOTE: You need to pass in the `apikey` header with the value `kxr9i@6XgKBUxe%O`

[Issuer Agent Swagger Interface](http://localhost:8080/apidocs/)  
[Holder Agent Swagger Interface](http://localhost:8090/apidocs/)  
[Verifier Agent Swagger Interface](http://localhost:9000/apidocs/)  

ℹ️ If you are running Ubuntu (or Linux) operating system and have a firewall enabled ensure that you allow communication between the docker instances.
Here is an example of adding a firewall rule with `ufw`:
```bash
sudo ufw allow to 172.17.0.1
```

### 3. Stop Prism Playground and Local Prism Agents
```bash
cd <path>/prism_v2_playground

# Stopping the Jupyter Notebook Server (Prism Playground)
docker-compose down

# Stopping the local Prism Agents.
./stop_agents.sh
```

## ℹ️ Customise Running Prism Agent Locally
Detailed information on how to run Prism Agent and Prism Node locally can be found [here](agent/README.md).

## ℹ️ Generating Prism Agent Open API Clients
Detailed information on how to generate Open API clients for Prism Agents in various programming languages can be found [here](openapi-generator/README.md).
> NOTE: When updating or generating new clients ensure that you rebuild the Jupyter Notebook docker images.

## ℹ️ Customise the Jupyter Notebook Environment (Optional steps)

The config files are located in `./config` folder, edit the `jupyter-config.json` for customization.

Remember that the local `./config` dir is mounted as `/home/jovyan/.jupyter/config` within the container.

### Exposing the Jupyter Notebooks publicly
In order to make the container publicly available, edit `docker-compose.yaml` and replace `- "127.0.0.1:8888:8888"` 
with `- "8888:8888"`. Remember, changing the port and host inside `jupyter-config.json` will only change the settings
inside the container, and likely to break the notebook.

### Passphrase

The default passphrase to access the notebook is `Prismv2`.

You will need to edit the `./config/jupyter-config.json` file and change the value of `NotebookApp.password` key. The
passphrase can be generated using the following command:

```bash
./passphrase
```

Use the output of the command to set the `NotebookApp.password` key.

### SSL

If you choose to set ssl certificates, place them in the `./config` folder and state the location of the files
as absolute paths in `./config/jupyter-config.json` starting with `/home/jovyan/work`:

```json
{
  "NotebookApp": {

    "certfile": "/home/jovyan/.jupyter/config/ssl-cert.pem",
    "keyfile": "/home/jovyan/.jupyter/config/ssl-cert.key",

  }
}
```
