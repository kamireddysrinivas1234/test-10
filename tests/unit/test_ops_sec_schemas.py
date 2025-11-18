
import math, pytest
from app import operations as ops
from app.security import hash_password, verify_password
from pydantic import ValidationError
from app.schemas import CalcRequest, UserCreate

def test_operations_all():
    assert ops.add(2,3)==5
    assert ops.subtract(7,2)==5
    assert ops.multiply(3,4)==12
    assert ops.divide(9,3)==3
    with pytest.raises(ZeroDivisionError): ops.divide(1,0)
    assert math.isclose(ops.divide(1,4),0.25,rel_tol=1e-9)

def test_security_hash_and_verify(monkeypatch):
    class StubCtx:
        def hash(self, s): return f"stub::{s}"
        def verify(self, s, h): return h == f"stub::{s}"
    import app.security as sec
    monkeypatch.setattr(sec, "pwd_context", StubCtx())
    h = hash_password("secret1")
    assert verify_password("secret1", h) and not verify_password("nope", h)

def test_schemas_validator_and_valid():
    _ = UserCreate(username="alice", email="alice@example.com", password="secret1")
    with pytest.raises(ValidationError):
        CalcRequest(a=1,b=2,op="pow")
