"""
Configuration settings for the Voice Assistant
"""

class Config:
    # Wake words that activate the assistant
    WAKE_WORDS = [
        "hello assistant",
        "hey assistant", 
        "hi assistant",
        "wake up assistant",
        "assistant"
    ]
    
    # Commands to exit the application
    EXIT_COMMANDS = [
        "exit",
        "quit", 
        "goodbye",
        "stop assistant",
        "shut down",
        "turn off"
    ]
    
    # Speech recognition settings
    SPEECH_TIMEOUT = 1  # Time to wait for speech to start
    PHRASE_TIME_LIMIT = 5  # Maximum time to record speech
    
    # TTS settings
    TTS_RATE = 180  # Words per minute
    TTS_VOLUME = 0.9  # Volume level (0.0 to 1.0)
    
    # Wikipedia settings
    WIKIPEDIA_SENTENCES = 2  # Number of sentences in summary
    
    # Common website mappings for easier voice recognition
    WEBSITE_SHORTCUTS = {
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
        'gmail': 'https://mail.google.com',
    }
    
    # Error messages
    ERROR_MESSAGES = {
        'mic_error': "I'm having trouble accessing your microphone. Please check your audio settings.",
        'speech_error': "I couldn't understand what you said. Please try speaking more clearly.",
        'internet_error': "I need an internet connection for that feature.",
        'general_error': "Sorry, I encountered an unexpected error."
    }
    
    # Success messages
    SUCCESS_MESSAGES = {
        'startup': "Voice Assistant is ready. Say 'hello assistant' to wake me up.",
        'wake': "Yes, how can I help you?",
        'goodbye': "Goodbye! Have a great day!"
    }
