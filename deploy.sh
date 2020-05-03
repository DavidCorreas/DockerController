#!/bin/bash

# Configuration
APP_INSTANCES=3
RABBIT_INSTANCES=2
MYSQL_SLAVES_INSTACES=2

# Clean the environment.
docker-compose down -v --remove-orphans

# Deploy the solution.
docker-compose up --build \
  --scale spring-app=$APP_INSTANCES \
  --scale rabbit-internal-service=$RABBIT_INSTANCES \
  --scale mysql-slave=$MYSQL_SLAVES_INSTACES

# Check the containers status.
docker ps
