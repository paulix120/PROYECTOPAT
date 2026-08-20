from typing import Optional

from sqlmodel import Session, select

from app.layers.data.base_repository import BaseRepository
from app.layers.models.auth import User


class UserRepository:

    # ==========================================
    # CONSULTAS
    # ==========================================

    @staticmethod
    def obtener_por_id(
        db: Session,
        usuario_id: int
    ) -> Optional[User]:

        return BaseRepository.obtener_por_id(
            db,
            User,
            usuario_id
        )

    @staticmethod
    def obtener_por_email(
        db: Session,
        email: str
    ) -> Optional[User]:

        return db.exec(
            select(User)
            .where(User.email == email)
        ).first()

    @staticmethod
    def obtener_por_token(
        db: Session,
        token: str
    ) -> Optional[User]:

        return db.exec(
            select(User)
            .where(
                User.token_recuperacion == token
            )
        ).first()

    @staticmethod
    def obtener_usuario_activo(
        db: Session,
        usuario_id: int
    ) -> Optional[User]:

        return db.exec(
            select(User)
            .where(
                User.id_usu == usuario_id,
                User.activo == True
            )
        ).first()

    # ==========================================
    # OPERACIONES
    # ==========================================

    @staticmethod
    def crear(
        db: Session,
        usuario: User
    ):

        return BaseRepository.guardar(
            db,
            usuario
        )

    @staticmethod
    def actualizar(
        db: Session,
        usuario: User
    ):

        return BaseRepository.actualizar(
            db,
            usuario
        )