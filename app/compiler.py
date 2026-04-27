# app/compiler.py

import uuid
import json
from openai import OpenAI

client = OpenAI()


def compile_to_graph(text: str):
    """
    Takes raw text and converts it into a structured legal reasoning graph.
    """

    prompt = f"""
Return ONLY valid JSON.

You are analyzing legal or technical text and must extract a structured reasoning graph.

CLASSIFY each node using STRICT RULES:

1. FactorNode (Factual level)
   - Observable facts
   - Definitions
   - Variables
   - Descriptions of systems
   - Example: "A similarity network is a graphical model"

2. ClaimNode (Legal level)
   - Assertions that something is true
   - Conclusions
   - Theorems or legal claims
   - Example: "The defendant breached the contract"

3. ToposNode (Intermediate level)
   - Reasoning patterns
   - Doctrines
   - General principles
   - Example: "If A implies B, and B implies C, then A implies C"

4. ProceduralGateNode
   - Timeliness
   - Jurisdiction
   - Standing
   - Anything that blocks a claim procedurally

LEVEL RULES:

- Factual → raw facts, definitions, variables
- Intermediate → reasoning rules, structures
- Legal → conclusions or assertions

POLARITY RULES:

- Plaintiff → supports a claim
- Defendant → attacks a claim
- Neutral → descriptive or unclear

RELATION TYPES:

- BAF_Support → supports another node
- BAF_Attack → attacks another node
- ConditionalDependency → causal/probabilistic relation
- ProceduralGate → blocks or enables

OUTPUT FORMAT:

{{
  "nodes": [
    {{
      "id": "string",
      "label": "string",
      "type": "FactorNode | ClaimNode | ToposNode | ProceduralGateNode",
      "level": "Factual | Intermediate | Legal",
      "polarity": "Plaintiff | Defendant | Neutral"
    }}
  ],
  "edges": [
    {{
      "source": "string",
      "target": "string",
      "relation_type": "BAF_Support | BAF_Attack | ConditionalDependency | ProceduralGate"
    }}
  ]
}}

TEXT:
{text[:2000]}
"""

    # 🔹 Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    raw_output = response.choices[0].message.content

    # 🔹 Parse JSON safely
    try:
        data = json.loads(raw_output)
    except Exception:
        raise Exception(f"LLM did not return valid JSON:\n{raw_output}")

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    # 🔹 Normalize nodes
    normalized_nodes = []
    id_map = {}

    for node in nodes:
        original_id = node.get("id", str(uuid.uuid4()))
        node_uuid = str(uuid.uuid4())

        normalized_node = {
            "id": original_id,
            "label": node.get("label", original_id),
            "node_id": node_uuid,

            # ✅ classification fields (now meaningful)
            "type": node.get("type", "FactorNode"),
            "level": node.get("level", "Factual"),
            "polarity": node.get("polarity", "Neutral"),

            # ✅ probabilistic base (Phase 3 will refine this)
            "cpt_priors": {
                "state_true": 0.5,
                "state_false": 0.5
            }
        }

        normalized_nodes.append(normalized_node)
        id_map[original_id] = node_uuid

    # 🔹 Normalize edges
    normalized_edges = []

    for edge in edges:
        source_id = edge.get("source")
        target_id = edge.get("target")

        if source_id not in id_map or target_id not in id_map:
            continue

        normalized_edge = {
            "source": source_id,
            "target": target_id,
            "edge_id": str(uuid.uuid4()),

            "source_node_id": id_map[source_id],
            "target_node_id": id_map[target_id],

            "relation_type": edge.get("relation_type", "ConditionalDependency"),

            # default logic gate (can refine later)
            "logic_gate": "NoisyOR"
        }

        normalized_edges.append(normalized_edge)

    graph = {
        "nodes": normalized_nodes,
        "edges": normalized_edges
    }

    return graph