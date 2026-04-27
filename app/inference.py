from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD

def run_inference(graph, observed_facts):
    edges = [(e["source_node_id"], e["target_node_id"]) for e in graph["edges"]]
    model = BayesianNetwork(edges)

    cpds = []

    for node in graph["nodes"]:
        prob_true = node["cpt_priors"]["state_true"]
        prob_false = node["cpt_priors"]["state_false"]

        cpd = TabularCPD(
            variable=node["node_id"],
            variable_card=2,
            values=[[prob_false], [prob_true]]
        )
        cpds.append(cpd)

    model.add_cpds(*cpds)

    infer = VariableElimination(model)

    results = {}
    for node in graph["nodes"]:
        q = infer.query(variables=[node["node_id"]])
        results[node["node_id"]] = float(q.values[1])

    meu = sum(results.values()) / len(results)

    return results, meu