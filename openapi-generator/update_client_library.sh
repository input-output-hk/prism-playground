#!/usr/bin/env bash
#pip3 install openapi-python-client
#openapi-python-client generate --url http://127.0.0.1:8080/prism-agent/api/openapi-spec.yaml
#openapi-python-client update --path derereferenced_openapi.yml/openapi/openapi.yaml

curl --location 'http://localhost:8080/docs/prism-agent/api/docs.yaml' --header 'apiKey: kxr9i@6XgKBUxe%O' > new_oas.yaml
openapi-python-client update --path new_oas.yaml