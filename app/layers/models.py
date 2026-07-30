from typing import Optional
from sqlmodel import SQLModel, Field

# 1. Representación de la tabla en MySQL (incluye todos los campos de la BD)
class User(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    email: str = Field(unique=True, index=True)
    password_hash: str
    rol_id: int = Field(default=1)
    activo: bool = Field(default=True)


# 2. LO QUE LE PEDIMOS AL USUARIO (Solo 4 datos)
class UserCreate(SQLModel):
    nombre: str
    apellido: str
    email: str
    password: str


# 3. Lo que le respondemos al usuario cuando se registra con éxito
class UserResponse(SQLModel):
    id: int
    nombre: str
    apellido: str
    email: str


# 4. Estructura de la respuesta del Login
class Token(SQLModel):
    access_token: str
    token_type: str