"""Domain Layer: сценарии и действия над объявлениями."""

from __future__ import annotations

from typing import Any

import allure
import requests
from pydantic import ValidationError

from api_client import AvitoApiClient, safe_json
from helpers import (
    attach_request_response,
    extract_item_id_from_malformed_post_success,
    timed_request,
)
from models import (
    ItemCreatePayload,
    ItemResponse,
    ItemStatistics,
    parse_item_from_get_payload,
    parse_seller_items_list,
    parse_statistics_payload,
)


class ItemDomain:
    def __init__(self, client: AvitoApiClient) -> None:
        self.client = client

    @allure.step("Создать объявление (POST /api/1/item)")
    def create_item(
        self, payload: dict[str, Any] | ItemCreatePayload
    ) -> tuple[requests.Response, ItemResponse]:
        body = payload.model_dump() if isinstance(payload, ItemCreatePayload) else payload
        with allure.step("Отправить POST"):
            r = self.client.post_item_json(body)
            attach_request_response("POST", self.client.url("/api/1/item"), r, body)
        r.raise_for_status()
        data = safe_json(r)
        if data is None:
            raise AssertionError("пустой JSON в ответе POST")
        if not isinstance(data, dict):
            raise AssertionError(f"ожидался JSON-объект в ответе POST, получено {type(data)}")

        try:
            item = ItemResponse.model_validate(data)
            return r, item
        except ValidationError:
            pass

        # ВРЕМЕННО: тело успешного POST на стенде не соответствует ItemResponse (Postman Success response).
        # Для сценариев GET_OI / GET_AI получаем объявление повторным GET по id.
        # Убрать этот блок после исправления ответа POST на контракт.
        item_id = extract_item_id_from_malformed_post_success(data)
        with allure.step("ВРЕМЕННО: GET по id после POST (обход неверного тела POST)"):
            gr = self.client.get_item_by_id(item_id)
            attach_request_response("GET", self.client.url(f"/api/1/item/{item_id}"), gr, None)
        gr.raise_for_status()
        gdata = safe_json(gr)
        if gdata is None:
            raise AssertionError("пустой JSON в GET после POST")
        item = parse_item_from_get_payload(gdata)
        return r, item

    @allure.step("Получить объявление по id (GET /api/1/item/{{id}})")
    def get_item(self, item_id: str) -> tuple[requests.Response, ItemResponse]:
        url = self.client.url(f"/api/1/item/{item_id}")
        r = self.client.get_item_by_id(item_id)
        attach_request_response("GET", url, r, None)
        r.raise_for_status()
        raw = safe_json(r)
        if raw is None:
            raise AssertionError("пустой JSON в GET по id")
        item = parse_item_from_get_payload(raw)
        return r, item

    @allure.step("Получить список объявлений продавца (GET /api/1/{{sellerID}}/item)")
    def list_seller_items(self, seller_id: int) -> tuple[requests.Response, list[ItemResponse]]:
        url = self.client.url(f"/api/1/{seller_id}/item")
        r = self.client.get_seller_items(seller_id)
        attach_request_response("GET", url, r, None)
        r.raise_for_status()
        data = safe_json(r)
        parsed = parse_seller_items_list(data)
        return r, parsed

    @allure.step("Получить статистику (GET /api/1/statistic/{{id}})")
    def get_statistics_v1(self, item_id: str) -> tuple[requests.Response, list[ItemStatistics]]:
        url = self.client.url(f"/api/1/statistic/{item_id}")
        r = self.client.get_statistic_v1(item_id)
        attach_request_response("GET", url, r, None)
        r.raise_for_status()
        raw = safe_json(r)
        if raw is None:
            raise AssertionError("пустой JSON в GET statistic v1")
        return r, parse_statistics_payload(raw)

    @allure.step("Получить статистику (GET /api/2/statistic/{{id}})")
    def get_statistics_v2(self, item_id: str) -> tuple[requests.Response, list[ItemStatistics]]:
        url = self.client.url(f"/api/2/statistic/{item_id}")
        r = self.client.get_statistic_v2(item_id)
        attach_request_response("GET", url, r, None)
        r.raise_for_status()
        raw = safe_json(r)
        if raw is None:
            raise AssertionError("пустой JSON в GET statistic v2")
        return r, parse_statistics_payload(raw)

    @allure.step("Сравнить поля объявления с ожидаемыми из запроса POST")
    def assert_item_equals_post(
        self,
        item: ItemResponse,
        expected: dict[str, Any],
    ) -> None:
        stats = expected["statistics"]
        assert item.name == expected["name"]
        assert item.price == expected["price"]
        assert item.sellerId == expected["sellerID"]
        assert item.statistics.likes == stats["likes"]
        assert item.statistics.viewCount == stats["viewCount"]
        assert item.statistics.contacts == stats["contacts"]
        assert item.createdAt

    @staticmethod
    def assert_statistics_matches_post(
        rows: list[ItemStatistics],
        post_body: dict[str, Any],
    ) -> None:
        """Хотя бы одна строка из ответа statistic совпадает с statistics из POST."""
        exp = post_body["statistics"]
        ok = any(
            r.likes == exp["likes"]
            and r.viewCount == exp["viewCount"]
            and r.contacts == exp["contacts"]
            for r in rows
        )
        assert ok, f"статистика не совпала с POST: {rows!r} vs {exp!r}"

    @staticmethod
    def find_item_in_list(items: list[ItemResponse], item_id: str) -> ItemResponse | None:
        for it in items:
            if it.id == item_id:
                return it
        return None


def post_json_for_test(client: AvitoApiClient, body: dict[str, Any]) -> requests.Response:
    """Прямой POST без raise — для негативных тестов."""
    r = client.post_item_json(body)
    attach_request_response("POST", client.url("/api/1/item"), r, body)
    return r


def timed_post_item(
    client: AvitoApiClient, body: dict[str, Any]
) -> tuple[requests.Response, float]:
    def _do() -> requests.Response:
        return client.post_item_json(body)

    r, ms = timed_request(_do)
    attach_request_response("POST", client.url("/api/1/item"), r, body)
    return r, ms


def timed_get_item(client: AvitoApiClient, item_id: str) -> tuple[requests.Response, float]:
    def _do() -> requests.Response:
        return client.get_item_by_id(item_id)

    r, ms = timed_request(_do)
    attach_request_response("GET", client.url(f"/api/1/item/{item_id}"), r, None)
    return r, ms


def timed_get_seller(client: AvitoApiClient, seller_id: int) -> tuple[requests.Response, float]:
    def _do() -> requests.Response:
        return client.get_seller_items(seller_id)

    r, ms = timed_request(_do)
    attach_request_response("GET", client.url(f"/api/1/{seller_id}/item"), r, None)
    return r, ms


def timed_get_statistic_v1(client: AvitoApiClient, item_id: str) -> tuple[requests.Response, float]:
    def _do() -> requests.Response:
        return client.get_statistic_v1(item_id)

    r, ms = timed_request(_do)
    attach_request_response("GET", client.url(f"/api/1/statistic/{item_id}"), r, None)
    return r, ms


def timed_get_statistic_v2(client: AvitoApiClient, item_id: str) -> tuple[requests.Response, float]:
    def _do() -> requests.Response:
        return client.get_statistic_v2(item_id)

    r, ms = timed_request(_do)
    attach_request_response("GET", client.url(f"/api/2/statistic/{item_id}"), r, None)
    return r, ms
