"""Pydantic-модели для валидации тел ответов API объявлений."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class ItemStatistics(BaseModel):
    model_config = ConfigDict(extra="ignore")

    likes: int
    viewCount: int
    contacts: int


class ItemCreatePayload(BaseModel):
    """Тело запроса POST /api/1/item (поля sellerID, name, price, statistics)."""

    model_config = ConfigDict(extra="ignore")

    sellerID: int
    name: str
    price: int
    statistics: ItemStatistics


class ItemResponse(BaseModel):
    """
    Успешное тело ответа по объявлению: POST 200 «Success response» и элементы массива
    в GET /api/1/item/:id (ok) и GET /api/1/:sellerID/item (ok) в Postman-коллекции.
    """

    model_config = ConfigDict(extra="ignore")

    id: str
    sellerId: int
    name: str
    price: int
    statistics: ItemStatistics
    createdAt: str


class ErrorResultDetailed(BaseModel):
    model_config = ConfigDict(extra="ignore")

    messages: dict[str, str] | None = None
    message: str


class ErrorResponse400(BaseModel):
    """Тело 400 Bad request из Postman (result.messages, result.message, status)."""

    model_config = ConfigDict(extra="ignore")

    result: ErrorResultDetailed
    status: str


class ErrorResult404Body(BaseModel):
    """Фактическое тело `result` на стенде: объект с `message` (и опционально `messages`)."""

    model_config = ConfigDict(extra="ignore")

    message: str
    messages: dict[str, str] | None = None


class ErrorResponse404(BaseModel):
    """
    404 Not Found: в Postman может быть `result` — строка; на стенде часто объект с `message`.
    """

    model_config = ConfigDict(extra="ignore")

    result: str | ErrorResult404Body
    status: str


def parse_item_from_get_payload(data: Any) -> ItemResponse:
    """
    Ответ GET /api/1/item/:id (ok в Postman): массив из одного или нескольких элементов
    либо один объект — нормализуем к ItemResponse.
    """
    if isinstance(data, list):
        if len(data) != 1:
            msg = f"ожидался ровно один элемент в списке, получено {len(data)}"
            raise ValueError(msg)
        return ItemResponse.model_validate(data[0])
    return ItemResponse.model_validate(data)


def parse_seller_items_list(data: Any) -> list[ItemResponse]:
    """Ответ GET /api/1/:sellerID/item (ok): массив объектов как в Postman."""
    if not isinstance(data, list):
        msg = "ожидался JSON-массив объявлений"
        raise TypeError(msg)
    return [ItemResponse.model_validate(x) for x in data]


def parse_statistics_payload(data: Any) -> list[ItemStatistics]:
    """
    Успешное тело GET /api/1/statistic/:id и GET /api/2/statistic/:id (ok в postman_collection_for_avito):
    массив из одного или нескольких объектов {likes, viewCount, contacts}; допускается один объект.
    """
    if isinstance(data, dict):
        return [ItemStatistics.model_validate(data)]
    if isinstance(data, list):
        return [ItemStatistics.model_validate(x) for x in data]
    msg = f"ожидался JSON-массив или объект статистики, получено {type(data)}"
    raise TypeError(msg)
