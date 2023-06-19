# Use the miminal-notebook as base container
ARG BASE_CONTAINER=jupyter/minimal-notebook
FROM $BASE_CONTAINER

USER root
# Install curl, nestat, jq, netcat, iputils-ping
RUN apt-get update && \
    apt-get install -y curl net-tools jq netcat iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jovyan
# Copy the requirements.txt file
COPY requirements.txt requirements.txt

# Install all Python dependencies
RUN python3 -m pip install -r requirements.txt



# Install Prism V2 Agent generated client controller library
# Copy the library folder
ADD openapi-generator/prism-agent-client .
# Install all Python dependencies
RUN pip install --no-cache-dir -e .

# Install the widgets
RUN jupyter nbextension enable --py widgetsnbextension

# The base container takes care of the rest.
