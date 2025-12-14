#!/bin/bash

# Configs
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}Shut Up Bot: Initializing version 1.4${NC}"
echo -e "${CYAN}Shut Up Bot: See GitHub repository for changes.${NC}"
echo " "
echo -e "${YELLOW}>> Shut Up Bot: Building image${NC}"
docker build -t shutupbot .

if [ $? -ne 0 ]; then
    echo -e "\n${RED} Shut Up Bot: BUILD FAILED. The bot refuses to be compiled. Check the Dockerfile.${NC}"
    exit 1
fi
echo -e "${GREEN}>> Shut Up Bot: Build successful.${NC}\n"
echo -e "${YELLOW}>> Shut Up Bot: Stopping and removing previous container ('my-bot')${NC}"
docker stop my-bot > /dev/null 2>&1
docker rm my-bot > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}>> Shut Up Bot: Clean up complete${NC}\n"
else
    echo -e "${CYAN}>> Shut Up Bot: No old container found. Proceeding with fresh deployment.${NC}\n"
fi

echo -e "${YELLOW}>> Shut Up Bot: Launching new 'my-bot' container...${NC}"
docker run -d \
    --restart always \
    --env-file .env \
    --name my-bot \
    shutupbot

if [ $? -ne 0 ]; then
    echo -e "\n${RED}Shut Up Bot: LAUNCH FAILED. The bot refuses to run. Check logs manually.${NC}"
    exit 1
fi
echo -e "${GREEN}>>Shut Up Bot: Container 'my-bot' is running in the background (Daemon Mode).${NC}\n"

echo -e "${YELLOW}>> Shut Up Bot: Tailing Logs (Press CTRL+C to detach)...${NC}"
echo -e "${CYAN}--------------------------------------------------------------------${NC}"
docker logs -f my-bot

echo -e "\n${CYAN}## Shut Up Bot: Deployment concluded ##${NC}"