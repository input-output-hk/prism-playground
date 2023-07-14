#!/usr/bin/env bash

#-a <authorization>, --auth <authorization>
#   adds authorization headers when fetching the OpenAPI definitions
#   remotely. Pass in a URL-encoded string of name:header with a comma
#   separating multiple values
#
# Example: 
#
#openapi-generator-cli generate -i http://localhost:8080/prism-agent/api/openapi-spec.yaml -g openapi-yaml -o ./derereferenced_openapi yml --auth apiKey:<url encoded token>

#openapi-generator-cli generate -i https://k8s-dev.atalaprism.io/docs/prism-agent/api/openapi-spec.yaml -g openapi-yaml -o ./derereferenced_openapi.yml

#openapi-generator-cli generate -i http://127.0.0.1:8080/prism-agent/api/openapi-spec.yaml -g openapi-yaml -o ./derereferenced_openapi.yml

#openapi-generator-cli generate -i https://nizhm0j69lrg.atalaprism.io/docs/prism-agent/api/openapi-spec.yaml -g openapi-yaml -o ./derereferenced_openapi.yml

#openapi-generator-cli generate -i http://localhost:8080/prism-agent/api/openapi-spec.yaml -g openapi-yaml -o ./derereferenced_openapi.yml --auth apiKey:kxr9i%406XgKBUxe%25O

openapi-generator-cli generate -i http://localhost:8080/docs/prism-agent/api/docs.yaml -g openapi-yaml -o ./derereferenced_openapi.yml --auth apiKey:kxr9i%406XgKBUxe%25O --skip-validate-spec