"""
Nó Coexum: registra no cluster e envia heartbeat periodicamente.
"""
import time, json
from agent.metrics import collect_metrics
from orchestrator.node_registry import register_node, report_heartbeat

HEARTBEAT_INTERVAL = 60  # segundos

def start_node():
    config = json.load(open('coexum.json'))
    node_id = register_node(config)
    while True:
        metrics = collect_metrics()
        report_heartbeat(node_id, metrics)
        time.sleep(HEARTBEAT_INTERVAL)

def stop_node():
    """Stub: para o nó Coexum (não implementado)."""
    print("Nó Coexum parado (stub)")
