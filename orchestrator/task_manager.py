"""
Gerencia a distribuição de jobs entre nós ativos (stub).
"""
import time
from orchestrator.node_registry import get_active_nodes
from orchestrator.network import send_task

def dispatch_tasks():
    nodes = get_active_nodes()
    print(f"✅ Dispatching {len(nodes)} task(s) to {len(nodes)} node(s)")
    for node in nodes:
        # Exemplo de payload
        task = {
            'task_id': f"task_{int(time.time())}",
            'type': 'inference',
            'model': 'tinyllm',
            'prompt': 'Olá, Coexum!'
        }
        send_task(node, task)
