# Overview

This is a Python Voice Assistant application that provides hands-free interaction through voice commands. The assistant listens for wake words, processes spoken commands, and responds using text-to-speech. It supports various functionalities including time/date queries, Wikipedia searches, web browsing, and basic conversational interactions.

**Recent Addition (August 2025):** Added a modern web interface that allows users to interact with the voice assistant through a chat-style web application, making it accessible without requiring microphone hardware.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Components

The application follows a modular architecture with clear separation of concerns:

**Main Controller (`main.py`)**
- Entry point that orchestrates all components
- Manages the main listening loop and wake word detection
- Handles application lifecycle and error recovery

**Web Interface (`web_app.py`)**
- Flask-based web application providing chat-style interface
- Real-time message processing with AJAX
- Mobile-responsive design with quick command buttons
- Conversation history and clear functionality

**Speech Recognition (`speech_handler.py`)**
- Uses the `speech_recognition` library for audio input processing
- Implements ambient noise adjustment for better accuracy
- Configurable timeout and phrase limits for responsive interaction

**Text-to-Speech (`tts_handler.py`)**
- Powered by `pyttsx3` for cross-platform speech synthesis
- Supports voice customization (prefers female voices)
- Implements queued speech processing to prevent overlapping audio

**Command Processing (`command_processor.py`)**
- Pattern-based command recognition using regular expressions
- Modular command handlers for different functionality types
- Extensible architecture for adding new command categories

**Configuration Management (`config.py`)**
- Centralized configuration for wake words, exit commands, and system settings
- Website shortcuts for easy voice-controlled web browsing
- Tunable parameters for speech recognition and TTS

## Design Patterns

**Command Pattern**: Each voice command type has dedicated handlers that can be easily extended or modified.

**Observer Pattern**: The main loop continuously listens for wake words and triggers appropriate responses.

**Configuration Pattern**: All system settings are externalized to a single configuration file for easy customization.

## Threading Model

The application uses threading to handle concurrent operations:
- Main thread manages the wake word listening loop
- TTS operations run in separate threads to prevent blocking
- Speech recognition operates synchronously within the main flow

# External Dependencies

## Core Libraries
- **speech_recognition**: Primary library for converting speech to text
- **pyttsx3**: Cross-platform text-to-speech synthesis engine
- **wikipedia**: API integration for knowledge queries and summaries

## System Dependencies
- **Microphone access**: Requires system microphone permissions
- **Audio output**: Needs functioning speakers or headphones for TTS
- **Internet connectivity**: Required for Wikipedia searches and web browsing commands

## Optional Integrations
- **Web browser**: Uses system default browser for web navigation commands
- **Operating system services**: Leverages OS-level audio and hardware interfaces

The application is designed to be lightweight and self-contained, with minimal external service dependencies beyond the core Python libraries.