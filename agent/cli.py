import typer
from agent.node import start_node, stop_node  # supondo que existam
from orchestrator.scheduler import schedule_jobs
from dashboard.api.main import app as dashboard_app  # FastAPI app

cli = typer.Typer()
node_app = typer.Typer()
dashboard_cli = typer.Typer()
scheduler_app = typer.Typer()

cli.add_typer(node_app, name="node")
cli.add_typer(dashboard_cli, name="dashboard")
cli.add_typer(scheduler_app, name="scheduler")

@node_app.command("start")
def node_start():
    """Inicia um nó Coexum (envia heartbeat)."""
    start_node()

@node_app.command("stop")
def node_stop():
    """Para o nó Coexum."""
    stop_node()

@scheduler_app.callback(invoke_without_command=True)
def scheduler():
    """Executa o orquestrador de tarefas."""
    schedule_jobs()

@dashboard_cli.command("serve")
def dashboard_serve():
    """
    Inicia o dashboard web (FastAPI + Uvicorn).
    """
    import uvicorn
    # Executa o FastAPI app definido em dashboard/api/main.py
    uvicorn.run(
        dashboard_app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )

@dashboard_cli.command("front")
def dashboard_front():
    """
    Inicia o frontend React (Vite + Tailwind) em modo dev.
    """
    import subprocess, os
    cwd = os.path.join(os.getcwd(), "dashboard", "frontend")
    subprocess.run("npm run dev", cwd=cwd, check=True, shell=True)

if __name__ == "__main__":
    cli()
