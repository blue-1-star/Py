#!/usr/bin/env python
"""
Главный скрипт для генерации всей архитектурной документации OSBB.
Запуск: python OSBB_util/scripts/build_docs.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from local_config import local_config


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_file(filepath: Path, content: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ {filepath.relative_to(local_config.py_root)}")


def create_roadmap() -> None:
    content = '''# OSBB Roadmap

<!-- RESIDENT_IDENTITY_REFACTOR_V1:BEGIN -->

## P1. Resident Identity Refactor

**Status:** planned  
**Date decided:** 2026-07-01  
**Reason:** current resident/client/admin flow mixes several different concepts and creates confusing behavior.

### Problem

The current legacy flow around "Режим мешканця", "Змінити квартиру", apartment binding, resident verification, and admin testing is mixed.

It currently blends together:
- resident self-service cabinet;
- apartment binding and verification;
- operator work on behalf of a resident;
- super-admin diagnostic view;
- real Telegram ID to apartment binding.

This creates unclear states, especially for super-admins and operators.

### Decision

Split the old mixed flow into three separate flows.

#### 1. Resident Cabinet
Real resident acts for themselves. Resident can:
- view and confirm their apartment;
- maintain personal contact data;
- add, edit, or request changes to vehicles;
- submit remote/pult requests;
- see charges, payments, and service history.

#### 2. Operator Workspace
Operator acts on request of a resident, but never becomes that resident. All actions must be auditable.

#### 3. Super-admin Diagnostic Resident View
Super-admin can temporarily view the bot as a chosen apartment/resident for diagnostics.

### Legacy rule
The existing flow around "Змінити квартиру" and "Режим мешканця" is considered legacy and should not be expanded.

<!-- RESIDENT_IDENTITY_REFACTOR_V1:END -->

<!-- CORE_NEW_LAYER_V1:BEGIN -->

## P2. New Architecture Layer (core_new)

**Status:** completed (2026-07-13)

### What was done

Created a new architectural layer `core_new/` that separates business logic from interface code.

#### 1. Adapters
Created `DBAdapter` — a wrapper around the legacy `Bots/db_access.py`.

#### 2. Domain Models

| Model | Status | Tests |
|-------|--------|-------|
| `Vehicle` | ✅ | ✅ |
| `Resident` | ✅ | ✅ |
| `Apartment` | ✅ | ✅ |
| `Payment` | ✅ | ✅ |
| `VehicleCandidate` | ✅ | ✅ |

#### 3. Testing

All models have working tests in `tests/`.

#### 4. Documentation

- [ADR-2026-07-13-core-new-layer.md](Architecture/ADR-2026-07-13-core-new-layer.md)
- [Domain models](../Domain/README.md)
- [core_new code docs](../Code/core_new.md)

### Next steps

1. Replace legacy calls with new domain models
2. Integrate all models into Telegram bot
3. Remove duplicate code

<!-- CORE_NEW_LAYER_V1:END -->

<!-- CASHIER_VEHICLE_CANDIDATE_V1:BEGIN -->

## P3. Cashier and Vehicle Candidate (В работе)

**Status:** in progress (2026-07-14)

### Problem

Cashier cannot accept payments for vehicles without an apartment.

### Decision

Create a new entity: `vehicle_candidates`.

### Lifecycle

PENDING -> RESOLVED -> vehicle created in vehicles
PENDING -> REJECTED

### Next steps

1. Integrate `vehicle_candidates` into cashier UI
2. Add operator workspace for reviewing candidates
3. Link payments to candidates via `candidate_id`

<!-- CASHIER_VEHICLE_CANDIDATE_V1:END -->
'''
    docs_dir = local_config.py_root / "OSBB" / "Docs"
    ensure_dir(docs_dir)
    write_file(docs_dir / "ROADMAP.md", content)


def create_changelog() -> None:
    content = '''# Changelog — core_new

## 2026-07-14 — Vehicle Candidate (новая сущность)

### Что сделано

Создана новая сущность `vehicle_candidates` для обработки автомобилей без квартиры.

**Причина:**
- Касса не могла принять оплату за автомобиль без квартиры (NOT NULL constraint).
- Оператору нужно принимать оплату на месте, даже если житель не помнит номер квартиры.

**Решение:**
- Создана таблица `vehicle_candidates`.
- Создана модель `VehicleCandidate` в `core_new/domain/`.
- Касса создаёт кандидата вместо прямого INSERT в `vehicles`.
- Платеж привязывается к `candidate_id`.

**Статусы кандидата:**
- `PENDING` — создан, ждёт обработки.
- `RESOLVED` — подтверждён, создан автомобиль в `vehicles`.
- `REJECTED` — отклонён.

---

## 2026-07-13 — Реализация нового ядра core_new

### Что сделано

#### 1. Создание слоя core_new

Создан новый архитектурный слой `core_new/` для отделения бизнес-логики от интерфейсов.

#### 2. Реализация адаптера

Создан `DBAdapter` — обёртка над `Bots/db_access.py`.

#### 3. Доменные модели

| Модель | Файл | Статус |
|--------|------|--------|
| `Vehicle` | `domain/vehicles.py` | ✅ |
| `Resident` | `domain/residents.py` | ✅ |
| `Apartment` | `domain/apartments.py` | ✅ |
| `Payment` | `domain/payments.py` | ✅ |
| `VehicleCandidate` | `domain/vehicle_candidate.py` | ✅ |

#### 4. Тесты

Созданы тесты для всех моделей.

#### 5. Документация

- `ADR-2026-07-13-core-new-layer.md`
- `ADR-2026-07-13-domain-models.md`
- `Domain/README.md`
- `Domain/vehicles.md`, `residents.md`, `apartments.md`, `payments.md`
- `Code/core_new.md`
'''
    docs_dir = local_config.py_root / "OSBB" / "Docs" / "Changelog"
    ensure_dir(docs_dir)
    write_file(docs_dir / "CHANGELOG_core_new.md", content)


def create_adr_core_new_analysis() -> None:
    content = '''# ADR-2026-07-14: Выделение бизнес-логики из интерфейса (core_new)

**Дата:** 2026-07-14

**Статус:** Принято

**Автор:** San Tretiak

## Контекст

Проект OSBB развивался как Telegram-бот. Бизнес-логика оказалась жёстко вплетена в код интерфейса.

### Проблема до внедрения

1. **Смешение ответственности:**
   - `Bots/parking_bot.py` содержал прямые вызовы к БД и бизнес-проверки.
   - `Bots/handlers/client_portal.py` содержал бизнес-логику формирования счетов.

2. **Сложность тестирования:**
   - Бизнес-правила можно было проверить только через запуск бота.

3. **Жёсткая связанность:**
   - Любое изменение в бизнес-логике требовало правки интерфейсного кода.

4. **Разрастание `db_access.py`:**
   - Файл вырос до 157 KB и содержал не только CRUD, но и бизнес-логику.

---

## Решение: создание слоя `core_new`

Создан новый слой, который:
1. **Не трогает старый код** — он продолжает работать.
2. **Содержит чистую бизнес-логику** в `domain/`.
3. **Общается со старым кодом через адаптеры** (`adapters/`).

---

## Преимущества внедрения

| Аспект | До `core_new` | После `core_new` |
|--------|---------------|------------------|
| **Тестируемость** | Бизнес-логику нельзя протестировать без бота. | Каждая модель тестируется изолированно. |
| **Развитие** | Новая фича -> правка бота -> риск сломать. | Новая фича -> добавляем модель -> подключаем через адаптер. |
| **Поддержка** | Логика размазана по `Bots/` и `tools/`. | Логика собрана в `domain/`. |
| **Интеграция** | Новый интерфейс -> копирование логики. | Новый интерфейс -> использование `domain/`. |

---

## Конкретные улучшения

| Модуль | Было | Стало |
|--------|------|-------|
| `Bots/parking_bot.py` | `show_my_vehicles()` содержала логику получения авто. | Теперь вызывает `Vehicle.get_by_apartment()`. |
| `Bots/handlers/client_portal.py` | `_billing_data()` — сложная логика расчётов. | Со временем переедет в `domain/billing.py`. |
| `Bots/db_access.py` | `get_next_vehicle_for_review()` — бизнес-правило. | Переписано как `Vehicle.get_next_for_review()`. |

---

## Связанные документы

- [core_new документация](../Code/core_new.md)
- [Доменная модель](../Domain/README.md)
- [ROADMAP.md](../ROADMAP.md) — секция P2
'''
    docs_dir = local_config.py_root / "OSBB" / "Docs" / "Architecture"
    ensure_dir(docs_dir)
    write_file(docs_dir / "ADR-2026-07-14-core_new-analysis.md", content)


def create_adr_vehicle_candidate() -> None:
    content = '''# ADR-2026-07-14: Введение сущности Vehicle Candidate

**Дата:** 2026-07-14

**Статус:** Принято

**Автор:** San Tretiak

## Контекст

Касса принимает оплату за парковку. Оператор вводит номер автомобиля.

Если автомобиль не найден в БД, оператору нужно создать "черновик" автомобиля и принять оплату. Но `vehicles` требует `apartment_id NOT NULL`, а квартира может быть неизвестна.

### Проблема

- `vehicles.apartment_id` — обязательное поле (`NOT NULL`).
- Оператор не может создать автомобиль без квартиры.
- Платеж (`payments`) требует `apartment_number NOT NULL`.

---

## Решение

Создать новую сущность `vehicle_candidates` — "кандидат в автомобили".

### Архитектура

vehicle_candidates (черновик)
  - PENDING -> ожидает обработки
  - RESOLVED -> создан автомобиль в vehicles
  - REJECTED -> отклонён

### Преимущества

| Аспект | Старый подход | Новый подход |
|--------|---------------|--------------|
| **Целостность** | Нарушается NOT NULL | Сохраняется |
| **Чистота данных** | "Квартира 0" в отчетах | Кандидаты не попадают в отчеты |
| **Логика** | Фиктивная квартира | Отдельная сущность со смыслом |

---

## Связанные документы

- [Data Dictionary](../Database/Data_Dictionary.md)
- [ROADMAP.md](../ROADMAP.md) — секция P3
'''
    docs_dir = local_config.py_root / "OSBB" / "Docs" / "Architecture"
    ensure_dir(docs_dir)
    write_file(docs_dir / "ADR-2026-07-14-vehicle-candidate.md", content)


def create_data_dictionary() -> None:
    content = '''# Словарь данных OSBB (Data Dictionary)

**Версия:** 1.0  
**Дата обновления:** 2026-07-14  
**Назначение:** Единый справочник по структуре базы данных проекта OSBB.

---

## 1. Таблица `apartments`

| Колонка | Тип | Обязательное | Описание |
|---------|-----|--------------|----------|
| `id` | INTEGER | ✅ | Уникальный идентификатор (PK) |
| `apartment_number` | TEXT | ✅ | Номер квартиры/помещения |
| `entrance` | TEXT | ❌ | Номер подъезда |
| `unit_type` | TEXT | ❌ | Тип: RESIDENTIAL, COMMERCIAL, PARKING |
| `record_status` | TEXT | ❌ | ACTIVE, ARCHIVED, MERGED |
| `display_name` | TEXT | ❌ | Отображаемое имя |
| `created_at` | TEXT | ❌ | Дата создания |

**Связи:** apartments.id -> resident_accounts.apartment_id, vehicles.apartment_id

---

## 2. Таблица `resident_accounts`

| Колонка | Тип | Обязательное | Описание |
|---------|-----|--------------|----------|
| `id` | INTEGER | ✅ | Уникальный идентификатор (PK) |
| `telegram_user_id` | INTEGER | ✅ | Telegram ID |
| `telegram_username` | TEXT | ❌ | Username |
| `telegram_first_name` | TEXT | ❌ | Имя |
| `telegram_last_name` | TEXT | ❌ | Фамилия |
| `language_code` | TEXT | ❌ | Язык: ru, uk, en |
| `apartment_id` | INTEGER | ❌ | Ссылка на квартиру |
| `role` | TEXT | ❌ | resident, admin, super_admin, guard, operator |
| `status` | TEXT | ❌ | new, apartment_confirmed, operator_verified, blocked |
| `verified_at` | TEXT | ❌ | Дата подтверждения |

**Связи:** resident_accounts.apartment_id -> apartments.id

---

## 3. Таблица `service_catalog`

| Колонка | Тип | Обязательное | Описание |
|---------|-----|--------------|----------|
| `id` | INTEGER | ✅ | Уникальный идентификатор (PK) |
| `service_code` | TEXT | ✅ | Код услуги (например, PARKING_DAY) |
| `service_name` | TEXT | ✅ | Название услуги |
| `service_group` | TEXT | ❌ | MONTHLY, FUNDRAISING, COMMERCIAL, ACCESS_CONTROL |
| `service_type` | TEXT | ❌ | MONTHLY, ONE_TIME, FUNDRAISING, COMMERCIAL |
| `category` | TEXT | ❌ | PARKING, ACCESS, IMPROVEMENT, EQUIPMENT, BARRIER |
| `is_active` | INTEGER | ❌ | Доступна (1 — да) |
| `access_policy_enabled` | INTEGER | ❌ | Включена политика доступа |
| `access_policy_mode` | TEXT | ❌ | BLOCK, ALLOW, WARN |

**Связи:** service_catalog.service_code -> payments.base_service_code

---

## 4. Таблица `vehicles`

| Колонка | Тип | Обязательное | Описание |
|---------|-----|--------------|----------|
| `id` | INTEGER | ✅ | Уникальный идентификатор (PK) |
| `apartment_id` | INTEGER | ✅ | Ссылка на квартиру |
| `license_plate` | TEXT | ❌ | Номер автомобиля |
| `license_plate_normalized` | TEXT | ❌ | Нормализованный номер |
| `car_model` | TEXT | ❌ | Марка и модель |
| `car_model_normalized` | TEXT | ❌ | Нормализованная марка |
| `parking_time` | TEXT | ❌ | Day, Night, Inactive, NULL |

**Связи:** vehicles.apartment_id -> apartments.id, vehicles.id -> payments.vehicle_id

---

## 5. Таблица `payments`

| Колонка | Тип | Обязательное | Описание |
|---------|-----|--------------|----------|
| `id` | INTEGER | ✅ | Уникальный идентификатор (PK) |
| `payment_date` | TEXT | ❌ | Дата платежа |
| `apartment_number` | TEXT | ✅ | Номер квартиры |
| `vehicle_id` | INTEGER | ❌ | Ссылка на автомобиль |
| `amount` | REAL | ✅ | Сумма |
| `currency` | TEXT | ✅ | UAH |
| `payment_method` | TEXT | ❌ | cash, card, bank |
| `base_service_code` | TEXT | ❌ | Код услуги из каталога |
| `candidate_id` | INTEGER | ❌ | Ссылка на vehicle_candidates.id |

---

## 6. Таблица `vehicle_candidates`

**Назначение:** Хранит информацию об автомобилях, которые ещё не подтверждены.

| Колонка | Тип | Обязательное | Описание |
|---------|-----|--------------|----------|
| `id` | INTEGER | ✅ | Уникальный идентификатор (PK) |
| `license_plate` | TEXT | ✅ | Номер автомобиля |
| `license_plate_normalized` | TEXT | ✅ | Нормализованный номер |
| `car_model` | TEXT | ❌ | Марка и модель |
| `apartment_id` | INTEGER | ❌ | Ссылка на квартиру (может быть NULL) |
| `apartment_number` | TEXT | ❌ | Номер квартиры |
| `status` | TEXT | ✅ | PENDING, RESOLVED, REJECTED, MERGED |
| `resolved_vehicle_id` | INTEGER | ❌ | Ссылка на vehicles.id |
| `created_by` | INTEGER | ❌ | ID создателя |
| `created_at` | TEXT | ❌ | Дата создания |
| `comment` | TEXT | ❌ | Комментарий оператора |
| `source` | TEXT | ❌ | cashier, telegram, tbot |

**Жизненный цикл:** PENDING -> RESOLVED / REJECTED
'''
    docs_dir = local_config.py_root / "OSBB" / "Docs" / "Database"
    ensure_dir(docs_dir)
    write_file(docs_dir / "Data_Dictionary.md", content)


def create_domain_models() -> None:
    domain_dir = local_config.py_root / "OSBB" / "Docs" / "Domain"
    ensure_dir(domain_dir)

    vehicles = '''# Vehicle — Модель автомобиля

## Назначение

Управление автомобилями в системе.

## Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int | Уникальный ID |
| `apartment_number` | str | Номер квартиры |
| `plate` | str | Номер автомобиля |
| `model` | str | Марка автомобиля |
| `parking_time` | str | Тариф: Day, Night, Inactive, NULL |

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `display_name` | str | AA8098MM | Toyota |
| `status_display` | str | День / Ночь / Не паркуется |
| `is_parking` | bool | Паркуется ли (Day или Night) |
| `is_active` | bool | Активен ли (не Inactive) |

## Методы

| Метод | Возвращает | Описание |
|-------|------------|----------|
| `get_by_id(id)` | `Vehicle` | Получить автомобиль по ID |
| `get_by_apartment(apartment)` | `List[Vehicle]` | Все авто квартиры |
| `set_parking_time(status)` | `tuple` | Установить тариф |

## Пример

from core_new.domain.vehicles import Vehicle

vehicles = Vehicle.get_by_apartment("105")
for v in vehicles:
    print(f"{v.display_name}: {v.status_display}")
'''
    write_file(domain_dir / "vehicles.md", vehicles)

    residents = '''# Resident — Модель жителя

## Назначение

Управление пользователями Telegram и их связью с квартирами.

## Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `telegram_user_id` | int | Telegram ID |
| `first_name` | str | Имя |
| `last_name` | str | Фамилия |
| `apartment_number` | str | Номер квартиры |
| `status` | str | new, apartment_confirmed, operator_verified, blocked |
| `role` | str | resident, admin, super_admin, guard, operator |

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `display_name` | str | Иван Петров |
| `has_apartment` | bool | Привязана ли квартира |
| `status_display` | str | Проверен оператором |

## Методы

| Метод | Возвращает | Описание |
|-------|------------|----------|
| `get_by_telegram_id(id)` | `Resident` | Получить по Telegram ID |
| `get_by_apartment(apartment)` | `List[Resident]` | Все жители квартиры |
| `link_apartment(apartment)` | `tuple` | Привязать квартиру |
| `mark_verified_by_operator()` | `tuple` | Подтвердить оператором |

## Пример

from core_new.domain.residents import Resident

resident = Resident.get_by_telegram_id(12345)
print(resident.display_name)
'''
    write_file(domain_dir / "residents.md", residents)

    apartments = '''# Apartment — Модель квартиры

## Назначение

Объединение жителей, автомобилей и статусов согласования.

## Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `apartment_number` | str | Номер квартиры |
| `entrance` | str | Подъезд |
| `verification_status` | str | new, confirmed, deferred, conflict, in_progress |

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `display_name` | str | 105 (п. 1) |
| `residents_count` | int | Количество жителей |
| `vehicles_count` | int | Количество автомобилей |
| `has_residents` | bool | Есть ли жители |
| `has_vehicles` | bool | Есть ли автомобили |

## Методы

| Метод | Возвращает | Описание |
|-------|------------|----------|
| `get_by_number(apartment)` | `Apartment` | Получить по номеру |
| `get_all(limit)` | `List[Apartment]` | Все квартиры |
| `get_by_entrance(entrance)` | `List[Apartment]` | Квартиры подъезда |
| `format_card()` | `str` | Карточка для отображения |

## Пример

from core_new.domain.apartments import Apartment

apartment = Apartment.get_by_number("105")
print(apartment.format_card())
'''
    write_file(domain_dir / "apartments.md", apartments)

    payments = '''# Payment — Модель платежа

## Назначение

Управление финансовыми операциями.

## Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `amount` | float | Сумма |
| `currency` | str | Валюта (UAH) |
| `apartment_number` | str | Номер квартиры |
| `service_code` | str | Код услуги |
| `status` | str | pending, completed, failed, refunded |
| `payment_method` | str | cash, card, bank |

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `amount_display` | str | 150.00 UAH |
| `status_display` | str | Завершен |
| `service_display` | str | Парковка |
| `is_completed` | bool | Завершён ли |

## Методы

| Метод | Возвращает | Описание |
|-------|------------|----------|
| `get_by_id(id)` | `Payment` | Получить по ID |
| `get_by_apartment(apartment)` | `List[Payment]` | Платежи квартиры |
| `create(...)` | `tuple` | Создать платёж |
| `format_card()` | `str` | Карточка платежа |

## Пример

from core_new.domain.payments import Payment

payment = Payment.create(
    amount=150.00,
    apartment_number="105",
    service_code="PARKING_DAY",
    payment_method="cash"
)
'''
    write_file(domain_dir / "payments.md", payments)

    candidate = '''# VehicleCandidate — Кандидат в автомобили

## Назначение

Хранит информацию об автомобилях, которые ещё не подтверждены и не привязаны к квартире.

## Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int | Уникальный ID |
| `license_plate` | str | Номер автомобиля |
| `car_model` | str | Марка и модель |
| `apartment_number` | str | Номер квартиры (может быть NULL) |
| `status` | str | PENDING, RESOLVED, REJECTED, MERGED |
| `created_by` | int | Telegram ID создателя |
| `source` | str | cashier, telegram, tbot |

## Жизненный цикл

PENDING -> RESOLVED -> vehicle created in vehicles
PENDING -> REJECTED

## Методы

| Метод | Возвращает | Описание |
|-------|------------|----------|
| `create(plate, model, apartment, created_by)` | `VehicleCandidate` | Создать кандидата |
| `resolve(apartment_number)` | `tuple` | Подтвердить -> создать автомобиль |
| `reject(reason)` | `tuple` | Отклонить кандидата |

## Пример

from core_new.domain.vehicle_candidate import VehicleCandidate

candidate = VehicleCandidate.create(
    plate="AA9999XX",
    model="Tesla",
    apartment_number=None,
    created_by=12345
)

success, vehicle = candidate.resolve("105")
'''
    write_file(domain_dir / "vehicle_candidate.md", candidate)


def create_domain_readme() -> None:
    content = '''# Доменная модель OSBB

## Сущности

| Сущность | Файл | Описание |
|----------|------|----------|
| **Vehicle** | `vehicles.md` | Автомобиль. Тарифы, привязка к квартире. |
| **Resident** | `residents.md` | Житель. Telegram-пользователь, квартира, статус верификации. |
| **Apartment** | `apartments.md` | Квартира. Объединяет жителей и автомобили. |
| **Payment** | `payments.md` | Платёж. Сумма, услуга, статус. |
| **VehicleCandidate** | `vehicle_candidate.md` | Кандидат в автомобили. Ожидает подтверждения. |

## Связи

Resident (N) ---- (1) Apartment
Apartment (1) ---- (N) Vehicle
Apartment (1) ---- (N) Payment
Vehicle (1) ---- (N) Payment
VehicleCandidate ---- (1) Payment (временная связь)

## Жизненные циклы

| Сущность | Жизненный цикл |
|----------|----------------|
| **Vehicle** | кандидат -> создан -> активен -> архивирован |
| **Resident** | новый -> подтвердил квартиру -> проверен оператором |
| **Payment** | создан -> завершён / возвращён |
| **VehicleCandidate** | PENDING -> RESOLVED / REJECTED |

## Тестирование

python tests/test_vehicle.py
python tests/test_resident.py
python tests/test_apartment.py
python tests/test_payment.py
'''
    docs_dir = local_config.py_root / "OSBB" / "Docs" / "Domain"
    ensure_dir(docs_dir)
    write_file(docs_dir / "README.md", content)


def create_readme() -> None:
    content = '''# Документация проекта OSBB

## Разделы

| Раздел | Описание |
|--------|----------|
| [OSBB Project State.docx](OSBB%20Project%20State.docx) | Исторический документ |
| [ROADMAP.md](ROADMAP.md) | План развития |
| [Architecture/](Architecture/) | Архитектура и ADR |
| [Domain/](Domain/) | Доменная модель |
| [Code/](Code/) | Код core_new |
| [Guide/](Guide/) | Руководства |
| [Changelog/](Changelog/) | История изменений |
| [Database/](Database/) | Словарь данных |

## Последние обновления

- **2026-07-14**: Добавлена сущность vehicle_candidates. (ADR)
- **2026-07-14**: Создан полный словарь данных.
- **2026-07-13**: Реализовано новое ядро core_new.
'''
    docs_dir = local_config.py_root / "OSBB" / "Docs"
    ensure_dir(docs_dir)
    write_file(docs_dir / "README.md", content)


def main():
    print("=" * 70)
    print("📚 ГЕНЕРАЦИЯ ДОКУМЕНТАЦИИ OSBB")
    print("=" * 70)
    print(f"📁 Путь: {local_config.py_root / 'OSBB' / 'Docs'}")
    print("-" * 70)

    create_roadmap()
    create_changelog()
    create_adr_core_new_analysis()
    create_adr_vehicle_candidate()
    create_data_dictionary()
    create_domain_models()
    create_domain_readme()
    create_readme()

    print("-" * 70)
    print("✅ ВСЕ ДОКУМЕНТЫ СОЗДАНЫ!")
    print("📁 Откройте: OSBB/Docs/README.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
    