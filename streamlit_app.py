import streamlit as st
import requests
from datetime import datetime
import json
import uuid

# Page config
st.set_page_config(
    page_title="Nikoo AI Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "threads" not in st.session_state:
    st.session_state.threads = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "current_thread" not in st.session_state:
    st.session_state.current_thread = None
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False
if "message_input" not in st.session_state:
    st.session_state.message_input = ""

# Custom CSS for better chat UI
st.markdown("""
<style>
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        max-width: 70%;
        float: right;
        clear: both;
        word-wrap: break-word;
    }
    .assistant-message {
        background-color: #e9ecef;
        color: #212529;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        max-width: 70%;
        float: left;
        clear: both;
        word-wrap: break-word;
    }
    .message-container {
        overflow-y: auto;
        height: 500px;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .typing-indicator {
        background-color: #e9ecef;
        color: #6c757d;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        max-width: 100px;
        float: left;
        clear: both;
        font-style: italic;
        animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("💬 Nikoo AI Assistant")
st.markdown("---")

# Sidebar for user management
with st.sidebar:
    st.header("👤 User Settings")
    
    # User ID input
    user_id = st.text_input(
        "Enter User ID:",
        value=st.session_state.user_id,
        placeholder="e.g., user_123"
    )
    
    if user_id:
        st.session_state.user_id = user_id
    
    if st.session_state.user_id:
        st.success(f"✅ Logged in as: {st.session_state.user_id}")
        
        st.markdown("---")
        st.header("📚 Threads")
        
        # Load threads button
        if st.button("🔄 Load Threads", use_container_width=True):
            try:
                response = requests.get(f"{API_BASE_URL}/api/threads/{st.session_state.user_id}")
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.threads = data.get("threads", [])
                    st.success(f"✅ Loaded {len(st.session_state.threads)} threads")
                else:
                    st.error("Failed to load threads")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        # New chat button
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            new_thread_id = str(uuid.uuid4())
            st.session_state.thread_id = new_thread_id
            st.session_state.current_thread = {
                "thread_id": new_thread_id,
                "title": "New Chat",
                "message_count": 0,
                "created_at": datetime.now().isoformat()
            }
            st.session_state.chat_messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Display threads
        if st.session_state.threads:
            st.subheader(f"Your Threads ({len(st.session_state.threads)})")
            
            for thread in st.session_state.threads:
                is_active = st.session_state.thread_id == thread['thread_id']
                
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Thread title with active indicator
                    thread_title = thread.get("title", "Untitled")[:40]
                    button_label = f"{'🟢 ' if is_active else ''}💬 {thread_title}"
                    
                    if st.button(
                        button_label,
                        key=f"thread_{thread['thread_id']}",
                        use_container_width=True,
                        type="primary" if is_active else "secondary"
                    ):
                        st.session_state.thread_id = thread["thread_id"]
                        st.session_state.current_thread = thread
                        st.session_state.chat_messages = []
                        
                        # Load messages from thread
                        try:
                            response = requests.get(
                                f"{API_BASE_URL}/api/threads/{thread['thread_id']}/{st.session_state.user_id}/messages"
                            )
                            if response.status_code == 200:
                                data = response.json()
                                st.session_state.chat_messages = data.get("messages", [])
                        except:
                            pass
                        
                        st.rerun()
                
                with col2:
                    # Delete button
                    if st.button(
                        "🗑️",
                        key=f"delete_{thread['thread_id']}",
                        help="Delete thread"
                    ):
                        try:
                            response = requests.delete(
                                f"{API_BASE_URL}/api/threads/{thread['thread_id']}/{st.session_state.user_id}"
                            )
                            if response.status_code == 200:
                                st.success("✅ Thread deleted")
                                st.session_state.threads = [
                                    t for t in st.session_state.threads 
                                    if t["thread_id"] != thread["thread_id"]
                                ]
                                if st.session_state.thread_id == thread["thread_id"]:
                                    st.session_state.thread_id = None
                                    st.session_state.current_thread = None
                                    st.session_state.chat_messages = []
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                # Show message count
                st.caption(f"📊 {thread.get('message_count', 0)} messages")
    
    else:
        st.warning("⚠️ Please enter a User ID to continue")

# Main chat area
if st.session_state.user_id and st.session_state.thread_id:
    # Current thread info
    if st.session_state.current_thread:
        thread = st.session_state.current_thread
        
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.subheader(f"📖 {thread.get('title', 'Chat')}")
        with col2:
            st.caption(f"💬 {len(st.session_state.chat_messages)} messages")
        with col3:
            if st.button("🔄 Refresh", key="refresh_chat"):
                # Reload messages
                try:
                    response = requests.get(
                        f"{API_BASE_URL}/api/threads/{st.session_state.thread_id}/{st.session_state.user_id}/messages"
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.chat_messages = data.get("messages", [])
                        st.rerun()
                except:
                    pass
        
        st.markdown("---")
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        if st.session_state.chat_messages:
            for i, msg in enumerate(st.session_state.chat_messages):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                timestamp = msg.get("created_at", "")
                
                if role == "user":
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col3:
                        st.markdown(f"""
                        <div style="text-align: right;">
                            <div class="user-message">
                                {content}
                            </div>
                            <small style="color: #888;">{timestamp[:16] if timestamp else ''}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("")  # Add spacing
                
                elif role == "assistant":
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col1:
                        st.markdown(f"""
                        <div style="text-align: left;">
                            <div class="assistant-message">
                                <strong>🤖 AI:</strong><br>
                                {content}
                            </div>
                            <small style="color: #888;">{timestamp[:16] if timestamp else ''}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("")  # Add spacing
        
        else:
            st.info("👋 Start a conversation! Type your message below.")
        
        # Typing indicator
        if st.session_state.is_typing:
            st.markdown("""
            <div class="typing-indicator">
                💭 AI is typing...
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Message input area
    with st.container():
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_message = st.text_area(
                "Type your message:",
                value=st.session_state.message_input,
                height=100,
                placeholder="Type your message here...",
                key="message_text_area",
                label_visibility="collapsed"
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            send_button = st.button("📤 Send", use_container_width=True, type="primary")
    
    # Send message using REST API (WebSocket can be added later for real-time)
    if send_button and user_message.strip():
        try:
            # Show typing indicator
            st.session_state.is_typing = True
            
            # Add user message to chat immediately
            user_msg = {
                "role": "user",
                "content": user_message,
                "created_at": datetime.now().isoformat()
            }
            st.session_state.chat_messages.append(user_msg)
            
            # Clear input
            st.session_state.message_input = ""
            
            # Send to API
            payload = {
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            }
            
            response = requests.post(
                f"{API_BASE_URL}/api/threads/{st.session_state.thread_id}/{st.session_state.user_id}/messages",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                
                # Add AI response to chat
                ai_msg = {
                    "role": "assistant",
                    "content": ai_response,
                    "created_at": datetime.now().isoformat()
                }
                st.session_state.chat_messages.append(ai_msg)
                
                # Update thread message count
                if st.session_state.current_thread:
                    st.session_state.current_thread["message_count"] = len(st.session_state.chat_messages)
                
                st.session_state.is_typing = False
                st.rerun()
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                st.session_state.is_typing = False
        
        except Exception as e:
            st.error(f"Error sending message: {str(e)}")
            st.session_state.is_typing = False

elif st.session_state.user_id:
    # No thread selected
    st.info("👈 Select a thread from the sidebar or click 'New Chat' to start!")
    
    st.markdown("### ✨ Welcome to Nikoo AI Assistant")
    st.markdown("""
    **Features:**
    - 💬 Continuous chat conversations
    - 🧵 Multiple thread support
    - 📝 Message history
    - 🤖 AI-powered responses
    - 🔄 Real-time updates
    
    **Get Started:**
    1. Click "➕ New Chat" in the sidebar
    2. Start typing your message
    3. Click "📤 Send" to get AI response
    """)

else:
    st.warning("⚠️ Please enter a User ID in the sidebar to continue")
    st.markdown("### 👋 Welcome!")
    st.markdown("Enter your User ID in the sidebar to start chatting with Nikoo AI Assistant.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>Nikoo AI Assistant • Powered by Groq API • Real-time Chat</small>
</div>
""", unsafe_allow_html=True)
