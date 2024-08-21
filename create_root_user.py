from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import User
from app.services.auth_service import hash_password

def create_root_user(db: Session):
    root_user = db.query(User).filter(User.username == "root").first()
    if not root_user:
        root_user = User(
            name="Root User",
            username="root",
            email="root@teconectapi.it.ao",
            hashed_password=hash_password("22446310"),  # Defina a senha do usuário root
            role="admin",
            is_active=True
        )
        db.add(root_user)
        db.commit()
        db.refresh(root_user)
        print("Root user created successfully")
    else:
        print("Root user already exists")

if __name__ == "__main__":
    with Session(engine) as db:
        create_root_user(db)
