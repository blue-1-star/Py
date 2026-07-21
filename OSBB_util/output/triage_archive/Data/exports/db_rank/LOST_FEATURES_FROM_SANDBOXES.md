# OSBB Lost / Stronger Feature Harvest from Sandbox DBs

Generated: 2026-07-02 18:58:41

## Base DB

`G:\Programming\Py\OSBB\Data\db\osbb_test.db`

- OK: `True`
- Integrity: `ok`
- Tables: `104`
- Size: `1.98 MB`

## Executive summary

| Feature | Base score | Best sandbox score | Best DB | Candidates |
|---|---:|---:|---|---:|
| Remote/pult orders | 54 | 17 | `osbb_test_before_promote_live_services_2026-07-01_12-41-42.db` | 1 |
| Resident identity / binding / verification | 26 | 22 | `osbb_test_before_promote_live_services_2026-07-01_12-41-42.db` | 1 |

## Detailed findings

### Payments / cashbox / payment allocations

Base evidence:

- Score: **63**
- Tables: `payments, payment_allocations, cashbox_operations`
- Non-empty rows: `payments=96, payment_allocations=13, cashbox_operations=97`
- Columns: `payments(amount, apartment_id, created_at); payment_allocations(payment_id, amount); cashbox_operations(amount, operation_type, created_at)`
- Keyword hits: `bot_admins: payment, payments: payment, payment_allocations: payment, idx_payments_period: payment, idx_payments_apartment: payment, idx_payments_vehicle: payment, idx_payments_date: payment, cashboxes: cashbox`

No stronger sandbox candidate detected.

### Debts / accruals / empty accrual fields

Base evidence:

- Score: **26**
- Tables: `charges`
- Non-empty rows: `charges=95`
- Columns: `charges(amount)`
- Keyword hits: `charges: charge, payment_allocations: charge, idx_charges_period: charge, idx_charges_apartment: charge, idx_charges_vehicle: charge, idx_charges_service: charge, idx_charges_status: charge, cashbox_operations: charge`

No stronger sandbox candidate detected.

### Remote/pult orders

Base evidence:

- Score: **54**
- Tables: `remote_requests, remote_order_details, service_orders, service_order_steps`
- Non-empty rows: `remote_order_details=4, service_orders=6, service_order_steps=18`
- Columns: `remote_requests(status, apartment_id, created_at); service_orders(apartment_id)`
- Keyword hits: `remote_requests: remote, idx_remote_requests_resident: remote, idx_remote_requests_status: remote, idx_remote_requests_apartment: remote, remote_handover_events: remote, idx_remote_handover_post: remote, idx_remote_handover_operator: remote, idx_remote_handover_request: remote`

Stronger sandbox candidates:

#### `osbb_test_before_promote_live_services_2026-07-01_12-41-42.db`

- Path: `G:\Programming\Py\OSBB\Data\db\backups\osbb_test_before_promote_live_services_2026-07-01_12-41-42.db`
- Modified: `2026-06-30 22:51:07`
- Tables total: `53`
- Size: `1.27 MB`
- Score: **17**
- Tables: `remote_requests`
- Non-empty rows: `remote_requests=1`
- Columns: `remote_requests(status, apartment_id, created_at)`
- Keyword hits: `remote_requests: remote, idx_remote_requests_resident: remote, idx_remote_requests_status: remote, idx_remote_requests_apartment: remote`

### Phone barrier access

Base evidence:

- Score: **36**
- Tables: `phone_access_requests, phone_access_request_points, barrier_phone_access`
- Non-empty rows: `phone_access_requests=3, phone_access_request_points=6`
- Columns: `phone_access_requests(apartment_id, created_at)`
- Keyword hits: `barrier_phone_access: phone_access, idx_barrier_phone_access_apt: phone_access, idx_barrier_phone_access_phone: phone_access, idx_barrier_phone_access_status: phone_access, commercial_contract_items: phone_access, v_commercial_contract_charge_debt: phone_access, v_commercial_contract_debt_summary: phone_access, service_access_credentials: barrier`

No stronger sandbox candidate detected.

### Commercial / non-residential units and contracts

Base evidence:

- Score: **47**
- Tables: `commercial_contracts, unit_groups, unit_group_members, unit_aliases`
- Non-empty rows: `unit_groups=4, unit_group_members=8`
- Columns: `commercial_contracts(contract_number, unit_id, status); unit_groups(group_type); unit_group_members(apartment_id)`
- Keyword hits: `service_catalog: commercial, charges: commercial, payments: commercial, cashbox_operations: commercial, unit_groups: unit_group, unit_group_members: unit_group, unit_group_aliases: unit_group, idx_unit_groups_status: unit_group`

No stronger sandbox candidate detected.

### Resident identity / binding / verification

Base evidence:

- Score: **26**
- Tables: `resident_accounts, resident_profile_schema_migrations`
- Non-empty rows: `resident_accounts=1, resident_profile_schema_migrations=1`
- Columns: `resident_accounts(telegram_user_id, apartment_id, status, updated_at)`
- Keyword hits: `apartments: resident, verification_log: verified, resident_accounts: resident, idx_resident_accounts_telegram_user: resident, idx_resident_accounts_apartment: resident, idx_resident_accounts_status: resident, idx_resident_accounts_role: resident, apartment_verification: verified`

Stronger sandbox candidates:

#### `osbb_test_before_promote_live_services_2026-07-01_12-41-42.db`

- Path: `G:\Programming\Py\OSBB\Data\db\backups\osbb_test_before_promote_live_services_2026-07-01_12-41-42.db`
- Modified: `2026-06-30 22:51:07`
- Tables total: `53`
- Size: `1.27 MB`
- Score: **22**
- Tables: `resident_accounts`
- Non-empty rows: `resident_accounts=3`
- Columns: `resident_accounts(telegram_user_id, apartment_id, status, updated_at)`
- Keyword hits: `apartments: resident, verification_log: verified, resident_accounts: resident, idx_resident_accounts_telegram_user: resident, idx_resident_accounts_apartment: resident, idx_resident_accounts_status: resident, idx_resident_accounts_role: resident, apartment_verification: verified`

### Admin roles / audit / operator log

Base evidence:

- Score: **42**
- Tables: `bot_admins, operator_audit_log, audit_log`
- Non-empty rows: `bot_admins=2, operator_audit_log=153`
- Columns: `bot_admins(telegram_user_id, role, can_read, can_write); operator_audit_log(created_at)`
- Keyword hits: `audit_log: audit, bot_admins: admin, idx_bot_admins_telegram_user: admin, idx_bot_admins_active: admin, idx_bot_admins_role: admin, idx_audit_log_actor: audit, idx_audit_log_table_record: audit, idx_audit_log_event_time: audit`

No stronger sandbox candidate detected.

### Guard workspace / parking time / access control

Base evidence:

- Score: **10**
- Keyword hits: `vehicles: parking_time, parking_time_review_tasks: parking_time, idx_ptrt_status: parking_time, idx_ptrt_apartment: parking_time, resident_profile_change_requests: parking_time, profile_parking_time_test_schema_migrations: parking_time, profile_parking_time_test_sessions: parking_time, idx_profile_parking_time_test_sessions_queue: parking_time`

No stronger sandbox candidate detected.

### Reports / exports / operational views

Base evidence:

- Score: **0**

No stronger sandbox candidate detected.

## Recommended next steps

1. Do not merge databases automatically.
2. Pick one feature area at a time.
3. Open the strongest sandbox candidate for that feature.
4. Compare schema, rows, and bot code handlers.
5. Decide whether to port schema, seed data, UI logic, or only documentation.
6. Apply changes only through explicit migrations or patches.
