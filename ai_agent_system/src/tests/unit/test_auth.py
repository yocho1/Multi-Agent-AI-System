import pytest

from src.utils.auth import hash_password, verify_password, create_access_token, decode_access_token, api_key_store


def test_password_hashing():
    pwd = "secure_password"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed)
    assert not verify_password("wrong_password", hashed)


def test_jwt_token():
    token = create_access_token({"sub": "user123", "scopes": ["read"]})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["scopes"] == ["read"]


def test_jwt_invalid_token():
    payload = decode_access_token("invalid.token.here")
    assert payload is None


def test_api_key_store():
    store = api_key_store
    assert store.validate_key("demo-key-12345")
    assert not store.validate_key("invalid-key")
    perms = store.get_permissions("demo-key-12345")
    assert "read" in perms
    assert "write" in perms
