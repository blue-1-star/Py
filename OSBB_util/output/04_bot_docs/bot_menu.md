# 🤖 Структура меню Telegram-бота

**Файл:** `parking_bot.py`  
**Дата:** 2026-07-12 21:52:39

---

## 📋 Список меню

### `ADMIN_MENU`

```
Квартиры | Помещения
```

### `APARTMENT_MENU`

```
Жильцы | Авто
```

### `CONFIRM_APARTMENT_MENU`

```
Да это моя квартира
```

### `LANG_MENU`

```
Українська
```

### `USERS_MENU`

```
Все пользователи
```

### `USER_VERIFY_MENU`

```
Подтвердить пользователя
```

### `VEHICLE_ACTION_MENU`

```
Day
```

### `VEHICLE_EDIT_MENU`

```
Статус
```

### `VEHICLE_REVIEW_MENU`

```
Все автомобили
```

### `VEHICLE_STATUS_MENU`

```
Day | Night
```

## 📌 Состояния пользователя

```
admin_confirm_unlink_user
admin_confirm_verify_user
admin_waiting_apartment_lookup
admin_waiting_user_id_unlink
admin_waiting_user_id_verify
confirm_apartment
vehicle_card
vehicle_edit_model
vehicle_edit_plate
vehicle_edit_status
vehicle_review
vehicle_select_in_apartment
waiting_apartment
```

## 🎯 Обработчики

### `handle_admin_confirm_user_action`

### `handle_admin_waiting_user_id`

### `handle_confirm_apartment`

### `handle_vehicle_review_action`

### `handle_waiting_apartment`

