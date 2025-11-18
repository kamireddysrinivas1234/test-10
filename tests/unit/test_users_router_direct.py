
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models                      # ensure user table registered
from app.routers import users as users_mod
from app.schemas import UserCreate
from app import security

def test_router_direct_success_and_list(tmp_path, monkeypatch):
    monkeypatch.setattr(security, "hash_password", lambda _: "H")
    dbfile = Path(tmp_path) / "router.db"
    engine = create_engine(f"sqlite:///{dbfile}")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = SessionLocal()
    payload = UserCreate(username="validuser", email="valid@example.com", password="secret1")
    user = users_mod.create_user(payload, db)
    assert user.username == "validuser"
    users = users_mod.list_users(db)
    assert any(u.username == "validuser" for u in users)
    db.close()
