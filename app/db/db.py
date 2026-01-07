from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel, select
from pathlib import Path
from contextlib import asynccontextmanager

from app.models.user import User
from app.core.hashing import hash_password


BASE_DIR = Path(__file__).resolve().parent.parent
sqlite_path = BASE_DIR / "db" / "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_path}"

#print("📂 SQLITE PATH REAL:", sqlite_path)
#print("📂 EXISTE?:", sqlite_path.exists())

#engine = create_engine(sqlite_url, echo=True)
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session

sessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app):
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        admin = session.exec(
            select(User).where(User.username == "admin")
        ).first()

        if not admin:
            admin = User(
                username="admin",
                full_name="Administrador",
                admin=True,
                disable=False,
                hashed_password=hash_password("admin123"),
            )
            session.add(admin)
            session.commit()

    yield