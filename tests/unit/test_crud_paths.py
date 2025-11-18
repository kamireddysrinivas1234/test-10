
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError
from app.db import Base
from app import crud, security

def _session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)()

def test_crud_success_and_getters(monkeypatch):
    monkeypatch.setattr(security, "hash_password", lambda _: "H")
    db = _session()
    u = crud.create_user(db, "eve123", "eve@example.com", "secret1")
    assert crud.get_user_by_username(db, "eve123").email == "eve@example.com"
    assert crud.get_user_by_email(db, "eve@example.com").username == "eve123"
    db.close()

class DummySession:
    def __init__(self): self.rollback_called = False
    def add(self, obj): pass
    def commit(self): raise IntegrityError("dup", params=None, orig=None)
    def rollback(self): self.rollback_called = True
    def refresh(self, obj): pass

def test_crud_integrityerror_rollback(monkeypatch):
    monkeypatch.setattr(security, "hash_password", lambda _: "H")
    db = DummySession()
    with pytest.raises(IntegrityError):
        crud.create_user(db, "dup", "dup@example.com", "secret1")
    assert db.rollback_called is True
