import os
import json
import uuid
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def compile_to_graph(text: str):
    prompt = f"""
Return ONLY valid JSON.

Schema:
{{
  "nodes": [],
  "edges": []
}}

Text:
{text[:2000]}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    print("RAW LLM OUTPUT:", repr(content))

    if not content or content.strip() == "":
        raise Exception("LLM returned EMPTY response")

    content = content.strip()

    try:
        graph = json.loads(content)
    except:
        import re
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            graph = json.loads(match.group())
        else:
            raise Exception(f"Invalid JSON from LLM: {content}")

    for node in graph.get("nodes", []):
        node["node_id"] = str(uuid.uuid4())

    for edge in graph.get("edges", []):
        edge["edge_id"] = str(uuid.uuid4())

    return graph