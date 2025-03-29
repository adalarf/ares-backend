from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Импортируем Base
from app.database import Base
from app.auth.models import *  # Это импортирует все модели

# Остальной код env.py...
target_metadata = Base.metadata 