"""Вспомогательные функции: UUID, вложения Allure, проверки ответов."""

from __future__ import annotations

import json
import random
import re
import time
import uuid
from typing import Any

import allure
import requests
from pydantic import ValidationError

from api_client import AvitoApiClient
from models import ErrorResponse400, ErrorResponse404, ErrorResult404Body


def random_uuid_str() -> str:
    return str(uuid.uuid4())


def random_int_non_uuid() -> int:
    return random.randint(1, 999999999)


def random_seller_id() -> int:
    return random.randint(111111, 999999)


def attach_request_response(
    method: str,
    url: str,
    response: requests.Response | None = None,
    request_body: Any = None,
) -> None:
    """Прикрепляет к шагу Allure сведения о запросе и ответе."""
    lines = [f"{method} {url}"]
    if request_body is not None:
        if isinstance(request_body, dict | list):
            lines.append("Request body:\n" + json.dumps(request_body, ensure_ascii=False, indent=2))
        else:
            lines.append(f"Request body (raw):\n{request_body!r}")
    if response is not None:
        lines.append(f"HTTP {response.status_code}")
        lines.append("Response headers:\n" + json.dumps(dict(response.headers), indent=2))
        try:
            body = response.json()
            lines.append("Response JSON:\n" + json.dumps(body, ensure_ascii=False, indent=2))
        except ValueError:
            lines.append(f"Response text:\n{response.text[:8000]}")
    allure.attach(
        "\n\n".join(lines),
        name="HTTP",
        attachment_type=allure.attachment_type.TEXT,
    )


def assert_json_error_400(
    response: requests.Response,
    message_contains: str,
    status_equals: str = "400",
) -> ErrorResponse400:
    assert response.status_code == 400, response.text
    data = response.json()
    try:
        err = ErrorResponse400.model_validate(data)
    except ValidationError as e:
        attach_request_response("", "", response, None)
        raise AssertionError(f"невалидное тело ошибки 400: {e}") from e
    assert status_equals in err.status, err.status
    assert message_contains.lower() in err.result.message.lower(), err.result.message
    assert err.result.messages is None or isinstance(err.result.messages, dict)
    return err


def extract_item_id_from_malformed_post_success(data: dict[str, Any]) -> str:
    """
    Временно: обход некорректного тела успешного POST на стенде.

    По контракту (API / TESTCASES) POST 200 должен быть валидным ItemResponse с полем id.
    Пока ответ не соответствует модели, извлекаем UUID из поля status или иных частей ответа.
    Удалить этот обход после исправления API.
    """
    if "id" in data:
        return str(data["id"])
    status = str(data.get("status", ""))
    m = re.search(
        r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
        status,
    )
    if m:
        return m.group(1)
    msg = f"не удалось извлечь id объявления из ответа POST: {data!r}"
    raise AssertionError(msg)


def _message_from_404_result(result: str | ErrorResult404Body) -> str:
    if isinstance(result, ErrorResult404Body):
        return result.message
    return result


def assert_error_response_404(
    response: requests.Response,
    *,
    item_id: str,
) -> ErrorResponse404:
    assert response.status_code == 404, response.text
    try:
        data = response.json()
    except ValueError as e:
        attach_request_response("", "", response, None)
        raise AssertionError("ожидался JSON в теле 404") from e
    try:
        err = ErrorResponse404.model_validate(data)
    except ValidationError as e:
        attach_request_response("", "", response, None)
        raise AssertionError(f"невалидное тело ошибки 404: {e}") from e
    assert "404" in err.status, err.status
    msg = _message_from_404_result(err.result)
    low = msg.lower()
    assert "не найден" in low or "not found" in low, msg
    assert item_id in msg, msg
    return err


def assert_get_item_not_found(response: requests.Response, item_id: str) -> ErrorResponse404:
    """GET /api/1/item/:id — 404 с result/status как в Postman (GET Not Found)."""
    return assert_error_response_404(response, item_id=item_id)


def assert_plain_route_not_found(response: requests.Response) -> None:
    """404 без id в пути (напр. GET /api/1/statistic) — тело вида {message, code}."""
    assert response.status_code == 404, response.text
    data = response.json()
    assert "message" in data
    low = str(data["message"]).lower()
    assert "not found" in low or "не найден" in low, data


def assert_statistic_or_item_not_found(response: requests.Response, item_id: str) -> None:
    """
    404 для GET statistic/item: фактическое тело — result.message, id в тексте.
    (см. `ErrorResponse404` в models.py — допускается и строка, и объект с `message`.)
    """
    assert response.status_code == 404, response.text
    data = response.json()
    result = data.get("result")
    if isinstance(result, dict):
        msg = str(result.get("message", ""))
    else:
        msg = str(result)
    assert item_id in msg, msg
    low = msg.lower()
    assert "not found" in low or "не найден" in low, msg


def assert_statistic_v2_invalid_id(response: requests.Response) -> None:
    """GET /api/2/statistic с id не UUID — на стенде HTTP 404 с телом ошибки валидации."""
    assert response.status_code == 404, response.text
    data = response.json()
    result = data.get("result")
    assert isinstance(result, dict), data
    msg = str(result.get("message", ""))
    assert "идентификатор" in msg.lower(), msg


def timed_request(do: Any) -> tuple[Any, float]:
    t0 = time.perf_counter()
    resp = do()
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    resp._elapsed_ms = elapsed_ms
    return resp, elapsed_ms


def find_seller_with_empty_list(api_client: AvitoApiClient, attempts: int = 40) -> int:
    """Подбирает sellerID в диапазоне, у которого GET /api/1/:id/item возвращает []."""
    for _ in range(attempts):
        sid = random_seller_id()
        r = api_client.get_seller_items(sid)
        if r.status_code == 200:
            data = r.json()
            if data == []:
                return sid
    msg = "не удалось найти продавца без объявлений за отведённые попытки"
    raise RuntimeError(msg)
