"""
Helper module for using Claude Opus in data analysis workflows.
"""
import pandas as pd
import json
from typing import Optional, Dict, Any
from claude_config import get_claude_client, get_model_name


def analyze_with_claude(
    prompt: str,
    data_summary: Optional[str] = None,
    data_sample: Optional[pd.DataFrame] = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> str:
    """
    Send a data analysis prompt to Claude Opus and get a response.
    
    Parameters:
    -----------
    prompt : str
        The analysis question or task for Claude
    data_summary : str, optional
        Summary statistics or description of the data
    data_sample : pd.DataFrame, optional
        Sample of the data to include in the prompt (first 100 rows)
    max_tokens : int
        Maximum tokens in the response (default: 4096)
    temperature : float
        Temperature for response generation (default: 0.7)
    
    Returns:
    --------
    str
        Claude's response
    """
    client = get_claude_client()
    model = get_model_name()
    
    # Build the full prompt
    full_prompt = ""
    
    if data_summary:
        full_prompt += f"Data Summary:\n{data_summary}\n\n"
    
    if data_sample is not None:
        sample_str = data_sample.head(100).to_string()
        full_prompt += f"Sample Data (first 100 rows):\n{sample_str}\n\n"
    
    full_prompt += f"Analysis Request:\n{prompt}"
    
    # Make the API call
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    )
    
    return message.content[0].text


def get_analysis_suggestions(data: pd.DataFrame, research_question: str) -> str:
    """
    Get suggestions from Claude on how to analyze the data.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The dataset to analyze
    research_question : str
        The main research question
    
    Returns:
    --------
    str
        Claude's analysis suggestions
    """
    data_info = f"""
    Dataset Shape: {data.shape}
    Columns: {list(data.columns)}
    Data Types:\n{data.dtypes}
    Missing Values:\n{data.isnull().sum()}
    Basic Statistics:\n{data.describe()}
    """
    
    prompt = f"""
    I have a dataset for a research project on trigeminal neuralgia. 
    Here's information about my data:
    
    {data_info}
    
    My research question is: {research_question}
    
    Please provide:
    1. Suggested statistical analyses appropriate for this research question
    2. Recommended visualizations
    3. Potential confounding variables to consider
    4. Statistical tests that would be appropriate
    5. Any data quality issues I should address first
    
    Please be specific and provide publishable-quality analysis recommendations.
    """
    
    return analyze_with_claude(prompt, data_summary=data_info)


def generate_code_suggestion(analysis_description: str, data: pd.DataFrame) -> str:
    """
    Get Python code suggestions from Claude for a specific analysis.
    
    Parameters:
    -----------
    analysis_description : str
        Description of the analysis to perform
    data : pd.DataFrame
        The dataset
    
    Returns:
    --------
    str
        Python code suggested by Claude
    """
    data_info = f"""
    Dataset Shape: {data.shape}
    Columns: {list(data.columns)}
    Data Types:\n{data.dtypes}
    """
    
    prompt = f"""
    I need to perform the following analysis: {analysis_description}
    
    Dataset information:
    {data_info}
    
    Please provide complete, production-ready Python code to perform this analysis.
    Include:
    - Data loading/preprocessing if needed
    - The specific analysis
    - Appropriate visualizations
    - Statistical tests with interpretation
    - Code should be well-commented and follow best practices
    
    Return only the Python code, ready to execute.
    """
    
    return analyze_with_claude(prompt, data_summary=data_info, temperature=0.3)
