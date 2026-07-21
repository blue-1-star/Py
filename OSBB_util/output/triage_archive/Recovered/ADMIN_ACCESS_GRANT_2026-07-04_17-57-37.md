# Admin access grant report

Generated: `2026-07-04 17:57:37`
DB: `G:\Programming\Py\OSBB\Data\db\osbb_test.db`
Applied: `False`

## Request

```json
{
  "telegram_id": "",
  "name": "",
  "admin": false,
  "service_operator": false,
  "guard": false,
  "resident": false,
  "apartment": ""
}
```

## Actions

- No actions.

## Inventory

### user-like tables

- none

### role-like tables

- `access_user_roles`: id, telegram_user_id, role_code, scope_type, scope_value, is_active, valid_from, valid_to, granted_by, note, created_at, updated_at
- `bot_admins`: id, telegram_user_id, telegram_username, display_name, role, can_read, can_write, can_manage_users, can_manage_payments, can_manage_bot, is_active, created_at, updated_at, notes

### apartment-like tables

- `apartments`: id, apartment_number, entrance, entrance_source, total_area, object_type, status, source, notes, created_at, created_by, updated_at, updated_by, unit_type, unit_code, entrance_number, official_number, display_name, area_sqm, record_status, source_note, internal_note, unit_updated_at

