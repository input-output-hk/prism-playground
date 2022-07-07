# Prism Playground Tutorial

This quick guide help you to set up with Kotlin Jupyter Notebooks to develop tutorials for Atala PRISM Kotlin SDK. 

# Environment set up

Before building Docker container, please, set up the following environment variables:
* `ATALA_GITHUB_ACTOR` - github username for the Atala PRISM repositories (atala-dev for common PPP token)
* `ATALA_GITHUB_TOKEN` - Prism access token provided to Prism Pioneers
* `ATALA_PRISM_VERSION` - version of Atala PRISM to use (latest for now is `v1.3.3`) 

## Option 1:

```shell
cp example.env .env
```

Once the example.env file is copied to .env, open the .env file and add the `PRISM_SDK_PASSWORD` token received from the Prism Pioneer program.

Then run the docker containers by executing:

```shell
./run.sh
```

The docker containers should build and execute Jupyter Notebook. The link to access the notebooks will be printed to screen as part of the output.

### Copy Atala Kotlin Dependancies into Jupyter Notebook
In the project directory, you will find `atala_sdk_dependencies.txt` file with the following content:
```text
@file:DependsOn("/home/atala_prism_sdk/prism-api-jvm-v1.3.3.jar")
@file:DependsOn("/home/atala_prism_sdk/prism-credentials-jvm-v1.3.3.jar")
@file:DependsOn("/home/atala_prism_sdk/prism-identity-jvm-v1.3.3.jar")
@file:DependsOn("/home/atala_prism_sdk/prism-crypto-jvm-v1.3.3.jar")
@file:DependsOn("/home/atala_prism_sdk/prism-protos-jvm-v1.3.3.jar")
...
```

You have to copy this file in your notebook before executing any imports from Atala PRISM SDK to make everything work.

## Option 2:
```shell
export PRISM_SDK_USER=atala-dev
export PRISM_SDK_PASSWORD=<secret-atala-token-ask-devs-for-it>
export ATALA_PRISM_VERSION=v1.3.3
```

### Build Docker container with Kotlin Jupyter kernel

After you successfully set the environment from previous section,
execute the following shell to build the Docker container:
```shell
docker build . \
    --build-arg PRISM_SDK_USER=${PRISM_SDK_USER} \
    --build-arg PRISM_SDK_PASSWORD=${PRISM_SDK_PASSWORD} \
    --build-arg ATALA_PRISM_VERSION=${ATALA_PRISM_VERSION} -t prism-playground
```

### Getting Atala PRISM SDK dependencies to use in Jupyter

Unfortunately, there is no simple way to connect external protected dependencies in Jupyter Kotlin kernel alltogether.
Neither new kernel creation nor all possible ways to pass additional `classpath` are not working without issues.
Some of them are breaking Kernel itself, some are just not working. As the result, we have to do one additional step
to prepare a quick file to copy-paste dependencies in the Notebook. To create such a file, execute the following command:
```shell
./gradlew saveAtalaSdkDependencies
```

### Copy Atala Kotlin Dependancies into Jupyter Notebook
In the project directory, you will find `atala_sdk_dependencies.txt` file with the following content:
```text
@file:DependsOn("/home/atala_prism_sdk/prism-api-jvm-v1.3.3.jar")
@file:DependsOn("/home/atala_prism_sdk/prism-credentials-jvm-v1.3.3.jar")
@file:DependsOn("/home/atala_prism_sdk/prism-identity-jvm-v1.3.3.jar")
@file:DependsOn("/home/atala_prism_sdk/prism-crypto-jvm-v1.3.3.jar")
@file:DependsOn("/home/atala_prism_sdk/prism-protos-jvm-v1.3.3.jar")
...
```

You have to copy this file in your notebook before executing any imports from Atala PRISM SDK to make everything work.

### Running Kotlin Jupyter kernel

When you successfully built Docker container, you could run it as follows:

```shell
docker container run -it --rm -p 8888:8888 -v "$(pwd)"/notebooks:/home/jovyan/notebooks prism-playground
```
