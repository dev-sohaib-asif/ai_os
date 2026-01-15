"""Main AI Agent for mouse control"""
import logging
from typing import Dict, Any
from screen_capture import ScreenCapture
from mouse_controller import MouseController
from vision_ai import VisionAI
import time

logger = logging.getLogger(__name__)


class MouseAgent:
    """AI Agent that controls mouse based on vision and voice commands"""
    
    def __init__(self):
        self.screen_capture = ScreenCapture()
        self.mouse_controller = MouseController()
        self.vision_ai = VisionAI()
        self.screen_width, self.screen_height = self.screen_capture.get_screen_dimensions()
        logger.info(f"Screen dimensions: {self.screen_width}x{self.screen_height}")
    
    async def process_command(self, voice_command: str) -> Dict[str, Any]:
        """
        Process a voice command and execute the appropriate mouse action
        
        Args:
            voice_command: The user's voice command
            
        Returns:
            Dictionary with execution result
        """
        try:
            logger.info(f"Processing command: {voice_command}")
            
            # Step 1: Capture the current screen
            logger.info("Capturing screen...")
            base64_image = self.screen_capture.capture_screen_base64()
            
            # Step 2: Analyze the screen with AI
            logger.info("Analyzing screen with AI...")
            analysis = self.vision_ai.analyze_screen_for_element(
                base64_image=base64_image,
                user_command=voice_command,
                screen_width=self.screen_width,
                screen_height=self.screen_height
            )
            
            # Step 3: Check if element was found
            if not analysis.get('found', False):
                return {
                    'success': False,
                    'message': f"Could not find the element: {analysis.get('error', 'Unknown error')}",
                    'analysis': analysis
                }
            
            # Step 4: Execute the action
            logger.info(f"Executing action: {analysis.get('action')}")
            action = analysis.get('action', 'click')
            
            if action == 'click':
                x = analysis.get('x')
                y = analysis.get('y')
                success = self.mouse_controller.move_and_click(x, y, 'left')
                
            elif action == 'double_click':
                x = analysis.get('x')
                y = analysis.get('y')
                self.mouse_controller.move_mouse_absolute(x, y)
                time.sleep(0.1)
                success = self.mouse_controller.double_click()
                
            elif action == 'right_click':
                x = analysis.get('x')
                y = analysis.get('y')
                success = self.mouse_controller.move_and_click(x, y, 'right')
                
            elif action == 'scroll_up':
                clicks = analysis.get('scroll_amount', 3)
                success = self.mouse_controller.scroll_up(clicks)
                
            elif action == 'scroll_down':
                clicks = analysis.get('scroll_amount', 3)
                success = self.mouse_controller.scroll_down(clicks)
                
            elif action == 'drag':
                start_x = analysis.get('start_x')
                start_y = analysis.get('start_y')
                end_x = analysis.get('end_x')
                end_y = analysis.get('end_y')
                success = self.mouse_controller.drag(start_x, start_y, end_x, end_y)
                
            else:
                return {
                    'success': False,
                    'message': f"Unknown action: {action}",
                    'analysis': analysis
                }
            
            if success:
                return {
                    'success': True,
                    'message': f"Successfully executed: {action} on {analysis.get('element_name')}",
                    'analysis': analysis
                }
            else:
                return {
                    'success': False,
                    'message': f"Failed to execute: {action}",
                    'analysis': analysis
                }
                
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'error': str(e)
            }
    
    async def get_screen_description(self) -> str:
        """
        Get a description of what's currently on screen
        
        Returns:
            Description string
        """
        try:
            base64_image = self.screen_capture.capture_screen_base64()
            description = self.vision_ai.get_general_screen_description(base64_image)
            return description
        except Exception as e:
            logger.error(f"Error getting screen description: {e}")
            return f"Error: {str(e)}"
