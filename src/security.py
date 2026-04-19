import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from src.config import settings

SECRET = settings.secret_key
ALGORITHM = settings.algorithm

# 1. Modelo para os dados DENTRO do token (Payload)
class AccessTokenPayload(BaseModel):
    iss: str
    sub: int  # Aqui fica o user_id
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str

# 2. Modelo para a RESPOSTA do login (JSON de saída)
class JWTResponse(BaseModel):
    access_token: str

def sign_jwt(user_id: int) -> dict:
    now = time.time()
    payload = {
        "iss": "desafio-bank.com.br",
        "sub": int(user_id), 
        "aud": "desafio-bank",
        "exp": now + (60 * 30),  # 30 minutos
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token}

async def decode_jwt(token: str) -> AccessTokenPayload | None:
    try:
        # Decodifica e valida a assinatura
        decoded_token = jwt.decode(token, SECRET, audience="desafio-bank", algorithms=[ALGORITHM])
        # Transforma o dicionário decodificado no objeto de Payload
        payload = AccessTokenPayload.model_validate(decoded_token)
        
        # Verifica expiração manualmente (opcional, o jwt.decode já faz isso)
        if payload.exp >= time.time():
            return payload
        return None
    except Exception:
        return None

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> AccessTokenPayload:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if credentials:
            if not scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Esquema de autenticação inválido.",
                )

            payload = await decode_jwt(credentials)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido ou expirado.",
                )
            return payload # Retorna o objeto validado
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cabeçalho de autorização ausente.",
            )

async def get_current_user(
    payload: Annotated[AccessTokenPayload, Depends(JWTBearer())],
) -> dict[str, int]:
    # Agora acessamos .sub diretamente do objeto validado
    return {"user_id": payload.sub}

def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    return current_user