#!/usr/bin/env python3
"""
Web interface for the Voice Assistant
Provides a clean web UI for text-based interaction
"""

from flask import Flask, render_template, request, jsonify
import json
from voice_assistant.command_processor import CommandProcessor
from voice_assistant.tts_handler import TTSHandler
import datetime

app = Flask(__name__)

class WebTTSHandler:
    """TTS handler for web interface - returns text instead of speaking"""
    def speak(self, text):
        return text

class WebVoiceAssistant:
    def __init__(self):
        """Initialize the web voice assistant"""
        try:
            self.tts = WebTTSHandler()
            self.processor = CommandProcessor(self.tts)
            self.conversation_history = []
        except Exception as e:
            print(f"Error initializing Web Voice Assistant: {e}")
            raise

    def process_message(self, user_input):
        """Process user input and return response"""
        if not user_input or not user_input.strip():
            return "Please say something!"
        
        try:
            # Add user message to history
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.conversation_history.append({
                'type': 'user',
                'message': user_input,
                'timestamp': timestamp
            })
            
            # Process the command
            response = self.processor.process_command(user_input)
            
            # Add assistant response to history
            self.conversation_history.append({
                'type': 'assistant',
                'message': response,
                'timestamp': timestamp
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.conversation_history.append({
                'type': 'assistant',
                'message': error_msg,
                'timestamp': timestamp
            })
            return error_msg

# Initialize the assistant
assistant = WebVoiceAssistant()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        response = assistant.process_message(user_input)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.datetime.now().strftime("%H:%M:%S")
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/history')
def history():
    """Get conversation history"""
    return jsonify({'history': assistant.conversation_history})

@app.route('/clear')
def clear_history():
    """Clear conversation history"""
    assistant.conversation_history = []
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)