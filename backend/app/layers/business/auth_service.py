from datetime import datetime, timedelta, timezone

import secrets

from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    validate_password
)

from app.layers.data.user_repository import UserRepository

from app.layers.models.auth import (
    User,
    UserCreate,
    UserLogin,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest
)


class AuthService:

    # =====================================================
    # REGISTRO
    # =====================================================

    @staticmethod
    def registrar_usuario(
        db: Session,
        data: UserCreate
    ):

        email = str(data.email).strip().lower()

        usuario_existente = UserRepository.obtener_por_email(
            db,
            email
        )

        if usuario_existente:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado."
            )

        validate_password(data.password)

        nuevo_usuario = User(
            nombre=data.nombre.strip(),
            apellido=data.apellido.strip(),
            email=email,
            password_hash=get_password_hash(
                data.password
            ),
            id_rol=1,
            activo=True
        )

        return UserRepository.crear(
            db,
            nuevo_usuario
        )

    # =====================================================
    # LOGIN
    # =====================================================

    @staticmethod
    def login(
        db: Session,
        data: UserLogin
    ):

        email = str(data.email).strip().lower()

        usuario = UserRepository.obtener_por_email(
            db,
            email
        )

        if not usuario:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos."
            )

        if not verify_password(
            data.password,
            usuario.password_hash
        ):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos."
            )

        if not usuario.activo:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos."
            )

        token = create_access_token(
            data={
                "sub": str(usuario.id_usu),
                "email": usuario.email,
                "id_rol": usuario.id_rol,
                "nombre": usuario.nombre
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    # =====================================================
    # CAMBIAR CONTRASEÑA
    # =====================================================

    @staticmethod
    def cambiar_password(
        db: Session,
        usuario: User,
        data: ChangePasswordRequest
    ):

        if not verify_password(
            data.current_password,
            usuario.password_hash
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña actual es incorrecta."
            )

        if data.current_password == data.new_password:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La nueva contraseña debe ser diferente a la actual."
            )

        validate_password(
            data.new_password
        )

        usuario.password_hash = get_password_hash(
            data.new_password
        )

        UserRepository.actualizar(
            db,
            usuario
        )

        return {
            "mensaje": "Contraseña actualizada correctamente."
        }

    # =====================================================
    # RECUPERAR CONTRASEÑA
    # =====================================================

    @staticmethod
    def forgot_password(
        db: Session,
        data: ForgotPasswordRequest
    ):

        email = str(data.email).strip().lower()

        usuario = UserRepository.obtener_por_email(
            db,
            email
        )

        mensaje = (
            "Si el correo está registrado, "
            "se enviaron las instrucciones."
        )

        if not usuario:
            return {
                "mensaje": mensaje
            }

        token = secrets.token_urlsafe(32)

        expiracion = (
            datetime.now(timezone.utc)
            + timedelta(minutes=15)
        )

        usuario.token_recuperacion = token

        # MySQL DATETIME no almacena zona horaria.
        usuario.token_expiracion = (
            expiracion.replace(tzinfo=None)
        )

        UserRepository.actualizar(
            db,
            usuario
        )

        return {
            "mensaje": mensaje,
            "token_desarrollo": token
        }

    # =====================================================
    # RESTABLECER CONTRASEÑA
    # =====================================================

    @staticmethod
    def reset_password(
        db: Session,
        data: ResetPasswordRequest
    ):

        usuario = UserRepository.obtener_por_token(
            db,
            data.token
        )

        if not usuario:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido."
            )

        expiracion = usuario.token_expiracion

        if expiracion is None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El token ya no es válido."
            )

        if expiracion.tzinfo is None:

            expiracion = expiracion.replace(
                tzinfo=timezone.utc
            )

        if datetime.now(
            timezone.utc
        ) > expiracion:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El token expiró."
            )

        validate_password(
            data.new_password
        )

        usuario.password_hash = get_password_hash(
            data.new_password
        )

        # Token de un solo uso
        usuario.token_recuperacion = None
        usuario.token_expiracion = None

        UserRepository.actualizar(
            db,
            usuario
        )

        return {
            "mensaje": "Contraseña actualizada correctamente."
        }