# Quick Start Guide - AI Mouse Agent 🚀

Get your AI Mouse Agent running in 5 minutes!

## Prerequisites

- Linux system with Wayland/Niri
- Python 3.10+
- OpenCode.Zen API key ([Get one here](https://opencode.ai))

## Installation Steps

### 1. Run the Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- ✓ Install system dependencies (grim, ydotool)
- ✓ Setup ydotool permissions
- ✓ Install uv package manager
- ✓ Install Python dependencies
- ✓ Configure environment variables

### 2. Add Your API Key

The setup script will prompt you for your OpenCode.Zen API key, or you can manually edit `.env`:

```bash
nano .env
```

Replace `token` with your actual API key:
```
OPENCODE_ZEN_API_KEY=your_actual_api_key_here
```

### 3. Test the Installation (Optional)

```bash
uv run python test_agent.py
```

### 4. Start the Server

```bash
uv run python main.py
```

### 5. Open the Web Interface

Navigate to: **http://localhost:8000**

## Using the Agent

### Example Commands

Type these in the web interface:

1. **"Move mouse to the YouTube play button"**
   - AI will find the play button and move the cursor there

2. **"Click on the submit button"**
   - AI will find and click the submit button

3. **"Scroll down"**
   - Scrolls down the page

4. **"Right click on the file icon"**
   - Finds the file icon and right-clicks it

5. **"Double click on the folder"**
   - Finds and double-clicks a folder

### How Commands Work

1. You speak/type a command
2. Agent captures your screen with `grim`
3. Sends screenshot to OpenCode.Zen AI
4. AI identifies the element and coordinates
5. Executes mouse action with `ydotool`

## Troubleshooting

### Issue: ydotool not working

```bash
# Start the daemon
sudo systemctl start ydotoold

# Check status
systemctl status ydotoold

# Log out and back in if you just added to input group
```

### Issue: Permission denied

```bash
# Add to sudoers (no password for ydotool)
sudo visudo
# Add line: yourusername ALL=(ALL) NOPASSWD: /usr/bin/ydotool
```

### Issue: grim not found

```bash
# Install grim
sudo pacman -S grim  # Arch
sudo apt install grim  # Debian/Ubuntu
```

### Issue: API errors

- Check your API key in `.env`
- Verify internet connection
- Check OpenCode.Zen API status

## Project Structure

```
ai-mouse-agent/
├── main.py              # FastAPI server (start here)
├── agent.py             # AI agent logic
├── vision_ai.py         # OpenCode.Zen integration
├── screen_capture.py    # Screen capture (grim)
├── mouse_controller.py  # Mouse control (ydotool)
├── config.py            # Configuration
├── .env                 # Your API key
├── setup.sh             # Auto setup script
└── test_agent.py        # Test components
```

## Next Steps

- Try different commands
- Adjust AI temperature in `vision_ai.py` for more/less creativity
- Add custom actions in `agent.py`
- Integrate with speech-to-text for true voice control

## Getting Help

- Check `README.md` for detailed documentation
- Run tests with `uv run python test_agent.py`
- Enable debug logging in `main.py`

## Tips for Best Results

1. **Be specific**: "Click the red play button" vs "click button"
2. **Use landmarks**: "Click the button in the top right corner"
3. **Describe appearance**: "The blue submit button at the bottom"
4. **One action at a time**: Break complex tasks into steps

Enjoy your AI-powered mouse control! 🎉
