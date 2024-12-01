# 😢 Thanks for the Memories!

We had such good times together! But if you really need to uninstall YTGrabber, here is how (our door's always open for you 😁).

## 🔄 Quick Uninstall

### Windows

```powershell
python cleanup_command.py
```

### Linux/MacOS

```bash
python3 cleanup_command.py
```

## ⚙️ What happens during uninstallation?

The cleanup script will:
- Remove YTGrabber commands from your system PATH
- Clean up config files
- Keep your downloaded media files intact

<details>
<summary>
 📝 <u>Notes for Different Platforms</u>
</summary>

#### Windows Users
- The cleanup script will request admin access to modify system PATH
- No other system modifications will be made
- Your downloaded content will remain untouched

#### Linux/MacOS Users
- You may need to restart your terminal or run `source ~/.bashrc` (or `~/.zshrc`) after uninstallation
- All shell configurations will be cleaned up automatically
- Your downloaded content will remain untouched
</details>

## ❓ Having Issues?

If you encounter any problems during uninstallation:
1. Ensure you're running the command from the YTGrabber directory
2. Check if you have appropriate permissions
3. [Open an issue](https://github.com/ad1tyac0des/ytgrabber/issues) if you need help 

<br>

<div align='center'>
    <img src="https://media.tenor.com/DLbH0i7N7yIAAAAM/bay-anime-bye-anime.gif" width='450' height='300' alt="Goodbye anime gif">
</div>