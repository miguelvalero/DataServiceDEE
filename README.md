# DataService

## Introduction
This module is responsible for interconnecting the API REST with the rest of the modules through the external broker.
The service receives data from modules in the ecosystem (pictures, positions) and stores them in the API REST. Modules can also ask the service to retrieve data.


## Installations
In order to run and contribute you must install Python 3.7. We recomend to use PyCharm as IDE for developments.
In order to contribute you must follow the contribution protocol described in the main repo of the Drone Engineering Ecosystem.
[![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-MainRepo-brightgreen.svg)](https://github.com/dronsEETAC/DroneEngineeringEcosystemDEE)

## Operation modes
The data service will run always in global communication mode.
To run the service you must edit the run/debug configuration in PyCharm in order to pass the required arguments to the script.
At least one parameter is required indicating the external broker to be used. In case the external broker requieres credentials,
two additional parameters must be included (username and password).


## Commands
In order to send a command to the data service, a module must publish a message in the external  broker. The topic of the message must be in the form:
```
"XXX/dataService/YYY"
```
where XXX is the name of the module requiring the service and YYY is the name of the service that is required. Some of the commands may require additional data that must be include in the payload of the message to be published.
In some cases, after completing the service requiered the data service publish a message as an answer. The topic of the answer has the format:
```
"dataService/XXX/ZZZ"
```
where XXX is the name of the module requiring the service and ZZZ is the answer. The message can include data in the message payload.

The table bellow indicates all the commands that are accepted by the data service in the current version.

Command | Description          | Payload | Answer | Answer payload
--- |----------------------| -- | --- |---
*storePosition* | stores a position | *latitude\*longitude* | No | No
*getStoredPositions* | provides the stored positions | No |  |Yes | string with stored positions
