from logging import config
from sqlalchemy import create_engine
from app.core.config import Base  # or wherever your Base is
from alembic import context

# Replace async engine with synchronous
DATABASE_URL = "postgresql://postgres:postgres@localhost/mi_db"  # Sync connection URL

# Sync Engine for Alembic
engine = create_engine(DATABASE_URL, echo=True)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
