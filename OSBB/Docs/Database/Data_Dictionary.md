# Словарь данных OSBB (Data Dictionary)

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
