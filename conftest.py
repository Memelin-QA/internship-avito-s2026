"""Pytest-фикстуры: клиент API, domain-слой, базовый URL."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from api_client import AvitoApiClient
from domain import ItemDomain
from helpers import random_seller_id


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Добавляет environment.properties в allure-results для отчёта."""
    raw = getattr(session.config.option, "allure_report_dir", None) or "allure-results"
    results_dir = Path(raw)
    if not results_dir.is_absolute():
        results_dir = Path(session.config.rootpath) / results_dir
    try:
        results_dir.mkdir(parents=True, exist_ok=True)
        base = os.environ.get("API_BASE_URL", "https://qa-internship.avito.com")
        lines = [
            f"API_BASE_URL={base}",
            "Framework=pytest",
            "Language=python",
        ]
        (results_dir / "environment.properties").write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )
    except OSError:
        pass


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get("API_BASE_URL", "https://qa-internship.avito.com")


@pytest.fixture(scope="session")
def api_client(base_url: str) -> AvitoApiClient:
    return AvitoApiClient(base_url=base_url)


@pytest.fixture(scope="session")
def session_seller_id() -> int:
    """Один sellerID на сессию pytest в диапазоне 111111–999999 (меньше пересечений на общем стенде)."""
    return random_seller_id()


@pytest.fixture
def speed_body(session_seller_id: int) -> dict:
    """Тело POST для NFR и сценариев «скорость»."""
    return {
        "sellerID": session_seller_id,
        "name": "Скорость",
        "price": 2000,
        "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
    }


@pytest.fixture
def domain(api_client: AvitoApiClient) -> ItemDomain:
    return ItemDomain(api_client)


@pytest.fixture
def nfr_max_ms() -> float:
    return float(os.environ.get("NFR_MAX_MS", "500"))
