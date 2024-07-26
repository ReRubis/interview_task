from pydantic import BaseModel


class TokenOut(BaseModel):
    access_token: str


class DecodedToken(BaseModel):
    id: int
    iss: str
    sub: str | int
    type: str
    jti: str
    iat: int
    nbf: int
