# Running locally

This folder contains scripts to run the Atala PRISM Cloud Agent locally.

All images will be pulled from remote repositories and the `.env` file controls the versions of these images.

**Running using the scripts in this directory does not create a production-ready or secure environment. It is designed to allow easy development and should not be used to run a production instance**

## Example usage

To run the Atala PRISM Cloud Agent - execute the `run.sh` script. This can be run from within the directory or at the root of the source code project:

`./agent/run.sh`

## Scripts

| Name   | Purpose                              | Notes                                                                    |
| ------ | ------------------------------------ | ------------------------------------------------------------------------ |
| run.sh | Run the Atala PRISM Cloud Agent | Runs using docker-compose and versions are controlled by the `.env` file. Can be used to run multiple instances with command line paramaters [see below] |
| stop.sh  | Stops a running instance                                                                             | Used to stop a running instance if you've executed `run.sh` with the `-b/--background` option. Please note - you must supply the same `-n/--name` parameter to this script if you have used a non-default value in the `run.sh` script |

## run.sh

The `run.sh` script allows you to run multiple PRISM Cloud Agents locally. Please run `run.sh --help` for command line options.

Example - Run an instance named `inviter` on port 8080 and an instance named `invitee` on port 8090

> These examples show running in `background mode` using the `-b` flag. This means that docker-compose is passed the `daemon -d` flag.
> If you wish to run them in the foreground to view logs - please make sure each line is executed in a different terminal and the `-b` flag is removed.
> After running in either mode (foreground or background) - you can remove the local state of volumes by using the `stop.sh` script with the `-d` argument.

Starting the instances:

```
./run.sh -n inviter -p 8080 -b
./run.sh -n invitee -p 8090 -b
```

Stopping the instances:

```
./stop.sh -n inviter
./stop.sh -n invitee
```

OR

Specify the `-d` argument when stopping the instances to remove state:

```
./stop.sh -n inviter -d
./stop.sh -n invitee -d
```