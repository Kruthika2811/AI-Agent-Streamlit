"""
Text-to-Speech Handler Module
Handles text-to-speech functionality using pyttsx3
"""

import pyttsx3
import threading
import queue

class TTSHandler:
    def __init__(self):
        """Initialize the text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()
            self.setup_voice()
            self.speech_queue = queue.Queue()
            self.is_speaking = False
            
        except Exception as e:
            print(f"Error initializing TTS engine: {e}")
            raise
    
    def setup_voice(self):
        """Configure voice properties"""
        try:
            # Get available voices
            voices = self.engine.getProperty('voices')
            
            # Set voice (prefer female voice if available)
            if voices:
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    # If no female voice found, use the first available
                    self.engine.setProperty('voice', voices[0].id)
            
            # Set speech rate (words per minute)
            self.engine.setProperty('rate', 180)
            
            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', 0.9)
            
            print("TTS voice configured successfully")
            
        except Exception as e:
            print(f"Error configuring voice: {e}")
    
    def speak(self, text):
        """
        Convert text to speech
        
        Args:
            text: Text string to convert to speech
        """
        if not text or not text.strip():
            return
            
        try:
            # Create a thread for speaking to avoid blocking
            speech_thread = threading.Thread(target=self._speak_threaded, args=(text,))
            speech_thread.daemon = True
            speech_thread.start()
            
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
    
    def _speak_threaded(self, text):
        """Internal method to handle speech in a separate thread"""
        try:
            self.is_speaking = True
            print(f"Speaking: {text}")
            
            self.engine.say(text)
            self.engine.runAndWait()
            
            self.is_speaking = False
            
        except Exception as e:
            print(f"Error in threaded speech: {e}")
            self.is_speaking = False
    
    def stop(self):
        """Stop current speech"""
        try:
            self.engine.stop()
            self.is_speaking = False
        except Exception as e:
            print(f"Error stopping speech: {e}")
    
    def is_busy(self):
        """Check if TTS engine is currently speaking"""
        return self.is_speaking
    
    def get_voices(self):
        """Get list of available voices"""
        try:
            voices = self.engine.getProperty('voices')
            voice_list = []
            for voice in voices:
                voice_info = {
                    'id': voice.id,
                    'name': voice.name,
                    'age': getattr(voice, 'age', 'Unknown'),
                    'gender': getattr(voice, 'gender', 'Unknown')
                }
                voice_list.append(voice_info)
            return voice_list
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    def set_voice_by_index(self, index):
        """Set voice by index from available voices"""
        try:
            voices = self.engine.getProperty('voices')
            if 0 <= index < len(voices):
                self.engine.setProperty('voice', voices[index].id)
                return True
            return False
        except Exception as e:
            print(f"Error setting voice: {e}")
            return False
