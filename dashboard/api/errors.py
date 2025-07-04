"""
Tipos de erro personalizados e handlers de exceção.
"""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Dict

class CoexumError(Exception):
    """Erro base para exceções personalizadas da Coexum."""
    def __init__(self, message: str, code: int = 400, details: Dict[str, Any] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)

class NodeNotFoundError(CoexumError):
    """Nó não encontrado no registro."""
    def __init__(self, node_id: str):
        super().__init__(
            message=f"Nó '{node_id}' não encontrado",
            code=404,
            details={"node_id": node_id}
        )

class ValidationError(CoexumError):
    """Erro de validação de dados."""
    def __init__(self, message: str, field: str):
        super().__init__(
            message=message,
            code=400,
            details={"field": field}
        )

class AuthenticationError(CoexumError):
    """Erro de autenticação."""
    def __init__(self, message: str = "Não autorizado"):
        super().__init__(message=message, code=401)

async def coexum_exception_handler(request: Request, exc: CoexumError):
    """Handler global para exceções da Coexum."""
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
            "path": request.url.path
        }
    )
