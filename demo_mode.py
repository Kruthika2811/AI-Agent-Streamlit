#!/usr/bin/env python3
"""
Demo mode for the Voice Assistant (text-based simulation)
This demonstrates all the functionality without requiring audio hardware
"""

import sys
from voice_assistant.command_processor import CommandProcessor
from voice_assistant.tts_handler import TTSHandler

class DemoVoiceAssistant:
    def __init__(self):
        """Initialize the demo voice assistant"""
        print("Initializing Demo Voice Assistant...")
        
        try:
            self.tts = TTSHandler()
            self.processor = CommandProcessor(self.tts)
            self.running = False
            
            print("Demo Voice Assistant initialized successfully!")
            print("This demo simulates voice commands through text input.")
            
        except Exception as e:
            print(f"Error initializing Demo Voice Assistant: {e}")
            # Continue without TTS if it fails
            self.tts = None
            self.processor = CommandProcessor(None)
    
    def simulate_speech(self, text):
        """Simulate TTS output"""
        print(f"🔊 Assistant says: {text}")
        if self.tts:
            try:
                self.tts.speak(text)
            except:
                pass  # Continue without audio if TTS fails
    
    def handle_command(self, command):
        """Handle a text command"""
        try:
            print(f"Processing command: {command}")
            response = self.processor.process_command(command)
            if response:
                self.simulate_speech(response)
            else:
                self.simulate_speech("I didn't understand that command.")
                
        except Exception as e:
            print(f"Error handling command: {e}")
            self.simulate_speech("Sorry, I encountered an error processing your command.")
    
    def start_demo(self):
        """Start the demo mode"""
        print("=" * 60)
        print("🎤 VOICE ASSISTANT DEMO MODE")
        print("=" * 60)
        print("Available commands:")
        print("- 'what time is it' - Get current time")
        print("- 'what date is it' - Get current date") 
        print("- 'search wikipedia for [topic]' - Wikipedia search")
        print("- 'open [website]' - Open websites")
        print("- 'hello' - Greeting")
        print("- 'help' - Show available commands")
        print("- 'exit' - Stop the demo")
        print("=" * 60)
        
        self.simulate_speech("Hello! I'm your voice assistant. Type your commands below.")
        
        self.running = True
        
        while self.running:
            try:
                # Get text input instead of voice
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'goodbye', 'stop']:
                    self.simulate_speech("Goodbye! Thanks for trying the voice assistant demo!")
                    self.running = False
                    break
                
                # Process the command
                self.handle_command(user_input)
                
            except KeyboardInterrupt:
                print("\n\nShutting down demo...")
                self.simulate_speech("Goodbye!")
                self.running = False
                break
            except Exception as e:
                print(f"Error in demo: {e}")

def main():
    """Main function to run the demo"""
    demo = DemoVoiceAssistant()
    demo.start_demo()

if __name__ == "__main__":
    main()