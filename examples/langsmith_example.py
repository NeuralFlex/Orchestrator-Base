"""
LangSmith Tracing Example for Video Editing Agent

This example demonstrates how to use LangSmith tracing to monitor
and debug the video editing agent's execution.
"""

import os
from src.agents.video_agent import create_video_editing_agent


def setup_langsmith_tracing():
    """Setup LangSmith tracing configuration"""
    
    # Set environment variables for LangSmith
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    
    # You can set these via environment variables or pass them directly
    langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
    langsmith_project = os.getenv("LANGSMITH_PROJECT", "video-editing-agent")
    
    if not langsmith_api_key:
        print("⚠️  LANGSMITH_API_KEY not found in environment variables.")
        print("   Set it with: export LANGSMITH_API_KEY='your-api-key'")
        return None, None
    
    os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
    os.environ["LANGCHAIN_PROJECT"] = langsmith_project
    
    print(f"🔍 LangSmith tracing enabled for project: {langsmith_project}")
    return langsmith_api_key, langsmith_project


def run_traced_examples():
    """Run examples with LangSmith tracing enabled"""
    
    # Setup tracing
    langsmith_key, langsmith_project = setup_langsmith_tracing()
    
    if not langsmith_key:
        print("❌ Cannot run examples without LangSmith API key")
        return
    
    # Get OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return
    
    # Create agent with tracing
    print("\n🚀 Creating video editing agent with LangSmith tracing...")
    agent = create_video_editing_agent(
        openai_api_key=openai_key,
        langsmith_api_key=langsmith_key,
        langsmith_project=langsmith_project
    )
    
    # Example 1: Simple operation
    print("\n📹 Example 1: Simple video trimming")
    uri = "s3://demo-bucket/input/video.mp4"
    result1 = agent.process_request(
        user_input=f"Trim this {uri} video from 10 seconds to 30 seconds and change the format of the trimmed video to .mov",
        video_uri=uri,
        thread_id="example_1"
    )
    print(f"   Result: {result1['final_output']}")
    # print(f"   Result: {result1['messages']}")

    # print(f"   History: {agent.get_conversation_history(thread_id='example_1')}")
    
    
    # Example 2: Complex multi-step operation
    # print("\n🎬 Example 2: Complex multi-step video editing")
    # print("   This will show how the agent chains multiple tools together")
    
    result2 = agent.process_request(
        user_input="Now add this s3://demo-bucket/input/intro_video.mp4 intro video at the start of the trimmed video",
        video_uri="s3://demo-bucket/input/intro_video.mp4",
        thread_id="example_1"
    )
    print(f"   Result: {result2['final_output']}")
    
   


def view_traces_guide():
    """Print guide on how to view traces in LangSmith"""
    
    print("\n" + "="*60)
    print("📊 HOW TO VIEW TRACES IN LANGSMITH")
    print("="*60)
    
    print("\n1. 🌐 Open LangSmith Dashboard:")
    print("   https://smith.langchain.com")
    
    print("\n2. 📁 Navigate to your project:")
    print("   - Go to 'Projects' in the sidebar")
    print("   - Find your project (default: 'video-editing-agent')")
    print("   - Click on it to view all traces")
    
    print("\n3. 🔍 View individual traces:")
    print("   - Each trace shows the complete execution flow")
    print("   - You can see:")
    print("     • Input messages and user requests")
    print("     • Agent reasoning and decision making")
    print("     • Tool calls and their parameters")
    print("     • Tool outputs and results")
    print("     • Final responses")
    print("     • Execution time and performance metrics")
    
    print("\n4. 📈 Analyze performance:")
    print("   - View execution times for each step")
    print("   - Identify bottlenecks in tool calls")
    print("   - Monitor token usage and costs")
    print("   - Track success/failure rates")
    
    print("\n5. 🐛 Debug issues:")
    print("   - See exactly where errors occur")
    print("   - View intermediate states")
    print("   - Understand tool selection logic")
    print("   - Trace conversation flow")
    
    print("\n6. 🔄 Compare runs:")
    print("   - Compare different approaches")
    print("   - A/B test different prompts")
    print("   - Optimize tool selection")
    
    print("\n💡 Pro Tips:")
    print("   - Use descriptive thread_id values for easier filtering")
    print("   - Add custom metadata to traces for better organization")
    print("   - Set up alerts for failed executions")
    print("   - Export traces for offline analysis")


if __name__ == "__main__":
    print("🎬 LangSmith Tracing Example for Video Editing Agent")
    print("="*60)
    
    # Show guide first
    # view_traces_guide()
    
    # Ask if user wants to run examples
    print("\n" + "="*60)
    run_examples = input("Would you like to run the traced examples? (y/n): ").strip().lower()
    
    if run_examples in ['y', 'yes']:
        run_traced_examples()
    else:
        print("👋 Skipping examples. You can run them later with:")
        print("   uv run langsmith_example.py")
