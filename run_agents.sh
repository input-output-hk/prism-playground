#!/usr/bin/env bash
# ====================================================================
# Get the Docker host address depending on the host system.
#
# Networking changes introduced in Docker 4.1.x and forward on
# Windows and MAC stop the direct use of the internal docker host IP
# returned by the `docker run --rm --net=host eclipse/che-ip` process.
# On Windows and MAC `host.docker.internal` needs to be used for
# internal connections between containers on separate docker networks.
#
# `host.docker.internal` has been available on Windows and Mac since
# Docker Engine version 18.03 (March 2018).
#
# Support for `host.docker.internal` on Linux was introduced in
# version 20.10.0 (2020-12-08), but it does not run out of the
# box yet (as of Docker Engine 20.10.11 (2021-11-17)).
# You need to add `--add-host=host.docker.internal:host-gateway`
# to the `docker run` command in order for it to work.
# --------------------------------------------------------------------
function getDockerHost() {
  (
    local dockerHostAddress
    unset dockerHostAddress
    if [[ $(uname) == "Linux" ]] ; then
      dockerHostAddress=$(docker run --rm --net=host eclipse/che-ip)
    else
      dockerHostAddress=host.docker.internal
    fi
    echo ${DOCKERHOST:-${APPLICATION_URL:-${dockerHostAddress}}}
  )
}
# ====================================================================
export DOCKERHOST=$(getDockerHost)
set -e

./agent/run.sh -n issuer -p 8080 -b;./agent/run.sh -n holder -p 8090 -b;./agent/run.sh -n verifier -p 9000 -b