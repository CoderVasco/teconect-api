from app.database import Base, engine
from app.models import User

# Certifique-se de que o modelo User esteja sendo importado corretamente.
Base.metadata.create_all(bind=engine)
