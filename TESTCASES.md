# Тест-кейсы API объявлений

**Базовый URL (`baseUrl`):** `https://qa-internship.avito.com`

---

## POST `/api/1/item` - позитивные

**ID:** POST-001

**Заголовок:** Успешное создание объявления с `sellerID` в диапазоне 111111-999999

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Велосипед горный",
  "price": 15000,
  "statistics": {
    "likes": 10,
    "viewCount": 100,
    "contacts": 5
  }
}
```

**Ожидаемый результат:** HTTP 200; `id` - строка; `sellerId` = число; `name` - строка, `price` - число, `statistics` - объект, как в запросе; есть `createdAt` - строка. Также проверяем, что значения соответствуют тем, которые были переданы в запросе

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-002

**Заголовок:** Нижняя граница для `sellerID` = 111111

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 111111,
  "name": "Стул офисный",
  "price": 3500,
  "statistics": {
    "likes": 0,
    "viewCount": 5,
    "contacts": 1
  }
}
```

**Ожидаемый результат:** HTTP 200; непустой `id` - строка; `sellerId` = число; `name` - строка, `price` - число, `statistics` - объект, как в запросе; есть `createdAt` - строка. Также проверяем, что значения соответствуют тем, которые были переданы в запросе

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-003

**Заголовок:** Верхняя граница для `sellerID` = 999999

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 999999,
  "name": "Монитор 27",
  "price": 22000,
  "statistics": {
    "likes": 3,
    "viewCount": 200,
    "contacts": 3
  }
}
```

**Ожидаемый результат:** HTTP 200; непустой `id` - строка; `sellerId` = число; `name` - строка, `price` - число, `statistics` - объект, как в запросе; есть `createdAt` - строка. Также проверяем, что значения соответствуют тем, которые были переданы в запросе

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-004

**Заголовок:** Минимальное положительное значение `price` = 1

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Ручка шариковая",
  "price": 1,
  "statistics": {
    "likes": 1,
    "viewCount": 1,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 200; непустой `id` - строка; `sellerId` = число; `name` - строка, `price` - число, `statistics` - объект, как в запросе; есть `createdAt` - строка. Также проверяем, что значения соответствуют тем, которые были переданы в запросе

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-005

**Заголовок:** Передача нулей в объекте `statistics`

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Коврик для мыши",
  "price": 500,
  "statistics": {
    "likes": 0,
    "viewCount": 0,
    "contacts": 0
  }
}
```

**Ожидаемый результат:** HTTP 200; непустой `id` - строка; `sellerId` = число; `name` - строка, `price` - число, `statistics` - объект, как в запросе; есть `createdAt` - строка. Также проверяем, что значения соответствуют тем, которые были переданы в запросе

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-006

**Заголовок:** Два POST с одинаковым телом - разные `id`

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "iPhone",
  "price": 5000,
  "statistics": {
    "likes": 2,
    "viewCount": 50,
    "contacts": 3
  }
}
```

2. Сохранить `id` первого объявления
3. Повторить тот же POST 
4. Сохранить `id` второго объявления

**Ожидаемый результат:** Оба POST - HTTP 200; непустой `id` - строка; `sellerId` = число; `name` - строка, `price` - число, `statistics` - объект, как в запросе; есть `createdAt` - строка. Также проверяем, что значения соответствуют тем, которые были переданы в запросе; 
`id` первого объявления не равен `id` второго объявления

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## POST `/api/1/item` - негативные

**ID:** POST-007

**Заголовок:** Отсутствует поле `name` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "price": 1000,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле name обязательно"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-008

**Заголовок:** Отсутствует поле `price` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "Стул",
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле price обязательно"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-009

**Заголовок:** Отсутствует поле `sellerID` в теле запроса 

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "name": "Книга",
  "price": 500,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле sellerID обязательно"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-010

**Заголовок:** Отсутствует объект `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 333333,
  "name": "Без статистики",
  "price": 900
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле statistics обязательно"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-011

**Заголовок:** Отсутствует поле `likes` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "iPhone",
  "price": 5000,
  "statistics": {
    "viewCount": 50,
    "contacts": 3
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле likes обязательно"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-012

**Заголовок:** Отсутствует поле `viewCount` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "iPhone",
  "price": 5000,
  "statistics": {
    "likes": 2,
    "contacts": 3
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле viewCount обязательно"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-013

**Заголовок:** Отсутствует поле `contacts` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "iPhone",
  "price": 5000,
  "statistics": {
    "likes": 2,
    "viewCount": 50
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле contacts обязательно"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-014

**Заголовок:** Пустое тело запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и пустым телом:
```json
{}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле name обязательно"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-015

**Заголовок:** Пустая строка параметра `name` в теле запроса

**Шаги:**

1.  Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "",
  "price": 100,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле name обязательно"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-016

**Заголовок:** Отрицательное значение для параметра `price` в теле запроса

**Шаги:**

1.  Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": -1,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле price должно быть положительным"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-017

**Заголовок:** Дробное значение для параметра `price` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 999.99,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле price должно быть целым"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-018

**Заголовок:** Строковое значение для параметра `price` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": "дорого",
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле price должно быть числом"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-019

**Заголовок:** Строковое значение для параметра `sellerID` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": "abc",
  "name": "Товар",
  "price": 100,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле sellerID должно быть числом"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-020

**Заголовок:** Числовое значение для параметра `name` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": 123,
  "price": 100,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле name должно быть строкой"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-021

**Заголовок:** Строковое значение для параметра `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 100,
  "statistics": "abc"
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле statistics должно быть объектом JSON"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-022

**Заголовок:** Отрицательное значение для параметра `likes` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 100,
  "statistics": {
    "likes": -1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле likes не должно быть отрицательным"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-023

**Заголовок:** Дробное значение для параметра `likes` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 999,
  "statistics": {
    "likes": 9.4,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле likes должно быть целым"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-024

**Заголовок:** Строковое значение для параметра `likes` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 1000,
  "statistics": {
    "likes": "abc",
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле likes должно быть числом"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-025

**Заголовок:** Отрицательное значение для параметра `viewCount` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 333338,
  "name": "Товар",
  "price": 100,
  "statistics": {
    "likes": 1,
    "viewCount": -1,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле viewCount не должно быть отрицательным"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-026

**Заголовок:** Дробное значение для параметра `viewCount` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 999,
  "statistics": {
    "likes": 1,
    "viewCount": 9.4,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле viewCount должно быть целым"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-027

**Заголовок:** Строковое значение для параметра `viewCount` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 1000,
  "statistics": {
    "likes": 1,
    "viewCount": "abc",
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле viewCount должно быть числом"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-028

**Заголовок:** Отрицательное значение для параметра `contacts` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 333338,
  "name": "Товар",
  "price": 100,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": -1
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле contacts не должно быть отрицательным"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-029

**Заголовок:** Дробное значение для параметра `contacts` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 999,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 9.4
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле contacts должно быть целым"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-030

**Заголовок:** Строковое значение для параметра `contacts` в объекте `statistics` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 1000,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": "abc"
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле contacts должно быть числом"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-031

**Заголовок:** Битый JSON в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` с синтаксической ошибкой JSON в теле запроса:

```json
{
  "sellerID": 111111, 
  "name": "обрыв
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "Передан не валидный JSON"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-032

**Заголовок:** Передача невалидного заголовка `Content-Type: text/plain` при отправке запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: text/plain`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Проверка заголовка",
  "price": 100,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "Недопустимый тип контента"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## POST `/api/1/item` - корнер-кейсы

**ID:** POST-033

**Заголовок:** Лишнее поле `extraField` в теле запроса

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "С лишним полем",
  "price": 700,
  "statistics": { 
    "likes": 1, 
    "viewCount": 2, 
    "contacts": 3 
  },
  "extraField": "test"
}
```

**Ожидаемый результат:** HTTP 200; `id` - строка; `sellerId` = число; `name` - строка, `price` - число, `statistics` - объект, как в запросе; есть `createdAt` - строка. Также проверяем, что значения соответствуют тем, которые были переданы в запросе. Излишние поля должны игнорироваться

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-034

**Заголовок:** Значение для поля `name` длиной 1000 символов `A`

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
  "price": 100,
  "statistics": { 
    "likes": 1, 
    "viewCount": 3, 
    "contacts": 7 }
}
```

**Ожидаемый результат:** HTTP 200; `id` - строка; `sellerId` = число; `name` - строка, `price` - число, `statistics` - объект, как в запросе; есть `createdAt` - строка. Также проверяем, что значения соответствуют тем, которые были переданы в запросе.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-035

**Заголовок:** Значение меньше границы диапазона для `sellerID` = 111110

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 111110,
  "name": "Ниже диапазона",
  "price": 200,
  "statistics": {
    "likes": 0,
    "viewCount": 0,
    "contacts": 0
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле sellerID должно быть в диапазоне 111111-999999"
Параметр `status` содержит "400"

**Комментарий:** Непонятно диапазон 111111-999999 для `sellerID` является ограничением или нет, я бы уточнил необходимость данного сценария. На данный момент считаем, что является ограничением

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** POST-036

**Заголовок:** Значение больше границы диапазона для `sellerID` = 1000000

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 1000000,
  "name": "Выше диапазона",
  "price": 200,
  "statistics": {
    "likes": 0,
    "viewCount": 0,
    "contacts": 0
  }
}
```

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "поле sellerID должно быть в диапазоне 111111-999999"
Параметр `status` содержит "400"

**Комментарий:** Непонятно диапазон 111111-999999 для `sellerID` является ограничением или нет, я бы уточнил необходимость данного сценария. На данный момент считаем, что является ограничением

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## GET `/api/1/item/:id` - позитивные

**ID:** GET-OI-001

**Заголовок:** Отправить существующий `id`

**Предусловия:** Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "GET",
  "price": 4000,
  "statistics": {
    "likes": 11,
    "viewCount": 22,
    "contacts": 33
  }
}
```

Сохранить `id` объявления и ответ POST

**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/item/{id}` с `Accept: application/json`

**Ожидаемый результат:** HTTP 200; В массиве GET есть объявление, данные которого совпадают с ответом POST, а именно в полях `name`, `price`, `sellerId`, `statistics`, `createdAt`

**Комментарий:** Необходимо уточнять про массив в GET по `id`. Это выглядит странно

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## GET `/api/1/item/:id` - негативные

**ID:** GET-OI-002

**Заголовок:** Отправить несуществующий `id`

**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/item/{random_uuid_id}` с `Accept: application/json`

**Ожидаемый результат:** HTTP 404; Получено тело ответа следующего вида:
```json
{
  "result": "<string>",
  "status": "<string>"
}
```
Параметр `result` содержит "Объявление `{random_uuid_id}` не найдено"
Параметр `status` содержит "404"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-OI-003

**Заголовок:** Отправить удаленный `id`

**Предусловия:** 

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "GET",
  "price": 4000,
  "statistics": {
    "likes": 11,
    "viewCount": 22,
    "contacts": 33
  }
}
```

2. Сохранить `id` объявления
3. Отправить запрос `DELETE {{baseUrl}}/api/2/item/{id}`, указав id созданного объявления

**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/item/{id}` с `Accept: application/json` и `id` удаленного объявления

**Ожидаемый результат:** HTTP 404; Получено тело ответа следующего вида:
```json
{
  "result": "<string>",
  "status": "<string>"
}
```
Параметр `result` содержит "Объявление `id` не найдено"
Параметр `status` содержит "404"

**Статус:** _Passed / Failed / Skipped / Blocked_


---
**ID:** GET-OI-004

**Заголовок:** Формат `id` не uuid

**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/item/{random_number}` с `Accept: application/json`

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "ID айтема не uuid: {random_number}"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## GET `/api/1/item/:id` - корнер-кейсы

**ID:** GET-OI-005

**Заголовок:** Два GET подряд одного `id`

**Предусловия:** Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "GET",
  "price": 4000,
  "statistics": {
    "likes": 11,
    "viewCount": 22,
    "contacts": 33
  }
}
```

Сохранить `id` объявления

**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/item/{id}` с `Accept: application/json` и `id` созданного объявления
2. Повторить тот же GET.

**Ожидаемый результат:** Оба HTTP 200; полученные данные совпадают.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## GET `/api/1/:sellerID/item` - позитивные

**ID:** GET-AI-001

**Заголовок:** Список продавца с объявлениями

**Предусловия:** 
1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "GET",
  "price": 4000,
  "statistics": {
    "likes": 11,
    "viewCount": 22,
    "contacts": 33
  }
}
```

2. Повторно отправляем запрос `POST` с этим же телом


**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/845125/item` с `Accept: application/json`

**Ожидаемый результат:** HTTP 200; массив объявлений; у всех объектов `sellerId` = 845125

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-AI-002

**Заголовок:** Продавец без объявлений

**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/{random_number}/item` с `Accept: application/json` (random_number число в диапазоне 111111-999999, необходимо получить продавца без объявлений, при необходимости выполнить ретраи с другим random_number).

**Ожидаемый результат:** HTTP 200 и пустой массив в теле ответа `[]`

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## GET `/api/1/:sellerID/item` - негативные

**ID:** GET-AI-003

**Заголовок:** Указать в path `sellerID` = abc

**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/abc/item` с `Accept: application/json`

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "передан некорректный идентификатор продавца"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-AI-004

**Заголовок:** Указать в path `sellerID` = 0

**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/0/item` с `Accept: application/json`

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "передан некорректный идентификатор продавца"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-AI-005

**Заголовок:** Указать в path `sellerID` = -1

**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/-1/item` с `Accept: application/json`

**Ожидаемый результат:** HTTP 400; Получено тело ответа следующего вида:
```json
{
  "result": {
    "messages": {
      "culpa_b92": "<string>",
      "enim_24f": "<string>",
      "mollit_aa": "<string>"
    },
    "message": "<string>"
  },
  "status": "<string>"
}
```
Параметр `message` в объекте `result` содержит "передан некорректный идентификатор продавца"
Параметр `status` содержит "400"

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## GET `/api/1/:sellerID/item` - корнер-кейсы

**ID:** GET-AI-006

**Заголовок:** Два GET списка подряд (Идемпотентность запроса)

**Предусловия:** 1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "Стабильный список",
  "price": 50,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```
**Шаги:**

1. Отправить запрос `GET {{baseUrl}}/api/1/845125/item`
2. Сохранить тело ответа
3. Повторить тот же GET
4. Сохранить тело ответа
5. Сравнить 2 тела ответа 

**Ожидаемый результат:** Оба запроса HTTP 200; тело ответа первого запроса равен телу запроса второго запроса.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## GET `/api/1/statistic/:id` и GET `/api/2/statistic/:id` — позитивные

**ID:** GET-STAT-001

**Заголовок:** Статистика по существующему объявлению (`GET /api/1/statistic/{id}`)

**Предусловия:** 1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 100,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```
2. Сохранить `id` и `statistics` 

**Шаги:**

1. Отправить `GET {{baseUrl}}/api/1/statistic/{id}` с `Accept: application/json`

**Ожидаемый результат:** HTTP 200; заголовок `Content-Type` с `application/json`; тело — JSON-массив объектов с полями `likes`, `viewCount`, `contacts`, должны совпадать с `statistics`, которую отправляли в POST

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-STAT-002

**Заголовок:** Статистика по существующему объявлению (`GET /api/2/statistic/{id}`)

**Предусловия:** 1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:

```json
{
  "sellerID": 845125,
  "name": "Товар",
  "price": 100,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```
2. Сохранить `id` и `statistics` 

**Шаги:**

1. Отправить `GET {{baseUrl}}/api/2/statistic/{id}` с `Accept: application/json`

**Ожидаемый результат:** HTTP 200; заголовок `Content-Type` с `application/json`; тело — JSON-массив объектов с полями `likes`, `viewCount`, `contacts`, должны совпадать с `statistics`, которую отправляли в POST

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## GET `/api/1/statistic/:id` и GET `/api/2/statistic/:id` — негативные

**ID:** GET-STAT-003

**Заголовок:** Запрос без идентификатора объявления (`GET /api/1/statistic` без `{id}`)

**Предусловия:** нет

**Шаги:**

1. Отправить `GET {{baseUrl}}/api/1/statistic` с `Accept: application/json` (без сегмента `/{id}` в пути).

**Ожидаемый результат:** HTTP 404; тело JSON с описанием, что маршрут не найден (например, сообщение вида `route ... not found`).

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-STAT-004

**Заголовок:** Запрос без идентификатора объявления (`GET /api/2/statistic` без `{id}`)

**Предусловия:** нет

**Шаги:**

1. Отправить `GET {{baseUrl}}/api/2/statistic` с `Accept: application/json`.

**Ожидаемый результат:** HTTP 404; тело JSON с описанием, что маршрут не найден.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-STAT-005

**Заголовок:** Параметр `id` не в формате UUID (`GET /api/1/statistic/{id}`)

**Предусловия:** нет

**Шаги:**

1. Отправить `GET {{baseUrl}}/api/1/statistic/{id}` с `Accept: application/json`, подставив вместо `{id}` строку из цифр (не UUID), например `123456`.

**Ожидаемый результат:** HTTP 400; тело ошибки в формате API для 400; в `result.message` есть текст о том, что передан некорректный идентификатор объявления.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-STAT-006

**Заголовок:** Параметр `id` не в формате UUID (`GET /api/2/statistic/{id}`)

**Предусловия:** нет

**Шаги:**

1. Отправить `GET {{baseUrl}}/api/2/statistic/{id}` с `Accept: application/json`, подставив вместо `{id}` строку из цифр (не UUID).

**Ожидаемый результат:** Отклонение запроса с ошибкой валидации идентификатора; на текущем стенде может отличаться код HTTP от v1 (например, 404 при том же смысле сообщения в теле). Автотест фиксирует фактическое поведение стенда.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-STAT-007

**Заголовок:** Существующий формат UUID, объявления нет (`GET /api/1/statistic/{id}`)

**Предусловия:** нет

**Шаги:**

1. Сгенерировать валидный UUID v4, которому не соответствует созданное объявление.
2. Отправить `GET {{baseUrl}}/api/1/statistic/{id}` с `Accept: application/json`.

**Ожидаемый результат:** HTTP 404; в теле указано, что статистика для данного `id` не найдена (или эквивалентная формулировка); идентификатор присутствует в тексте сообщения.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-STAT-008

**Заголовок:** Существующий формат UUID, объявления нет (`GET /api/2/statistic/{id}`)

**Предусловия:** нет

**Шаги:**

1. Сгенерировать валидный UUID v4 без объявления в системе.
2. Отправить `GET {{baseUrl}}/api/2/statistic/{id}` с `Accept: application/json`.

**Ожидаемый результат:** HTTP 404; сообщение о том, что статистика для `id` не найдена.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## GET `/api/1/statistic/:id` и GET `/api/2/statistic/:id` — корнер-кейсы

**ID:** GET-STAT-009

**Заголовок:** Два запроса `GET /api/1/statistic/{id}` подряд (идемпотентность)

**Предусловия:** 1. Создать объявление `POST {{baseUrl}}/api/1/item`, сохранить `id`.

**Шаги:**

1. Отправить `GET {{baseUrl}}/api/1/statistic/{id}` с `Accept: application/json`, сохранить тело ответа.
2. Повторить тот же запрос.
3. Сравнить два тела ответа.

**Ожидаемый результат:** Оба ответа HTTP 200; JSON-массивы побайтово/логически совпадают (при неизменных данных на сервере).

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-STAT-010

**Заголовок:** Два запроса `GET /api/2/statistic/{id}` подряд (идемпотентность)

**Предусловия:** 1. Создать объявление `POST {{baseUrl}}/api/1/item`, сохранить `id`.

**Шаги:**

1. Дважды выполнить `GET {{baseUrl}}/api/2/statistic/{id}` с `Accept: application/json`.

**Ожидаемый результат:** Оба HTTP 200; тела ответов совпадают.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-STAT-011

**Заголовок:** Заголовок `Content-Type: text/plain` на GET (у GET нет тела запроса)

**Предусловия:** 1. Создать объявление, сохранить `id`.

**Шаги:**

1. Отправить `GET {{baseUrl}}/api/1/statistic/{id}` или `GET {{baseUrl}}/api/2/statistic/{id}` с заголовками `Accept: application/json` и `Content-Type: text/plain`.

**Ожидаемый результат:** HTTP 200; ответ по-прежнему JSON; заголовок ответа `Content-Type` содержит `application/json`; значения статистики согласованы с телом создания объявления.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** GET-STAT-012

**Заголовок:** Заголовок `Accept: */*`

**Предусловия:** 1. Создать объявление, сохранить `id`.

**Шаги:**

1. Отправить `GET {{baseUrl}}/api/1/statistic/{id}` с `Accept: */*`.

**Ожидаемый результат:** HTTP 200; тело — JSON-массив статистики; при необходимости проверить `Content-Type` ответа.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## E2E

**ID:** E2E-001

**Заголовок:** Объявление — GET по id, список продавца, статистика v1 и v2

**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с 
`Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "E2E цикл",
  "price": 5000,
  "statistics": {
    "likes": 1,
    "viewCount": 2,
    "contacts": 3
  }
}
```
2. Сохраняем `id` из тела ответа POST (или из последующего GET при необходимости)
3. Отправить запрос `GET {{baseUrl}}/api/1/item/{id}` с `Accept: application/json` — HTTP 200, данные объявления совпадают с телом `POST`
4. Отправить запрос `GET {{baseUrl}}/api/1/845125/item` с `Accept: application/json` — объявление присутствует в списке
5. Отправить `GET {{baseUrl}}/api/1/statistic/{id}` — HTTP 200, массив статистики согласован с `statistics` из POST
6. Отправить `GET {{baseUrl}}/api/2/statistic/{id}` — HTTP 200, массив статистики согласован с `statistics` из POST

**Ожидаемый результат (ОР):** Все шаги с ожидаемыми результатами.

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** E2E-002

**Заголовок:** Три объявления — список и статистика по каждому id

**Шаги:**

1-3. Отправить три запроса `POST {{baseUrl}}/api/1/item` с разными телами (один `sellerID`, разные `name`/`price`/`statistics`), сохранить три `id`.
4. `GET {{baseUrl}}/api/1/845125/item` — в списке есть все три `id`.
5. Для каждого `id` выполнить `GET {{baseUrl}}/api/1/statistic/{id}` и `GET {{baseUrl}}/api/2/statistic/{id}` — HTTP 200, значения совпадают с `statistics` соответствующего POST.

**Ожидаемый результат:** Ожидания на каждом шаге выполнены

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** E2E-003
**Заголовок:** Два продавца
**Предусловия:** нет
**Шаги:**

1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 111222,
  "name": "A",
  "price": 1000,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
``` 
(Ожидаем получение id_1)
2. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 333444,
  "name": "B",
  "price": 2000,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```
(Ожидаем получение id_2)
3. GET `/api/1/111222/item` - Видим объявление с `id_1`, но не видим объявление с `id_2`
4. GET `/api/1/333444/item` - Видим объявление с `id_2`, но не видим объявление с `id_1`

**Ожидаемый результат:** Объявления изолированы по пользователям при вызове списка объявлений продавца

**Статус:** _Passed / Failed / Skipped / Blocked_

---
## Нефункциональные

**ID:** NFR-001

**Заголовок:** Время ответа и `Content-Type: application/json` POST запроса

**Шаги:**
1. Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "Скорость",
  "price": 2000,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

**Ожидаемый результат:** HTTP 200. Время ≤ порога, например 500 мс (может быть другим, необходимо уточнять). Есть заголовок `Content-Type: application/json`

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** NFR-002

**Заголовок:** Время GET по `id`

**Предусловия:** Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "Скорость",
  "price": 2000,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

Сохранить `id`

**Шаги:**
1. Отправить запрос `GET {{baseUrl}}/api/1/item/{id}` с `Accept: application/json`

**Ожидаемый результат:** HTTP 200. Время ≤ порога, например 500 мс (может быть другим, необходимо уточнять). Есть заголовок `Content-Type: application/json`

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** NFR-003

**Заголовок:** Время GET списка

**Предусловия:** Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "Скорость",
  "price": 2000,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

Сохранить `id`

**Шаги:**
1. Отправить запрос `GET {{baseUrl}}/api/1/845125/item` с `Accept: application/json`

**Ожидаемый результат:** HTTP 200. Время ≤ порога, например 500 мс (может быть другим, необходимо уточнять). Есть заголовок `Content-Type: application/json`

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** NFR-004

**Заголовок:** Неподдерживаемый метод PATCH

**Предусловия:** Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "Скорость",
  "price": 2000,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

Сохранить `id`

**Шаги:**
1. `PATCH {{baseUrl}}/api/1/item/{id}` с телом `{}`.

**Ожидаемый результат:** HTTP 405. Пустое тело ответа

**Статус:** _Passed / Failed / Skipped / Blocked_

---
**ID:** NFR-005

**Заголовок:** Время ответа GET статистики v1 и v2

**Предусловия:** Отправить запрос `POST {{baseUrl}}/api/1/item` с `Content-Type: application/json`, `Accept: application/json` и телом:
```json
{
  "sellerID": 845125,
  "name": "Скорость",
  "price": 2000,
  "statistics": {
    "likes": 1,
    "viewCount": 3,
    "contacts": 7
  }
}
```

Сохранить `id`

**Шаги:**

1. Измерить время ответа `GET {{baseUrl}}/api/1/statistic/{id}` с `Accept: application/json`.
2. Измерить время ответа `GET {{baseUrl}}/api/2/statistic/{id}` с `Accept: application/json`.

**Ожидаемый результат:** Оба запроса HTTP 200; время каждого не превышает порога (например, 500 мс — задаётся в автотестах переменной окружения). Заголовок `Content-Type` ответа содержит `application/json`.

**Статус:** _Passed / Failed / Skipped / Blocked_
