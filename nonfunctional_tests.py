"""Test Layer: нефункциональные проверки (NFR-001 - NFR-005)."""

from __future__ import annotations

import allure

from api_client import AvitoApiClient
from domain import (
    ItemDomain,
    timed_get_item,
    timed_get_seller,
    timed_get_statistic_v1,
    timed_get_statistic_v2,
    timed_post_item,
)


def _assert_json_content_type(response: object) -> None:
    ct = response.headers.get("Content-Type", "")
    assert "application/json" in ct.lower(), ct


@allure.epic("API объявлений")
@allure.feature("Нефункциональные")
class TestNFR:
    @allure.story("Производительность и заголовки")
    @allure.title("NFR-001: время ответа POST и Content-Type")
    @allure.testcase("NFR-001")
    def test_nfr_001_post_latency(
        self, api_client: AvitoApiClient, nfr_max_ms: float, speed_body: dict
    ) -> None:
        r, ms = timed_post_item(api_client, speed_body)
        assert r.status_code == 200
        assert ms <= nfr_max_ms
        _assert_json_content_type(r)

    @allure.story("Производительность и заголовки")
    @allure.title("NFR-002: время GET по id")
    @allure.testcase("NFR-002")
    def test_nfr_002_get_by_id_latency(
        self,
        domain: ItemDomain,
        api_client: AvitoApiClient,
        nfr_max_ms: float,
        speed_body: dict,
    ) -> None:
        _, created = domain.create_item(speed_body)
        r, ms = timed_get_item(api_client, created.id)
        assert r.status_code == 200
        assert ms <= nfr_max_ms
        _assert_json_content_type(r)

    @allure.story("Производительность и заголовки")
    @allure.title("NFR-003: время GET списка")
    @allure.testcase("NFR-003")
    def test_nfr_003_get_list_latency(
        self,
        domain: ItemDomain,
        api_client: AvitoApiClient,
        nfr_max_ms: float,
        speed_body: dict,
        session_seller_id: int,
    ) -> None:
        domain.create_item(speed_body)
        r, ms = timed_get_seller(api_client, session_seller_id)
        assert r.status_code == 200
        assert ms <= nfr_max_ms
        _assert_json_content_type(r)

    @allure.story("Методы HTTP")
    @allure.title("NFR-004: PATCH не поддерживается (405)")
    @allure.testcase("NFR-004")
    def test_nfr_004_patch_not_allowed(
        self, domain: ItemDomain, api_client: AvitoApiClient, speed_body: dict
    ) -> None:
        _, created = domain.create_item(speed_body)
        r = api_client.patch_item(created.id, {})
        assert r.status_code == 405
        assert (r.text or "").strip() == ""

    @allure.story("Производительность и заголовки")
    @allure.title("NFR-005: время GET /api/1/statistic и /api/2/statistic")
    @allure.testcase("NFR-005")
    def test_nfr_005_get_statistic_latency(
        self,
        domain: ItemDomain,
        api_client: AvitoApiClient,
        nfr_max_ms: float,
        speed_body: dict,
    ) -> None:
        _, created = domain.create_item(speed_body)
        r1, ms1 = timed_get_statistic_v1(api_client, created.id)
        r2, ms2 = timed_get_statistic_v2(api_client, created.id)
        assert r1.status_code == 200
        assert r2.status_code == 200
        assert ms1 <= nfr_max_ms
        assert ms2 <= nfr_max_ms
        _assert_json_content_type(r1)
        _assert_json_content_type(r2)
