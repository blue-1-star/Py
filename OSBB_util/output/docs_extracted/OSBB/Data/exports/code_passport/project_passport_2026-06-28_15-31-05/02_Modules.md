# Python Modules

## `access_control.py`

- Lines: 400
- Functions: 17
- Classes: 0
- Imports: 8
- DB tables: __future__, access_audit_log, access_role_permissions, access_roles, access_user_permissions, access_user_roles, audit_log, audit_logger, config, datetime, operator_audit_log, pathlib, sqlite_master, typing
- TODO/FIXME: 0

## `audit_composite_apartments.py`

- Lines: 178
- Functions: 7
- Classes: 0
- Imports: 5
- DB tables: apartments, config, pathlib, tbot_parking_import
- TODO/FIXME: 0

## `audit_logger.py`

- Lines: 297
- Functions: 11
- Classes: 0
- Imports: 7
- DB tables: IF, audit_log, config, datetime, operator_audit_log, pathlib, sqlite_master
- TODO/FIXME: 0

## `audit_osbb_telegram_messages.py`

- Lines: 201
- Functions: 2
- Classes: 0
- Imports: 6
- DB tables: apartments, config, datetime, pathlib, telegram_chats, telegram_messages
- TODO/FIXME: 0

## `audit_registry.py`

- Lines: 256
- Functions: 6
- Classes: 1
- Imports: 5
- DB tables: PAPER, apartments, audit_log, config, contact_methods, datetime, in, not, pathlib, persons, vehicles
- TODO/FIXME: 0

## `audit_tbot_quarantine.py`

- Lines: 469
- Functions: 9
- Classes: 1
- Imports: 6
- DB tables: TBOT, apartments, config, datetime, error, pathlib, persons, source_files, tbot_parking_import, utils, vehicles
- TODO/FIXME: 0

## `billing/build_parking_time_review_tasks.py`

- Lines: 196
- Functions: 6
- Classes: 0
- Imports: 5
- DB tables: IF, apartments, config, datetime, parking_time_review_tasks, pathlib, vehicles
- TODO/FIXME: 0

## `billing/import_ohorona_parking_time.py`

- Lines: 435
- Functions: 11
- Classes: 0
- Imports: 9
- DB tables: apartments, collections, config, datetime, openpyxl, pathlib, vehicles
- TODO/FIXME: 0

## `billing/import_ohorona_parking_time_simple_preview.py`

- Lines: 472
- Functions: 13
- Classes: 0
- Imports: 9
- DB tables: apartments, collections, config, datetime, openpyxl, pathlib, vehicles
- TODO/FIXME: 0

## `billing/import_parking_time_hints_from_ohorona.py`

- Lines: 366
- Functions: 8
- Classes: 0
- Imports: 8
- DB tables: apartments, collections, config, datetime, openpyxl, pathlib, vehicles
- TODO/FIXME: 0

## `billing/migrate_add_parking_billing.py`

- Lines: 173
- Functions: 2
- Classes: 0
- Imports: 5
- DB tables: IF, apartments, billing_periods, cashboxes, charges, config, datetime, parking_charges, parking_tariffs, pathlib, payments, vehicles
- TODO/FIXME: 0

## `billing/report_missing_parking_time.py`

- Lines: 1
- Functions: 0
- Classes: 0
- Imports: 0
- DB tables: -
- TODO/FIXME: 0

## `billing/report_parking_time_review_tasks.py`

- Lines: 233
- Functions: 3
- Classes: 0
- Imports: 7
- DB tables: apartments, collections, config, datetime, parking_time_review_tasks, pathlib, telegram_facts, utils, vehicles
- TODO/FIXME: 0

## `billing/report_parking_time_with_hints.py`

- Lines: 494
- Functions: 11
- Classes: 0
- Imports: 8
- DB tables: apartments, collections, config, datetime, openpyxl, parking_time_review_tasks, pathlib, telegram_facts, vehicles
- TODO/FIXME: 0

## `billing_reconciliation_report.py`

- Lines: 396
- Functions: 18
- Classes: 0
- Imports: 6
- DB tables: charges, config, datetime, pathlib, payment_allocations, payments, sqlite_master, vehicles
- TODO/FIXME: 0

## `billing_statement_excel.py`

- Lines: 551
- Functions: 20
- Classes: 0
- Imports: 11
- DB tables: apartments, charges, collections, config, datetime, import, openpyxl, pathlib, payment_allocations, payments, sqlite_master, vehicles
- TODO/FIXME: 0

## `Bots/data_park_bot.py`

- Lines: 155
- Functions: 4
- Classes: 0
- Imports: 2
- DB tables: telegram
- TODO/FIXME: 0

## `Bots/db_access - Copy.py`

- Lines: 4914
- Functions: 147
- Classes: 0
- Imports: 6
- DB tables: Bots, SET, apartment_verification, apartments, audit_log, bot_admins, config, datetime, operator_audit_log, pathlib, payments, resident_accounts, sqlite_master, tbot_parking_import, telegram_facts, telegram_messages, vehicles
- TODO/FIXME: 0

## `Bots/db_access.py`

- Lines: 6012
- Functions: 174
- Classes: 0
- Imports: 7
- DB tables: Bots, SET, apartment_verification, apartments, audit_log, bot_admins, config, datetime, exc, from, operator_audit_log, pathlib, payments, resident_accounts, sqlite_master, tbot_parking_import, telegram_facts, telegram_messages, unit_group_aliases, unit_group_members, unit_groups, unit_resolver, vehicles
- TODO/FIXME: 0

## `Bots/handlers/__init___.py`

- Lines: 1
- Functions: 0
- Classes: 0
- Imports: 0
- DB tables: -
- TODO/FIXME: 0

## `Bots/handlers/agreement - Copy.py`

- Lines: 542
- Functions: 17
- Classes: 0
- Imports: 2
- DB tables: Bots, apartment_verification, apartments, telegram, vehicles
- TODO/FIXME: 0

## `Bots/handlers/agreement.py`

- Lines: 542
- Functions: 17
- Classes: 0
- Imports: 2
- DB tables: Bots, apartment_verification, apartments, telegram, vehicles
- TODO/FIXME: 0

## `Bots/handlers/audit_viewer - Copy.py`

- Lines: 231
- Functions: 13
- Classes: 0
- Imports: 5
- DB tables: audit_log, config, operator_audit_log, pathlib, sqlite_master, telegram
- TODO/FIXME: 0

## `Bots/handlers/audit_viewer.py`

- Lines: 366
- Functions: 15
- Classes: 0
- Imports: 7
- DB tables: __future__, audit_log, config, handlers, operator_audit_log, pathlib, sqlite_master, telegram, typing
- TODO/FIXME: 0

## `Bots/handlers/cashier_operator.py`

- Lines: 2427
- Functions: 61
- Classes: 0
- Imports: 13
- DB tables: __future__, apartments, audit_log, audit_logger, cashbox_operations, cashboxes, cashier_receipts, charges, config, datetime, db_access, exc, handlers, pathlib, payment_allocations, payments, sqlite_master, telegram, typing, unit_resolver, uuid
- TODO/FIXME: 0

## `Bots/handlers/cashier_operator_v2.py`

- Lines: 1098
- Functions: 29
- Classes: 0
- Imports: 7
- DB tables: __future__, cashier_v2_core, charges, handlers, pathlib, service_catalog, service_items, telegram, typing
- TODO/FIXME: 0

## `Bots/handlers/client_portal.py`

- Lines: 2184
- Functions: 60
- Classes: 0
- Imports: 10
- DB tables: __future__, apartment_link_requests, apartments, audit_log, audit_logger, charges, config, datetime, missing, pathlib, payment_allocations, payments, remote_requests, resident_accounts, sqlite_master, telegram, this, typing, vehicles
- TODO/FIXME: 0

## `Bots/handlers/client_portal_safe_linking.py`

- Lines: 2184
- Functions: 60
- Classes: 0
- Imports: 10
- DB tables: __future__, apartment_link_requests, apartments, audit_log, audit_logger, charges, config, datetime, missing, pathlib, payment_allocations, payments, remote_requests, resident_accounts, sqlite_master, telegram, this, typing, vehicles
- TODO/FIXME: 0

## `Bots/handlers/client_portal_v2.py`

- Lines: 666
- Functions: 19
- Classes: 0
- Imports: 7
- DB tables: __future__, cashier_v2_core, charges, handlers, old, pathlib, payments, telegram, the, typing
- TODO/FIXME: 0

## `Bots/handlers/client_portal_v3.py`

- Lines: 97
- Functions: 3
- Classes: 0
- Imports: 5
- DB tables: __future__, handlers, pathlib, service_orders
- TODO/FIXME: 0

## `Bots/handlers/commercial_contract_editor.py`

- Lines: 1582
- Functions: 55
- Classes: 0
- Imports: 12
- DB tables: __future__, apartments, audit_log, audit_logger, commercial, commercial_access_phones, commercial_contract_items, commercial_contract_recipients, commercial_contracts, commercial_notifications, config, datetime, exc, handlers, operator_audit_log, pathlib, resident_accounts, sqlite_master, telegram, typing, unit_registry_editor, v_commercial_contract_debt_summary
- TODO/FIXME: 0

## `Bots/handlers/guard_workspace.py`

- Lines: 1151
- Functions: 29
- Classes: 0
- Imports: 10
- DB tables: __future__, access_control, audit_log, cashbox_operations, cashier_receipts, cashier_v2_core, datetime, operator_audit_log, pathlib, payment_notices, payments, remote_handover_events, remote_requests, telegram, the, typing
- TODO/FIXME: 0

## `Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py`

- Lines: 1141
- Functions: 29
- Classes: 0
- Imports: 10
- DB tables: __future__, access_control, audit_log, cashbox_operations, cashier_receipts, cashier_v2_core, datetime, operator_audit_log, pathlib, payment_notices, payments, remote_handover_events, remote_requests, telegram, the, typing
- TODO/FIXME: 0

## `Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py`

- Lines: 1144
- Functions: 29
- Classes: 0
- Imports: 10
- DB tables: __future__, access_control, audit_log, cashbox_operations, cashier_receipts, cashier_v2_core, datetime, operator_audit_log, pathlib, payment_notices, payments, remote_handover_events, remote_requests, telegram, the, typing
- TODO/FIXME: 0

## `Bots/handlers/profile_parking_time_test_workspace.py`

- Lines: 365
- Functions: 9
- Classes: 0
- Imports: 7
- DB tables: __future__, pathlib, profile_parking_time_test_core, service_orders, service_orders_core, telegram, typing, vehicles
- TODO/FIXME: 0

## `Bots/handlers/profile_verification_workspace.py`

- Lines: 768
- Functions: 19
- Classes: 0
- Imports: 9
- DB tables: __future__, handlers, pathlib, profile_verification_core, service_orders, service_orders_core, telegram, the, typing, vehicles
- TODO/FIXME: 0

## `Bots/handlers/service_orders_workspace.py`

- Lines: 1743
- Functions: 58
- Classes: 0
- Imports: 17
- DB tables: __future__, access_control, both, cashier_v2_core, handlers, pathlib, phone_barrier_access_core, phone_barrier_access_service, possibly, profile, profile_verification_core, remote_order_details, service_item_workflows, service_items, service_order_steps, service_orders, service_orders_core, service_preorders_core, service_workflow_profiles, telegram, typing
- TODO/FIXME: 0

## `Bots/handlers/unit_registry_editor - Copy.py`

- Lines: 1036
- Functions: 35
- Classes: 0
- Imports: 14
- DB tables: Bots, __future__, apartments, audit_log, audit_logger, commercial_contract_editor, config, datetime, db_access, handlers, operator_audit_log, pathlib, sqlite_master, telegram, typing, unit_contacts
- TODO/FIXME: 0

## `Bots/handlers/unit_registry_editor.py`

- Lines: 1077
- Functions: 35
- Classes: 0
- Imports: 14
- DB tables: Bots, __future__, apartments, audit_log, audit_logger, commercial_contract_editor, config, datetime, db_access, handlers, operator_audit_log, pathlib, sqlite_master, telegram, typing, unit_contacts
- TODO/FIXME: 0

## `Bots/handlers/vehicle_card_editor.py`

- Lines: 595
- Functions: 23
- Classes: 0
- Imports: 7
- DB tables: apartments, audit_log, audit_logger, config, pathlib, telegram, vehicles
- TODO/FIXME: 0

## `Bots/handlers/vehicle_full_list.py`

- Lines: 127
- Functions: 8
- Classes: 0
- Imports: 5
- DB tables: apartments, config, pathlib, telegram, vehicles
- TODO/FIXME: 0

## `Bots/handlers/vehicle_verification.py`

- Lines: 519
- Functions: 28
- Classes: 0
- Imports: 8
- DB tables: apartments, audit_log, config, consensus, datetime, has, operator_audit_log, pathlib, payments, plate_consensus_report, sqlite_master, telegram, vehicles
- TODO/FIXME: 0

## `Bots/hello.py`

- Lines: 72
- Functions: 3
- Classes: 0
- Imports: 3
- DB tables: telegram
- TODO/FIXME: 0

## `Bots/parking_bot - Copy.py`

- Lines: 1301
- Functions: 27
- Classes: 0
- Imports: 12
- DB tables: Bots, apartments, config, handlers, pathlib, resident_accounts, telegram, telegram_osbb, vehicles
- TODO/FIXME: 0

## `Bots/parking_bot.py`

- Lines: 1359
- Functions: 27
- Classes: 0
- Imports: 15
- DB tables: Bots, apartments, config, handlers, pathlib, resident_accounts, telegram, telegram_osbb, vehicles
- TODO/FIXME: 0

## `Bots/parking_bot_before_cashier_editor_2026-06-25_14-45-08.py`

- Lines: 1343
- Functions: 27
- Classes: 0
- Imports: 14
- DB tables: Bots, apartments, config, handlers, pathlib, resident_accounts, telegram, telegram_osbb, vehicles
- TODO/FIXME: 0

## `Bots/parking_bot_before_client_portal_2026-06-25_10-25-49.py`

- Lines: 1310
- Functions: 27
- Classes: 0
- Imports: 13
- DB tables: Bots, apartments, config, handlers, pathlib, resident_accounts, telegram, telegram_osbb, vehicles
- TODO/FIXME: 0

## `Bots/parking_bot_before_language_gate_fix_2026-06-25_10-45-39.py`

- Lines: 1342
- Functions: 27
- Classes: 0
- Imports: 14
- DB tables: Bots, apartments, config, handlers, pathlib, resident_accounts, telegram, telegram_osbb, vehicles
- TODO/FIXME: 0

## `Bots/parking_bot_before_launch_queues_menu_2026-06-25_12-21-29.py`

- Lines: 1342
- Functions: 27
- Classes: 0
- Imports: 14
- DB tables: Bots, apartments, config, handlers, pathlib, resident_accounts, telegram, telegram_osbb, vehicles
- TODO/FIXME: 0

## `build_plate_candidates.py`

- Lines: 329
- Functions: 9
- Classes: 0
- Imports: 6
- DB tables: IF, collections, config, datetime, pathlib, verification_candidates, verification_evidence, verification_tasks
- TODO/FIXME: 0

## `build_plate_evidence_by_digits_and_apartment.py`

- Lines: 343
- Functions: 10
- Classes: 0
- Imports: 5
- DB tables: config, datetime, pathlib, tbot_parking_import, telegram_facts, verification_evidence, verification_tasks
- TODO/FIXME: 0

## `build_plate_evidence_from_telegram.py`

- Lines: 175
- Functions: 3
- Classes: 0
- Imports: 5
- DB tables: config, datetime, pathlib, telegram_facts, verification_evidence, verification_tasks
- TODO/FIXME: 0

## `build_verification_tasks.py`

- Lines: 231
- Functions: 6
- Classes: 0
- Imports: 5
- DB tables: apartments, config, datetime, pathlib, vehicles, verification_tasks
- TODO/FIXME: 0

## `cashier_journal.py`

- Lines: 1731
- Functions: 44
- Classes: 0
- Imports: 11
- DB tables: apartments, audit_log, audit_logger, cashbox_operations, cashboxes, charges, config, datetime, openpyxl, pathlib, payment_allocations, payments, service_catalog, service_items, sqlite_master, uuid, vehicles
- TODO/FIXME: 0

## `cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py`

- Lines: 708
- Functions: 17
- Classes: 0
- Imports: 16
- DB tables: __future__, access_role_permissions, access_user_roles, audit_log, datetime, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_order_interests, service_order_steps, service_orders, service_preorders_core, sqlite_master, telegram_osbb, the, types, typing
- TODO/FIXME: 0

## `cashier_v2_core.py`

- Lines: 1556
- Functions: 42
- Classes: 0
- Imports: 12
- DB tables: __future__, apartments, audit_log, audit_logger, bank_transactions, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, charges, config, datetime, exc, handlers, pathlib, payment_allocations, payment_notices, payments, repeated, resident_accounts, service_catalog, service_items, typing, unit_resolver, uuid, v1
- TODO/FIXME: 6

## `cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py`

- Lines: 1536
- Functions: 42
- Classes: 0
- Imports: 12
- DB tables: __future__, apartments, audit_log, audit_logger, bank_transactions, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, charges, config, datetime, exc, handlers, pathlib, payment_allocations, payment_notices, payments, repeated, resident_accounts, service_catalog, service_items, typing, unit_resolver, uuid, v1
- TODO/FIXME: 6

## `cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py`

- Lines: 1480
- Functions: 42
- Classes: 0
- Imports: 12
- DB tables: __future__, apartments, audit_log, audit_logger, bank_transactions, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, charges, config, datetime, exc, handlers, pathlib, payment_allocations, payment_notices, payments, repeated, resident_accounts, service_catalog, service_items, typing, unit_resolver, uuid, v1
- TODO/FIXME: 6

## `cashier_v2_preflight.py`

- Lines: 486
- Functions: 10
- Classes: 0
- Imports: 9
- DB tables: __future__, bank_transactions, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, charges, config, datetime, for, in, pathlib, payment_allocations, payment_notices, payments, service_catalog, sqlite_master, this, typing
- TODO/FIXME: 0

## `cashier_v2_preflight_compat.py`

- Lines: 317
- Functions: 8
- Classes: 0
- Imports: 8
- DB tables: __future__, bank_transactions, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, charges, config, datetime, pathlib, payment_allocations, payment_notices, payments, service_catalog, sqlite_master
- TODO/FIXME: 0

## `CHECK_guard_sandbox_service_orders.py`

- Lines: 493
- Functions: 17
- Classes: 0
- Imports: 9
- DB tables: G, PATCHED, __future__, audit_log, datetime, pathlib, payments, remote_assets, remote_handover_events, remote_order_details, remote_requests, service_order_steps, service_orders, sqlite_master, typing
- TODO/FIXME: 0

## `CHECK_guard_sandbox_service_orders_v2.py`

- Lines: 471
- Functions: 16
- Classes: 0
- Imports: 8
- DB tables: __future__, audit_log, datetime, in, pathlib, payments, remote_assets, remote_handover_events, remote_order_details, remote_requests, service_order_steps, service_orders, sqlite_master, typing
- TODO/FIXME: 0

## `CHECK_phone_barrier_access_operational_sandbox.py`

- Lines: 77
- Functions: 1
- Classes: 0
- Imports: 6
- DB tables: __future__, access_debt_warnings, access_schema_migrations, charges, for, in, pathlib, phone_access_requests, phone_access_subscription_charges, phone_access_subscription_points, phone_access_subscriptions, phone_barrier_access_core
- TODO/FIXME: 0

## `CHECK_phone_barrier_access_sandbox_schema.py`

- Lines: 129
- Functions: 1
- Classes: 0
- Imports: 5
- DB tables: __future__, access_debt_warnings, access_points, access_policy_values, access_policy_versions, access_tariff_versions, for, in, pathlib, phone_access_subscriptions, phone_barrier_access_core
- TODO/FIXME: 0

## `CHECK_profile_button_early_route_fix.py`

- Lines: 62
- Functions: 1
- Classes: 0
- Imports: 4
- DB tables: __future__, pathlib
- TODO/FIXME: 0

## `CHECK_profile_confirmation_ready_visibility_fix.py`

- Lines: 37
- Functions: 1
- Classes: 0
- Imports: 1
- DB tables: pathlib
- TODO/FIXME: 0

## `CHECK_profile_critical_codes_fix.py`

- Lines: 40
- Functions: 1
- Classes: 0
- Imports: 1
- DB tables: pathlib
- TODO/FIXME: 0

## `CHECK_profile_parking_time_test_sandbox.py`

- Lines: 97
- Functions: 1
- Classes: 0
- Imports: 5
- DB tables: __future__, pathlib, profile_parking_time_test_core, profile_parking_time_test_schema_migrations, profile_parking_time_test_sessions, vehicles
- TODO/FIXME: 0

## `CHECK_profile_test_candidate_apartment_40.py`

- Lines: 356
- Functions: 13
- Classes: 0
- Imports: 6
- DB tables: __future__, apartments, for, in, not, pathlib, sqlite_master, that, typing, vehicles
- TODO/FIXME: 0

## `CHECK_profile_verification_sandbox.py`

- Lines: 40
- Functions: 1
- Classes: 0
- Imports: 5
- DB tables: __future__, pathlib, profile_verification_core, resident_profile_change_requests, resident_profile_policy_values, resident_profile_policy_versions, resident_profile_schema_migrations, resident_profile_verifications, sqlite_master
- TODO/FIXME: 0

## `CHECK_profile_verification_terminology_v2.py`

- Lines: 57
- Functions: 1
- Classes: 0
- Imports: 1
- DB tables: data, pathlib, service_orders
- TODO/FIXME: 0

## `CHECK_service_code_compatibility_phone_v2.py`

- Lines: 122
- Functions: 2
- Classes: 0
- Imports: 3
- DB tables: __future__, pathlib, payments, service_items, service_order_interests, service_orders
- TODO/FIXME: 0

## `Collect_sheets.py`

- Lines: 143
- Functions: 1
- Classes: 0
- Imports: 2
- DB tables: -
- TODO/FIXME: 0

## `Collect_sheets1.py`

- Lines: 169
- Functions: 1
- Classes: 0
- Imports: 2
- DB tables: -
- TODO/FIXME: 0

## `Collect_word_tables.py`

- Lines: 105
- Functions: 1
- Classes: 0
- Imports: 4
- DB tables: docx, openpyxl
- TODO/FIXME: 0

## `commercial_contracts.py`

- Lines: 1312
- Functions: 33
- Classes: 1
- Imports: 11
- DB tables: __future__, apartments, audit_log, audit_logger, charges, commercial_access_actions, commercial_access_phones, commercial_contract_items, commercial_contract_recipients, commercial_contracts, commercial_notifications, config, dataclasses, datetime, pathlib, payment_allocations, sqlite_master, typing, v_commercial_contract_charge_debt
- TODO/FIXME: 0

## `commercial_notification_delivery.py`

- Lines: 256
- Functions: 8
- Classes: 0
- Imports: 9
- DB tables: __future__, apartments, audit_log, audit_logger, commercial_contracts, commercial_notification_delivery, commercial_notifications, config, datetime, pathlib, typing
- TODO/FIXME: 0

## `create_clean_live_sandbox.py`

- Lines: 460
- Functions: 10
- Classes: 0
- Imports: 12
- DB tables: SET, __future__, access_user_roles, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, datetime, pathlib, payment_notices, payments, remote_assets, remote_handover_events, service_orders, sqlite_master, staff_principals, types, typing
- TODO/FIXME: 0

## `create_isolated_live_sandbox_v2.py`

- Lines: 458
- Functions: 10
- Classes: 0
- Imports: 12
- DB tables: SET, __future__, access_user_roles, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, datetime, osbb_test, pathlib, payment_notices, payments, remote_assets, remote_handover_events, service_orders, sqlite_master, staff_principals, types, typing
- TODO/FIXME: 0

## `CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.py`

- Lines: 175
- Functions: 4
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib, payments, service_orders
- TODO/FIXME: 0

## `Data/audit_databases.py`

- Lines: 68
- Functions: 3
- Classes: 0
- Imports: 4
- DB tables: datetime
- TODO/FIXME: 0

## `Data/Audit_for_merge.py`

- Lines: 39
- Functions: 3
- Classes: 0
- Imports: 3
- DB tables: -
- TODO/FIXME: 0

## `Data/backups/source_code/cashier_route_repair_2026-06-27_20-04-49/run_bot_live_services_sandbox_v1.py`

- Lines: 705
- Functions: 17
- Classes: 0
- Imports: 16
- DB tables: __future__, access_role_permissions, access_user_roles, audit_log, datetime, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_order_interests, service_order_steps, service_orders, service_preorders_core, sqlite_master, telegram_osbb, the, types, typing
- TODO/FIXME: 0

## `Data/backups/source_code/parking_time_test_v1_2026-06-28_12-12-01/run_bot_live_services_sandbox_v1.py`

- Lines: 865
- Functions: 18
- Classes: 0
- Imports: 16
- DB tables: __future__, access_role_permissions, access_user_roles, audit_log, datetime, handlers, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_order_interests, service_order_steps, service_orders, service_preorders_core, sqlite_master, telegram_osbb, the, types, typing
- TODO/FIXME: 0

## `Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/Bots/handlers/service_orders_workspace.py`

- Lines: 1406
- Functions: 50
- Classes: 0
- Imports: 14
- DB tables: __future__, access_control, cashier_v2_core, handlers, pathlib, possibly, remote_order_details, service_item_workflows, service_items, service_order_steps, service_orders, service_orders_core, service_preorders_core, service_workflow_profiles, telegram, typing
- TODO/FIXME: 0

## `Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/phone_barrier_access_core.py`

- Lines: 1018
- Functions: 21
- Classes: 0
- Imports: 6
- DB tables: IF, __future__, access_operation_journal, access_points, access_policy_values, access_policy_versions, access_schema_migrations, access_tariff_versions, charges, datetime, in, payments, sqlite_master, typing
- TODO/FIXME: 0

## `Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/service_orders_core.py`

- Lines: 1374
- Functions: 32
- Classes: 0
- Imports: 9
- DB tables: __future__, access_control, audit_log, audit_logger, charges, config, datetime, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_access_credentials, service_item_workflows, service_items, service_order_charge_links, service_order_events, service_order_payment_links, service_order_steps, service_orders, service_price_versions, service_workflow_profiles, service_workflow_steps, sqlite_master, typing
- TODO/FIXME: 0

## `Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/service_preorders_core.py`

- Lines: 1096
- Functions: 24
- Classes: 0
- Imports: 5
- DB tables: IF, __future__, a, datetime, payment_notices, payments, remote_assets, remote_order_issued_assets, remote_supplier_batch_links, remote_supplier_batches, service_item_workflows, service_items, service_order_interests, service_order_payment_links, service_order_steps, service_orders, service_orders_core, service_workflow_profiles, service_workflow_steps, supplier, the, typing
- TODO/FIXME: 0

## `Data/backups/source_code/profile_button_early_route_2026-06-27_21-33-50/run_bot_live_services_sandbox_v1.py`

- Lines: 831
- Functions: 18
- Classes: 0
- Imports: 16
- DB tables: __future__, access_role_permissions, access_user_roles, audit_log, datetime, handlers, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_order_interests, service_order_steps, service_orders, service_preorders_core, sqlite_master, telegram_osbb, the, types, typing
- TODO/FIXME: 0

## `Data/backups/source_code/profile_confirmation_ready_visibility_2026-06-27_21-55-54/profile_verification_workspace.py`

- Lines: 765
- Functions: 19
- Classes: 0
- Imports: 9
- DB tables: __future__, handlers, pathlib, profile_verification_core, service_orders, service_orders_core, telegram, the, typing, vehicles
- TODO/FIXME: 0

## `Data/backups/source_code/profile_critical_codes_fix_2026-06-27_21-47-24/profile_verification_workspace.py`

- Lines: 760
- Functions: 19
- Classes: 0
- Imports: 9
- DB tables: __future__, handlers, pathlib, profile_verification_core, service_orders, service_orders_core, telegram, the, typing, vehicles
- TODO/FIXME: 0

## `Data/backups/source_code/profile_verification_2026-06-27_20-51-33/Bots/handlers/service_orders_workspace.py`

- Lines: 1632
- Functions: 55
- Classes: 0
- Imports: 16
- DB tables: __future__, access_control, both, cashier_v2_core, handlers, pathlib, phone_barrier_access_core, phone_barrier_access_service, possibly, remote_order_details, service_item_workflows, service_items, service_order_steps, service_orders, service_orders_core, service_preorders_core, service_workflow_profiles, telegram, typing
- TODO/FIXME: 0

## `Data/backups/source_code/profile_verification_2026-06-27_20-51-33/run_bot_live_services_sandbox_v1.py`

- Lines: 708
- Functions: 17
- Classes: 0
- Imports: 16
- DB tables: __future__, access_role_permissions, access_user_roles, audit_log, datetime, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_order_interests, service_order_steps, service_orders, service_preorders_core, sqlite_master, telegram_osbb, the, types, typing
- TODO/FIXME: 0

## `Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/Bots/handlers/profile_verification_workspace.py`

- Lines: 714
- Functions: 18
- Classes: 0
- Imports: 9
- DB tables: __future__, handlers, pathlib, profile_verification_core, service_orders, service_orders_core, telegram, the, typing, vehicles
- TODO/FIXME: 0

## `Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/Bots/handlers/service_orders_workspace.py`

- Lines: 1736
- Functions: 58
- Classes: 0
- Imports: 17
- DB tables: __future__, access_control, both, cashier_v2_core, handlers, pathlib, phone_barrier_access_core, phone_barrier_access_service, possibly, profile, profile_verification_core, remote_order_details, service_item_workflows, service_items, service_order_steps, service_orders, service_orders_core, service_preorders_core, service_workflow_profiles, telegram, typing
- TODO/FIXME: 0

## `Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/profile_verification_core.py`

- Lines: 1531
- Functions: 39
- Classes: 0
- Imports: 6
- DB tables: IF, __future__, contact, datetime, primary, resident, resident_profile_change_requests, resident_profile_operation_journal, resident_profile_policy_values, resident_profile_policy_versions, resident_profile_schema_migrations, resident_profile_verifications, sqlite_master, typing, vehicles
- TODO/FIXME: 0

## `Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/Bots/handlers/service_orders_workspace.py`

- Lines: 1614
- Functions: 55
- Classes: 0
- Imports: 16
- DB tables: __future__, access_control, cashier_v2_core, handlers, pathlib, phone_barrier_access_core, phone_barrier_access_service, possibly, remote_order_details, service_item_workflows, service_items, service_order_steps, service_orders, service_orders_core, service_preorders_core, service_workflow_profiles, telegram, typing
- TODO/FIXME: 0

## `Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/service_orders_core.py`

- Lines: 1338
- Functions: 31
- Classes: 0
- Imports: 9
- DB tables: __future__, access_control, audit_log, audit_logger, charges, config, datetime, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_access_credentials, service_item_workflows, service_items, service_order_charge_links, service_order_events, service_order_payment_links, service_order_steps, service_orders, service_price_versions, service_workflow_profiles, service_workflow_steps, sqlite_master, typing
- TODO/FIXME: 0

## `Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/service_preorders_core.py`

- Lines: 1147
- Functions: 24
- Classes: 0
- Imports: 6
- DB tables: IF, __future__, a, datetime, payment_notices, payments, phone_barrier_access_service, remote_assets, remote_order_issued_assets, remote_supplier_batch_links, remote_supplier_batches, service_item_workflows, service_items, service_order_interests, service_order_payment_links, service_order_steps, service_orders, service_orders_core, service_workflow_profiles, service_workflow_steps, supplier, the, typing
- TODO/FIXME: 0

## `Data/car_registry.py`

- Lines: 54
- Functions: 1
- Classes: 0
- Imports: 2
- DB tables: -
- TODO/FIXME: 0

## `Data/check_passport_columns.py`

- Lines: 37
- Functions: 1
- Classes: 0
- Imports: 2
- DB tables: -
- TODO/FIXME: 0

## `Data/Clean_Base.py`

- Lines: 36
- Functions: 2
- Classes: 0
- Imports: 2
- DB tables: -
- TODO/FIXME: 0

## `Data/clean_base_01.py`

- Lines: 55
- Functions: 2
- Classes: 0
- Imports: 4
- DB tables: datetime
- TODO/FIXME: 0

## `Data/clean_base_02.py`

- Lines: 44
- Functions: 2
- Classes: 0
- Imports: 3
- DB tables: datetime
- TODO/FIXME: 0

## `Data/Clean_Data.py`

- Lines: 276
- Functions: 5
- Classes: 0
- Imports: 3
- DB tables: -
- TODO/FIXME: 0

## `Data/conflicts.py`

- Lines: 39
- Functions: 3
- Classes: 0
- Imports: 3
- DB tables: -
- TODO/FIXME: 0

## `Data/create_payment_sheet.py`

- Lines: 62
- Functions: 1
- Classes: 0
- Imports: 5
- DB tables: openpyxl
- TODO/FIXME: 0

## `Data/debug_conflict.py`

- Lines: 65
- Functions: 3
- Classes: 0
- Imports: 3
- DB tables: -
- TODO/FIXME: 0

## `Data/final_merge.py`

- Lines: 68
- Functions: 3
- Classes: 0
- Imports: 3
- DB tables: -
- TODO/FIXME: 0

## `Data/merge_all.py`

- Lines: 71
- Functions: 3
- Classes: 0
- Imports: 3
- DB tables: -
- TODO/FIXME: 0

## `Data/rub_flat_merge.py`

- Lines: 54
- Functions: 3
- Classes: 0
- Imports: 2
- DB tables: -
- TODO/FIXME: 0

## `Data/run_direct_merge.py`

- Lines: 82
- Functions: 4
- Classes: 0
- Imports: 3
- DB tables: -
- TODO/FIXME: 0

## `Data/run_flat_merge.py`

- Lines: 64
- Functions: 3
- Classes: 0
- Imports: 2
- DB tables: -
- TODO/FIXME: 0

## `Data/run_smart_merge.py`

- Lines: 64
- Functions: 3
- Classes: 0
- Imports: 2
- DB tables: -
- TODO/FIXME: 0

## `diagnose_osbb_audit.py`

- Lines: 333
- Functions: 5
- Classes: 0
- Imports: 8
- DB tables: __future__, apartments, audit_log, datetime, operator_audit_log, pathlib, sqlite_master
- TODO/FIXME: 0

## `diagnose_sandbox_charges.py`

- Lines: 207
- Functions: 4
- Classes: 0
- Imports: 4
- DB tables: __future__, apartments, charges, in, pathlib, payment_allocations, service_catalog, service_items, sqlite_master
- TODO/FIXME: 0

## `extract_telegram_remote_facts.py`

- Lines: 270
- Functions: 6
- Classes: 0
- Imports: 7
- DB tables: apartments, config, datetime, pathlib, telegram_chats, telegram_facts, telegram_messages, utils
- TODO/FIXME: 0

## `extract_telegram_vehicle_facts.py`

- Lines: 415
- Functions: 13
- Classes: 0
- Imports: 7
- DB tables: apartments, config, datetime, pathlib, telegram_chats, telegram_facts, telegram_messages, utils
- TODO/FIXME: 0

## `FIND_actual_service_order_state.py`

- Lines: 436
- Functions: 18
- Classes: 0
- Imports: 8
- DB tables: __future__, another, datetime, pathlib, payments, remote_order_details, remote_requests, service_order_steps, service_orders, sqlite_master, typing
- TODO/FIXME: 0

## `find_sandbox_telegram_id.py`

- Lines: 149
- Functions: 4
- Classes: 0
- Imports: 4
- DB tables: __future__, apartments, pathlib, resident_accounts, sqlite_master
- TODO/FIXME: 0

## `FIX_live_services_sandbox_payment_schema.py`

- Lines: 348
- Functions: 11
- Classes: 0
- Imports: 7
- DB tables: __future__, apartment_number, apartments, datetime, pathlib, payments, service_orders, sqlite_master
- TODO/FIXME: 0

## `fix_parking_bot_language_gate.py`

- Lines: 143
- Functions: 4
- Classes: 0
- Imports: 6
- DB tables: __future__, datetime, pathlib
- TODO/FIXME: 0

## `fix_source_ref_schema.py`

- Lines: 310
- Functions: 14
- Classes: 0
- Imports: 8
- DB tables: __future__, aliased, but, candidate, datetime, name, names, not, pathlib, payments, service_orders, sqlite_master, the, there, typing
- TODO/FIXME: 0

## `generate_parking_charges.py`

- Lines: 492
- Functions: 15
- Classes: 0
- Imports: 6
- DB tables: apartments, charges, config, datetime, pathlib, service_tariffs, vehicles
- TODO/FIXME: 0

## `Generate_Stetement.py`

- Lines: 77
- Functions: 0
- Classes: 0
- Imports: 0
- DB tables: -
- TODO/FIXME: 0

## `guard_workspace_preflight.py`

- Lines: 337
- Functions: 7
- Classes: 0
- Imports: 12
- DB tables: SET, __future__, access_user_roles, audit_log, bank_transactions, cashbox_operations, cashier_receipts, datetime, pathlib, payment_notices, remote_handover_events, remote_requests, sqlite_master, staff_principals, types
- TODO/FIXME: 0

## `guard_workspace_preflight_v2.py`

- Lines: 337
- Functions: 7
- Classes: 0
- Imports: 12
- DB tables: SET, __future__, access_user_roles, audit_log, bank_transactions, cashbox_operations, cashier_receipts, datetime, pathlib, payment_notices, remote_handover_events, remote_requests, sqlite_master, staff_principals, types
- TODO/FIXME: 0

## `import_house_registry.py`

- Lines: 166
- Functions: 4
- Classes: 0
- Imports: 6
- DB tables: apartments, config, datetime, pathlib, persons
- TODO/FIXME: 0

## `import_ohorona_list1_to_central_cashbox.py`

- Lines: 909
- Functions: 23
- Classes: 0
- Imports: 15
- DB tables: __future__, audit_log, audit_logger, calendar, cashboxes, cashier_journal, charges, config, datetime, decimal, pathlib, payments, service_catalog
- TODO/FIXME: 0

## `import_ohorona_sheet1_payments.py`

- Lines: 800
- Functions: 29
- Classes: 0
- Imports: 9
- DB tables: OHORONA, Sheet1, apartments, charges, config, datetime, decimal, openpyxl, pathlib, payment_allocations, payments, sqlite_master, vehicles
- TODO/FIXME: 0

## `import_ohorona_to_cashbox.py`

- Lines: 977
- Functions: 23
- Classes: 0
- Imports: 11
- DB tables: audit_log, audit_logger, cashbox_operations, cashboxes, cashier_journal, config, datetime, decimal, openpyxl, pathlib, payments, service_catalog
- TODO/FIXME: 0

## `import_osbb_telegram_messages.py`

- Lines: 233
- Functions: 5
- Classes: 0
- Imports: 10
- DB tables: config, datetime, pathlib, telegram_chats, telegram_messages, telegram_osbb, telethon
- TODO/FIXME: 0

## `import_paper_parking.py`

- Lines: 324
- Functions: 8
- Classes: 0
- Imports: 6
- DB tables: apartments, config, datetime, pathlib, persons, vehicles
- TODO/FIXME: 0

## `import_tbot_quarantine.py`

- Lines: 150
- Functions: 3
- Classes: 0
- Imports: 7
- DB tables: config, datetime, pathlib, source_files, tbot_parking_import, utils
- TODO/FIXME: 0

## `init_osbb_db.py`

- Lines: 226
- Functions: 2
- Classes: 0
- Imports: 5
- DB tables: IF, apartments, audit_log, config, contact_methods, datetime, message_sources, pathlib, persons, raw_messages, schema_info, vehicles
- TODO/FIXME: 0

## `init_osbb_quarantine_db.py`

- Lines: 71
- Functions: 2
- Classes: 0
- Imports: 5
- DB tables: IF, config, datetime, pathlib
- TODO/FIXME: 0

## `init_osbb_telegram_db.py`

- Lines: 133
- Functions: 2
- Classes: 0
- Imports: 5
- DB tables: IF, config, datetime, pathlib, telegram_chats, telegram_messages
- TODO/FIXME: 0

## `inspect_osbb_folder_filter.py`

- Lines: 56
- Functions: 1
- Classes: 0
- Imports: 7
- DB tables: config, pathlib, telegram_osbb, telethon
- TODO/FIXME: 0

## `INSTALL_cashier_route_after_phone_v2.py`

- Lines: 101
- Functions: 1
- Classes: 0
- Imports: 7
- DB tables: __future__, datetime, pathlib, service_orders
- TODO/FIXME: 0

## `INSTALL_PHONE_ACCESS_UI_FIX_v2.py`

- Lines: 143
- Functions: 3
- Classes: 0
- Imports: 10
- DB tables: __future__, datetime, exc, pathlib, service_orders
- TODO/FIXME: 0

## `INSTALL_PHONE_ACCESS_UI_FIX_v3.py`

- Lines: 111
- Functions: 3
- Classes: 0
- Imports: 9
- DB tables: __future__, datetime, exc, pathlib, service_orders
- TODO/FIXME: 0

## `INSTALL_phone_barrier_access_v2.py`

- Lines: 139
- Functions: 3
- Classes: 0
- Imports: 7
- DB tables: __future__, datetime, pathlib, service_orders
- TODO/FIXME: 0

## `INSTALL_profile_button_early_route_fix.py`

- Lines: 78
- Functions: 1
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib
- TODO/FIXME: 0

## `INSTALL_profile_confirmation_ready_visibility_fix.py`

- Lines: 76
- Functions: 1
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib, payments, vehicles
- TODO/FIXME: 0

## `INSTALL_profile_critical_codes_fix.py`

- Lines: 76
- Functions: 1
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib
- TODO/FIXME: 0

## `INSTALL_profile_parking_time_test_v1.py`

- Lines: 125
- Functions: 3
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib
- TODO/FIXME: 0

## `INSTALL_profile_verification_terminology_v2.py`

- Lines: 123
- Functions: 3
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib, payments, service_orders, vehicles
- TODO/FIXME: 0

## `INSTALL_profile_verification_v1.py`

- Lines: 52
- Functions: 2
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib, service_orders
- TODO/FIXME: 0

## `INSTALL_service_code_compatibility_phone_v2.py`

- Lines: 101
- Functions: 2
- Classes: 0
- Imports: 6
- DB tables: __future__, a, datetime, pathlib, payments, service_orders
- TODO/FIXME: 0

## `install_service_orders_ui.py`

- Lines: 136
- Functions: 5
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib, payments, service_order_payment_links, service_order_steps, service_orders, service_workflow_profiles, v3
- TODO/FIXME: 0

## `list_osbb_folder_dialogs.py`

- Lines: 106
- Functions: 3
- Classes: 0
- Imports: 8
- DB tables: config, datetime, pathlib, telegram_osbb, telethon
- TODO/FIXME: 0

## `list_osbb_included_peers.py`

- Lines: 154
- Functions: 4
- Classes: 0
- Imports: 9
- DB tables: config, datetime, pathlib, telegram_osbb, telethon
- TODO/FIXME: 0

## `list_telegram_dialogs.py`

- Lines: 113
- Functions: 3
- Classes: 0
- Imports: 8
- DB tables: config, datetime, pathlib, telegram_osbb, telethon
- TODO/FIXME: 0

## `list_telegram_folders.py`

- Lines: 60
- Functions: 1
- Classes: 0
- Imports: 7
- DB tables: config, pathlib, telegram_osbb, telethon
- TODO/FIXME: 0

## `manage_staff_access.py`

- Lines: 450
- Functions: 9
- Classes: 0
- Imports: 10
- DB tables: SET, __future__, access_audit_log, access_control, access_role_permissions, access_roles, access_user_permissions, access_user_roles, audit_log, audit_logger, cashier_receipts, config, datetime, pathlib, payment_notices, remote_handover_events, remote_requests, staff_principals, typing
- TODO/FIXME: 0

## `manage_staff_access_v2.py`

- Lines: 450
- Functions: 9
- Classes: 0
- Imports: 10
- DB tables: SET, __future__, access_audit_log, access_control, access_role_permissions, access_roles, access_user_permissions, access_user_roles, audit_log, audit_logger, cashier_receipts, config, datetime, pathlib, payment_notices, remote_handover_events, remote_requests, staff_principals, typing
- TODO/FIXME: 0

## `mark_audit_enabled.py`

- Lines: 9
- Functions: 0
- Classes: 0
- Imports: 1
- DB tables: audit_log, audit_logger, operator_audit_log
- TODO/FIXME: 0

## `migrate_access_control_and_guard.py`

- Lines: 557
- Functions: 13
- Classes: 0
- Imports: 9
- DB tables: IF, SET, __future__, access_role_permissions, access_roles, audit_log, audit_logger, cashbox_operations, cashier_batches, cashier_receipts, config, datetime, missing, pathlib, payment_notices, remote_handover_events, remote_requests, sqlite_master, typing
- TODO/FIXME: 0

## `migrate_add_normalized_fields.py`

- Lines: 65
- Functions: 3
- Classes: 0
- Imports: 4
- DB tables: config, pathlib, vehicles
- TODO/FIXME: 0

## `migrate_add_verification_evidence.py`

- Lines: 53
- Functions: 1
- Classes: 0
- Imports: 4
- DB tables: IF, config, created, pathlib, verification_evidence, verification_tasks
- TODO/FIXME: 0

## `migrate_add_verification_tasks.py`

- Lines: 83
- Functions: 1
- Classes: 0
- Imports: 4
- DB tables: IF, apartments, config, created, pathlib, verification_tasks
- TODO/FIXME: 0

## `migrate_apartment_link_requests.py`

- Lines: 203
- Functions: 5
- Classes: 0
- Imports: 8
- DB tables: IF, __future__, apartments, audit_log, audit_logger, config, datetime, existed, operator_audit_log, pathlib, resident_accounts, sqlite_master
- TODO/FIXME: 0

## `migrate_apartment_verification.py`

- Lines: 109
- Functions: 3
- Classes: 0
- Imports: 5
- DB tables: IF, apartment_verification, apartments, config, datetime, pathlib
- TODO/FIXME: 0

## `migrate_billing_core.py`

- Lines: 199
- Functions: 2
- Classes: 0
- Imports: 4
- DB tables: IF, charges, config, pathlib, payment_allocations, payments, service_catalog, service_tariffs, vehicles
- TODO/FIXME: 0

## `migrate_bot_core.py`

- Lines: 366
- Functions: 4
- Classes: 0
- Imports: 5
- DB tables: IF, apartments, audit_log, bot, config, datetime, in, pathlib, payments, resident_accounts
- TODO/FIXME: 0

## `migrate_cashier_core.py`

- Lines: 341
- Functions: 15
- Classes: 0
- Imports: 6
- DB tables: IF, audit_log, cashbox_operations, cashboxes, cashier_batches, charges, config, datetime, operator_audit_log, pathlib, payments, sqlite_master, vehicles
- TODO/FIXME: 0

## `migrate_cashier_operator_editor.py`

- Lines: 558
- Functions: 14
- Classes: 0
- Imports: 8
- DB tables: IF, __future__, audit_log, audit_logger, cashbox_operations, cashboxes, cashier_receipts, config, datetime, pathlib, payments, sqlite_master
- TODO/FIXME: 0

## `migrate_cashier_v2.py`

- Lines: 513
- Functions: 15
- Classes: 0
- Imports: 8
- DB tables: IF, __future__, apartments, audit_log, audit_logger, bank_transactions, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, charges, config, datetime, for, in, missing, pathlib, payment_notices, payments, resident_accounts, service_catalog, sqlite_master
- TODO/FIXME: 0

## `migrate_cashier_v2_compat.py`

- Lines: 684
- Functions: 19
- Classes: 0
- Imports: 9
- DB tables: IF, __future__, audit_log, audit_logger, bank_transactions, cashbox_operations, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, config, datetime, missing, pathlib, payment_notices, payments, sqlite_master, typing, will
- TODO/FIXME: 0

## `migrate_charge_adjustments.py`

- Lines: 405
- Functions: 15
- Classes: 0
- Imports: 7
- DB tables: IF, adjustment_assignments, adjustment_catalog, audit_log, audit_logger, charges, config, datetime, pathlib, sqlite_master
- TODO/FIXME: 0

## `migrate_commercial_contract_core.py`

- Lines: 936
- Functions: 19
- Classes: 0
- Imports: 9
- DB tables: IF, __future__, apartments, audit_log, audit_logger, cashbox_operations, charges, commercial_access_phones, commercial_contract_items, commercial_contract_recipients, commercial_contracts, commercial_notifications, config, datetime, pathlib, payment_allocations, payments, resident_accounts, service_catalog, service_tariffs, sqlite_master, typing, v_commercial_contract_charge_debt
- TODO/FIXME: 0

## `migrate_operator_audit_log.py`

- Lines: 103
- Functions: 2
- Classes: 0
- Imports: 4
- DB tables: IF, audit_log, config, operator_audit_log, pathlib
- TODO/FIXME: 0

## `migrate_operator_audit_log_v2.py`

- Lines: 188
- Functions: 6
- Classes: 0
- Imports: 4
- DB tables: IF, audit_log, config, operator_audit_log, pathlib, sqlite_master
- TODO/FIXME: 0

## `MIGRATE_phone_barrier_access_operational_sandbox.py`

- Lines: 151
- Functions: 2
- Classes: 0
- Imports: 9
- DB tables: __future__, access_schema_migrations, datetime, in, pathlib, phone_barrier_access_core, service_order_interests, service_orders
- TODO/FIXME: 0

## `MIGRATE_phone_barrier_access_sandbox.py`

- Lines: 152
- Functions: 3
- Classes: 0
- Imports: 9
- DB tables: __future__, datetime, pathlib, payments, phone_barrier_access_core, service_order_interests, service_orders
- TODO/FIXME: 0

## `MIGRATE_profile_parking_time_test_sandbox.py`

- Lines: 110
- Functions: 1
- Classes: 0
- Imports: 8
- DB tables: __future__, apartments, datetime, pathlib, profile_parking_time_test_core, sqlite_master, vehicles
- TODO/FIXME: 0

## `MIGRATE_profile_verification_sandbox.py`

- Lines: 63
- Functions: 1
- Classes: 0
- Imports: 8
- DB tables: __future__, datetime, pathlib, profile_verification_core, resident_accounts, sqlite_master, vehicles
- TODO/FIXME: 0

## `migrate_remote_requests.py`

- Lines: 238
- Functions: 6
- Classes: 0
- Imports: 8
- DB tables: IF, __future__, apartments, audit_log, audit_logger, config, datetime, existed, operator_audit_log, pathlib, remote_requests, resident_accounts, sqlite_master
- TODO/FIXME: 0

## `migrate_service_items.py`

- Lines: 463
- Functions: 20
- Classes: 0
- Imports: 7
- DB tables: IF, audit_log, audit_logger, barrier_phone_access, cashbox_operations, charges, config, datetime, in, pathlib, payment_allocations, payments, service_catalog, service_items, sqlite_master
- TODO/FIXME: 0

## `migrate_service_orders_and_fulfillment.py`

- Lines: 770
- Functions: 15
- Classes: 0
- Imports: 9
- DB tables: IF, SET, __future__, access_role_permissions, access_roles, audit_log, audit_logger, barrier_phone_access, config, datetime, pathlib, remote_asset_movements, remote_assets, remote_handover_events, remote_order_details, remote_requests, service_catalog, service_item_workflows, service_items, service_order_steps, service_orders, service_workflow_profiles, service_workflow_steps, sqlite_master, typing
- TODO/FIXME: 0

## `MIGRATE_simplified_services_sandbox.py`

- Lines: 147
- Functions: 4
- Classes: 0
- Imports: 9
- DB tables: G, OSBB, __future__, datetime, exc, pathlib, service_orders, service_preorders_core, the
- TODO/FIXME: 0

## `migrate_unit_registry_composite_groups.py`

- Lines: 786
- Functions: 24
- Classes: 0
- Imports: 10
- DB tables: IF, __future__, apartments, audit_log, audit_logger, collections, config, datetime, pathlib, payments, sqlite_master, tbot_parking_import, unit_group_aliases, unit_group_members, unit_groups, vehicles
- TODO/FIXME: 0

## `normalize_registry_fields.py`

- Lines: 207
- Functions: 8
- Classes: 1
- Imports: 8
- DB tables: config, datetime, pathlib, tbot_parking_import, utils, vehicles
- TODO/FIXME: 0

## `OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py`

- Lines: 770
- Functions: 15
- Classes: 0
- Imports: 9
- DB tables: IF, SET, __future__, access_role_permissions, access_roles, audit_log, audit_logger, barrier_phone_access, config, datetime, pathlib, remote_asset_movements, remote_assets, remote_handover_events, remote_order_details, remote_requests, service_catalog, service_item_workflows, service_items, service_order_steps, service_orders, service_workflow_profiles, service_workflow_steps, sqlite_master, typing
- TODO/FIXME: 0

## `OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py`

- Lines: 571
- Functions: 14
- Classes: 0
- Imports: 8
- DB tables: SET, __future__, access_control, charges, datetime, exc, pathlib, payments, service_catalog, service_item_workflows, service_items, service_orders, service_orders_core, service_price_versions, service_workflow_profiles, typing
- TODO/FIXME: 0

## `OSBB_Service_Orders_Foundation_v1/service_orders_core.py`

- Lines: 1126
- Functions: 31
- Classes: 0
- Imports: 9
- DB tables: __future__, access_control, audit_log, audit_logger, charges, config, datetime, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_access_credentials, service_item_workflows, service_items, service_order_charge_links, service_order_events, service_order_payment_links, service_order_steps, service_orders, service_price_versions, service_workflow_profiles, service_workflow_steps, sqlite_master, typing
- TODO/FIXME: 0

## `OSBB_Service_Orders_Foundation_v1/service_orders_preflight.py`

- Lines: 438
- Functions: 9
- Classes: 0
- Imports: 12
- DB tables: __future__, active, apartments, audit_log, datetime, pathlib, resident_accounts, service_catalog, service_orders, sqlite_master, types
- TODO/FIXME: 0

## `parking_billing_statement.py`

- Lines: 475
- Functions: 16
- Classes: 0
- Imports: 6
- DB tables: apartments, charges, config, datetime, pathlib, payment_allocations, payments, sqlite_master, vehicles
- TODO/FIXME: 0

## `parking_time_test_payload/Bots/handlers/profile_parking_time_test_workspace.py`

- Lines: 365
- Functions: 9
- Classes: 0
- Imports: 7
- DB tables: __future__, pathlib, profile_parking_time_test_core, service_orders, service_orders_core, telegram, typing, vehicles
- TODO/FIXME: 0

## `parking_time_test_payload/profile_parking_time_test_core.py`

- Lines: 828
- Functions: 27
- Classes: 0
- Imports: 5
- DB tables: IF, __future__, apartments, datetime, profile_parking_time_test_events, profile_parking_time_test_schema_migrations, profile_parking_time_test_sessions, resident, sqlite_master, typing, vehicles
- TODO/FIXME: 0

## `parking_time_test_payload/run_bot_live_services_sandbox_v1.py`

- Lines: 919
- Functions: 18
- Classes: 0
- Imports: 16
- DB tables: __future__, access_role_permissions, access_user_roles, audit_log, datetime, handlers, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_order_interests, service_order_steps, service_orders, service_preorders_core, sqlite_master, telegram_osbb, the, types, typing
- TODO/FIXME: 0

## `patch_cashier_v2_core_period_and_schemafix.py`

- Lines: 184
- Functions: 5
- Classes: 0
- Imports: 11
- DB tables: __future__, audit_log, charges, datetime, exc, pathlib, types
- TODO/FIXME: 0

## `patch_cashier_v2_core_schemafix.py`

- Lines: 205
- Functions: 6
- Classes: 0
- Imports: 13
- DB tables: __future__, apartments, audit_log, being, charges, datetime, exc, pathlib, payment_allocations, types
- TODO/FIXME: 0

## `patch_guard_workspace_default_cash_note.py`

- Lines: 181
- Functions: 3
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib
- TODO/FIXME: 0

## `patch_guard_workspace_direct_notice_confirm.py`

- Lines: 134
- Functions: 2
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib
- TODO/FIXME: 0

## `patch_parking_bot_cashier_operator.py`

- Lines: 212
- Functions: 6
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, handlers, pathlib
- TODO/FIXME: 0

## `patch_parking_bot_client_cabinet.py`

- Lines: 163
- Functions: 4
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, handlers, pathlib
- TODO/FIXME: 0

## `patch_parking_bot_client_portal.py`

- Lines: 203
- Functions: 6
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, handlers, pathlib
- TODO/FIXME: 0

## `patch_parking_bot_guard_workspace_v2.py`

- Lines: 281
- Functions: 4
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, handlers, pathlib
- TODO/FIXME: 0

## `patch_parking_bot_guard_workspace_v3.py`

- Lines: 257
- Functions: 6
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, handlers, pathlib
- TODO/FIXME: 0

## `patch_parking_bot_guard_workspace_v4.py`

- Lines: 267
- Functions: 6
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, handlers, pathlib
- TODO/FIXME: 0

## `patch_parking_bot_launch_queues_menu.py`

- Lines: 127
- Functions: 4
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib
- TODO/FIXME: 0

## `patch_parking_bot_service_orders_ui_v1.py`

- Lines: 324
- Functions: 10
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, handlers, pathlib, service_orders
- TODO/FIXME: 0

## `patch_parking_bot_service_orders_v1.py`

- Lines: 104
- Functions: 3
- Classes: 0
- Imports: 2
- DB tables: __future__, handlers, pathlib, service_orders, the
- TODO/FIXME: 0

## `phone_barrier_access_core.py`

- Lines: 2163
- Functions: 45
- Classes: 0
- Imports: 9
- DB tables: IF, __future__, access_control, access_operation_journal, access_points, access_policy_values, access_policy_versions, access_schema_migrations, access_tariff_versions, charges, datetime, in, payments, phone_access_request_points, phone_access_requests, phone_access_subscription_charges, phone_access_subscription_points, phone_access_subscriptions, service_access_credentials, service_orders, service_orders_core, sqlite_master, typing, using
- TODO/FIXME: 0

## `phone_barrier_access_service.py`

- Lines: 208
- Functions: 6
- Classes: 0
- Imports: 7
- DB tables: __future__, charges, datetime, phone_barrier_access_core, service_orders, service_orders_core, service_preorders_core, the, typing
- TODO/FIXME: 0

## `phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py`

- Lines: 1614
- Functions: 55
- Classes: 0
- Imports: 16
- DB tables: __future__, access_control, cashier_v2_core, handlers, pathlib, phone_barrier_access_core, phone_barrier_access_service, possibly, remote_order_details, service_item_workflows, service_items, service_order_steps, service_orders, service_orders_core, service_preorders_core, service_workflow_profiles, telegram, typing
- TODO/FIXME: 0

## `phone_barrier_access_v2_payload/phone_barrier_access_core.py`

- Lines: 2163
- Functions: 45
- Classes: 0
- Imports: 9
- DB tables: IF, __future__, access_control, access_operation_journal, access_points, access_policy_values, access_policy_versions, access_schema_migrations, access_tariff_versions, charges, datetime, in, payments, phone_access_request_points, phone_access_requests, phone_access_subscription_charges, phone_access_subscription_points, phone_access_subscriptions, service_access_credentials, service_orders, service_orders_core, sqlite_master, typing, using
- TODO/FIXME: 0

## `phone_barrier_access_v2_payload/phone_barrier_access_service.py`

- Lines: 208
- Functions: 6
- Classes: 0
- Imports: 7
- DB tables: __future__, charges, datetime, phone_barrier_access_core, service_orders, service_orders_core, service_preorders_core, the, typing
- TODO/FIXME: 0

## `phone_barrier_access_v2_payload/service_orders_core.py`

- Lines: 1338
- Functions: 31
- Classes: 0
- Imports: 9
- DB tables: __future__, access_control, audit_log, audit_logger, charges, config, datetime, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_access_credentials, service_item_workflows, service_items, service_order_charge_links, service_order_events, service_order_payment_links, service_order_steps, service_orders, service_price_versions, service_workflow_profiles, service_workflow_steps, sqlite_master, typing
- TODO/FIXME: 0

## `phone_barrier_access_v2_payload/service_preorders_core.py`

- Lines: 1147
- Functions: 24
- Classes: 0
- Imports: 6
- DB tables: IF, __future__, a, datetime, payment_notices, payments, phone_barrier_access_service, remote_assets, remote_order_issued_assets, remote_supplier_batch_links, remote_supplier_batches, service_item_workflows, service_items, service_order_interests, service_order_payment_links, service_order_steps, service_orders, service_orders_core, service_workflow_profiles, service_workflow_steps, supplier, the, typing
- TODO/FIXME: 0

## `plate_consensus_apply.py`

- Lines: 369
- Functions: 11
- Classes: 0
- Imports: 7
- DB tables: apartments, audit_log, config, datetime, operator_audit_log, paper, pathlib, plate_consensus_report, sqlite_master, vehicles
- TODO/FIXME: 0

## `plate_consensus_report.py`

- Lines: 705
- Functions: 38
- Classes: 0
- Imports: 9
- DB tables: apartments, collections, config, datetime, difflib, pathlib, payments, sqlite_master, tbot_parking_import, vehicles, verification_candidates
- TODO/FIXME: 0

## `plate_consensus_report_v3.py`

- Lines: 635
- Functions: 34
- Classes: 0
- Imports: 9
- DB tables: apartments, collections, config, datetime, difflib, pathlib, payments, sqlite_master, tbot_parking_import, vehicles, verification_candidates
- TODO/FIXME: 0

## `plate_consensus_top6.py`

- Lines: 102
- Functions: 3
- Classes: 0
- Imports: 6
- DB tables: config, datetime, pathlib, plate, plate_consensus_report
- TODO/FIXME: 0

## `prepare_live_service_test.py`

- Lines: 344
- Functions: 8
- Classes: 0
- Imports: 13
- DB tables: SET, __future__, access_audit_log, access_roles, access_user_roles, audit_log, datetime, exc, pathlib, remote_assets, service_catalog, service_orders, staff_principals, types, typing
- TODO/FIXME: 0

## `profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py`

- Lines: 865
- Functions: 18
- Classes: 0
- Imports: 16
- DB tables: __future__, access_role_permissions, access_user_roles, audit_log, datetime, handlers, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_order_interests, service_order_steps, service_orders, service_preorders_core, sqlite_master, telegram_osbb, the, types, typing
- TODO/FIXME: 0

## `profile_confirmation_button_ready_payload/Bots/handlers/profile_verification_workspace.py`

- Lines: 768
- Functions: 19
- Classes: 0
- Imports: 9
- DB tables: __future__, handlers, pathlib, profile_verification_core, service_orders, service_orders_core, telegram, the, typing, vehicles
- TODO/FIXME: 0

## `profile_parking_time_test_core.py`

- Lines: 828
- Functions: 27
- Classes: 0
- Imports: 5
- DB tables: IF, __future__, apartments, datetime, profile_parking_time_test_events, profile_parking_time_test_schema_migrations, profile_parking_time_test_sessions, resident, sqlite_master, typing, vehicles
- TODO/FIXME: 0

## `profile_verification_core.py`

- Lines: 1557
- Functions: 39
- Classes: 0
- Imports: 6
- DB tables: IF, __future__, contact, datetime, primary, resident, resident_profile_change_requests, resident_profile_operation_journal, resident_profile_policy_values, resident_profile_policy_versions, resident_profile_schema_migrations, resident_profile_verifications, sqlite_master, typing, vehicles
- TODO/FIXME: 0

## `profile_verification_critical_codes_payload/Bots/handlers/profile_verification_workspace.py`

- Lines: 765
- Functions: 19
- Classes: 0
- Imports: 9
- DB tables: __future__, handlers, pathlib, profile_verification_core, service_orders, service_orders_core, telegram, the, typing, vehicles
- TODO/FIXME: 0

## `profile_verification_payload/Bots/handlers/profile_verification_workspace.py`

- Lines: 714
- Functions: 18
- Classes: 0
- Imports: 9
- DB tables: __future__, handlers, pathlib, profile_verification_core, service_orders, service_orders_core, telegram, the, typing, vehicles
- TODO/FIXME: 0

## `profile_verification_payload/Bots/handlers/service_orders_workspace.py`

- Lines: 1736
- Functions: 58
- Classes: 0
- Imports: 17
- DB tables: __future__, access_control, both, cashier_v2_core, handlers, pathlib, phone_barrier_access_core, phone_barrier_access_service, possibly, profile, profile_verification_core, remote_order_details, service_item_workflows, service_items, service_order_steps, service_orders, service_orders_core, service_preorders_core, service_workflow_profiles, telegram, typing
- TODO/FIXME: 0

## `profile_verification_payload/profile_verification_core.py`

- Lines: 1531
- Functions: 39
- Classes: 0
- Imports: 6
- DB tables: IF, __future__, contact, datetime, primary, resident, resident_profile_change_requests, resident_profile_operation_journal, resident_profile_policy_values, resident_profile_policy_versions, resident_profile_schema_migrations, resident_profile_verifications, sqlite_master, typing, vehicles
- TODO/FIXME: 0

## `profile_verification_payload/run_bot_live_services_sandbox_v1.py`

- Lines: 831
- Functions: 18
- Classes: 0
- Imports: 16
- DB tables: __future__, access_role_permissions, access_user_roles, audit_log, datetime, handlers, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_order_interests, service_order_steps, service_orders, service_preorders_core, sqlite_master, telegram_osbb, the, types, typing
- TODO/FIXME: 0

## `profile_verification_terminology_v2_payload/Bots/handlers/profile_verification_workspace.py`

- Lines: 760
- Functions: 19
- Classes: 0
- Imports: 9
- DB tables: __future__, handlers, pathlib, profile_verification_core, service_orders, service_orders_core, telegram, the, typing, vehicles
- TODO/FIXME: 0

## `profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py`

- Lines: 1743
- Functions: 58
- Classes: 0
- Imports: 17
- DB tables: __future__, access_control, both, cashier_v2_core, handlers, pathlib, phone_barrier_access_core, phone_barrier_access_service, possibly, profile, profile_verification_core, remote_order_details, service_item_workflows, service_items, service_order_steps, service_orders, service_orders_core, service_preorders_core, service_workflow_profiles, telegram, typing
- TODO/FIXME: 0

## `profile_verification_terminology_v2_payload/profile_verification_core.py`

- Lines: 1557
- Functions: 39
- Classes: 0
- Imports: 6
- DB tables: IF, __future__, contact, datetime, primary, resident, resident_profile_change_requests, resident_profile_operation_journal, resident_profile_policy_values, resident_profile_policy_versions, resident_profile_schema_migrations, resident_profile_verifications, sqlite_master, typing, vehicles
- TODO/FIXME: 0

## `repair_confirmed_unit_seed_notes.py`

- Lines: 140
- Functions: 3
- Classes: 0
- Imports: 8
- DB tables: __future__, apartments, audit_log, audit_logger, config, datetime, operator_audit_log, pathlib
- TODO/FIXME: 0

## `report_bot_admins.py`

- Lines: 163
- Functions: 3
- Classes: 0
- Imports: 5
- DB tables: bot_admins, config, datetime, pathlib, payments
- TODO/FIXME: 0

## `report_plate_candidates.py`

- Lines: 268
- Functions: 5
- Classes: 0
- Imports: 6
- DB tables: config, datetime, pathlib, utils, verification_candidates, verification_tasks
- TODO/FIXME: 0

## `report_verification_evidence.py`

- Lines: 197
- Functions: 2
- Classes: 0
- Imports: 6
- DB tables: config, datetime, pathlib, utils, verification_evidence, verification_tasks
- TODO/FIXME: 0

## `report_verification_tasks.py`

- Lines: 164
- Functions: 6
- Classes: 1
- Imports: 6
- DB tables: config, datetime, pathlib, utils, verification_tasks
- TODO/FIXME: 0

## `report_verification_tasks_enriched.py`

- Lines: 268
- Functions: 4
- Classes: 0
- Imports: 7
- DB tables: collections, config, datetime, pathlib, utils, verification_evidence, verification_tasks
- TODO/FIXME: 0

## `reset_service_catalog.py`

- Lines: 628
- Functions: 15
- Classes: 0
- Imports: 7
- DB tables: audit_log, audit_logger, barrier_phone_access, cashbox_operations, charges, config, datetime, pathlib, payment_allocations, payments, service_catalog, service_items, sqlite_master, sqlite_sequence
- TODO/FIXME: 1

## `restore_resident_apartment_link.py`

- Lines: 321
- Functions: 12
- Classes: 0
- Imports: 9
- DB tables: __future__, apartments, audit_log, audit_logger, config, datetime, operator_audit_log, pathlib, resident_accounts, sqlite_master, typing
- TODO/FIXME: 0

## `RETIRE_legacy_new_remote_test_orders_sandbox.py`

- Lines: 118
- Functions: 1
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, pathlib, remote_asset_movements, remote_assets, service_order_payment_links, service_order_steps, service_orders
- TODO/FIXME: 0

## `run_bot_guard_sandbox.py`

- Lines: 236
- Functions: 8
- Classes: 0
- Imports: 12
- DB tables: __future__, audit_log, cashier_receipts, exc, in, pathlib, payment_notices, remote_handover_events, remote_requests, sqlite_master, types, typing
- TODO/FIXME: 0

## `run_bot_guard_sandbox_v2.py`

- Lines: 236
- Functions: 8
- Classes: 0
- Imports: 12
- DB tables: __future__, audit_log, cashier_receipts, exc, in, pathlib, payment_notices, remote_handover_events, remote_requests, sqlite_master, types, typing
- TODO/FIXME: 0

## `run_bot_guard_sandbox_v3.py`

- Lines: 236
- Functions: 8
- Classes: 0
- Imports: 12
- DB tables: __future__, audit_log, cashier_receipts, exc, in, pathlib, payment_notices, remote_handover_events, remote_requests, sqlite_master, types, typing
- TODO/FIXME: 0

## `run_bot_live_service_sandbox_v4.py`

- Lines: 250
- Functions: 9
- Classes: 0
- Imports: 12
- DB tables: __future__, audit_log, cashier_receipts, exc, pathlib, payment_notices, remote_asset_movements, remote_assets, service_catalog, service_order_steps, service_orders, sqlite_master, types, typing
- TODO/FIXME: 0

## `run_bot_live_services_sandbox_v1.py`

- Lines: 919
- Functions: 18
- Classes: 0
- Imports: 16
- DB tables: __future__, access_role_permissions, access_user_roles, audit_log, datetime, handlers, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_order_interests, service_order_steps, service_orders, service_preorders_core, sqlite_master, telegram_osbb, the, types, typing
- TODO/FIXME: 0

## `run_bot_sandbox_v2.py`

- Lines: 286
- Functions: 9
- Classes: 0
- Imports: 12
- DB tables: __future__, audit_log, bank_transactions, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, exc, for, in, its, pathlib, payment_notices, payments, sqlite_master, types, typing
- TODO/FIXME: 0

## `search_vehicle_by_plate_fragment.py`

- Lines: 244
- Functions: 11
- Classes: 0
- Imports: 7
- DB tables: apartments, config, contacts, difflib, pathlib, sqlite_master, vehicles
- TODO/FIXME: 0

## `seed_bot_admins.py`

- Lines: 179
- Functions: 4
- Classes: 0
- Imports: 6
- DB tables: SET, bot_admins, config, datetime, e, pathlib, payments, telegram_osbb
- TODO/FIXME: 0

## `seed_commercial_unit_placeholders.py`

- Lines: 395
- Functions: 15
- Classes: 0
- Imports: 8
- DB tables: IF, __future__, apartments, audit_log, audit_logger, config, datetime, pathlib, sqlite_master, unit_contacts
- TODO/FIXME: 0

## `seed_parking_tariffs.py`

- Lines: 166
- Functions: 4
- Classes: 0
- Imports: 4
- DB tables: config, pathlib, service_catalog, service_tariffs
- TODO/FIXME: 0

## `service_catalog_admin_core.py`

- Lines: 571
- Functions: 14
- Classes: 0
- Imports: 8
- DB tables: SET, __future__, access_control, charges, datetime, exc, pathlib, payments, service_catalog, service_item_workflows, service_items, service_orders, service_orders_core, service_price_versions, service_workflow_profiles, typing
- TODO/FIXME: 0

## `service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py`

- Lines: 1632
- Functions: 55
- Classes: 0
- Imports: 16
- DB tables: __future__, access_control, both, cashier_v2_core, handlers, pathlib, phone_barrier_access_core, phone_barrier_access_service, possibly, remote_order_details, service_item_workflows, service_items, service_order_steps, service_orders, service_orders_core, service_preorders_core, service_workflow_profiles, telegram, typing
- TODO/FIXME: 0

## `service_code_compatibility_payload/service_orders_core.py`

- Lines: 1409
- Functions: 32
- Classes: 0
- Imports: 9
- DB tables: __future__, access_control, audit_log, audit_logger, charges, config, datetime, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_access_credentials, service_item_workflows, service_items, service_order_charge_links, service_order_events, service_order_payment_links, service_order_steps, service_orders, service_price_versions, service_workflow_profiles, service_workflow_steps, sqlite_master, typing
- TODO/FIXME: 0

## `service_code_compatibility_payload/service_preorders_core.py`

- Lines: 1155
- Functions: 24
- Classes: 0
- Imports: 6
- DB tables: IF, __future__, a, datetime, payment_notices, payments, phone_barrier_access_service, remote_assets, remote_order_issued_assets, remote_supplier_batch_links, remote_supplier_batches, service_item_workflows, service_items, service_order_interests, service_order_payment_links, service_order_steps, service_orders, service_orders_core, service_workflow_profiles, service_workflow_steps, supplier, the, typing
- TODO/FIXME: 0

## `service_orders_core.py`

- Lines: 1409
- Functions: 32
- Classes: 0
- Imports: 9
- DB tables: __future__, access_control, audit_log, audit_logger, charges, config, datetime, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_access_credentials, service_item_workflows, service_items, service_order_charge_links, service_order_events, service_order_payment_links, service_order_steps, service_orders, service_price_versions, service_workflow_profiles, service_workflow_steps, sqlite_master, typing
- TODO/FIXME: 0

## `service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py`

- Lines: 1126
- Functions: 31
- Classes: 0
- Imports: 9
- DB tables: __future__, access_control, audit_log, audit_logger, charges, config, datetime, pathlib, payments, remote_asset_movements, remote_assets, remote_order_details, service_access_credentials, service_item_workflows, service_items, service_order_charge_links, service_order_events, service_order_payment_links, service_order_steps, service_orders, service_price_versions, service_workflow_profiles, service_workflow_steps, sqlite_master, typing
- TODO/FIXME: 0

## `service_orders_preflight.py`

- Lines: 438
- Functions: 9
- Classes: 0
- Imports: 12
- DB tables: __future__, active, apartments, audit_log, datetime, pathlib, resident_accounts, service_catalog, service_orders, sqlite_master, types
- TODO/FIXME: 0

## `service_preorders_core.py`

- Lines: 1155
- Functions: 24
- Classes: 0
- Imports: 6
- DB tables: IF, __future__, a, datetime, payment_notices, payments, phone_barrier_access_service, remote_assets, remote_order_issued_assets, remote_supplier_batch_links, remote_supplier_batches, service_item_workflows, service_items, service_order_interests, service_order_payment_links, service_order_steps, service_orders, service_orders_core, service_workflow_profiles, service_workflow_steps, supplier, the, typing
- TODO/FIXME: 0

## `supervisor_dashboard.py`

- Lines: 647
- Functions: 20
- Classes: 0
- Imports: 11
- DB tables: IF, apartments, audit_log, charges, collections, config, datetime, exc, in, openpyxl, operator_audit_log, pathlib, payment_allocations, payments, plate_consensus_report, service_catalog, service_tariffs, sqlite_master, vehicles
- TODO/FIXME: 0

## `switch_parking_bot_to_cashier_v2.py`

- Lines: 135
- Functions: 3
- Classes: 0
- Imports: 5
- DB tables: __future__, datetime, handlers, pathlib
- TODO/FIXME: 0

## `telegram_test_login.py`

- Lines: 42
- Functions: 1
- Classes: 0
- Imports: 7
- DB tables: config, pathlib, telegram_osbb, telegram_secrets, telethon
- TODO/FIXME: 0

## `telegram_test_login_manual.py`

- Lines: 65
- Functions: 1
- Classes: 0
- Imports: 6
- DB tables: config, pathlib, telegram_osbb, telethon
- TODO/FIXME: 0

## `test.py`

- Lines: 1
- Functions: 0
- Classes: 0
- Imports: 0
- DB tables: -
- TODO/FIXME: 0
- Parse error: IndentationError: unexpected indent (test.py, line 1)

## `test_db_access_unit_resolver.py`

- Lines: 82
- Functions: 1
- Classes: 0
- Imports: 4
- DB tables: __future__, pathlib
- TODO/FIXME: 0

## `tools/cashier_parking_payments_audit_v4.py`

- Lines: 616
- Functions: 24
- Classes: 0
- Imports: 14
- DB tables: __future__, apartments, charges, collections, config, datetime, import, openpyxl, paid, pathlib, payment_allocations, payments, sqlite_master, typing, vehicles
- TODO/FIXME: 0

## `tools/cashier_unpaid_preview.py`

- Lines: 203
- Functions: 12
- Classes: 0
- Imports: 5
- DB tables: alloc, apartments, charges, config, datetime, pathlib, payment_allocations, sqlite_master, vehicles
- TODO/FIXME: 0

## `tools/cashier_unpaid_preview_v2.py`

- Lines: 260
- Functions: 10
- Classes: 0
- Imports: 6
- DB tables: apartments, charges, config, datetime, pathlib, payment_allocations, sqlite_master, vehicles
- TODO/FIXME: 0

## `tools/cashier_unpaid_preview_v3.py`

- Lines: 580
- Functions: 22
- Classes: 0
- Imports: 14
- DB tables: __future__, apartments, charges, collections, config, datetime, import, openpyxl, paid, pathlib, payment_allocations, payments, sqlite_master, typing, vehicles
- TODO/FIXME: 0

## `tools/db_schema_compare.py`

- Lines: 407
- Functions: 16
- Classes: 0
- Imports: 11
- DB tables: OSBB, STRUCTURAL, __future__, config, datetime, differences, in, pathlib, sqlite_master, typing
- TODO/FIXME: 0

## `tools/db_schema_snapshot.py`

- Lines: 361
- Functions: 14
- Classes: 0
- Imports: 10
- DB tables: LIST, OSBB, __future__, apartments, audit_log, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, charges, collections, config, contact_methods, datetime, in, operator_audit_log, parking_time_review_tasks, pathlib, payment_allocations, payments, persons, resident_accounts, service_catalog, service_items, service_tariffs, sqlite_master, typing, vehicles
- TODO/FIXME: 0

## `tools/db_schema_snapshot_full.py`

- Lines: 356
- Functions: 16
- Classes: 0
- Imports: 10
- DB tables: LIST, __future__, apartments, audit_log, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, charges, collections, config, contact_methods, datetime, in, operator_audit_log, parking_time_review_tasks, pathlib, payment_allocations, payments, persons, resident_accounts, service_catalog, service_items, service_tariffs, sqlite_master, typing, vehicles
- TODO/FIXME: 0

## `tools/project_code_search.py`

- Lines: 154
- Functions: 5
- Classes: 0
- Imports: 4
- DB tables: datetime, pathlib, remote_requests
- TODO/FIXME: 0

## `tools/project_passport.py`

- Lines: 613
- Functions: 15
- Classes: 7
- Imports: 11
- DB tables: References, __future__, apartment_verification, apartments, audit_log, bank_transactions, barrier_phone_access, cashbox_operations, cashboxes, cashier_batch_items, cashier_batches, cashier_receipts, cashier_reconciliation_cases, charges, commercial_contract_items, commercial_contracts, commercial_notifications, contact_methods, dataclasses, datetime, in, operator_audit_log, parking_time_review_tasks, pathlib, payment_allocations, payment_notices, payments, persons, references, refs, remote_asset_movements, remote_assets, remote_handover_events, remote_order_details, remote_requests, resident_accounts, service_catalog, service_items, service_order_interests, service_order_items, service_order_steps, service_orders, service_tariffs, service_workflow_profiles, service_workflow_steps, typing, unit_aliases, unit_contacts, unit_group_aliases, unit_group_members, unit_groups, vehicles, verification_candidates, verification_evidence, verification_tasks
- TODO/FIXME: 5

## `unit_resolver.py`

- Lines: 551
- Functions: 25
- Classes: 2
- Imports: 10
- DB tables: __future__, apartments, config, dataclasses, in, pathlib, sqlite_master, typing, unit_group_aliases, unit_group_members, unit_groups
- TODO/FIXME: 0

## `utils.py`

- Lines: 268
- Functions: 10
- Classes: 0
- Imports: 2
- DB tables: -
- TODO/FIXME: 0

## `vehicle_data_quality_tasks.py`

- Lines: 381
- Functions: 21
- Classes: 0
- Imports: 8
- DB tables: apartments, config, datetime, difflib, has, not, pathlib, payment, payments, sqlite_master, unlinked, vehicles
- TODO/FIXME: 0

## `vehicle_verification_tasks.py`

- Lines: 596
- Functions: 23
- Classes: 0
- Imports: 8
- DB tables: apartments, config, datetime, difflib, pathlib, payments, sqlite_master, tbot_parking_import, vehicles, verification_tasks
- TODO/FIXME: 0

## `Word_table_to_Excel.py`

- Lines: 62
- Functions: 1
- Classes: 0
- Imports: 4
- DB tables: docx, in, openpyxl
- TODO/FIXME: 0
