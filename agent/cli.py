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
