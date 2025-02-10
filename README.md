# Events Gateway

## Overview
The **Events Gateway** is a microservice designed to provide an API for events generators and the configuration client.
After receiving an event, the gateway sends it to the **Events Preprocessor** using selected message broker (Apache Kafka by default).

## Architecture
The **Events Gateway** service is a part of the **Events Flow Analyser** project. 
This service based on the Clean Architecture principles.
The service has the following layers:
* **Entities** - contains the business objects of the application. No particular framework or library should influence these objects.
* **Use Cases** - contains the application's business rules. This layer is independent of the infrastructure and frameworks.
* **Adapters** - This layer is a bridge between the Use Cases and the infrastructure.
* **Infrastructure** - contains the infrastructure (Databases, APIs, etc.) and frameworks. 
* **Main file** - This is the entry point of the application. Here you can configure which infrastructure you want to use.

## Testing
The service has unit and integration tests. Unit tests mostly cover the Use Cases layer, and integration tests cover the Adapters and Infrastructure layers.
For the types checking the service uses MyPy.

## Database
The service uses Kafka as a message broker. For storing configuration data and the business entities, the service uses PostgreSQL (connection is based on SQLAlchemy).
But you can easily change the database adding implementation of the AbstractEventsStorage or the AbstractEntitiesStorage interfaces.

## Requirements
python 3.11 or higher

## Running

```uvicorn main:app``` to run the server

```pytest``` to run unit and integration tests