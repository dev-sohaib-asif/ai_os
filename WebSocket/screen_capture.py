"""Screen capture utilities for Wayland/Niri"""
import subprocess
import base64
import io
import os
from PIL import Image
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class ScreenCapture:
    """Handles screen capturing on Wayland/Niri using grim"""
    
    def __init__(self):
        self.check_dependencies()
    
    def check_dependencies(self):
        """Check if required tools are installed"""
        try:
            subprocess.run(['which', 'grim'], check=True, capture_output=True)
            logger.info("grim is installed")
        except subprocess.CalledProcessError:
            logger.warning("grim is not installed. Install with: sudo pacman -S grim (Arch) or sudo apt install grim (Debian/Ubuntu)")
    
    def capture_screen(self, output_path: Optional[str] = None) -> str:
        """
        Capture the current screen using grim
        
        Args:
            output_path: Optional path to save the screenshot
            
        Returns:
            Path to the captured screenshot
        """
        if output_path is None:
            output_path = "/tmp/screenshot.png"
        
        try:
            # Use grim to capture the screen on Wayland
            subprocess.run(['grim', output_path], check=True, capture_output=True)
            logger.info(f"Screenshot captured: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to capture screen: {e}")
            raise
    
    def capture_screen_base64(self) -> str:
        """
        Capture screen and return as base64 encoded string
        
        Returns:
            Base64 encoded screenshot
        """
        screenshot_path = self.capture_screen()
        
        with open(screenshot_path, 'rb') as f:
            image_data = f.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Clean up temporary file
        os.remove(screenshot_path)
        
        return base64_image
    
    def get_screen_dimensions(self) -> Tuple[int, int]:
        """
        Get the screen dimensions
        
        Returns:
            Tuple of (width, height)
        """
        screenshot_path = self.capture_screen()
        
        with Image.open(screenshot_path) as img:
            dimensions = img.size
        
        os.remove(screenshot_path)
        
        return dimensions
