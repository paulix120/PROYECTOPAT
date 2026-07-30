from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.db.session import get_session
from app.layers.models import User, UserCreate, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token

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