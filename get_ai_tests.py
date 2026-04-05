"""Test Layer: GET /api/1/:sellerID/item (GET-AI-001 … GET-AI-006)."""

from __future__ import annotations

import json

import allure
import pytest

from api_client import AvitoApiClient
from domain import ItemDomain
from helpers import assert_json_error_400, attach_request_response, find_seller_with_empty_list


@pytest.fixture
def list_body(session_seller_id: int) -> dict:
    return {
        "sellerID": session_seller_id,
        "name": "GET",
        "price": 4000,
        "statistics": {"likes": 11, "viewCount": 22, "contacts": 33},
    }


@pytest.fixture
def stable_body(session_seller_id: int) -> dict:
    return {
        "sellerID": session_seller_id,
        "name": "Стабильный список",
        "price": 50,
        "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
    }


@allure.epic("API объявлений")
@allure.feature("GET /api/1/:sellerID/item")
class TestGetSellerItemsPositive:
    @allure.story("Позитивные")
    @allure.title("GET-AI-001: список продавца с объявлениями")
    @allure.testcase("GET-AI-001")
    def test_get_ai_001_seller_has_items(
        self, domain: ItemDomain, list_body: dict, session_seller_id: int
    ) -> None:
        domain.create_item(list_body)
        domain.create_item(list_body)
        _, items = domain.list_seller_items(session_seller_id)
        assert len(items) >= 2
        for it in items:
            assert it.sellerId == session_seller_id

    @allure.story("Позитивные")
    @allure.title("GET-AI-002: продавец без объявлений — пустой массив")
    @allure.testcase("GET-AI-002")
    def test_get_ai_002_empty_seller(self, api_client: AvitoApiClient) -> None:
        try:
            sid = find_seller_with_empty_list(api_client)
        except RuntimeError as e:
            pytest.skip(str(e))
        r = api_client.get_seller_items(sid)
        attach_request_response("GET", api_client.url(f"/api/1/{sid}/item"), r, None)
        assert r.status_code == 200
        assert r.json() == []


@allure.epic("API объявлений")
@allure.feature("GET /api/1/:sellerID/item")
class TestGetSellerItemsNegative:
    @allure.story("Негативные")
    @allure.title("GET-AI-003: sellerID = abc в path")
    @allure.testcase("GET-AI-003")
    def test_get_ai_003_seller_not_int(self, api_client: AvitoApiClient) -> None:
        r = api_client.get_seller_items("abc")
        attach_request_response("GET", api_client.url("/api/1/abc/item"), r, None)
        assert_json_error_400(r, "передан некорректный идентификатор продавца")

    @allure.story("Негативные")
    @allure.title("GET-AI-004: sellerID = 0")
    @allure.testcase("GET-AI-004")
    @pytest.mark.xfail(reason="BUG-002: см. BUGS.md — sellerID 0 и 400", strict=False)
    def test_get_ai_004_seller_zero(self, api_client: AvitoApiClient) -> None:
        r = api_client.get_seller_items(0)
        attach_request_response("GET", api_client.url("/api/1/0/item"), r, None)
        assert_json_error_400(r, "передан некорректный идентификатор продавца")

    @allure.story("Негативные")
    @allure.title("GET-AI-005: sellerID = -1")
    @allure.testcase("GET-AI-005")
    @pytest.mark.xfail(reason="BUG-002: см. BUGS.md — отрицательный sellerID и 400", strict=False)
    def test_get_ai_005_seller_negative(self, api_client: AvitoApiClient) -> None:
        r = api_client.get_seller_items(-1)
        attach_request_response("GET", api_client.url("/api/1/-1/item"), r, None)
        assert_json_error_400(r, "передан некорректный идентификатор продавца")


@allure.epic("API объявлений")
@allure.feature("GET /api/1/:sellerID/item")
class TestGetSellerItemsCorner:
    @allure.story("Корнер-кейсы")
    @allure.title("GET-AI-006: два GET списка подряд — идентичное тело")
    @allure.testcase("GET-AI-006")
    def test_get_ai_006_idempotent_list(
        self,
        domain: ItemDomain,
        api_client: AvitoApiClient,
        stable_body: dict,
        session_seller_id: int,
    ) -> None:
        domain.create_item(stable_body)
        url = api_client.url(f"/api/1/{session_seller_id}/item")
        r1 = api_client.get_seller_items(session_seller_id)
        attach_request_response("GET", url, r1, None)
        r2 = api_client.get_seller_items(session_seller_id)
        attach_request_response("GET", url, r2, None)
        assert r1.status_code == 200 and r2.status_code == 200
        assert json.dumps(r1.json(), sort_keys=True) == json.dumps(r2.json(), sort_keys=True)
