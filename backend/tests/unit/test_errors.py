from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.errors import AppError, register_error_handlers


def _make_app() -> FastAPI:
    app = FastAPI()
    register_error_handlers(app)

    @app.get("/not-found")
    def not_found() -> None:
        raise AppError("NOT_FOUND", "Not found.", 404)

    @app.get("/items/{n}")
    def item(n: int) -> dict[str, int]:
        return {"n": n}

    @app.get("/boom")
    def boom() -> None:
        raise RuntimeError("password=xyz")

    return app


def test_app_error_envelope() -> None:
    client = TestClient(_make_app())

    response = client.get("/not-found")

    assert response.status_code == 404
    assert response.json() == {
        "error": {"code": "NOT_FOUND", "message": "Not found.", "details": {}}
    }


def test_validation_error_envelope_has_fields() -> None:
    client = TestClient(_make_app())

    response = client.get("/items/abc")

    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert error["message"] == "Invalid request."
    assert error["details"]["fields"][0]["loc"] == ["path", "n"]
    assert "abc" not in response.text


def test_unhandled_error_hides_details() -> None:
    client = TestClient(_make_app(), raise_server_exceptions=False)

    response = client.get("/boom")

    assert response.status_code == 500
    assert response.json() == {
        "error": {"code": "INTERNAL_ERROR", "message": "Unexpected error.", "details": {}}
    }
    assert "xyz" not in response.text
    