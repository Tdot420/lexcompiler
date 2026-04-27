from pydantic import BaseModel
from typing import List, Dict
from uuid import UUID

class GraphModel(BaseModel):
    nodes: list
    edges: list

class InferenceRequest(BaseModel):
    graph: GraphModel
    observed_facts: Dict[UUID, bool]

class InferenceResult(BaseModel):
    posterior_probabilities: Dict[str, float]
    meu_score: float