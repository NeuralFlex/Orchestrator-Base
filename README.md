# Video Editing Agent with LangGraph

A powerful AI-powered video editing agent built with LangGraph that can understand natural language commands and perform complex video editing operations using a ReAct (Reasoning and Acting) pattern.

## Features

🎬 **Comprehensive Video Editing Capabilities:**
- Trim, split, and merge videos
- Crop, resize, and change resolution
- Add transitions, overlays, and effects
- Add subtitles, captions, and soundtracks
- Color correction and audio adjustments
- Export and format conversion

🧠 **AI-Powered:**
- Natural language understanding
- ReAct pattern for reasoning and tool selection
- Memory management (last 5 messages)
- Multi-tool orchestration

🛠️ **Available Tools:**
- `trim_video` - Trim video between start and end times
- `split_video` - Split video into two clips
- `merge_clips` - Merge two video clips
- `crop_frame` - Crop video frame to specific region
- `resize_video` - Resize video to target dimensions
- `change_resolution` - Change video resolution
- `adjust_frame_rate` - Adjust video frame rate
- `color_correct` - Apply color correction
- `add_transition` - Add transition effects
- `add_overlay` - Overlay image on video
- `add_subtitles` - Add subtitle file
- `add_captions` - Add custom text captions
- `add_soundtrack` - Add audio soundtrack
- `adjust_volume` - Adjust audio volume
- `remove_background_noise` - Remove audio noise
- `generate_thumbnail` - Generate thumbnail
- `add_intro` - Add intro clip
- `add_outro` - Add outro clip
- `export_video` - Export to specific format
- `change_format` - Change file format

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd orchestrator-POC
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

3. **Set up API keys:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export LANGSMITH_API_KEY="your-langsmith-api-key"  # Optional but recommended
   export LANGSMITH_PROJECT="video-editing-agent"     # Optional, defaults to above
   ```

## Usage

### Interactive Mode

Run the main application for an interactive video editing session:

```bash
uv run main.py
```

### Programmatic Usage

```python
from src.agents.video_agent import create_video_editing_agent

# Create the agent with LangSmith tracing
agent = create_video_editing_agent(
    openai_api_key="your-openai-api-key",
    langsmith_api_key="your-langsmith-api-key",  # Optional
    langsmith_project="video-editing-agent"      # Optional
)

# Process a video editing request
result = agent.process_request(
    user_input="Trim my video from 10 seconds to 30 seconds",
    video_uri="s3://your-bucket/input/video.mp4",
    thread_id="session_1"
)

print(result["final_output"])
```

### Example Commands

- "Trim my video from 10 seconds to 30 seconds"
- "Split my video at 15 seconds"
- "Resize my video to 1920x1080"
- "Add a fade transition between two clips"
- "Apply color correction with brightness 1.2"
- "Add subtitles to my video"
- "Merge two clips with a wipe transition"

**Note:** You'll be prompted to provide a video URI (S3 path) for each request. The agent will use this URI for all video editing operations.

## Architecture

The agent is built using:

- **LangGraph**: For creating the ReAct workflow
- **OpenAI GPT-4**: For natural language understanding
- **Pydantic**: For data validation and state management
- **Memory Management**: Maintains conversation history
- **LangSmith**: For tracing, monitoring, and debugging

### Workflow

1. **User Input**: Natural language video editing request
2. **Agent Reasoning**: LLM analyzes the request and determines required tools
3. **Tool Execution**: Appropriate video editing tools are called
4. **Memory Update**: Conversation state is updated
5. **Response**: Final output is provided to the user

## File Structure

```
orchestrator-POC/
├── src/                       # Source code
│   ├── agents/               # Agent implementations
│   │   └── video_agent.py    # Core video editing agent
│   └── tools/                # Tool implementations
│       └── tools.py          # Video editing tools
├── examples/                  # Usage examples
│   ├── example_usage.py      # Basic usage examples
│   └── langsmith_example.py  # LangSmith tracing examples
├── tests/                     # Test files
│   └── test_agent.py         # Agent testing script
├── main.py                   # Main interactive interface
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
├── .gitignore               # Git ignore patterns
├── .python-version          # Python version specification
└── README.md                # This file
```

## Configuration

The agent can be configured through:

- **OpenAI API Key**: Set via environment variable or direct parameter
- **LangSmith API Key**: Optional, enables tracing and monitoring
- **LangSmith Project**: Custom project name for organizing traces
- **Model**: Currently uses `gpt-4o-mini` (configurable in `video_agent.py`)
- **Memory**: Maintains last 5 messages (configurable)
- **Thread Management**: Supports multiple conversation threads

## Development

### Adding New Tools

1. Add the tool function to `src/tools/tools.py`
2. The agent will automatically register it
3. Update the system prompt in `src/agents/video_agent.py` if needed

### Customizing the Agent

- Modify the system prompt in `_call_agent` method
- Adjust memory management in `_call_agent`
- Add new state fields in `AgentState` class

## LangSmith Tracing

The agent includes comprehensive LangSmith tracing for monitoring and debugging:

### Setup Tracing

```bash
# Set LangSmith API key
export LANGSMITH_API_KEY="your-langsmith-api-key"
export LANGSMITH_PROJECT="video-editing-agent"  # Optional
```

### View Traces

1. Open [LangSmith Dashboard](https://smith.langchain.com)
2. Navigate to your project
3. View individual traces showing:
   - User input and agent reasoning
   - Tool selection and execution
   - Performance metrics and timing
   - Error handling and debugging info

### Tracing Examples

```bash
# Run examples with tracing
uv run langsmith_example.py
```

## Examples

### Running Examples

```bash
# Run basic usage examples
uv run examples/example_usage.py

# Run LangSmith tracing examples
uv run examples/langsmith_example.py

# Run agent tests
uv run tests/test_agent.py
```

See `examples/example_usage.py` for comprehensive usage examples including:
- Simple operations
- Multi-step workflows
- Complex video editing tasks

See `examples/langsmith_example.py` for tracing examples and monitoring setup.

## Requirements

- Python 3.12+
- OpenAI API key
- LangSmith API key (optional but recommended for tracing)
- uv package manager

## License

This project is for demonstration purposes. Please ensure you have appropriate licenses for any video content you process.
