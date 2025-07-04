README.md

````markdown
# Coexum

## 🚀 Quickstart

```bash
# 1) Clone o repositório
git clone https://github.com/abimaeltech/coexum.git
cd coexum

# 2) Crie e ative um virtualenv
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\Activate     # Windows

# 3) Instale em modo editable
pip install -e .

# 4) Registre um nó de exemplo
coexum node start

# 5) Inicie o scheduler
coexum scheduler

# 6) Rode o dashboard (http://localhost:8000)
coexum dashboard serve

# 7) Teste a API no Swagger UI
open http://localhost:8000/docs
```

## 4. Docker & Docker-Compose
### Dockerfile do Dashboard
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -e .
EXPOSE 8000
CMD ["coexum","dashboard","serve","--host","0.0.0.0"]
```

docker-compose.yml
```yaml
version: "3.8"
services:
  dashboard:
    build: .
    ports:
      - "8000:8000"
  scheduler:
    build: .
    command: coexum scheduler
  node:
    build: .
    command: coexum node start
```

Coloque esses arquivos na raiz e documente no README.

## 5. CI/CD básico com GitHub Actions
Crie `.github/workflows/ci.yml`:

```yaml
name: CI

on: [push, pull_request]

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v5
        with: python-version: 3.12
      - name: Install deps
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install -e .[test]
      - name: Run lint
        run: flake8 .
      - name: Run tests
        run: pytest --maxfail=1 --disable-warnings -q
```

## 6. Publicação no PyPI
Configure `~/.pypirc` com suas credenciais PyPI.

Gere sdist/wheel e faça upload com twine:

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

---

## 📦 Instalação

### From source
```bash
# Clone e instale em modo editável
git clone https://github.com/potiguarailab/coexum.git
cd coexum
pip install -e .
# alternativa: via script de instalação
source agent/install.sh
````

### Binário via script

#### Linux/macOS

```bash
curl -sSL https://coexum.org/install.sh | bash
```

#### Windows (PowerShell)

```powershell
iwr -useb https://coexum.org/install.ps1 | iex
```

---

## ⚙️ Uso Básico

```bash
# Iniciar o nó local
coexum node start

# Servir dashboard web
coexum dashboard serve
```

---

## 📚 Documentação & Recursos

* White Paper técnico: `docs/WhitePaper.md`
* Guia de Contribuição: `CONTRIBUTING.md`
* Issue Tracker: [https://github.com/potiguarailab/coexum/issues](https://github.com/potiguarailab/coexum/issues)

---

## 🤝 Como Contribuir

1. Fork do repositório
2. Branch (`feature/<nome>`)
3. Commit e PR para `main`
4. Revisão e merge

---

## 📄 Licença

MIT License — veja `LICENSE`

````

---

## setup.py
```python
from setuptools import setup, find_packages

setup(
    name="coexum",
    version="0.1.0",
    description="Rede descentralizada de IA - Potiguar AI Lab",
    packages=find_packages(exclude=['tests', 'docs']),
    entry_points={
        'console_scripts': [
            'coexum=agent.cli:main',
        ],
    },
    install_requires=[
        'typer>=0.6',
        'psutil>=5.9',
        'fastapi>=0.85',
        'uvicorn>=0.18',
        'websockets>=10.4',
        'requests>=2.28',
        'web3>=6.0',
        'docker>=6.0',
        'pydantic>=1.10'
    ],
    python_requires='>=3.10',
)
````

---

## coexum.json (template)

```json
{
  "node_id": "",                    // ID gerado no registro
  "api_port": 8000,                  // Porta da API e dashboard
  "p2p_port": 9000,                  // Porta P2P para WebSockets
  "registry_url": "https://registry.coexum.org",
  "blockchain_rpc": "https://polygon-rpc.com"
}
```

---

# Módulos de Código

### agent/install.sh

```bash
#!/usr/bin/env bash
# Instala dependências em Linux/macOS e configura alias
set -e
sudo apt update && sudo apt install -y python3 python3-pip docker.io git
pip3 install -e .
echo "alias coexum='python3 -m coexum'" >> ~/.bashrc
source ~/.bashrc
```

### agent/install.ps1

```powershell
# PowerShell installer para Windows
Set-ExecutionPolicy Bypass -Scope Process -Force
choco install python3 docker-desktop git -y
pip install -e .
Add-Content -Path $PROFILE -Value "Set-Alias coexum python -m coexum"
```

### agent/cli.py

```python
import typer
from agent.node import start_node
from dashboard.api.main import serve_dashboard
from orchestrator.scheduler import schedule_jobs

app = typer.Typer(help="CLI do Coexum: gerencie nós e dashboard")

@app.command()
def node(action: str = typer.Argument(..., help="start|stop")):
    """Controla o ciclo de vida do nó Coexum"""
    if action == 'start':
        start_node()
    else:
        typer.secho("Ação não suportada.", fg=typer.colors.RED)

@app.command()
def dashboard():
    """Inicia o dashboard web"""
    serve_dashboard()

@app.command()
def scheduler():
    """Executa o orquestrador de tarefas"""
    schedule_jobs()

def main():
    app()

if __name__ == '__main__':
    main()
```

### agent/node.py

```python
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
```

### agent/metrics.py

```python
"""
Coleta métricas locais de CPU, memória e uptime.
"""
import psutil

def collect_metrics() -> dict:
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'boot_time': psutil.boot_time(),
    }
```

(continua nos módulos `orchestrator/`, `models/`, `dashboard/` e `cxm_token/`...)

---

*Este nível técnico inclui docstrings, tipagem mínima, comentários e estrutura clara para cada componente.*
