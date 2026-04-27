import os
import json
import uuid
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def compile_to_graph(text: str):
    prompt = f"""
You are a legal decision compiler.

Return ONLY valid JSON with this structure:

{{
  "nodes": [],
  "edges": []
}}

No explanations. No text. Only JSON.

Text:
{text[:3000]}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # 🧠 DEBUG PRINT (important)
    print("LLM OUTPUT:", content)

    # 🛑 SAFETY CHECK
    if not content:
        raise Exception("LLM returned empty response")

    # 🛠️ TRY TO FIX COMMON JSON ISSUES
    try:
        graph = json.loads(content)
    except:
        # attempt recovery if extra text exists
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end != -1:
            graph = json.loads(content[start:end])
        else:
            raise Exception(f"Invalid JSON from LLM: {content}")

    # assign UUIDs
    for node in graph.get("nodes", []):
        node["node_id"] = str(uuid.uuid4())

    for edge in graph.get("edges", []):
        edge["edge_id"] = str(uuid.uuid4())

    return graph