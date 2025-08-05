#!/usr/bin/env python3
"""
Automatic demo of the Voice Assistant - no input required
"""

import time
from voice_assistant.command_processor import CommandProcessor

class SilentTTS:
    """Silent TTS handler for demo purposes"""
    def speak(self, text):
        print(f"🔊 Assistant: {text}")

def run_auto_demo():
    """Run automatic demonstration of all features"""
    print("=" * 60)
    print("🎤 VOICE ASSISTANT - AUTOMATIC DEMONSTRATION")
    print("=" * 60)
    
    # Initialize with silent TTS
    tts = SilentTTS()
    processor = CommandProcessor(tts)
    
    # Demo commands
    demo_commands = [
        ("what time is it", "Getting current time"),
        ("what date is it", "Getting current date"),
        ("search wikipedia for python programming", "Searching Wikipedia"),
        ("open google", "Opening website"),
        ("hello", "Basic greeting"),
        ("help", "Showing help information")
    ]
    
    print("Demonstrating voice assistant capabilities:\n")
    
    for i, (command, description) in enumerate(demo_commands, 1):
        print(f"{i}. {description}")
        print(f"   Command: '{command}'")
        
        try:
            response = processor.process_command(command)
            print(f"   🔊 Assistant: {response}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()  # Empty line for readability
        time.sleep(0.5)  # Brief pause between commands
    
    print("=" * 60)
    print("✅ DEMONSTRATION COMPLETE!")
    print("=" * 60)
    print("\nYour Voice Assistant features:")
    print("✓ Speech recognition (speech_recognition library)")
    print("✓ Text-to-speech responses (pyttsx3)")
    print("✓ Wake word detection")
    print("✓ Time and date queries")
    print("✓ Wikipedia searches")
    print("✓ Website opening commands")
    print("✓ Basic conversation handling")
    print("✓ Help system")
    print("\n🚀 Voice Assistant is ready for use!")
    print("   - Use main.py for full voice interaction (on local machine)")
    print("   - Use demo_mode.py for interactive text testing")

if __name__ == "__main__":
    run_auto_demo()