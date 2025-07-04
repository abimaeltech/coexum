"""
Registro e heartbeat dos nós no cluster.
"""
def register_node(config):
    print("Nó registrado (stub)")
    return "node_id_stub"

def report_heartbeat(node_id, metrics):
    print(f"Heartbeat de {node_id}: {metrics}")

def get_active_nodes():
    """
    Stub que retorna lista de nós ativos com métricas de rede.
    """
    return [
        {
            "node_id": "node_stub",
            "cpu_percent": 4.3,
            "memory_percent": 87.5,
            "boot_time": 1751232721.52868,
            "network_usage_mb": 512.0,
            "network_speed_mbps": 120.0
        },
        {
            "node_id": "node2",
            "cpu_percent": 10.1,
            "memory_percent": 65.2,
            "boot_time": 1751232721.52868,
            "network_usage_mb": 1024.0,
            "network_speed_mbps": 80.0
        }
    ]

def get_peers(node_id):
    """
    Stub: retorna lista de peers conectados a um nó.
    """
    if node_id == "node_stub":
        return ["node2"]
    if node_id == "node2":
        return ["node_stub"]
    return []
