from fastapi import APIRouter
from .settings import settings
from typing import List, Dict

router = APIRouter(prefix="/network", tags=["network"])

@router.get("/summary", summary="Resumo da rede")
def get_network_summary() -> Dict:
    """
    Retorna:
      total_nodes: int
      total_data_mb: float
      total_data_gb: float
      avg_speed_mbps: float
    """
    from orchestrator.node_registry import get_active_nodes
    nodes = get_active_nodes()  # retorna List[{...}]
    total_nodes   = len(nodes)
    total_data_mb = sum(n.get("network_usage_mb", 0) for n in nodes)
    total_data_gb = total_data_mb / 1024
    avg_speed     = (sum(n.get("network_speed_mbps", 0) for n in nodes) / total_nodes) if total_nodes else 0
    return {
        "total_nodes": total_nodes,
        "total_data_mb": round(total_data_mb, 2),
        "total_data_gb": round(total_data_gb, 2),
        "avg_speed_mbps": round(avg_speed, 2),
    }

@router.get("/topology", summary="Topologia da rede")
def get_network_topology() -> Dict[str, List]:
    """
    Retorna grafo simples no formato:
      {
        "nodes": [{ "id": "node1" }, ...],
        "links": [{ "source": "node1", "target": "node2" }, ...]
      }
    """
    from orchestrator.node_registry import get_active_nodes, get_peers
    nodes = get_active_nodes()
    graph = {
        "nodes": [{"id": n["node_id"]} for n in nodes],
        "links": []
    }
    for n in nodes:
        for peer in get_peers(n["node_id"]):
            graph["links"].append({"source": n["node_id"], "target": peer})
    return graph
