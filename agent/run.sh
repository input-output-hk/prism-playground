#!/usr/bin/env bash

set -e

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

export VAULT_DEV_ROOT_TOKEN_ID="root"

Help() {
	# Display Help
	echo "Run an instance of the ATALA bulding-block stack locally"
	echo
	echo "Syntax: run.sh [-n/--name NAME|-p/--port PORT|-b/--background|-e/--env|-w/--wait|--network|-n/--ngrok|--debug|-h/--help]"
	echo "options:"
	echo "-n/--name              Name of this instance - defaults to dev."
	echo "-p/--port              Port to run this instance on - defaults to 80."
	echo "-b/--background        Run in docker-compose daemon mode in the background."
	echo "-e/--env               Provide your own .env file with versions."
	echo "-w/--wait              Wait until all containers are healthy (only in the background)."
	echo "--network              Specify a docker network to run containers on."
    echo "-n/--ngrok             Attempt to use an ngrok tunnel public URL for service endpoint"
	echo "--debug                Run additional services for debug using docker-compose debug profile."
	echo "-h/--help              Print this help text."
	echo
}

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
	case $1 in
	-n | --name)
		NAME="$2"
		shift # past argument
		shift # past value
		;;
	-p | --port)
		PORT="$2"
		shift # past argument
		shift # past value
		;;
	-b | --background)
		BACKGROUND="-d"
		shift # past argument
		;;
	-w | --wait)
		WAIT="--wait"
		shift # past argument
		;;
	-e | --env)
		ENV_FILE="$2"
		shift # past argument
		shift # past value
		;;
	-n|--ngrok)
		NGROK_TUNNEL=$(curl --silent localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
		if [ -z "$NGROK_TUNNEL" ]
		then
		echo "ngrok flag passed but could not determine ngrok tunnel endpoint. exiting."
		exit;
		fi
		DIDCOMM_SERVICE_ENDPOINT=${NGROK_TUNNEL}/didcomm
		shift # past argument
		;;
	--debug)
		DEBUG="--profile debug"
		shift # past argument
		;;
	-h | --help)
		Help
		exit
		;;
	-* | --*)
		echo "Unknown option $1"
		Help
		exit 1
		;;
	*)
		POSITIONAL_ARGS+=("$1") # save positional arg
		shift                   # past argument
		;;
	esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

if [[ -n $1 ]]; then
	echo "Last line of file specified as non-opt/last argument:"
	tail -1 "$1"
fi

NAME="${NAME:=local}"
PORT="${PORT:=80}"
ENV_FILE="${ENV_FILE:=${SCRIPT_DIR}/.env}"
DIDCOMM_SERVICE_ENDPOINT="${DIDCOMM_SERVICE_ENDPOINT:=http://${DOCKERHOST}:${PORT}/didcomm}"

echo "NAME                                = ${NAME}"
echo "PORT                                = ${PORT}"
echo "ENV_FILE                            = ${ENV_FILE}"
echo "NETWORK         					  = ${NETWORK}"
echo "DIDCOMM_SERVICE_ENDPOINT            = ${DIDCOMM_SERVICE_ENDPOINT}"

echo "--------------------------------------"
echo "Starting stack using docker compose"
echo "--------------------------------------"

PORT=${PORT} \
DIDCOMM_SERVICE_ENDPOINT=${DIDCOMM_SERVICE_ENDPOINT} \
docker compose \
	-p ${NAME} \
	-f ${SCRIPT_DIR}/docker-compose.yml \
	--env-file ${ENV_FILE} ${DEBUG} up ${BACKGROUND} ${WAIT}