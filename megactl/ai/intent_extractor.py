import json
from decouple import config
from openai import OpenAI

from megactl.ai.prompts.system_prompt import SYSTEM_PROMPT

client = OpenAI(api_key=config("OPENAI_API_KEY"))
model = config("OPENAI_MODEL", default="gpt-4")


def get_k8s_intent(user_input: str) -> dict:
    """Send user input to GPT and return parsed intent as dict."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)

    except json.JSONDecodeError as je:
        raise RuntimeError(f"❌ Invalid JSON in GPT response: {je}")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to get intent from GPT: {e}")


def retry_intent_with_error(user_input: str, error_output: str) -> dict:
    retry_prompt = f"""
The user asked: "{user_input}"

Your last kubectl command caused this error:

{error_output}

Based on the error, regenerate a corrected intent object with a valid kubectl command. Only return the JSON.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": retry_prompt}
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()
    return json.loads(content)