from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session

from app.core.config import settings
from app.db.session import get_session
from app.layers.models.auth import User
from app.layers.data.user_repository import UserRepository


# ==========================================
# Esquema OAuth2
# ==========================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ==========================================
# Obtener usuario autenticado
# ==========================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
) -> User:

    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No fue posible validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credenciales_exception

    except JWTError:
        raise credenciales_exception

    usuario = UserRepository.obtener_por_id(
        db,
        int(user_id)
    )

    if usuario is None:
        raise credenciales_exception

    if not usuario.activo:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario se encuentra inactivo."
        )

    return usuario