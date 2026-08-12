#!/bin/bash

# Get the exact directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if the server is already running by looking at port 5001
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo "yt-dlp server is already running in the background!"
else
    echo "Starting yt-dlp server..."
    # Tell macOS to open a fresh Terminal window and run the python server
    osascript -e "tell application \"Terminal\" to do script \"cd '$DIR' && python3 server.py\""
    
    # Give the Flask server 2 seconds to fully boot up before opening the browser
    sleep 2
fi

# Open the UI in the default web browser (Safari, Chrome, etc.)
echo "Launching Web UI..."
open "http://127.0.0.1:5001/"