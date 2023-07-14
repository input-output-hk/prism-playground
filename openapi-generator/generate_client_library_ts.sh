#!/usr/bin/env bash

# openapi-generator-cli generate \
#   -i http://localhost:8090/prism-agent/api/openapi-spec.yaml \
#   -o prism-agent-ts-open-api \
#   -g typescript-fetch \
#   -a apiKey:kxr9i%406XgKBUxe%25O \
#   --additional-properties=supportsES6=true,typescriptThreePlus=true


  openapi-generator-cli generate \
  -i http://localhost:8080/docs/prism-agent/api/docs.yaml \
  -o prism-agent-ts-open-api \
  -g typescript-fetch \
  -a apiKey:kxr9i%406XgKBUxe%25O \
  --additional-properties=supportsES6=true,typescriptThreePlus=true --skip-validate-spec