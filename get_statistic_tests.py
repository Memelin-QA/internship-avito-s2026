"""Test Layer: GET /api/1/statistic/:id и GET /api/2/statistic/:id (GET-STAT-001 - GET-STAT-012)."""

from __future__ import annotations

import allure
import pytest

from api_client import AvitoApiClient, safe_json
from domain import ItemDomain
from helpers import (
    assert_json_error_400,
    assert_plain_route_not_found,
    assert_statistic_or_item_not_found,
    assert_statistic_v2_invalid_id,
    attach_request_response,
    random_int_non_uuid,
    random_uuid_str,
)
from models import ItemStatistics, parse_statistics_payload


@pytest.fixture
def stat_body(session_seller_id: int) -> dict:
    return {
        "sellerID": session_seller_id,
        "name": "Статистика",
        "price": 1200,
        "statistics": {"likes": 5, "viewCount": 10, "contacts": 2},
    }


_INVALID_ID_MSG = "передан некорректный идентификатор объявления"


def _assert_json_content_type(response: object) -> None:
    ct = response.headers.get("Content-Type", "")
    assert "application/json" in ct.lower(), ct


@allure.epic("API объявлений")
@allure.feature("GET statistic")
class TestGetStatisticPositive:
    @allure.story("Позитивные")
    @allure.title("GET-STAT-001: GET /api/1/statistic/{id} — статистика существующего объявления")
    @allure.description(
        "См. postman_collection_for_avito: «Получить статистику по объявлению» (api/1/statistic)."
    )
    @allure.testcase("GET-STAT-001")
    def test_get_stat_001_api_v1(self, domain: ItemDomain, stat_body: dict) -> None:
        _, created = domain.create_item(stat_body)
        _, rows = domain.get_statistics_v1(created.id)
        domain.assert_statistics_matches_post(rows, stat_body)

    @allure.story("Позитивные")
    @allure.title("GET-STAT-002: GET /api/2/statistic/{id} — статистика существующего объявления")
    @allure.description(
        "См. postman_collection_for_avito: вторая ручка «Получить статистику по объявлению» (api/2/statistic)."
    )
    @allure.testcase("GET-STAT-002")
    def test_get_stat_002_api_v2(self, domain: ItemDomain, stat_body: dict) -> None:
        _, created = domain.create_item(stat_body)
        _, rows = domain.get_statistics_v2(created.id)
        domain.assert_statistics_matches_post(rows, stat_body)


@allure.epic("API объявлений")
@allure.feature("GET statistic")
class TestGetStatisticNegative:
    @allure.story("Негативные")
    @allure.title("GET-STAT-003: GET /api/1/statistic без id — маршрут не найден")
    @allure.testcase("GET-STAT-003")
    def test_get_stat_003_no_id_v1(self, api_client: AvitoApiClient) -> None:
        url = api_client.url("/api/1/statistic")
        r = api_client.get_statistic_v1(None)
        attach_request_response("GET", url, r, None)
        assert_plain_route_not_found(r)

    @allure.story("Негативные")
    @allure.title("GET-STAT-004: GET /api/2/statistic без id — маршрут не найден")
    @allure.testcase("GET-STAT-004")
    def test_get_stat_004_no_id_v2(self, api_client: AvitoApiClient) -> None:
        url = api_client.url("/api/2/statistic")
        r = api_client.get_statistic_v2(None)
        attach_request_response("GET", url, r, None)
        assert_plain_route_not_found(r)

    @allure.story("Негативные")
    @allure.title("GET-STAT-005: GET /api/1/statistic/{id} — id не UUID")
    @allure.testcase("GET-STAT-005")
    def test_get_stat_005_not_uuid_v1(self, api_client: AvitoApiClient) -> None:
        num = random_int_non_uuid()
        url = api_client.url(f"/api/1/statistic/{num}")
        r = api_client.get_statistic_v1(str(num))
        attach_request_response("GET", url, r, None)
        assert_json_error_400(r, _INVALID_ID_MSG)

    @allure.story("Негативные")
    @allure.title("GET-STAT-006: GET /api/2/statistic/{id} — id не UUID")
    @allure.testcase("GET-STAT-006")
    def test_get_stat_006_not_uuid_v2(self, api_client: AvitoApiClient) -> None:
        num = random_int_non_uuid()
        url = api_client.url(f"/api/2/statistic/{num}")
        r = api_client.get_statistic_v2(str(num))
        attach_request_response("GET", url, r, None)
        assert_statistic_v2_invalid_id(r)

    @allure.story("Негативные")
    @allure.title("GET-STAT-007: GET /api/1/statistic/{id} — несуществующий UUID")
    @allure.testcase("GET-STAT-007")
    def test_get_stat_007_not_found_v1(self, api_client: AvitoApiClient) -> None:
        rid = random_uuid_str()
        url = api_client.url(f"/api/1/statistic/{rid}")
        r = api_client.get_statistic_v1(rid)
        attach_request_response("GET", url, r, None)
        assert_statistic_or_item_not_found(r, rid)

    @allure.story("Негативные")
    @allure.title("GET-STAT-008: GET /api/2/statistic/{id} — несуществующий UUID")
    @allure.testcase("GET-STAT-008")
    def test_get_stat_008_not_found_v2(self, api_client: AvitoApiClient) -> None:
        rid = random_uuid_str()
        url = api_client.url(f"/api/2/statistic/{rid}")
        r = api_client.get_statistic_v2(rid)
        attach_request_response("GET", url, r, None)
        assert_statistic_or_item_not_found(r, rid)


@allure.epic("API объявлений")
@allure.feature("GET statistic")
class TestGetStatisticCorner:
    @allure.story("Корнер-кейсы")
    @allure.title("GET-STAT-009: два GET /api/1/statistic подряд — одинаковое тело")
    @allure.testcase("GET-STAT-009")
    def test_get_stat_009_two_gets_v1(
        self, domain: ItemDomain, api_client: AvitoApiClient, stat_body: dict
    ) -> None:
        _, created = domain.create_item(stat_body)
        r1 = api_client.get_statistic_v1(created.id)
        r2 = api_client.get_statistic_v1(created.id)
        attach_request_response("GET", api_client.url(f"/api/1/statistic/{created.id}"), r2, None)
        assert r1.status_code == 200 and r2.status_code == 200
        a = parse_statistics_payload(r1.json())
        b = parse_statistics_payload(r2.json())
        assert [x.model_dump() for x in a] == [x.model_dump() for x in b]

    @allure.story("Корнер-кейсы")
    @allure.title("GET-STAT-010: два GET /api/2/statistic подряд — одинаковое тело")
    @allure.testcase("GET-STAT-010")
    def test_get_stat_010_two_gets_v2(
        self, domain: ItemDomain, api_client: AvitoApiClient, stat_body: dict
    ) -> None:
        _, created = domain.create_item(stat_body)
        r1 = api_client.get_statistic_v2(created.id)
        r2 = api_client.get_statistic_v2(created.id)
        attach_request_response("GET", api_client.url(f"/api/2/statistic/{created.id}"), r2, None)
        assert r1.status_code == 200 and r2.status_code == 200
        a = parse_statistics_payload(r1.json())
        b = parse_statistics_payload(r2.json())
        assert [x.model_dump() for x in a] == [x.model_dump() for x in b]

    @allure.story("Корнер-кейсы")
    @allure.title("GET-STAT-011: GET с заголовком Content-Type: text/plain — ответ JSON")
    @allure.description(
        "У GET нет тела; клиент всё же может прислать Content-Type — проверяем, что ответ остаётся JSON."
    )
    @allure.testcase("GET-STAT-011")
    @pytest.mark.parametrize(
        "getter",
        [
            pytest.param("v1", id="api_v1"),
            pytest.param("v2", id="api_v2"),
        ],
    )
    def test_get_stat_011_content_type_text_plain(
        self,
        domain: ItemDomain,
        api_client: AvitoApiClient,
        stat_body: dict,
        getter: str,
    ) -> None:
        _, created = domain.create_item(stat_body)
        headers = {"Content-Type": "text/plain"}
        if getter == "v1":
            r = api_client.get_statistic_v1(created.id, extra_headers=headers)
            path = f"/api/1/statistic/{created.id}"
        else:
            r = api_client.get_statistic_v2(created.id, extra_headers=headers)
            path = f"/api/2/statistic/{created.id}"
        attach_request_response("GET", api_client.url(path), r, None)
        assert r.status_code == 200
        _assert_json_content_type(r)
        raw = safe_json(r)
        assert raw is not None
        rows = parse_statistics_payload(raw)
        assert all(isinstance(x, ItemStatistics) for x in rows)
        domain.assert_statistics_matches_post(rows, stat_body)

    @allure.story("Корнер-кейсы")
    @allure.title("GET-STAT-012: Accept: */* — успешный JSON")
    @allure.testcase("GET-STAT-012")
    def test_get_stat_012_accept_any(
        self, domain: ItemDomain, api_client: AvitoApiClient, stat_body: dict
    ) -> None:
        _, created = domain.create_item(stat_body)
        r = api_client.get_statistic_v1(created.id, extra_headers={"Accept": "*/*"})
        attach_request_response("GET", api_client.url(f"/api/1/statistic/{created.id}"), r, None)
        assert r.status_code == 200
        _assert_json_content_type(r)
        rows = parse_statistics_payload(r.json())
        domain.assert_statistics_matches_post(rows, stat_body)
