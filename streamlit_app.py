import streamlit as st
import datetime
from voice_assistant.command_processor import CommandProcessor

# Configure Streamlit page
st.set_page_config(
    page_title="Voice Assistant",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize the command processor
@st.cache_resource
def get_command_processor():
    # For Streamlit, we don't need TTS, so we pass None
    return CommandProcessor(tts_handler=None)

def main():
    st.title("🎤 Voice Assistant")
    st.markdown("*Your AI-powered assistant for time, Wikipedia searches, and web browsing*")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize command processor
    processor = get_command_processor()

    # Quick command buttons
    st.markdown("### Quick Commands")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⏰ What time is it?"):
            st.session_state.current_command = "what time is it"
    with col2:
        if st.button("📅 What date is it?"):
            st.session_state.current_command = "what date is it"
    with col3:
        if st.button("🌐 Open Google"):
            st.session_state.current_command = "open google"
    with col4:
        if st.button("❓ Help"):
            st.session_state.current_command = "help"
    
    # Additional quick commands
    st.markdown("### Popular Searches")
    col5, col6, col7 = st.columns(3)
    
    with col5:
        if st.button("🐍 Python Info"):
            st.session_state.current_command = "search wikipedia for python programming"
    with col6:
        if st.button("🤖 AI Info"):
            st.session_state.current_command = "search wikipedia for artificial intelligence"
    with col7:
        if st.button("🌍 Space Info"):
            st.session_state.current_command = "search wikipedia for space exploration"

    # Process quick command if one was clicked
    if hasattr(st.session_state, 'current_command'):
        command = st.session_state.current_command
        
        # Add user message
        st.session_state.messages.append({
            "role": "user", 
            "content": command,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })
        
        # Process command
        with st.spinner("Processing..."):
            response = processor.process_command(command)
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })
        
        # Clear the current command
        del st.session_state.current_command
        st.rerun()

    # Chat input
    st.markdown("### Chat")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                content = message["content"]
                
                # Make URLs clickable in Streamlit
                import re
                url_pattern = r'(https?://[^\s]+)'
                if re.search(url_pattern, content):
                    # Replace URLs with markdown links
                    content = re.sub(url_pattern, r'[\1](\1)', content)
                
                st.markdown(content)
                st.caption(f"*{message['timestamp']}*")

    # Chat input box
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })
        
        # Process command
        with st.spinner("Processing..."):
            response = processor.process_command(prompt)
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })
        
        st.rerun()

    # Sidebar with information
    with st.sidebar:
        st.markdown("### About")
        st.info("""
        This Voice Assistant can:
        - Tell you the current time and date
        - Search Wikipedia for any topic
        - Open websites with clickable links
        - Handle natural conversation
        """)
        
        st.markdown("### Examples")
        st.code("""
        • "What time is it?"
        • "Search Wikipedia for cats"
        • "Open YouTube"
        • "Tell me about space"
        • "What date is it?"
        """)
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()