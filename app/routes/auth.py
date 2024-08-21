from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db
from app.models import User
from app.services.auth_service import get_current_user  # Importando serviços de autenticação
from app.auth_utils import create_access_token, hash_password, verify_password  # Importando utilitários
from datetime import datetime, timedelta  # Importando datetime e timedelta

router = APIRouter()

# Configuração do Limiter
limiter = Limiter(key_func=get_remote_address)

# Classe para definir a estrutura dos dados de entrada no registro
class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

# Classe para a atualização dos dados do usuário
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

# Classe para a estrutura dos dados de entrada no login
class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
@limiter.limit("5/minute")  # Limita a 5 registros por minuto
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(name=user.name, username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/login")
@limiter.limit("10/minute")  # Limita a 10 tentativas de login por minuto
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is suspended")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/admin/users/{user_id}/edit")
@limiter.limit("5/minute")  # Limita a 5 edições por minuto
def update_user(request: Request, user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin" and current_user.role != "root":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_update.name:
        user.name = user_update.name
    if user_update.email:
        # Verificar se o novo e-mail já está em uso
        db_user = db.query(User).filter(User.email == user_update.email).first()
        if db_user and db_user.id != user.id:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = user_update.email
    if user_update.password:
        user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": user}

@router.get("/me")
@limiter.limit("10/minute")  # Limita a 10 requisições por minuto
def read_users_me(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.last_activity = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/me")
@limiter.limit("5/minute")  # Limita a 5 atualizações por minuto
def update_user(request: Request, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_update.name:
        current_user.name = user_update.name
    if user_update.email:
        # Verificar se o novo e-mail já está em uso
        db_user = db.query(User).filter(User.email == user_update.email).first()
        if db_user and db_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = user_update.email
    if user_update.password:
        current_user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(current_user)
    return {"message": "User updated successfully", "user": current_user}

@router.delete("/me")
@limiter.limit("3/minute")  # Limita a 3 exclusões por minuto
def delete_user(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.get("/users/total")
@limiter.limit("5/minute")  # Limita a 5 requisições por minuto
def get_total_users(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin" and current_user.role != "root":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    total_users = db.query(User).count()
    return {"total_users": total_users}

@router.get("/users/online")
@limiter.limit("5/minute")  # Limita a 5 requisições por minuto
def get_online_users(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin" and current_user.role != "root":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    # Aqui, online users são definidos como aqueles que fizeram login nos últimos 15 minutos.
    time_threshold = datetime.utcnow() - timedelta(minutes=15)
    online_users = db.query(User).filter(User.last_login >= time_threshold).count()

    return {"online_users": online_users}
