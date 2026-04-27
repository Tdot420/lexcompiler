import os
import uuid
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------
# PDF EXTRACTION
# -------------------------
def extract_text_from_pdf(file_bytes):
    import fitz  # PyMuPDF
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


# -------------------------
# HELPERS
# -------------------------
def normalize_id(text):
    return text.lower().replace(" ", "_").replace("-", "_")[:50]


def safe_json_load(content):
    try:
        return json.loads(content)
    except Exception:
        raise ValueError(f"Invalid JSON returned from model:\n{content}")


def classify_node(label):
    label_lower = label.lower()

    claim_indicators = [
        "must", "should", "is", "are", "exists", "can",
        "valid", "holds", "required", "sound", "exhaustive"
    ]

    if any(word in label_lower for word in claim_indicators):
        return "ClaimNode", "Legal"

    return "FactorNode", "Factual"


# -------------------------
# MAIN COMPILER
# -------------------------
def compile_to_graph(text: str):
    prompt = f"""
You are a legal reasoning compiler that converts text into a structured argument graph.

OUTPUT STRICT JSON:
{{
  "nodes": [...],
  "edges": [...]
}}

-------------------------
NODE RULES
-------------------------
Each node must be:
- ClaimNode (legal assertion)
- FactorNode (fact, definition, evidence)

-------------------------
EDGE RULES (STRICT)
-------------------------
1. BAF_Support
   - FactorNode → ClaimNode
   - ClaimNode → ClaimNode (only if logically derived)

2. BAF_Attack
   - ClaimNode → ClaimNode

3. ConditionalDependency
   - ONLY FactorNode → FactorNode

4. ProceduralGate
   - Blocks a claim

-------------------------
CRITICAL CONSTRAINTS
-------------------------
- DO NOT overconnect nodes
- ONLY include necessary edges
- NO duplicate or meaningless edges

-------------------------
TEXT
-------------------------
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You output strict JSON only."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()
    graph = safe_json_load(content)

    # -------------------------
    # NODE PROCESSING
    # -------------------------
    nodes = []
    node_map = {}
    label_to_id = {}

    for n in graph.get("nodes", []):
        label = n.get("label", "").strip()
        if not label:
            continue

        node_id = str(uuid.uuid4())
        nid = normalize_id(label)

        node_type, level = classify_node(label)

        node = {
            "id": nid,
            "label": label,
            "node_id": node_id,
            "type": n.get("type", node_type),
            "level": n.get("level", level),
            "polarity": "Neutral",
            "cpt_priors": {
                "state_true": 0.5,
                "state_false": 0.5
            }
        }

        node_map[nid] = node
        label_to_id[label] = nid
        nodes.append(node)

    # -------------------------
    # EDGE PROCESSING (FIXED)
    # -------------------------
    edges = []

    for e in graph.get("edges", []):
        source_label = e.get("source", "").strip()
        target_label = e.get("target", "").strip()

        if source_label not in label_to_id or target_label not in label_to_id:
            continue

        source = label_to_id[source_label]
        target = label_to_id[target_label]

        source_node = node_map[source]
        target_node = node_map[target]

        relation = e.get("relation_type", "BAF_Support")

        # -------------------------
        # VALIDATION
        # -------------------------
        valid = False

        if relation == "BAF_Support":
            if source_node["type"] == "FactorNode" and target_node["type"] == "ClaimNode":
                valid = True
            elif source_node["type"] == "ClaimNode" and target_node["type"] == "ClaimNode":
                valid = True

        elif relation == "BAF_Attack":
            if source_node["type"] == "ClaimNode" and target_node["type"] == "ClaimNode":
                valid = True

        elif relation == "ConditionalDependency":
            if source_node["type"] == "FactorNode" and target_node["type"] == "FactorNode":
                valid = True

        elif relation == "ProceduralGate":
            valid = True

        if not valid:
            continue

        edge = {
            "source": source,
            "target": target,
            "edge_id": str(uuid.uuid4()),
            "source_node_id": source_node["node_id"],
            "target_node_id": target_node["node_id"],
            "relation_type": relation,
            "logic_gate": "NoisyOR"
        }

        edges.append(edge)

    return {
        "nodes": nodes,
        "edges": edges
    }