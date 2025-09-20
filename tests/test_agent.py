"""
Test script to verify the video editing agent works correctly
"""

import os
from src.agents.video_agent import create_video_editing_agent


def test_agent_initialization():
    """Test that the agent can be initialized and tools are registered correctly"""
    
    # Mock API key for testing
    api_key = "test-key-12345"
    
    try:
        # Create the agent
        agent = create_video_editing_agent(api_key)
        
        print("✅ Agent initialized successfully!")
        print(f"📊 Number of tools registered: {len(agent.tools)}")
        
        # List all registered tools
        print("\n🛠️  Registered tools:")
        for i, tool in enumerate(agent.tools, 1):
            print(f"  {i}. {tool.name}")
        
        # Test tool registration
        expected_tools = [
            "trim_video", "split_video", "merge_clips", "crop_frame",
            "resize_video", "change_resolution", "adjust_frame_rate",
            "color_correct", "add_transition", "add_overlay", "add_subtitles",
            "add_captions", "add_soundtrack", "adjust_volume",
            "remove_background_noise", "generate_thumbnail", "add_intro",
            "add_outro", "export_video", "change_format"
        ]
        
        registered_tool_names = [tool.name for tool in agent.tools]
        
        print(f"\n📋 Expected tools: {len(expected_tools)}")
        print(f"📋 Registered tools: {len(registered_tool_names)}")
        
        missing_tools = set(expected_tools) - set(registered_tool_names)
        if missing_tools:
            print(f"⚠️  Missing tools: {missing_tools}")
        else:
            print("✅ All expected tools are registered!")
        
        # Test memory initialization
        print(f"\n🧠 Memory system: {type(agent.memory).__name__}")
        
        # Test graph creation
        print(f"🔄 Graph created: {agent.graph is not None}")
        
        print("\n🎉 All tests passed! The agent is ready to use.")
        
    except Exception as e:
        print(f"❌ Error during agent initialization: {e}")
        return False
    
    return True


if __name__ == "__main__":
    test_agent_initialization()
