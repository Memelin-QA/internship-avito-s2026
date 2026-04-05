"""Test Layer: POST /api/1/item (TESTCASES POST-001 - POST-036)."""

from __future__ import annotations

import json

import allure
import pytest

from api_client import AvitoApiClient
from domain import ItemDomain, post_json_for_test
from helpers import assert_json_error_400


@allure.epic("API объявлений")
@allure.feature("POST /api/1/item")
class TestPostPositive:
    @allure.story("Позитивные")
    @allure.title("POST-001: успешное создание с sellerID в диапазоне")
    @allure.description("Проверка HTTP 200 и соответствия полей запросу.")
    @allure.testcase("POST-001")
    # Перед удалением xfail, проверить, что тело ответа соответствует ItemResponse, и исправить получение id объявления из ответа POST
    @pytest.mark.xfail(
        reason="BUG-004: см. BUGS.md — некорретное тело ответа POST / отклонение 200", strict=False
    )
    def test_post_001_success_mid_range_seller(self, domain: ItemDomain) -> None:
        body = {
            "sellerID": 845125,
            "name": "Велосипед горный",
            "price": 15000,
            "statistics": {"likes": 10, "viewCount": 100, "contacts": 5},
        }
        _, item = domain.create_item(body)
        domain.assert_item_equals_post(item, body)

    @allure.story("Позитивные")
    @allure.title("POST-002: нижняя граница sellerID = 111111")
    @allure.testcase("POST-002")
    @pytest.mark.xfail(
        reason="BUG-003: см. BUGS.md — граница sellerID / отклонение 400", strict=False
    )
    def test_post_002_seller_lower_bound(self, domain: ItemDomain) -> None:
        body = {
            "sellerID": 111111,
            "name": "Стул офисный",
            "price": 3500,
            "statistics": {"likes": 0, "viewCount": 5, "contacts": 1},
        }
        _, item = domain.create_item(body)
        domain.assert_item_equals_post(item, body)

    @allure.story("Позитивные")
    @allure.title("POST-003: верхняя граница sellerID = 999999")
    @allure.testcase("POST-003")
    def test_post_003_seller_upper_bound(self, domain: ItemDomain) -> None:
        body = {
            "sellerID": 999999,
            "name": "Монитор 27",
            "price": 22000,
            "statistics": {"likes": 3, "viewCount": 200, "contacts": 3},
        }
        _, item = domain.create_item(body)
        domain.assert_item_equals_post(item, body)

    @allure.story("Позитивные")
    @allure.title("POST-004: минимальное price = 1")
    @allure.testcase("POST-004")
    def test_post_004_min_price(self, domain: ItemDomain) -> None:
        body = {
            "sellerID": 845125,
            "name": "Ручка шариковая",
            "price": 1,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 7},
        }
        _, item = domain.create_item(body)
        domain.assert_item_equals_post(item, body)

    @allure.story("Позитивные")
    @allure.title("POST-005: нули в statistics")
    @allure.testcase("POST-005")
    @pytest.mark.xfail(
        reason="BUG-003: см. BUGS.md — нули в statistics / отклонение 400", strict=False
    )
    def test_post_005_statistics_zeros(self, domain: ItemDomain) -> None:
        body = {
            "sellerID": 845125,
            "name": "Коврик для мыши",
            "price": 500,
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0},
        }
        _, item = domain.create_item(body)
        domain.assert_item_equals_post(item, body)

    @allure.story("Позитивные")
    @allure.title("POST-006: два одинаковых POST — разные id")
    @allure.testcase("POST-006")
    def test_post_006_duplicate_body_different_ids(self, domain: ItemDomain) -> None:
        body = {
            "sellerID": 845125,
            "name": "iPhone",
            "price": 5000,
            "statistics": {"likes": 2, "viewCount": 50, "contacts": 3},
        }
        _, first = domain.create_item(body)
        _, second = domain.create_item(body)
        assert first.id != second.id
        domain.assert_item_equals_post(first, body)
        domain.assert_item_equals_post(second, body)

    @allure.story("Корнер-кейсы")
    @allure.title("POST-033: лишнее поле extraField игнорируется")
    @allure.testcase("POST-033")
    def test_post_033_extra_field(self, domain: ItemDomain) -> None:
        body = {
            "sellerID": 845125,
            "name": "С лишним полем",
            "price": 700,
            "statistics": {"likes": 1, "viewCount": 2, "contacts": 3},
            "extraField": "test",
        }
        _, item = domain.create_item(body)
        base = {k: v for k, v in body.items() if k != "extraField"}
        domain.assert_item_equals_post(item, base)

    @allure.story("Корнер-кейсы")
    @allure.title("POST-034: name длиной 1000 символов")
    @allure.testcase("POST-034")
    def test_post_034_long_name(self, domain: ItemDomain) -> None:
        long_name = "A" * 1000
        body = {
            "sellerID": 845125,
            "name": long_name,
            "price": 100,
            "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
        }
        _, item = domain.create_item(body)
        domain.assert_item_equals_post(item, body)


def _neg_params() -> list:
    # Ожидаемые провалы до исправления стенда — см. BUGS.md (BUG-005).
    _xfail_validation = pytest.mark.xfail(
        reason="BUG-005: валидация POST не совпадает с TESTCASES — см. BUGS.md",
        strict=False,
    )
    return [
        pytest.param(
            {
                "sellerID": 845125,
                "price": 1000,
                "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
            },
            "поле name обязательно",
            id="POST-007",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Стул",
                "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
            },
            "поле price обязательно",
            id="POST-008",
        ),
        pytest.param(
            {
                "name": "Книга",
                "price": 500,
                "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
            },
            "поле sellerID обязательно",
            id="POST-009",
        ),
        pytest.param(
            {"sellerID": 845125, "name": "Без статистики", "price": 900},
            "поле statistics обязательно",
            marks=_xfail_validation,
            id="POST-010",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "iPhone",
                "price": 5000,
                "statistics": {"viewCount": 50, "contacts": 3},
            },
            "поле likes обязательно",
            id="POST-011",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "iPhone",
                "price": 5000,
                "statistics": {"likes": 2, "contacts": 3},
            },
            "поле viewCount обязательно",
            id="POST-012",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "iPhone",
                "price": 5000,
                "statistics": {"likes": 2, "viewCount": 50},
            },
            "поле contacts обязательно",
            id="POST-013",
        ),
        pytest.param({}, "поле name обязательно", id="POST-014"),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "",
                "price": 100,
                "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
            },
            "поле name обязательно",
            id="POST-015",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": -1,
                "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
            },
            "поле price должно быть положительным",
            marks=_xfail_validation,
            id="POST-016",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 999.99,
                "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
            },
            "поле price должно быть целым",
            marks=_xfail_validation,
            id="POST-017",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": "дорого",
                "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
            },
            "поле price должно быть числом",
            marks=_xfail_validation,
            id="POST-018",
        ),
        pytest.param(
            {
                "sellerID": "abc",
                "name": "Товар",
                "price": 100,
                "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
            },
            "поле sellerID должно быть числом",
            marks=_xfail_validation,
            id="POST-019",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": 123,
                "price": 100,
                "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
            },
            "поле name должно быть строкой",
            marks=_xfail_validation,
            id="POST-020",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 100,
                "statistics": "abc",
            },
            "поле statistics должно быть объектом JSON",
            marks=_xfail_validation,
            id="POST-021",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 100,
                "statistics": {"likes": -1, "viewCount": 3, "contacts": 7},
            },
            "поле likes не должно быть отрицательным",
            marks=_xfail_validation,
            id="POST-022",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 999,
                "statistics": {"likes": 9.4, "viewCount": 3, "contacts": 7},
            },
            "поле likes должно быть целым",
            marks=_xfail_validation,
            id="POST-023",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 1000,
                "statistics": {"likes": "abc", "viewCount": 3, "contacts": 7},
            },
            "поле likes должно быть числом",
            marks=_xfail_validation,
            id="POST-024",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 100,
                "statistics": {"likes": 1, "viewCount": -1, "contacts": 7},
            },
            "поле viewCount не должно быть отрицательным",
            marks=_xfail_validation,
            id="POST-025",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 999,
                "statistics": {"likes": 1, "viewCount": 9.4, "contacts": 7},
            },
            "поле viewCount должно быть целым",
            marks=_xfail_validation,
            id="POST-026",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 1000,
                "statistics": {"likes": 1, "viewCount": "abc", "contacts": 7},
            },
            "поле viewCount должно быть числом",
            marks=_xfail_validation,
            id="POST-027",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 100,
                "statistics": {"likes": 1, "viewCount": 3, "contacts": -1},
            },
            "поле contacts не должно быть отрицательным",
            marks=_xfail_validation,
            id="POST-028",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 999,
                "statistics": {"likes": 1, "viewCount": 3, "contacts": 9.4},
            },
            "поле contacts должно быть целым",
            marks=_xfail_validation,
            id="POST-029",
        ),
        pytest.param(
            {
                "sellerID": 845125,
                "name": "Товар",
                "price": 1000,
                "statistics": {"likes": 1, "viewCount": 3, "contacts": "abc"},
            },
            "поле contacts должно быть числом",
            marks=_xfail_validation,
            id="POST-030",
        ),
    ]


@allure.epic("API объявлений")
@allure.feature("POST /api/1/item")
class TestPostNegative:
    @allure.story("Негативные")
    @pytest.mark.parametrize("body,msg", _neg_params())
    def test_post_validation_errors(
        self,
        api_client: AvitoApiClient,
        body: dict,
        msg: str,
        request: pytest.FixtureRequest,
    ) -> None:
        case_id = request.node.callspec.id
        allure.dynamic.title(f"{case_id}: ответ 400, message содержит «{msg}»")
        allure.dynamic.description(
            f"Негативный POST: ожидается HTTP 400 и подстрока «{msg}» в теле ошибки."
        )
        with allure.step(f"Отправить POST (кейс {case_id})"):
            r = post_json_for_test(api_client, body)
        with allure.step("Проверить структуру ErrorResponse400 и текст message"):
            assert_json_error_400(r, msg)

    @allure.story("Негативные")
    @allure.title("POST-031: битый JSON")
    @allure.testcase("POST-031")
    @pytest.mark.xfail(reason="BUG-006: см. BUGS.md — сообщение о невалидном JSON", strict=False)
    def test_post_031_invalid_json(self, api_client: AvitoApiClient) -> None:
        raw = '{\n  "sellerID": 111111, \n  "name": "обрыв\n}'
        r = api_client.post_item_raw(raw.encode("utf-8"))
        assert_json_error_400(r, "Передан не валидный JSON")

    @allure.story("Негативные")
    @allure.title("POST-032: Content-Type text/plain")
    @allure.testcase("POST-032")
    @pytest.mark.xfail(
        reason="BUG-007: см. BUGS.md — тело ошибки 400 при неверном Content-Type", strict=False
    )
    def test_post_032_wrong_content_type(self, api_client: AvitoApiClient) -> None:
        body = {
            "sellerID": 845125,
            "name": "Проверка заголовка",
            "price": 100,
            "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
        }
        r = api_client.post_item_raw(
            json.dumps(body, ensure_ascii=False), content_type="text/plain"
        )
        assert_json_error_400(r, "Недопустимый тип контента")


@allure.epic("API объявлений")
@allure.feature("POST /api/1/item")
class TestPostCornerNegativeRange:
    @allure.story("Корнер-кейсы")
    @allure.title("POST-035: sellerID ниже диапазона (111110)")
    @allure.testcase("POST-035")
    @pytest.mark.xfail(reason="BUG-008: см. BUGS.md — сообщение о диапазоне sellerID", strict=False)
    def test_post_035_seller_below_range(self, api_client: AvitoApiClient) -> None:
        body = {
            "sellerID": 111110,
            "name": "Ниже диапазона",
            "price": 200,
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0},
        }
        r = post_json_for_test(api_client, body)
        assert_json_error_400(r, "поле sellerID должно быть в диапазоне 111111-999999")

    @allure.story("Корнер-кейсы")
    @allure.title("POST-036: sellerID выше диапазона (1000000)")
    @allure.testcase("POST-036")
    @pytest.mark.xfail(reason="BUG-008: см. BUGS.md — сообщение о диапазоне sellerID", strict=False)
    def test_post_036_seller_above_range(self, api_client: AvitoApiClient) -> None:
        body = {
            "sellerID": 1000000,
            "name": "Выше диапазона",
            "price": 200,
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0},
        }
        r = post_json_for_test(api_client, body)
        assert_json_error_400(r, "поле sellerID должно быть в диапазоне 111111-999999")
