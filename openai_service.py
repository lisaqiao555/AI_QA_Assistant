import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_test_cases(requirement):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
You are a Senior QA Engineer.

Requirement:
{requirement}

Generate 8 to 12 software test cases.

Return valid JSON only.

Schema:
[
  {{
    "test_case_id": "TC001",
    "title": "",
    "priority": "High/Medium/Low",
    "precondition": "",
    "steps": "",
    "expected_result": ""
  }}
]

Do not return markdown.
Do not return explanation.
Return JSON only.
"""
    )

    return response.output_text