# config.py

import os

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "22446310")  # Busca pela SECRET_KEY nas variáveis de ambiente, ou usa um valor padrão
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")  # Também pode configurar o banco de dados via variável de ambiente

settings = Settings()
