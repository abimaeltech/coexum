from fastapi import FastAPI, HTTPException, Body, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from uuid import uuid4
from .settings import settings
from .network import router as network_router
from .auth import router as auth_router

app = FastAPI(
    title="🕸️ Coexum Dashboard API",
    description="API para status, nós, tarefas e rede na Coexum.",
    version="1.2.0",
    docs_url=None,
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Frontend Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema de segurança
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Middleware de autenticação.
    Em produção, validar o token JWT e retornar o usuário.
    """
    token = credentials.credentials
    # TODO: Validar token JWT
    return {"username": "user"}  # stub

# ———————————————— MODELS —————————————————

class NodeInfo(BaseModel):
    node_id: str
    cpu_percent: float
    memory_percent: float
    boot_time: float

class NodeRegister(BaseModel):
    node_id: str = Field(..., description="ID do nó", examples=["node3"])
    # opcionalmente mais campos: ip, hostname, ...

class Task(BaseModel):
    task_id: str
    node_id: str
    payload: Dict[str, Any]

class TaskCreate(BaseModel):
    node_id: str = Field(..., description="ID do nó", examples=["node3"])
    payload: Dict[str, Any] = Field(..., description="Payload da tarefa", examples=[{"action": "train", "model": "resnet"}])

# —————————————— IN‐MEMORY DBs —————————————————

NODE_REGISTRY: Dict[str, NodeInfo] = {}
TASK_STORE: List[Task] = []

# —————————————— STATUS & NODES —————————————————

@app.get("/status", response_model=Dict[str,str])
def get_status():
    """Retorna o status geral da rede Coexum."""
    return {"status": "Coexum online"}

@app.get("/nodes", response_model=List[NodeInfo], dependencies=[Depends(get_current_user)])
def list_nodes():
    """Retorna a lista de nós ativos e suas métricas."""
    return list(NODE_REGISTRY.values())

@app.post(
    "/nodes",
    response_model=NodeInfo,
    status_code=201,
    summary="Registra um novo nó",
    description="Adiciona um nó à rede Coexum.",
)
def register_node(data: NodeRegister = Body(..., examples=[{"node_id": "node3"}])):
    if data.node_id in NODE_REGISTRY:
        raise HTTPException(409, f"Node '{data.node_id}' já cadastrado")
    info = NodeInfo(node_id=data.node_id, cpu_percent=0.0, memory_percent=0.0, boot_time=0.0)
    NODE_REGISTRY[data.node_id] = info
    return info

@app.get("/nodes/{node_id}", response_model=NodeInfo)
def get_node(node_id: str):
    node = NODE_REGISTRY.get(node_id)
    if not node:
        raise HTTPException(404, f"Node '{node_id}' não encontrado")
    return node

@app.delete("/nodes/{node_id}", status_code=204)
def delete_node(node_id: str):
    if node_id not in NODE_REGISTRY:
        raise HTTPException(404, f"Node '{node_id}' não encontrado")
    del NODE_REGISTRY[node_id]

# —————————————— TASKS —————————————————

@app.get(
    "/tasks",
    response_model=List[Task],
    summary="Lista tarefas pendentes",
)
def list_tasks():
    """
    Retorna a lista de tarefas pendentes na fila.
    """
    return TASK_STORE

@app.post(
    "/tasks",
    response_model=Task,
    status_code=201,
    summary="Cria uma nova tarefa",
    description="Cria uma tarefa para um nó registrado.",
)
def create_task(request: TaskCreate = Body(..., examples=[{"node_id": "node3", "payload": {"action": "train", "model": "resnet"}}])):
    if request.node_id not in NODE_REGISTRY:
        raise HTTPException(404, f"Node '{request.node_id}' não existe")
    task_id = uuid4().hex
    task = Task(task_id=task_id, node_id=request.node_id, payload=request.payload)
    TASK_STORE.append(task)
    return task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    for t in TASK_STORE:
        if t.task_id == task_id:
            return t
    raise HTTPException(404, f"Tarefa '{task_id}' não encontrada")

app.include_router(network_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "dashboard.api.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        log_level="info",
    )

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1.0" />
  <title>Coexum - Monitoramento da Rede</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@3.4.1/dist/tailwind.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body { background: #f3f4f6; }
    .card { background: #fff; border-radius: 0.5rem; box-shadow: 0 2px 8px #0001; }
  </style>
</head>
<body class="min-h-screen flex flex-col">
  <header class="bg-indigo-700 text-white p-6 shadow">
    <h1 class="text-3xl font-bold">Coexum - Monitoramento da Rede</h1>
    <p class="mt-2 text-indigo-100">Acompanhe o status e a topologia da rede em tempo real</p>
  </header>
  <main class="flex-1 max-w-5xl mx-auto p-6">
    <section class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8" id="cards">
      <div class="card p-4 text-center">
        <h2 class="text-gray-500 text-sm">Nós ativos</h2>
        <p id="total_nodes" class="text-3xl font-bold">--</p>
      </div>
      <div class="card p-4 text-center">
        <h2 class="text-gray-500 text-sm">Consumo total (MB)</h2>
        <p id="total_mb" class="text-3xl font-bold">--</p>
      </div>
      <div class="card p-4 text-center">
        <h2 class="text-gray-500 text-sm">Consumo total (GB)</h2>
        <p id="total_gb" class="text-3xl font-bold">--</p>
      </div>
      <div class="card p-4 text-center">
        <h2 class="text-gray-500 text-sm">Velocidade média (Mbps)</h2>
        <p id="avg_speed" class="text-3xl font-bold">--</p>
      </div>
    </section>
    <section class="mb-8">
      <h2 class="text-xl font-semibold mb-2">Histórico de Velocidade Média</h2>
      <canvas id="speedChart" height="80"></canvas>
    </section>
    <section>
      <h2 class="text-xl font-semibold mb-2">Topologia da Rede</h2>
      <div id="topology" class="card p-4 overflow-x-auto">
        <table class="min-w-full text-sm text-left">
          <thead>
            <tr>
              <th class="font-semibold">Nó</th>
              <th class="font-semibold">Conexões</th>
            </tr>
          </thead>
          <tbody id="topology_table"></tbody>
        </table>
      </div>
    </section>
  </main>
  <footer class="text-center text-gray-400 py-4 text-xs">
    &copy; 2025 Coexum. Todos os direitos reservados.
  </footer>
  <script>
    // Função para buscar e atualizar os dados da rede
    async function updateNetwork() {
      try {
        // Resumo
        const summary = (await axios.get('/network/summary')).data;
        document.getElementById('total_nodes').textContent = summary.total_nodes;
        document.getElementById('total_mb').textContent = summary.total_data_mb;
        document.getElementById('total_gb').textContent = summary.total_data_gb;
        document.getElementById('avg_speed').textContent = summary.avg_speed_mbps;

        // Histórico de velocidade (simulado)
        window.speedHistory = window.speedHistory || [];
        window.speedHistory.push({ x: new Date().toLocaleTimeString(), y: summary.avg_speed_mbps });
        if (window.speedHistory.length > 20) window.speedHistory.shift();
        speedChart.data.labels = window.speedHistory.map(p => p.x);
        speedChart.data.datasets[0].data = window.speedHistory.map(p => p.y);
        speedChart.update();

        // Topologia
        const topo = (await axios.get('/network/topology')).data;
        const table = document.getElementById('topology_table');
        table.innerHTML = '';
        topo.nodes.forEach(n => {
          const peers = topo.links.filter(l => l.source === n.id).map(l => l.target).join(', ') || '—';
          table.innerHTML += `<tr>
            <td class="py-1 pr-4">${n.id}</td>
            <td class="py-1">${peers}</td>
          </tr>`;
        });
      } catch (e) {
        document.getElementById('cards').innerHTML = '<div class="col-span-4 text-center text-red-500">Erro ao buscar dados da API</div>';
      }
    }

    // Gráfico de velocidade média
    const ctx = document.getElementById('speedChart').getContext('2d');
    const speedChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: 'Mbps',
          data: [],
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99,102,241,0.1)',
          tension: 0.3,
          fill: true,
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      }
    });

    // Atualiza a cada 5 segundos
    updateNetwork();
    setInterval(updateNetwork, 5000);
  </script>
</body>
</html>
