<div align="center">

# 🤖 Android Installation Guide

<span style="font-size: 1.1em; color: #3DDC84;">Download videos from YouTube on Android using Termux</span>

[![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)](https://www.android.com/)
[![Termux](https://img.shields.io/badge/Termux-000000?style=for-the-badge&logo=termux&logoColor=white)](https://f-droid.org/en/packages/com.termux/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)

<img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNW9hN29lY2FlZHhpN3hkcnZmZ211Y2Y4MjBoaWZ6NTF0dG1uazM2MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/10mzF0YmVmZNuw/giphy.gif" width="500" height="300">

</div>

## 📲 Installing Termux
##### 1. Download F-Droid from [here](https://f-droid.org/) 🔍
##### 2. Open F-Droid and search for `Termux` or directly visit [Termux on F-Droid](https://f-droid.org/en/packages/com.termux/) 🔎
##### 3. Install Termux from F-Droid ⬇️

## 🛠️ Setting Up the Environment
#### 1. Open Termux and run these commands one by one:
   ```bash
   pkg update && pkg upgrade -y
   ```

   ```bash
   pkg install python git ffmpeg -y
   ```
   ```bash
   termux-setup-storage
   ```

## 🚀 Installing and Running the YTGrabber
#### 1. Clone the repository
   ```bash
   git clone https://github.com/ad1tyac0des/ytgrabber
   ```
   ```bash
   cd ytgrabber
   ```

#### 2. Make quickstart-termux.sh executable
   ```bash
   chmod +x quickstart-termux.sh
   ```

#### 3. Run the application
   ```bash
   ./quickstart-termux.sh
   ```

<br>

<div align="center">
<img src="https://i.pinimg.com/originals/38/20/04/38200478b91db2d19a12ecf4672391c9.gif" width="500" height="300">

</div>

## ⚠️ Troubleshooting

- If you encounter permission errors, ensure all commands are run with proper permissions
- For storage access issues, run: `termux-setup-storage`, or click [here](https://wiki.termux.com/wiki/Termux-setup-storage) to know more about it
- If FFmpeg fails to install, try: `pkg install ffmpeg -y` separately

## 📝 Notes
- The `quickstart-termux.sh` script will automatically install all required dependencies
- First run might take longer as it sets up the virtual environment and installs packages