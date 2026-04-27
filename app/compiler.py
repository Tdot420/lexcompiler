import os
import json
import uuid
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def compile_to_graph(text: str):
    prompt = f"""
Convert this legal text into a JSON graph with nodes and edges.

Text:
{text[:3000]}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    graph = json.loads(content)

    for node in graph["nodes"]:
        node["node_id"] = str(uuid.uuid4())

    for edge in graph["edges"]:
        edge["edge_id"] = str(uuid.uuid4())

    return graph