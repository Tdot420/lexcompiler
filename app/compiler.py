import os
import uuid
import json
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------
# PDF EXTRACTION
# -------------------------
def extract_text_from_pdf(file_bytes):
    import fitz
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


def clean_json(content):
    """
    Removes ```json blocks and extracts raw JSON
    """
    content = content.strip()

    # Remove markdown ```json ```
    if content.startswith("```"):
        content = re.sub(r"```json|```", "", content).strip()

    # Extract JSON object
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        return match.group(0)

    return content


def safe_json_load(content):
    try:
        cleaned = clean_json(content)
        return json.loads(cleaned)
    except Exception:
        return {"nodes": [], "edges": []}


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

    if not text.strip():
        return {"nodes": [], "edges": []}

    prompt = f"""
Convert the following text into a structured argument graph.

STRICT JSON ONLY. NO MARKDOWN.

FORMAT:
{{
  "nodes": [
    {{"label": "...", "type": "ClaimNode or FactorNode"}}
  ],
  "edges": [
    {{"source": "...", "target": "...", "relation_type": "BAF_Support"}}
  ]
}}

TEXT:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content
    graph = safe_json_load(raw)

    # -------------------------
    # FAILSAFE: ensure nodes exist
    # -------------------------
    if not graph.get("nodes"):
        # fallback: create nodes from sentences
        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]

        nodes = []
        for s in sentences[:10]:
            nid = normalize_id(s)
            node_type, level = classify_node(s)

            nodes.append({
                "id": nid,
                "label": s,
                "node_id": str(uuid.uuid4()),
                "type": node_type,
                "level": level,
                "polarity": "Neutral",
                "cpt_priors": {
                    "state_true": 0.5,
                    "state_false": 0.5
                }
            })

        return {"nodes": nodes, "edges": []}

    # -------------------------
    # NORMAL PROCESSING
    # -------------------------
    nodes = []
    node_map = {}
    label_to_id = {}

    for n in graph.get("nodes", []):
        label = n.get("label", "").strip()
        if not label:
            continue

        nid = normalize_id(label)

        node_type, level = classify_node(label)

        node = {
            "id": nid,
            "label": label,
            "node_id": str(uuid.uuid4()),
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

    edges = []

    for e in graph.get("edges", []):
        source_label = e.get("source", "").strip()
        target_label = e.get("target", "").strip()

        if source_label not in label_to_id or target_label not in label_to_id:
            continue

        source = label_to_id[source_label]
        target = label_to_id[target_label]

        edges.append({
            "source": source,
            "target": target,
            "edge_id": str(uuid.uuid4()),
            "source_node_id": node_map[source]["node_id"],
            "target_node_id": node_map[target]["node_id"],
            "relation_type": e.get("relation_type", "BAF_Support"),
            "logic_gate": "NoisyOR"
        })

    return {
        "nodes": nodes,
        "edges": edges
    }