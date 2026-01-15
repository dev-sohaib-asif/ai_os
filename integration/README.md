# AI Mouse Agent 🖱️

AI-powered mouse control agent that uses OpenCode.Zen vision API to control your mouse based on voice commands on Wayland/Niri.

## Features

- 🎯 Vision-based element detection using OpenCode.Zen big-pickle model
- 🖱️ Full mouse control with ydotool on Wayland/Niri
- 🎤 Voice command processing via WebSocket
- 🔄 Real-time screen capture with grim
- 🚀 FastAPI WebSocket server
- 📦 Package management with `uv`

## Prerequisites

### System Requirements

1. **Wayland/Niri** window manager
2. **grim** - Screenshot utility for Wayland
3. **ydotool** - Generic command-line automation tool for Wayland

### Install System Dependencies

#### Arch Linux
```bash
sudo pacman -S grim ydotool
```

#### Ubuntu/Debian
```bash
sudo apt install grim ydotool
```

#### Fedora
```bash
sudo dnf install grim ydotool
```

### Setup ydotool

ydotool requires proper permissions. You need to either:

1. **Run ydotool daemon** (recommended):
```bash
# Start ydotool daemon
sudo systemctl enable ydotoold
sudo systemctl start ydotoold

# Add your user to input group
sudo usermod -aG input $USER
```

2. **Or configure sudoers** to run ydotool without password:
```bash
sudo visudo
# Add this line:
yourusername ALL=(ALL) NOPASSWD: /usr/bin/ydotool
```

## Installation

### 1. Install uv (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone or download this project
```bash
# Navigate to project directory
cd ai-mouse-agent
```

### 3. Install Python dependencies with uv
```bash
uv sync
```

### 4. Configure environment variables
Edit the `.env` file and add your OpenCode.Zen API key:
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# OpenCode.Zen API Configuration
OPENCODE_ZEN_API_KEY=your_actual_api_key_here
OPENCODE_ZEN_BASE_URL=https://opencode.ai/zen/v1
OPENCODE_ZEN_MODEL=big-pickle
```

## Usage

### Start the AI Mouse Agent

```bash
uv run python main.py
```

Or with uvicorn directly:
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Access the Web Interface

Open your browser and navigate to:
```
http://localhost:8000
```

### Send Voice Commands

You can send commands through:

1. **Web Interface**: Type commands in the web UI
2. **WebSocket**: Connect to `ws://localhost:8000/ws`

### Example Commands

- "Move mouse to YouTube play button"
- "Click on the submit button"
- "Right click on the file icon"
- "Scroll down"
- "Double click on the folder"
- "Drag from top left to bottom right"

## How It Works

1. **Screen Capture**: Uses `grim` to capture the current screen
2. **Vision Analysis**: Sends screenshot to OpenCode.Zen big-pickle model
3. **Element Detection**: AI identifies the target element and coordinates
4. **Mouse Control**: Executes mouse actions using `ydotool`

### Architecture

```
User Voice Command → WebSocket → FastAPI Server
                                      ↓
                              AI Agent (agent.py)
                                      ↓
                    ┌─────────────────┴─────────────────┐
                    ↓                                   ↓
            Screen Capture (grim)              Vision AI (OpenCode.Zen)
                    ↓                                   ↓
                Screenshot                      Element Detection
                    ↓                                   ↓
                    └─────────────────┬─────────────────┘
                                      ↓
                          Mouse Controller (ydotool)
                                      ↓
                              Execute Action
```

## Project Structure

```
ai-mouse-agent/
├── .env                    # Environment configuration
├── pyproject.toml          # UV project configuration
├── main.py                 # FastAPI server & WebSocket
├── agent.py                # Main AI agent logic
├── config.py               # Configuration management
├── screen_capture.py       # Screen capture utilities
├── mouse_controller.py     # Mouse control with ydotool
├── vision_ai.py            # OpenCode.Zen API integration
└── README.md               # This file
```

## API Endpoints

### WebSocket
- `ws://localhost:8000/ws` - Main WebSocket endpoint

### HTTP
- `GET /` - Web interface
- `GET /health` - Health check endpoint

## WebSocket Message Format

### Send Command
```json
{
  "type": "command",
  "command": "move mouse to play button"
}
```

### Get Screen Description
```json
{
  "type": "describe"
}
```

### Response
```json
{
  "type": "result",
  "success": true,
  "message": "Successfully executed: click on Play button",
  "analysis": {
    "found": true,
    "element_name": "Play button",
    "x": 640,
    "y": 360,
    "action": "click",
    "confidence": 0.95,
    "reasoning": "Located red play button in center"
  }
}
```

## Supported Mouse Actions

- **click**: Left click at coordinates
- **double_click**: Double left click
- **right_click**: Right click at coordinates
- **scroll_up**: Scroll up
- **scroll_down**: Scroll down
- **drag**: Drag from start to end coordinates

## ydotool Commands Reference

```bash
# Move mouse relatively
sudo ydotool mousemove 100 50
sudo ydotool mousemove -- -50 -30

# Move mouse absolutely
sudo ydotool mousemove -a 500 300

# Left click
sudo ydotool click 0xC0

# Right click
sudo ydotool click 0xC1

# Move and click
sudo ydotool mousemove -a 500 300 click 0xC0

# Drag operation
ydotool mousedown 0xC0 mousemove 200 100 mouseup 0xC0

# Scroll up
sudo ydotool click 0xC3

# Scroll down
sudo ydotool click 0xC4
```

## Troubleshooting

### ydotool not working
```bash
# Check if ydotool daemon is running
systemctl status ydotoold

# Start it if not running
sudo systemctl start ydotoold

# Check permissions
groups  # Should include 'input' group
```

### grim not capturing screen
```bash
# Test grim
grim /tmp/test.png

# Check if you're on Wayland
echo $XDG_SESSION_TYPE  # Should output 'wayland'
```

### OpenCode.Zen API errors
- Verify your API key in `.env`
- Check API quota/limits
- Ensure internet connection

### WebSocket connection issues
```bash
# Check if server is running
curl http://localhost:8000/health

# Check firewall
sudo ufw status
```

## Development

### Run with auto-reload
```bash
uv run uvicorn main:app --reload
```

### View logs
The application logs all actions to stdout. Check console for detailed information.

## Security Notes

- The agent requires `sudo` access for ydotool
- Be cautious with commands as they directly control your mouse
- Only expose the server on trusted networks
- Consider using authentication for production use

## License

MIT

## Contributing

Contributions welcome! Please feel free to submit pull requests or open issues.

## Acknowledgments

- OpenCode.Zen for the vision API
- ydotool for Wayland mouse control
- grim for screen capture
- FastAPI for the web framework
