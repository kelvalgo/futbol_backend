from datetime import datetime
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel, select
from pathlib import Path
from contextlib import asynccontextmanager

from app.core.enum.rol import Rol
from app.models.user import User
from app.models.group_friends import GroupFriends
from app.models.user_groupf import UserGroupF
from app.core.security.hashing import hash_password



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

            group= GroupFriends(               
                    name="Team 0",
                    description="Team 0",
                    date_creation=datetime.now().strftime("%Y-%m-%d"),
                    perioding_donation=30,
                    activo=True
                    )
            session.add(group)
            session.commit()

            user_group= UserGroupF(
                    user_id=1,
                    group_id=1,
                    rol=Rol.admin,
                    disable=False,
                    fecha_ingreso=datetime.now().strftime("%Y-%m-%d")
                    )
            session.add(user_group)
            session.commit()    

        user2 = session.exec(
            select(User).where(User.username == "user2")
        ).first()
        
        if not user2:
            admin = User(
                username="user2",
                full_name="usuario",
                admin=False,
                disable=False,
                hashed_password=hash_password("user123"),
            )
            session.add(admin)
            session.commit()

            group= GroupFriends(               
                    name="Team 1",
                    description="Team 1",
                    date_creation=datetime.now().strftime("%Y-%m-%d"),
                    perioding_donation=30,
                    activo=True
                    )
            session.add(group)
            session.commit()

            user_group= UserGroupF(
                    user_id=2,
                    group_id=2,
                    rol=Rol.user,
                    disable=False,
                    fecha_ingreso=datetime.now().strftime("%Y-%m-%d")
                    )
            session.add(user_group)
            session.commit()

    yield