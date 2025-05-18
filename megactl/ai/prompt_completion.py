from openai import OpenAI
from decouple import config

client = OpenAI(api_key=config("OPENAI_API_KEY"))
model = config("OPENAI_MODEL", default="gpt-4")


def get_prompt_suggestion(user_input: str, context_data: dict) -> str:
    """
    Suggest how the user might finish their input based on real cluster context.
    context_data = { "pods": [...], "deployments": [...], "namespaces": [...] }
    """
    pods = ", ".join(context_data.get("pods", [])[:20])
    deployments = ", ".join(context_data.get("deployments", [])[:20])
    namespaces = ", ".join(context_data.get("namespaces", [])[:10])

    SYSTEM_PROMPT = f"""
You are a Kubernetes CLI assistant helping users write natural-language commands.
Here are known resources in the cluster:

Pods: {pods}
Deployments: {deployments}
Namespaces: {namespaces}

Use only these known names. Complete the user's intent as natural language, not a kubectl command.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Complete this: {user_input}"}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return ""
