from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine


DB = Path(__file__).parents[2] / "database.db"

SQLITE_URL = f"sqlite:///{str(DB)}"
connect_args = { "check_same_thread": False }
engine = create_engine(SQLITE_URL, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

# def get_session_fastapi():
#     yield get_session()

# SessionDep = Annotated[Session, Depends(get_session_fastapi)]  no need for this right now