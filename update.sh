#!/bin/bash

echo "Building Shut Up Bot..."
docker build -t shutupbot .

echo "Stopping old container..."
docker stop my-bot 2>/dev/null

echo "Removing old container..."
docker rm my-bot 2>/dev/null

echo "Starting new container..."
docker run -d \
    --restart always \
    --env-file .env \
    --name my-bot \
    shutupbot

echo "Tailing logs..."
docker logs -f my-bot