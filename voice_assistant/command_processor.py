"""
Command Processor Module
Handles parsing and execution of voice commands
"""

import datetime
import webbrowser
import wikipedia
import re
import os

class CommandProcessor:
    def __init__(self, tts_handler):
        """
        Initialize the command processor
        
        Args:
            tts_handler: TTS handler instance for speaking responses
        """
        self.tts = tts_handler
        
        # Command patterns and their handlers
        self.command_patterns = {
            'time': [r'what time is it', r'tell me the time', r'current time', r'time'],
            'date': [r'what date is it', r'tell me the date', r'current date', r'date', r'what day is it'],
            'wikipedia': [r'search wikipedia for (.+)', r'wikipedia (.+)', r'look up (.+)', r'tell me about (.+)'],
            'web': [r'open (.+)', r'go to (.+)', r'browse (.+)', r'visit (.+)'],
            'greeting': [r'hello', r'hi', r'hey', r'good morning', r'good afternoon', r'good evening'],
            'help': [r'help', r'what can you do', r'commands', r'assistance'],
            'weather': [r'weather', r'temperature', r'forecast'],
        }
    
    def process_command(self, command):
        """
        Process a voice command and return appropriate response
        
        Args:
            command: Voice command string to process
            
        Returns:
            Response string to be spoken
        """
        if not command:
            return "I didn't hear anything."
        
        command = command.lower().strip()
        print(f"Processing command: {command}")
        
        try:
            # Check each command pattern
            for command_type, patterns in self.command_patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, command)
                    if match:
                        return self._execute_command(command_type, match, command)
            
            # If no pattern matches, try to be helpful
            return self._handle_unknown_command(command)
            
        except Exception as e:
            print(f"Error processing command: {e}")
            return "Sorry, I encountered an error processing your command."
    
    def _execute_command(self, command_type, match, original_command):
        """Execute a specific command type"""
        try:
            if command_type == 'time':
                return self._get_time()
            
            elif command_type == 'date':
                return self._get_date()
            
            elif command_type == 'wikipedia':
                query = match.group(1) if match.groups() else original_command.replace('wikipedia', '').strip()
                return self._search_wikipedia(query)
            
            elif command_type == 'web':
                website = match.group(1) if match.groups() else original_command.replace('open', '').strip()
                return self._open_website(website)
            
            elif command_type == 'greeting':
                return self._handle_greeting()
            
            elif command_type == 'help':
                return self._get_help()
            
            elif command_type == 'weather':
                return "I don't have access to weather data yet, but I can help you with time, Wikipedia searches, and opening websites."
            
            else:
                return "I'm not sure how to handle that command."
                
        except Exception as e:
            print(f"Error executing command {command_type}: {e}")
            return f"Sorry, I had trouble with that {command_type} request."
    
    def _get_time(self):
        """Get current time"""
        try:
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p")
            return f"The current time is {time_str}"
        except Exception as e:
            print(f"Error getting time: {e}")
            return "Sorry, I couldn't get the current time."
    
    def _get_date(self):
        """Get current date"""
        try:
            now = datetime.datetime.now()
            date_str = now.strftime("%A, %B %d, %Y")
            return f"Today is {date_str}"
        except Exception as e:
            print(f"Error getting date: {e}")
            return "Sorry, I couldn't get the current date."
    
    def _search_wikipedia(self, query):
        """Search Wikipedia for information"""
        if not query or query.strip() == "":
            return "What would you like me to search for on Wikipedia?"
        
        try:
            print(f"Searching Wikipedia for: {query}")
            
            # Set language to English
            wikipedia.set_lang("en")
            
            # First try direct search
            try:
                summary = wikipedia.summary(query, sentences=2)
                if summary:
                    return f"According to Wikipedia: {summary}"
            except wikipedia.exceptions.PageError:
                # If direct search fails, try searching for similar topics
                search_results = wikipedia.search(query, results=3)
                if search_results:
                    # Try the first search result
                    summary = wikipedia.summary(search_results[0], sentences=2)
                    return f"According to Wikipedia: {summary}"
            
            return f"I couldn't find information about {query} on Wikipedia."
                
        except wikipedia.exceptions.DisambiguationError as e:
            # If there are multiple options, pick the first one
            try:
                summary = wikipedia.summary(e.options[0], sentences=2)
                return f"I found multiple results. Here's information about {e.options[0]}: {summary}"
            except:
                return f"I found multiple results for {query}. Could you be more specific?"
        
        except wikipedia.exceptions.PageError:
            return f"I couldn't find a Wikipedia page for {query}. Try rephrasing your search."
        
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return f"Sorry, I had trouble searching Wikipedia for {query}."
    
    def _open_website(self, website):
        """Open a website in the default browser"""
        if not website or website.strip() == "":
            return "Which website would you like me to open?"
        
        try:
            # Clean up the website name
            website = website.strip().lower()
            
            # Add common website mappings
            website_mappings = {
                'google': 'https://www.google.com',
                'youtube': 'https://www.youtube.com',
                'facebook': 'https://www.facebook.com',
                'twitter': 'https://www.twitter.com',
                'instagram': 'https://www.instagram.com',
                'linkedin': 'https://www.linkedin.com',
                'github': 'https://www.github.com',
                'reddit': 'https://www.reddit.com',
                'amazon': 'https://www.amazon.com',
                'wikipedia': 'https://www.wikipedia.org',
                'stack overflow': 'https://stackoverflow.com',
                'gmail': 'https://mail.google.com',
            }
            
            # Check if it's a mapped website
            if website in website_mappings:
                url = website_mappings[website]
            else:
                # Try to construct URL
                if not website.startswith(('http://', 'https://')):
                    if '.' in website:
                        url = f"https://{website}"
                    else:
                        url = f"https://www.{website}.com"
                else:
                    url = website
            
            print(f"Opening website: {url}")
            # Note: webbrowser.open() only works in desktop environments
            # For web interface, we'll return the URL so the frontend can handle it
            webbrowser.open(url)
            
            return f"Opening {website}: {url}"
            
        except Exception as e:
            print(f"Error opening website: {e}")
            return f"Sorry, I couldn't open {website}."
    
    def _handle_greeting(self):
        """Handle greeting commands"""
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What would you like to know?",
            "Hey! I'm here to assist you.",
            "Good to hear from you! What can I do for you?"
        ]
        
        import random
        return random.choice(greetings)
    
    def _get_help(self):
        """Provide help information"""
        help_text = """I can help you with several things:
        - Tell you the current time by saying 'what time is it'
        - Tell you the current date by saying 'what date is it'
        - Search Wikipedia by saying 'search wikipedia for' followed by your topic
        - Open websites by saying 'open' followed by the website name
        - Just say 'hello assistant' to wake me up anytime
        """
        return help_text
    
    def _handle_unknown_command(self, command):
        """Handle unknown commands with helpful suggestions"""
        suggestions = [
            "I'm not sure what you mean. Try asking me for the time, searching Wikipedia, or opening a website.",
            "I didn't understand that. I can tell you the time, search Wikipedia, or open websites for you.",
            "Sorry, I don't know how to do that yet. Ask me about the time, Wikipedia, or websites.",
        ]
        
        import random
        return random.choice(suggestions)
