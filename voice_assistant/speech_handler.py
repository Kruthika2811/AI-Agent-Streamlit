"""
Speech Handler Module
Handles speech recognition functionality
"""

import speech_recognition as sr
import threading
import time

class SpeechHandler:
    def __init__(self):
        """Initialize the speech recognition system"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Ambient noise adjustment complete.")
        
        # Configure recognition settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.operation_timeout = 2
    
    def listen(self, timeout=1, phrase_time_limit=None):
        """
        Listen for audio input from the microphone
        
        Args:
            timeout: Time to wait for speech to start
            phrase_time_limit: Maximum time to record speech
            
        Returns:
            AudioData object or None if no speech detected
        """
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                return audio
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"Error listening: {e}")
            return None
    
    def recognize(self, audio):
        """
        Convert audio to text using Google Speech Recognition
        
        Args:
            audio: AudioData object to recognize
            
        Returns:
            Recognized text string or None if recognition failed
        """
        if not audio:
            return None
            
        try:
            # Use Google Speech Recognition (free tier)
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None
    
    def test_microphone(self):
        """Test if microphone is working properly"""
        try:
            print("Testing microphone... Say something!")
            audio = self.listen(timeout=5, phrase_time_limit=3)
            if audio:
                text = self.recognize(audio)
                if text:
                    print(f"Microphone test successful! You said: {text}")
                    return True
                else:
                    print("Microphone detected audio but couldn't recognize speech")
                    return False
            else:
                print("No audio detected. Check your microphone.")
                return False
        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False
