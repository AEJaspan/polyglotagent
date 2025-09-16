from google.adk.tools.tool_context import ToolContext
from google.adk.tools import FunctionTool
from typing import Any, Dict

def log_scores(tool_context: ToolContext, evaluation: Dict[str, Any]) -> str:
    """Saves the complete CEFR speaking evaluation JSON to the agent's memory.

    Use this tool only after you have fully evaluated the user's speaking
    performance and have generated the complete JSON object conforming to the
    SpeakingEvaluation schema. This tool persists the results of the analysis.

    Args:
        evaluation: The complete JSON object of the speaking evaluation.

    Returns:
        A string confirming that the scores were logged successfully.
    """
    print('*'*1000)
    print(f"Logging evaluation: {evaluation}")
    print('*'*1000)
    tool_context.memory["scores"] = evaluation
    return "Scores logged successfully."

def get_scores(tool_context: ToolContext) -> Dict[str, Any]:
    """Retrieves the most recent CEFR speaking evaluation from the agent's memory.

    Use this tool when the user asks about their previous results, wants a summary
    of their last performance, or if you need to access the last evaluation
    data for comparison.

    Returns:
        The complete JSON object of the last saved speaking evaluation,
        or an empty dictionary if no evaluation has been saved yet.
    """
    scores = tool_context.memory.get("scores", {})
    print('*'*1000)
    print(f"Scores: {scores}")
    print('*'*1000)
    return scores


log_scores_tool = FunctionTool(func=log_scores)
get_scores_tool = FunctionTool(func=get_scores)