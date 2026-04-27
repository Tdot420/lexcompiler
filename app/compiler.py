import os
import json
import uuid
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def normalize_graph(graph):
    node_map = {}

    # Normalize nodes
    for node in graph.get("nodes", []):
        node_uuid = str(uuid.uuid4())
        node["node_id"] = node_uuid
        node_map[node.get("id")] = node_uuid

        node["type"] = "FactorNode"
        node["level"] = "Factual"
        node["polarity"] = "Neutral"
        node["cpt_priors"] = {
            "state_true": 0.5,
            "state_false": 0.5
        }

    # Normalize edges
    for edge in graph.get("edges", []):
        edge["edge_id"] = str(uuid.uuid4())

        edge["source_node_id"] = node_map.get(edge.get("source"))
        edge["target_node_id"] = node_map.get(edge.get("target"))

        edge["relation_type"] = "ConditionalDependency"
        edge["logic_gate"] = "NoisyOR"

    return graph


def compile_to_graph(text: str):

    prompt = f"""
Return ONLY valid JSON:

{{
  "nodes": [
    {{"id": "string", "label": "string"}}
  ],
  "edges": [
    {{"source": "string", "target": "string", "label": "string"}}
  ]
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

    print("RAW:", repr(content))

    try:
        graph = json.loads(content)
    except:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise Exception("Invalid JSON")
        graph = json.loads(match.group())

    # ✅ THIS MUST BE INSIDE THE FUNCTION
    graph = normalize_graph(graph)

    return graph