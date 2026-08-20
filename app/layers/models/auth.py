from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# ======================================================
# MODELO DE BASE DE DATOS
# ======================================================

class User(SQLModel, table=True):
    __tablename__ = "usuario"

    id_usu: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    nombre: str
    apellido: str

    email: str = Field(
        index=True
    )

    password_hash: str

    id_rol: int = Field(
        default=1
    )

    activo: bool = Field(
        default=True
    )

    token_recuperacion: Optional[str] = None

    token_expiracion: Optional[datetime] = None

    created_at: Optional[datetime] = None


# ======================================================
# DTO CREAR USUARIO
# ======================================================

class UserCreate(SQLModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: str


# ======================================================
# DTO LOGIN
# ======================================================

class UserLogin(SQLModel):
    email: EmailStr
    password: str


# ======================================================
# DTO RESPUESTA
# ======================================================

class UserResponse(SQLModel):
    id_usu: int
    nombre: str
    apellido: str
    email: str
    id_rol: int
    activo: bool


# ======================================================
# TOKEN JWT
# ======================================================

class Token(SQLModel):
    access_token: str
    token_type: str


# ======================================================
# RECUPERAR CONTRASEÑA
# ======================================================

class ForgotPasswordRequest(SQLModel):
    email: EmailStr


class ResetPasswordRequest(SQLModel):
    token: str
    new_password: str


# ======================================================
# CAMBIAR CONTRASEÑA
# ======================================================

class ChangePasswordRequest(SQLModel):
    current_password: str
    new_password: str