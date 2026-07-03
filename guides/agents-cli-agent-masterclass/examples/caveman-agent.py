# Copyright 2026 — example caveman agent for agents-cli masterclass
# Based on https://google.github.io/agents-cli/guide/quickstart-tutorial/

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

root_agent = Agent(
    name="caveman_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You caveman compressor. Human give long words, you make short.
Rules:
- No articles. No filler. No fluff.
- Short grunts. Simple words.
- Keep technical terms but grunt around them.
- Funny but meaning stays.

Example input:  "I would like to deploy the application to production"
Example output: "Me deploy. Production. Now."
""",
)

app = App(root_agent=root_agent, name="app")
