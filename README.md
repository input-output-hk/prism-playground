# Prism V2 Playground  

This repository contains the PRISM Playground, a Jupyter Deployment that runs from a docker container. It also includes scripts to run local Prism Agents. The default script will start/stop three Prism Agents for the various actors (`issuer`, `holder` and `verifier`) used as part the Prism Playground.  

Within the PRISM Playground, we provide several notebooks to showcase the interactions that can be performed using the Atala PRISM Agent. These notebooks offer code examples for the following functionalities:
- Create a connection: Playground/Example 01 - Connections.ipynb
- DID Registrar: Playground/Example 02 - DID Registrar.ipynb 
- Issue a credential: Playground/Example 03 - Issue Credential.ipynb
- Present proof: Playground/Example 04 - Present proof.ipynb
- Schema registry: Playground/Example 05 - Schema registry.ipynb

To make the most of these examples, we encourage you to run the notebook cells in sequence, following the order specified in the file names. This will ensure a smooth experience and will help you to better understand the relationships between the different functionalities. 

In addition to the playground we mention here some alternative ways to interact with the PRISM Agents.


> ℹ️ Note  
If you don't want to do the setup and only like to see the notebooks examples results, we provide .md files with the notebooks outcomes in the folder `notebooks-output`

## Prerequisites 
Install and start [Docker Desktop](https://www.docker.com/products/docker-desktop/) and `docker-compose` in your local machine and ensure you have an active internet connection.  

To start the Prism Playground you can use the commands below to start and stop the Jupyter Notebook server and Prism Agents.

## Quick Start Guide

### 1. Run Prism Playground and Local Prism Agents

```bash
cd <path>/prism-playground

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
> ⚠ Warning  
Deployment using Window PowerShell is not supported. If you are using a Windows System run the scripts from a WSL2 Terminal. 

> ⚠ Warning  
If you are running Ubuntu (or Linux) operating system and have a firewall enabled ensure that you allow communication between the docker instances. Here is an example of adding a firewall rule with `ufw`:  
>> ```bash
>> sudo ufw allow to 172.17.0.1
>> ```

### 2a. Access the Prism Playground Jupyter Notebooks
   
This is the default location to access the Prism Playground notebooks:

```bash
http://127.0.0.1:8888/
```
The default password is `Prismv2` 

### 2b. Access the Prism Agent Swagger API

As an alternative to the notebooks you have the option to interact with the PRISM Agents using the Swagger Interface. These are the default locations to the Prism Agent Swagger:

[Issuer Agent Swagger Interface](http://localhost:8080/docs/prism-agent/api/)  
[Holder Agent Swagger Interface](http://localhost:8090/docs/prism-agent/api/)  
[Verifier Agent Swagger Interface](http://localhost:9000/docs/prism-agent/api/)  

> ℹ️ Note  
To use the Swagger API on a browser, you must include the `apikey` header with the value `kxr9i@6XgKBUxe%O` in your requests. To accomplish this, you can use a browser extension that allows you to add custom headers. There are multiple extensions available for Chromium based browsers, so feel free to use whichever one you prefer.

### 2c. Using the Prism Agent with Postman

If you would like to communicate with the PRISM Agent through Postman, you can import the OpenAPI specification file directly into Postman as a collection.
Here's how you can do it:  

#### Step 1: Launch Postman
Open the Postman application on your computer. If you haven't installed it yet, you can download it from the [official website](https://www.postman.com/downloads/).

#### Step 2: Navigate to the Import Menu
Look for the "Import" button, which is usually at the top left corner of the Postman interface.
Click on it to open the Import dialog.

#### Step 3: Choose Your File
In the Import dialog, you'll see several options for importing data. You can:
Drag and drop the .yaml file into the area labeled "Drag and Drop".
Click "Upload Files" and navigate to the location of the .yaml file on your computer, select it, and click "Open".

The .yaml file is located at `openapi-generator/derereferenced_openapi.yml/openapi/openapi.yaml`

#### Step 4: Import the File
After you've selected the file, Postman will display a preview of the import.
Click the "Import" button to finalize the process.

#### Step 5: View the Generated Collection
After importing, Postman will automatically generate a new collection based on the OpenAPI specification. This collection will appear in the "Collections" tab, usually located on the left sidebar.

### 2d. Using BlockTrust Credential Builder

Another option is to interact with the PRISM Agents using [Blocktrust credential builder](https://blocktrust.dev/credentialbuilder). Is important to mention the Atala Team does not gives support or maintain BlockTrust.dev projects but they offer nice tools that work with Atala PRISM.

> ℹ️ Note  
To use the Credential Builder with locally deployed PRISM Agents you need to use a workaround to `Enable Access-Control-Allow-Origin` and `Overwrite 4xx status codes` in your browser. In chrome the [cors-unblock](https://chrome.google.com/webstore/detail/cors-unblock/lfhmikememgdcahcdlaciloancbhjino) extensions does the trick.


### 3. Stop Prism Playground and Local Prism Agents
```bash
cd <path>/prism-playground

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
