# Trigeminal Neuralgia Cosmos Data Analytics

Data analysis project using Claude Opus for publishable research on trigeminal neuralgia.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API key:**
   - Copy `.env.example` to `.env`
   - Add your Anthropic API key to `.env`:
     ```
     ANTHROPIC_API_KEY=your_api_key_here
     CLAUDE_MODEL=claude-3-opus-20240229
     ```
   - Get your API key from: https://console.anthropic.com/

3. **Verify setup:**
   ```python
   from claude_config import get_claude_client, get_model_name
   print(f"Using model: {get_model_name()}")
   ```

## Usage

### Basic Analysis with Claude Opus

```python
from claude_analysis import analyze_with_claude
import pandas as pd

# Load your data
df = pd.read_csv('your_data.csv')

# Ask Claude for analysis
response = analyze_with_claude(
    prompt="What statistical tests should I use to compare treatment groups?",
    data_summary=df.describe().to_string(),
    data_sample=df
)
print(response)
```

### Get Analysis Suggestions

```python
from claude_analysis import get_analysis_suggestions

suggestions = get_analysis_suggestions(
    data=df,
    research_question="Does treatment X reduce pain scores compared to control?"
)
print(suggestions)
```

### Generate Analysis Code

```python
from claude_analysis import generate_code_suggestion

code = generate_code_suggestion(
    analysis_description="Perform a t-test comparing pain scores between two groups",
    data=df
)
print(code)
```

## Model Configuration

The project is configured to use **Claude 3 Opus** (`claude-3-opus-20240229`) by default. To change the model, update the `CLAUDE_MODEL` variable in your `.env` file.

Available Claude models:
- `claude-3-opus-20240229` (Opus - most capable)
- `claude-3-sonnet-20240229` (Sonnet - balanced)
- `claude-3-haiku-20240307` (Haiku - fastest)

## Project Structure

```
.
├── claude_config.py      # Configuration and client setup
├── claude_analysis.py    # Helper functions for analysis
├── requirements.txt      # Python dependencies
├── .env                  # API keys (not in git)
└── README.md            # This file
```
