import asyncio
import websockets
import json
import uuid

# Configuration
WEBSOCKET_URL = "ws://localhost:8000/ws/chat"
TEST_THREAD_ID = str(uuid.uuid4())
TEST_USER_ID = "test_user_123"

async def test_websocket():
    """Test WebSocket chat endpoint"""
    uri = f"{WEBSOCKET_URL}/{TEST_THREAD_ID}/{TEST_USER_ID}"
    
    print(f"Connecting to: {uri}")
    print(f"Thread ID: {TEST_THREAD_ID}")
    print(f"User ID: {TEST_USER_ID}\n")
    
    try:
        # Increase ping settings to be tolerant during long model generations
        async with websockets.connect(uri, ping_interval=40, ping_timeout=40) as websocket:
            print("✓ WebSocket connection established")
            
            # Receive connection confirmation
            connection_msg = await websocket.recv()
            connection_data = json.loads(connection_msg)
            print(f"✓ Connection confirmed: {connection_data}\n")
            
            # Test messages
            test_messages = [
                "Hello, how are you?",
                "My name is Nikoo.",
                "What's the weather like?",
                "Can you tell me my name?",
                "Tell me a joke"
            ]
            
            for idx, message in enumerate(test_messages, 1):
                print(f"[{idx}] Sending message: {message}")
                
                # Send message
                await websocket.send(json.dumps({
                    "type": "message",
                    "content": message,
                    "role": "user"
                }))
                
                # Receive responses
                while True:
                    response = await websocket.recv()
                    response_data = json.loads(response)
                    
                    if response_data.get("type") == "typing":
                        print("    ⋯ AI is typing...")
                    
                    elif response_data.get("type") == "response":
                        print(f"    ✓ Response: {response_data.get('content')[:100]}...")
                        print(f"    ✓ Success: {response_data.get('success')}\n")
                        break
                    
                    elif response_data.get("type") == "error":
                        print(f"    ✗ Error: {response_data.get('content')}\n")
                        break
            
            print("✓ All test messages sent and received successfully")
            
    except websockets.exceptions.WebSocketException as e:
        print(f"✗ WebSocket error: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("WebSocket Chat Test")
    print("=" * 60 + "\n")
    
    asyncio.run(test_websocket())
    
    print("\n" + "=" * 60)
    print("Test completed")
    print("=" * 60)
