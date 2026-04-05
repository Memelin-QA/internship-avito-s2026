# internship-avito-s2026 — API-автотесты

Автотесты по [TESTCASES.md](TESTCASES.md) для сервиса объявлений (`baseUrl`: `https://qa-internship.avito.com`).

## Структура проекта (корень репозитория)

| Файл | Назначение |
|------|------------|
| `models.py` | Pydantic-модели ответов |
| `helpers.py` | UUID, вложения Allure, проверки 400/404, извлечение `id` из успешного POST, поиск «пустого» продавца |
| `conftest.py` | Фикстуры: `base_url`, `api_client`, `session_seller_id` (111111–999999 на сессию), `speed_body`, `domain`, `nfr_max_ms`. |
| `api_client.py` | **Client Layer** — `requests.Session`, методы POST/GET/PATCH, в т.ч. statistic v1/v2. |
| `domain.py` | **Domain Layer** — сценарии: создание объявления, списки, статистика, шаги Allure. |
| `post_tests.py` | **Test Layer** — POST `/api/1/item` (POST-001 - POST-036). |
| `get_oi_tests.py` | GET `/api/1/item/:id` (GET-OI-001 - GET-OI-005). |
| `get_ai_tests.py` | GET `/api/1/:sellerID/item` (GET-AI-001 - GET-AI-006). |
| `get_statistic_tests.py` | GET `/api/1/statistic/:id`, `/api/2/statistic/:id` (GET-STAT-001 - GET-STAT-012). |
| `e2e_tests.py` | E2E-001 - E2E-003. |
| `nonfunctional_tests.py` | NFR-001 - NFR-005 (время ответа, PATCH 405). |
| `requirements.txt` | Зависимости с **зафиксированными версиями** (`==`). |
| `pyproject.toml` | Метаданные проекта и настройки **Ruff** (линтер + форматтер). |
| `pytest.ini` | Pytest: собираются файлы `*_tests.py`, результаты Allure в `allure-results/`. |
| `BUGS.md` | Дефекты стенда относительно TESTCASES; тесты с расхождениями помечены `pytest.mark.xfail`. |

Переменные окружения:

- `API_BASE_URL` — базовый URL (по умолчанию `https://qa-internship.avito.com`).
- `NFR_MAX_MS` — порог времени для NFR (по умолчанию `500`).

## Установка

Требуется **Python 3.10+**.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

На Linux/macOS: `source .venv/bin/activate`.

Если команды `pytest` / `ruff` не находятся в PATH, используйте `python -m pytest` и `python -m ruff` из активированного venv.

## Запуск тестов

Все тесты:

```bash
pytest -v
```

Один файл (пример):

```bash
pytest post_tests.py -v
```

Один тест по полному идентификатору (пример — POST-001):

```bash
pytest post_tests.py::TestPostPositive::test_post_001_success_mid_range_seller -v
```

### Линтер, форматтер и полный прогон тестов

Из корня репозитория после установки зависимостей:

```bash
ruff check .
ruff format . --check
pytest -q
```

Эквивалент через `python -m` (если в PATH нет исполняемых `ruff` / `pytest`):

```bash
python -m ruff check .
python -m ruff format . --check
python -m pytest -q
```

Идентификаторы из [TESTCASES.md](TESTCASES.md) (`POST-001`, `GET-OI-002`, `NFR-005` и т.д.) дублируются в **`@allure.testcase(...)`** и в заголовках `@allure.title`. Один файл тестов соответствует группе ручек (например `get_statistic_tests.py` — GET-STAT).

### Данные: `sellerID`

Для сценариев с созданием объявлений используется **`session_seller_id`**, чтобы снизить пересечения с чужими данными на общем стенде.

## Allure

Плагин `allure-pytest` подключён в `pytest.ini` (`--alluredir=allure-results`). В тестах и в `domain` используются `@allure.step`, `@allure.title`, `@allure.description`, `@allure.epic` / `feature` / `story`, динамические заголовки/описания в параметризованных кейсах, вложения запроса/ответа через `helpers.attach_request_response`. В `conftest.py` после прогона добавляется `allure-results/environment.properties` (в т.ч. `API_BASE_URL`).

### Требования для генерации отчёта

- **Java 8+** и `JAVA_HOME` (проверьте: `java -version`)
- **Allure Commandline** (проверьте: `allure --version`)

#### Установка Allure CLI

- **Windows** `scoop install allure`
- **macOS**: `brew install allure`
- **Linux**: `sudo apt-add-repository ppa:qameta/allure && sudo apt-get install allure`

### 1. Записать результаты прогона

```bash
pytest
```

### 2. Сгенерировать HTML-отчёт (каталог `allure-report/`) и открыть в браузере

**С установленным [Allure Commandline](https://github.com/allure-framework/allure2/releases )** (`allure` в `PATH`):

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## Линтер и форматтер (Ruff)

Конфигурация зафиксирована в **`pyproject.toml`**:

- **`[tool.ruff]`** — целевая версия Python, длина строки, каталоги исходников, исключения (в т.ч. `allure-results`).
- **`[tool.ruff.lint]`** — включённые правила: `E`, `W`, `F`, `I`, `UP`, `B`; строка длиной игнорируется как `E501` (контроль через форматтер).
- **`[tool.ruff.lint.isort]`** — известные first-party-модули проекта.
- **`[tool.ruff.format]`** — стиль кавычек и форматирование (аналог Black).

Зависимость `ruff` указана в `requirements.txt` (секция dev). Установка вместе с остальным: `pip install -r requirements.txt`.

Проверка стиля и импортов:

```bash
ruff check .
```

Автоисправление где возможно:

```bash
ruff check . --fix
```

Форматирование кода:

```bash
ruff format .
```

Проверка форматирования без записи в файлы:

```bash
ruff format . --check
```

## Дефекты стенда и xfail

Расхождения живого стенда с [TESTCASES.md](TESTCASES.md) описаны в **[BUGS.md](BUGS.md)** (шаблон: описание, шаги, факт/ожидание, серьёзность, окружение). Соответствующие автотесты помечены **`pytest.mark.xfail`**, чтобы общий прогон оставался зелёным до исправления API.

## Про стенд и TESTCASES.md

Автотесты ориентированы на **ожидания из TESTCASES.md** (тексты ошибок, коды, границы полей). Публичный стенд `qa-internship.avito.com` может отличаться (например, успешный POST возвращает только строку `status` с UUID, а полное объявление приходит из GET). В коде учтено извлечение `id` из ответа POST и последующий GET для проверки полей. Оставшиеся расхождения при прогоне против живого стенда отражают разницу между спецификацией в `TESTCASES.md` и текущей реализацией API.
