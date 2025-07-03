"""
Registro e heartbeat dos nós no cluster.
"""
def register_node(config):
    print("Nó registrado (stub)")
    return "node_id_stub"

def report_heartbeat(node_id, metrics):
    print(f"Heartbeat de {node_id}: {metrics}")
