from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.db.session import get_session
from app.layers.models import User, UserCreate, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token
import secrets
from datetime import datetime, timedelta, timezone
from app.layers.models import User, UserCreate, UserResponse, Token, ForgotPasswordRequest, ResetPasswordRequest
from app.core.security import get_password_hash



router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_session)):
    # Validar si el email ya existe
    existing_user = db.exec(
        select(User).where(User.email == user_in.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado."
        )

    # El sistema arma el registro completo con el hash y el rol por defecto
    db_user = User(
        nombre=user_in.nombre,
        apellido=user_in.apellido,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        rol_id=1,      # Automático por el sistema
        activo=True    # Automático por el sistema
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    # Tu lógica de login sigue aquí...
    user = db.exec(select(User).where(User.email == form_data.username)).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id), 
            "email": user.email, 
            "rol_id": user.rol_id  # <--- Agregamos el rol aquí
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_session)
):
    user = db.exec(select(User).where(User.email == data.email)).first()
    
    if not user:
        return {"mensaje": "Si el correo está registrado, se enviaron las instrucciones."}
    
    token = secrets.token_urlsafe(32)
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    user.token_recuperacion = token
    user.token_expiracion = expiracion
    
    db.add(user)
    db.commit()
    
    return {
        "mensaje": "Instrucciones de recuperación generadas con éxito.",
        "token_desarrollo": token
    }

@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest = Body(...), # <--- Agregamos Body(...) aquí también
    db: Session = Depends(get_session)
):
    
    # 1. Buscar usuario por el token de recuperación
    user = db.exec(
        select(User).where(User.token_recuperacion == data.token)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de recuperación inválido o no encontrado."
        )
    
    # 2. Verificar expiración del token
    # Ajustar zona horaria si aplica
    expiracion = user.token_expiracion
    if expiracion.tzinfo is None:
        expiracion = expiracion.replace(tzinfo=timezone.utc)
        
    if datetime.now(timezone.utc) > expiracion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token de recuperación ha expirado. Solicita uno nuevo."
        )
    
    # 3. Actualizar contraseña y limpiar campos de recuperación
    user.password_hash = get_password_hash(data.new_password)
    user.token_recuperacion = None
    user.token_expiracion = None
    
    db.add(user)
    db.commit()
    
    return {"mensaje": "La contraseña ha sido actualizada correctamente. Ya puedes iniciar sesión."}