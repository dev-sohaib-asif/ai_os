"""FastAPI WebSocket Server for AI Mouse Agent"""

import logging
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from WebSocket.config import settings
from WebSocket.agent import MouseAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Mouse Agent",
    description="AI-powered mouse control using vision and voice commands",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the AI agent
agent = MouseAgent()

# Store active WebSocket connections
active_connections: List[WebSocket] = []


class ConnectionManager:
    """Manages WebSocket connections"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def send_message(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")


manager = ConnectionManager()


@app.get("/")
async def get_home():
    """Home page with WebSocket test client"""
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>AI Mouse Agent - Control Panel</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .container {
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                }
                h1 {
                    color: #667eea;
                    text-align: center;
                    margin-bottom: 10px;
                }
                .subtitle {
                    text-align: center;
                    color: #666;
                    margin-bottom: 30px;
                }
                .status {
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    text-align: center;
                    font-weight: bold;
                }
                .status.connected {
                    background: #d4edda;
                    color: #155724;
                }
                .status.disconnected {
                    background: #f8d7da;
                    color: #721c24;
                }
                .input-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                    color: #333;
                    font-weight: 500;
                }
                input[type="text"] {
                    width: 100%;
                    padding: 12px;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    font-size: 16px;
                    box-sizing: border-box;
                    transition: border-color 0.3s;
                }
                input[type="text"]:focus {
                    outline: none;
                    border-color: #667eea;
                }
                button {
                    background: #667eea;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    cursor: pointer;
                    margin-right: 10px;
                    transition: background 0.3s;
                }
                button:hover {
                    background: #5568d3;
                }
                button:disabled {
                    background: #ccc;
                    cursor: not-allowed;
                }
                #messages {
                    margin-top: 20px;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 8px;
                    max-height: 400px;
                    overflow-y: auto;
                }
                .message {
                    padding: 10px;
                    margin: 5px 0;
                    border-radius: 5px;
                    font-size: 14px;
                }
                .message.sent {
                    background: #e3f2fd;
                    border-left: 4px solid #2196f3;
                }
                .message.received {
                    background: #f1f8e9;
                    border-left: 4px solid #8bc34a;
                }
                .message.error {
                    background: #ffebee;
                    border-left: 4px solid #f44336;
                }
                .examples {
                    margin-top: 20px;
                    padding: 15px;
                    background: #fff3cd;
                    border-radius: 8px;
                    border-left: 4px solid #ffc107;
                }
                .examples h3 {
                    margin-top: 0;
                    color: #856404;
                }
                .examples ul {
                    margin: 10px 0;
                    padding-left: 20px;
                }
                .examples li {
                    margin: 5px 0;
                    color: #856404;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🖱️ AI Mouse Agent</h1>
                <p class="subtitle">Control your mouse with voice commands powered by AI vision</p>
                
                <div id="status" class="status disconnected">Disconnected</div>
                
                <div class="input-group">
                    <label for="command">Voice Command:</label>
                    <input type="text" id="command" placeholder="e.g., move mouse to YouTube play button">
                </div>
                
                <button id="sendBtn" onclick="sendCommand()" disabled>Send Command</button>
                <button onclick="getDescription()">Describe Screen</button>
                <button onclick="clearMessages()">Clear Messages</button>
                
                <div class="examples">
                    <h3>📝 Example Commands:</h3>
                    <ul>
                        <li>"Move mouse to YouTube play button"</li>
                        <li>"Click on the submit button"</li>
                        <li>"Right click on the file icon"</li>
                        <li>"Scroll down"</li>
                        <li>"Double click on the folder"</li>
                        <li>"Drag from the top left to bottom right"</li>
                    </ul>
                </div>
                
                <div id="messages"></div>
            </div>
            
            <script>
                let ws = null;
                
                function connect() {
                    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                    ws = new WebSocket(protocol + '//' + window.location.host + '/ws');
                    
                    ws.onopen = function(event) {
                        updateStatus(true);
                        addMessage('Connected to AI Mouse Agent', 'received');
                    };
                    
                    ws.onmessage = function(event) {
                        const data = JSON.parse(event.data);
                        handleResponse(data);
                    };
                    
                    ws.onerror = function(error) {
                        addMessage('WebSocket Error: ' + error, 'error');
                    };
                    
                    ws.onclose = function(event) {
                        updateStatus(false);
                        addMessage('Disconnected from server', 'error');
                        // Attempt to reconnect after 3 seconds
                        setTimeout(connect, 3000);
                    };
                }
                
                function updateStatus(connected) {
                    const status = document.getElementById('status');
                    const sendBtn = document.getElementById('sendBtn');
                    
                    if (connected) {
                        status.textContent = 'Connected';
                        status.className = 'status connected';
                        sendBtn.disabled = false;
                    } else {
                        status.textContent = 'Disconnected';
                        status.className = 'status disconnected';
                        sendBtn.disabled = true;
                    }
                }
                
                function sendCommand() {
                    const command = document.getElementById('command').value;
                    if (!command.trim()) {
                        alert('Please enter a command');
                        return;
                    }
                    
                    const message = {
                        type: 'command',
                        command: command
                    };
                    
                    ws.send(JSON.stringify(message));
                    addMessage('Sent: ' + command, 'sent');
                    document.getElementById('command').value = '';
                }
                
                function getDescription() {
                    const message = {
                        type: 'describe'
                    };
                    ws.send(JSON.stringify(message));
                    addMessage('Requesting screen description...', 'sent');
                }
                
                function handleResponse(data) {
                    if (data.type === 'result') {
                        const success = data.success;
                        const message = data.message;
                        const className = success ? 'received' : 'error';
                        addMessage('Result: ' + message, className);
                        
                        if (data.analysis) {
                            const details = `Element: ${data.analysis.element_name || 'N/A'}, ` +
                                          `Action: ${data.analysis.action || 'N/A'}, ` +
                                          `Confidence: ${(data.analysis.confidence * 100).toFixed(1)}%`;
                            addMessage(details, className);
                        }
                    } else if (data.type === 'description') {
                        addMessage('Screen: ' + data.description, 'received');
                    } else if (data.type === 'error') {
                        addMessage('Error: ' + data.message, 'error');
                    }
                }
                
                function addMessage(text, className) {
                    const messages = document.getElementById('messages');
                    const message = document.createElement('div');
                    message.className = 'message ' + className;
                    message.textContent = new Date().toLocaleTimeString() + ' - ' + text;
                    messages.appendChild(message);
                    messages.scrollTop = messages.scrollHeight;
                }
                
                function clearMessages() {
                    document.getElementById('messages').innerHTML = '';
                }
                
                // Allow Enter key to send command
                document.getElementById('command').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendCommand();
                    }
                });
                
                // Connect on page load
                connect();
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for receiving voice commands"""
    await manager.connect(websocket)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)

            logger.info(f"Received message: {message}")

            # Handle different message types
            if message.get("type") == "command":
                command = message.get("command", "")

                # Process the command with the AI agent
                result = await agent.process_command(command)

                # Send result back to client
                await manager.send_message(
                    websocket,
                    {
                        "type": "result",
                        "success": result.get("success", False),
                        "message": result.get("message", ""),
                        "analysis": result.get("analysis", {}),
                    },
                )

            elif message.get("type") == "describe":
                # Get screen description
                description = await agent.get_screen_description()

                await manager.send_message(
                    websocket, {"type": "description", "description": description}
                )

            else:
                await manager.send_message(
                    websocket, {"type": "error", "message": "Unknown message type"}
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": settings.opencode_zen_model,
        "base_url": settings.opencode_zen_base_url,
    }


if __name__ == "__main__":
    logger.info(f"Starting AI Mouse Agent on {settings.api_host}:{settings.api_port}")
    logger.info(f"Using model: {settings.opencode_zen_model}")

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level="info",
    )
