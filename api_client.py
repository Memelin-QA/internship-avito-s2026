"""Client Layer: HTTP-вызовы к API без бизнес-логики."""

from __future__ import annotations

from typing import Any

import requests


class AvitoApiClient:
    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def post_item_json(self, body: dict[str, Any]) -> requests.Response:
        r = self.session.post(
            self.url("/api/1/item"),
            json=body,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout,
        )
        return r

    def post_item_raw(
        self,
        body: str | bytes,
        content_type: str = "application/json",
    ) -> requests.Response:
        return self.session.post(
            self.url("/api/1/item"),
            data=body,
            headers={"Content-Type": content_type},
            timeout=self.timeout,
        )

    def get_item_by_id(self, item_id: str) -> requests.Response:
        return self.session.get(
            self.url(f"/api/1/item/{item_id}"),
            timeout=self.timeout,
        )

    def get_seller_items(self, seller_id: int | str) -> requests.Response:
        return self.session.get(
            self.url(f"/api/1/{seller_id}/item"),
            timeout=self.timeout,
        )

    def get_statistic_v1(
        self,
        item_id: str | None = None,
        *,
        extra_headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """GET /api/1/statistic или GET /api/1/statistic/:id — postman_collection_for_avito."""
        path = "/api/1/statistic" if item_id is None else f"/api/1/statistic/{item_id}"
        return self.session.get(
            self.url(path),
            headers=extra_headers,
            timeout=self.timeout,
        )

    def get_statistic_v2(
        self,
        item_id: str | None = None,
        *,
        extra_headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """GET /api/2/statistic или GET /api/2/statistic/:id — postman_collection_for_avito."""
        path = "/api/2/statistic" if item_id is None else f"/api/2/statistic/{item_id}"
        return self.session.get(
            self.url(path),
            headers=extra_headers,
            timeout=self.timeout,
        )

    def patch_item(self, item_id: str, body: dict[str, Any] | None = None) -> requests.Response:
        return self.session.patch(
            self.url(f"/api/1/item/{item_id}"),
            json=body if body is not None else {},
            timeout=self.timeout,
        )


def safe_json(response: requests.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return None
