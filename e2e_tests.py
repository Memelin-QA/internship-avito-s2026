"""Test Layer: сквозные сценарии (E2E-001 … E2E-003)."""

from __future__ import annotations

import allure

from domain import ItemDomain
from helpers import random_seller_id


@allure.epic("API объявлений")
@allure.feature("E2E")
class TestE2ELifecycle:
    @allure.story("Сквозные сценарии")
    @allure.title("E2E-001: объявление — GET по id, список, статистика v1 и v2")
    @allure.description(
        "POST → GET по id → GET списка → GET /api/1/statistic → GET /api/2/statistic."
    )
    @allure.testcase("E2E-001")
    def test_e2e_001_lifecycle(self, domain: ItemDomain, session_seller_id: int) -> None:
        body = {
            "sellerID": session_seller_id,
            "name": "E2E цикл",
            "price": 5000,
            "statistics": {"likes": 1, "viewCount": 2, "contacts": 3},
        }
        _, created = domain.create_item(body)
        _, by_id = domain.get_item(created.id)
        domain.assert_item_equals_post(by_id, body)

        _, items = domain.list_seller_items(session_seller_id)
        assert domain.find_item_in_list(items, created.id) is not None

        _, s1 = domain.get_statistics_v1(created.id)
        domain.assert_statistics_matches_post(s1, body)
        _, s2 = domain.get_statistics_v2(created.id)
        domain.assert_statistics_matches_post(s2, body)

    @allure.story("Сквозные сценарии")
    @allure.title("E2E-002: три объявления — список и статистика по каждому id")
    @allure.testcase("E2E-002")
    def test_e2e_002_three_items_statistics(
        self, domain: ItemDomain, session_seller_id: int
    ) -> None:
        b1 = {
            "sellerID": session_seller_id,
            "name": "Объявление 1",
            "price": 100,
            "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
        }
        b2 = {
            "sellerID": session_seller_id,
            "name": "Объявление 2",
            "price": 200,
            "statistics": {"likes": 2, "viewCount": 4, "contacts": 8},
        }
        b3 = {
            "sellerID": session_seller_id,
            "name": "Объявление 3",
            "price": 300,
            "statistics": {"likes": 3, "viewCount": 5, "contacts": 9},
        }
        _, i1 = domain.create_item(b1)
        _, i2 = domain.create_item(b2)
        _, i3 = domain.create_item(b3)

        _, items = domain.list_seller_items(session_seller_id)
        ids_in_list = {it.id for it in items}
        assert i1.id in ids_in_list and i2.id in ids_in_list and i3.id in ids_in_list

        for item_id, b in ((i1.id, b1), (i2.id, b2), (i3.id, b3)):
            _, sv1 = domain.get_statistics_v1(item_id)
            domain.assert_statistics_matches_post(sv1, b)
            _, sv2 = domain.get_statistics_v2(item_id)
            domain.assert_statistics_matches_post(sv2, b)

    @allure.story("Сквозные сценарии")
    @allure.title("E2E-003: изоляция объявлений по продавцам")
    @allure.testcase("E2E-003")
    def test_e2e_003_two_sellers(self, domain: ItemDomain) -> None:
        sid_a = random_seller_id()
        sid_b = random_seller_id()
        while sid_b == sid_a:
            sid_b = random_seller_id()
        body_a = {
            "sellerID": sid_a,
            "name": "A",
            "price": 1000,
            "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
        }
        body_b = {
            "sellerID": sid_b,
            "name": "B",
            "price": 2000,
            "statistics": {"likes": 1, "viewCount": 3, "contacts": 7},
        }
        _, a = domain.create_item(body_a)
        _, b = domain.create_item(body_b)

        _, list_a = domain.list_seller_items(sid_a)
        ids_a = {it.id for it in list_a}
        assert a.id in ids_a and b.id not in ids_a

        _, list_b = domain.list_seller_items(sid_b)
        ids_b = {it.id for it in list_b}
        assert b.id in ids_b and a.id not in ids_b
