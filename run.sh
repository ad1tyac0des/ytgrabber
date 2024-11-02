#!/bin/bash

# Before running this script, make sure to make it executable using:
# chmod +x run.sh
# Then run it with: ./run.sh

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