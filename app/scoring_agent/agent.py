from google.adk.agents import Agent
from google.adk.tools import load_artifacts
from google.adk.tools.tool_context import ToolContext
from google.genai import Client
from google.genai import types
import google
import os
from typing import Any
# from zoneinfo import ZoneInfo
from google.adk.tools import FunctionTool
import google.auth
# from google.adk.agents import Agent

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")



client = Client()

def judge_speaking(user_input: str) -> dict[str, Any]:
    """
    Evaluate a learner's speaking sample (transcript or written proxy) 
    against CEFR rubrics and return a structured SpeakingEvaluation.
    """
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input,
        config={
            "response_mime_type": "application/json",
            "response_schema": SpeakingEvaluation,
        },
    )

    evaluation = resp.parsed if resp.parsed else SpeakingEvaluation.model_validate_json(resp.text)

    return evaluation.model_dump()

judge_speaking_tool = FunctionTool(func=judge_speaking)

speach_eval_agent = Agent(
    model="gemini-2.5-flash",
    name="cefr_speaking_judge",
    instruction=(
        "You are a CEFR speaking evaluation assistant. "
        "When the user provides speech or a transcript, call the 'judge_speaking' tool. "
        "Return structured CEFR-based evaluation and explain the scores clearly."
    ),
    tools=[judge_speaking_tool],
)

# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    user_text = "Yesterday I go to the market and buy many fruit because it was cheap."
    result = judge_speaking(user_text)
    print(result)  # dict with full CEFR-based evaluation