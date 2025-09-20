"""
Video Editing Agent using LangGraph ReAct Pattern
"""

import os
from typing import Dict, List, Any, Optional, Sequence, Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END, add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from src.tools import tools
import langsmith
from langsmith import traceable


class AgentState(TypedDict):
    """State for the video editing agent"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_video_uri: Optional[str]


class VideoEditingAgent:
    """Video Editing Agent using LangGraph ReAct pattern"""
    
    def __init__(self, openai_api_key: str = None, langsmith_api_key: str = None, 
                 langsmith_project: str = "video-editing-agent"):
        """Initialize the video editing agent"""
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly.")
        
        # Initialize LangSmith tracing
        self.langsmith_api_key = langsmith_api_key or os.getenv("LANGSMITH_API_KEY")
        self.langsmith_project = langsmith_project or os.getenv("LANGSMITH_PROJECT", "video-editing-agent")
        
        if self.langsmith_api_key:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
            os.environ["LANGCHAIN_API_KEY"] = self.langsmith_api_key
            os.environ["LANGCHAIN_PROJECT"] = self.langsmith_project
            print(f"🔍 LangSmith tracing enabled for project: {self.langsmith_project}")
        else:
            print("⚠️  LangSmith API key not provided. Tracing disabled.")
        
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=self.openai_api_key,
            temperature=0.2
        )

        # Memory for conversation history
        self.memory = MemorySaver()
        
        # Register all video editing tools
        self.tools = self._register_tools()
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Create tool node
        self.tool_node = ToolNode(self.tools)
        
        # Create the graph
        self.graph = self._create_graph()
        
    def _register_tools(self) -> List:
        """Register all video editing tools from tools.py"""
        registered_tools = []
        
        # Get all functions from tools module
        tool_functions = [
            tools.trim_video,
            tools.split_video,
            tools.merge_clips,
            tools.crop_frame,
            tools.resize_video,
            tools.change_resolution,
            tools.adjust_frame_rate,
            tools.color_correct,
            tools.add_transition,
            tools.add_overlay,
            tools.add_subtitles,
            tools.add_captions,
            tools.add_soundtrack,
            tools.adjust_volume,
            tools.remove_background_noise,
            tools.generate_thumbnail,
            tools.add_intro,
            tools.add_outro,
            tools.export_video,
            tools.change_format
        ]
        
        # Convert functions to LangChain tools
        for func in tool_functions:
            tool_wrapper = tool(func)
            registered_tools.append(tool_wrapper)
        
        return registered_tools
    
    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self._call_agent)
        workflow.add_node("tools", self.tool_node)  # ToolNode handles the state directly
        
        # Add edges
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )
        workflow.add_edge("tools", "agent")
        
        # Compile the graph with memory
        return workflow.compile(checkpointer=self.memory)
    
    def _create_system_message(self, video_uri: str) -> SystemMessage:
        """Create the system message with current video URI"""
        return SystemMessage(content=f"""
You are a professional video editing assistant. You can help users edit videos by calling various video editing tools.

CURRENT VIDEO URI: {video_uri}

Available tools:
- trim_video: Trim video between start and end times
- split_video: Split video into two clips at a specific time
- merge_clips: Merge two video clips sequentially
- crop_frame: Crop video frame to specific region
- resize_video: Resize video to target dimensions
- change_resolution: Change video resolution
- adjust_frame_rate: Adjust video frame rate
- color_correct: Apply color correction (brightness, contrast, saturation)
- add_transition: Add transition effects between clips
- add_overlay: Overlay image on video
- add_subtitles: Add subtitle file to video
- add_captions: Add custom text captions
- add_soundtrack: Add audio soundtrack
- adjust_volume: Adjust video audio volume
- remove_background_noise: Remove noise from audio
- generate_thumbnail: Generate thumbnail from video
- add_intro: Add intro clip before main video
- add_outro: Add outro clip after main video
- export_video: Export video to specific format
- change_format: Change video file format

When a user provides a video editing request:
1. Analyze what they want to do
2. Use the CURRENT VIDEO URI provided above for all tool calls
3. Determine which tools to use
4. Call the appropriate tools with correct parameters (including the video URI)
5. If multiple operations are needed, call them in sequence
6. Provide clear feedback about what was done

IMPORTANT: Always use the CURRENT VIDEO URI provided above when calling tools. If no video URI is provided, ask the user to provide one.

Always ask for clarification if the request is ambiguous or missing required parameters.
""")
    
    @traceable(name="video_agent_call")
    def _call_agent(self, state: AgentState) -> Dict:
        """Call the agent to process the current state"""
        # Get current video URI from state (now using dict access)
        current_video_uri = state.get("current_video_uri") or "No video URI provided"
        
        # Create system message
        system_message = self._create_system_message(current_video_uri)
        
        # Prepare messages for LLM
        messages_for_llm = [system_message]
        
        # Add all non-system messages from state
        for msg in state["messages"]:
            if not isinstance(msg, SystemMessage):
                messages_for_llm.append(msg)
        
        # Debug: Print message types before calling LLM
        print(f"Calling LLM with {len(messages_for_llm)} messages:")
        for i, msg in enumerate(messages_for_llm):
            msg_type = type(msg).__name__
            if isinstance(msg, ToolMessage):
                print(f"  [{i}] {msg_type}: tool_call_id={msg.tool_call_id}")
            elif isinstance(msg, AIMessage) and hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"  [{i}] {msg_type}: has {len(msg.tool_calls)} tool_calls")
            else:
                print(f"  [{i}] {msg_type}")
        
        # Invoke the LLM
        try:
            response = self.llm_with_tools.invoke(messages_for_llm)
            print(f"LLM response: {type(response).__name__}, has tool_calls: {hasattr(response, 'tool_calls') and bool(response.tool_calls)}")
        except Exception as e:
            print(f"Error invoking LLM: {e}")
            raise
        
        # Return updated state - append the response to messages
        return {"messages": [response]}  # LangGraph will merge this with existing messages
    
    def _should_continue(self, state: AgentState) -> str:
        """Determine whether to continue with tool calls or end"""
        messages = state.get("messages", [])
        if not messages:
            return "end"
            
        last_message = messages[-1]
        
        # If the last message has tool calls, continue to tools
        if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            print(f"Continuing to tools - last message has {len(last_message.tool_calls)} tool calls")
            return "continue"
        
        # Otherwise, end the conversation
        print("Ending conversation - no tool calls in last message")
        return "end"
    
    @traceable(name="video_editing_request")
    def process_request(self, user_input: str, video_uri: str = None, thread_id: str = "default") -> Dict:
        """Process a video editing request from the user"""
        config = {"configurable": {"thread_id": thread_id}}
        
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "current_video_uri": video_uri
        }
        
        try:
            # Run the graph
            print(f"\n=== Processing request: '{user_input[:100]}...' ===")
            final_state = self.graph.invoke(initial_state, config=config)
            
            # Extract final output
            final_messages = final_state.get("messages", [])
            
            # Find the last AI message with content
            final_output = "No response generated"
            for msg in reversed(final_messages):
                if isinstance(msg, AIMessage) and msg.content:
                    final_output = msg.content
                    break
            
            return {
                "final_output": final_output,
                "messages": final_messages,
                "current_video_uri": final_state.get("current_video_uri"),
                "success": True
            }
        except Exception as e:
            print(f"Error processing request: {e}")
            import traceback
            traceback.print_exc()
            return {
                "final_output": f"Error processing request: {str(e)}",
                "messages": [],
                "current_video_uri": video_uri,
                "success": False
            }
    
    def get_conversation_history(self, thread_id: str = "default") -> List[Dict]:
        """Get conversation history for a thread"""
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            # Get the current state from memory
            current_state = self.graph.get_state(config)
            
            if current_state and current_state.values:
                messages = current_state.values.get("messages", [])
                history = []
                
                for msg in messages:
                    if isinstance(msg, HumanMessage):
                        history.append({
                            "type": "human",
                            "content": msg.content,
                            "timestamp": getattr(msg, "timestamp", None)
                        })
                    elif isinstance(msg, AIMessage):
                        # Include both content and tool calls if present
                        content = msg.content
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            tool_info = f" [Called tools: {', '.join(tc['name'] for tc in msg.tool_calls)}]"
                            content = (content or "") + tool_info
                        if content:
                            history.append({
                                "type": "ai",
                                "content": content,
                                "timestamp": getattr(msg, "timestamp", None)
                            })
                    elif isinstance(msg, ToolMessage):
                        history.append({
                            "type": "tool",
                            "content": msg.content,
                            "tool_call_id": getattr(msg, "tool_call_id", None),
                            "timestamp": getattr(msg, "timestamp", None)
                        })
                
                return history
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
        
        return []
    
    def clear_history(self, thread_id: str = "default") -> bool:
        """Clear conversation history for a thread"""
        try:
            config = {"configurable": {"thread_id": thread_id}}
            # Reset state to empty
            self.graph.update_state(
                config,
                {"messages": []},
                as_node="__start__"
            )
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False


def create_video_editing_agent(openai_api_key: str = None, langsmith_api_key: str = None, 
                              langsmith_project: str = "video-editing-agent") -> VideoEditingAgent:
    """Factory function to create a video editing agent with optional LangSmith tracing"""
    return VideoEditingAgent(
        openai_api_key=openai_api_key,
        langsmith_api_key=langsmith_api_key,
        langsmith_project=langsmith_project
    )