"""
Example script demonstrating how to use Claude Opus for data analysis.
"""
import pandas as pd
from claude_analysis import (
    analyze_with_claude,
    get_analysis_suggestions,
    generate_code_suggestion
)

# Example: Load your data (replace with your actual data file)
# df = pd.read_csv('your_data.csv')

# Example 1: Simple analysis question
def example_simple_analysis():
    """Example of asking Claude a simple analysis question."""
    response = analyze_with_claude(
        prompt="What statistical methods are appropriate for analyzing pain scores "
               "in a clinical trial comparing two treatment groups?",
        max_tokens=2048
    )
    print("Claude's Response:")
    print(response)
    return response


# Example 2: Get analysis suggestions for your dataset
def example_get_suggestions(df: pd.DataFrame, research_question: str):
    """Example of getting analysis suggestions from Claude."""
    suggestions = get_analysis_suggestions(
        data=df,
        research_question=research_question
    )
    print("Analysis Suggestions:")
    print(suggestions)
    return suggestions


# Example 3: Generate code for a specific analysis
def example_generate_code(df: pd.DataFrame, analysis_description: str):
    """Example of getting Python code from Claude for a specific analysis."""
    code = generate_code_suggestion(
        analysis_description=analysis_description,
        data=df
    )
    print("Generated Code:")
    print(code)
    return code


# Example 4: Interactive analysis workflow
def example_workflow(df: pd.DataFrame):
    """
    Example workflow: Ask Claude for suggestions, then generate code.
    """
    # Step 1: Get analysis suggestions
    print("Step 1: Getting analysis suggestions...")
    suggestions = get_analysis_suggestions(
        data=df,
        research_question="Compare treatment efficacy between groups"
    )
    
    # Step 2: Generate code for a specific analysis
    print("\nStep 2: Generating code for t-test analysis...")
    code = generate_code_suggestion(
        analysis_description="Perform independent samples t-test comparing pain scores",
        data=df
    )
    
    return suggestions, code


if __name__ == "__main__":
    # Uncomment and modify these examples based on your data:
    
    # Example 1: Simple question
    # example_simple_analysis()
    
    # Example 2: With actual data
    # df = pd.read_csv('your_data.csv')
    # example_get_suggestions(df, "Your research question here")
    
    print("See the functions above for usage examples.")
    print("Uncomment the examples and provide your data to get started.")
