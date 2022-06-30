FROM jupyter/base-notebook

USER root

# Install linux dependencies
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk ant git ca-certificates-java build-essential && \
    apt-get clean && update-ca-certificates -f

# Install kotlin kernel
RUN conda install -c jetbrains kotlin-jupyter-kernel

# Token to download SDK dependencies
ARG PRISM_SDK_USER
RUN test -n "${PRISM_SDK_USER}"
ENV PRISM_SDK_USER ${PRISM_SDK_USER}

ARG PRISM_SDK_PASSWORD
RUN test -n "${PRISM_SDK_PASSWORD}"
ENV PRISM_SDK_PASSWORD ${PRISM_SDK_PASSWORD}

# Version of Atala PRISM to be downloaded
ARG ATALA_PRISM_VERSION="v1.3.3"
ENV ATALA_PRISM_VERSION ${ATALA_PRISM_VERSION}

COPY . /kotlin-jupyter-example
RUN cd /kotlin-jupyter-example && ./gradlew copyToJypiterClassPath --info

USER jovyan

ENV ATALA_PRISM_SDK_JAVA_HOME "/home/atala_prism_sdk/*"
