from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    email: str
    password_hash: str
    rol_id: int = Field(default=1)
    activo: bool = Field(default=True)
    token_recuperacion: Optional[str] = Field(default=None)
    token_expiracion: Optional[datetime] = Field(default=None)

# Esquemas para autenticación
class UserCreate(SQLModel):
    nombre: str
    apellido: str
    email: str
    password: str

class UserResponse(SQLModel):
    id: int
    nombre: str
    apellido: str
    email: str
    rol_id: int

class Token(SQLModel):
    access_token: str
    token_type: str

class ForgotPasswordRequest(SQLModel):
    email: str

class ResetPasswordRequest(SQLModel):
    token: str
    new_password: str