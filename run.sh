#!/bin/bash

# Before running this script, make sure to make it executable using:
# chmod +x run.sh
# Then run it with: ./run.sh

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo "Creating Virtual Environment..."
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo ""

if ! command -v python3 -m venv &> /dev/null; then
    echo "Installing python3-venv..."
    sudo apt-get update && sudo apt-get install -y python3-venv
fi

if ! command -v ffmpeg &> /dev/null; then
    echo "Installing FFmpeg..."
    if ! sudo apt-get install -y ffmpeg; then
        sudo apt-get update --ignore-missing && sudo apt-get install -y ffmpeg
    fi
fi

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo "Installing Necessary Packages..."
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo ""

python3 -m pip install --upgrade pip
pip3 install -r requirements.txt -q

echo ""
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo "Necessary Packages Installed"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo ""

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo "App is Initializing..."
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo ""

python3 app.py
deactivate