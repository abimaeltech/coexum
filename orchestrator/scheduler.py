"""
Agendador principal: dispara o dispatch de tarefas em intervalos regulares.
"""
import time
from orchestrator.task_manager import dispatch_tasks

# intervalo entre rodadas de dispatch (em segundos)
SCHEDULE_INTERVAL = 30

def schedule_jobs():
    print("🚀 Agendador de tarefas iniciado")
    while True:
        print(f"⏱ Dispatching tasks at {time.strftime('%X')}...")
        dispatch_tasks()
        time.sleep(SCHEDULE_INTERVAL)
