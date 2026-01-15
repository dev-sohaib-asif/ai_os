"""Mouse control utilities using ydotool for Wayland/Niri"""
import subprocess
import logging
from typing import Tuple, Optional
import time

logger = logging.getLogger(__name__)


class MouseController:
    """Handles mouse control using ydotool on Wayland/Niri"""
    
    def __init__(self):
        self.check_dependencies()
    
    def check_dependencies(self):
        """Check if ydotool is installed and running"""
        try:
            subprocess.run(['which', 'ydotool'], check=True, capture_output=True)
            logger.info("ydotool is installed")
        except subprocess.CalledProcessError:
            logger.warning("ydotool is not installed. Install with your package manager.")
    
    def move_mouse_relative(self, x: int, y: int) -> bool:
        """
        Move mouse relatively
        
        Args:
            x: X offset
            y: Y offset
            
        Returns:
            True if successful
        """
        try:
            cmd = ['sudo', 'ydotool', 'mousemove', str(x), str(y)]
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Moved mouse relatively: ({x}, {y})")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to move mouse: {e}")
            return False
    
    def move_mouse_absolute(self, x: int, y: int) -> bool:
        """
        Move mouse to absolute position
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful
        """
        try:
            cmd = ['sudo', 'ydotool', 'mousemove', '-a', str(x), str(y)]
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Moved mouse to absolute position: ({x}, {y})")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to move mouse: {e}")
            return False
    
    def left_click(self) -> bool:
        """
        Perform left click at current position
        
        Returns:
            True if successful
        """
        try:
            cmd = ['sudo', 'ydotool', 'click', '0xC0']
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info("Left click performed")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to left click: {e}")
            return False
    
    def right_click(self) -> bool:
        """
        Perform right click at current position
        
        Returns:
            True if successful
        """
        try:
            cmd = ['sudo', 'ydotool', 'click', '0xC1']
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info("Right click performed")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to right click: {e}")
            return False
    
    def double_click(self) -> bool:
        """
        Perform double click
        
        Returns:
            True if successful
        """
        try:
            self.left_click()
            time.sleep(0.1)
            self.left_click()
            logger.info("Double click performed")
            return True
        except Exception as e:
            logger.error(f"Failed to double click: {e}")
            return False
    
    def move_and_click(self, x: int, y: int, click_type: str = 'left') -> bool:
        """
        Move mouse to absolute position and click
        
        Args:
            x: X coordinate
            y: Y coordinate
            click_type: 'left' or 'right'
            
        Returns:
            True if successful
        """
        try:
            # Move to position
            self.move_mouse_absolute(x, y)
            time.sleep(0.1)  # Small delay for stability
            
            # Click
            if click_type == 'left':
                self.left_click()
            elif click_type == 'right':
                self.right_click()
            
            logger.info(f"Moved to ({x}, {y}) and clicked {click_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to move and click: {e}")
            return False
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        """
        Perform drag operation
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            
        Returns:
            True if successful
        """
        try:
            # Move to start position
            self.move_mouse_absolute(start_x, start_y)
            time.sleep(0.1)
            
            # Mouse down
            cmd = ['sudo', 'ydotool', 'mousedown', '0xC0']
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Move to end position
            time.sleep(0.1)
            self.move_mouse_absolute(end_x, end_y)
            
            # Mouse up
            time.sleep(0.1)
            cmd = ['sudo', 'ydotool', 'mouseup', '0xC0']
            subprocess.run(cmd, check=True, capture_output=True)
            
            logger.info(f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to drag: {e}")
            return False
    
    def scroll_up(self, clicks: int = 1) -> bool:
        """
        Scroll up
        
        Args:
            clicks: Number of scroll clicks
            
        Returns:
            True if successful
        """
        try:
            for _ in range(clicks):
                cmd = ['sudo', 'ydotool', 'click', '0xC3']
                subprocess.run(cmd, check=True, capture_output=True)
                time.sleep(0.05)
            logger.info(f"Scrolled up {clicks} times")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to scroll up: {e}")
            return False
    
    def scroll_down(self, clicks: int = 1) -> bool:
        """
        Scroll down
        
        Args:
            clicks: Number of scroll clicks
            
        Returns:
            True if successful
        """
        try:
            for _ in range(clicks):
                cmd = ['sudo', 'ydotool', 'click', '0xC4']
                subprocess.run(cmd, check=True, capture_output=True)
                time.sleep(0.05)
            logger.info(f"Scrolled down {clicks} times")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to scroll down: {e}")
            return False
