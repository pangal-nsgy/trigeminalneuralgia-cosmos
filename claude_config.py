"""
Configuration module for Claude Opus API integration.
"""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize Anthropic client
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")

if not ANTHROPIC_API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY not found. Please set it in your .env file or environment variables."
    )

# Initialize the client
claude_client = Anthropic(api_key=ANTHROPIC_API_KEY)


def get_claude_client():
    """Get the configured Claude client."""
    return claude_client


def get_model_name():
    """Get the configured model name."""
    return CLAUDE_MODEL
