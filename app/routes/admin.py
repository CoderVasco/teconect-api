from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db
from app.models import User
from app.services.auth_service import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

# Configuração do Limiter
limiter = Limiter(key_func=get_remote_address)

@router.get("/users")
@limiter.limit("10/minute")  # Limita a 10 requisições por minuto
def get_users(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "root"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    users = db.query(User).all()
    return users

@router.get("/users/total")
@limiter.limit("5/minute")  # Limita a 5 requisições por minuto
def get_total_users(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "root"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    total_users = db.query(func.count(User.id)).scalar()
    return {"total_users": total_users}

@router.get("/users/online")
@limiter.limit("5/minute")  # Limita a 5 requisições por minuto
def get_online_users(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "root"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    # Considerando um usuário online se a última atividade foi nos últimos 5 minutos
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    online_users = db.query(User).filter(User.last_activity >= five_minutes_ago, User.is_active == True).count()
    return {"online_users": online_users}

@router.put("/users/{user_id}/suspend")
@limiter.limit("3/minute")  # Limita a 3 requisições por minuto
def suspend_user(user_id: int, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "root"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.commit()
    return {"message": f"User {user.username} suspended successfully"}

@router.put("/users/{user_id}/activate")
@limiter.limit("3/minute")  # Limita a 3 requisições por minuto
def activate_user(user_id: int, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "root"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()
    db.refresh(user)
    return {"message": f"User {user.username} activated successfully"}

@router.delete("/users/{user_id}")
@limiter.limit("3/minute")  # Limita a 3 requisições por minuto
def delete_user(user_id: int, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "root"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": f"User {user.username} deleted successfully"}

@router.put("/users/{user_id}/edit")
@limiter.limit("3/minute")  # Limita a 3 requisições por minuto
def edit_user(user_id: int, request: Request, name: str | None = None, email: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "root"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if name:
        user.name = name
    if email:
        # Verificar se o novo e-mail já está em uso por outro usuário
        existing_user = db.query(User).filter(User.email == email, User.id != user.id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = email
    
    db.commit()
    return {"message": f"User {user.username} updated successfully"}
