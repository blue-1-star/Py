# OSBB Release Notes Draft

Generated: 2026-06-30 21:46:11
Git range: `5bf92ff..HEAD`

## Summary

- Commits: **4**
- Changed files: **424**
- Detected themes: access policy / debt gate, agreement / verification, bot admins / roles, cashbox / kassa, phone access, premises / non-residential, remote / pult orders, service orders, vehicles / tariffs

## Candidate release checklist

- [ ] access policy / debt gate
- [ ] agreement / verification
- [ ] bot admins / roles
- [ ] cashbox / kassa
- [ ] phone access
- [ ] premises / non-residential
- [ ] remote / pult orders
- [ ] service orders
- [ ] vehicles / tariffs

## Commit timeline

### 2026-06-26 `8a59eab` — OSBB Project  81 edit modules (bot admins / roles, cashbox / kassa, premises / non-residential, remote / pult orders)
**BOT / MENUS / HANDLERS**
- `M` OSBB/Bots/db_access.py
- `M` OSBB/Bots/handlers/audit_viewer - Copy.py
- `M` OSBB/Bots/handlers/audit_viewer.py
- `A` OSBB/Bots/handlers/cashier_operator.py
- `A` OSBB/Bots/handlers/cashier_operator_v2.py
- `A` OSBB/Bots/handlers/client_portal.py
- `A` OSBB/Bots/handlers/client_portal_safe_linking.py
- `A` OSBB/Bots/handlers/client_portal_v2.py
- `A` OSBB/Bots/handlers/commercial_contract_editor.py
- `A` OSBB/Bots/handlers/unit_registry_editor - Copy.py
- `A` OSBB/Bots/handlers/unit_registry_editor.py
- `M` OSBB/Bots/parking_bot - Copy.py
- `M` OSBB/Bots/parking_bot.py
- `A` OSBB/Bots/parking_bot_before_cashier_editor_2026-06-25_14-45-08.py
- `A` OSBB/Bots/parking_bot_before_client_portal_2026-06-25_10-25-49.py
- `A` OSBB/Bots/parking_bot_before_language_gate_fix_2026-06-25_10-45-39.py
- `A` OSBB/Bots/parking_bot_before_launch_queues_menu_2026-06-25_12-21-29.py
- `A` OSBB/fix_parking_bot_language_gate.py
- `A` OSBB/patch_parking_bot_cashier_operator.py
- `A` OSBB/patch_parking_bot_client_cabinet.py
- `A` OSBB/patch_parking_bot_client_portal.py
- `A` OSBB/patch_parking_bot_launch_queues_menu.py
- `A` OSBB/run_bot_sandbox_v2.py
- `A` OSBB/switch_parking_bot_to_cashier_v2.py
**DATABASE / MIGRATIONS**
- `A` OSBB/Data/db/osbb_test - Copy.db
- `M` OSBB/Data/db/osbb_test.db
- `A` OSBB/Data/db/sandbox/cashier_v2_preflight_2026-06-25_18-53-50.txt
- `A` OSBB/Data/db/sandbox/cashier_v2_preflight_compat_2026-06-25_19-47-09.txt
- `A` OSBB/Data/db/sandbox/osbb_test_cashier_v2_check_2026-06-25_18-53-50.db
- `A` OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db
- `A` OSBB/Data/exports/cashier/cashier_operator_migration_2026-06-25_14-43-23.txt
- `A` OSBB/Data/exports/cashier/cashier_operator_migration_2026-06-25_14-43-41.txt
- `A` OSBB/Data/exports/cashier/cashier_v2_migration_2026-06-25_17-56-05.txt
- `A` OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_10-23-49.txt
- `A` OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_10-24-18.txt
- `A` OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_11-42-17.txt
- `A` OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_12-05-57.txt
- `A` OSBB/Data/exports/users/apartment_link_requests_migration_2026-06-25_11-42-33.txt
- `A` OSBB/Data/exports/users/apartment_link_requests_migration_2026-06-25_12-07-06.txt
- `A` OSBB/cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py
- `A` OSBB/cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py
- `A` OSBB/migrate_apartment_link_requests.py
- `A` OSBB/migrate_cashier_operator_editor.py
- `A` OSBB/migrate_cashier_v2.py
- `A` OSBB/migrate_cashier_v2_compat.py
- `A` OSBB/migrate_commercial_contract_core.py
- `A` OSBB/migrate_remote_requests.py
- `A` OSBB/migrate_unit_registry_composite_groups.py
- `A` OSBB/patch_cashier_v2_core_period_and_schemafix.py
- `A` OSBB/patch_cashier_v2_core_schemafix.py
**DOCS / EXPORTS**
- `M` .claude/cloude-code-toolbox-mcp-skills-awareness.md
- `M` CLAUDE.md
- `A` OSBB/Data/exports/commercial/commercial_contract_core_2026-06-24_12-27-30.txt
- `A` OSBB/Data/exports/commercial/commercial_contract_core_2026-06-24_12-30-30.txt
- `A` OSBB/Data/exports/commercial/commercial_notification_queue_2026-06-24_dry_run_2026-06-24_12-32-13.txt
- `A` OSBB/Data/exports/units/commercial_unit_placeholders_2026-06-24_10-48-47.txt
- `A` OSBB/Data/exports/units/commercial_unit_placeholders_2026-06-24_10-49-12.txt
- `A` OSBB/Data/exports/units/composite_unit_inventory_2026-06-23_17-20-07.txt
- `A` OSBB/Data/exports/units/unit_registry_aliases_2026-06-23_16-09-28.txt
- `A` OSBB/Data/exports/units/unit_registry_composite_groups_2026-06-23_17-36-23.txt
- `A` OSBB/Data/exports/units/unit_registry_composite_groups_2026-06-23_17-40-54.txt
- `A` OSBB/Data/exports/users/restore_resident_link_2026-06-25_12-51-41.txt
- `A` OSBB/Data/exports/users/restore_resident_link_2026-06-25_12-52-09.txt
- `A` OSBB/Docs/non_residential_unit_draft_template.xlsx
**OTHER**
- `A` OSBB/Data/exports/units/composite_unit_inventory_2026-06-23_17-20-07.csv
- `D` "OSBB/Data/raw/typed/~$\320\236\321\205\320\276\321\200\320\276\320\275\320\260.xlsx"
- `A` OSBB/commercial_contracts.py
- `A` OSBB/commercial_notification_delivery.py
- `A` OSBB/diagnose_osbb_audit.py
- `A` OSBB/repair_confirmed_unit_seed_notes.py
- `A` OSBB/restore_resident_apartment_link.py
- `A` OSBB/seed_commercial_unit_placeholders.py
- `A` OSBB/unit_resolver.py
**SERVICES / BUSINESS LOGIC**
- `A` OSBB/Data/exports/cashier/ohorona_list1_central_apply_2026-06-22_22-53-00.txt
- `A` OSBB/cashier_v2_core.py
- `A` OSBB/cashier_v2_preflight.py
- `A` OSBB/cashier_v2_preflight_compat.py
- `A` OSBB/diagnose_sandbox_charges.py
**TOOLS / INSPECTION / ACCEPTANCE**
- `A` OSBB/Data/exports/audits/registry_audit_2026-06-23_17-18-21.txt
- `A` OSBB/Data/exports/diagnostics/audit_diagnostic_2026-06-24_20-17-19.txt
- `A` OSBB/test_db_access_unit_resolver.py

### 2026-06-26 `19f39f4` — Remouts? Cashbox? Kassa O (bot admins / roles, cashbox / kassa, service orders)
**BOT / MENUS / HANDLERS**
- `A` OSBB/Bots/Start_OSBB_Guard_Sandbox_Bot.bat
- `A` OSBB/Bots/Start_OSBB_Guard_Sandbox_Bot_v2.bat
- `A` OSBB/Bots/handlers/guard_workspace.py
- `A` OSBB/Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py
- `A` OSBB/Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py
- `A` OSBB/patch_parking_bot_guard_workspace_v2.py
- `A` OSBB/patch_parking_bot_guard_workspace_v3.py
- `A` OSBB/patch_parking_bot_guard_workspace_v4.py
- `A` OSBB/run_bot_guard_sandbox.py
- `A` OSBB/run_bot_guard_sandbox_v2.py
- `A` OSBB/run_bot_guard_sandbox_v3.py
**DATABASE / MIGRATIONS**
- `A` OSBB/Data/db/sandbox/clean_live_sandbox_2026-06-26_20-13-26.txt
- `A` OSBB/Data/db/sandbox/guard_workspace_preflight_2026-06-26_12-39-50.txt
- `A` OSBB/Data/db/sandbox/guard_workspace_preflight_2026-06-26_12-56-09.txt
- `A` OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-39-50.db
- `A` OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09.db
- `A` OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09_service_orders_check_2026-06-26_19-42-50.db
- `A` OSBB/Data/db/sandbox/osbb_test_live_services_2026-06-26_20-13-26.db
- `A` OSBB/Data/db/sandbox/service_orders_preflight_2026-06-26_19-42-50.txt
- `A` OSBB/OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py
- `A` OSBB/migrate_access_control_and_guard.py
- `A` OSBB/migrate_service_orders_and_fulfillment.py
**OTHER**
- `A` OSBB/access_control.py
- `A` OSBB/create_clean_live_sandbox.py
- `A` OSBB/create_isolated_live_sandbox_v2.py
- `A` OSBB/find_sandbox_telegram_id.py
- `A` OSBB/guard_workspace_preflight.py
- `A` OSBB/guard_workspace_preflight_v2.py
- `A` OSBB/manage_staff_access.py
- `A` OSBB/manage_staff_access_v2.py
- `A` OSBB/test.py
**SERVICES / BUSINESS LOGIC**
- `A` OSBB/OSBB_Service_Orders_Foundation_v1.zip
- `A` OSBB/OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py
- `A` OSBB/OSBB_Service_Orders_Foundation_v1/service_orders_core.py
- `A` OSBB/OSBB_Service_Orders_Foundation_v1/service_orders_preflight.py
- `A` OSBB/Start_OSBB_Live_Service_Sandbox_Bot.bat
- `A` OSBB/patch_guard_workspace_default_cash_note.py
- `A` OSBB/service_catalog_admin_core.py
- `A` OSBB/service_orders_core.py
- `A` OSBB/service_orders_preflight.py
**TOOLS / INSPECTION / ACCEPTANCE**
- `A` OSBB/patch_guard_workspace_direct_notice_confirm.py

### 2026-06-28 `e7d857d` — 27.06.2026 - коммит всех дневных изменений (access policy / debt gate, agreement / verification, bot admins / roles, cashbox / kassa, phone access, remote / pult orders, service orders)
**BOT / MENUS / HANDLERS**
- `A` OSBB/Bots/handlers/client_portal_v3.py
- `A` OSBB/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/Bots/handlers/service_orders_workspace.py
- `A` OSBB/Bots/handlers/service_orders_workspace.py.before_phone_access_ui_fix_2026-06-27_16-47-09
- `A` OSBB/Bots/handlers/service_orders_workspace.py.before_phone_access_ui_fix_2026-06-27_16-52-29
- `A` OSBB/Bots/handlers/service_orders_workspace.py.before_phone_access_ui_fix_v3_2026-06-27_17-22-40
- `A` OSBB/Data/backups/source_code/cashier_route_repair_2026-06-27_20-04-49/run_bot_live_services_sandbox_v1.py
- `A` OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/Bots/handlers/service_orders_workspace.py
- `A` OSBB/Data/backups/source_code/profile_button_early_route_2026-06-27_21-33-50/run_bot_live_services_sandbox_v1.py
- `A` OSBB/Data/backups/source_code/profile_verification_2026-06-27_20-51-33/Bots/handlers/service_orders_workspace.py
- `A` OSBB/Data/backups/source_code/profile_verification_2026-06-27_20-51-33/run_bot_live_services_sandbox_v1.py
- `A` OSBB/Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/Bots/handlers/service_orders_workspace.py
- `A` OSBB/Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/Bots/handlers/service_orders_workspace.py
- `A` OSBB/Start_OSBB_Guard_Sandbox_Bot_v2.bat
- `A` OSBB/Start_OSBB_Live_Service_Sandbox_Bot_before_service_ui_2026-06-26_20-50-39.bat
- `A` OSBB/Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
- `A` OSBB/cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py
- `A` OSBB/patch_parking_bot_service_orders_ui_v1.py
- `A` OSBB/patch_parking_bot_service_orders_v1.py
- `A` OSBB/phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py
- `A` OSBB/profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py
- `A` OSBB/profile_confirmation_button_ready_payload/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/profile_verification_critical_codes_payload/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/profile_verification_payload/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/profile_verification_payload/Bots/handlers/service_orders_workspace.py
- `A` OSBB/profile_verification_payload/run_bot_live_services_sandbox_v1.py
- `A` OSBB/profile_verification_terminology_v2_payload/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py
- `A` OSBB/run_bot_live_service_sandbox_v4.py
- `A` OSBB/run_bot_live_services_sandbox_v1.py
- `A` OSBB/service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py
**DATABASE / MIGRATIONS**
- `A` OSBB/CHECK_phone_barrier_access_sandbox_schema.py
- `A` OSBB/Data/db/logs/actual_service_order_state_20260627_115724.txt
- `A` OSBB/Data/db/logs/guard_sandbox_service_orders_diagnosis_20260627_114522.txt
- `A` OSBB/Data/db/logs/guard_sandbox_service_orders_diagnosis_20260627_114911.txt
- `A` OSBB/Data/db/logs/guard_sandbox_service_orders_diagnosis_v2_20260627_115123.txt
- `A` OSBB/Data/db/logs/live_services_payment_schema_fix_20260627_122549.txt
- `A` OSBB/Data/db/logs/phone_barrier_access_operational_migration_2026-06-27_19-38-08.txt
- `A` OSBB/Data/db/logs/phone_barrier_access_schema_migration_2026-06-27_19-16-27.txt
- `A` OSBB/Data/db/logs/profile_verification_migration_2026-06-27_20-52-07.txt
- `A` OSBB/Data/db/logs/simplified_services_migration_2026-06-27_14-10-45.txt
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_payment_schema_fix_20260627_122548.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_phone_barrier_access_operational_2026-06-27_19-38-08.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_phone_barrier_access_schema_2026-06-27_19-16-27.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_profile_verification_2026-06-27_20-52-07.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_retire_legacy_new_remote_tests_2026-06-27_13-31-55.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_service_operator_permissions_2026-06-27_12-18-22.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_simplified_service_permissions_2026-06-27_16-08-06.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_simplified_services_2026-06-27_13-32-32.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_simplified_services_2026-06-27_14-10-45.db
- `M` OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09.db
- `M` OSBB/Data/db/sandbox/osbb_test_live_services_2026-06-26_20-13-26.db
- `A` OSBB/FIX_live_services_sandbox_payment_schema.py
- `A` OSBB/MIGRATE_phone_barrier_access_operational_sandbox.py
- `A` OSBB/MIGRATE_phone_barrier_access_sandbox.py
- `A` OSBB/MIGRATE_profile_verification_sandbox.py
- `A` OSBB/MIGRATE_simplified_services_sandbox.py
- `A` OSBB/OSBB_phone_barrier_access_schema_migration.zip
- `A` OSBB/README_PHONE_BARRIER_ACCESS_SCHEMA_MIGRATION.txt
- `A` OSBB/RUN_CHECK_phone_barrier_access_sandbox_schema.bat
- `A` OSBB/RUN_FIX_live_services_sandbox_payment_schema.bat
- `A` OSBB/RUN_MIGRATE_phone_barrier_access_operational_sandbox.bat
- `A` OSBB/RUN_MIGRATE_phone_barrier_access_sandbox.bat
- `A` OSBB/RUN_MIGRATE_profile_verification_sandbox.bat
- `A` OSBB/RUN_MIGRATE_simplified_services_sandbox.bat
- `A` OSBB/RUN_fix_source_ref_schema.bat
- `A` OSBB/fix_source_ref_schema.py
**DOCS / EXPORTS**
- `M` .claude/cloude-code-toolbox-mcp-skills-awareness.md
- `M` CLAUDE.md
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27.zip
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/DO_NOT_UPLOAD_SECRETS.md
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/OSBB_BUSINESS_HANDOFF_2026-06-27.md
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/OSBB_PROJECT_INSTRUCTIONS.md
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/SHA256SUMS.txt
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/START_OSBB_BUSINESS_CHAT_2026-06-28.txt
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/TRANSFER_CHECKLIST_2026-06-27.txt
- `A` OSBB/README_LIVE_SERVICES_SANDBOX.txt
- `A` OSBB/README_PROFILE_BUTTON_EARLY_ROUTE_FIX.txt
- `A` OSBB/README_PROFILE_CONFIRMATION_READY_VISIBILITY_FIX.txt
- `A` OSBB/README_PROFILE_CRITICAL_CODES_FIX.txt
- `A` OSBB/README_PROFILE_VERIFICATION_TERMINOLOGY_V2.txt
- `A` OSBB/README_PROFILE_VERIFICATION_V1.txt
- `A` OSBB/README_SIMPLIFIED_SERVICES.txt
**OTHER**
- `A` OSBB/CHECK_profile_button_early_route_fix.py
- `A` OSBB/CHECK_profile_confirmation_ready_visibility_fix.py
- `A` OSBB/CHECK_profile_critical_codes_fix.py
- `A` OSBB/CHECK_profile_verification_sandbox.py
- `A` OSBB/CHECK_profile_verification_terminology_v2.py
- `A` OSBB/Data/backups/source_code/profile_confirmation_ready_visibility_2026-06-27_21-55-54/profile_verification_workspace.py
- `A` OSBB/Data/backups/source_code/profile_critical_codes_fix_2026-06-27_21-47-24/profile_verification_workspace.py
- `A` OSBB/Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/profile_verification_core.py
- `A` OSBB/INSTALL_profile_button_early_route_fix.py
- `A` OSBB/INSTALL_profile_confirmation_ready_visibility_fix.py
- `A` OSBB/INSTALL_profile_critical_codes_fix.py
- `A` OSBB/INSTALL_profile_verification_terminology_v2.py
- `A` OSBB/INSTALL_profile_verification_v1.py
- `A` OSBB/OSBB_profile_button_early_route_fix_v2.zip
- `A` OSBB/OSBB_profile_confirmation_ready_visibility_fix.zip
- `A` OSBB/OSBB_profile_verification_terminology_v2 (1).zip
- `A` OSBB/OSBB_profile_verification_v1_sandbox_final.zip
- `A` OSBB/OSBB_simplified_services_preorders_bundle.zip
- `A` OSBB/RUN_CHECK_profile_button_early_route_fix.bat
- `A` OSBB/RUN_CHECK_profile_confirmation_ready_visibility_fix.bat
- `A` OSBB/RUN_CHECK_profile_critical_codes_fix.bat
- `A` OSBB/RUN_CHECK_profile_verification_sandbox.bat
- `A` OSBB/RUN_CHECK_profile_verification_terminology_v2.bat
- `A` OSBB/RUN_INSTALL_profile_button_early_route_fix.bat
- `A` OSBB/RUN_INSTALL_profile_confirmation_ready_visibility_fix.bat
- `A` OSBB/RUN_INSTALL_profile_critical_codes_fix.bat
- `A` OSBB/RUN_INSTALL_profile_verification_terminology_v2.bat
- `A` OSBB/RUN_INSTALL_profile_verification_v1.bat
- `A` OSBB/STOP_old_guard_sandbox_bots.bat
- `A` OSBB/profile_verification_core.py
- `A` OSBB/profile_verification_payload/profile_verification_core.py
- `A` OSBB/profile_verification_terminology_v2_payload/profile_verification_core.py
**SERVICES / BUSINESS LOGIC**
- `A` OSBB/CHECK_guard_sandbox_service_orders.py
- `A` OSBB/CHECK_guard_sandbox_service_orders_v2.py
- `A` OSBB/CHECK_phone_barrier_access_operational_sandbox.py
- `A` OSBB/CHECK_service_code_compatibility_phone_v2.py
- `A` OSBB/CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.bat
- `A` OSBB/CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.py
- `A` OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/phone_barrier_access_core.py
- `A` OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/service_orders_core.py
- `A` OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/service_preorders_core.py
- `A` OSBB/Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/service_orders_core.py
- `A` OSBB/Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/service_preorders_core.py
- `A` OSBB/FIND_actual_service_order_state.py
- `A` OSBB/INSTALL_PHONE_ACCESS_UI_FIX.bat
- `A` OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v2.bat
- `A` OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v2.py
- `A` OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v3.bat
- `A` OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v3.py
- `A` OSBB/INSTALL_cashier_route_after_phone_v2.py
- `A` OSBB/INSTALL_phone_barrier_access_v2.py
- `A` OSBB/INSTALL_service_code_compatibility_phone_v2.py
- `A` OSBB/OSBB_cashier_route_fix.zip
- `A` OSBB/OSBB_cashier_route_repair_after_phone_v2.zip
- `A` OSBB/OSBB_phone_access_ui_fix.zip
- `A` OSBB/OSBB_phone_access_ui_fix_v3.zip
- `A` OSBB/OSBB_phone_barrier_access_v2_working_sandbox.zip
- `A` OSBB/OSBB_service_code_compatibility_repair_phone_v2.zip
- `A` OSBB/README_CASHIER_ROUTE_FIX.txt
- `A` OSBB/README_CASHIER_ROUTE_REPAIR_AFTER_PHONE_V2.txt
- `A` OSBB/README_LIVE_SERVICE_UI.txt
- `A` OSBB/README_PHONE_ACCESS_FIX.txt
- `A` OSBB/README_PHONE_ACCESS_FIX_v2.txt
- `A` OSBB/README_PHONE_ACCESS_FIX_v3.txt
- `A` OSBB/README_PHONE_BARRIER_ACCESS_V2.txt
- `A` OSBB/README_SERVICE_CODE_COMPATIBILITY_PHONE_V2.txt
- `A` OSBB/RETIRE_legacy_new_remote_test_orders_sandbox.py
- `A` OSBB/RUN_CHECK_cashier_route_after_phone_v2.bat
- `A` OSBB/RUN_CHECK_guard_sandbox_service_orders.bat
- `A` OSBB/RUN_CHECK_guard_sandbox_service_orders_v2.bat
- `A` OSBB/RUN_CHECK_phone_barrier_access_operational_sandbox.bat
- `A` OSBB/RUN_CHECK_service_code_compatibility_phone_v2.bat
- `A` OSBB/RUN_FIND_actual_service_order_state.bat
- `A` OSBB/RUN_INSTALL_cashier_route_after_phone_v2.bat
- `A` OSBB/RUN_INSTALL_phone_barrier_access_v2.bat
- `A` OSBB/RUN_INSTALL_service_code_compatibility_phone_v2.bat
- `A` OSBB/RUN_RETIRE_legacy_new_remote_test_orders_sandbox.bat
- `M` OSBB/Start_OSBB_Live_Service_Sandbox_Bot.bat
- `A` OSBB/install_service_orders_ui.py
- `A` OSBB/phone_barrier_access_core.py
- `A` OSBB/phone_barrier_access_service.py
- `A` OSBB/phone_barrier_access_v2_payload/phone_barrier_access_core.py
- `A` OSBB/phone_barrier_access_v2_payload/phone_barrier_access_service.py
- `A` OSBB/phone_barrier_access_v2_payload/service_orders_core.py
- `A` OSBB/phone_barrier_access_v2_payload/service_preorders_core.py
- `A` OSBB/prepare_live_service_test.py
- `A` OSBB/service_code_compatibility_payload/service_orders_core.py
- `A` OSBB/service_code_compatibility_payload/service_preorders_core.py
- `M` OSBB/service_orders_core.py
- `A` OSBB/service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py
- `A` OSBB/service_preorders_core.py
**TOOLS / INSPECTION / ACCEPTANCE**
- `A` OSBB/CHECK_profile_test_candidate_apartment_40.py
- `A` OSBB/OSBB_apartment_40_profile_test_preflight.zip
- `A` OSBB/README_APARTMENT_40_PROFILE_TEST_PREFLIGHT.txt
- `A` OSBB/RUN_CHECK_profile_test_candidate_apartment_40.bat

### 2026-06-29 `ab23af5` — GPT Bisiness first day (access policy / debt gate, cashbox / kassa, premises / non-residential, remote / pult orders, vehicles / tariffs)
**BOT / MENUS / HANDLERS**
- `M` OSBB/Bots/handlers/client_portal.py
- `M` OSBB/Bots/handlers/guard_workspace.py
- `A` OSBB/Bots/handlers/profile_parking_time_test_workspace.py
- `A` OSBB/Data/backups/source_code/parking_time_test_v1_2026-06-28_12-12-01/run_bot_live_services_sandbox_v1.py
- `A` OSBB/Data/backups/source_patches/remote_debt_gate_v1_2026-06-28_17-41-41/Bots/handlers/client_portal.py
- `A` OSBB/Data/backups/source_patches/remote_debt_gate_v1_2026-06-28_17-41-41/Bots/handlers/guard_workspace.py
- `A` OSBB/parking_time_test_payload/Bots/handlers/profile_parking_time_test_workspace.py
- `A` OSBB/parking_time_test_payload/run_bot_live_services_sandbox_v1.py
- `M` OSBB/run_bot_live_services_sandbox_v1.py
**DATABASE / MIGRATIONS**
- `A` OSBB/Data/db/backups/osbb_test_before_remote_debt_gate_fixture_2026-06-28_18-32-29.db
- `A` OSBB/Data/db/logs/profile_parking_time_test_migration_2026-06-28_12-12-37.txt
- `M` OSBB/Data/db/osbb_test.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_profile_parking_time_test_2026-06-28_12-12-37.db
- `M` OSBB/Data/db/sandbox/osbb_test_live_services_2026-06-26_20-13-26.db
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/00_Project.md
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/01_File_System.md
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/02_Modules.md
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/03_Technical_Debt.md
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/04_DB_Table_References.md
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/classes.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/db_table_refs.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/files.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/functions.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/imports.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/modules.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/todos.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/summary.json
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/00_Project.md
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/01_File_System.md
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/02_Modules.md
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/03_Technical_Debt.md
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/04_DB_Table_References.md
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/classes.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/db_table_refs.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/files.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/functions.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/imports.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/modules.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/todos.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/summary.json
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/00_Project_v3.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/05_Entrypoints.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/06_Active_Candidates.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/07_Legacy_Backups.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/08_Bot_Handlers.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/09_Remote_Access_Service_Modules.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/10_Code_Risk_Summary.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/entrypoints.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/files_classified.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/functions.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/import_edges.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/python_modules_classified.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/summary.json
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/00_Runtime_Schema_Audit.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/01_Strict_Entrypoints.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/02_Runtime_Import_Closure.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/03_Missing_Tables_From_Code.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/04_Remote_Access_Modules.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/05_Debt_Gate_Candidates.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/db_table_refs.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/debt_gate_candidates.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/missing_tables_from_code.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/remote_access_modules.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/runtime_import_edges.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/runtime_import_nodes.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/strict_entrypoints.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/summary.json
- `A` OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/00_Remote_Debt_Gate_Audit.md
- `A` OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/inventory/candidate_lines.csv
- ... 31 more
**DOCS / EXPORTS**
- `M` .claude/cloude-code-toolbox-mcp-skills-awareness.md
- `M` CLAUDE.md
- `A` OSBB/Data/exports/code/code_search_2026-06-28_15-20-58.txt
**SERVICES / BUSINESS LOGIC**
- `A` OSBB/Data/exports/cashier/cashier_payments_audit_2026-05_2026-06_2026-06-28_15-01-16.csv
- `A` OSBB/Data/exports/cashier/cashier_payments_audit_2026-05_2026-06_2026-06-28_15-01-16.txt
- `A` OSBB/Data/exports/cashier/cashier_payments_audit_2026-05_2026-06_2026-06-28_15-01-16.xlsx
- `A` OSBB/Data/exports/cashier/cashier_unpaid_2026-05_2026-06_2026-06-28_14-46-09.csv
- `A` OSBB/Data/exports/cashier/cashier_unpaid_2026-05_2026-06_2026-06-28_14-46-09.txt
- `A` OSBB/Data/exports/cashier/cashier_unpaid_2026-05_2026-06_2026-06-28_14-46-09.xlsx
- `A` OSBB/Data/exports/debt_policy/debt_policy_matrix_preview_2026-06-28_20-23-44.csv
- `A` OSBB/Data/exports/debt_policy/debt_policy_matrix_preview_2026-06-28_20-23-44.txt
- `A` OSBB/Data/exports/debt_policy/service_codes_live_sandbox.txt
- `A` OSBB/Docs/Architecture/Services/service_catalog_v2_design.md
- `A` OSBB/Docs/Architecture/Services/service_catalog_v2_design_approved_updates.md
- `A` OSBB/tools/INSTALL_remote_debt_gate_v1.py
- `A` OSBB/tools/cashier_parking_payments_audit_v4.py
- `A` OSBB/tools/cashier_unpaid_preview.py
- `A` OSBB/tools/cashier_unpaid_preview_v2.py
- `A` OSBB/tools/cashier_unpaid_preview_v3.py
- `A` OSBB/tools/debt_policy_matrix_preview.py
- `A` OSBB/tools/dump_service_codes_live_sandbox.py
- `A` OSBB/tools/extract_remote_gate_sources.py
- `A` OSBB/tools/remote_debt_gate_audit.py
- `A` OSBB/tools/remote_debt_gate_test_fixture.py
**TOOLS / INSPECTION / ACCEPTANCE**
- `A` OSBB/CHECK_profile_parking_time_test_sandbox.py
- `A` OSBB/INSTALL_profile_parking_time_test_v1.py
- `A` OSBB/OSBB_profile_parking_time_test_v1_sandbox.zip
- `A` OSBB/README_PROFILE_PARKING_TIME_TEST_V1.txt
- `A` OSBB/RUN_CHECK_profile_parking_time_test_sandbox.bat
- `A` OSBB/RUN_INSTALL_profile_parking_time_test_v1.bat
- `A` OSBB/parking_time_test_payload/profile_parking_time_test_core.py
- `A` OSBB/profile_parking_time_test_core.py
- `A` OSBB/tools/project_code_search.py
- `A` OSBB/tools/show_running_osbb_bots.py
- `A` OSBB/tools/start_live_services_bot.py
- `A` OSBB/tools/stop_live_services_bot.py

## Changed files by category

### DATABASE / MIGRATIONS
- `A` OSBB/CHECK_phone_barrier_access_sandbox_schema.py
- `A` OSBB/Data/db/backups/osbb_test_before_remote_debt_gate_fixture_2026-06-28_18-32-29.db
- `A` OSBB/Data/db/logs/actual_service_order_state_20260627_115724.txt
- `A` OSBB/Data/db/logs/guard_sandbox_service_orders_diagnosis_20260627_114522.txt
- `A` OSBB/Data/db/logs/guard_sandbox_service_orders_diagnosis_20260627_114911.txt
- `A` OSBB/Data/db/logs/guard_sandbox_service_orders_diagnosis_v2_20260627_115123.txt
- `A` OSBB/Data/db/logs/live_services_payment_schema_fix_20260627_122549.txt
- `A` OSBB/Data/db/logs/phone_barrier_access_operational_migration_2026-06-27_19-38-08.txt
- `A` OSBB/Data/db/logs/phone_barrier_access_schema_migration_2026-06-27_19-16-27.txt
- `A` OSBB/Data/db/logs/profile_parking_time_test_migration_2026-06-28_12-12-37.txt
- `A` OSBB/Data/db/logs/profile_verification_migration_2026-06-27_20-52-07.txt
- `A` OSBB/Data/db/logs/simplified_services_migration_2026-06-27_14-10-45.txt
- `A` OSBB/Data/db/osbb_test - Copy.db
- `M` OSBB/Data/db/osbb_test.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_payment_schema_fix_20260627_122548.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_phone_barrier_access_operational_2026-06-27_19-38-08.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_phone_barrier_access_schema_2026-06-27_19-16-27.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_profile_parking_time_test_2026-06-28_12-12-37.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_profile_verification_2026-06-27_20-52-07.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_retire_legacy_new_remote_tests_2026-06-27_13-31-55.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_service_operator_permissions_2026-06-27_12-18-22.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_simplified_service_permissions_2026-06-27_16-08-06.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_simplified_services_2026-06-27_13-32-32.db
- `A` OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_simplified_services_2026-06-27_14-10-45.db
- `A` OSBB/Data/db/sandbox/cashier_v2_preflight_2026-06-25_18-53-50.txt
- `A` OSBB/Data/db/sandbox/cashier_v2_preflight_compat_2026-06-25_19-47-09.txt
- `A` OSBB/Data/db/sandbox/clean_live_sandbox_2026-06-26_20-13-26.txt
- `A` OSBB/Data/db/sandbox/guard_workspace_preflight_2026-06-26_12-39-50.txt
- `A` OSBB/Data/db/sandbox/guard_workspace_preflight_2026-06-26_12-56-09.txt
- `A` OSBB/Data/db/sandbox/osbb_test_cashier_v2_check_2026-06-25_18-53-50.db
- `A` OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db
- `A` OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-39-50.db
- `A` OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09.db
- `A` OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09_service_orders_check_2026-06-26_19-42-50.db
- `A` OSBB/Data/db/sandbox/osbb_test_live_services_2026-06-26_20-13-26.db
- `A` OSBB/Data/db/sandbox/service_orders_preflight_2026-06-26_19-42-50.txt
- `A` OSBB/Data/exports/cashier/cashier_operator_migration_2026-06-25_14-43-23.txt
- `A` OSBB/Data/exports/cashier/cashier_operator_migration_2026-06-25_14-43-41.txt
- `A` OSBB/Data/exports/cashier/cashier_v2_migration_2026-06-25_17-56-05.txt
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/00_Project.md
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/01_File_System.md
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/02_Modules.md
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/03_Technical_Debt.md
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/04_DB_Table_References.md
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/classes.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/db_table_refs.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/files.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/functions.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/imports.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/modules.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/todos.csv
- `A` OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/summary.json
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/00_Project.md
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/01_File_System.md
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/02_Modules.md
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/03_Technical_Debt.md
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/04_DB_Table_References.md
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/classes.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/db_table_refs.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/files.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/functions.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/imports.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/modules.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/todos.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/summary.json
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/00_Project_v3.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/05_Entrypoints.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/06_Active_Candidates.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/07_Legacy_Backups.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/08_Bot_Handlers.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/09_Remote_Access_Service_Modules.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/10_Code_Risk_Summary.md
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/entrypoints.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/files_classified.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/functions.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/import_edges.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/python_modules_classified.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/summary.json
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/00_Runtime_Schema_Audit.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/01_Strict_Entrypoints.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/02_Runtime_Import_Closure.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/03_Missing_Tables_From_Code.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/04_Remote_Access_Modules.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/05_Debt_Gate_Candidates.md
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/db_table_refs.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/debt_gate_candidates.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/missing_tables_from_code.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/remote_access_modules.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/runtime_import_edges.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/runtime_import_nodes.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/strict_entrypoints.csv
- `A` OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/summary.json
- `A` OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/00_Remote_Debt_Gate_Audit.md
- `A` OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/inventory/candidate_lines.csv
- `A` OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/inventory/db_status.csv
- `A` OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/inventory/files_scanned.csv
- `A` OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/inventory/functions_remote_debt_scan.csv
- `A` OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/summary.json
- `A` OSBB/Data/exports/code_passport/remote_gate_sources_2026-06-28_16-59-59.txt
- `A` OSBB/Data/exports/code_passport/running_bots_after_start.txt
- `A` OSBB/Data/exports/code_passport/running_bots_now.txt
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/01_schema.txt
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/02_columns.csv
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/03_indexes.csv
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/04_foreign_keys.csv
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/05_code_references.csv
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/06_service_code_usage.csv
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/07_sample_rows.csv
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/08_distinct_values.txt
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/09_code_references_by_kind.txt
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/10_architecture_notes.md
- `A` OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/passport_summary.txt
- `A` OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_10-23-49.txt
- `A` OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_10-24-18.txt
- `A` OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_11-42-17.txt
- `A` OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_12-05-57.txt
- `A` OSBB/Data/exports/schema/schema_compare_2026-06-28_13-09-32.txt
- `A` OSBB/Data/exports/schema/schema_snapshot_test_2026-06-28_14-30-02.txt
- `A` OSBB/Data/exports/users/apartment_link_requests_migration_2026-06-25_11-42-33.txt
- `A` OSBB/Data/exports/users/apartment_link_requests_migration_2026-06-25_12-07-06.txt
- `A` OSBB/FIX_live_services_sandbox_payment_schema.py
- `A` OSBB/MIGRATE_phone_barrier_access_operational_sandbox.py
- `A` OSBB/MIGRATE_phone_barrier_access_sandbox.py
- `A` OSBB/MIGRATE_profile_parking_time_test_sandbox.py
- `A` OSBB/MIGRATE_profile_verification_sandbox.py
- `A` OSBB/MIGRATE_simplified_services_sandbox.py
- `A` OSBB/OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py
- `A` OSBB/OSBB_phone_barrier_access_schema_migration.zip
- `A` OSBB/README_PHONE_BARRIER_ACCESS_SCHEMA_MIGRATION.txt
- `A` OSBB/RUN_CHECK_phone_barrier_access_sandbox_schema.bat
- `A` OSBB/RUN_FIX_live_services_sandbox_payment_schema.bat
- `A` OSBB/RUN_MIGRATE_phone_barrier_access_operational_sandbox.bat
- `A` OSBB/RUN_MIGRATE_phone_barrier_access_sandbox.bat
- `A` OSBB/RUN_MIGRATE_profile_parking_time_test_sandbox.bat
- `A` OSBB/RUN_MIGRATE_profile_verification_sandbox.bat
- `A` OSBB/RUN_MIGRATE_simplified_services_sandbox.bat
- `A` OSBB/RUN_fix_source_ref_schema.bat
- `A` OSBB/cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py
- `A` OSBB/cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py
- `A` OSBB/fix_source_ref_schema.py
- `A` OSBB/migrate_access_control_and_guard.py
- `A` OSBB/migrate_apartment_link_requests.py
- `A` OSBB/migrate_cashier_operator_editor.py
- `A` OSBB/migrate_cashier_v2.py
- `A` OSBB/migrate_cashier_v2_compat.py
- `A` OSBB/migrate_commercial_contract_core.py
- `A` OSBB/migrate_remote_requests.py
- `A` OSBB/migrate_service_orders_and_fulfillment.py
- `A` OSBB/migrate_unit_registry_composite_groups.py
- `A` OSBB/patch_cashier_v2_core_period_and_schemafix.py
- `A` OSBB/patch_cashier_v2_core_schemafix.py
- `A` OSBB/tools/MIGRATE_debt_policy_rules_v1.py
- `A` OSBB/tools/db_schema_compare.py
- `A` OSBB/tools/db_schema_snapshot.py
- `A` OSBB/tools/db_schema_snapshot_full.py
- `A` OSBB/tools/db_table_passport.py
- `A` OSBB/tools/project_passport.py
- `A` OSBB/tools/project_passport_v2.py
- `A` OSBB/tools/project_passport_v3_classifier.py
- `A` OSBB/tools/project_passport_v4_runtime_schema_audit.py

### BOT / MENUS / HANDLERS
- `A` OSBB/Bots/Start_OSBB_Guard_Sandbox_Bot.bat
- `A` OSBB/Bots/Start_OSBB_Guard_Sandbox_Bot_v2.bat
- `M` OSBB/Bots/db_access.py
- `M` OSBB/Bots/handlers/audit_viewer - Copy.py
- `M` OSBB/Bots/handlers/audit_viewer.py
- `A` OSBB/Bots/handlers/cashier_operator.py
- `A` OSBB/Bots/handlers/cashier_operator_v2.py
- `A` OSBB/Bots/handlers/client_portal.py
- `A` OSBB/Bots/handlers/client_portal_safe_linking.py
- `A` OSBB/Bots/handlers/client_portal_v2.py
- `A` OSBB/Bots/handlers/client_portal_v3.py
- `A` OSBB/Bots/handlers/commercial_contract_editor.py
- `A` OSBB/Bots/handlers/guard_workspace.py
- `A` OSBB/Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py
- `A` OSBB/Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py
- `A` OSBB/Bots/handlers/profile_parking_time_test_workspace.py
- `A` OSBB/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/Bots/handlers/service_orders_workspace.py
- `A` OSBB/Bots/handlers/service_orders_workspace.py.before_phone_access_ui_fix_2026-06-27_16-47-09
- `A` OSBB/Bots/handlers/service_orders_workspace.py.before_phone_access_ui_fix_2026-06-27_16-52-29
- `A` OSBB/Bots/handlers/service_orders_workspace.py.before_phone_access_ui_fix_v3_2026-06-27_17-22-40
- `A` OSBB/Bots/handlers/unit_registry_editor - Copy.py
- `A` OSBB/Bots/handlers/unit_registry_editor.py
- `M` OSBB/Bots/parking_bot - Copy.py
- `M` OSBB/Bots/parking_bot.py
- `A` OSBB/Bots/parking_bot_before_cashier_editor_2026-06-25_14-45-08.py
- `A` OSBB/Bots/parking_bot_before_client_portal_2026-06-25_10-25-49.py
- `A` OSBB/Bots/parking_bot_before_language_gate_fix_2026-06-25_10-45-39.py
- `A` OSBB/Bots/parking_bot_before_launch_queues_menu_2026-06-25_12-21-29.py
- `A` OSBB/Data/backups/source_code/cashier_route_repair_2026-06-27_20-04-49/run_bot_live_services_sandbox_v1.py
- `A` OSBB/Data/backups/source_code/parking_time_test_v1_2026-06-28_12-12-01/run_bot_live_services_sandbox_v1.py
- `A` OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/Bots/handlers/service_orders_workspace.py
- `A` OSBB/Data/backups/source_code/profile_button_early_route_2026-06-27_21-33-50/run_bot_live_services_sandbox_v1.py
- `A` OSBB/Data/backups/source_code/profile_verification_2026-06-27_20-51-33/Bots/handlers/service_orders_workspace.py
- `A` OSBB/Data/backups/source_code/profile_verification_2026-06-27_20-51-33/run_bot_live_services_sandbox_v1.py
- `A` OSBB/Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/Bots/handlers/service_orders_workspace.py
- `A` OSBB/Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/Bots/handlers/service_orders_workspace.py
- `A` OSBB/Data/backups/source_patches/remote_debt_gate_v1_2026-06-28_17-41-41/Bots/handlers/client_portal.py
- `A` OSBB/Data/backups/source_patches/remote_debt_gate_v1_2026-06-28_17-41-41/Bots/handlers/guard_workspace.py
- `A` OSBB/Start_OSBB_Guard_Sandbox_Bot_v2.bat
- `A` OSBB/Start_OSBB_Live_Service_Sandbox_Bot_before_service_ui_2026-06-26_20-50-39.bat
- `A` OSBB/Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
- `A` OSBB/cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py
- `A` OSBB/fix_parking_bot_language_gate.py
- `A` OSBB/parking_time_test_payload/Bots/handlers/profile_parking_time_test_workspace.py
- `A` OSBB/parking_time_test_payload/run_bot_live_services_sandbox_v1.py
- `A` OSBB/patch_parking_bot_cashier_operator.py
- `A` OSBB/patch_parking_bot_client_cabinet.py
- `A` OSBB/patch_parking_bot_client_portal.py
- `A` OSBB/patch_parking_bot_guard_workspace_v2.py
- `A` OSBB/patch_parking_bot_guard_workspace_v3.py
- `A` OSBB/patch_parking_bot_guard_workspace_v4.py
- `A` OSBB/patch_parking_bot_launch_queues_menu.py
- `A` OSBB/patch_parking_bot_service_orders_ui_v1.py
- `A` OSBB/patch_parking_bot_service_orders_v1.py
- `A` OSBB/phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py
- `A` OSBB/profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py
- `A` OSBB/profile_confirmation_button_ready_payload/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/profile_verification_critical_codes_payload/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/profile_verification_payload/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/profile_verification_payload/Bots/handlers/service_orders_workspace.py
- `A` OSBB/profile_verification_payload/run_bot_live_services_sandbox_v1.py
- `A` OSBB/profile_verification_terminology_v2_payload/Bots/handlers/profile_verification_workspace.py
- `A` OSBB/profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py
- `A` OSBB/run_bot_guard_sandbox.py
- `A` OSBB/run_bot_guard_sandbox_v2.py
- `A` OSBB/run_bot_guard_sandbox_v3.py
- `A` OSBB/run_bot_live_service_sandbox_v4.py
- `A` OSBB/run_bot_live_services_sandbox_v1.py
- `A` OSBB/run_bot_sandbox_v2.py
- `A` OSBB/service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py
- `A` OSBB/switch_parking_bot_to_cashier_v2.py

### SERVICES / BUSINESS LOGIC
- `A` OSBB/CHECK_guard_sandbox_service_orders.py
- `A` OSBB/CHECK_guard_sandbox_service_orders_v2.py
- `A` OSBB/CHECK_phone_barrier_access_operational_sandbox.py
- `A` OSBB/CHECK_service_code_compatibility_phone_v2.py
- `A` OSBB/CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.bat
- `A` OSBB/CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.py
- `A` OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/phone_barrier_access_core.py
- `A` OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/service_orders_core.py
- `A` OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/service_preorders_core.py
- `A` OSBB/Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/service_orders_core.py
- `A` OSBB/Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/service_preorders_core.py
- `A` OSBB/Data/exports/cashier/cashier_payments_audit_2026-05_2026-06_2026-06-28_15-01-16.csv
- `A` OSBB/Data/exports/cashier/cashier_payments_audit_2026-05_2026-06_2026-06-28_15-01-16.txt
- `A` OSBB/Data/exports/cashier/cashier_payments_audit_2026-05_2026-06_2026-06-28_15-01-16.xlsx
- `A` OSBB/Data/exports/cashier/cashier_unpaid_2026-05_2026-06_2026-06-28_14-46-09.csv
- `A` OSBB/Data/exports/cashier/cashier_unpaid_2026-05_2026-06_2026-06-28_14-46-09.txt
- `A` OSBB/Data/exports/cashier/cashier_unpaid_2026-05_2026-06_2026-06-28_14-46-09.xlsx
- `A` OSBB/Data/exports/cashier/ohorona_list1_central_apply_2026-06-22_22-53-00.txt
- `A` OSBB/Data/exports/debt_policy/debt_policy_matrix_preview_2026-06-28_20-23-44.csv
- `A` OSBB/Data/exports/debt_policy/debt_policy_matrix_preview_2026-06-28_20-23-44.txt
- `A` OSBB/Data/exports/debt_policy/service_codes_live_sandbox.txt
- `A` OSBB/Docs/Architecture/Services/service_catalog_v2_design.md
- `A` OSBB/Docs/Architecture/Services/service_catalog_v2_design_approved_updates.md
- `A` OSBB/FIND_actual_service_order_state.py
- `A` OSBB/INSTALL_PHONE_ACCESS_UI_FIX.bat
- `A` OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v2.bat
- `A` OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v2.py
- `A` OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v3.bat
- `A` OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v3.py
- `A` OSBB/INSTALL_cashier_route_after_phone_v2.py
- `A` OSBB/INSTALL_phone_barrier_access_v2.py
- `A` OSBB/INSTALL_service_code_compatibility_phone_v2.py
- `A` OSBB/OSBB_Service_Orders_Foundation_v1.zip
- `A` OSBB/OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py
- `A` OSBB/OSBB_Service_Orders_Foundation_v1/service_orders_core.py
- `A` OSBB/OSBB_Service_Orders_Foundation_v1/service_orders_preflight.py
- `A` OSBB/OSBB_cashier_route_fix.zip
- `A` OSBB/OSBB_cashier_route_repair_after_phone_v2.zip
- `A` OSBB/OSBB_phone_access_ui_fix.zip
- `A` OSBB/OSBB_phone_access_ui_fix_v3.zip
- `A` OSBB/OSBB_phone_barrier_access_v2_working_sandbox.zip
- `A` OSBB/OSBB_service_code_compatibility_repair_phone_v2.zip
- `A` OSBB/README_CASHIER_ROUTE_FIX.txt
- `A` OSBB/README_CASHIER_ROUTE_REPAIR_AFTER_PHONE_V2.txt
- `A` OSBB/README_LIVE_SERVICE_UI.txt
- `A` OSBB/README_PHONE_ACCESS_FIX.txt
- `A` OSBB/README_PHONE_ACCESS_FIX_v2.txt
- `A` OSBB/README_PHONE_ACCESS_FIX_v3.txt
- `A` OSBB/README_PHONE_BARRIER_ACCESS_V2.txt
- `A` OSBB/README_SERVICE_CODE_COMPATIBILITY_PHONE_V2.txt
- `A` OSBB/RETIRE_legacy_new_remote_test_orders_sandbox.py
- `A` OSBB/RUN_CHECK_cashier_route_after_phone_v2.bat
- `A` OSBB/RUN_CHECK_guard_sandbox_service_orders.bat
- `A` OSBB/RUN_CHECK_guard_sandbox_service_orders_v2.bat
- `A` OSBB/RUN_CHECK_phone_barrier_access_operational_sandbox.bat
- `A` OSBB/RUN_CHECK_service_code_compatibility_phone_v2.bat
- `A` OSBB/RUN_FIND_actual_service_order_state.bat
- `A` OSBB/RUN_INSTALL_cashier_route_after_phone_v2.bat
- `A` OSBB/RUN_INSTALL_phone_barrier_access_v2.bat
- `A` OSBB/RUN_INSTALL_service_code_compatibility_phone_v2.bat
- `A` OSBB/RUN_RETIRE_legacy_new_remote_test_orders_sandbox.bat
- `A` OSBB/Start_OSBB_Live_Service_Sandbox_Bot.bat
- `A` OSBB/cashier_v2_core.py
- `A` OSBB/cashier_v2_preflight.py
- `A` OSBB/cashier_v2_preflight_compat.py
- `A` OSBB/diagnose_sandbox_charges.py
- `A` OSBB/install_service_orders_ui.py
- `A` OSBB/patch_guard_workspace_default_cash_note.py
- `A` OSBB/phone_barrier_access_core.py
- `A` OSBB/phone_barrier_access_service.py
- `A` OSBB/phone_barrier_access_v2_payload/phone_barrier_access_core.py
- `A` OSBB/phone_barrier_access_v2_payload/phone_barrier_access_service.py
- `A` OSBB/phone_barrier_access_v2_payload/service_orders_core.py
- `A` OSBB/phone_barrier_access_v2_payload/service_preorders_core.py
- `A` OSBB/prepare_live_service_test.py
- `A` OSBB/service_catalog_admin_core.py
- `A` OSBB/service_code_compatibility_payload/service_orders_core.py
- `A` OSBB/service_code_compatibility_payload/service_preorders_core.py
- `A` OSBB/service_orders_core.py
- `A` OSBB/service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py
- `A` OSBB/service_orders_preflight.py
- `A` OSBB/service_preorders_core.py
- `A` OSBB/tools/INSTALL_remote_debt_gate_v1.py
- `A` OSBB/tools/cashier_parking_payments_audit_v4.py
- `A` OSBB/tools/cashier_unpaid_preview.py
- `A` OSBB/tools/cashier_unpaid_preview_v2.py
- `A` OSBB/tools/cashier_unpaid_preview_v3.py
- `A` OSBB/tools/debt_policy_matrix_preview.py
- `A` OSBB/tools/dump_service_codes_live_sandbox.py
- `A` OSBB/tools/extract_remote_gate_sources.py
- `A` OSBB/tools/remote_debt_gate_audit.py
- `A` OSBB/tools/remote_debt_gate_test_fixture.py

### TOOLS / INSPECTION / ACCEPTANCE
- `A` OSBB/CHECK_profile_parking_time_test_sandbox.py
- `A` OSBB/CHECK_profile_test_candidate_apartment_40.py
- `A` OSBB/Data/exports/audits/registry_audit_2026-06-23_17-18-21.txt
- `A` OSBB/Data/exports/diagnostics/audit_diagnostic_2026-06-24_20-17-19.txt
- `A` OSBB/INSTALL_profile_parking_time_test_v1.py
- `A` OSBB/OSBB_apartment_40_profile_test_preflight.zip
- `A` OSBB/OSBB_profile_parking_time_test_v1_sandbox.zip
- `A` OSBB/README_APARTMENT_40_PROFILE_TEST_PREFLIGHT.txt
- `A` OSBB/README_PROFILE_PARKING_TIME_TEST_V1.txt
- `A` OSBB/RUN_CHECK_profile_parking_time_test_sandbox.bat
- `A` OSBB/RUN_CHECK_profile_test_candidate_apartment_40.bat
- `A` OSBB/RUN_INSTALL_profile_parking_time_test_v1.bat
- `A` OSBB/parking_time_test_payload/profile_parking_time_test_core.py
- `A` OSBB/patch_guard_workspace_direct_notice_confirm.py
- `A` OSBB/profile_parking_time_test_core.py
- `A` OSBB/test_db_access_unit_resolver.py
- `A` OSBB/tools/project_code_search.py
- `A` OSBB/tools/show_running_osbb_bots.py
- `A` OSBB/tools/start_live_services_bot.py
- `A` OSBB/tools/stop_live_services_bot.py

### DOCS / EXPORTS
- `M` .claude/cloude-code-toolbox-mcp-skills-awareness.md
- `M` CLAUDE.md
- `A` OSBB/Data/exports/code/code_search_2026-06-28_15-20-58.txt
- `A` OSBB/Data/exports/commercial/commercial_contract_core_2026-06-24_12-27-30.txt
- `A` OSBB/Data/exports/commercial/commercial_contract_core_2026-06-24_12-30-30.txt
- `A` OSBB/Data/exports/commercial/commercial_notification_queue_2026-06-24_dry_run_2026-06-24_12-32-13.txt
- `A` OSBB/Data/exports/units/commercial_unit_placeholders_2026-06-24_10-48-47.txt
- `A` OSBB/Data/exports/units/commercial_unit_placeholders_2026-06-24_10-49-12.txt
- `A` OSBB/Data/exports/units/composite_unit_inventory_2026-06-23_17-20-07.txt
- `A` OSBB/Data/exports/units/unit_registry_aliases_2026-06-23_16-09-28.txt
- `A` OSBB/Data/exports/units/unit_registry_composite_groups_2026-06-23_17-36-23.txt
- `A` OSBB/Data/exports/units/unit_registry_composite_groups_2026-06-23_17-40-54.txt
- `A` OSBB/Data/exports/users/restore_resident_link_2026-06-25_12-51-41.txt
- `A` OSBB/Data/exports/users/restore_resident_link_2026-06-25_12-52-09.txt
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27.zip
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/DO_NOT_UPLOAD_SECRETS.md
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/OSBB_BUSINESS_HANDOFF_2026-06-27.md
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/OSBB_PROJECT_INSTRUCTIONS.md
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/SHA256SUMS.txt
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/START_OSBB_BUSINESS_CHAT_2026-06-28.txt
- `A` OSBB/Docs/OSBB_Business_Handoff_2026-06-27/TRANSFER_CHECKLIST_2026-06-27.txt
- `A` OSBB/Docs/non_residential_unit_draft_template.xlsx
- `A` OSBB/README_LIVE_SERVICES_SANDBOX.txt
- `A` OSBB/README_PROFILE_BUTTON_EARLY_ROUTE_FIX.txt
- `A` OSBB/README_PROFILE_CONFIRMATION_READY_VISIBILITY_FIX.txt
- `A` OSBB/README_PROFILE_CRITICAL_CODES_FIX.txt
- `A` OSBB/README_PROFILE_VERIFICATION_TERMINOLOGY_V2.txt
- `A` OSBB/README_PROFILE_VERIFICATION_V1.txt
- `A` OSBB/README_SIMPLIFIED_SERVICES.txt

### OTHER
- `A` OSBB/CHECK_profile_button_early_route_fix.py
- `A` OSBB/CHECK_profile_confirmation_ready_visibility_fix.py
- `A` OSBB/CHECK_profile_critical_codes_fix.py
- `A` OSBB/CHECK_profile_verification_sandbox.py
- `A` OSBB/CHECK_profile_verification_terminology_v2.py
- `A` OSBB/Data/backups/source_code/profile_confirmation_ready_visibility_2026-06-27_21-55-54/profile_verification_workspace.py
- `A` OSBB/Data/backups/source_code/profile_critical_codes_fix_2026-06-27_21-47-24/profile_verification_workspace.py
- `A` OSBB/Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/profile_verification_core.py
- `A` OSBB/Data/exports/units/composite_unit_inventory_2026-06-23_17-20-07.csv
- `D` "OSBB/Data/raw/typed/~$\320\236\321\205\320\276\321\200\320\276\320\275\320\260.xlsx"
- `A` OSBB/INSTALL_profile_button_early_route_fix.py
- `A` OSBB/INSTALL_profile_confirmation_ready_visibility_fix.py
- `A` OSBB/INSTALL_profile_critical_codes_fix.py
- `A` OSBB/INSTALL_profile_verification_terminology_v2.py
- `A` OSBB/INSTALL_profile_verification_v1.py
- `A` OSBB/OSBB_profile_button_early_route_fix_v2.zip
- `A` OSBB/OSBB_profile_confirmation_ready_visibility_fix.zip
- `A` OSBB/OSBB_profile_verification_terminology_v2 (1).zip
- `A` OSBB/OSBB_profile_verification_v1_sandbox_final.zip
- `A` OSBB/OSBB_simplified_services_preorders_bundle.zip
- `A` OSBB/RUN_CHECK_profile_button_early_route_fix.bat
- `A` OSBB/RUN_CHECK_profile_confirmation_ready_visibility_fix.bat
- `A` OSBB/RUN_CHECK_profile_critical_codes_fix.bat
- `A` OSBB/RUN_CHECK_profile_verification_sandbox.bat
- `A` OSBB/RUN_CHECK_profile_verification_terminology_v2.bat
- `A` OSBB/RUN_INSTALL_profile_button_early_route_fix.bat
- `A` OSBB/RUN_INSTALL_profile_confirmation_ready_visibility_fix.bat
- `A` OSBB/RUN_INSTALL_profile_critical_codes_fix.bat
- `A` OSBB/RUN_INSTALL_profile_verification_terminology_v2.bat
- `A` OSBB/RUN_INSTALL_profile_verification_v1.bat
- `A` OSBB/STOP_old_guard_sandbox_bots.bat
- `A` OSBB/access_control.py
- `A` OSBB/commercial_contracts.py
- `A` OSBB/commercial_notification_delivery.py
- `A` OSBB/create_clean_live_sandbox.py
- `A` OSBB/create_isolated_live_sandbox_v2.py
- `A` OSBB/diagnose_osbb_audit.py
- `A` OSBB/find_sandbox_telegram_id.py
- `A` OSBB/guard_workspace_preflight.py
- `A` OSBB/guard_workspace_preflight_v2.py
- `A` OSBB/manage_staff_access.py
- `A` OSBB/manage_staff_access_v2.py
- `A` OSBB/profile_verification_core.py
- `A` OSBB/profile_verification_payload/profile_verification_core.py
- `A` OSBB/profile_verification_terminology_v2_payload/profile_verification_core.py
- `A` OSBB/repair_confirmed_unit_seed_notes.py
- `A` OSBB/restore_resident_apartment_link.py
- `A` OSBB/seed_commercial_unit_placeholders.py
- `A` OSBB/test.py
- `A` OSBB/unit_resolver.py

## Diff stat

```
 .../cloude-code-toolbox-mcp-skills-awareness.md    |     2 +-
 CLAUDE.md                                          |    10 +-
 OSBB/Bots/Start_OSBB_Guard_Sandbox_Bot.bat         |    40 +
 OSBB/Bots/Start_OSBB_Guard_Sandbox_Bot_v2.bat      |    40 +
 OSBB/Bots/db_access.py                             |  1098 ++
 OSBB/Bots/handlers/audit_viewer - Copy.py          |   156 +-
 OSBB/Bots/handlers/audit_viewer.py                 |   361 +-
 OSBB/Bots/handlers/cashier_operator.py             |  2426 +++
 OSBB/Bots/handlers/cashier_operator_v2.py          |  1097 ++
 OSBB/Bots/handlers/client_portal.py                |  2268 +++
 OSBB/Bots/handlers/client_portal_safe_linking.py   |  2183 +++
 OSBB/Bots/handlers/client_portal_v2.py             |   665 +
 OSBB/Bots/handlers/client_portal_v3.py             |    96 +
 OSBB/Bots/handlers/commercial_contract_editor.py   |  1581 ++
 OSBB/Bots/handlers/guard_workspace.py              |  1313 ++
 ...before_default_cash_note_2026-06-26_16-25-02.py |  1140 ++
 ...re_direct_notice_confirm_2026-06-26_18-28-39.py |  1143 ++
 .../profile_parking_time_test_workspace.py         |   364 +
 .../handlers/profile_verification_workspace.py     |   767 +
 OSBB/Bots/handlers/service_orders_workspace.py     |  1742 ++
 ....before_phone_access_ui_fix_2026-06-27_16-47-09 |  1342 ++
 ....before_phone_access_ui_fix_2026-06-27_16-52-29 |  1342 ++
 ...fore_phone_access_ui_fix_v3_2026-06-27_17-22-40 |  1405 ++
 OSBB/Bots/handlers/unit_registry_editor - Copy.py  |  1035 +
 OSBB/Bots/handlers/unit_registry_editor.py         |  1076 ++
 OSBB/Bots/parking_bot - Copy.py                    |     8 +-
 OSBB/Bots/parking_bot.py                           |    68 +-
 ...ot_before_cashier_editor_2026-06-25_14-45-08.py |  1342 ++
 ...bot_before_client_portal_2026-06-25_10-25-49.py |  1309 ++
 ...before_language_gate_fix_2026-06-25_10-45-39.py |  1341 ++
 ...efore_launch_queues_menu_2026-06-25_12-21-29.py |  1341 ++
 OSBB/CHECK_guard_sandbox_service_orders.py         |   492 +
 OSBB/CHECK_guard_sandbox_service_orders_v2.py      |   470 +
 ...ECK_phone_barrier_access_operational_sandbox.py |    76 +
 OSBB/CHECK_phone_barrier_access_sandbox_schema.py  |   128 +
 OSBB/CHECK_profile_button_early_route_fix.py       |    61 +
 ...CK_profile_confirmation_ready_visibility_fix.py |    36 +
 OSBB/CHECK_profile_critical_codes_fix.py           |    39 +
 OSBB/CHECK_profile_parking_time_test_sandbox.py    |    96 +
 OSBB/CHECK_profile_test_candidate_apartment_40.py  |   355 +
 OSBB/CHECK_profile_verification_sandbox.py         |    39 +
 OSBB/CHECK_profile_verification_terminology_v2.py  |    56 +
 OSBB/CHECK_service_code_compatibility_phone_v2.py  |   121 +
 .../CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.bat |    38 +
 OSBB/CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.py |   174 +
 .../run_bot_live_services_sandbox_v1.py            |   704 +
 .../run_bot_live_services_sandbox_v1.py            |   864 +
 .../Bots/handlers/service_orders_workspace.py      |  1405 ++
 .../phone_barrier_access_core.py                   |  1017 +
 .../service_orders_core.py                         |  1373 ++
 .../service_preorders_core.py                      |  1095 ++
 .../run_bot_live_services_sandbox_v1.py            |   830 +
 .../profile_verification_workspace.py              |   764 +
 .../profile_verification_workspace.py              |   759 +
 .../Bots/handlers/service_orders_workspace.py      |  1631 ++
 .../run_bot_live_services_sandbox_v1.py            |   707 +
 .../handlers/profile_verification_workspace.py     |   713 +
 .../Bots/handlers/service_orders_workspace.py      |  1735 ++
 .../profile_verification_core.py                   |  1530 ++
 .../Bots/handlers/service_orders_workspace.py      |  1613 ++
 .../service_orders_core.py                         |  1337 ++
 .../service_preorders_core.py                      |  1146 ++
 .../Bots/handlers/client_portal.py                 |  2183 +++
 .../Bots/handlers/guard_workspace.py               |  1150 ++
 ...remote_debt_gate_fixture_2026-06-28_18-32-29.db |   Bin 0 -> 1331200 bytes
 .../actual_service_order_state_20260627_115724.txt |    79 +
 ...ox_service_orders_diagnosis_20260627_114522.txt |    22 +
 ...ox_service_orders_diagnosis_20260627_114911.txt |    18 +
 ...service_orders_diagnosis_v2_20260627_115123.txt |   204 +
 ...services_payment_schema_fix_20260627_122549.txt |    16 +
 ...s_operational_migration_2026-06-27_19-38-08.txt |     9 +
 ...access_schema_migration_2026-06-27_19-16-27.txt |    29 +
 ...ing_time_test_migration_2026-06-28_12-12-37.txt |    10 +
 ..._verification_migration_2026-06-27_20-52-07.txt |    18 +
 ...fied_services_migration_2026-06-27_14-10-45.txt |     8 +
 OSBB/Data/db/osbb_test - Copy.db                   |   Bin 0 -> 1081344 bytes
 OSBB/Data/db/osbb_test.db                          |   Bin 884736 -> 1331200 bytes
 ...26_before_payment_schema_fix_20260627_122548.db |   Bin 0 -> 1597440 bytes
 ...rrier_access_operational_2026-06-27_19-38-08.db |   Bin 0 -> 1851392 bytes
 ...ne_barrier_access_schema_2026-06-27_19-16-27.db |   Bin 0 -> 1679360 bytes
 ...rofile_parking_time_test_2026-06-28_12-12-37.db |   Bin 0 -> 1982464 bytes
 ...ore_profile_verification_2026-06-27_20-52-07.db |   Bin 0 -> 1912832 bytes
 ..._legacy_new_remote_tests_2026-06-27_13-31-55.db |   Bin 0 -> 1605632 bytes
 ...ice_operator_permissions_2026-06-27_12-18-22.db |   Bin 0 -> 1593344 bytes
 ...fied_service_permissions_2026-06-27_16-08-06.db |   Bin 0 -> 1662976 bytes
 ...fore_simplified_services_2026-06-27_13-32-32.db |   Bin 0 -> 1605632 bytes
 ...fore_simplified_services_2026-06-27_14-10-45.db |   Bin 0 -> 1605632 bytes
 .../cashier_v2_preflight_2026-06-25_18-53-50.txt   |    47 +
 ...ier_v2_preflight_compat_2026-06-25_19-47-09.txt |    43 +
 .../clean_live_sandbox_2026-06-26_20-13-26.txt     |    50 +
 ...ard_workspace_preflight_2026-06-26_12-39-50.txt |    52 +
 ...ard_workspace_preflight_2026-06-26_12-56-09.txt |    46 +
 ...bb_test_cashier_v2_check_2026-06-25_18-53-50.db |   Bin 0 -> 1331200 bytes
 ..._cashier_v2_compat_check_2026-06-25_19-47-09.db |   Bin 0 -> 1347584 bytes
 ...-25_19-47-09_guard_check_2026-06-26_12-39-50.db |   Bin 0 -> 1433600 bytes
 ...-25_19-47-09_guard_check_2026-06-26_12-56-09.db |   Bin 0 -> 1441792 bytes
 ...-09_service_orders_check_2026-06-26_19-42-50.db |   Bin 0 -> 1593344 bytes
 .../osbb_test_live_services_2026-06-26_20-13-26.db |   Bin 0 -> 2023424 bytes
 ...ervice_orders_preflight_2026-06-26_19-42-50.txt |    31 +
 .../audits/registry_audit_2026-06-23_17-18-21.txt  |   157 +
 ...hier_operator_migration_2026-06-25_14-43-23.txt |    54 +
 ...hier_operator_migration_2026-06-25_14-43-41.txt |    54 +
 ...s_audit_2026-05_2026-06_2026-06-28_15-01-16.csv |    96 +
 ...s_audit_2026-05_2026-06_2026-06-28_15-01-16.txt |    45 +
 ..._audit_2026-05_2026-06_2026-06-28_15-01-16.xlsx |   Bin 0 -> 38435 bytes
 ..._unpaid_2026-05_2026-06_2026-06-28_14-46-09.csv |    91 +
 ..._unpaid_2026-05_2026-06_2026-06-28_14-46-09.txt |   124 +
 ...unpaid_2026-05_2026-06_2026-06-28_14-46-09.xlsx |   Bin 0 -> 17584 bytes
 .../cashier_v2_migration_2026-06-25_17-56-05.txt   |    30 +
 ...ona_list1_central_apply_2026-06-22_22-53-00.txt |    99 +
 .../code/code_search_2026-06-28_15-20-58.txt       | 19088 +++++++++++++++++++
 .../00_Project.md                                  |    89 +
 .../01_File_System.md                              |   694 +
 .../02_Modules.md                                  |  2477 +++
 .../03_Technical_Debt.md                           |    30 +
 .../04_DB_Table_References.md                      |  6814 +++++++
 .../inventory/classes.csv                          |    15 +
 .../inventory/db_table_refs.csv                    | 13096 +++++++++++++
 .../inventory/files.csv                            |   462 +
 .../inventory/functions.csv                        |  4178 ++++
 .../inventory/imports.csv                          |  2103 ++
 .../inventory/modules.csv                          |   276 +
 .../inventory/todos.csv                            |    29 +
 .../summary.json                                   |    14 +
 .../00_Project.md                                  |   101 +
 .../01_File_System.md                              |   440 +
 .../02_Modules.md                                  |  2333 +++
 .../03_Technical_Debt.md                           |    31 +
 .../04_DB_Table_References.md                      |  5034 +++++
 .../inventory/classes.csv                          |    22 +
 .../inventory/db_table_refs.csv                    |  7708 ++++++++
 .../inventory/files.csv                            |   330 +
 .../inventory/functions.csv                        |  3678 ++++
 .../inventory/imports.csv                          |  1920 ++
 .../inventory/modules.csv                          |   260 +
 .../inventory/todos.csv                            |    30 +
 .../summary.json                                   |    15 +
 .../00_Project_v3.md                               |    69 +
 .../05_Entrypoints.md                              |  1171 ++
 .../06_Active_Candidates.md                        |   111 +
 .../07_Legacy_Backups.md                           |    30 +
 .../08_Bot_Handlers.md                             |    20 +
 .../09_Remote_Access_Service_Modules.md            |   177 +
 .../10_Code_Risk_Summary.md                        |    53 +
 .../inventory/entrypoints.csv                      |   196 +
 .../inventory/files_classified.csv                 |   331 +
 .../inventory/functions.csv                        |  3693 ++++
 .../inventory/import_edges.csv                     |  2935 +++
 .../inventory/python_modules_classified.csv        |   261 +
 .../summary.json                                   |    33 +
 .../00_Runtime_Schema_Audit.md                     |    29 +
 .../01_Strict_Entrypoints.md                       |   191 +
 .../02_Runtime_Import_Closure.md                   |     3 +
 .../03_Missing_Tables_From_Code.md                 |   818 +
 .../04_Remote_Access_Modules.md                    |   174 +
 .../05_Debt_Gate_Candidates.md                     |  1003 +
 .../inventory/db_table_refs.csv                    |  7733 ++++++++
 .../inventory/debt_gate_candidates.csv             |  3552 ++++
 .../inventory/missing_tables_from_code.csv         |   164 +
 .../inventory/remote_access_modules.csv            |   173 +
 .../inventory/runtime_import_edges.csv             |     1 +
 .../inventory/runtime_import_nodes.csv             |     2 +
 .../inventory/strict_entrypoints.csv               |   190 +
 .../summary.json                                   |    19 +
 .../00_Remote_Debt_Gate_Audit.md                   |   376 +
 .../inventory/candidate_lines.csv                  |  1047 +
 .../inventory/db_status.csv                        |     2 +
 .../inventory/files_scanned.csv                    |    80 +
 .../inventory/functions_remote_debt_scan.csv       |   517 +
 .../summary.json                                   |    24 +
 .../remote_gate_sources_2026-06-28_16-59-59.txt    |  2470 +++
 .../code_passport/running_bots_after_start.txt     |    63 +
 .../exports/code_passport/running_bots_now.txt     |    51 +
 ...ommercial_contract_core_2026-06-24_12-27-30.txt |    40 +
 ...ommercial_contract_core_2026-06-24_12-30-30.txt |    40 +
 ...ueue_2026-06-24_dry_run_2026-06-24_12-32-13.txt |    16 +
 .../gold_2026-06-28_22-23-17/01_schema.txt         |    31 +
 .../gold_2026-06-28_22-23-17/02_columns.csv        |    17 +
 .../gold_2026-06-28_22-23-17/03_indexes.csv        |     6 +
 .../gold_2026-06-28_22-23-17/04_foreign_keys.csv   |     1 +
 .../05_code_references.csv                         |  1901 ++
 .../06_service_code_usage.csv                      |    17 +
 .../gold_2026-06-28_22-23-17/07_sample_rows.csv    |    17 +
 .../08_distinct_values.txt                         |    96 +
 .../09_code_references_by_kind.txt                 |  1178 ++
 .../10_architecture_notes.md                       |    31 +
 .../gold_2026-06-28_22-23-17/passport_summary.txt  |    23 +
 ...t_policy_matrix_preview_2026-06-28_20-23-44.csv |    18 +
 ...t_policy_matrix_preview_2026-06-28_20-23-44.txt |    30 +
 .../debt_policy/service_codes_live_sandbox.txt     |   195 +
 .../audit_diagnostic_2026-06-24_20-17-19.txt       |    56 +
 ...mote_requests_migration_2026-06-25_10-23-49.txt |    17 +
 ...mote_requests_migration_2026-06-25_10-24-18.txt |    17 +
 ...mote_requests_migration_2026-06-25_11-42-17.txt |    17 +
 ...mote_requests_migration_2026-06-25_12-05-57.txt |    17 +
 .../schema/schema_compare_2026-06-28_13-09-32.txt  |   661 +
 .../schema_snapshot_test_2026-06-28_14-30-02.txt   |  4148 ++++
 ...rcial_unit_placeholders_2026-06-24_10-48-47.txt |    34 +
 ...rcial_unit_placeholders_2026-06-24_10-49-12.txt |    34 +
 ...omposite_unit_inventory_2026-06-23_17-20-07.csv |     5 +
 ...omposite_unit_inventory_2026-06-23_17-20-07.txt |    65 +
 .../unit_registry_aliases_2026-06-23_16-09-28.txt  |    19 +
 ...gistry_composite_groups_2026-06-23_17-36-23.txt |    31 +
 ...gistry_composite_groups_2026-06-23_17-40-54.txt |    38 +
 ...link_requests_migration_2026-06-25_11-42-33.txt |    17 +
 ...link_requests_migration_2026-06-25_12-07-06.txt |    17 +
 .../restore_resident_link_2026-06-25_12-51-41.txt  |    22 +
 .../restore_resident_link_2026-06-25_12-52-09.txt  |    22 +
 ...5\320\276\321\200\320\276\320\275\320\260.xlsx" |   Bin 165 -> 0 bytes
 .../Services/service_catalog_v2_design.md          |   363 +
 .../service_catalog_v2_design_approved_updates.md  |   112 +
 OSBB/Docs/OSBB_Business_Handoff_2026-06-27.zip     |   Bin 0 -> 8560 bytes
 .../DO_NOT_UPLOAD_SECRETS.md                       |    12 +
 .../OSBB_BUSINESS_HANDOFF_2026-06-27.md            |   207 +
 .../OSBB_PROJECT_INSTRUCTIONS.md                   |    28 +
 .../SHA256SUMS.txt                                 |     5 +
 .../START_OSBB_BUSINESS_CHAT_2026-06-28.txt        |    11 +
 .../TRANSFER_CHECKLIST_2026-06-27.txt              |    35 +
 OSBB/Docs/non_residential_unit_draft_template.xlsx |   Bin 0 -> 8817 bytes
 OSBB/FIND_actual_service_order_state.py            |   435 +
 OSBB/FIX_live_services_sandbox_payment_schema.py   |   347 +
 OSBB/INSTALL_PHONE_ACCESS_UI_FIX.bat               |    49 +
 OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v2.bat            |    13 +
 OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v2.py             |   142 +
 OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v3.bat            |    11 +
 OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v3.py             |   110 +
 OSBB/INSTALL_cashier_route_after_phone_v2.py       |   100 +
 OSBB/INSTALL_phone_barrier_access_v2.py            |   138 +
 OSBB/INSTALL_profile_button_early_route_fix.py     |    77 +
 ...LL_profile_confirmation_ready_visibility_fix.py |    75 +
 OSBB/INSTALL_profile_critical_codes_fix.py         |    75 +
 OSBB/INSTALL_profile_parking_time_test_v1.py       |   124 +
 .../INSTALL_profile_verification_terminology_v2.py |   122 +
 OSBB/INSTALL_profile_verification_v1.py            |    51 +
 .../INSTALL_service_code_compatibility_phone_v2.py |   100 +
 ...ATE_phone_barrier_access_operational_sandbox.py |   150 +
 OSBB/MIGRATE_phone_barrier_access_sandbox.py       |   151 +
 OSBB/MIGRATE_profile_parking_time_test_sandbox.py  |   109 +
 OSBB/MIGRATE_profile_verification_sandbox.py       |    62 +
 OSBB/MIGRATE_simplified_services_sandbox.py        |   146 +
 OSBB/OSBB_Service_Orders_Foundation_v1.zip         |   Bin 0 -> 23082 bytes
 .../migrate_service_orders_and_fulfillment.py      |   769 +
 .../service_catalog_admin_core.py                  |   570 +
 .../service_orders_core.py                         |  1125 ++
 .../service_orders_preflight.py                    |   437 +
 OSBB/OSBB_apartment_40_profile_test_preflight.zip  |   Bin 0 -> 5061 bytes
 OSBB/OSBB_cashier_route_fix.zip                    |   Bin 0 -> 8097 bytes
 OSBB/OSBB_cashier_route_repair_after_phone_v2.zip  |   Bin 0 -> 10492 bytes
 OSBB/OSBB_phone_access_ui_fix.zip                  |   Bin 0 -> 15546 bytes
 OSBB/OSBB_phone_access_ui_fix_v3.zip               |   Bin 0 -> 16838 bytes
 .../OSBB_phone_barrier_access_schema_migration.zip |   Bin 0 -> 12647 bytes
 ...SBB_phone_barrier_access_v2_working_sandbox.zip |   Bin 0 -> 58761 bytes
 OSBB/OSBB_profile_button_early_route_fix_v2.zip    |   Bin 0 -> 13069 bytes
 ...B_profile_confirmation_ready_visibility_fix.zip |   Bin 0 -> 10418 bytes
 OSBB/OSBB_profile_parking_time_test_v1_sandbox.zip |   Bin 0 -> 26162 bytes
 ...SBB_profile_verification_terminology_v2 (1).zip |   Bin 0 -> 40017 bytes
 .../OSBB_profile_verification_v1_sandbox_final.zip |   Bin 0 -> 48474 bytes
 ..._service_code_compatibility_repair_phone_v2.zip |   Bin 0 -> 39633 bytes
 OSBB/OSBB_simplified_services_preorders_bundle.zip |   Bin 0 -> 35672 bytes
 .../README_APARTMENT_40_PROFILE_TEST_PREFLIGHT.txt |    53 +
 OSBB/README_CASHIER_ROUTE_FIX.txt                  |    43 +
 .../README_CASHIER_ROUTE_REPAIR_AFTER_PHONE_V2.txt |    74 +
 OSBB/README_LIVE_SERVICES_SANDBOX.txt              |    67 +
 OSBB/README_LIVE_SERVICE_UI.txt                    |    18 +
 OSBB/README_PHONE_ACCESS_FIX.txt                   |    51 +
 OSBB/README_PHONE_ACCESS_FIX_v2.txt                |    29 +
 OSBB/README_PHONE_ACCESS_FIX_v3.txt                |    30 +
 ...EADME_PHONE_BARRIER_ACCESS_SCHEMA_MIGRATION.txt |    92 +
 OSBB/README_PHONE_BARRIER_ACCESS_V2.txt            |   151 +
 OSBB/README_PROFILE_BUTTON_EARLY_ROUTE_FIX.txt     |    69 +
 ...E_PROFILE_CONFIRMATION_READY_VISIBILITY_FIX.txt |    56 +
 OSBB/README_PROFILE_CRITICAL_CODES_FIX.txt         |    64 +
 OSBB/README_PROFILE_PARKING_TIME_TEST_V1.txt       |   110 +
 .../README_PROFILE_VERIFICATION_TERMINOLOGY_V2.txt |   119 +
 OSBB/README_PROFILE_VERIFICATION_V1.txt            |    76 +
 .../README_SERVICE_CODE_COMPATIBILITY_PHONE_V2.txt |    88 +
 OSBB/README_SIMPLIFIED_SERVICES.txt                |    87 +
 ...RETIRE_legacy_new_remote_test_orders_sandbox.py |   117 +
 OSBB/RUN_CHECK_cashier_route_after_phone_v2.bat    |    13 +
 OSBB/RUN_CHECK_guard_sandbox_service_orders.bat    |    43 +
 OSBB/RUN_CHECK_guard_sandbox_service_orders_v2.bat |    39 +
 ...CK_phone_barrier_access_operational_sandbox.bat |    11 +
 ...N_CHECK_phone_barrier_access_sandbox_schema.bat |    13 +
 OSBB/RUN_CHECK_profile_button_early_route_fix.bat  |    11 +
 ...K_profile_confirmation_ready_visibility_fix.bat |    11 +
 OSBB/RUN_CHECK_profile_critical_codes_fix.bat      |    11 +
 ...RUN_CHECK_profile_parking_time_test_sandbox.bat |    10 +
 ...N_CHECK_profile_test_candidate_apartment_40.bat |    13 +
 OSBB/RUN_CHECK_profile_verification_sandbox.bat    |    10 +
 ...N_CHECK_profile_verification_terminology_v2.bat |    11 +
 ...N_CHECK_service_code_compatibility_phone_v2.bat |    13 +
 OSBB/RUN_FIND_actual_service_order_state.bat       |    39 +
 ...UN_FIX_live_services_sandbox_payment_schema.bat |    46 +
 OSBB/RUN_INSTALL_cashier_route_after_phone_v2.bat  |    13 +
 OSBB/RUN_INSTALL_phone_barrier_access_v2.bat       |    12 +
 .../RUN_INSTALL_profile_button_early_route_fix.bat |    11 +
 ...L_profile_confirmation_ready_visibility_fix.bat |    11 +
 OSBB/RUN_INSTALL_profile_critical_codes_fix.bat    |    11 +
 OSBB/RUN_INSTALL_profile_parking_time_test_v1.bat  |    11 +
 ...INSTALL_profile_verification_terminology_v2.bat |    11 +
 OSBB/RUN_INSTALL_profile_verification_v1.bat       |    10 +
 ...INSTALL_service_code_compatibility_phone_v2.bat |    13 +
 ...TE_phone_barrier_access_operational_sandbox.bat |    11 +
 OSBB/RUN_MIGRATE_phone_barrier_access_sandbox.bat  |    14 +
 ...N_MIGRATE_profile_parking_time_test_sandbox.bat |    11 +
 OSBB/RUN_MIGRATE_profile_verification_sandbox.bat  |    10 +
 OSBB/RUN_MIGRATE_simplified_services_sandbox.bat   |    33 +
 ...ETIRE_legacy_new_remote_test_orders_sandbox.bat |    14 +
 OSBB/RUN_fix_source_ref_schema.bat                 |    41 +
 OSBB/STOP_old_guard_sandbox_bots.bat               |    16 +
 OSBB/Start_OSBB_Guard_Sandbox_Bot_v2.bat           |    40 +
 OSBB/Start_OSBB_Live_Service_Sandbox_Bot.bat       |    37 +
 ...x_Bot_before_service_ui_2026-06-26_20-50-39.bat |    37 +
 OSBB/Start_OSBB_Live_Services_Sandbox_Bot_v1.bat   |    44 +
 OSBB/access_control.py                             |   399 +
 .../run_bot_live_services_sandbox_v1.py            |   707 +
 OSBB/cashier_v2_core.py                            |  1555 ++
 ..._before_period_schemafix_2026-06-25_23-17-38.py |  1535 ++
 ...v2_core_before_schemafix_2026-06-25_22-19-22.py |  1479 ++
 OSBB/cashier_v2_preflight.py                       |   485 +
 OSBB/cashier_v2_preflight_compat.py                |   316 +
 OSBB/commercial_contracts.py                       |  1311 ++
 OSBB/commercial_notification_delivery.py           |   255 +
 OSBB/create_clean_live_sandbox.py                  |   459 +
 OSBB/create_isolated_live_sandbox_v2.py            |   457 +
 OSBB/diagnose_osbb_audit.py                        |   332 +
 OSBB/diagnose_sandbox_charges.py                   |   206 +
 OSBB/find_sandbox_telegram_id.py                   |   148 +
 OSBB/fix_parking_bot_language_gate.py              |   142 +
 OSBB/fix_source_ref_schema.py                      |   309 +
 OSBB/guard_workspace_preflight.py                  |   336 +
 OSBB/guard_workspace_preflight_v2.py               |   336 +
 OSBB/install_service_orders_ui.py                  |   135 +
 OSBB/manage_staff_access.py                        |   449 +
 OSBB/manage_staff_access_v2.py                     |   449 +
 OSBB/migrate_access_control_and_guard.py           |   556 +
 OSBB/migrate_apartment_link_requests.py            |   202 +
 OSBB/migrate_cashier_operator_editor.py            |   557 +
 OSBB/migrate_cashier_v2.py                         |   512 +
 OSBB/migrate_cashier_v2_compat.py                  |   683 +
 OSBB/migrate_commercial_contract_core.py           |   935 +
 OSBB/migrate_remote_requests.py                    |   237 +
 OSBB/migrate_service_orders_and_fulfillment.py     |   769 +
 OSBB/migrate_unit_registry_composite_groups.py     |   785 +
 .../profile_parking_time_test_workspace.py         |   364 +
 .../profile_parking_time_test_core.py              |   827 +
 .../run_bot_live_services_sandbox_v1.py            |   918 +
 OSBB/patch_cashier_v2_core_period_and_schemafix.py |   183 +
 OSBB/patch_cashier_v2_core_schemafix.py            |   204 +
 OSBB/patch_guard_workspace_default_cash_note.py    |   180 +
 .../patch_guard_workspace_direct_notice_confirm.py |   133 +
 OSBB/patch_parking_bot_cashier_operator.py         |   211 +
 OSBB/patch_parking_bot_client_cabinet.py           |   162 +
 OSBB/patch_parking_bot_client_portal.py            |   202 +
 OSBB/patch_parking_bot_guard_workspace_v2.py       |   280 +
 OSBB/patch_parking_bot_guard_workspace_v3.py       |   256 +
 OSBB/patch_parking_bot_guard_workspace_v4.py       |   266 +
 OSBB/patch_parking_bot_launch_queues_menu.py       |   126 +
 OSBB/patch_parking_bot_service_orders_ui_v1.py     |   323 +
 OSBB/patch_parking_bot_service_orders_v1.py        |   103 +
 OSBB/phone_barrier_access_core.py                  |  2162 +++
 OSBB/phone_barrier_access_service.py               |   207 +
 .../Bots/handlers/service_orders_workspace.py      |  1613 ++
 .../phone_barrier_access_core.py                   |  2162 +++
 .../phone_barrier_access_service.py                |   207 +
 .../service_orders_core.py                         |  1337 ++
 .../service_preorders_core.py                      |  1146 ++
 OSBB/prepare_live_service_test.py                  |   343 +
 .../run_bot_live_services_sandbox_v1.py            |   864 +
 .../handlers/profile_verification_workspace.py     |   767 +
 OSBB/profile_parking_time_test_core.py             |   827 +
 OSBB/profile_verification_core.py                  |  1556 ++
 .../handlers/profile_verification_workspace.py     |   764 +
 .../handlers/profile_verification_workspace.py     |   713 +
 .../Bots/handlers/service_orders_workspace.py      |  1735 ++
 .../profile_verification_core.py                   |  1530 ++
 .../run_bot_live_services_sandbox_v1.py            |   830 +
 .../handlers/profile_verification_workspace.py     |   759 +
 .../Bots/handlers/service_orders_workspace.py      |  1742 ++
 .../profile_verification_core.py                   |  1556 ++
 OSBB/repair_confirmed_unit_seed_notes.py           |   139 +
 OSBB/restore_resident_apartment_link.py            |   320 +
 OSBB/run_bot_guard_sandbox.py                      |   235 +
 OSBB/run_bot_guard_sandbox_v2.py                   |   235 +
 OSBB/run_bot_guard_sandbox_v3.py                   |   235 +
 OSBB/run_bot_live_service_sandbox_v4.py            |   249 +
 OSBB/run_bot_live_services_sandbox_v1.py           |   918 +
 OSBB/run_bot_sandbox_v2.py                         |   285 +
 OSBB/seed_commercial_unit_placeholders.py          |   394 +
 OSBB/service_catalog_admin_core.py                 |   570 +
 .../Bots/handlers/service_orders_workspace.py      |  1631 ++
 .../service_orders_core.py                         |  1408 ++
 .../service_preorders_core.py                      |  1154 ++
 OSBB/service_orders_core.py                        |  1408 ++
 ...fore_safe_payment_policy_2026-06-26_20-50-39.py |  1125 ++
 OSBB/service_orders_preflight.py                   |   437 +
 OSBB/service_preorders_core.py                     |  1154 ++
 OSBB/switch_parking_bot_to_cashier_v2.py           |   134 +
 OSBB/test.py                                       |     1 +
 OSBB/test_db_access_unit_resolver.py               |    81 +
 OSBB/tools/INSTALL_remote_debt_gate_v1.py          |   723 +
 OSBB/tools/MIGRATE_debt_policy_rules_v1.py         |   289 +
 OSBB/tools/cashier_parking_payments_audit_v4.py    |   615 +
 OSBB/tools/cashier_unpaid_preview.py               |   202 +
 OSBB/tools/cashier_unpaid_preview_v2.py            |   259 +
 OSBB/tools/cashier_unpaid_preview_v3.py            |   579 +
 OSBB/tools/db_schema_compare.py                    |   406 +
 OSBB/tools/db_schema_snapshot.py                   |   360 +
 OSBB/tools/db_schema_snapshot_full.py              |   355 +
 OSBB/tools/db_table_passport.py                    |   626 +
 OSBB/tools/debt_policy_matrix_preview.py           |   238 +
 OSBB/tools/dump_service_codes_live_sandbox.py      |   111 +
 OSBB/tools/extract_remote_gate_sources.py          |   216 +
 OSBB/tools/project_code_search.py                  |   153 +
 OSBB/tools/project_passport.py                     |   612 +
 OSBB/tools/project_passport_v2.py                  |   657 +
 OSBB/tools/project_passport_v3_classifier.py       |   630 +
 .../project_passport_v4_runtime_schema_audit.py    |   715 +
 OSBB/tools/remote_debt_gate_audit.py               |   537 +
 OSBB/tools/remote_debt_gate_test_fixture.py        |   709 +
 OSBB/tools/show_running_osbb_bots.py               |   185 +
 OSBB/tools/start_live_services_bot.py              |    78 +
 OSBB/tools/stop_live_services_bot.py               |    98 +
 OSBB/unit_resolver.py                              |   550 +
 424 files changed, 238952 insertions(+), 211 deletions(-)
```

## Full name-status diff

```
M	.claude/cloude-code-toolbox-mcp-skills-awareness.md
M	CLAUDE.md
A	OSBB/Bots/Start_OSBB_Guard_Sandbox_Bot.bat
A	OSBB/Bots/Start_OSBB_Guard_Sandbox_Bot_v2.bat
M	OSBB/Bots/db_access.py
M	OSBB/Bots/handlers/audit_viewer - Copy.py
M	OSBB/Bots/handlers/audit_viewer.py
A	OSBB/Bots/handlers/cashier_operator.py
A	OSBB/Bots/handlers/cashier_operator_v2.py
A	OSBB/Bots/handlers/client_portal.py
A	OSBB/Bots/handlers/client_portal_safe_linking.py
A	OSBB/Bots/handlers/client_portal_v2.py
A	OSBB/Bots/handlers/client_portal_v3.py
A	OSBB/Bots/handlers/commercial_contract_editor.py
A	OSBB/Bots/handlers/guard_workspace.py
A	OSBB/Bots/handlers/guard_workspace_before_default_cash_note_2026-06-26_16-25-02.py
A	OSBB/Bots/handlers/guard_workspace_before_direct_notice_confirm_2026-06-26_18-28-39.py
A	OSBB/Bots/handlers/profile_parking_time_test_workspace.py
A	OSBB/Bots/handlers/profile_verification_workspace.py
A	OSBB/Bots/handlers/service_orders_workspace.py
A	OSBB/Bots/handlers/service_orders_workspace.py.before_phone_access_ui_fix_2026-06-27_16-47-09
A	OSBB/Bots/handlers/service_orders_workspace.py.before_phone_access_ui_fix_2026-06-27_16-52-29
A	OSBB/Bots/handlers/service_orders_workspace.py.before_phone_access_ui_fix_v3_2026-06-27_17-22-40
A	OSBB/Bots/handlers/unit_registry_editor - Copy.py
A	OSBB/Bots/handlers/unit_registry_editor.py
M	OSBB/Bots/parking_bot - Copy.py
M	OSBB/Bots/parking_bot.py
A	OSBB/Bots/parking_bot_before_cashier_editor_2026-06-25_14-45-08.py
A	OSBB/Bots/parking_bot_before_client_portal_2026-06-25_10-25-49.py
A	OSBB/Bots/parking_bot_before_language_gate_fix_2026-06-25_10-45-39.py
A	OSBB/Bots/parking_bot_before_launch_queues_menu_2026-06-25_12-21-29.py
A	OSBB/CHECK_guard_sandbox_service_orders.py
A	OSBB/CHECK_guard_sandbox_service_orders_v2.py
A	OSBB/CHECK_phone_barrier_access_operational_sandbox.py
A	OSBB/CHECK_phone_barrier_access_sandbox_schema.py
A	OSBB/CHECK_profile_button_early_route_fix.py
A	OSBB/CHECK_profile_confirmation_ready_visibility_fix.py
A	OSBB/CHECK_profile_critical_codes_fix.py
A	OSBB/CHECK_profile_parking_time_test_sandbox.py
A	OSBB/CHECK_profile_test_candidate_apartment_40.py
A	OSBB/CHECK_profile_verification_sandbox.py
A	OSBB/CHECK_profile_verification_terminology_v2.py
A	OSBB/CHECK_service_code_compatibility_phone_v2.py
A	OSBB/CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.bat
A	OSBB/CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.py
A	OSBB/Data/backups/source_code/cashier_route_repair_2026-06-27_20-04-49/run_bot_live_services_sandbox_v1.py
A	OSBB/Data/backups/source_code/parking_time_test_v1_2026-06-28_12-12-01/run_bot_live_services_sandbox_v1.py
A	OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/Bots/handlers/service_orders_workspace.py
A	OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/phone_barrier_access_core.py
A	OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/service_orders_core.py
A	OSBB/Data/backups/source_code/phone_barrier_access_v2_2026-06-27_19-37-24/service_preorders_core.py
A	OSBB/Data/backups/source_code/profile_button_early_route_2026-06-27_21-33-50/run_bot_live_services_sandbox_v1.py
A	OSBB/Data/backups/source_code/profile_confirmation_ready_visibility_2026-06-27_21-55-54/profile_verification_workspace.py
A	OSBB/Data/backups/source_code/profile_critical_codes_fix_2026-06-27_21-47-24/profile_verification_workspace.py
A	OSBB/Data/backups/source_code/profile_verification_2026-06-27_20-51-33/Bots/handlers/service_orders_workspace.py
A	OSBB/Data/backups/source_code/profile_verification_2026-06-27_20-51-33/run_bot_live_services_sandbox_v1.py
A	OSBB/Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/Bots/handlers/profile_verification_workspace.py
A	OSBB/Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/Bots/handlers/service_orders_workspace.py
A	OSBB/Data/backups/source_code/profile_verification_terminology_v2_2026-06-27_21-23-44/profile_verification_core.py
A	OSBB/Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/Bots/handlers/service_orders_workspace.py
A	OSBB/Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/service_orders_core.py
A	OSBB/Data/backups/source_code/service_code_compatibility_2026-06-27_20-20-03/service_preorders_core.py
A	OSBB/Data/backups/source_patches/remote_debt_gate_v1_2026-06-28_17-41-41/Bots/handlers/client_portal.py
A	OSBB/Data/backups/source_patches/remote_debt_gate_v1_2026-06-28_17-41-41/Bots/handlers/guard_workspace.py
A	OSBB/Data/db/backups/osbb_test_before_remote_debt_gate_fixture_2026-06-28_18-32-29.db
A	OSBB/Data/db/logs/actual_service_order_state_20260627_115724.txt
A	OSBB/Data/db/logs/guard_sandbox_service_orders_diagnosis_20260627_114522.txt
A	OSBB/Data/db/logs/guard_sandbox_service_orders_diagnosis_20260627_114911.txt
A	OSBB/Data/db/logs/guard_sandbox_service_orders_diagnosis_v2_20260627_115123.txt
A	OSBB/Data/db/logs/live_services_payment_schema_fix_20260627_122549.txt
A	OSBB/Data/db/logs/phone_barrier_access_operational_migration_2026-06-27_19-38-08.txt
A	OSBB/Data/db/logs/phone_barrier_access_schema_migration_2026-06-27_19-16-27.txt
A	OSBB/Data/db/logs/profile_parking_time_test_migration_2026-06-28_12-12-37.txt
A	OSBB/Data/db/logs/profile_verification_migration_2026-06-27_20-52-07.txt
A	OSBB/Data/db/logs/simplified_services_migration_2026-06-27_14-10-45.txt
A	OSBB/Data/db/osbb_test - Copy.db
M	OSBB/Data/db/osbb_test.db
A	OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_payment_schema_fix_20260627_122548.db
A	OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_phone_barrier_access_operational_2026-06-27_19-38-08.db
A	OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_phone_barrier_access_schema_2026-06-27_19-16-27.db
A	OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_profile_parking_time_test_2026-06-28_12-12-37.db
A	OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_profile_verification_2026-06-27_20-52-07.db
A	OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_retire_legacy_new_remote_tests_2026-06-27_13-31-55.db
A	OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_service_operator_permissions_2026-06-27_12-18-22.db
A	OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_simplified_service_permissions_2026-06-27_16-08-06.db
A	OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_simplified_services_2026-06-27_13-32-32.db
A	OSBB/Data/db/sandbox/backups/osbb_test_live_services_2026-06-26_20-13-26_before_simplified_services_2026-06-27_14-10-45.db
A	OSBB/Data/db/sandbox/cashier_v2_preflight_2026-06-25_18-53-50.txt
A	OSBB/Data/db/sandbox/cashier_v2_preflight_compat_2026-06-25_19-47-09.txt
A	OSBB/Data/db/sandbox/clean_live_sandbox_2026-06-26_20-13-26.txt
A	OSBB/Data/db/sandbox/guard_workspace_preflight_2026-06-26_12-39-50.txt
A	OSBB/Data/db/sandbox/guard_workspace_preflight_2026-06-26_12-56-09.txt
A	OSBB/Data/db/sandbox/osbb_test_cashier_v2_check_2026-06-25_18-53-50.db
A	OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db
A	OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-39-50.db
A	OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09.db
A	OSBB/Data/db/sandbox/osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09_service_orders_check_2026-06-26_19-42-50.db
A	OSBB/Data/db/sandbox/osbb_test_live_services_2026-06-26_20-13-26.db
A	OSBB/Data/db/sandbox/service_orders_preflight_2026-06-26_19-42-50.txt
A	OSBB/Data/exports/audits/registry_audit_2026-06-23_17-18-21.txt
A	OSBB/Data/exports/cashier/cashier_operator_migration_2026-06-25_14-43-23.txt
A	OSBB/Data/exports/cashier/cashier_operator_migration_2026-06-25_14-43-41.txt
A	OSBB/Data/exports/cashier/cashier_payments_audit_2026-05_2026-06_2026-06-28_15-01-16.csv
A	OSBB/Data/exports/cashier/cashier_payments_audit_2026-05_2026-06_2026-06-28_15-01-16.txt
A	OSBB/Data/exports/cashier/cashier_payments_audit_2026-05_2026-06_2026-06-28_15-01-16.xlsx
A	OSBB/Data/exports/cashier/cashier_unpaid_2026-05_2026-06_2026-06-28_14-46-09.csv
A	OSBB/Data/exports/cashier/cashier_unpaid_2026-05_2026-06_2026-06-28_14-46-09.txt
A	OSBB/Data/exports/cashier/cashier_unpaid_2026-05_2026-06_2026-06-28_14-46-09.xlsx
A	OSBB/Data/exports/cashier/cashier_v2_migration_2026-06-25_17-56-05.txt
A	OSBB/Data/exports/cashier/ohorona_list1_central_apply_2026-06-22_22-53-00.txt
A	OSBB/Data/exports/code/code_search_2026-06-28_15-20-58.txt
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/00_Project.md
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/01_File_System.md
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/02_Modules.md
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/03_Technical_Debt.md
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/04_DB_Table_References.md
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/classes.csv
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/db_table_refs.csv
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/files.csv
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/functions.csv
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/imports.csv
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/modules.csv
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/inventory/todos.csv
A	OSBB/Data/exports/code_passport/project_passport_2026-06-28_15-31-05/summary.json
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/00_Project.md
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/01_File_System.md
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/02_Modules.md
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/03_Technical_Debt.md
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/04_DB_Table_References.md
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/classes.csv
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/db_table_refs.csv
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/files.csv
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/functions.csv
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/imports.csv
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/modules.csv
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/inventory/todos.csv
A	OSBB/Data/exports/code_passport/project_passport_v2_2026-06-28_15-35-59/summary.json
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/00_Project_v3.md
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/05_Entrypoints.md
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/06_Active_Candidates.md
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/07_Legacy_Backups.md
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/08_Bot_Handlers.md
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/09_Remote_Access_Service_Modules.md
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/10_Code_Risk_Summary.md
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/entrypoints.csv
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/files_classified.csv
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/functions.csv
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/import_edges.csv
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/inventory/python_modules_classified.csv
A	OSBB/Data/exports/code_passport/project_passport_v3_2026-06-28_15-51-11/summary.json
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/00_Runtime_Schema_Audit.md
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/01_Strict_Entrypoints.md
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/02_Runtime_Import_Closure.md
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/03_Missing_Tables_From_Code.md
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/04_Remote_Access_Modules.md
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/05_Debt_Gate_Candidates.md
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/db_table_refs.csv
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/debt_gate_candidates.csv
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/missing_tables_from_code.csv
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/remote_access_modules.csv
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/runtime_import_edges.csv
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/runtime_import_nodes.csv
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/inventory/strict_entrypoints.csv
A	OSBB/Data/exports/code_passport/project_passport_v4_2026-06-28_15-56-10/summary.json
A	OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/00_Remote_Debt_Gate_Audit.md
A	OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/inventory/candidate_lines.csv
A	OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/inventory/db_status.csv
A	OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/inventory/files_scanned.csv
A	OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/inventory/functions_remote_debt_scan.csv
A	OSBB/Data/exports/code_passport/remote_debt_gate_audit_2026-06-28_16-48-56/summary.json
A	OSBB/Data/exports/code_passport/remote_gate_sources_2026-06-28_16-59-59.txt
A	OSBB/Data/exports/code_passport/running_bots_after_start.txt
A	OSBB/Data/exports/code_passport/running_bots_now.txt
A	OSBB/Data/exports/commercial/commercial_contract_core_2026-06-24_12-27-30.txt
A	OSBB/Data/exports/commercial/commercial_contract_core_2026-06-24_12-30-30.txt
A	OSBB/Data/exports/commercial/commercial_notification_queue_2026-06-24_dry_run_2026-06-24_12-32-13.txt
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/01_schema.txt
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/02_columns.csv
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/03_indexes.csv
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/04_foreign_keys.csv
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/05_code_references.csv
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/06_service_code_usage.csv
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/07_sample_rows.csv
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/08_distinct_values.txt
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/09_code_references_by_kind.txt
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/10_architecture_notes.md
A	OSBB/Data/exports/db_passports/service_catalog/gold_2026-06-28_22-23-17/passport_summary.txt
A	OSBB/Data/exports/debt_policy/debt_policy_matrix_preview_2026-06-28_20-23-44.csv
A	OSBB/Data/exports/debt_policy/debt_policy_matrix_preview_2026-06-28_20-23-44.txt
A	OSBB/Data/exports/debt_policy/service_codes_live_sandbox.txt
A	OSBB/Data/exports/diagnostics/audit_diagnostic_2026-06-24_20-17-19.txt
A	OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_10-23-49.txt
A	OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_10-24-18.txt
A	OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_11-42-17.txt
A	OSBB/Data/exports/remotes/remote_requests_migration_2026-06-25_12-05-57.txt
A	OSBB/Data/exports/schema/schema_compare_2026-06-28_13-09-32.txt
A	OSBB/Data/exports/schema/schema_snapshot_test_2026-06-28_14-30-02.txt
A	OSBB/Data/exports/units/commercial_unit_placeholders_2026-06-24_10-48-47.txt
A	OSBB/Data/exports/units/commercial_unit_placeholders_2026-06-24_10-49-12.txt
A	OSBB/Data/exports/units/composite_unit_inventory_2026-06-23_17-20-07.csv
A	OSBB/Data/exports/units/composite_unit_inventory_2026-06-23_17-20-07.txt
A	OSBB/Data/exports/units/unit_registry_aliases_2026-06-23_16-09-28.txt
A	OSBB/Data/exports/units/unit_registry_composite_groups_2026-06-23_17-36-23.txt
A	OSBB/Data/exports/units/unit_registry_composite_groups_2026-06-23_17-40-54.txt
A	OSBB/Data/exports/users/apartment_link_requests_migration_2026-06-25_11-42-33.txt
A	OSBB/Data/exports/users/apartment_link_requests_migration_2026-06-25_12-07-06.txt
A	OSBB/Data/exports/users/restore_resident_link_2026-06-25_12-51-41.txt
A	OSBB/Data/exports/users/restore_resident_link_2026-06-25_12-52-09.txt
D	"OSBB/Data/raw/typed/~$\320\236\321\205\320\276\321\200\320\276\320\275\320\260.xlsx"
A	OSBB/Docs/Architecture/Services/service_catalog_v2_design.md
A	OSBB/Docs/Architecture/Services/service_catalog_v2_design_approved_updates.md
A	OSBB/Docs/OSBB_Business_Handoff_2026-06-27.zip
A	OSBB/Docs/OSBB_Business_Handoff_2026-06-27/DO_NOT_UPLOAD_SECRETS.md
A	OSBB/Docs/OSBB_Business_Handoff_2026-06-27/OSBB_BUSINESS_HANDOFF_2026-06-27.md
A	OSBB/Docs/OSBB_Business_Handoff_2026-06-27/OSBB_PROJECT_INSTRUCTIONS.md
A	OSBB/Docs/OSBB_Business_Handoff_2026-06-27/SHA256SUMS.txt
A	OSBB/Docs/OSBB_Business_Handoff_2026-06-27/START_OSBB_BUSINESS_CHAT_2026-06-28.txt
A	OSBB/Docs/OSBB_Business_Handoff_2026-06-27/TRANSFER_CHECKLIST_2026-06-27.txt
A	OSBB/Docs/non_residential_unit_draft_template.xlsx
A	OSBB/FIND_actual_service_order_state.py
A	OSBB/FIX_live_services_sandbox_payment_schema.py
A	OSBB/INSTALL_PHONE_ACCESS_UI_FIX.bat
A	OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v2.bat
A	OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v2.py
A	OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v3.bat
A	OSBB/INSTALL_PHONE_ACCESS_UI_FIX_v3.py
A	OSBB/INSTALL_cashier_route_after_phone_v2.py
A	OSBB/INSTALL_phone_barrier_access_v2.py
A	OSBB/INSTALL_profile_button_early_route_fix.py
A	OSBB/INSTALL_profile_confirmation_ready_visibility_fix.py
A	OSBB/INSTALL_profile_critical_codes_fix.py
A	OSBB/INSTALL_profile_parking_time_test_v1.py
A	OSBB/INSTALL_profile_verification_terminology_v2.py
A	OSBB/INSTALL_profile_verification_v1.py
A	OSBB/INSTALL_service_code_compatibility_phone_v2.py
A	OSBB/MIGRATE_phone_barrier_access_operational_sandbox.py
A	OSBB/MIGRATE_phone_barrier_access_sandbox.py
A	OSBB/MIGRATE_profile_parking_time_test_sandbox.py
A	OSBB/MIGRATE_profile_verification_sandbox.py
A	OSBB/MIGRATE_simplified_services_sandbox.py
A	OSBB/OSBB_Service_Orders_Foundation_v1.zip
A	OSBB/OSBB_Service_Orders_Foundation_v1/migrate_service_orders_and_fulfillment.py
A	OSBB/OSBB_Service_Orders_Foundation_v1/service_catalog_admin_core.py
A	OSBB/OSBB_Service_Orders_Foundation_v1/service_orders_core.py
A	OSBB/OSBB_Service_Orders_Foundation_v1/service_orders_preflight.py
A	OSBB/OSBB_apartment_40_profile_test_preflight.zip
A	OSBB/OSBB_cashier_route_fix.zip
A	OSBB/OSBB_cashier_route_repair_after_phone_v2.zip
A	OSBB/OSBB_phone_access_ui_fix.zip
A	OSBB/OSBB_phone_access_ui_fix_v3.zip
A	OSBB/OSBB_phone_barrier_access_schema_migration.zip
A	OSBB/OSBB_phone_barrier_access_v2_working_sandbox.zip
A	OSBB/OSBB_profile_button_early_route_fix_v2.zip
A	OSBB/OSBB_profile_confirmation_ready_visibility_fix.zip
A	OSBB/OSBB_profile_parking_time_test_v1_sandbox.zip
A	OSBB/OSBB_profile_verification_terminology_v2 (1).zip
A	OSBB/OSBB_profile_verification_v1_sandbox_final.zip
A	OSBB/OSBB_service_code_compatibility_repair_phone_v2.zip
A	OSBB/OSBB_simplified_services_preorders_bundle.zip
A	OSBB/README_APARTMENT_40_PROFILE_TEST_PREFLIGHT.txt
A	OSBB/README_CASHIER_ROUTE_FIX.txt
A	OSBB/README_CASHIER_ROUTE_REPAIR_AFTER_PHONE_V2.txt
A	OSBB/README_LIVE_SERVICES_SANDBOX.txt
A	OSBB/README_LIVE_SERVICE_UI.txt
A	OSBB/README_PHONE_ACCESS_FIX.txt
A	OSBB/README_PHONE_ACCESS_FIX_v2.txt
A	OSBB/README_PHONE_ACCESS_FIX_v3.txt
A	OSBB/README_PHONE_BARRIER_ACCESS_SCHEMA_MIGRATION.txt
A	OSBB/README_PHONE_BARRIER_ACCESS_V2.txt
A	OSBB/README_PROFILE_BUTTON_EARLY_ROUTE_FIX.txt
A	OSBB/README_PROFILE_CONFIRMATION_READY_VISIBILITY_FIX.txt
A	OSBB/README_PROFILE_CRITICAL_CODES_FIX.txt
A	OSBB/README_PROFILE_PARKING_TIME_TEST_V1.txt
A	OSBB/README_PROFILE_VERIFICATION_TERMINOLOGY_V2.txt
A	OSBB/README_PROFILE_VERIFICATION_V1.txt
A	OSBB/README_SERVICE_CODE_COMPATIBILITY_PHONE_V2.txt
A	OSBB/README_SIMPLIFIED_SERVICES.txt
A	OSBB/RETIRE_legacy_new_remote_test_orders_sandbox.py
A	OSBB/RUN_CHECK_cashier_route_after_phone_v2.bat
A	OSBB/RUN_CHECK_guard_sandbox_service_orders.bat
A	OSBB/RUN_CHECK_guard_sandbox_service_orders_v2.bat
A	OSBB/RUN_CHECK_phone_barrier_access_operational_sandbox.bat
A	OSBB/RUN_CHECK_phone_barrier_access_sandbox_schema.bat
A	OSBB/RUN_CHECK_profile_button_early_route_fix.bat
A	OSBB/RUN_CHECK_profile_confirmation_ready_visibility_fix.bat
A	OSBB/RUN_CHECK_profile_critical_codes_fix.bat
A	OSBB/RUN_CHECK_profile_parking_time_test_sandbox.bat
A	OSBB/RUN_CHECK_profile_test_candidate_apartment_40.bat
A	OSBB/RUN_CHECK_profile_verification_sandbox.bat
A	OSBB/RUN_CHECK_profile_verification_terminology_v2.bat
A	OSBB/RUN_CHECK_service_code_compatibility_phone_v2.bat
A	OSBB/RUN_FIND_actual_service_order_state.bat
A	OSBB/RUN_FIX_live_services_sandbox_payment_schema.bat
A	OSBB/RUN_INSTALL_cashier_route_after_phone_v2.bat
A	OSBB/RUN_INSTALL_phone_barrier_access_v2.bat
A	OSBB/RUN_INSTALL_profile_button_early_route_fix.bat
A	OSBB/RUN_INSTALL_profile_confirmation_ready_visibility_fix.bat
A	OSBB/RUN_INSTALL_profile_critical_codes_fix.bat
A	OSBB/RUN_INSTALL_profile_parking_time_test_v1.bat
A	OSBB/RUN_INSTALL_profile_verification_terminology_v2.bat
A	OSBB/RUN_INSTALL_profile_verification_v1.bat
A	OSBB/RUN_INSTALL_service_code_compatibility_phone_v2.bat
A	OSBB/RUN_MIGRATE_phone_barrier_access_operational_sandbox.bat
A	OSBB/RUN_MIGRATE_phone_barrier_access_sandbox.bat
A	OSBB/RUN_MIGRATE_profile_parking_time_test_sandbox.bat
A	OSBB/RUN_MIGRATE_profile_verification_sandbox.bat
A	OSBB/RUN_MIGRATE_simplified_services_sandbox.bat
A	OSBB/RUN_RETIRE_legacy_new_remote_test_orders_sandbox.bat
A	OSBB/RUN_fix_source_ref_schema.bat
A	OSBB/STOP_old_guard_sandbox_bots.bat
A	OSBB/Start_OSBB_Guard_Sandbox_Bot_v2.bat
A	OSBB/Start_OSBB_Live_Service_Sandbox_Bot.bat
A	OSBB/Start_OSBB_Live_Service_Sandbox_Bot_before_service_ui_2026-06-26_20-50-39.bat
A	OSBB/Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
A	OSBB/access_control.py
A	OSBB/cashier_route_repair_payload/run_bot_live_services_sandbox_v1.py
A	OSBB/cashier_v2_core.py
A	OSBB/cashier_v2_core_before_period_schemafix_2026-06-25_23-17-38.py
A	OSBB/cashier_v2_core_before_schemafix_2026-06-25_22-19-22.py
A	OSBB/cashier_v2_preflight.py
A	OSBB/cashier_v2_preflight_compat.py
A	OSBB/commercial_contracts.py
A	OSBB/commercial_notification_delivery.py
A	OSBB/create_clean_live_sandbox.py
A	OSBB/create_isolated_live_sandbox_v2.py
A	OSBB/diagnose_osbb_audit.py
A	OSBB/diagnose_sandbox_charges.py
A	OSBB/find_sandbox_telegram_id.py
A	OSBB/fix_parking_bot_language_gate.py
A	OSBB/fix_source_ref_schema.py
A	OSBB/guard_workspace_preflight.py
A	OSBB/guard_workspace_preflight_v2.py
A	OSBB/install_service_orders_ui.py
A	OSBB/manage_staff_access.py
A	OSBB/manage_staff_access_v2.py
A	OSBB/migrate_access_control_and_guard.py
A	OSBB/migrate_apartment_link_requests.py
A	OSBB/migrate_cashier_operator_editor.py
A	OSBB/migrate_cashier_v2.py
A	OSBB/migrate_cashier_v2_compat.py
A	OSBB/migrate_commercial_contract_core.py
A	OSBB/migrate_remote_requests.py
A	OSBB/migrate_service_orders_and_fulfillment.py
A	OSBB/migrate_unit_registry_composite_groups.py
A	OSBB/parking_time_test_payload/Bots/handlers/profile_parking_time_test_workspace.py
A	OSBB/parking_time_test_payload/profile_parking_time_test_core.py
A	OSBB/parking_time_test_payload/run_bot_live_services_sandbox_v1.py
A	OSBB/patch_cashier_v2_core_period_and_schemafix.py
A	OSBB/patch_cashier_v2_core_schemafix.py
A	OSBB/patch_guard_workspace_default_cash_note.py
A	OSBB/patch_guard_workspace_direct_notice_confirm.py
A	OSBB/patch_parking_bot_cashier_operator.py
A	OSBB/patch_parking_bot_client_cabinet.py
A	OSBB/patch_parking_bot_client_portal.py
A	OSBB/patch_parking_bot_guard_workspace_v2.py
A	OSBB/patch_parking_bot_guard_workspace_v3.py
A	OSBB/patch_parking_bot_guard_workspace_v4.py
A	OSBB/patch_parking_bot_launch_queues_menu.py
A	OSBB/patch_parking_bot_service_orders_ui_v1.py
A	OSBB/patch_parking_bot_service_orders_v1.py
A	OSBB/phone_barrier_access_core.py
A	OSBB/phone_barrier_access_service.py
A	OSBB/phone_barrier_access_v2_payload/Bots/handlers/service_orders_workspace.py
A	OSBB/phone_barrier_access_v2_payload/phone_barrier_access_core.py
A	OSBB/phone_barrier_access_v2_payload/phone_barrier_access_service.py
A	OSBB/phone_barrier_access_v2_payload/service_orders_core.py
A	OSBB/phone_barrier_access_v2_payload/service_preorders_core.py
A	OSBB/prepare_live_service_test.py
A	OSBB/profile_button_early_route_payload/run_bot_live_services_sandbox_v1.py
A	OSBB/profile_confirmation_button_ready_payload/Bots/handlers/profile_verification_workspace.py
A	OSBB/profile_parking_time_test_core.py
A	OSBB/profile_verification_core.py
A	OSBB/profile_verification_critical_codes_payload/Bots/handlers/profile_verification_workspace.py
A	OSBB/profile_verification_payload/Bots/handlers/profile_verification_workspace.py
A	OSBB/profile_verification_payload/Bots/handlers/service_orders_workspace.py
A	OSBB/profile_verification_payload/profile_verification_core.py
A	OSBB/profile_verification_payload/run_bot_live_services_sandbox_v1.py
A	OSBB/profile_verification_terminology_v2_payload/Bots/handlers/profile_verification_workspace.py
A	OSBB/profile_verification_terminology_v2_payload/Bots/handlers/service_orders_workspace.py
A	OSBB/profile_verification_terminology_v2_payload/profile_verification_core.py
A	OSBB/repair_confirmed_unit_seed_notes.py
A	OSBB/restore_resident_apartment_link.py
A	OSBB/run_bot_guard_sandbox.py
A	OSBB/run_bot_guard_sandbox_v2.py
A	OSBB/run_bot_guard_sandbox_v3.py
A	OSBB/run_bot_live_service_sandbox_v4.py
A	OSBB/run_bot_live_services_sandbox_v1.py
A	OSBB/run_bot_sandbox_v2.py
A	OSBB/seed_commercial_unit_placeholders.py
A	OSBB/service_catalog_admin_core.py
A	OSBB/service_code_compatibility_payload/Bots/handlers/service_orders_workspace.py
A	OSBB/service_code_compatibility_payload/service_orders_core.py
A	OSBB/service_code_compatibility_payload/service_preorders_core.py
A	OSBB/service_orders_core.py
A	OSBB/service_orders_core_before_safe_payment_policy_2026-06-26_20-50-39.py
A	OSBB/service_orders_preflight.py
A	OSBB/service_preorders_core.py
A	OSBB/switch_parking_bot_to_cashier_v2.py
A	OSBB/test.py
A	OSBB/test_db_access_unit_resolver.py
A	OSBB/tools/INSTALL_remote_debt_gate_v1.py
A	OSBB/tools/MIGRATE_debt_policy_rules_v1.py
A	OSBB/tools/cashier_parking_payments_audit_v4.py
A	OSBB/tools/cashier_unpaid_preview.py
A	OSBB/tools/cashier_unpaid_preview_v2.py
A	OSBB/tools/cashier_unpaid_preview_v3.py
A	OSBB/tools/db_schema_compare.py
A	OSBB/tools/db_schema_snapshot.py
A	OSBB/tools/db_schema_snapshot_full.py
A	OSBB/tools/db_table_passport.py
A	OSBB/tools/debt_policy_matrix_preview.py
A	OSBB/tools/dump_service_codes_live_sandbox.py
A	OSBB/tools/extract_remote_gate_sources.py
A	OSBB/tools/project_code_search.py
A	OSBB/tools/project_passport.py
A	OSBB/tools/project_passport_v2.py
A	OSBB/tools/project_passport_v3_classifier.py
A	OSBB/tools/project_passport_v4_runtime_schema_audit.py
A	OSBB/tools/remote_debt_gate_audit.py
A	OSBB/tools/remote_debt_gate_test_fixture.py
A	OSBB/tools/show_running_osbb_bots.py
A	OSBB/tools/start_live_services_bot.py
A	OSBB/tools/stop_live_services_bot.py
A	OSBB/unit_resolver.py
```

## Manual review questions

1. Which sandbox DB is strongest now?
2. What schema/features exist in sandbox but not in current osbb_test.db?
3. Are there any important records in osbb_test.db that must be preserved?
4. Which smoke tests must pass before promoting a sandbox DB?
