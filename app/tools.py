
from google.adk.tools.tool_context import ToolContext
from google.adk.tools import FunctionTool
from typing import Any

def log_scores(tool_context: ToolContext, **scores: Any) -> str:
    """
    Saves a set of scores to the agent's memory.
    This should be called after an evaluation is complete.
    """
    print('*'*1000)
    print(scores)
    print('*'*1000)
    tool_context.memory["scores"] = scores
    return "Scores logged successfully."

def get_scores(tool_context: ToolContext) -> dict[str, Any]:
    """
    Retrieves the last logged set of scores from the agent's memory.
    """
    return tool_context.memory.get("scores", {})

log_scores_tool = FunctionTool(func=log_scores)
get_scores_tool = FunctionTool(func=get_scores)