"""
Example usage of the Video Editing Agent
"""

import os
from src.agents.video_agent import create_video_editing_agent


def example_usage():
    """Example of how to use the video editing agent with LangSmith tracing"""
    
    # Set your API keys (or set environment variables)
    api_key = os.getenv("OPENAI_API_KEY")
    langsmith_key = os.getenv("LANGSMITH_API_KEY")
    langsmith_project = os.getenv("LANGSMITH_PROJECT", "video-editing-examples")
    
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return
    
    # Create the agent with LangSmith tracing
    agent = create_video_editing_agent(
        openai_api_key=api_key,
        langsmith_api_key=langsmith_key,
        langsmith_project=langsmith_project
    )
    
    # Example 1: Simple video trimming
    print("Example 1: Trimming a video")
    print("   Video URI: s3://demo-bucket/input/video.mp4")
    result1 = agent.process_request(
        user_input="Trim my video from 10 seconds to 30 seconds",
        video_uri="s3://demo-bucket/input/video.mp4",
        thread_id="example_1"
    )
    print(f"Result: {result1['final_output']}\n")
    
    # Example 2: Multiple operations
    print("Example 2: Multiple operations - trim and resize")
    print("   Video URI: s3://demo-bucket/input/video.mp4")
    result2 = agent.process_request(
        user_input="First trim my video from 5 to 25 seconds, then resize it to 1920x1080",
        video_uri="s3://demo-bucket/input/video.mp4",
        thread_id="example_2"
    )
    print(f"Result: {result2['final_output']}\n")
    
    # Example 3: Adding effects
    print("Example 3: Adding color correction and soundtrack")
    print("   Video URI: s3://demo-bucket/input/video.mp4")
    result3 = agent.process_request(
        user_input="Apply color correction with brightness 1.2 and contrast 1.1, then add a soundtrack",
        video_uri="s3://demo-bucket/input/video.mp4",
        thread_id="example_3"
    )
    print(f"Result: {result3['final_output']}\n")
    
    # Example 4: Complex workflow
    print("Example 4: Complex workflow - split, merge with transition")
    print("   Video URI: s3://demo-bucket/input/video.mp4")
    result4 = agent.process_request(
        user_input="Split my video at 15 seconds, then merge the two parts with a fade transition of 2 seconds",
        video_uri="s3://demo-bucket/input/video.mp4",
        thread_id="example_4"
    )
    print(f"Result: {result4['final_output']}\n")


if __name__ == "__main__":
    example_usage()
