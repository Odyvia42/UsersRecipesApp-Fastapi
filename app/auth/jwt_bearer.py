from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.jwt_handler import decode_jwt


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid or Expired Token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or Expired Token!")

    def verify_jwt(self, jwtoken: str):
        is_token_valid: bool = False
        payload = decode_jwt(jwtoken)
        if payload:
            is_token_valid = True
        return is_token_valid
