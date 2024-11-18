#!/data/data/com.termux/files/usr/bin/bash
# Before running this script, make sure to make it executable using:
# chmod +x run.sh
# Then run it with: ./run.sh

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo "Creating Virtual Environment..."
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo ""

if ! command -v python &> /dev/null; then
    echo "Python is not installed. Installing Python..."
    pkg update -y
    pkg install -y python
fi

if ! python -c "import venv" &> /dev/null; then
    echo "Installing python-venv..."
    pkg install -y python-venv
fi

if ! command -v ffmpeg &> /dev/null; then
    echo "Installing FFmpeg..."
    pkg install -y ffmpeg
fi

if [ ! -d "venv" ]; then
    python -m venv venv
fi

source venv/bin/activate

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo "Installing Necessary Packages..."
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo ""

python -m pip install --upgrade pip
pip install -r requirements.txt -q

echo ""
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo "Necessary Packages Installed"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo ""

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo "App is Initializing..."
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo ""

python app.py

deactivate