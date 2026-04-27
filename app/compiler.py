import os
import json
import uuid
import re
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def normalize_graph(graph):
    """
    Converts raw LLM output into the required schema
    expected by the inference engine.
    """
    node_map = {}

    # Normalize nodes
    for node in graph.get("nodes", []):
        node_uuid = str(uuid.uuid4())
        node["node_id"] = node_uuid

        # Map original ID to UUID
        node_map[node.get("id")] = node_uuid

        # Add required fields
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

        # Map source/target IDs → UUIDs
        edge["source_node_id"] = node_map.get(edge.get("source"))
        edge["target_node_id"] = node_map.get(edge.get("target"))

        # Add required inference fields
        edge["relation_type"] = "ConditionalDependency"
        edge["logic_gate"] = "NoisyOR"

graph = normalize_graph(graph)
return graph


def compile_to_graph(text: str):
    """
    Main compiler pipeline:
    - Sends legal text to LLM
    - Extracts nodes/edges
    - Validates JSON
    - Normalizes structure
    """

    prompt = f"""
You are a legal decision compiler.

Return ONLY valid JSON in this exact format:

{{
  "nodes": [
    {{"id": "string", "label": "string"}}
  ],
  "edges": [
    {{"source": "string", "target": "string", "label": "string"}}
  ]
}}

Rules:
- No explanations
- No markdown
- No extra text
- Only JSON

Text:
{text[:2000]}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    # Debug log (visible in Railway logs)
    print("RAW LLM OUTPUT:", repr(content))

    if not content or content.strip() == "":
        raise Exception("LLM returned EMPTY response")

    content = content.strip()

    # Attempt strict JSON parse
    try:
        graph = json.loads(content)

    except Exception:
        # Attempt recovery if LLM included extra text
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            try:
                graph = json.loads(match.group())
            except Exception:
                raise Exception(f"JSON recovery failed: {content}")
        else:
            raise Exception(f"Invalid JSON from LLM: {content}")

    # Normalize to inference-compatible schema
    graph = normalize_graph(graph)

    return graph