#!/usr/bin/env python3
"""
Main entry point for the Python Voice Assistant
"""

import sys
import time
import threading
from voice_assistant.speech_handler import SpeechHandler
from voice_assistant.command_processor import CommandProcessor
from voice_assistant.tts_handler import TTSHandler
from config import Config

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant with all necessary components"""
        print("Initializing Voice Assistant...")
        
        try:
            self.tts = TTSHandler()
            self.speech = SpeechHandler()
            self.processor = CommandProcessor(self.tts)
            self.running = False
            
            print("Voice Assistant initialized successfully!")
            self.tts.speak("Voice Assistant is ready. Say 'hello assistant' to wake me up.")
            
        except Exception as e:
            print(f"Error initializing Voice Assistant: {e}")
            sys.exit(1)
    
    def listen_for_wake_word(self):
        """Listen for the wake word to activate the assistant"""
        wake_words = Config.WAKE_WORDS
        
        while self.running:
            try:
                print("Listening for wake word...")
                audio = self.speech.listen(timeout=1, phrase_time_limit=3)
                
                if audio:
                    text = self.speech.recognize(audio)
                    if text:
                        text_lower = text.lower()
                        print(f"Heard: {text}")
                        
                        # Check for wake words
                        for wake_word in wake_words:
                            if wake_word in text_lower:
                                print("Wake word detected!")
                                self.tts.speak("Yes, how can I help you?")
                                self.handle_command()
                                break
                        
                        # Check for exit commands
                        if any(exit_word in text_lower for exit_word in Config.EXIT_COMMANDS):
                            self.tts.speak("Goodbye!")
                            self.stop()
                            break
                            
            except KeyboardInterrupt:
                print("\nShutting down...")
                self.stop()
                break
            except Exception as e:
                print(f"Error in wake word detection: {e}")
                time.sleep(1)
    
    def handle_command(self):
        """Handle a command after wake word is detected"""
        try:
            print("Listening for command...")
            audio = self.speech.listen(timeout=5, phrase_time_limit=5)
            
            if audio:
                command = self.speech.recognize(audio)
                if command:
                    print(f"Command received: {command}")
                    response = self.processor.process_command(command)
                    if response:
                        self.tts.speak(response)
                else:
                    self.tts.speak("I didn't catch that. Could you repeat?")
            else:
                self.tts.speak("I didn't hear anything. Try again.")
                
        except Exception as e:
            print(f"Error handling command: {e}")
            self.tts.speak("Sorry, I encountered an error processing your command.")
    
    def start(self):
        """Start the voice assistant"""
        print("Starting Voice Assistant...")
        self.running = True
        
        try:
            self.listen_for_wake_word()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the voice assistant"""
        self.running = False
        print("Voice Assistant stopped.")

def main():
    """Main function to run the voice assistant"""
    print("=" * 50)
    print("Python Voice Assistant")
    print("=" * 50)
    print("Commands:")
    print("- 'hello assistant' or 'hey assistant' to wake up")
    print("- 'what time is it' for current time")
    print("- 'search wikipedia for [topic]' for Wikipedia search")
    print("- 'open [website]' to open websites")
    print("- 'exit' or 'quit' to stop")
    print("=" * 50)
    
    assistant = VoiceAssistant()
    assistant.start()

if __name__ == "__main__":
    main()
