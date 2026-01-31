#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting The Factory Dashboard...${NC}"

# Check for existing processes on ports 3000 and 8000
echo "Checking for conflicting processes..."

# Kill port 3000 (Next.js default)
if lsof -ti:3000 >/dev/null; then
    echo -e "${RED}Found process on port 3000. Killing it...${NC}"
    lsof -ti:3000 | xargs kill -9
fi

# Kill port 8000 (Python server default - just in case user left it running)
if lsof -ti:8000 >/dev/null; then
    echo -e "${RED}Found process on port 8000. Killing it...${NC}"
    lsof -ti:8000 | xargs kill -9
fi

# Navigate to dashboard directory
cd "$(dirname "$0")/../dashboard" || { echo "Dashboard directory not found!"; exit 1; }

# Install dependencies if node_modules is missing
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies (first run)..."
    npm install
fi

# Start the dev server in the background
echo "Starting development server..."
npm run dev &
SERVER_PID=$!

echo "Waiting for server to be ready on http://localhost:3000..."

# Wait loop
MAX_RETRIES=30
count=0
while ! nc -z localhost 3000; do   
  sleep 1
  count=$((count+1))
  if [ $count -ge $MAX_RETRIES ]; then
      echo -e "${RED}Timeout waiting for server!${NC}"
      kill $SERVER_PID
      exit 1
  fi
done

echo -e "${GREEN}✅ Server is UP! Opening dashboard...${NC}"
sleep 2 # Give it a moment to initialize fully
open http://localhost:3000

# Keep script running to maintain the server process
wait $SERVER_PID
