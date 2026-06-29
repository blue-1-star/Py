# Tables Referenced by Code but Missing in DB

These are table names referenced by scanned source code but not present in the selected DB schema.

## `service_orders`
- refs: 390
- files: Bots/handlers/client_portal_v3.py, Bots/handlers/profile_parking_time_test_workspace.py, Bots/handlers/profile_verification_workspace.py, Bots/handlers/service_orders_workspace.py, CHECK_guard_sandbox_service_orders.py, CHECK_guard_sandbox_service_orders_v2.py, CHECK_profile_verification_terminology_v2.py, CHECK_service_code_compatibility_phone_v2.py, CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.py, FIND_actual_service_order_state.py, FIX_live_services_sandbox_payment_schema.py, INSTALL_PHONE_ACCESS_UI_FIX_v2.py, INSTALL_PHONE_ACCESS_UI_FIX_v3.py, INSTALL_cashier_route_after_phone_v2.py, INSTALL_phone_barrier_access_v2.py, INSTALL_profile_verification_terminology_v2.py, INSTALL_profile_verification_v1.py, INSTALL_service_code_compatibility_phone_v2.py, MIGRATE_phone_barrier_access_operational_sandbox.py, MIGRATE_phone_barrier_access_sandbox.py ... +46
- sample: `Сам процесс находится в service_orders_workspace.py и подключается`

## `pathlib`
- refs: 218
- files: Bots/db_access - Copy.py, Bots/db_access.py, Bots/handlers/audit_viewer - Copy.py, Bots/handlers/audit_viewer.py, Bots/handlers/cashier_operator.py, Bots/handlers/cashier_operator_v2.py, Bots/handlers/client_portal.py, Bots/handlers/client_portal_safe_linking.py, Bots/handlers/client_portal_v2.py, Bots/handlers/client_portal_v3.py, Bots/handlers/commercial_contract_editor.py, Bots/handlers/guard_workspace.py, Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py, Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py, Bots/handlers/profile_parking_time_test_workspace.py, Bots/handlers/profile_verification_workspace.py, Bots/handlers/service_orders_workspace.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py, Bots/handlers/vehicle_card_editor.py ... +198
- sample: `from pathlib import Path`

## `datetime`
- refs: 175
- files: Bots/db_access - Copy.py, Bots/db_access.py, Bots/handlers/cashier_operator.py, Bots/handlers/client_portal.py, Bots/handlers/client_portal_safe_linking.py, Bots/handlers/commercial_contract_editor.py, Bots/handlers/guard_workspace.py, Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py, Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py, Bots/handlers/vehicle_verification.py, CHECK_guard_sandbox_service_orders.py, CHECK_guard_sandbox_service_orders_v2.py, CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.py, Data/audit_databases.py, Data/clean_base_01.py, Data/clean_base_02.py, FIND_actual_service_order_state.py, FIX_live_services_sandbox_payment_schema.py ... +155
- sample: `from datetime import datetime`

## `IF`
- refs: 170
- files: OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, audit_logger.py, billing/build_parking_time_review_tasks.py, billing/migrate_add_parking_billing.py, build_plate_candidates.py, init_osbb_db.py, init_osbb_quarantine_db.py, init_osbb_telegram_db.py, migrate_access_control_and_guard.py, migrate_add_verification_evidence.py, migrate_add_verification_tasks.py, migrate_apartment_link_requests.py, migrate_apartment_verification.py, migrate_billing_core.py, migrate_bot_core.py, migrate_cashier_core.py, migrate_cashier_operator_editor.py, migrate_cashier_v2.py, migrate_cashier_v2_compat.py, migrate_charge_adjustments.py ... +19
- sample: `CREATE TABLE IF NOT EXISTS operator_audit_log (`

## `__future__`
- refs: 145
- files: Bots/handlers/audit_viewer.py, Bots/handlers/cashier_operator.py, Bots/handlers/cashier_operator_v2.py, Bots/handlers/client_portal.py, Bots/handlers/client_portal_safe_linking.py, Bots/handlers/client_portal_v2.py, Bots/handlers/client_portal_v3.py, Bots/handlers/commercial_contract_editor.py, Bots/handlers/guard_workspace.py, Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py, Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py, Bots/handlers/profile_parking_time_test_workspace.py, Bots/handlers/profile_verification_workspace.py, Bots/handlers/service_orders_workspace.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py, CHECK_guard_sandbox_service_orders.py, CHECK_guard_sandbox_service_orders_v2.py, CHECK_phone_barrier_access_operational_sandbox.py, CHECK_phone_barrier_access_sandbox_schema.py ... +125
- sample: `from __future__ import annotations`

## `config`
- refs: 129
- files: Bots/db_access - Copy.py, Bots/db_access.py, Bots/handlers/audit_viewer - Copy.py, Bots/handlers/audit_viewer.py, Bots/handlers/cashier_operator.py, Bots/handlers/client_portal.py, Bots/handlers/client_portal_safe_linking.py, Bots/handlers/commercial_contract_editor.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py, Bots/handlers/vehicle_card_editor.py, Bots/handlers/vehicle_full_list.py, Bots/handlers/vehicle_verification.py, Bots/parking_bot - Copy.py, Bots/parking_bot.py, Bots/parking_bot_before_cashier_editor_2026-06-25_14-45-08.py, Bots/parking_bot_before_client_portal_2026-06-25_10-25-49.py, Bots/parking_bot_before_language_gate_fix_2026-06-25_10-45-39.py, Bots/parking_bot_before_launch_queues_menu_2026-06-25_12-21-29.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py ... +104
- sample: `from config import paths, USE_TEST_DB`

## `sqlite_master`
- refs: 128
- files: Bots/db_access - Copy.py, Bots/db_access.py, Bots/handlers/audit_viewer - Copy.py, Bots/handlers/audit_viewer.py, Bots/handlers/cashier_operator.py, Bots/handlers/client_portal.py, Bots/handlers/client_portal_safe_linking.py, Bots/handlers/commercial_contract_editor.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py, Bots/handlers/vehicle_verification.py, CHECK_guard_sandbox_service_orders.py, CHECK_guard_sandbox_service_orders_v2.py, CHECK_profile_test_candidate_apartment_40.py, CHECK_profile_verification_sandbox.py, FIND_actual_service_order_state.py, FIX_live_services_sandbox_payment_schema.py, MIGRATE_profile_parking_time_test_sandbox.py, MIGRATE_profile_verification_sandbox.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py ... +74
- sample: `"SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",`

## `handlers`
- refs: 122
- files: Bots/handlers/audit_viewer.py, Bots/handlers/cashier_operator.py, Bots/handlers/cashier_operator_v2.py, Bots/handlers/client_portal_v2.py, Bots/handlers/client_portal_v3.py, Bots/handlers/commercial_contract_editor.py, Bots/handlers/profile_verification_workspace.py, Bots/handlers/service_orders_workspace.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py, Bots/parking_bot - Copy.py, Bots/parking_bot.py, Bots/parking_bot_before_cashier_editor_2026-06-25_14-45-08.py, Bots/parking_bot_before_client_portal_2026-06-25_10-25-49.py, Bots/parking_bot_before_language_gate_fix_2026-06-25_10-45-39.py, Bots/parking_bot_before_launch_queues_menu_2026-06-25_12-21-29.py, cashier_v2_core.py, cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py, cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py ... +20
- sample: `from handlers.audit_viewer import handle_audit_viewer_text`

## `service_order_steps`
- refs: 116
- files: Bots/handlers/service_orders_workspace.py, CHECK_guard_sandbox_service_orders.py, CHECK_guard_sandbox_service_orders_v2.py, FIND_actual_service_order_state.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, OSBB_Service_Orders_Foundation_v1/service_orders_core.py, RETIRE_legacy_new_remote_test_orders_sandbox.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, install_service_orders_ui.py, migrate_service_orders_and_fulfillment.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/service_orders_core.py, phone_barrier_access_v2_payload/service_preorders_core.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, run_bot_live_service_sandbox_v4.py, run_bot_live_services_sandbox_v1.py ... +9
- sample: `resource = "service_order_steps" if action == "CONFIRM" else "service_orders"`

## `remote_assets`
- refs: 90
- files: CHECK_guard_sandbox_service_orders.py, CHECK_guard_sandbox_service_orders_v2.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, OSBB_Service_Orders_Foundation_v1/service_orders_core.py, RETIRE_legacy_new_remote_test_orders_sandbox.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, create_clean_live_sandbox.py, create_isolated_live_sandbox_v2.py, migrate_service_orders_and_fulfillment.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, phone_barrier_access_v2_payload/service_orders_core.py, phone_barrier_access_v2_payload/service_preorders_core.py, prepare_live_service_test.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, run_bot_live_service_sandbox_v4.py, run_bot_live_services_sandbox_v1.py, service_code_compatibility_payload/service_orders_core.py, service_code_compatibility_payload/service_preorders_core.py, service_orders_core.py ... +5
- sample: `("remote_assets", "VIEW", "POST", "O"),`

## `typing`
- refs: 86
- files: Bots/handlers/audit_viewer.py, Bots/handlers/cashier_operator.py, Bots/handlers/cashier_operator_v2.py, Bots/handlers/client_portal.py, Bots/handlers/client_portal_safe_linking.py, Bots/handlers/client_portal_v2.py, Bots/handlers/commercial_contract_editor.py, Bots/handlers/guard_workspace.py, Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py, Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py, Bots/handlers/profile_parking_time_test_workspace.py, Bots/handlers/profile_verification_workspace.py, Bots/handlers/service_orders_workspace.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py, CHECK_guard_sandbox_service_orders.py, CHECK_guard_sandbox_service_orders_v2.py, CHECK_profile_test_candidate_apartment_40.py, FIND_actual_service_order_state.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py ... +66
- sample: `from typing import Any`

## `service_workflow_profiles`
- refs: 59
- files: Bots/handlers/service_orders_workspace.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py, OSBB_Service_Orders_Foundation_v1/service_orders_core.py, install_service_orders_ui.py, migrate_service_orders_and_fulfillment.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/service_orders_core.py, phone_barrier_access_v2_payload/service_preorders_core.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, service_catalog_admin_core.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/service_orders_core.py, service_code_compatibility_payload/service_preorders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py, service_preorders_core.py, tools/project_passport.py, tools/project_passport_v2.py ... +1
- sample: `JOIN service_workflow_profiles p`

## `remote_handover_events`
- refs: 54
- files: Bots/handlers/guard_workspace.py, Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py, Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py, CHECK_guard_sandbox_service_orders.py, CHECK_guard_sandbox_service_orders_v2.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, create_clean_live_sandbox.py, create_isolated_live_sandbox_v2.py, guard_workspace_preflight.py, guard_workspace_preflight_v2.py, manage_staff_access.py, manage_staff_access_v2.py, migrate_access_control_and_guard.py, migrate_service_orders_and_fulfillment.py, run_bot_guard_sandbox.py, run_bot_guard_sandbox_v2.py, run_bot_guard_sandbox_v3.py, tools/project_passport.py, tools/project_passport_v2.py, tools/project_passport_v4_runtime_schema_audit.py
- sample: `"remote_handover_events",`

## `service_order_interests`
- refs: 51
- files: CHECK_service_code_compatibility_phone_v2.py, MIGRATE_phone_barrier_access_operational_sandbox.py, MIGRATE_phone_barrier_access_sandbox.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, phone_barrier_access_v2_payload/service_preorders_core.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, run_bot_live_services_sandbox_v1.py, service_code_compatibility_payload/service_preorders_core.py, service_preorders_core.py, tools/project_passport.py, tools/project_passport_v2.py, tools/project_passport_v4_runtime_schema_audit.py
- sample: `"service_order_interests",`

## `telegram`
- refs: 47
- files: Bots/data_park_bot.py, Bots/handlers/agreement - Copy.py, Bots/handlers/agreement.py, Bots/handlers/audit_viewer - Copy.py, Bots/handlers/audit_viewer.py, Bots/handlers/cashier_operator.py, Bots/handlers/cashier_operator_v2.py, Bots/handlers/client_portal.py, Bots/handlers/client_portal_safe_linking.py, Bots/handlers/client_portal_v2.py, Bots/handlers/commercial_contract_editor.py, Bots/handlers/guard_workspace.py, Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py, Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py, Bots/handlers/profile_parking_time_test_workspace.py, Bots/handlers/profile_verification_workspace.py, Bots/handlers/service_orders_workspace.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py, Bots/handlers/vehicle_card_editor.py ... +18
- sample: `from telegram import Update, ReplyKeyboardMarkup`

## `remote_order_details`
- refs: 42
- files: Bots/handlers/service_orders_workspace.py, CHECK_guard_sandbox_service_orders.py, CHECK_guard_sandbox_service_orders_v2.py, FIND_actual_service_order_state.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, OSBB_Service_Orders_Foundation_v1/service_orders_core.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, migrate_service_orders_and_fulfillment.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/service_orders_core.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, run_bot_live_services_sandbox_v1.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/service_orders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py ... +3
- sample: `cur.execute("UPDATE remote_order_details SET resident_asset_id = ?, updated_at = ? WHERE service_order_id = ?", (int(asset["id"]), __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'), int(order["id"])))`

## `remote_asset_movements`
- refs: 41
- files: OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, OSBB_Service_Orders_Foundation_v1/service_orders_core.py, RETIRE_legacy_new_remote_test_orders_sandbox.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, migrate_service_orders_and_fulfillment.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, phone_barrier_access_v2_payload/service_orders_core.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, run_bot_live_service_sandbox_v4.py, run_bot_live_services_sandbox_v1.py, service_code_compatibility_payload/service_orders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py, tools/project_passport.py, tools/project_passport_v2.py, tools/project_passport_v4_runtime_schema_audit.py
- sample: `("remote_asset_movements", "VIEW", "POST", "O"),`

## `audit_logger`
- refs: 40
- files: Bots/handlers/cashier_operator.py, Bots/handlers/client_portal.py, Bots/handlers/client_portal_safe_linking.py, Bots/handlers/commercial_contract_editor.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py, Bots/handlers/vehicle_card_editor.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, OSBB_Service_Orders_Foundation_v1/service_orders_core.py, access_control.py, cashier_journal.py, cashier_v2_core.py, cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py, cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py, commercial_contracts.py, commercial_notification_delivery.py, import_ohorona_list1_to_central_cashbox.py, import_ohorona_to_cashbox.py, manage_staff_access.py, manage_staff_access_v2.py ... +20
- sample: `from audit_logger import audit_log`

## `in`
- refs: 33
- files: CHECK_guard_sandbox_service_orders_v2.py, CHECK_phone_barrier_access_operational_sandbox.py, CHECK_phone_barrier_access_sandbox_schema.py, CHECK_profile_test_candidate_apartment_40.py, MIGRATE_phone_barrier_access_operational_sandbox.py, Word_table_to_Excel.py, audit_registry.py, cashier_v2_preflight.py, diagnose_sandbox_charges.py, migrate_bot_core.py, migrate_cashier_v2.py, migrate_service_items.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py, run_bot_guard_sandbox.py, run_bot_guard_sandbox_v2.py, run_bot_guard_sandbox_v3.py, run_bot_sandbox_v2.py, supervisor_dashboard.py, tools/db_schema_compare.py ... +6
- sample: `for table in tables:`

## `access_user_roles`
- refs: 32
- files: access_control.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, create_clean_live_sandbox.py, create_isolated_live_sandbox_v2.py, guard_workspace_preflight.py, guard_workspace_preflight_v2.py, manage_staff_access.py, manage_staff_access_v2.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, prepare_live_service_test.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, run_bot_live_services_sandbox_v1.py
- sample: `FROM access_user_roles ur`

## `resident_profile_verifications`
- refs: 31
- files: CHECK_profile_verification_sandbox.py, profile_verification_core.py, profile_verification_payload/profile_verification_core.py, profile_verification_terminology_v2_payload/profile_verification_core.py
- sample: `print("Profile rows:",conn.execute("SELECT COUNT(*) FROM resident_profile_verifications").fetchone()[0])`

## `service_orders_core`
- refs: 31
- files: Bots/handlers/profile_parking_time_test_workspace.py, Bots/handlers/profile_verification_workspace.py, Bots/handlers/service_orders_workspace.py, OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py, parking_time_test_payload/Bots/handlers/profile_parking_time_test_workspace.py, phone_barrier_access_core.py, phone_barrier_access_service.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_service.py, phone_barrier_access_v2_payload/service_preorders_core.py, profile_confirmation_button_ready_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_critical_codes_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, service_catalog_admin_core.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/service_preorders_core.py ... +1
- sample: `from service_orders_core import get_conn, text`

## `service_workflow_steps`
- refs: 31
- files: OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, OSBB_Service_Orders_Foundation_v1/service_orders_core.py, migrate_service_orders_and_fulfillment.py, phone_barrier_access_v2_payload/service_orders_core.py, phone_barrier_access_v2_payload/service_preorders_core.py, service_code_compatibility_payload/service_orders_core.py, service_code_compatibility_payload/service_preorders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py, service_preorders_core.py, tools/project_passport.py, tools/project_passport_v2.py, tools/project_passport_v4_runtime_schema_audit.py
- sample: `"service_workflow_steps": """`

## `SET`
- refs: 31
- files: Bots/db_access - Copy.py, Bots/db_access.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py, create_clean_live_sandbox.py, create_isolated_live_sandbox_v2.py, guard_workspace_preflight.py, guard_workspace_preflight_v2.py, manage_staff_access.py, manage_staff_access_v2.py, migrate_access_control_and_guard.py, migrate_service_orders_and_fulfillment.py, prepare_live_service_test.py, seed_bot_admins.py, service_catalog_admin_core.py
- sample: `DO UPDATE SET`

## `openpyxl`
- refs: 30
- files: Collect_word_tables.py, Data/create_payment_sheet.py, Word_table_to_Excel.py, billing/import_ohorona_parking_time.py, billing/import_ohorona_parking_time_simple_preview.py, billing/import_parking_time_hints_from_ohorona.py, billing/report_parking_time_with_hints.py, billing_statement_excel.py, cashier_journal.py, import_ohorona_sheet1_payments.py, import_ohorona_to_cashbox.py, supervisor_dashboard.py, tools/cashier_parking_payments_audit_v4.py, tools/cashier_unpaid_preview_v3.py
- sample: `from openpyxl import load_workbook`

## `exc`
- refs: 29
- files: Bots/db_access.py, Bots/handlers/cashier_operator.py, Bots/handlers/commercial_contract_editor.py, INSTALL_PHONE_ACCESS_UI_FIX_v2.py, INSTALL_PHONE_ACCESS_UI_FIX_v3.py, MIGRATE_simplified_services_sandbox.py, OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py, cashier_v2_core.py, cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py, cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py, patch_cashier_v2_core_period_and_schemafix.py, patch_cashier_v2_core_schemafix.py, prepare_live_service_test.py, run_bot_guard_sandbox.py, run_bot_guard_sandbox_v2.py, run_bot_guard_sandbox_v3.py, run_bot_live_service_sandbox_v4.py, run_bot_sandbox_v2.py, service_catalog_admin_core.py, supervisor_dashboard.py
- sample: `) from exc`

## `the`
- refs: 27
- files: Bots/handlers/client_portal_v2.py, Bots/handlers/guard_workspace.py, Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py, Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py, Bots/handlers/profile_verification_workspace.py, MIGRATE_simplified_services_sandbox.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, fix_source_ref_schema.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, patch_parking_bot_service_orders_v1.py, phone_barrier_access_service.py, phone_barrier_access_v2_payload/phone_barrier_access_service.py, phone_barrier_access_v2_payload/service_preorders_core.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_confirmation_button_ready_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_critical_codes_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, profile_verification_terminology_v2_payload/Bots/handlers/profile_verification_workspace.py, run_bot_live_services_sandbox_v1.py ... +2
- sample: `"choose_service": "Choose a service from the catalogue.",`

## `Bots`
- refs: 24
- files: Bots/db_access - Copy.py, Bots/db_access.py, Bots/handlers/agreement - Copy.py, Bots/handlers/agreement.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py, Bots/parking_bot - Copy.py, Bots/parking_bot.py, Bots/parking_bot_before_cashier_editor_2026-06-25_14-45-08.py, Bots/parking_bot_before_client_portal_2026-06-25_10-25-49.py, Bots/parking_bot_before_language_gate_fix_2026-06-25_10-45-39.py, Bots/parking_bot_before_launch_queues_menu_2026-06-25_12-21-29.py
- sample: `# Add this block into Bots\db_access.py after resident account functions.`

## `remote_supplier_batch_links`
- refs: 24
- files: phone_barrier_access_v2_payload/service_preorders_core.py, service_code_compatibility_payload/service_preorders_core.py, service_preorders_core.py
- sample: `SELECT 1 FROM remote_supplier_batch_links l`

## `service_order_payment_links`
- refs: 24
- files: OSBB_Service_Orders_Foundation_v1/service_orders_core.py, RETIRE_legacy_new_remote_test_orders_sandbox.py, install_service_orders_ui.py, phone_barrier_access_v2_payload/service_orders_core.py, phone_barrier_access_v2_payload/service_preorders_core.py, service_code_compatibility_payload/service_orders_core.py, service_code_compatibility_payload/service_preorders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py, service_preorders_core.py
- sample: `SAFE_PAYMENT_FUNCTION = 'def link_payment_to_order(\n    *,\n    order_id: int,\n    payment_id: int,\n    amount: float | None,\n    actor_id: int | str | None,\n    note: str = "",\n    conn: sqlite3.Connection | None = None,\n) -> dict:\n    # SAFE_PAYMENT_LINK_POLICY_V1\n    #\n    # Payment is evidence of money received, not a generic button that may\n    # close an order. A link is allowed only for the same unit/service and\n    # only up to the remaining amount. PAYMENT_CONFIRMED is set o`

## `service_item_workflows`
- refs: 23
- files: Bots/handlers/service_orders_workspace.py, OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py, OSBB_Service_Orders_Foundation_v1/service_orders_core.py, migrate_service_orders_and_fulfillment.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/service_orders_core.py, phone_barrier_access_v2_payload/service_preorders_core.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, service_catalog_admin_core.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/service_orders_core.py, service_code_compatibility_payload/service_preorders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py, service_preorders_core.py
- sample: `JOIN service_item_workflows w`

## `access_role_permissions`
- refs: 22
- files: OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, access_control.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, manage_staff_access.py, manage_staff_access_v2.py, migrate_access_control_and_guard.py, migrate_service_orders_and_fulfillment.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, run_bot_live_services_sandbox_v1.py
- sample: `JOIN access_role_permissions rp`

## `resident_profile_change_requests`
- refs: 22
- files: CHECK_profile_verification_sandbox.py, profile_verification_core.py, profile_verification_payload/profile_verification_core.py, profile_verification_terminology_v2_payload/profile_verification_core.py
- sample: `print("Open correction requests:",conn.execute("SELECT COUNT(*) FROM resident_profile_change_requests WHERE request_status='PENDING_OPERATOR'").fetchone()[0])`

## `telegram_facts`
- refs: 22
- files: Bots/db_access - Copy.py, Bots/db_access.py, billing/report_parking_time_review_tasks.py, billing/report_parking_time_with_hints.py, build_plate_evidence_by_digits_and_apartment.py, build_plate_evidence_from_telegram.py, extract_telegram_remote_facts.py, extract_telegram_vehicle_facts.py
- sample: `FROM telegram_facts`

## `telegram_osbb`
- refs: 21
- files: Bots/parking_bot - Copy.py, Bots/parking_bot.py, Bots/parking_bot_before_cashier_editor_2026-06-25_14-45-08.py, Bots/parking_bot_before_client_portal_2026-06-25_10-25-49.py, Bots/parking_bot_before_language_gate_fix_2026-06-25_10-45-39.py, Bots/parking_bot_before_launch_queues_menu_2026-06-25_12-21-29.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, import_osbb_telegram_messages.py, inspect_osbb_folder_filter.py, list_osbb_folder_dialogs.py, list_osbb_included_peers.py, list_telegram_dialogs.py, list_telegram_folders.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, run_bot_live_services_sandbox_v1.py, seed_bot_admins.py, telegram_test_login.py, telegram_test_login_manual.py
- sample: `from telegram_osbb import (`

## `access_control`
- refs: 19
- files: Bots/handlers/guard_workspace.py, Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py, Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py, Bots/handlers/service_orders_workspace.py, OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py, OSBB_Service_Orders_Foundation_v1/service_orders_core.py, manage_staff_access.py, manage_staff_access_v2.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py, phone_barrier_access_v2_payload/service_orders_core.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, service_catalog_admin_core.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/service_orders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py
- sample: `from access_control import (`

## `types`
- refs: 19
- files: OSBB_Service_Orders_Foundation_v1/service_orders_preflight.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, create_clean_live_sandbox.py, create_isolated_live_sandbox_v2.py, guard_workspace_preflight.py, guard_workspace_preflight_v2.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, patch_cashier_v2_core_period_and_schemafix.py, patch_cashier_v2_core_schemafix.py, prepare_live_service_test.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, run_bot_guard_sandbox.py, run_bot_guard_sandbox_v2.py, run_bot_guard_sandbox_v3.py, run_bot_live_service_sandbox_v4.py, run_bot_live_services_sandbox_v1.py, run_bot_sandbox_v2.py, service_orders_preflight.py
- sample: `from types import ModuleType, SimpleNamespace`

## `remote_supplier_batches`
- refs: 18
- files: phone_barrier_access_v2_payload/service_preorders_core.py, service_code_compatibility_payload/service_preorders_core.py, service_preorders_core.py
- sample: `INSERT INTO remote_supplier_batches (`

## `telegram_messages`
- refs: 18
- files: Bots/db_access - Copy.py, Bots/db_access.py, audit_osbb_telegram_messages.py, extract_telegram_remote_facts.py, extract_telegram_vehicle_facts.py, import_osbb_telegram_messages.py, init_osbb_telegram_db.py
- sample: `FROM telegram_messages`

## `collections`
- refs: 16
- files: billing/import_ohorona_parking_time.py, billing/import_ohorona_parking_time_simple_preview.py, billing/import_parking_time_hints_from_ohorona.py, billing/report_parking_time_review_tasks.py, billing/report_parking_time_with_hints.py, billing_statement_excel.py, build_plate_candidates.py, migrate_unit_registry_composite_groups.py, plate_consensus_report.py, plate_consensus_report_v3.py, report_verification_tasks_enriched.py, supervisor_dashboard.py, tools/cashier_parking_payments_audit_v4.py, tools/cashier_unpaid_preview_v3.py, tools/db_schema_snapshot.py, tools/db_schema_snapshot_full.py
- sample: `from collections import defaultdict`

## `resident_profile_policy_versions`
- refs: 16
- files: CHECK_profile_verification_sandbox.py, profile_verification_core.py, profile_verification_payload/profile_verification_core.py, profile_verification_terminology_v2_payload/profile_verification_core.py
- sample: `policy=conn.execute("SELECT id,version_number,effective_from FROM resident_profile_policy_versions WHERE policy_set_code=? AND policy_status='ACTIVE' ORDER BY effective_from DESC,version_number DESC LIMIT 1",(PROFILE_POLICY_SET,)).fetchone()`

## `telethon`
- refs: 16
- files: import_osbb_telegram_messages.py, inspect_osbb_folder_filter.py, list_osbb_folder_dialogs.py, list_osbb_included_peers.py, list_telegram_dialogs.py, list_telegram_folders.py, telegram_test_login.py, telegram_test_login_manual.py
- sample: `from telethon import TelegramClient`

## `profile_parking_time_test_sessions`
- refs: 15
- files: CHECK_profile_parking_time_test_sandbox.py, parking_time_test_payload/profile_parking_time_test_core.py, profile_parking_time_test_core.py
- sample: `"SELECT COUNT(*) FROM profile_parking_time_test_sessions"`

## `phone_access_subscription_charges`
- refs: 14
- files: CHECK_phone_barrier_access_operational_sandbox.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `"SELECT COUNT(*) FROM phone_access_subscription_charges WHERE charge_kind = 'CONNECT'"`

## `phone_access_subscriptions`
- refs: 14
- files: CHECK_phone_barrier_access_operational_sandbox.py, CHECK_phone_barrier_access_sandbox_schema.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `print("Subscriptions:", cur.execute("SELECT COUNT(*) FROM phone_access_subscriptions").fetchone()[0])`

## `cashier_v2_core`
- refs: 13
- files: Bots/handlers/cashier_operator_v2.py, Bots/handlers/client_portal_v2.py, Bots/handlers/guard_workspace.py, Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py, Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py, Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py
- sample: `from cashier_v2_core import (`

## `resident_profile_policy_values`
- refs: 13
- files: CHECK_profile_verification_sandbox.py, profile_verification_core.py, profile_verification_payload/profile_verification_core.py, profile_verification_terminology_v2_payload/profile_verification_core.py
- sample: `for row in conn.execute("SELECT setting_code,value_text FROM resident_profile_policy_values WHERE policy_version_id=? ORDER BY setting_code",(int(policy[0]),)):`

## `service_preorders_core`
- refs: 13
- files: Bots/handlers/service_orders_workspace.py, MIGRATE_simplified_services_sandbox.py, cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py, parking_time_test_payload/run_bot_live_services_sandbox_v1.py, phone_barrier_access_service.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/phone_barrier_access_service.py, profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_payload/run_bot_live_services_sandbox_v1.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, run_bot_live_services_sandbox_v1.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py
- sample: `from service_preorders_core import (`

## `access_policy_versions`
- refs: 11
- files: CHECK_phone_barrier_access_sandbox_schema.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `FROM access_policy_versions`

## `phone_access_requests`
- refs: 11
- files: CHECK_phone_barrier_access_operational_sandbox.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `print("Requests:", cur.execute("SELECT COUNT(*) FROM phone_access_requests").fetchone()[0])`

## `phone_barrier_access_core`
- refs: 11
- files: Bots/handlers/service_orders_workspace.py, CHECK_phone_barrier_access_operational_sandbox.py, CHECK_phone_barrier_access_sandbox_schema.py, MIGRATE_phone_barrier_access_operational_sandbox.py, MIGRATE_phone_barrier_access_sandbox.py, phone_barrier_access_service.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/phone_barrier_access_service.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py
- sample: `from phone_barrier_access_core import BARRIER_FAR_01, BARRIER_NEAR_02`

## `service_price_versions`
- refs: 11
- files: OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py, OSBB_Service_Orders_Foundation_v1/service_orders_core.py, phone_barrier_access_v2_payload/service_orders_core.py, service_catalog_admin_core.py, service_code_compatibility_payload/service_orders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py
- sample: `FROM service_price_versions`

## `utils`
- refs: 11
- files: audit_tbot_quarantine.py, billing/report_parking_time_review_tasks.py, extract_telegram_remote_facts.py, extract_telegram_vehicle_facts.py, import_tbot_quarantine.py, normalize_registry_fields.py, report_plate_candidates.py, report_verification_evidence.py, report_verification_tasks.py, report_verification_tasks_enriched.py
- sample: `from utils import norm_text, norm_apartment`

## `a`
- refs: 10
- files: INSTALL_service_code_compatibility_phone_v2.py, phone_barrier_access_v2_payload/service_preorders_core.py, service_code_compatibility_payload/service_preorders_core.py, service_preorders_core.py
- sample: `# Guard against copying into a wrong unrelated folder.`

## `access_roles`
- refs: 10
- files: OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py, access_control.py, manage_staff_access.py, manage_staff_access_v2.py, migrate_access_control_and_guard.py, migrate_service_orders_and_fulfillment.py, prepare_live_service_test.py
- sample: `JOIN access_roles r`

## `access_schema_migrations`
- refs: 10
- files: CHECK_phone_barrier_access_operational_sandbox.py, MIGRATE_phone_barrier_access_operational_sandbox.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `"SELECT applied_at FROM access_schema_migrations WHERE migration_code = ?",`

## `profile_verification_core`
- refs: 10
- files: Bots/handlers/profile_verification_workspace.py, Bots/handlers/service_orders_workspace.py, CHECK_profile_verification_sandbox.py, MIGRATE_profile_verification_sandbox.py, profile_confirmation_button_ready_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_critical_codes_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/profile_verification_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py
- sample: `from profile_verification_core import (`

## `service_order_charge_links`
- refs: 10
- files: OSBB_Service_Orders_Foundation_v1/service_orders_core.py, phone_barrier_access_v2_payload/service_orders_core.py, service_code_compatibility_payload/service_orders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py
- sample: `INSERT INTO service_order_charge_links (`

## `access_policy_values`
- refs: 9
- files: CHECK_phone_barrier_access_sandbox_schema.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `FROM access_policy_values`

## `access_user_permissions`
- refs: 9
- files: access_control.py, manage_staff_access.py, manage_staff_access_v2.py
- sample: `FROM access_user_permissions`

## `phone_access_subscription_points`
- refs: 9
- files: CHECK_phone_barrier_access_operational_sandbox.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `print("Subscription points:", cur.execute("SELECT COUNT(*) FROM phone_access_subscription_points").fetchone()[0])`

## `service_access_credentials`
- refs: 9
- files: OSBB_Service_Orders_Foundation_v1/service_orders_core.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py, phone_barrier_access_v2_payload/service_orders_core.py, service_code_compatibility_payload/service_orders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py
- sample: `INSERT INTO service_access_credentials (`

## `staff_principals`
- refs: 9
- files: create_clean_live_sandbox.py, create_isolated_live_sandbox_v2.py, guard_workspace_preflight.py, guard_workspace_preflight_v2.py, manage_staff_access.py, manage_staff_access_v2.py, prepare_live_service_test.py
- sample: `INSERT INTO staff_principals (`

## `for`
- refs: 8
- files: CHECK_phone_barrier_access_operational_sandbox.py, CHECK_phone_barrier_access_sandbox_schema.py, CHECK_profile_test_candidate_apartment_40.py, cashier_v2_preflight.py, migrate_cashier_v2.py, run_bot_sandbox_v2.py
- sample: `return sorted(table for table in required if not table_exists(cur, table))`

## `phone_barrier_access_service`
- refs: 8
- files: Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/service_preorders_core.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/service_preorders_core.py, service_preorders_core.py
- sample: `from phone_barrier_access_service import (`

## `access_points`
- refs: 7
- files: CHECK_phone_barrier_access_sandbox_schema.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `FROM access_points`

## `access_tariff_versions`
- refs: 7
- files: CHECK_phone_barrier_access_sandbox_schema.py, phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `FROM access_tariff_versions`

## `resident_profile_schema_migrations`
- refs: 7
- files: CHECK_profile_verification_sandbox.py, profile_verification_core.py, profile_verification_payload/profile_verification_core.py, profile_verification_terminology_v2_payload/profile_verification_core.py
- sample: `marker=conn.execute("SELECT migration_code FROM resident_profile_schema_migrations WHERE migration_code=?",(PROFILE_SCHEMA_MIGRATION_CODE,)).fetchone()`

## `telegram_chats`
- refs: 7
- files: audit_osbb_telegram_messages.py, extract_telegram_remote_facts.py, extract_telegram_vehicle_facts.py, import_osbb_telegram_messages.py, init_osbb_telegram_db.py
- sample: `FROM telegram_chats`

## `dataclasses`
- refs: 6
- files: commercial_contracts.py, tools/project_passport.py, tools/project_passport_v2.py, tools/project_passport_v3_classifier.py, tools/project_passport_v4_runtime_schema_audit.py, unit_resolver.py
- sample: `from dataclasses import dataclass, asdict`

## `missing`
- refs: 6
- files: Bots/handlers/client_portal.py, Bots/handlers/client_portal_safe_linking.py, migrate_access_control_and_guard.py, migrate_cashier_v2.py, migrate_cashier_v2_compat.py
- sample: `result["error"] = "charges table missing"`

## `profile`
- refs: 6
- files: Bots/handlers/service_orders_workspace.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py
- sample: `"phone_intro": "Enter the separate phone number that needs gate access. It may differ from profile contacts. After confirmed payment, the request is automatically sent to an operator for activation.",`

## `difflib`
- refs: 5
- files: plate_consensus_report.py, plate_consensus_report_v3.py, search_vehicle_by_plate_fragment.py, vehicle_data_quality_tasks.py, vehicle_verification_tasks.py
- sample: `from difflib import SequenceMatcher`

## `possibly`
- refs: 5
- files: Bots/handlers/service_orders_workspace.py, phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py
- sample: `"""Choose the one resident-facing phone offer from possibly noisy catalog data."""`

## `profile_parking_time_test_schema_migrations`
- refs: 5
- files: CHECK_profile_parking_time_test_sandbox.py, parking_time_test_payload/profile_parking_time_test_core.py, profile_parking_time_test_core.py
- sample: `FROM profile_parking_time_test_schema_migrations`

## `resident`
- refs: 5
- files: parking_time_test_payload/profile_parking_time_test_core.py, profile_parking_time_test_core.py, profile_verification_core.py, profile_verification_payload/profile_verification_core.py, profile_verification_terminology_v2_payload/profile_verification_core.py
- sample: `This module is deliberately separate from resident profile verification.`

## `service_order_events`
- refs: 5
- files: OSBB_Service_Orders_Foundation_v1/service_orders_core.py, phone_barrier_access_v2_payload/service_orders_core.py, service_code_compatibility_payload/service_orders_core.py, service_orders_core.py, service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py
- sample: `INSERT INTO service_order_events (`

## `unit_resolver`
- refs: 5
- files: Bots/db_access.py, Bots/handlers/cashier_operator.py, cashier_v2_core.py, cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py, cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py
- sample: `from unit_resolver import resolve_unit_ref`

## `uuid`
- refs: 5
- files: Bots/handlers/cashier_operator.py, cashier_journal.py, cashier_v2_core.py, cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py, cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py
- sample: `from uuid import uuid4`

## `access_audit_log`
- refs: 4
- files: access_control.py, manage_staff_access.py, manage_staff_access_v2.py, prepare_live_service_test.py
- sample: `INSERT INTO access_audit_log (`

## `both`
- refs: 4
- files: Bots/handlers/service_orders_workspace.py, profile_verification_payload/Bots/handlers/service_orders_workspace.py, profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py, service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py
- sample: `Read offers from both supported service-item schemas.`

## `existed`
- refs: 4
- files: migrate_apartment_link_requests.py, migrate_remote_requests.py
- sample: `f"Table existed before: {existed}",`

## `not`
- refs: 4
- files: CHECK_profile_test_candidate_apartment_40.py, audit_registry.py, fix_source_ref_schema.py, vehicle_data_quality_tasks.py
- sample: `report.add(f"{table:20}: table not found")`

## `paid`
- refs: 4
- files: tools/cashier_parking_payments_audit_v4.py, tools/cashier_unpaid_preview_v3.py
- sample: `LEFT JOIN paid p ON p.charge_id = c.id`

## `phone_access_request_points`
- refs: 4
- files: phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `FROM phone_access_request_points`

## `plate_consensus_report`
- refs: 4
- files: Bots/handlers/vehicle_verification.py, plate_consensus_apply.py, plate_consensus_top6.py, supervisor_dashboard.py
- sample: `from plate_consensus_report import DEFAULT_PERIOD_CODE, build_consensus, normalize_plate`

## `profile_parking_time_test_core`
- refs: 4
- files: Bots/handlers/profile_parking_time_test_workspace.py, CHECK_profile_parking_time_test_sandbox.py, MIGRATE_profile_parking_time_test_sandbox.py, parking_time_test_payload/Bots/handlers/profile_parking_time_test_workspace.py
- sample: `from profile_parking_time_test_core import (`

## `profile_parking_time_test_events`
- refs: 4
- files: parking_time_test_payload/profile_parking_time_test_core.py, profile_parking_time_test_core.py
- sample: `INSERT INTO profile_parking_time_test_events (`

## `refs`
- refs: 4
- files: tools/project_passport.py, tools/project_passport_v2.py, tools/project_passport_v4_runtime_schema_audit.py
- sample: `# DB table refs md`

## `cashier_journal`
- refs: 3
- files: import_ohorona_list1_to_central_cashbox.py, import_ohorona_to_cashbox.py
- sample: `from cashier_journal import (`

## `contact`
- refs: 3
- files: profile_verification_core.py, profile_verification_payload/profile_verification_core.py, profile_verification_terminology_v2_payload/profile_verification_core.py
- sample: `link columns are available. Does not infer anything from contact phones.`

## `db_access`
- refs: 3
- files: Bots/handlers/cashier_operator.py, Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py
- sample: `from db_access import get_admin_record  # type: ignore`

## `decimal`
- refs: 3
- files: import_ohorona_list1_to_central_cashbox.py, import_ohorona_sheet1_payments.py, import_ohorona_to_cashbox.py
- sample: `from decimal import Decimal, InvalidOperation`

## `import`
- refs: 3
- files: billing_statement_excel.py, tools/cashier_parking_payments_audit_v4.py, tools/cashier_unpaid_preview_v3.py
- sample: `from openpyxl.worksheet.table import Table, TableStyleInfo`

## `name`
- refs: 3
- files: fix_source_ref_schema.py
- sample: `to the actual SQLite table name. Schema prefixes are not expected in OSBB.`

## `names`
- refs: 3
- files: fix_source_ref_schema.py, tools/project_passport_v4_runtime_schema_audit.py
- sample: `Locate table names assigned to alias p in the SQL statement that reads`

## `OSBB`
- refs: 3
- files: MIGRATE_simplified_services_sandbox.py, tools/db_schema_compare.py, tools/db_schema_snapshot.py
- sample: `config from the parent Python project directory, not from OSBB itself.`

## `primary`
- refs: 3
- files: profile_verification_core.py, profile_verification_payload/profile_verification_core.py, profile_verification_terminology_v2_payload/profile_verification_core.py
- sample: `# Keep external numbers human-readable; table primary keys remain authoritative.`

## `references`
- refs: 3
- files: tools/project_passport.py, tools/project_passport_v2.py, tools/project_passport_v4_runtime_schema_audit.py
- sample: `body.append(f"- DB table references: **{summary['db_table_refs']}**")`

## `remote_order_issued_assets`
- refs: 3
- files: phone_barrier_access_v2_payload/service_preorders_core.py, service_code_compatibility_payload/service_preorders_core.py, service_preorders_core.py
- sample: `INSERT INTO remote_order_issued_assets (`

## `repeated`
- refs: 3
- files: cashier_v2_core.py, cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py, cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py
- sample: `# Protect from repeated identical notice on the same day while status NEW.`

## `resident_profile_operation_journal`
- refs: 3
- files: profile_verification_core.py, profile_verification_payload/profile_verification_core.py, profile_verification_terminology_v2_payload/profile_verification_core.py
- sample: `INSERT INTO resident_profile_operation_journal (`

## `service_order_items`
- refs: 3
- files: tools/project_passport.py, tools/project_passport_v2.py, tools/project_passport_v4_runtime_schema_audit.py
- sample: `"service_order_items",`

## `source_files`
- refs: 3
- files: audit_tbot_quarantine.py, import_tbot_quarantine.py
- sample: `FROM source_files`

## `supplier`
- refs: 3
- files: phone_barrier_access_v2_payload/service_preorders_core.py, service_code_compatibility_payload/service_preorders_core.py, service_preorders_core.py
- sample: `- new remotes are paid preorders, aggregated into supplier batches;`

## `this`
- refs: 3
- files: Bots/handlers/client_portal.py, Bots/handlers/client_portal_safe_linking.py, cashier_v2_preflight.py
- sample: `# Language pack. Each submenu uses keys from this pack, not hard-coded RU.`

## `v1`
- refs: 3
- files: cashier_v2_core.py, cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py, cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py
- sample: `# Reuse battle-tested dynamic schema helpers from v1.  This does not route UI`

## `access_debt_warnings`
- refs: 2
- files: CHECK_phone_barrier_access_operational_sandbox.py, CHECK_phone_barrier_access_sandbox_schema.py
- sample: `print("Warnings:", cur.execute("SELECT COUNT(*) FROM access_debt_warnings").fetchone()[0])`

## `access_operation_journal`
- refs: 2
- files: phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `INSERT OR IGNORE INTO access_operation_journal (`

## `active`
- refs: 2
- files: OSBB_Service_Orders_Foundation_v1/service_orders_preflight.py, service_orders_preflight.py
- sample: `"retired offer hidden from active list": (`

## `aliased`
- refs: 2
- files: fix_source_ref_schema.py
- sample: `2. Finds the table aliased as "p" in the SQL that uses p.source_ref.`

## `billing_periods`
- refs: 2
- files: billing/migrate_add_parking_billing.py
- sample: `FOREIGN KEY(billing_period_id) REFERENCES billing_periods(id),`

## `commercial_contract_editor`
- refs: 2
- files: Bots/handlers/unit_registry_editor - Copy.py, Bots/handlers/unit_registry_editor.py
- sample: `from commercial_contract_editor import handle_commercial_contract_editor_text`

## `created`
- refs: 2
- files: migrate_add_verification_evidence.py, migrate_add_verification_tasks.py
- sample: `print("verification_evidence table created successfully")`

## `docx`
- refs: 2
- files: Collect_word_tables.py, Word_table_to_Excel.py
- sample: `from docx import Document`

## `G`
- refs: 2
- files: CHECK_guard_sandbox_service_orders.py, MIGRATE_simplified_services_sandbox.py
- sample: `"Put this diagnosis script directly into G:\\Programming\\Py\\OSBB\\."`

## `has`
- refs: 2
- files: Bots/handlers/vehicle_verification.py, vehicle_data_quality_tasks.py
- sample: `raise RuntimeError("vehicles table has no license plate columns")`

## `LIST`
- refs: 2
- files: tools/db_schema_snapshot.py, tools/db_schema_snapshot_full.py
- sample: `"TABLE LIST",`

## `References`
- refs: 2
- files: tools/project_passport.py, tools/project_passport_v2.py
- sample: `write_md(out_dir / "04_DB_Table_References.md", "Database Table References", "\n".join(ref_lines))`

## `using`
- refs: 2
- files: phone_barrier_access_core.py, phone_barrier_access_v2_payload/phone_barrier_access_core.py
- sample: `# That bridge prevents us from using resident_comment as an accounting record:`

## `v_commercial_contract_charge_debt`
- refs: 2
- files: commercial_contracts.py, migrate_commercial_contract_core.py
- sample: `FROM v_commercial_contract_charge_debt`

## `alloc`
- refs: 1
- files: tools/cashier_unpaid_preview.py
- sample: `LEFT JOIN alloc ON alloc.charge_id = c.id`

## `another`
- refs: 1
- files: FIND_actual_service_order_state.py
- sample: `"The earlier reprogramming workflow was therefore run from another "`

## `apartment_number`
- refs: 1
- files: FIX_live_services_sandbox_payment_schema.py
- sample: `4. Resolves apartment_id from apartment_number, first via apartments and then`

## `being`
- refs: 1
- files: patch_cashier_v2_core_schemafix.py
- sample: `# prevent a previously loaded live module from being reused`

## `bot`
- refs: 1
- files: migrate_bot_core.py
- sample: `# All critical changes from bot/operator/admin`

## `but`
- refs: 1
- files: fix_source_ref_schema.py
- sample: `f"SQLite completed ALTER TABLE but {table_name}.source_ref is still absent."`

## `calendar`
- refs: 1
- files: import_ohorona_list1_to_central_cashbox.py
- sample: `from calendar import monthrange`

## `candidate`
- refs: 1
- files: fix_source_ref_schema.py
- sample: `emit(f"Detected p.source_ref table candidate(s): {', '.join(candidates)}")`

## `code`
- refs: 1
- files: tools/project_passport_v4_runtime_schema_audit.py
- sample: `print(f"Missing tables from code: {len(missing_tables)}")`

## `commercial`
- refs: 1
- files: Bots/handlers/commercial_contract_editor.py
- sample: `# Entry from commercial unit card.`

## `commercial_notification_delivery`
- refs: 1
- files: commercial_notification_delivery.py
- sample: `from commercial_notification_delivery import deliver_ready_notifications`

## `consensus`
- refs: 1
- files: Bots/handlers/vehicle_verification.py
- sample: `comment="Operator selected correct plate from consensus tie",`

## `contacts`
- refs: 1
- files: search_vehicle_by_plate_fragment.py
- sample: `contact_join = f"LEFT JOIN contacts c ON c.{apartment_id_col} = a.id"`

## `data`
- refs: 1
- files: CHECK_profile_verification_terminology_v2.py
- sample: `print(" - confirmation is separate from data completeness")`

## `differences`
- refs: 1
- files: tools/db_schema_compare.py
- sample: `add("No structural table differences found.")`

## `e`
- refs: 1
- files: seed_bot_admins.py
- sample: `) from e`

## `error`
- refs: 1
- files: audit_tbot_quarantine.py
- sample: `report.add(f"source_files table error: {e}")`

## `from`
- refs: 1
- files: Bots/db_access.py
- sample: `# The old implementation inferred composite references from the Telegram`

## `its`
- refs: 1
- files: run_bot_sandbox_v2.py
- sample: `parking_bot.py executed from its true path, but only the patched source`

## `OHORONA`
- refs: 1
- files: import_ohorona_sheet1_payments.py
- sample: `lines.append("UNKNOWN PLATES FROM OHORONA")`

## `old`
- refs: 1
- files: Bots/handlers/client_portal_v2.py
- sample: `# A stale v2 state should not fall into old client portal text parser.`

## `osbb_test`
- refs: 1
- files: create_isolated_live_sandbox_v2.py
- sample: `"Baseline workflow counts inherited from osbb_test.db:",`

## `PAPER`
- refs: 1
- files: audit_registry.py
- sample: `report.section("APARTMENTS CREATED FROM PAPER PARKING")`

## `paper`
- refs: 1
- files: plate_consensus_apply.py
- sample: `Consensus correction updates only vehicles from paper/main DB.`

## `parking_charges`
- refs: 1
- files: billing/migrate_add_parking_billing.py
- sample: `FOREIGN KEY(parking_charge_id) REFERENCES parking_charges(id),`

## `parking_tariffs`
- refs: 1
- files: billing/migrate_add_parking_billing.py
- sample: `INSERT OR IGNORE INTO parking_tariffs`

## `PATCHED`
- refs: 1
- files: CHECK_guard_sandbox_service_orders.py
- sample: `say("  - If 'service_orders_workspace' / 'handle_service_orders_text' is absent from PATCHED source,")`

## `payment`
- refs: 1
- files: vehicle_data_quality_tasks.py
- sample: `def apply_vehicle_plate_correction(payment_id, vehicle_id, operator_id=None, comment="vehicle quality correction from payment"):`

## `plate`
- refs: 1
- files: plate_consensus_top6.py
- sample: `description="Show only unresolved Tie cases from plate consensus report."`

## `service_supplier_batch_items`
- refs: 1
- files: tools/project_passport_v4_runtime_schema_audit.py
- sample: `"service_supplier_batches", "service_supplier_batch_items",`

## `service_supplier_batches`
- refs: 1
- files: tools/project_passport_v4_runtime_schema_audit.py
- sample: `"service_supplier_batches", "service_supplier_batch_items",`

## `Sheet1`
- refs: 1
- files: import_ohorona_sheet1_payments.py
- sample: `parser = argparse.ArgumentParser(description="Import payments from Sheet1 of Охорона.xlsx.")`

## `STRUCTURAL`
- refs: 1
- files: tools/db_schema_compare.py
- sample: `add("TABLE STRUCTURAL DIFFERENCES")`

## `TBOT`
- refs: 1
- files: audit_tbot_quarantine.py
- sample: `report.section("OWNERSHIP TYPE FROM TBOT")`

## `telegram_secrets`
- refs: 1
- files: telegram_test_login.py
- sample: `# from telegram_secrets import API_ID, API_HASH, PHONE`

## `that`
- refs: 1
- files: CHECK_profile_test_candidate_apartment_40.py
- sample: `# Prefer the table that is used by existing vehicle linkage.`

## `there`
- refs: 1
- files: fix_source_ref_schema.py
- sample: `r"G:\Programming\Py\OSBB\ and run it from there."`

## `unit_registry_editor`
- refs: 1
- files: Bots/handlers/commercial_contract_editor.py
- sample: `from unit_registry_editor import show_unit_card`

## `unlinked`
- refs: 1
- files: vehicle_data_quality_tasks.py
- sample: `parser = argparse.ArgumentParser(description="Find vehicle plate quality tasks from unlinked payments.")`

## `v3`
- refs: 1
- files: install_service_orders_ui.py
- sample: `- switches the live sandbox launcher from v3 to v4;`

## `v_commercial_contract_debt_summary`
- refs: 1
- files: Bots/handlers/commercial_contract_editor.py
- sample: `FROM v_commercial_contract_debt_summary`

## `will`
- refs: 1
- files: migrate_cashier_v2_compat.py
- sample: `plan[table] = ["<table will be created>"]`
