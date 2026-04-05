"""Test Layer: GET /api/1/item/:id (GET-OI-001 - GET-OI-004)."""

from __future__ import annotations

import allure
import pytest

from api_client import AvitoApiClient
from domain import ItemDomain
from helpers import (
    assert_get_item_not_found,
    assert_json_error_400,
    random_int_non_uuid,
    random_uuid_str,
)
from models import parse_item_from_get_payload


@pytest.fixture
def pre_body(session_seller_id: int) -> dict:
    return {
        "sellerID": session_seller_id,
        "name": "GET",
        "price": 4000,
        "statistics": {"likes": 11, "viewCount": 22, "contacts": 33},
    }


@allure.epic("API объявлений")
@allure.feature("GET /api/1/item/:id")
class TestGetItemByIdPositive:
    @allure.story("Позитивные")
    @allure.title("GET-OI-001: существующий id")
    @allure.description(
        "Данные GET совпадают с POST по полям name, price, sellerId, statistics, createdAt."
    )
    @allure.testcase("GET-OI-001")
    def test_get_oi_001_existing_id(self, domain: ItemDomain, pre_body: dict) -> None:
        _, created = domain.create_item(pre_body)
        _, got = domain.get_item(created.id)
        domain.assert_item_equals_post(got, pre_body)


@allure.epic("API объявлений")
@allure.feature("GET /api/1/item/:id")
class TestGetItemByIdNegative:
    @allure.story("Негативные")
    @allure.title("GET-OI-002: несуществующий id")
    @allure.testcase("GET-OI-002")
    def test_get_oi_002_not_found(self, api_client: AvitoApiClient) -> None:
        rid = random_uuid_str()
        r = api_client.get_item_by_id(rid)
        assert_get_item_not_found(r, rid)

    @allure.story("Негативные")
    @allure.title("GET-OI-003: id не uuid")
    @allure.testcase("GET-OI-003")
    def test_get_oi_003_not_uuid(self, api_client: AvitoApiClient) -> None:
        num = random_int_non_uuid()
        r = api_client.get_item_by_id(str(num))
        assert_json_error_400(r, f"ID айтема не uuid: {num}")


@allure.epic("API объявлений")
@allure.feature("GET /api/1/item/:id")
class TestGetItemByIdCorner:
    @allure.story("Корнер-кейсы")
    @allure.title("GET-OI-004: два GET подряд — одинаковые тела")
    @allure.testcase("GET-OI-004")
    def test_get_oi_004_two_gets_same(
        self, domain: ItemDomain, api_client: AvitoApiClient, pre_body: dict
    ) -> None:
        _, created = domain.create_item(pre_body)
        r1 = api_client.get_item_by_id(created.id)
        r2 = api_client.get_item_by_id(created.id)
        assert r1.status_code == 200 and r2.status_code == 200
        a = parse_item_from_get_payload(r1.json())
        b = parse_item_from_get_payload(r2.json())
        assert a.model_dump() == b.model_dump()
