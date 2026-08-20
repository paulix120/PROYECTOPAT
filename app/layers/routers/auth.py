from fastapi import APIRouter, Depends, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user
from app.layers.business.auth_service import AuthService
from app.layers.models.auth import (
    User,
    UserCreate,
    UserResponse,
    Token,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
    UserLogin
)


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


# ==========================================
# REGISTRO
# ==========================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_session)
):

    return AuthService.registrar_usuario(
        db,
        data
    )


# ==========================================
# LOGIN - SWAGGER
# ==========================================

@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):

    data = UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    return AuthService.login(
        db,
        data
    )


# ==========================================
# LOGIN JSON - FRONTEND
# ==========================================

@router.post(
    "/login-json",
    response_model=Token
)
def login_json(
    data: UserLogin,
    db: Session = Depends(get_session)
):

    return AuthService.login(
        db,
        data
    )


# ==========================================
# USUARIO ACTUAL
# ==========================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    usuario: User = Depends(get_current_user)
):

    return usuario


# ==========================================
# CAMBIAR CONTRASEÑA
# ==========================================

@router.put(
    "/change-password"
)
def change_password(
    data: ChangePasswordRequest,
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):

    return AuthService.cambiar_password(
        db,
        usuario,
        data
    )


# ==========================================
# FORGOT PASSWORD
# ==========================================

@router.post(
    "/forgot-password"
)
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_session)
):

    return AuthService.forgot_password(
        db,
        data
    )


# ==========================================
# RESET PASSWORD
# ==========================================

@router.post(
    "/reset-password"
)
def reset_password(
    data: ResetPasswordRequest = Body(...),
    db: Session = Depends(get_session)
):

    return AuthService.reset_password(
        db,
        data
    )