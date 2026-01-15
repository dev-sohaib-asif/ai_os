"""OpenCode.Zen Vision AI integration"""
import logging
from typing import Dict, Any, Optional, Tuple
from openai import OpenAI
from config import settings

logger = logging.getLogger(__name__)


class VisionAI:
    """Handles vision AI interactions using OpenCode.Zen API"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.opencode_zen_api_key,
            base_url=settings.opencode_zen_base_url
        )
        self.model = settings.opencode_zen_model
    
    def analyze_screen_for_element(
        self, 
        base64_image: str, 
        user_command: str,
        screen_width: int,
        screen_height: int
    ) -> Dict[str, Any]:
        """
        Analyze screen to find the element described in user command
        
        Args:
            base64_image: Base64 encoded screenshot
            user_command: User's voice command
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            
        Returns:
            Dictionary with action details
        """
        try:
            # Create a detailed prompt for the AI
            prompt = f"""You are a computer vision assistant that helps control the mouse cursor.

Screen dimensions: {screen_width}x{screen_height} pixels

User command: "{user_command}"

Your task:
1. Analyze the screenshot and identify the element the user wants to interact with
2. Determine the exact pixel coordinates of that element's center
3. Determine what action to perform (click, double-click, right-click, drag, scroll)

Respond ONLY with a JSON object in this exact format:
{{
    "found": true/false,
    "element_name": "description of what was found",
    "x": pixel_x_coordinate,
    "y": pixel_y_coordinate,
    "action": "click|double_click|right_click|scroll_up|scroll_down|drag",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}

If dragging is required, use this format:
{{
    "found": true,
    "element_name": "description",
    "action": "drag",
    "start_x": start_pixel_x,
    "start_y": start_pixel_y,
    "end_x": end_pixel_x,
    "end_y": end_pixel_y,
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}

Important:
- Coordinates must be within screen bounds (0 to {screen_width} for x, 0 to {screen_height} for y)
- Be precise with coordinate detection
- Set found=false if you cannot locate the element with confidence
- Common elements: buttons, links, icons, text fields, play buttons, etc.
"""

            # Call the OpenCode.Zen API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            # Extract the response
            response_text = response.choices[0].message.content
            logger.info(f"AI Response: {response_text}")
            
            # Parse JSON response
            import json
            # Try to extract JSON from response (in case there's extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                return result
            else:
                logger.error("Could not find JSON in response")
                return {
                    "found": False,
                    "error": "Invalid response format"
                }
                
        except Exception as e:
            logger.error(f"Error analyzing screen: {e}")
            return {
                "found": False,
                "error": str(e)
            }
    
    def get_general_screen_description(self, base64_image: str) -> str:
        """
        Get a general description of what's on screen
        
        Args:
            base64_image: Base64 encoded screenshot
            
        Returns:
            Description of the screen
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe what you see on this screen in 2-3 sentences."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error getting screen description: {e}")
            return f"Error: {str(e)}"
