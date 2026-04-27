import uuid
import hashlib
import re
from typing import List, Dict
from collections import defaultdict


# -------------------------------
# Helpers
# -------------------------------

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def generate_id(label: str) -> str:
    """Generate deterministic short ID + uniqueness suffix"""
    base = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
    short_hash = hashlib.md5(label.encode()).hexdigest()[:6]
    return f"{base[:40]}_{short_hash}"


def classify_node(label: str) -> Dict:
    """Classify node type + level"""
    label_lower = label.lower()

    claim_keywords = [
        "must", "can", "is", "are", "exists", "proven",
        "constructed", "established", "delineates"
    ]

    factual_keywords = [
        "definition", "denotes", "represents", "means"
    ]

    if any(k in label_lower for k in factual_keywords):
        return {"type": "ClaimNode", "level": "Factual"}

    if any(k in label_lower for k in claim_keywords):
        return {"type": "ClaimNode", "level": "Legal"}

    return {"type": "ClaimNode", "level": "Factual"}


def extract_sentences(text: str) -> List[str]:
    """Basic sentence splitting"""
    raw = re.split(r"[.\n]+", text)
    return [normalize_text(s) for s in raw if len(s.strip()) > 20]


# -------------------------------
# Core Compiler
# -------------------------------

def compile_to_graph(text: str) -> Dict:
    sentences = extract_sentences(text)

    nodes = []
    edges = []

    node_lookup = {}
    edge_set = set()

    # -------------------------------
    # Create Nodes
    # -------------------------------
    for sentence in sentences:
        node_id_str = generate_id(sentence)

        if node_id_str in node_lookup:
            continue

        classification = classify_node(sentence)

        node = {
            "id": node_id_str,
            "label": sentence,
            "node_id": str(uuid.uuid4()),
            "type": classification["type"],
            "level": classification["level"],
            "polarity": "Neutral",
            "cpt_priors": {
                "state_true": 0.5,
                "state_false": 0.5
            }
        }

        node_lookup[node_id_str] = node
        nodes.append(node)

    # -------------------------------
    # Create Edges (simple chain logic)
    # -------------------------------
    node_ids = list(node_lookup.keys())

    for i in range(len(node_ids) - 1):
        source = node_ids[i]
        target = node_ids[i + 1]

        edge_key = (source, target)

        if edge_key in edge_set:
            continue

        edge = {
            "source": source,
            "target": target,
            "edge_id": str(uuid.uuid4()),
            "source_node_id": node_lookup[source]["node_id"],
            "target_node_id": node_lookup[target]["node_id"],
            "relation_type": "BAF_Support",
            "logic_gate": "NoisyOR"
        }

        edge_set.add(edge_key)
        edges.append(edge)

    # -------------------------------
    # Final Graph
    # -------------------------------
    graph = {
        "nodes": nodes,
        "edges": edges
    }

    return graph