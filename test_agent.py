#!/usr/bin/env python3
"""Test script for AI Mouse Agent components"""
import asyncio
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


async def test_screen_capture():
    """Test screen capture functionality"""
    print("\n" + "="*50)
    print("Testing Screen Capture")
    print("="*50)
    
    try:
        from screen_capture import ScreenCapture
        
        capture = ScreenCapture()
        
        # Test getting screen dimensions
        width, height = capture.get_screen_dimensions()
        print(f"✓ Screen dimensions: {width}x{height}")
        
        # Test capturing screen
        screenshot_path = capture.capture_screen("/tmp/test_screenshot.png")
        print(f"✓ Screenshot saved to: {screenshot_path}")
        
        # Test base64 encoding
        base64_data = capture.capture_screen_base64()
        print(f"✓ Base64 screenshot generated (length: {len(base64_data)} chars)")
        
        return True
    except Exception as e:
        print(f"✗ Screen capture test failed: {e}")
        return False


async def test_mouse_controller():
    """Test mouse controller functionality"""
    print("\n" + "="*50)
    print("Testing Mouse Controller")
    print("="*50)
    
    try:
        from mouse_controller import MouseController
        
        controller = MouseController()
        
        print("⚠ This will move your mouse! Press Ctrl+C to cancel within 3 seconds...")
        await asyncio.sleep(3)
        
        # Test relative movement
        print("Testing relative movement...")
        controller.move_mouse_relative(10, 10)
        await asyncio.sleep(0.5)
        controller.move_mouse_relative(-10, -10)
        print("✓ Relative movement works")
        
        return True
    except KeyboardInterrupt:
        print("\n✗ Mouse controller test cancelled")
        return False
    except Exception as e:
        print(f"✗ Mouse controller test failed: {e}")
        return False


async def test_vision_ai():
    """Test Vision AI functionality"""
    print("\n" + "="*50)
    print("Testing Vision AI")
    print("="*50)
    
    try:
        from vision_ai import VisionAI
        from screen_capture import ScreenCapture
        
        # Check if API key is set
        from config import settings
        if settings.opencode_zen_api_key == "token":
            print("✗ Please set your OpenCode.Zen API key in .env file")
            return False
        
        vision = VisionAI()
        capture = ScreenCapture()
        
        # Get screen description
        print("Getting screen description...")
        base64_image = capture.capture_screen_base64()
        description = vision.get_general_screen_description(base64_image)
        print(f"✓ Screen description: {description}")
        
        return True
    except Exception as e:
        print(f"✗ Vision AI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_agent():
    """Test the full AI agent"""
    print("\n" + "="*50)
    print("Testing AI Agent")
    print("="*50)
    
    try:
        from agent import MouseAgent
        
        # Check if API key is set
        from config import settings
        if settings.opencode_zen_api_key == "token":
            print("✗ Please set your OpenCode.Zen API key in .env file")
            return False
        
        agent = MouseAgent()
        
        # Test screen description
        print("\nGetting screen description...")
        description = await agent.get_screen_description()
        print(f"✓ Screen: {description}")
        
        # Interactive command test
        print("\n" + "="*50)
        print("Interactive Command Test")
        print("="*50)
        print("Enter a command to test (or 'skip' to skip):")
        print("Example: 'move mouse to the center of the screen'")
        
        command = input("> ").strip()
        
        if command.lower() != 'skip' and command:
            print(f"\nProcessing: {command}")
            result = await agent.process_command(command)
            
            if result['success']:
                print(f"✓ Success: {result['message']}")
                if 'analysis' in result:
                    print(f"  Element: {result['analysis'].get('element_name', 'N/A')}")
                    print(f"  Action: {result['analysis'].get('action', 'N/A')}")
                    print(f"  Confidence: {result['analysis'].get('confidence', 0)*100:.1f}%")
            else:
                print(f"✗ Failed: {result['message']}")
        
        return True
    except Exception as e:
        print(f"✗ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" AI MOUSE AGENT - COMPONENT TESTS")
    print("="*70)
    
    results = {}
    
    # Test screen capture
    results['screen_capture'] = await test_screen_capture()
    
    # Test mouse controller
    results['mouse_controller'] = await test_mouse_controller()
    
    # Test vision AI
    results['vision_ai'] = await test_vision_ai()
    
    # Test full agent
    results['agent'] = await test_agent()
    
    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    
    for component, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{component.replace('_', ' ').title():.<50} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print("\n" + "="*70)
    print(f"Total: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n🎉 All tests passed! Your AI Mouse Agent is ready to use.")
        print("\nTo start the server:")
        print("  uv run python main.py")
    else:
        print("\n⚠ Some tests failed. Please check the error messages above.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
