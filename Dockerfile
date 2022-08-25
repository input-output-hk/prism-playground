FROM jupyter/base-notebook

USER root

# Install linux dependencies
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk ant git ca-certificates-java build-essential python3 && \
    apt-get clean && update-ca-certificates -f

RUN pip install -U pip setuptools wheel
RUN pip install JPype1==1.3.0

# Install kotlin kernel
RUN conda install -c jetbrains kotlin-jupyter-kernel

# Github User
ARG ATALA_GITHUB_ACTOR
RUN test -n "${ATALA_GITHUB_ACTOR}"
ENV ATALA_GITHUB_ACTOR ${ATALA_GITHUB_ACTOR}

# Token to download SDK dependencies
ARG ATALA_GITHUB_TOKEN
RUN test -n "${ATALA_GITHUB_TOKEN}"
ENV ATALA_GITHUB_TOKEN ${ATALA_GITHUB_TOKEN}

# Version of Atala PRISM to be downloaded
ARG ATALA_PRISM_VERSION="v1.4.0"
ENV ATALA_PRISM_VERSION ${ATALA_PRISM_VERSION}

COPY . /prism-playground
RUN cd /prism-playground && ./gradlew copyToJypiterClassPath --info

USER jovyan

ENV ATALA_PRISM_JARS "/home/atala_prism_sdk/"
