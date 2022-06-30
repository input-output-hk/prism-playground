#!/bin/bash

# Simple script to build Docker Images and run the Prism Playground environment

# Step 1 - Load Github Username and Token
source .env

# Step 2 - Build docker images
docker build . \
    --build-arg PRISM_SDK_USER=${PRISM_SDK_USER} \
    --build-arg PRISM_SDK_PASSWORD=${PRISM_SDK_PASSWORD} \
    --build-arg ATALA_PRISM_VERSION=${ATALA_PRISM_VERSION} -t prism-playground

# Step 3 - Build Gradle dependancies
./gradlew saveAtalaSdkDependencies

# Step 4 - Run Prism Playground Docker Image
docker container run -it --rm -p 8888:8888 -v "$(pwd)"/notebooks:/home/jovyan/notebooks prism-playground

