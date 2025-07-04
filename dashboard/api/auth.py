from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from datetime import datetime, timedelta
import jwt

router = APIRouter(prefix="/auth", tags=["auth"])

# Chave secreta para assinar os tokens JWT (em produção, usar variável de ambiente)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

@router.post("/login", response_model=Token)
def login(data: LoginRequest) -> Dict:
    """
    Autentica um usuário e retorna um token JWT.
    Em produção, validar contra banco de dados.
    """
    if not data.username or not data.password:
        raise HTTPException(401, "Credenciais inválidas")
    
    # Em produção, validar credenciais no banco
    # Por enquanto, aceita qualquer usuário/senha
    
    expires = datetime.utcnow() + timedelta(hours=24)
    to_encode = {
        "sub": data.username,
        "exp": expires,
        "type": "access"
    }
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 24 * 3600  # 24 horas em segundos
    }
