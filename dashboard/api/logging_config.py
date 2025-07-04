"""
Configuração de logging para a API.
"""
import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    # Criar diretório de logs se não existir
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Nome do arquivo com timestamp
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"coexum-api-{today}.log")
    
    # Configuração do logger raiz
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Handler para arquivo com rotação
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10_485_760,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(file_handler)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(levelname)s: %(message)s"
    ))
    logger.addHandler(console_handler)
    
    return logger
