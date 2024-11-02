# YTGrabber

🎥 YTGrabber is a lightweight command-line tool that lets you download YouTube videos and audio with ease. Built with Python, it provides an interactive interface for selecting your preferred quality and format.

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![LICENSE](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

</div>

## Features

- Download videos in available quality formats (up to 4K)
- Extract audio in MP3 format 
- Interactive format selection:
  - Quick "Best Quality" option
  - Manual format selection with resolution, FPS and file size details
- Simple command-line interface
- Downloads saved in organized local folder

## Installation

1. Clone the repository
bash
git clone https://github.com/yourusername/ytgrabber.git
cd ytgrabber


2. Install dependencies and run the app using the automated script:

*Windows PowerShell*:
powershell
.\run.ps1


*Linux/MacOS*:
bash
chmod +x run.sh
./run.sh


3. Or install manually:

powershell
pip install -r requirements.txt
python app.py


## Usage

1. Run the application: python app.py
2. Enter the YouTube video URL when prompted
3. Choose between "Best Quality" or "Manual Selection"
4. Select your preferred format and type (video/audio)
5. Wait for download to complete

Files are saved in the downloads folder within the project directory.

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.