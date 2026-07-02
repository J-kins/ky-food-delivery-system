from typing import Dict, Any
from pydantic import ValidationError
import networkx as nx
from core.models import PertSpec
from core.errors import InvalidInputError, CyclicDependencyError, MissingDependencyError

def validate_pert(spec_dict: Dict[str, Any]) -> PertSpec:
    try:
        spec = PertSpec(**spec_dict)
    except ValidationError as e:
        raise InvalidInputError(f"Schema validation failed:\n{e}")

    pc = spec.pert_chart
    task_ids = {t.id for t in pc.tasks}

    # Build networkx DiGraph to validate DAG properties
    G = nx.DiGraph()
    for t in pc.tasks:
        G.add_node(t.id)

    for t in pc.tasks:
        for dep in t.dependencies:
            if dep not in task_ids:
                raise MissingDependencyError(dep)
            # Edge from predecessor to successor
            G.add_edge(dep, t.id)

    if not nx.is_directed_acyclic_graph(G):
        raise CyclicDependencyError()

    return spec
