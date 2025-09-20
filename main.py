"""
Video Editing Agent - Main Interface
"""

import os
import sys
from typing import Optional
from src.agents.video_agent import create_video_editing_agent


def get_openai_api_key() -> str:
    """Get OpenAI API key from environment or user input"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("OpenAI API key not found in environment variables.")
        api_key = input("Please enter your OpenAI API key: ").strip()
        
        if not api_key:
            print("API key is required to run the video editing agent.")
            sys.exit(1)
    
    return api_key


def get_langsmith_config() -> tuple[str, str]:
    """Get LangSmith API key and project from environment or user input"""
    api_key = os.getenv("LANGSMITH_API_KEY")
    project = os.getenv("LANGSMITH_PROJECT", "video-editing-agent")
    
    if not api_key:
        print("\n🔍 LangSmith tracing is optional but recommended for monitoring.")
        enable_tracing = input("Would you like to enable LangSmith tracing? (y/n): ").strip().lower()
        
        if enable_tracing in ['y', 'yes']:
            api_key = input("Please enter your LangSmith API key: ").strip()
            if api_key:
                custom_project = input(f"Enter project name (default: {project}): ").strip()
                if custom_project:
                    project = custom_project
            else:
                print("⚠️  No API key provided. Tracing will be disabled.")
                api_key = None
        else:
            print("📊 LangSmith tracing disabled.")
            api_key = None
    
    return api_key, project


def print_welcome():
    """Print welcome message and instructions"""
    print("=" * 60)
    print("🎬 VIDEO EDITING AGENT")
    print("=" * 60)
    print("Welcome to the AI-powered video editing assistant!")
    print("\nThis agent can help you with various video editing tasks:")
    print("• Trim, split, and merge videos")
    print("• Crop, resize, and change resolution")
    print("• Add transitions, overlays, and effects")
    print("• Add subtitles, captions, and soundtracks")
    print("• Color correction and audio adjustments")
    print("• Export and format conversion")
    print("\nJust describe what you want to do in plain text!")
    print("=" * 60)


def print_help():
    """Print help information"""
    print("\n📖 HELP - Available Commands:")
    print("• Type your video editing request in plain text")
    print("• Example: 'Trim my video from 10 seconds to 30 seconds'")
    print("• Example: 'Add a fade transition between two clips'")
    print("• Example: 'Resize my video to 1920x1080'")
    print("• You'll be prompted to enter a video URI for each request")
    print("• Type 'help' to see this message again")
    print("• Type 'history' to see conversation history")
    print("• Type 'quit' or 'exit' to stop")
    print("• Type 'clear' to clear the conversation")


def print_history(agent, thread_id: str):
    """Print conversation history"""
    history = agent.get_conversation_history(thread_id)
    
    if not history:
        print("No conversation history found.")
        return
    
    print(f"\n📜 CONVERSATION HISTORY (Thread: {thread_id}):")
    print("-" * 50)
    
    for i, msg in enumerate(history, 1):
        msg_type = "👤 You" if msg["type"] == "human" else "🤖 Agent"
        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
        print(f"{i}. {msg_type}: {content}")


def main():
    """Main function to run the video editing agent"""
    print_welcome()
    
    # Get API keys and configuration
    try:
        api_key = get_openai_api_key()
        langsmith_key, langsmith_project = get_langsmith_config()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    
    # Create the agent
    try:
        print("\n🚀 Initializing video editing agent...")
        agent = create_video_editing_agent(
            openai_api_key=api_key,
            langsmith_api_key=langsmith_key,
            langsmith_project=langsmith_project
        )
        print("✅ Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        sys.exit(1)
    
    # Main interaction loop
    thread_id = "main_session"
    print_help()
    
    while True:
        try:
            print("\n" + "-" * 40)
            user_input = input("🎬 Your request: ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif user_input.lower() == 'history':
                print_history(agent, thread_id)
                continue
            elif user_input.lower() == 'clear':
                # Create a new thread for fresh conversation
                thread_id = f"session_{len(thread_id)}"
                print("🧹 Conversation cleared. Starting fresh session.")
                continue
            
            # Process the video editing request
            print("\n🔄 Processing your request...")
            
            # Get video URI from user or use default
            video_uri = input("📹 Enter video URI (or press Enter for demo video): ").strip()
            if not video_uri:
                video_uri = "s3://demo-bucket/input/video.mp4"
                print(f"   Using demo video: {video_uri}")
            else:
                print(f"   Using video: {video_uri}")
            
            result = agent.process_request(
                user_input=user_input,
                video_uri=video_uri,
                thread_id=thread_id
            )
            
            if result["success"]:
                print("\n✅ Response:")
                print(result["final_output"])
            else:
                print("\n❌ Error processing request")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or type 'help' for assistance.")


if __name__ == "__main__":
    main()
