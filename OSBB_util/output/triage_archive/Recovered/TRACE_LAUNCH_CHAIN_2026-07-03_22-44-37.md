# OSBB launch chain trace

Generated: `2026-07-03 22:44:37`
Root: `G:\Programming\Py\OSBB`

## Main hypothesis to verify

The adult service-orders UI may have worked through sandbox/live launchers that patched or wired `service_orders_workspace` into `parking_bot.py` at launch time.

## Ranked interesting files

| Rank | Score | Kind | Size KB | SHA | Modified | Markers | Path |
|---:|---:|---|---:|---|---|---|---|
| 1 | 158 | `py` | 30.9 | `c79dc72c59c7` | `2026-06-27 21:33:04` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `Data\backups\source_code\parking_time_test_v1_2026-06-28_12-12-01\run_bot_live_services_sandbox_v1.py` |
| 2 | 158 | `py` | 29.6 | `f7e5d56ecb68` | `2026-06-27 20:49:00` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `Data\backups\source_code\profile_button_early_route_2026-06-27_21-33-50\run_bot_live_services_sandbox_v1.py` |
| 3 | 158 | `py` | 33.1 | `51e635b6958c` | `2026-06-28 12:11:31` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `parking_time_test_payload\run_bot_live_services_sandbox_v1.py` |
| 4 | 158 | `py` | 8.1 | `49721c32f14f` | `2026-06-26 20:40:59` | `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db, remote_button` | `run_bot_live_service_sandbox_v4.py` |
| 5 | 158 | `py` | 30.9 | `c79dc72c59c7` | `2026-06-27 21:42:13` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `profile_button_early_route_payload\run_bot_live_services_sandbox_v1.py` |
| 6 | 158 | `py` | 29.6 | `f7e5d56ecb68` | `2026-06-27 20:49:00` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `profile_verification_payload\run_bot_live_services_sandbox_v1.py` |
| 7 | 158 | `py` | 8.1 | `49721c32f14f` | `2026-07-02 22:59:39` | `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db, remote_button` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_service_sandbox\run_bot_live_service_sandbox_v4__49721c32f14f.py` |
| 8 | 158 | `py` | 33.1 | `51e635b6958c` | `2026-07-02 22:59:36` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__51e635b6958c.py` |
| 9 | 158 | `py` | 30.9 | `c79dc72c59c7` | `2026-07-02 22:59:36` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__c79dc72c59c7.py` |
| 10 | 158 | `py` | 29.6 | `f7e5d56ecb68` | `2026-07-02 22:59:37` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__f7e5d56ecb68.py` |
| 11 | 158 | `py` | 8.1 | `49721c32f14f` | `2026-07-02 22:59:39` | `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db, remote_button` | `Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\run_bot_live_service_sandbox_v4.py` |
| 12 | 158 | `py` | 11.2 | `b14c6b81aa98` | `2026-07-02 22:59:39` | `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db, remote_button` | `Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\patch_parking_bot_service_orders_ui_v1.py` |
| 13 | 158 | `py` | 30.9 | `c79dc72c59c7` | `2026-07-02 22:59:36` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `Recovered_Releases\2026-06-27__OSBB_profile_button_early_route_fix_v2\profile_button_early_route_payload\run_bot_live_services_sandbox_v1.py` |
| 14 | 158 | `py` | 29.6 | `f7e5d56ecb68` | `2026-07-02 22:59:37` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\profile_verification_payload\run_bot_live_services_sandbox_v1.py` |
| 15 | 158 | `py` | 33.1 | `51e635b6958c` | `2026-07-02 22:59:36` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\parking_time_test_payload\run_bot_live_services_sandbox_v1.py` |
| 16 | 158 | `py` | 33.1 | `51e635b6958c` | `2026-06-28 12:11:31` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button` | `run_bot_live_services_sandbox_v1.py` |
| 17 | 150 | `py` | 11.2 | `b14c6b81aa98` | `2026-06-26 20:40:59` | `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db, remote_button` | `patch_parking_bot_service_orders_ui_v1.py` |
| 18 | 148 | `py` | 24.5 | `2c2db2c9c866` | `2026-06-27 20:00:41` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button` | `cashier_route_repair_payload\run_bot_live_services_sandbox_v1.py` |
| 19 | 148 | `py` | 24.3 | `def3aac9ee8e` | `2026-06-27 17:34:24` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button` | `Data\backups\source_code\cashier_route_repair_2026-06-27_20-04-49\run_bot_live_services_sandbox_v1.py` |
| 20 | 148 | `py` | 24.5 | `2c2db2c9c866` | `2026-06-27 20:00:41` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button` | `Data\backups\source_code\profile_verification_2026-06-27_20-51-33\run_bot_live_services_sandbox_v1.py` |
| 21 | 148 | `py` | 24.5 | `2c2db2c9c866` | `2026-07-02 22:59:37` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__2c2db2c9c866.py` |
| 22 | 148 | `py` | 24.3 | `def3aac9ee8e` | `2026-07-02 22:59:38` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__def3aac9ee8e.py` |
| 23 | 148 | `py` | 12.8 | `84a6bab32e35` | `2026-07-02 22:59:39` | `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db` | `Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\install_service_orders_ui.py` |
| 24 | 148 | `py` | 24.3 | `def3aac9ee8e` | `2026-07-02 22:59:38` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button` | `Recovered_Releases\2026-06-27__OSBB_cashier_route_fix\run_bot_live_services_sandbox_v1.py` |
| 25 | 148 | `py` | 24.5 | `2c2db2c9c866` | `2026-07-02 22:59:37` | `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button` | `Recovered_Releases\2026-06-27__OSBB_cashier_route_repair_after_phone_v2\cashier_route_repair_payload\run_bot_live_services_sandbox_v1.py` |
| 26 | 140 | `py` | 12.8 | `84a6bab32e35` | `2026-06-26 20:40:59` | `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db` | `install_service_orders_ui.py` |
| 27 | 123 | `py` | 15.3 | `93460fdabb4f` | `2026-06-27 11:43:52` | `parking_bot, service_orders_workspace, patches_in_memory, installer, sandbox_db, remote_button` | `CHECK_guard_sandbox_service_orders.py` |
| 28 | 123 | `py` | 14.1 | `97ef1dd399ce` | `2026-06-27 11:50:08` | `parking_bot, service_orders_workspace, patches_in_memory, installer, sandbox_db, remote_button` | `CHECK_guard_sandbox_service_orders_v2.py` |
| 29 | 118 | `py` | 19.8 | `1fb99c606cdb` | `2026-07-02 22:59:39` | `parking_bot, service_orders_workspace, client_portal, patches_in_memory, installer, sandbox_db` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__1fb99c606cdb.py` |
| 30 | 118 | `py` | 19.8 | `1fb99c606cdb` | `2026-07-02 22:59:39` | `parking_bot, service_orders_workspace, client_portal, patches_in_memory, installer, sandbox_db` | `Recovered_Releases\2026-06-27__OSBB_live_services_sandbox_bundle\run_bot_live_services_sandbox_v1.py` |
| 31 | 113 | `py` | 12.4 | `38850209e90a` | `2026-06-26 20:40:59` | `parking_bot, service_orders_workspace, patches_in_memory, installer, sandbox_db` | `prepare_live_service_test.py` |
| 32 | 105 | `py` | 13.8 | `a23e9644c711` | `2026-06-27 11:56:43` | `parking_bot, service_orders_workspace, patches_in_memory, installer, sandbox_db` | `FIND_actual_service_order_state.py` |
| 33 | 88 | `py` | 7.4 | `40cd02f33d4f` | `2026-06-26 17:27:16` | `parking_bot, client_portal, patches_in_memory, installer, sandbox_db` | `run_bot_guard_sandbox_v3.py` |
| 34 | 88 | `py` | 7.4 | `12bd4911eea4` | `2026-06-26 12:38:25` | `parking_bot, client_portal, patches_in_memory, installer, sandbox_db` | `run_bot_guard_sandbox.py` |
| 35 | 88 | `py` | 7.4 | `3fc3c15cb59b` | `2026-06-26 13:44:44` | `parking_bot, client_portal, patches_in_memory, installer, sandbox_db` | `run_bot_guard_sandbox_v2.py` |
| 36 | 83 | `py` | 3.1 | `07e623d30310` | `2026-07-02 22:59:39` | `parking_bot, service_orders_workspace, patches_in_memory` | `Recovered_Releases\2026-06-27__OSBB_live_services_sandbox_bundle\patch_parking_bot_service_orders_v1.py` |
| 37 | 80 | `py` | 16.6 | `4b7af3d6ab60` | `2026-06-25 18:35:51` | `parking_bot, client_portal, patches_in_memory, installer, sandbox_db` | `cashier_v2_preflight.py` |
| 38 | 80 | `py` | 1.9 | `ab47ded545cb` | `2026-06-27 21:42:12` | `client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db` | `CHECK_profile_button_early_route_fix.py` |
| 39 | 80 | `py` | 2.3 | `fdadce23cbcd` | `2026-06-27 21:42:12` | `parking_bot, client_portal, patches_in_memory, installer, sandbox_db` | `INSTALL_profile_button_early_route_fix.py` |
| 40 | 75 | `py` | 96.0 | `ff43b32733d3` | `2026-06-28 17:41:44` | `parking_bot, client_portal, handle_client_portal_text, sandbox_db, ukrainian_ui, remote_button` | `Bots\handlers\client_portal.py` |
| 41 | 75 | `py` | 3.1 | `07e623d30310` | `2026-06-27 12:15:01` | `parking_bot, service_orders_workspace, patches_in_memory` | `patch_parking_bot_service_orders_v1.py` |
| 42 | 75 | `bat` | 1.3 | `75ad4a9b988f` | `2026-06-27 16:45:04` | `service_orders_workspace, installer, sandbox_db` | `INSTALL_PHONE_ACCESS_UI_FIX.bat` |
| 43 | 70 | `py` | 4.4 | `28dadc592b16` | `2026-06-25 17:44:55` | `parking_bot, client_portal, patches_in_memory, installer` | `switch_parking_bot_to_cashier_v2.py` |
| 44 | 68 | `py` | 9.3 | `1312e7f35e0b` | `2026-06-25 21:09:41` | `parking_bot, client_portal, patches_in_memory, sandbox_db` | `run_bot_sandbox_v2.py` |
| 45 | 65 | `py` | 9.0 | `0d8d4e9fb6b3` | `2026-06-26 17:25:49` | `parking_bot, patches_in_memory, installer` | `patch_parking_bot_guard_workspace_v4.py` |
| 46 | 65 | `py` | 9.6 | `f76dd1f10258` | `2026-06-26 12:36:23` | `parking_bot, patches_in_memory, installer` | `patch_parking_bot_guard_workspace_v2.py` |
| 47 | 65 | `py` | 8.4 | `6ae388f7041a` | `2026-06-26 12:52:06` | `parking_bot, patches_in_memory, installer` | `patch_parking_bot_guard_workspace_v3.py` |
| 48 | 63 | `py` | 17.7 | `c2fb6916e07a` | `2026-07-02 18:35:54` | `patches_in_memory, installer, sandbox_db` | `tools\harvest_lost_features_from_sandboxes.py` |
| 49 | 60 | `py` | 3.4 | `373835d6b404` | `2026-06-27 20:18:29` | `service_orders_workspace, installer, sandbox_db` | `INSTALL_service_code_compatibility_phone_v2.py` |
| 50 | 55 | `py` | 47.1 | `282fb147a8fc` | `2026-06-30 20:24:15` | `client_portal, handle_client_portal_text, sandbox_db, ukrainian_ui, remote_button` | `Bots\parking_bot.py` |
| 51 | 55 | `py` | 28.5 | `8b23fc5687f3` | `2026-06-25 17:42:42` | `parking_bot, client_portal, handle_client_portal_text, ukrainian_ui` | `Bots\handlers\client_portal_v2.py` |
| 52 | 45 | `bat` | 0.4 | `348f4ca1e243` | `2026-06-27 16:50:16` | `installer, sandbox_db` | `INSTALL_PHONE_ACCESS_UI_FIX_v2.bat` |
| 53 | 45 | `bat` | 0.3 | `a77dbef10399` | `2026-06-27 17:20:35` | `installer, sandbox_db` | `INSTALL_PHONE_ACCESS_UI_FIX_v3.bat` |
| 54 | 45 | `bat` | 0.3 | `a60f1fe05e10` | `2026-06-27 20:00:41` | `installer, sandbox_db` | `RUN_INSTALL_cashier_route_after_phone_v2.bat` |
| 55 | 45 | `bat` | 0.4 | `47ff9e10d5a7` | `2026-06-27 19:31:21` | `installer, sandbox_db` | `RUN_INSTALL_phone_barrier_access_v2.bat` |
| 56 | 45 | `bat` | 0.3 | `741a23a50e94` | `2026-06-27 21:42:12` | `installer, sandbox_db` | `RUN_INSTALL_profile_button_early_route_fix.bat` |
| 57 | 45 | `bat` | 0.3 | `8f7cc69360c6` | `2026-06-27 21:55:13` | `installer, sandbox_db` | `RUN_INSTALL_profile_confirmation_ready_visibility_fix.bat` |
| 58 | 45 | `bat` | 0.3 | `f456e71c0a00` | `2026-06-27 21:45:58` | `installer, sandbox_db` | `RUN_INSTALL_profile_critical_codes_fix.bat` |
| 59 | 45 | `bat` | 0.3 | `df9e25301e89` | `2026-06-28 12:11:29` | `installer, sandbox_db` | `RUN_INSTALL_profile_parking_time_test_v1.bat` |
| 60 | 45 | `bat` | 0.3 | `34e655342372` | `2026-06-27 21:22:51` | `installer, sandbox_db` | `RUN_INSTALL_profile_verification_terminology_v2.bat` |
| 61 | 45 | `bat` | 0.3 | `e224114dac20` | `2026-06-27 20:48:59` | `installer, sandbox_db` | `RUN_INSTALL_profile_verification_v1.bat` |
| 62 | 45 | `bat` | 0.3 | `45cec96c4559` | `2026-06-27 20:18:30` | `installer, sandbox_db` | `RUN_INSTALL_service_code_compatibility_phone_v2.bat` |
| 63 | 40 | `py` | 3.7 | `31a1838dbae4` | `2026-06-27 20:18:29` | `service_orders_workspace, sandbox_db` | `CHECK_service_code_compatibility_phone_v2.py` |
| 64 | 38 | `py` | 15.4 | `1e76adf6c00e` | `2026-06-26 20:04:47` | `parking_bot, sandbox_db` | `create_clean_live_sandbox.py` |
| 65 | 38 | `py` | 15.7 | `0bb5e5ebef65` | `2026-06-26 20:12:35` | `parking_bot, sandbox_db` | `create_isolated_live_sandbox_v2.py` |
| 66 | 38 | `py` | 4.7 | `488cb403453d` | `2026-06-27 19:31:21` | `installer, sandbox_db` | `MIGRATE_phone_barrier_access_operational_sandbox.py` |
| 67 | 38 | `py` | 4.5 | `81c26d447942` | `2026-06-27 19:14:05` | `installer, sandbox_db` | `MIGRATE_phone_barrier_access_sandbox.py` |
| 68 | 38 | `py` | 2.5 | `5a90e4cb254d` | `2026-06-27 20:48:58` | `installer, sandbox_db` | `MIGRATE_profile_verification_sandbox.py` |
| 69 | 38 | `py` | 4.4 | `6557cb508eff` | `2026-06-27 14:09:06` | `installer, sandbox_db` | `MIGRATE_simplified_services_sandbox.py` |
| 70 | 38 | `py` | 4.7 | `488cb403453d` | `2026-07-02 22:59:37` | `installer, sandbox_db` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_phone_barrier_access_operational_sandbox\MIGRATE_phone_barrier_access_operational_sandbox__488cb403453d.py` |
| 71 | 38 | `py` | 4.5 | `81c26d447942` | `2026-07-02 22:59:38` | `installer, sandbox_db` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_phone_barrier_access_sandbox\MIGRATE_phone_barrier_access_sandbox__81c26d447942.py` |
| 72 | 38 | `py` | 2.5 | `5a90e4cb254d` | `2026-07-02 22:59:36` | `installer, sandbox_db` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_profile_verification_sandbox\MIGRATE_profile_verification_sandbox__5a90e4cb254d.py` |
| 73 | 38 | `py` | 2.2 | `cb84fbcee38c` | `2026-07-02 22:59:39` | `installer, sandbox_db` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_simplified_services_sandbox\MIGRATE_simplified_services_sandbox__cb84fbcee38c.py` |
| 74 | 38 | `py` | 4.5 | `81c26d447942` | `2026-07-02 22:59:38` | `installer, sandbox_db` | `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_schema_migration\MIGRATE_phone_barrier_access_sandbox.py` |
| 75 | 38 | `py` | 4.7 | `488cb403453d` | `2026-07-02 22:59:37` | `installer, sandbox_db` | `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_v2_working_sandbox\MIGRATE_phone_barrier_access_operational_sandbox.py` |
| 76 | 38 | `py` | 2.5 | `5a90e4cb254d` | `2026-07-02 22:59:36` | `installer, sandbox_db` | `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\MIGRATE_profile_verification_sandbox.py` |
| 77 | 38 | `py` | 47.2 | `68b9c00f27e8` | `2026-07-02 22:59:37` | `installer, sandbox_db` | `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\profile_verification_payload\profile_verification_core.py` |
| 78 | 38 | `py` | 2.2 | `cb84fbcee38c` | `2026-07-02 22:59:39` | `installer, sandbox_db` | `Recovered_Releases\2026-06-27__OSBB_simplified_services_preorders_bundle\MIGRATE_simplified_services_sandbox.py` |
| 79 | 38 | `py` | 24.5 | `45ab47b5a24a` | `2026-07-02 22:59:36` | `installer, sandbox_db` | `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\parking_time_test_payload\profile_parking_time_test_core.py` |
| 80 | 38 | `py` | 6.1 | `82dec2cafaa3` | `2026-07-01 12:30:15` | `installer, sandbox_db` | `tools\promote_sandbox_to_training_db.py` |
| 81 | 38 | `py` | 11.4 | `da4c2bff61a0` | `2026-06-29 22:06:34` | `installer, sandbox_db` | `tools\sandbox_switch_admin_apartment.py` |
| 82 | 38 | `py` | 2.3 | `aabb1a7d11bb` | `2026-06-28 19:19:58` | `installer, sandbox_db` | `tools\stop_live_services_bot.py` |
| 83 | 33 | `bat` | 0.9 | `e67e852d1396` | `2026-06-27 11:44:42` | `sandbox_db` | `RUN_CHECK_guard_sandbox_service_orders.bat` |
| 84 | 33 | `bat` | 0.8 | `f79c84809c86` | `2026-06-27 11:50:26` | `sandbox_db` | `RUN_CHECK_guard_sandbox_service_orders_v2.bat` |
| 85 | 33 | `bat` | 0.3 | `9d5054423fec` | `2026-06-27 19:31:23` | `sandbox_db` | `RUN_CHECK_phone_barrier_access_operational_sandbox.bat` |
| 86 | 33 | `bat` | 0.3 | `caffbf887830` | `2026-06-27 19:14:06` | `sandbox_db` | `RUN_CHECK_phone_barrier_access_sandbox_schema.bat` |
| 87 | 33 | `bat` | 0.3 | `eef720ccc049` | `2026-06-28 12:11:30` | `sandbox_db` | `RUN_CHECK_profile_parking_time_test_sandbox.bat` |
| 88 | 33 | `bat` | 0.3 | `c39c95fad8be` | `2026-06-27 20:48:59` | `sandbox_db` | `RUN_CHECK_profile_verification_sandbox.bat` |
| 89 | 33 | `bat` | 1.1 | `8ef742cf5cf6` | `2026-06-27 12:24:42` | `sandbox_db` | `RUN_FIX_live_services_sandbox_payment_schema.bat` |
| 90 | 33 | `bat` | 0.3 | `f021bfaf5110` | `2026-06-27 19:31:22` | `sandbox_db` | `RUN_MIGRATE_phone_barrier_access_operational_sandbox.bat` |
| 91 | 33 | `bat` | 0.4 | `641853fd8857` | `2026-06-27 19:14:06` | `sandbox_db` | `RUN_MIGRATE_phone_barrier_access_sandbox.bat` |
| 92 | 33 | `bat` | 0.3 | `81b1355766b8` | `2026-06-28 12:11:30` | `sandbox_db` | `RUN_MIGRATE_profile_parking_time_test_sandbox.bat` |
| 93 | 33 | `bat` | 0.3 | `dbbf2c0ece24` | `2026-06-27 20:48:59` | `sandbox_db` | `RUN_MIGRATE_profile_verification_sandbox.bat` |
| 94 | 33 | `bat` | 0.8 | `4cb3f9a902de` | `2026-06-27 13:29:00` | `sandbox_db` | `RUN_MIGRATE_simplified_services_sandbox.bat` |
| 95 | 33 | `bat` | 0.5 | `55c44a814cc2` | `2026-06-27 13:29:01` | `sandbox_db` | `RUN_RETIRE_legacy_new_remote_test_orders_sandbox.bat` |
| 96 | 33 | `bat` | 1.2 | `fdfc05def4bb` | `2026-06-26 17:28:19` | `sandbox_db` | `Start_OSBB_Guard_Sandbox_Bot_v2.bat` |
| 97 | 33 | `bat` | 1.1 | `c968b5c43bcf` | `2026-06-26 20:50:39` | `sandbox_db` | `Start_OSBB_Live_Service_Sandbox_Bot.bat` |
| 98 | 33 | `bat` | 1.0 | `9723d9d7c961` | `2026-06-27 12:15:02` | `sandbox_db` | `Start_OSBB_Live_Services_Sandbox_Bot_v1.bat` |
| 99 | 33 | `bat` | 0.7 | `fd7887cdb161` | `2026-06-27 12:15:02` | `sandbox_db` | `STOP_old_guard_sandbox_bots.bat` |
| 100 | 30 | `py` | 90.0 | `5b73b4c3a060` | `2026-06-25 14:39:13` | `installer, sandbox_db` | `Bots\handlers\cashier_operator.py` |
| 101 | 30 | `py` | 19.2 | `f9066052061a` | `2026-06-25 14:38:58` | `installer, sandbox_db` | `migrate_cashier_operator_editor.py` |
| 102 | 30 | `py` | 23.5 | `a3a2daac0227` | `2026-06-25 19:44:05` | `installer, sandbox_db` | `migrate_cashier_v2_compat.py` |
| 103 | 30 | `py` | 17.6 | `f46266059d0a` | `2026-06-25 17:39:59` | `installer, sandbox_db` | `migrate_cashier_v2.py` |
| 104 | 30 | `py` | 20.5 | `2fb3c0073893` | `2026-06-26 12:32:09` | `installer, sandbox_db` | `migrate_access_control_and_guard.py` |
| 105 | 30 | `py` | 15.0 | `78723771b5d1` | `2026-06-26 12:32:58` | `installer, sandbox_db` | `manage_staff_access.py` |
| 106 | 30 | `py` | 29.5 | `33ef6dda81b9` | `2026-06-26 19:39:26` | `installer, sandbox_db` | `migrate_service_orders_and_fulfillment.py` |
| 107 | 30 | `py` | 48.4 | `d06fa33f0c95` | `2026-06-27 21:22:51` | `installer, sandbox_db` | `profile_verification_core.py` |
| 108 | 30 | `py` | 24.5 | `45ab47b5a24a` | `2026-06-28 12:11:31` | `installer, sandbox_db` | `parking_time_test_payload\profile_parking_time_test_core.py` |
| 109 | 30 | `py` | 47.2 | `68b9c00f27e8` | `2026-06-27 20:49:00` | `installer, sandbox_db` | `profile_verification_payload\profile_verification_core.py` |
| 110 | 30 | `py` | 24.5 | `45ab47b5a24a` | `2026-06-28 12:11:31` | `installer, sandbox_db` | `profile_parking_time_test_core.py` |
| 111 | 30 | `py` | 10.3 | `0b7c94b2f975` | `2026-06-27 10:40:17` | `service_orders_workspace` | `fix_source_ref_schema.py` |
| 112 | 30 | `bat` | 1.1 | `426128b5c4f0` | `2026-06-26 20:13:28` | `sandbox_db` | `Start_OSBB_Live_Service_Sandbox_Bot_before_service_ui_2026-06-26_20-50-39.bat` |
| 113 | 28 | `py` | 3.7 | `8e4c82b70733` | `2026-06-27 19:14:06` | `sandbox_db, ukrainian_ui` | `CHECK_phone_barrier_access_sandbox_schema.py` |
| 114 | 28 | `py` | 3.7 | `8e4c82b70733` | `2026-07-02 22:59:38` | `sandbox_db, ukrainian_ui` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_phone_barrier_access_sandbox_schema\CHECK_phone_barrier_access_sandbox_schema__8e4c82b70733.py` |
| 115 | 28 | `py` | 3.7 | `8e4c82b70733` | `2026-07-02 22:59:38` | `sandbox_db, ukrainian_ui` | `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_schema_migration\CHECK_phone_barrier_access_sandbox_schema.py` |
| 116 | 25 | `bat` | 0.8 | `e6ca58918126` | `2026-06-27 12:15:02` | `sandbox_db` | `CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.bat` |
| 117 | 25 | `bat` | 0.3 | `25934662ba47` | `2026-06-27 20:00:41` | `sandbox_db` | `RUN_CHECK_cashier_route_after_phone_v2.bat` |
| 118 | 18 | `py` | 2.9 | `c22827184b78` | `2026-06-27 19:31:22` | `sandbox_db` | `CHECK_phone_barrier_access_operational_sandbox.py` |
| 119 | 18 | `py` | 2.7 | `55c1f1aa3c66` | `2026-06-28 12:11:29` | `sandbox_db` | `CHECK_profile_parking_time_test_sandbox.py` |
| 120 | 18 | `py` | 2.5 | `73286e2ac2f8` | `2026-06-27 20:48:58` | `sandbox_db` | `CHECK_profile_verification_sandbox.py` |
| 121 | 18 | `py` | 7.1 | `452ce751f633` | `2026-06-25 22:20:08` | `sandbox_db` | `diagnose_sandbox_charges.py` |
| 122 | 18 | `py` | 5.1 | `867a20b2903c` | `2026-06-26 13:45:55` | `sandbox_db` | `find_sandbox_telegram_id.py` |
| 123 | 18 | `py` | 11.2 | `80264d1a0e65` | `2026-06-27 12:24:35` | `sandbox_db` | `FIX_live_services_sandbox_payment_schema.py` |
| 124 | 18 | `py` | 3.0 | `57324665edea` | `2026-06-28 12:11:28` | `sandbox_db` | `MIGRATE_profile_parking_time_test_sandbox.py` |
| 125 | 18 | `py` | 2.9 | `c22827184b78` | `2026-07-02 22:59:38` | `sandbox_db` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_phone_barrier_access_operational_sandbox\CHECK_phone_barrier_access_operational_sandbox__c22827184b78.py` |
| 126 | 18 | `py` | 2.7 | `55c1f1aa3c66` | `2026-07-02 22:59:35` | `sandbox_db` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_profile_parking_time_test_sandbox\CHECK_profile_parking_time_test_sandbox__55c1f1aa3c66.py` |
| 127 | 18 | `py` | 2.5 | `73286e2ac2f8` | `2026-07-02 22:59:36` | `sandbox_db` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_profile_verification_sandbox\CHECK_profile_verification_sandbox__73286e2ac2f8.py` |
| 128 | 18 | `py` | 3.0 | `57324665edea` | `2026-07-02 22:59:35` | `sandbox_db` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_profile_parking_time_test_sandbox\MIGRATE_profile_parking_time_test_sandbox__57324665edea.py` |
| 129 | 18 | `py` | 4.3 | `3a3bab1d10c1` | `2026-07-02 22:59:39` | `sandbox_db` | `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\RETIRE_legacy_new_remote_test_orders_sandbox\RETIRE_legacy_new_remote_test_orders_sandbox__3a3bab1d10c1.py` |
| 130 | 18 | `py` | 2.9 | `c22827184b78` | `2026-07-02 22:59:38` | `sandbox_db` | `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_v2_working_sandbox\CHECK_phone_barrier_access_operational_sandbox.py` |
| 131 | 18 | `py` | 2.5 | `73286e2ac2f8` | `2026-07-02 22:59:36` | `sandbox_db` | `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\CHECK_profile_verification_sandbox.py` |
| 132 | 18 | `py` | 4.3 | `3a3bab1d10c1` | `2026-07-02 22:59:39` | `sandbox_db` | `Recovered_Releases\2026-06-27__OSBB_simplified_services_preorders_bundle\RETIRE_legacy_new_remote_test_orders_sandbox.py` |
| 133 | 18 | `py` | 2.7 | `55c1f1aa3c66` | `2026-07-02 22:59:35` | `sandbox_db` | `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\CHECK_profile_parking_time_test_sandbox.py` |
| 134 | 18 | `py` | 3.0 | `57324665edea` | `2026-07-02 22:59:35` | `sandbox_db` | `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\MIGRATE_profile_parking_time_test_sandbox.py` |
| 135 | 18 | `py` | 4.3 | `3a3bab1d10c1` | `2026-06-27 13:29:00` | `sandbox_db` | `RETIRE_legacy_new_remote_test_orders_sandbox.py` |
| 136 | 18 | `py` | 3.4 | `4eb7b95ad64b` | `2026-06-28 21:28:54` | `sandbox_db` | `tools\dump_service_codes_live_sandbox.py` |
| 137 | 18 | `py` | 1.9 | `b818c2430c1f` | `2026-06-28 19:20:09` | `sandbox_db` | `tools\start_live_services_bot.py` |
| 138 | 15 | `py` | 55.6 | `e0a50264b274` | `2026-06-25 23:17:40` | `client_portal, sandbox_db` | `cashier_v2_core.py` |
| 139 | 15 | `bat` | 0.3 | `59782ec1dd02` | `2026-06-27 21:42:13` | `` | `RUN_CHECK_profile_button_early_route_fix.bat` |
| 140 | 15 | `bat` | 0.3 | `ee2ad5a2ce50` | `2026-06-27 21:55:14` | `` | `RUN_CHECK_profile_confirmation_ready_visibility_fix.bat` |
| 141 | 15 | `bat` | 0.3 | `c18229d452b7` | `2026-06-27 21:45:58` | `` | `RUN_CHECK_profile_critical_codes_fix.bat` |
| 142 | 15 | `bat` | 0.3 | `c4b403c66187` | `2026-06-27 22:23:23` | `` | `RUN_CHECK_profile_test_candidate_apartment_40.bat` |
| 143 | 15 | `bat` | 0.3 | `91a7950b9d89` | `2026-06-27 21:22:51` | `` | `RUN_CHECK_profile_verification_terminology_v2.bat` |
| 144 | 15 | `bat` | 0.3 | `a510e56abde4` | `2026-06-27 20:18:30` | `` | `RUN_CHECK_service_code_compatibility_phone_v2.bat` |
| 145 | 15 | `bat` | 0.8 | `9b3a1956b363` | `2026-06-27 11:56:04` | `` | `RUN_FIND_actual_service_order_state.bat` |
| 146 | 15 | `bat` | 0.8 | `f45709673fcb` | `2026-06-27 10:41:04` | `` | `RUN_fix_source_ref_schema.bat` |
| 147 | 15 | `py` | 29.6 | `131afe386eac` | `2026-06-27 21:55:14` | `client_portal, ukrainian_ui` | `Bots\handlers\profile_verification_workspace.py` |
| 148 | 10 | `py` | 5.8 | `84207464df23` | `2026-06-17 14:57:03` | `sandbox_db` | `G:\Programming\Py\config.py` |
| 149 | 10 | `py` | 43.2 | `a67ea947627b` | `2026-07-02 22:59:37` | `ukrainian_ui` | `service_preorders_core.py` |
| 150 | 10 | `py` | 43.9 | `7c2d3ac6f66f` | `2026-07-02 22:59:37` | `sandbox_db` | `service_orders_core.py` |
| 151 | 10 | `py` | 11.1 | `e22bedb3aa11` | `2026-06-26 12:15:06` | `sandbox_db` | `access_control.py` |
| 152 | 10 | `py` | 10.2 | `3df07d574dc8` | `2026-06-27 22:23:22` | `sandbox_db` | `CHECK_profile_test_candidate_apartment_40.py` |
| 153 | 0 | `py` | 44.6 | `a0cc7e357610` | `2026-06-25 17:41:58` | `` | `Bots\handlers\cashier_operator_v2.py` |
| 154 | 0 | `py` | 18.7 | `9b34ba89291d` | `2026-06-26 19:39:26` | `` | `service_catalog_admin_core.py` |
| 155 | 0 | `py` | 1.1 | `2f6acd85e87e` | `2026-06-27 21:55:13` | `` | `CHECK_profile_confirmation_ready_visibility_fix.py` |
| 156 | 0 | `py` | 1.1 | `48d683777040` | `2026-06-27 21:45:58` | `` | `CHECK_profile_critical_codes_fix.py` |
| 157 | 0 | `py` | 2.2 | `1697bf1e439b` | `2026-06-27 21:55:12` | `` | `INSTALL_profile_confirmation_ready_visibility_fix.py` |
| 158 | 0 | `py` | 2.2 | `29396ec18d50` | `2026-06-27 21:45:58` | `` | `INSTALL_profile_critical_codes_fix.py` |

## Chains from launch roots

### `Bots\parking_bot.py`

```text
- Bots\parking_bot.py
  - Bots\handlers\client_portal.py
    - Let the existing mode switch be processed by parking_bot.py
```

### `cashier_route_repair_payload\run_bot_live_services_sandbox_v1.py`

```text
- cashier_route_repair_payload\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `CHECK_guard_sandbox_service_orders.py`

```text
- CHECK_guard_sandbox_service_orders.py
  - - parking_bot.py
  - - config.py
  - run_bot_guard_sandbox_v3.py
    - Bots\parking_bot.py
      - Bots\handlers\client_portal.py
        - Let the existing mode switch be processed by parking_bot.py
    - G:\Programming\Py\config.py
      - telegram_osbb.py
    - switch_parking_bot_to_cashier_v2.py
      - backup parking_bot.py
      - Bots\handlers\client_portal_v2.py
        - These two functions are used by parking_bot.py
      - Bots\handlers\cashier_operator_v2.py
        - Bots\handlers\cashier_operator.py
      - cashier_v2_core.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - service_orders_workspace.py
  - Raw parking_bot.py
  - Patched parking_bot.py
```

### `CHECK_guard_sandbox_service_orders_v2.py`

```text
- CHECK_guard_sandbox_service_orders_v2.py
  - - does not modify config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_guard_workspace_v4.py
    - guard_workspace.py
  - Raw parking_bot.py
  - Patched parking_bot.py
```

### `CHECK_phone_barrier_access_operational_sandbox.py`

```text
- CHECK_phone_barrier_access_operational_sandbox.py
```

### `CHECK_phone_barrier_access_sandbox_schema.py`

```text
- CHECK_phone_barrier_access_sandbox_schema.py
```

### `CHECK_profile_parking_time_test_sandbox.py`

```text
- CHECK_profile_parking_time_test_sandbox.py
```

### `CHECK_profile_verification_sandbox.py`

```text
- CHECK_profile_verification_sandbox.py
```

### `create_clean_live_sandbox.py`

```text
- create_clean_live_sandbox.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - run_bot_guard_sandbox_v3.py
    - G:\Programming\Py\config.py
      - telegram_osbb.py
    - switch_parking_bot_to_cashier_v2.py
      - backup parking_bot.py
      - Bots\handlers\client_portal_v2.py
        - These two functions are used by parking_bot.py
      - Bots\handlers\cashier_operator_v2.py
        - Bots\handlers\cashier_operator.py
      - cashier_v2_core.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - \\run_bot_guard_sandbox_v3.py
  - migrate_cashier_operator_editor.py
  - migrate_cashier_v2_compat.py
    - cashier_v2_preflight.py
      - - migrate_cashier_operator_editor.py
      - - migrate_cashier_v2.py
      - migrate_cashier_v2.py
      - client_portal.py
      - OK  cashier_v2_core.py
      - Import cashier_v2_core.py
      - ERR cashier_v2_core.py
      - OK  cashier_operator_v2.py
      - Import cashier_operator_v2.py
      - ERR cashier_operator_v2.py
      - OK  client_portal_v2.py
      - Import client_portal_v2.py
      - ERR client_portal_v2.py
      - parking_bot_v2_in_memory.py
  - migrate_access_control_and_guard.py
    - manage_staff_access.py
  - migrate_service_orders_and_fulfillment.py
```

### `create_isolated_live_sandbox_v2.py`

```text
- create_isolated_live_sandbox_v2.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - create_clean_live_sandbox.py
    - run_bot_guard_sandbox_v3.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
      - switch_parking_bot_to_cashier_v2.py
        - backup parking_bot.py
        - Bots\handlers\client_portal_v2.py
        - Bots\handlers\cashier_operator_v2.py
        - cashier_v2_core.py
      - patch_parking_bot_guard_workspace_v4.py
        - guard_workspace.py
    - \\run_bot_guard_sandbox_v3.py
    - migrate_cashier_operator_editor.py
    - migrate_cashier_v2_compat.py
      - cashier_v2_preflight.py
        - - migrate_cashier_operator_editor.py
        - - migrate_cashier_v2.py
        - migrate_cashier_v2.py
        - client_portal.py
        - Bots\handlers\cashier_operator.py
        - OK  cashier_v2_core.py
        - Import cashier_v2_core.py
        - ERR cashier_v2_core.py
        - OK  cashier_operator_v2.py
        - Import cashier_operator_v2.py
        - ERR cashier_operator_v2.py
        - OK  client_portal_v2.py
        - Import client_portal_v2.py
        - ERR client_portal_v2.py
        - parking_bot_v2_in_memory.py
    - migrate_access_control_and_guard.py
      - manage_staff_access.py
    - migrate_service_orders_and_fulfillment.py
```

### `CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.bat`

```text
- CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.bat
  - \CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.py
```

### `Data\backups\source_code\cashier_route_repair_2026-06-27_20-04-49\run_bot_live_services_sandbox_v1.py`

```text
- Data\backups\source_code\cashier_route_repair_2026-06-27_20-04-49\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Data\backups\source_code\parking_time_test_v1_2026-06-28_12-12-01\run_bot_live_services_sandbox_v1.py`

```text
- Data\backups\source_code\parking_time_test_v1_2026-06-28_12-12-01\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_core.py
  - profile_verification_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Data\backups\source_code\profile_button_early_route_2026-06-27_21-33-50\run_bot_live_services_sandbox_v1.py`

```text
- Data\backups\source_code\profile_button_early_route_2026-06-27_21-33-50\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_core.py
  - profile_verification_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Data\backups\source_code\profile_verification_2026-06-27_20-51-33\run_bot_live_services_sandbox_v1.py`

```text
- Data\backups\source_code\profile_verification_2026-06-27_20-51-33\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `diagnose_sandbox_charges.py`

```text
- diagnose_sandbox_charges.py
```

### `find_sandbox_telegram_id.py`

```text
- find_sandbox_telegram_id.py
```

### `FIX_live_services_sandbox_payment_schema.py`

```text
- FIX_live_services_sandbox_payment_schema.py
  - - config.py
```

### `INSTALL_PHONE_ACCESS_UI_FIX.bat`

```text
- INSTALL_PHONE_ACCESS_UI_FIX.bat
  - echo This installer replaces only Bots\handlers\service_orders_workspace.py
  - dp0Bots\handlers\service_orders_workspace.py
  - \Bots\handlers\service_orders_workspace.py
  - echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
```

### `INSTALL_PHONE_ACCESS_UI_FIX_v2.bat`

```text
- INSTALL_PHONE_ACCESS_UI_FIX_v2.bat
  - dp0INSTALL_PHONE_ACCESS_UI_FIX_v2.py
  - stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
```

### `INSTALL_PHONE_ACCESS_UI_FIX_v3.bat`

```text
- INSTALL_PHONE_ACCESS_UI_FIX_v3.bat
  - dp0INSTALL_PHONE_ACCESS_UI_FIX_v3.py
  - echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
```

### `MIGRATE_phone_barrier_access_operational_sandbox.py`

```text
- MIGRATE_phone_barrier_access_operational_sandbox.py
  - this script needs the updated phone_barrier_access_core.py
```

### `MIGRATE_phone_barrier_access_sandbox.py`

```text
- MIGRATE_phone_barrier_access_sandbox.py
```

### `MIGRATE_profile_parking_time_test_sandbox.py`

```text
- MIGRATE_profile_parking_time_test_sandbox.py
```

### `MIGRATE_profile_verification_sandbox.py`

```text
- MIGRATE_profile_verification_sandbox.py
```

### `MIGRATE_simplified_services_sandbox.py`

```text
- MIGRATE_simplified_services_sandbox.py
  - G:\Programming\Py\config.py
    - telegram_osbb.py
  - service_preorders_core.py
```

### `parking_time_test_payload\run_bot_live_services_sandbox_v1.py`

```text
- parking_time_test_payload\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_core.py
  - profile_verification_workspace.py
  - parking_time_test_payload\profile_parking_time_test_core.py
  - profile_parking_time_test_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `prepare_live_service_test.py`

```text
- prepare_live_service_test.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_core.py
  - service_catalog_admin_core.py
  - service_orders_workspace.py
  - install_service_orders_ui.py
    - client_portal_v3.py
    - run_bot_live_service_sandbox_v4.py
      - switch_parking_bot_to_cashier_v2.py
        - backup parking_bot.py
        - Bots\handlers\client_portal_v2.py
        - Bots\handlers\cashier_operator_v2.py
        - cashier_v2_core.py
      - patch_parking_bot_guard_workspace_v4.py
        - guard_workspace.py
      - patch_parking_bot_service_orders_ui_v1.py
        - - leaves source parking_bot.py
      - config.py or parking_bot.py
    - run_bot_guard_sandbox_v3.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - access_control.py
```

### `profile_button_early_route_payload\run_bot_live_services_sandbox_v1.py`

```text
- profile_button_early_route_payload\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_core.py
  - profile_verification_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `profile_verification_payload\run_bot_live_services_sandbox_v1.py`

```text
- profile_verification_payload\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_payload\profile_verification_core.py
  - profile_verification_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_phone_barrier_access_operational_sandbox\CHECK_phone_barrier_access_operational_sandbox__c22827184b78.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_phone_barrier_access_operational_sandbox\CHECK_phone_barrier_access_operational_sandbox__c22827184b78.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_phone_barrier_access_sandbox_schema\CHECK_phone_barrier_access_sandbox_schema__8e4c82b70733.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_phone_barrier_access_sandbox_schema\CHECK_phone_barrier_access_sandbox_schema__8e4c82b70733.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_profile_parking_time_test_sandbox\CHECK_profile_parking_time_test_sandbox__55c1f1aa3c66.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_profile_parking_time_test_sandbox\CHECK_profile_parking_time_test_sandbox__55c1f1aa3c66.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_profile_verification_sandbox\CHECK_profile_verification_sandbox__73286e2ac2f8.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_profile_verification_sandbox\CHECK_profile_verification_sandbox__73286e2ac2f8.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_phone_barrier_access_operational_sandbox\MIGRATE_phone_barrier_access_operational_sandbox__488cb403453d.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_phone_barrier_access_operational_sandbox\MIGRATE_phone_barrier_access_operational_sandbox__488cb403453d.py
  - this script needs the updated phone_barrier_access_core.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_phone_barrier_access_sandbox\MIGRATE_phone_barrier_access_sandbox__81c26d447942.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_phone_barrier_access_sandbox\MIGRATE_phone_barrier_access_sandbox__81c26d447942.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_profile_parking_time_test_sandbox\MIGRATE_profile_parking_time_test_sandbox__57324665edea.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_profile_parking_time_test_sandbox\MIGRATE_profile_parking_time_test_sandbox__57324665edea.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_profile_verification_sandbox\MIGRATE_profile_verification_sandbox__5a90e4cb254d.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_profile_verification_sandbox\MIGRATE_profile_verification_sandbox__5a90e4cb254d.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_simplified_services_sandbox\MIGRATE_simplified_services_sandbox__cb84fbcee38c.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_simplified_services_sandbox\MIGRATE_simplified_services_sandbox__cb84fbcee38c.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\RETIRE_legacy_new_remote_test_orders_sandbox\RETIRE_legacy_new_remote_test_orders_sandbox__3a3bab1d10c1.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\RETIRE_legacy_new_remote_test_orders_sandbox\RETIRE_legacy_new_remote_test_orders_sandbox__3a3bab1d10c1.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_service_sandbox\run_bot_live_service_sandbox_v4__49721c32f14f.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_service_sandbox\run_bot_live_service_sandbox_v4__49721c32f14f.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_guard_workspace_v4.py
    - guard_workspace.py
  - patch_parking_bot_service_orders_ui_v1.py
    - - leaves source parking_bot.py
    - service_orders_workspace.py
    - client_portal_v3.py
  - service_orders_core.py
  - install_service_orders_ui.py
    - run_bot_live_service_sandbox_v4.py
      - config.py or parking_bot.py
    - run_bot_guard_sandbox_v3.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__1fb99c606cdb.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__1fb99c606cdb.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__2c2db2c9c866.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__2c2db2c9c866.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__51e635b6958c.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__51e635b6958c.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_core.py
  - profile_verification_workspace.py
  - profile_parking_time_test_core.py
  - profile_parking_time_test_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__c79dc72c59c7.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__c79dc72c59c7.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_core.py
  - profile_verification_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__def3aac9ee8e.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__def3aac9ee8e.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__f7e5d56ecb68.py`

```text
- Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__f7e5d56ecb68.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_core.py
  - profile_verification_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\run_bot_live_service_sandbox_v4.py`

```text
- Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\run_bot_live_service_sandbox_v4.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_guard_workspace_v4.py
    - guard_workspace.py
  - Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\patch_parking_bot_service_orders_ui_v1.py
    - - leaves source parking_bot.py
    - service_orders_workspace.py
    - client_portal_v3.py
  - service_orders_core.py
  - Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\install_service_orders_ui.py
    - run_bot_guard_sandbox_v3.py
  - config.py or parking_bot.py
```

### `Recovered_Releases\2026-06-27__OSBB_cashier_route_fix\run_bot_live_services_sandbox_v1.py`

```text
- Recovered_Releases\2026-06-27__OSBB_cashier_route_fix\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered_Releases\2026-06-27__OSBB_cashier_route_repair_after_phone_v2\cashier_route_repair_payload\run_bot_live_services_sandbox_v1.py`

```text
- Recovered_Releases\2026-06-27__OSBB_cashier_route_repair_after_phone_v2\cashier_route_repair_payload\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered_Releases\2026-06-27__OSBB_live_services_sandbox_bundle\run_bot_live_services_sandbox_v1.py`

```text
- Recovered_Releases\2026-06-27__OSBB_live_services_sandbox_bundle\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - Recovered_Releases\2026-06-27__OSBB_live_services_sandbox_bundle\patch_parking_bot_service_orders_v1.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_schema_migration\CHECK_phone_barrier_access_sandbox_schema.py`

```text
- Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_schema_migration\CHECK_phone_barrier_access_sandbox_schema.py
```

### `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_schema_migration\MIGRATE_phone_barrier_access_sandbox.py`

```text
- Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_schema_migration\MIGRATE_phone_barrier_access_sandbox.py
```

### `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_v2_working_sandbox\CHECK_phone_barrier_access_operational_sandbox.py`

```text
- Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_v2_working_sandbox\CHECK_phone_barrier_access_operational_sandbox.py
```

### `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_v2_working_sandbox\MIGRATE_phone_barrier_access_operational_sandbox.py`

```text
- Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_v2_working_sandbox\MIGRATE_phone_barrier_access_operational_sandbox.py
  - this script needs the updated phone_barrier_access_core.py
```

### `Recovered_Releases\2026-06-27__OSBB_profile_button_early_route_fix_v2\profile_button_early_route_payload\run_bot_live_services_sandbox_v1.py`

```text
- Recovered_Releases\2026-06-27__OSBB_profile_button_early_route_fix_v2\profile_button_early_route_payload\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_core.py
  - profile_verification_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\CHECK_profile_verification_sandbox.py`

```text
- Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\CHECK_profile_verification_sandbox.py
```

### `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\MIGRATE_profile_verification_sandbox.py`

```text
- Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\MIGRATE_profile_verification_sandbox.py
```

### `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\profile_verification_payload\run_bot_live_services_sandbox_v1.py`

```text
- Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\profile_verification_payload\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\profile_verification_payload\profile_verification_core.py
  - profile_verification_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `Recovered_Releases\2026-06-27__OSBB_simplified_services_preorders_bundle\MIGRATE_simplified_services_sandbox.py`

```text
- Recovered_Releases\2026-06-27__OSBB_simplified_services_preorders_bundle\MIGRATE_simplified_services_sandbox.py
```

### `Recovered_Releases\2026-06-27__OSBB_simplified_services_preorders_bundle\RETIRE_legacy_new_remote_test_orders_sandbox.py`

```text
- Recovered_Releases\2026-06-27__OSBB_simplified_services_preorders_bundle\RETIRE_legacy_new_remote_test_orders_sandbox.py
```

### `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\CHECK_profile_parking_time_test_sandbox.py`

```text
- Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\CHECK_profile_parking_time_test_sandbox.py
```

### `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\MIGRATE_profile_parking_time_test_sandbox.py`

```text
- Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\MIGRATE_profile_parking_time_test_sandbox.py
```

### `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\parking_time_test_payload\run_bot_live_services_sandbox_v1.py`

```text
- Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\parking_time_test_payload\run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_core.py
  - profile_verification_workspace.py
  - Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\parking_time_test_payload\profile_parking_time_test_core.py
  - profile_parking_time_test_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `RETIRE_legacy_new_remote_test_orders_sandbox.py`

```text
- RETIRE_legacy_new_remote_test_orders_sandbox.py
```

### `run_bot_guard_sandbox.py`

```text
- run_bot_guard_sandbox.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - G:\Programming\Py\config.py
    - telegram_osbb.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
  - patch_parking_bot_guard_workspace_v2.py
    - guard_workspace.py
```

### `run_bot_guard_sandbox_v2.py`

```text
- run_bot_guard_sandbox_v2.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - G:\Programming\Py\config.py
    - telegram_osbb.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
  - patch_parking_bot_guard_workspace_v3.py
    - guard_workspace.py
```

### `run_bot_guard_sandbox_v3.py`

```text
- run_bot_guard_sandbox_v3.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - G:\Programming\Py\config.py
    - telegram_osbb.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
  - patch_parking_bot_guard_workspace_v4.py
    - guard_workspace.py
```

### `run_bot_live_service_sandbox_v4.py`

```text
- run_bot_live_service_sandbox_v4.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_guard_workspace_v4.py
    - guard_workspace.py
  - patch_parking_bot_service_orders_ui_v1.py
    - - leaves source parking_bot.py
    - service_orders_workspace.py
    - client_portal_v3.py
  - service_orders_core.py
  - install_service_orders_ui.py
    - run_bot_guard_sandbox_v3.py
  - config.py or parking_bot.py
```

### `run_bot_live_services_sandbox_v1.py`

```text
- run_bot_live_services_sandbox_v1.py
  - - never changes Bots\\parking_bot.py or config.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - service_orders_workspace.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
  - patch_parking_bot_service_orders_v1.py
  - profile_verification_core.py
  - profile_verification_workspace.py
  - profile_parking_time_test_core.py
  - profile_parking_time_test_workspace.py
  - run_bot_guard_sandbox_v3.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
  - Bots\\parking_bot.py and config.py
```

### `run_bot_sandbox_v2.py`

```text
- run_bot_sandbox_v2.py
  - G:\Programming\Py\config.py
    - telegram_osbb.py
  - Bots\parking_bot.py
    - Bots\handlers\client_portal.py
      - Let the existing mode switch be processed by parking_bot.py
  - switch_parking_bot_to_cashier_v2.py
    - backup parking_bot.py
    - Bots\handlers\client_portal_v2.py
      - These two functions are used by parking_bot.py
    - Bots\handlers\cashier_operator_v2.py
      - Bots\handlers\cashier_operator.py
        - migrate_cashier_operator_editor.py
    - cashier_v2_core.py
  - Must run before importing parking_bot.py
```

### `RUN_CHECK_cashier_route_after_phone_v2.bat`

```text
- RUN_CHECK_cashier_route_after_phone_v2.bat
  - \run_bot_live_services_sandbox_v1.py
```

### `RUN_CHECK_guard_sandbox_service_orders.bat`

```text
- RUN_CHECK_guard_sandbox_service_orders.bat
  - CHECK_guard_sandbox_service_orders.py
    - - parking_bot.py
    - - config.py
    - run_bot_guard_sandbox_v3.py
      - Bots\parking_bot.py
        - Bots\handlers\client_portal.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
      - switch_parking_bot_to_cashier_v2.py
        - backup parking_bot.py
        - Bots\handlers\client_portal_v2.py
        - Bots\handlers\cashier_operator_v2.py
        - cashier_v2_core.py
      - patch_parking_bot_guard_workspace_v4.py
        - guard_workspace.py
    - service_orders_workspace.py
    - Raw parking_bot.py
    - Patched parking_bot.py
  - echo Put this BAT and CHECK_guard_sandbox_service_orders.py
```

### `RUN_CHECK_guard_sandbox_service_orders_v2.bat`

```text
- RUN_CHECK_guard_sandbox_service_orders_v2.bat
  - CHECK_guard_sandbox_service_orders_v2.py
    - - does not modify config.py
    - Bots\parking_bot.py
      - Bots\handlers\client_portal.py
        - Let the existing mode switch be processed by parking_bot.py
    - service_orders_workspace.py
    - switch_parking_bot_to_cashier_v2.py
      - backup parking_bot.py
      - Bots\handlers\client_portal_v2.py
        - These two functions are used by parking_bot.py
      - Bots\handlers\cashier_operator_v2.py
        - Bots\handlers\cashier_operator.py
      - cashier_v2_core.py
        - G:\Programming\Py\config.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
    - Raw parking_bot.py
    - Patched parking_bot.py
```

### `RUN_CHECK_phone_barrier_access_operational_sandbox.bat`

```text
- RUN_CHECK_phone_barrier_access_operational_sandbox.bat
  - \CHECK_phone_barrier_access_operational_sandbox.py
```

### `RUN_CHECK_phone_barrier_access_sandbox_schema.bat`

```text
- RUN_CHECK_phone_barrier_access_sandbox_schema.bat
  - \CHECK_phone_barrier_access_sandbox_schema.py
```

### `RUN_CHECK_profile_button_early_route_fix.bat`

```text
- RUN_CHECK_profile_button_early_route_fix.bat
  - CHECK_profile_button_early_route_fix.py
    - run_bot_live_services_sandbox_v1.py
      - - never changes Bots\\parking_bot.py or config.py
      - Bots\parking_bot.py
        - Bots\handlers\client_portal.py
      - service_orders_workspace.py
      - switch_parking_bot_to_cashier_v2.py
        - backup parking_bot.py
        - Bots\handlers\client_portal_v2.py
        - Bots\handlers\cashier_operator_v2.py
        - cashier_v2_core.py
      - patch_parking_bot_service_orders_v1.py
      - profile_verification_core.py
      - profile_verification_workspace.py
      - profile_parking_time_test_core.py
      - profile_parking_time_test_workspace.py
      - run_bot_guard_sandbox_v3.py
        - G:\Programming\Py\config.py
        - patch_parking_bot_guard_workspace_v4.py
      - Bots\\parking_bot.py and config.py
```

### `RUN_CHECK_profile_confirmation_ready_visibility_fix.bat`

```text
- RUN_CHECK_profile_confirmation_ready_visibility_fix.bat
  - CHECK_profile_confirmation_ready_visibility_fix.py
    - profile_verification_workspace.py
```

### `RUN_CHECK_profile_critical_codes_fix.bat`

```text
- RUN_CHECK_profile_critical_codes_fix.bat
  - CHECK_profile_critical_codes_fix.py
    - profile_verification_workspace.py
```

### `RUN_CHECK_profile_parking_time_test_sandbox.bat`

```text
- RUN_CHECK_profile_parking_time_test_sandbox.bat
  - \CHECK_profile_parking_time_test_sandbox.py
```

### `RUN_CHECK_profile_test_candidate_apartment_40.bat`

```text
- RUN_CHECK_profile_test_candidate_apartment_40.bat
  - CHECK_profile_test_candidate_apartment_40.py
```

### `RUN_CHECK_profile_verification_sandbox.bat`

```text
- RUN_CHECK_profile_verification_sandbox.bat
  - \CHECK_profile_verification_sandbox.py
```

### `RUN_CHECK_profile_verification_terminology_v2.bat`

```text
- RUN_CHECK_profile_verification_terminology_v2.bat
  - \CHECK_profile_verification_terminology_v2.py
```

### `RUN_CHECK_service_code_compatibility_phone_v2.bat`

```text
- RUN_CHECK_service_code_compatibility_phone_v2.bat
  - CHECK_service_code_compatibility_phone_v2.py
    - service_orders_core.py
    - service_preorders_core.py
    - service_orders_workspace.py
```

### `RUN_FIND_actual_service_order_state.bat`

```text
- RUN_FIND_actual_service_order_state.bat
  - FIND_actual_service_order_state.py
    - Bots\parking_bot.py
      - Bots\handlers\client_portal.py
        - Let the existing mode switch be processed by parking_bot.py
    - service_orders_workspace.py
    - run_bot_guard_sandbox_v3.py
      - G:\Programming\Py\config.py
        - telegram_osbb.py
      - switch_parking_bot_to_cashier_v2.py
        - backup parking_bot.py
        - Bots\handlers\client_portal_v2.py
        - Bots\handlers\cashier_operator_v2.py
        - cashier_v2_core.py
      - patch_parking_bot_guard_workspace_v4.py
        - guard_workspace.py
```

### `RUN_FIX_live_services_sandbox_payment_schema.bat`

```text
- RUN_FIX_live_services_sandbox_payment_schema.bat
  - FIX_live_services_sandbox_payment_schema.py
    - - config.py
  - echo Put this BAT and FIX_live_services_sandbox_payment_schema.py
  - echo 1. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
```

### `RUN_fix_source_ref_schema.bat`

```text
- RUN_fix_source_ref_schema.bat
  - fix_source_ref_schema.py
    - 1. Reads Bots\handlers\service_orders_workspace.py
    - service_orders_workspace.py
```

### `RUN_INSTALL_cashier_route_after_phone_v2.bat`

```text
- RUN_INSTALL_cashier_route_after_phone_v2.bat
  - \INSTALL_cashier_route_after_phone_v2.py
```

### `RUN_INSTALL_phone_barrier_access_v2.bat`

```text
- RUN_INSTALL_phone_barrier_access_v2.bat
  - \INSTALL_phone_barrier_access_v2.py
  - echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
```

### `RUN_INSTALL_profile_button_early_route_fix.bat`

```text
- RUN_INSTALL_profile_button_early_route_fix.bat
  - INSTALL_profile_button_early_route_fix.py
    - Bots\parking_bot.py
      - Bots\handlers\client_portal.py
        - Let the existing mode switch be processed by parking_bot.py
    - run_bot_live_services_sandbox_v1.py
      - - never changes Bots\\parking_bot.py or config.py
      - service_orders_workspace.py
      - switch_parking_bot_to_cashier_v2.py
        - backup parking_bot.py
        - Bots\handlers\client_portal_v2.py
        - Bots\handlers\cashier_operator_v2.py
        - cashier_v2_core.py
      - patch_parking_bot_service_orders_v1.py
      - profile_verification_core.py
      - profile_verification_workspace.py
      - profile_parking_time_test_core.py
      - profile_parking_time_test_workspace.py
      - run_bot_guard_sandbox_v3.py
        - G:\Programming\Py\config.py
        - patch_parking_bot_guard_workspace_v4.py
      - Bots\\parking_bot.py and config.py
```

### `RUN_INSTALL_profile_confirmation_ready_visibility_fix.bat`

```text
- RUN_INSTALL_profile_confirmation_ready_visibility_fix.bat
  - INSTALL_profile_confirmation_ready_visibility_fix.py
    - Bots\handlers\profile_verification_workspace.py
    - profile_verification_workspace.py
```

### `RUN_INSTALL_profile_critical_codes_fix.bat`

```text
- RUN_INSTALL_profile_critical_codes_fix.bat
  - INSTALL_profile_critical_codes_fix.py
    - Bots\handlers\profile_verification_workspace.py
    - profile_verification_workspace.py
```

### `RUN_INSTALL_profile_parking_time_test_v1.bat`

```text
- RUN_INSTALL_profile_parking_time_test_v1.bat
  - \INSTALL_profile_parking_time_test_v1.py
  - echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
```

### `RUN_INSTALL_profile_verification_terminology_v2.bat`

```text
- RUN_INSTALL_profile_verification_terminology_v2.bat
  - \INSTALL_profile_verification_terminology_v2.py
```

### `RUN_INSTALL_profile_verification_v1.bat`

```text
- RUN_INSTALL_profile_verification_v1.bat
  - \INSTALL_profile_verification_v1.py
  - echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
```

### `RUN_INSTALL_service_code_compatibility_phone_v2.bat`

```text
- RUN_INSTALL_service_code_compatibility_phone_v2.bat
  - INSTALL_service_code_compatibility_phone_v2.py
    - service_orders_core.py
    - service_preorders_core.py
    - service_orders_workspace.py
```

### `RUN_MIGRATE_phone_barrier_access_operational_sandbox.bat`

```text
- RUN_MIGRATE_phone_barrier_access_operational_sandbox.bat
  - \MIGRATE_phone_barrier_access_operational_sandbox.py
  - echo SANDBOX ONLY. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
```

### `RUN_MIGRATE_phone_barrier_access_sandbox.bat`

```text
- RUN_MIGRATE_phone_barrier_access_sandbox.bat
  - \MIGRATE_phone_barrier_access_sandbox.py
  - echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
```

### `RUN_MIGRATE_profile_parking_time_test_sandbox.bat`

```text
- RUN_MIGRATE_profile_parking_time_test_sandbox.bat
  - \MIGRATE_profile_parking_time_test_sandbox.py
```

### `RUN_MIGRATE_profile_verification_sandbox.bat`

```text
- RUN_MIGRATE_profile_verification_sandbox.bat
  - \MIGRATE_profile_verification_sandbox.py
```

### `RUN_MIGRATE_simplified_services_sandbox.bat`

```text
- RUN_MIGRATE_simplified_services_sandbox.bat
  - \MIGRATE_simplified_services_sandbox.py
```

### `RUN_RETIRE_legacy_new_remote_test_orders_sandbox.bat`

```text
- RUN_RETIRE_legacy_new_remote_test_orders_sandbox.bat
  - \RETIRE_legacy_new_remote_test_orders_sandbox.py
```

### `Start_OSBB_Guard_Sandbox_Bot_v2.bat`

```text
- Start_OSBB_Guard_Sandbox_Bot_v2.bat
  - run_bot_guard_sandbox_v3.py
    - Bots\parking_bot.py
      - Bots\handlers\client_portal.py
        - Let the existing mode switch be processed by parking_bot.py
    - G:\Programming\Py\config.py
      - telegram_osbb.py
    - switch_parking_bot_to_cashier_v2.py
      - backup parking_bot.py
      - Bots\handlers\client_portal_v2.py
        - These two functions are used by parking_bot.py
      - Bots\handlers\cashier_operator_v2.py
        - Bots\handlers\cashier_operator.py
      - cashier_v2_core.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
```

### `Start_OSBB_Live_Service_Sandbox_Bot.bat`

```text
- Start_OSBB_Live_Service_Sandbox_Bot.bat
  - \run_bot_live_service_sandbox_v4.py
```

### `Start_OSBB_Live_Service_Sandbox_Bot_before_service_ui_2026-06-26_20-50-39.bat`

```text
- Start_OSBB_Live_Service_Sandbox_Bot_before_service_ui_2026-06-26_20-50-39.bat
  - run_bot_guard_sandbox_v3.py
    - Bots\parking_bot.py
      - Bots\handlers\client_portal.py
        - Let the existing mode switch be processed by parking_bot.py
    - G:\Programming\Py\config.py
      - telegram_osbb.py
    - switch_parking_bot_to_cashier_v2.py
      - backup parking_bot.py
      - Bots\handlers\client_portal_v2.py
        - These two functions are used by parking_bot.py
      - Bots\handlers\cashier_operator_v2.py
        - Bots\handlers\cashier_operator.py
      - cashier_v2_core.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
```

### `Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

```text
- Start_OSBB_Live_Services_Sandbox_Bot_v1.bat
  - \run_bot_live_services_sandbox_v1.py
  - echo Use STOP_old_guard_sandbox_bots.bat
```

### `STOP_old_guard_sandbox_bots.bat`

```text
- STOP_old_guard_sandbox_bots.bat
  - echo run_bot_guard_sandbox_v3.py
  - run_bot_guard_sandbox_v3.py
    - Bots\parking_bot.py
      - Bots\handlers\client_portal.py
        - Let the existing mode switch be processed by parking_bot.py
    - G:\Programming\Py\config.py
      - telegram_osbb.py
    - switch_parking_bot_to_cashier_v2.py
      - backup parking_bot.py
      - Bots\handlers\client_portal_v2.py
        - These two functions are used by parking_bot.py
      - Bots\handlers\cashier_operator_v2.py
        - Bots\handlers\cashier_operator.py
      - cashier_v2_core.py
    - patch_parking_bot_guard_workspace_v4.py
      - guard_workspace.py
```

### `tools\dump_service_codes_live_sandbox.py`

```text
- tools\dump_service_codes_live_sandbox.py
```

### `tools\harvest_lost_features_from_sandboxes.py`

```text
- tools\harvest_lost_features_from_sandboxes.py
```

### `tools\promote_sandbox_to_training_db.py`

```text
- tools\promote_sandbox_to_training_db.py
```

### `tools\sandbox_switch_admin_apartment.py`

```text
- tools\sandbox_switch_admin_apartment.py
```

### `tools\start_live_services_bot.py`

```text
- tools\start_live_services_bot.py
  - run_bot_live_services_sandbox_v1.py
    - - never changes Bots\\parking_bot.py or config.py
    - Bots\parking_bot.py
      - Bots\handlers\client_portal.py
        - Let the existing mode switch be processed by parking_bot.py
    - service_orders_workspace.py
    - switch_parking_bot_to_cashier_v2.py
      - backup parking_bot.py
      - Bots\handlers\client_portal_v2.py
        - These two functions are used by parking_bot.py
      - Bots\handlers\cashier_operator_v2.py
        - Bots\handlers\cashier_operator.py
      - cashier_v2_core.py
        - G:\Programming\Py\config.py
    - patch_parking_bot_service_orders_v1.py
    - profile_verification_core.py
    - profile_verification_workspace.py
    - profile_parking_time_test_core.py
    - profile_parking_time_test_workspace.py
    - run_bot_guard_sandbox_v3.py
      - patch_parking_bot_guard_workspace_v4.py
        - guard_workspace.py
    - Bots\\parking_bot.py and config.py
```

### `tools\stop_live_services_bot.py`

```text
- tools\stop_live_services_bot.py
  - run_bot_live_services_sandbox_v1.py
    - - never changes Bots\\parking_bot.py or config.py
    - Bots\parking_bot.py
      - Bots\handlers\client_portal.py
        - Let the existing mode switch be processed by parking_bot.py
    - service_orders_workspace.py
    - switch_parking_bot_to_cashier_v2.py
      - backup parking_bot.py
      - Bots\handlers\client_portal_v2.py
        - These two functions are used by parking_bot.py
      - Bots\handlers\cashier_operator_v2.py
        - Bots\handlers\cashier_operator.py
      - cashier_v2_core.py
        - G:\Programming\Py\config.py
    - patch_parking_bot_service_orders_v1.py
    - profile_verification_core.py
    - profile_verification_workspace.py
    - profile_parking_time_test_core.py
    - profile_parking_time_test_workspace.py
    - run_bot_guard_sandbox_v3.py
      - patch_parking_bot_guard_workspace_v4.py
        - guard_workspace.py
    - Bots\\parking_bot.py and config.py
```

## File details

### `Data\backups\source_code\parking_time_test_v1_2026-06-28_12-12-01\run_bot_live_services_sandbox_v1.py`

- Score: `158`
- Kind: `py`
- SHA: `c79dc72c59c7`
- Size: `31628`
- Modified: `2026-06-27 21:33:04`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
56: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
69: def clone_paths(original: Any, sandbox_db: Path) -> Any:
82:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
86: def configure_sandbox(sandbox_db: Path) -> None:
93:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
95:     if sandbox_db.resolve() in {original_test, original_prod}:
97:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
101:     config.paths = clone_paths(config.paths, sandbox_db)
103:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
104:     os.environ["OSBB_SANDBOX_MODE"] = "1"
105:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
157: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
159:     Give configured test operators only the sandbox permissions required by the
247:                 (str(user_id), SANDBOX_SERVICE_ROLE),
272:                     SANDBOX_SERVICE_ROLE,
308:                     (str(user_id), SANDBOX_SERVICE_ROLE),
320:                             SANDBOX_SERVICE_ROLE,
321:                             "Sandbox role for simplified service-workflow testing.",
348:                         SANDBOX_SERVICE_ROLE,
353:                         "Sandbox-only simplified-service workflow permission.",
393:             "В service_orders_workspace.py не установлена готовая версия "
407:         "handlers.client_portal",
408:         "handlers.client_portal_v2",
411:         "handlers.service_orders_workspace",
424:     """Patch profile verification into the bot source in memory only."""
451:         "uk": "📋 Перевірити мої дані",
535:         "    # Клиентский кабинет / заявки на пульты\n"
565: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
572:     sandbox launcher. Bots/parking_bot.py is not written to disk.
576:         "    # Клиентский кабинет / заявки на пульты\n"
591:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
601:             "Не найден следующий раздел навигации в parking_bot.py."
608:         "await handle_client_portal_text(",
618:             "В parking_bot.py не найдены обработчики для перестановки: "
632: def patch_bot_source() -> tuple[str, list[str]]:
634:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
637:     if not SERVICE_PATCHER.is_file():
638:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
645:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
646:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
648:     source, v2_changes = v2.patch(source)
649:     source, service_changes = service.patch(source)
651:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
670: def live_service_preflight(db_path: Path) -> None:
692:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
754:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
780:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
789:         help="Do not create sandbox-only service operator permissions.",
794:     print("OSBB LIVE SERVICES SANDBOX")
796:     print("Database:", LIVE_SERVICES_DB)
799:     if not LIVE_SERVICES_DB.is_file():
801:             "Не найдена live-services sandbox-БД:\n"
802:             f"  {LIVE_SERVICES_DB}"
805:     configure_sandbox(LIVE_SERVICES_DB)
806:     live_service_preflight(LIVE_SERVICES_DB)
811:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
812:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
814:             print("Sandbox backup before permission seed:", backup)
822:     source, bot_changes = patch_bot_source()
833:         print("Bots\\parking_bot.py and config.py were not changed.")
839:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
846:     print("Starting live services sandbox bot.")
848:     print(" ", LIVE_SERVICES_DB)
859:         print("\nLive services sandbox bot stopped by Ctrl+C.")
862:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Data\backups\source_code\profile_button_early_route_2026-06-27_21-33-50\run_bot_live_services_sandbox_v1.py`

- Score: `158`
- Kind: `py`
- SHA: `f7e5d56ecb68`
- Size: `30322`
- Modified: `2026-06-27 20:49:00`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
56: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
69: def clone_paths(original: Any, sandbox_db: Path) -> Any:
82:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
86: def configure_sandbox(sandbox_db: Path) -> None:
93:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
95:     if sandbox_db.resolve() in {original_test, original_prod}:
97:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
101:     config.paths = clone_paths(config.paths, sandbox_db)
103:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
104:     os.environ["OSBB_SANDBOX_MODE"] = "1"
105:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
157: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
159:     Give configured test operators only the sandbox permissions required by the
247:                 (str(user_id), SANDBOX_SERVICE_ROLE),
272:                     SANDBOX_SERVICE_ROLE,
308:                     (str(user_id), SANDBOX_SERVICE_ROLE),
320:                             SANDBOX_SERVICE_ROLE,
321:                             "Sandbox role for simplified service-workflow testing.",
348:                         SANDBOX_SERVICE_ROLE,
353:                         "Sandbox-only simplified-service workflow permission.",
393:             "В service_orders_workspace.py не установлена готовая версия "
407:         "handlers.client_portal",
408:         "handlers.client_portal_v2",
411:         "handlers.service_orders_workspace",
424:     """Patch profile verification into the bot source in memory only."""
450:         "uk": "📋 Перевірити мої дані",
502:         "    # Клиентский кабинет / заявки на пульты\n"
531: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
538:     sandbox launcher. Bots/parking_bot.py is not written to disk.
542:         "    # Клиентский кабинет / заявки на пульты\n"
557:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
567:             "Не найден следующий раздел навигации в parking_bot.py."
574:         "await handle_client_portal_text(",
584:             "В parking_bot.py не найдены обработчики для перестановки: "
598: def patch_bot_source() -> tuple[str, list[str]]:
600:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
603:     if not SERVICE_PATCHER.is_file():
604:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
611:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
612:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
614:     source, v2_changes = v2.patch(source)
615:     source, service_changes = service.patch(source)
617:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
636: def live_service_preflight(db_path: Path) -> None:
658:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
720:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
746:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
755:         help="Do not create sandbox-only service operator permissions.",
760:     print("OSBB LIVE SERVICES SANDBOX")
762:     print("Database:", LIVE_SERVICES_DB)
765:     if not LIVE_SERVICES_DB.is_file():
767:             "Не найдена live-services sandbox-БД:\n"
768:             f"  {LIVE_SERVICES_DB}"
771:     configure_sandbox(LIVE_SERVICES_DB)
772:     live_service_preflight(LIVE_SERVICES_DB)
777:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
778:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
780:             print("Sandbox backup before permission seed:", backup)
788:     source, bot_changes = patch_bot_source()
799:         print("Bots\\parking_bot.py and config.py were not changed.")
805:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
812:     print("Starting live services sandbox bot.")
814:     print(" ", LIVE_SERVICES_DB)
825:         print("\nLive services sandbox bot stopped by Ctrl+C.")
828:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `parking_time_test_payload\run_bot_live_services_sandbox_v1.py`

- Score: `158`
- Kind: `py`
- SHA: `51e635b6958c`
- Size: `33905`
- Modified: `2026-06-28 12:11:31`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\parking_time_test_payload\profile_parking_time_test_core.py`
- `profile_parking_time_test_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
60: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
73: def clone_paths(original: Any, sandbox_db: Path) -> Any:
86:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
90: def configure_sandbox(sandbox_db: Path) -> None:
97:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
99:     if sandbox_db.resolve() in {original_test, original_prod}:
101:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
105:     config.paths = clone_paths(config.paths, sandbox_db)
107:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
108:     os.environ["OSBB_SANDBOX_MODE"] = "1"
109:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
161: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
163:     Give configured test operators only the sandbox permissions required by the
251:                 (str(user_id), SANDBOX_SERVICE_ROLE),
276:                     SANDBOX_SERVICE_ROLE,
312:                     (str(user_id), SANDBOX_SERVICE_ROLE),
324:                             SANDBOX_SERVICE_ROLE,
325:                             "Sandbox role for simplified service-workflow testing.",
352:                         SANDBOX_SERVICE_ROLE,
357:                         "Sandbox-only simplified-service workflow permission.",
397:             "В service_orders_workspace.py не установлена готовая версия "
411:         "handlers.client_portal",
412:         "handlers.client_portal_v2",
415:         "handlers.service_orders_workspace",
430:     """Patch profile verification into the bot source in memory only."""
468:         "uk": "📋 Перевірити мої дані",
581:         "    # Клиентский кабинет / заявки на пульты\n"
611: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
618:     sandbox launcher. Bots/parking_bot.py is not written to disk.
622:         "    # Клиентский кабинет / заявки на пульты\n"
637:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
647:             "Не найден следующий раздел навигации в parking_bot.py."
654:         "await handle_client_portal_text(",
664:             "В parking_bot.py не найдены обработчики для перестановки: "
678: def patch_bot_source() -> tuple[str, list[str]]:
680:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
683:     if not SERVICE_PATCHER.is_file():
684:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
697:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
698:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
700:     source, v2_changes = v2.patch(source)
701:     source, service_changes = service.patch(source)
703:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
722: def live_service_preflight(db_path: Path) -> None:
746:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
808:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
834:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
843:         help="Do not create sandbox-only service operator permissions.",
848:     print("OSBB LIVE SERVICES SANDBOX")
850:     print("Database:", LIVE_SERVICES_DB)
853:     if not LIVE_SERVICES_DB.is_file():
855:             "Не найдена live-services sandbox-БД:\n"
856:             f"  {LIVE_SERVICES_DB}"
859:     configure_sandbox(LIVE_SERVICES_DB)
860:     live_service_preflight(LIVE_SERVICES_DB)
865:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
866:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
868:             print("Sandbox backup before permission seed:", backup)
876:     source, bot_changes = patch_bot_source()
887:         print("Bots\\parking_bot.py and config.py were not changed.")
893:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
900:     print("Starting live services sandbox bot.")
902:     print(" ", LIVE_SERVICES_DB)
913:         print("\nLive services sandbox bot stopped by Ctrl+C.")
916:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `run_bot_live_service_sandbox_v4.py`

- Score: `158`
- Kind: `py`
- SHA: `49721c32f14f`
- Size: `8293`
- Modified: `2026-06-26 20:40:59`
- Markers: `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_guard_workspace_v4.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_ui_v1.py`
- `G:\Programming\Py\OSBB\service_orders_core.py`
- `guard_workspace.py`
- `client_portal_v3.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\install_service_orders_ui.py`
- `config.py or parking_bot.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from pathlib import Path`
- `from types import SimpleNamespace`
- `from typing import Any`
- `import config`

Interesting lines:
```text
2: Запуск изолированной live sandbox с кабинетами:
3: - житель: «Пульты и доступ»;
7: Все изменения Bots/parking_bot.py выполняются только в памяти текущего процесса.
8: Работает исключительно с указанной .db внутри Data\db\sandbox.
27: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
28: BOT_FILE = BOTS / "parking_bot.py"
30: GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v4.py"
31: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_ui_v1.py"
45: def inside_sandbox(path: Path) -> Path:
48:         resolved.relative_to(SANDBOX_DIR.resolve())
51:             "Для запуска разрешены только .db внутри Data\\db\\sandbox."
56: def clone_paths(original: Any, sandbox_db: Path):
70:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
74: def configure_sandbox(sandbox_db: Path) -> None:
81:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
83:     if sandbox_db in {original_test, original_prod}:
84:         raise RuntimeError("Отказ: указан путь рабочей базы, а не sandbox-копии.")
86:     config.paths = clone_paths(config.paths, sandbox_db)
88:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
89:     os.environ["OSBB_SANDBOX_MODE"] = "1"
92: def table_rows(sandbox_db: Path) -> dict[str, int]:
106:     conn = sqlite3.connect(sandbox_db)
129:         GUARD_PATCHER,
130:         SERVICE_PATCHER,
133:         BOTS / "handlers" / "client_portal_v3.py",
134:         BOTS / "handlers" / "service_orders_workspace.py",
138: def patched_source() -> tuple[str, list[str], list[str], list[str]]:
146:             "Сначала выполните install_service_orders_ui.py --apply."
149:     v2 = load_module(V2_SWITCHER, "_live_service_v2_switcher")
150:     guard = load_module(GUARD_PATCHER, "_live_service_guard_patcher")
151:     service = load_module(SERVICE_PATCHER, "_live_service_ui_patcher")
154:     source, v2_changes = v2.patch(source)
155:     source, guard_changes = guard.patch(source)
156:     source, service_changes = service.patch(source)
173:             "handlers.client_portal",
174:             "handlers.client_portal_v2",
175:             "handlers.client_portal_v3",
179:             "handlers.service_orders_workspace",
188:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
193:     parser.add_argument("--sandbox", required=True)
197:     sandbox_db = inside_sandbox(Path(args.sandbox))
198:     if not sandbox_db.exists():
199:         raise SystemExit(f"Не найдена sandbox-БД: {sandbox_db}")
202:     print("OSBB LIVE SERVICE SANDBOX BOT V4")
204:     print("Sandbox DB:", sandbox_db)
208:         summary = table_rows(sandbox_db)
212:                 "Sandbox не подготовлен для услуг/пультов. Нет таблиц: "
216:         print("\nSandbox rows:")
220:         configure_sandbox(sandbox_db)
221:         source, v2_changes, guard_changes, service_changes = patched_source()
222:         print("\nRuntime patches:")
230:             print("No database, config.py or parking_bot.py was changed.")
234:         print("All new records will be written only to:", sandbox_db)
235:         print("Stop this sandbox bot with Ctrl+C.\n")
240:         print("\nLive service sandbox bot stopped by Ctrl+C.")
243:         print("\nLIVE SERVICE SANDBOX LAUNCH FAILED")
```

### `profile_button_early_route_payload\run_bot_live_services_sandbox_v1.py`

- Score: `158`
- Kind: `py`
- SHA: `c79dc72c59c7`
- Size: `31628`
- Modified: `2026-06-27 21:42:13`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
56: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
69: def clone_paths(original: Any, sandbox_db: Path) -> Any:
82:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
86: def configure_sandbox(sandbox_db: Path) -> None:
93:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
95:     if sandbox_db.resolve() in {original_test, original_prod}:
97:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
101:     config.paths = clone_paths(config.paths, sandbox_db)
103:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
104:     os.environ["OSBB_SANDBOX_MODE"] = "1"
105:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
157: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
159:     Give configured test operators only the sandbox permissions required by the
247:                 (str(user_id), SANDBOX_SERVICE_ROLE),
272:                     SANDBOX_SERVICE_ROLE,
308:                     (str(user_id), SANDBOX_SERVICE_ROLE),
320:                             SANDBOX_SERVICE_ROLE,
321:                             "Sandbox role for simplified service-workflow testing.",
348:                         SANDBOX_SERVICE_ROLE,
353:                         "Sandbox-only simplified-service workflow permission.",
393:             "В service_orders_workspace.py не установлена готовая версия "
407:         "handlers.client_portal",
408:         "handlers.client_portal_v2",
411:         "handlers.service_orders_workspace",
424:     """Patch profile verification into the bot source in memory only."""
451:         "uk": "📋 Перевірити мої дані",
535:         "    # Клиентский кабинет / заявки на пульты\n"
565: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
572:     sandbox launcher. Bots/parking_bot.py is not written to disk.
576:         "    # Клиентский кабинет / заявки на пульты\n"
591:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
601:             "Не найден следующий раздел навигации в parking_bot.py."
608:         "await handle_client_portal_text(",
618:             "В parking_bot.py не найдены обработчики для перестановки: "
632: def patch_bot_source() -> tuple[str, list[str]]:
634:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
637:     if not SERVICE_PATCHER.is_file():
638:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
645:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
646:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
648:     source, v2_changes = v2.patch(source)
649:     source, service_changes = service.patch(source)
651:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
670: def live_service_preflight(db_path: Path) -> None:
692:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
754:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
780:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
789:         help="Do not create sandbox-only service operator permissions.",
794:     print("OSBB LIVE SERVICES SANDBOX")
796:     print("Database:", LIVE_SERVICES_DB)
799:     if not LIVE_SERVICES_DB.is_file():
801:             "Не найдена live-services sandbox-БД:\n"
802:             f"  {LIVE_SERVICES_DB}"
805:     configure_sandbox(LIVE_SERVICES_DB)
806:     live_service_preflight(LIVE_SERVICES_DB)
811:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
812:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
814:             print("Sandbox backup before permission seed:", backup)
822:     source, bot_changes = patch_bot_source()
833:         print("Bots\\parking_bot.py and config.py were not changed.")
839:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
846:     print("Starting live services sandbox bot.")
848:     print(" ", LIVE_SERVICES_DB)
859:         print("\nLive services sandbox bot stopped by Ctrl+C.")
862:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `profile_verification_payload\run_bot_live_services_sandbox_v1.py`

- Score: `158`
- Kind: `py`
- SHA: `f7e5d56ecb68`
- Size: `30322`
- Modified: `2026-06-27 20:49:00`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_payload\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
56: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
69: def clone_paths(original: Any, sandbox_db: Path) -> Any:
82:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
86: def configure_sandbox(sandbox_db: Path) -> None:
93:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
95:     if sandbox_db.resolve() in {original_test, original_prod}:
97:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
101:     config.paths = clone_paths(config.paths, sandbox_db)
103:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
104:     os.environ["OSBB_SANDBOX_MODE"] = "1"
105:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
157: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
159:     Give configured test operators only the sandbox permissions required by the
247:                 (str(user_id), SANDBOX_SERVICE_ROLE),
272:                     SANDBOX_SERVICE_ROLE,
308:                     (str(user_id), SANDBOX_SERVICE_ROLE),
320:                             SANDBOX_SERVICE_ROLE,
321:                             "Sandbox role for simplified service-workflow testing.",
348:                         SANDBOX_SERVICE_ROLE,
353:                         "Sandbox-only simplified-service workflow permission.",
393:             "В service_orders_workspace.py не установлена готовая версия "
407:         "handlers.client_portal",
408:         "handlers.client_portal_v2",
411:         "handlers.service_orders_workspace",
424:     """Patch profile verification into the bot source in memory only."""
450:         "uk": "📋 Перевірити мої дані",
502:         "    # Клиентский кабинет / заявки на пульты\n"
531: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
538:     sandbox launcher. Bots/parking_bot.py is not written to disk.
542:         "    # Клиентский кабинет / заявки на пульты\n"
557:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
567:             "Не найден следующий раздел навигации в parking_bot.py."
574:         "await handle_client_portal_text(",
584:             "В parking_bot.py не найдены обработчики для перестановки: "
598: def patch_bot_source() -> tuple[str, list[str]]:
600:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
603:     if not SERVICE_PATCHER.is_file():
604:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
611:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
612:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
614:     source, v2_changes = v2.patch(source)
615:     source, service_changes = service.patch(source)
617:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
636: def live_service_preflight(db_path: Path) -> None:
658:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
720:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
746:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
755:         help="Do not create sandbox-only service operator permissions.",
760:     print("OSBB LIVE SERVICES SANDBOX")
762:     print("Database:", LIVE_SERVICES_DB)
765:     if not LIVE_SERVICES_DB.is_file():
767:             "Не найдена live-services sandbox-БД:\n"
768:             f"  {LIVE_SERVICES_DB}"
771:     configure_sandbox(LIVE_SERVICES_DB)
772:     live_service_preflight(LIVE_SERVICES_DB)
777:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
778:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
780:             print("Sandbox backup before permission seed:", backup)
788:     source, bot_changes = patch_bot_source()
799:         print("Bots\\parking_bot.py and config.py were not changed.")
805:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
812:     print("Starting live services sandbox bot.")
814:     print(" ", LIVE_SERVICES_DB)
825:         print("\nLive services sandbox bot stopped by Ctrl+C.")
828:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_service_sandbox\run_bot_live_service_sandbox_v4__49721c32f14f.py`

- Score: `158`
- Kind: `py`
- SHA: `49721c32f14f`
- Size: `8293`
- Modified: `2026-07-02 22:59:39`
- Markers: `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_guard_workspace_v4.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_ui_v1.py`
- `G:\Programming\Py\OSBB\service_orders_core.py`
- `guard_workspace.py`
- `client_portal_v3.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\install_service_orders_ui.py`
- `config.py or parking_bot.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from pathlib import Path`
- `from types import SimpleNamespace`
- `from typing import Any`
- `import config`

Interesting lines:
```text
2: Запуск изолированной live sandbox с кабинетами:
3: - житель: «Пульты и доступ»;
7: Все изменения Bots/parking_bot.py выполняются только в памяти текущего процесса.
8: Работает исключительно с указанной .db внутри Data\db\sandbox.
27: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
28: BOT_FILE = BOTS / "parking_bot.py"
30: GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v4.py"
31: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_ui_v1.py"
45: def inside_sandbox(path: Path) -> Path:
48:         resolved.relative_to(SANDBOX_DIR.resolve())
51:             "Для запуска разрешены только .db внутри Data\\db\\sandbox."
56: def clone_paths(original: Any, sandbox_db: Path):
70:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
74: def configure_sandbox(sandbox_db: Path) -> None:
81:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
83:     if sandbox_db in {original_test, original_prod}:
84:         raise RuntimeError("Отказ: указан путь рабочей базы, а не sandbox-копии.")
86:     config.paths = clone_paths(config.paths, sandbox_db)
88:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
89:     os.environ["OSBB_SANDBOX_MODE"] = "1"
92: def table_rows(sandbox_db: Path) -> dict[str, int]:
106:     conn = sqlite3.connect(sandbox_db)
129:         GUARD_PATCHER,
130:         SERVICE_PATCHER,
133:         BOTS / "handlers" / "client_portal_v3.py",
134:         BOTS / "handlers" / "service_orders_workspace.py",
138: def patched_source() -> tuple[str, list[str], list[str], list[str]]:
146:             "Сначала выполните install_service_orders_ui.py --apply."
149:     v2 = load_module(V2_SWITCHER, "_live_service_v2_switcher")
150:     guard = load_module(GUARD_PATCHER, "_live_service_guard_patcher")
151:     service = load_module(SERVICE_PATCHER, "_live_service_ui_patcher")
154:     source, v2_changes = v2.patch(source)
155:     source, guard_changes = guard.patch(source)
156:     source, service_changes = service.patch(source)
173:             "handlers.client_portal",
174:             "handlers.client_portal_v2",
175:             "handlers.client_portal_v3",
179:             "handlers.service_orders_workspace",
188:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
193:     parser.add_argument("--sandbox", required=True)
197:     sandbox_db = inside_sandbox(Path(args.sandbox))
198:     if not sandbox_db.exists():
199:         raise SystemExit(f"Не найдена sandbox-БД: {sandbox_db}")
202:     print("OSBB LIVE SERVICE SANDBOX BOT V4")
204:     print("Sandbox DB:", sandbox_db)
208:         summary = table_rows(sandbox_db)
212:                 "Sandbox не подготовлен для услуг/пультов. Нет таблиц: "
216:         print("\nSandbox rows:")
220:         configure_sandbox(sandbox_db)
221:         source, v2_changes, guard_changes, service_changes = patched_source()
222:         print("\nRuntime patches:")
230:             print("No database, config.py or parking_bot.py was changed.")
234:         print("All new records will be written only to:", sandbox_db)
235:         print("Stop this sandbox bot with Ctrl+C.\n")
240:         print("\nLive service sandbox bot stopped by Ctrl+C.")
243:         print("\nLIVE SERVICE SANDBOX LAUNCH FAILED")
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__51e635b6958c.py`

- Score: `158`
- Kind: `py`
- SHA: `51e635b6958c`
- Size: `33905`
- Modified: `2026-07-02 22:59:36`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\profile_parking_time_test_core.py`
- `profile_parking_time_test_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
60: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
73: def clone_paths(original: Any, sandbox_db: Path) -> Any:
86:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
90: def configure_sandbox(sandbox_db: Path) -> None:
97:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
99:     if sandbox_db.resolve() in {original_test, original_prod}:
101:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
105:     config.paths = clone_paths(config.paths, sandbox_db)
107:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
108:     os.environ["OSBB_SANDBOX_MODE"] = "1"
109:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
161: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
163:     Give configured test operators only the sandbox permissions required by the
251:                 (str(user_id), SANDBOX_SERVICE_ROLE),
276:                     SANDBOX_SERVICE_ROLE,
312:                     (str(user_id), SANDBOX_SERVICE_ROLE),
324:                             SANDBOX_SERVICE_ROLE,
325:                             "Sandbox role for simplified service-workflow testing.",
352:                         SANDBOX_SERVICE_ROLE,
357:                         "Sandbox-only simplified-service workflow permission.",
397:             "В service_orders_workspace.py не установлена готовая версия "
411:         "handlers.client_portal",
412:         "handlers.client_portal_v2",
415:         "handlers.service_orders_workspace",
430:     """Patch profile verification into the bot source in memory only."""
468:         "uk": "📋 Перевірити мої дані",
581:         "    # Клиентский кабинет / заявки на пульты\n"
611: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
618:     sandbox launcher. Bots/parking_bot.py is not written to disk.
622:         "    # Клиентский кабинет / заявки на пульты\n"
637:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
647:             "Не найден следующий раздел навигации в parking_bot.py."
654:         "await handle_client_portal_text(",
664:             "В parking_bot.py не найдены обработчики для перестановки: "
678: def patch_bot_source() -> tuple[str, list[str]]:
680:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
683:     if not SERVICE_PATCHER.is_file():
684:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
697:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
698:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
700:     source, v2_changes = v2.patch(source)
701:     source, service_changes = service.patch(source)
703:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
722: def live_service_preflight(db_path: Path) -> None:
746:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
808:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
834:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
843:         help="Do not create sandbox-only service operator permissions.",
848:     print("OSBB LIVE SERVICES SANDBOX")
850:     print("Database:", LIVE_SERVICES_DB)
853:     if not LIVE_SERVICES_DB.is_file():
855:             "Не найдена live-services sandbox-БД:\n"
856:             f"  {LIVE_SERVICES_DB}"
859:     configure_sandbox(LIVE_SERVICES_DB)
860:     live_service_preflight(LIVE_SERVICES_DB)
865:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
866:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
868:             print("Sandbox backup before permission seed:", backup)
876:     source, bot_changes = patch_bot_source()
887:         print("Bots\\parking_bot.py and config.py were not changed.")
893:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
900:     print("Starting live services sandbox bot.")
902:     print(" ", LIVE_SERVICES_DB)
913:         print("\nLive services sandbox bot stopped by Ctrl+C.")
916:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__c79dc72c59c7.py`

- Score: `158`
- Kind: `py`
- SHA: `c79dc72c59c7`
- Size: `31628`
- Modified: `2026-07-02 22:59:36`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
56: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
69: def clone_paths(original: Any, sandbox_db: Path) -> Any:
82:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
86: def configure_sandbox(sandbox_db: Path) -> None:
93:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
95:     if sandbox_db.resolve() in {original_test, original_prod}:
97:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
101:     config.paths = clone_paths(config.paths, sandbox_db)
103:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
104:     os.environ["OSBB_SANDBOX_MODE"] = "1"
105:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
157: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
159:     Give configured test operators only the sandbox permissions required by the
247:                 (str(user_id), SANDBOX_SERVICE_ROLE),
272:                     SANDBOX_SERVICE_ROLE,
308:                     (str(user_id), SANDBOX_SERVICE_ROLE),
320:                             SANDBOX_SERVICE_ROLE,
321:                             "Sandbox role for simplified service-workflow testing.",
348:                         SANDBOX_SERVICE_ROLE,
353:                         "Sandbox-only simplified-service workflow permission.",
393:             "В service_orders_workspace.py не установлена готовая версия "
407:         "handlers.client_portal",
408:         "handlers.client_portal_v2",
411:         "handlers.service_orders_workspace",
424:     """Patch profile verification into the bot source in memory only."""
451:         "uk": "📋 Перевірити мої дані",
535:         "    # Клиентский кабинет / заявки на пульты\n"
565: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
572:     sandbox launcher. Bots/parking_bot.py is not written to disk.
576:         "    # Клиентский кабинет / заявки на пульты\n"
591:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
601:             "Не найден следующий раздел навигации в parking_bot.py."
608:         "await handle_client_portal_text(",
618:             "В parking_bot.py не найдены обработчики для перестановки: "
632: def patch_bot_source() -> tuple[str, list[str]]:
634:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
637:     if not SERVICE_PATCHER.is_file():
638:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
645:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
646:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
648:     source, v2_changes = v2.patch(source)
649:     source, service_changes = service.patch(source)
651:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
670: def live_service_preflight(db_path: Path) -> None:
692:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
754:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
780:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
789:         help="Do not create sandbox-only service operator permissions.",
794:     print("OSBB LIVE SERVICES SANDBOX")
796:     print("Database:", LIVE_SERVICES_DB)
799:     if not LIVE_SERVICES_DB.is_file():
801:             "Не найдена live-services sandbox-БД:\n"
802:             f"  {LIVE_SERVICES_DB}"
805:     configure_sandbox(LIVE_SERVICES_DB)
806:     live_service_preflight(LIVE_SERVICES_DB)
811:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
812:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
814:             print("Sandbox backup before permission seed:", backup)
822:     source, bot_changes = patch_bot_source()
833:         print("Bots\\parking_bot.py and config.py were not changed.")
839:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
846:     print("Starting live services sandbox bot.")
848:     print(" ", LIVE_SERVICES_DB)
859:         print("\nLive services sandbox bot stopped by Ctrl+C.")
862:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__f7e5d56ecb68.py`

- Score: `158`
- Kind: `py`
- SHA: `f7e5d56ecb68`
- Size: `30322`
- Modified: `2026-07-02 22:59:37`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
56: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
69: def clone_paths(original: Any, sandbox_db: Path) -> Any:
82:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
86: def configure_sandbox(sandbox_db: Path) -> None:
93:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
95:     if sandbox_db.resolve() in {original_test, original_prod}:
97:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
101:     config.paths = clone_paths(config.paths, sandbox_db)
103:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
104:     os.environ["OSBB_SANDBOX_MODE"] = "1"
105:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
157: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
159:     Give configured test operators only the sandbox permissions required by the
247:                 (str(user_id), SANDBOX_SERVICE_ROLE),
272:                     SANDBOX_SERVICE_ROLE,
308:                     (str(user_id), SANDBOX_SERVICE_ROLE),
320:                             SANDBOX_SERVICE_ROLE,
321:                             "Sandbox role for simplified service-workflow testing.",
348:                         SANDBOX_SERVICE_ROLE,
353:                         "Sandbox-only simplified-service workflow permission.",
393:             "В service_orders_workspace.py не установлена готовая версия "
407:         "handlers.client_portal",
408:         "handlers.client_portal_v2",
411:         "handlers.service_orders_workspace",
424:     """Patch profile verification into the bot source in memory only."""
450:         "uk": "📋 Перевірити мої дані",
502:         "    # Клиентский кабинет / заявки на пульты\n"
531: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
538:     sandbox launcher. Bots/parking_bot.py is not written to disk.
542:         "    # Клиентский кабинет / заявки на пульты\n"
557:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
567:             "Не найден следующий раздел навигации в parking_bot.py."
574:         "await handle_client_portal_text(",
584:             "В parking_bot.py не найдены обработчики для перестановки: "
598: def patch_bot_source() -> tuple[str, list[str]]:
600:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
603:     if not SERVICE_PATCHER.is_file():
604:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
611:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
612:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
614:     source, v2_changes = v2.patch(source)
615:     source, service_changes = service.patch(source)
617:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
636: def live_service_preflight(db_path: Path) -> None:
658:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
720:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
746:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
755:         help="Do not create sandbox-only service operator permissions.",
760:     print("OSBB LIVE SERVICES SANDBOX")
762:     print("Database:", LIVE_SERVICES_DB)
765:     if not LIVE_SERVICES_DB.is_file():
767:             "Не найдена live-services sandbox-БД:\n"
768:             f"  {LIVE_SERVICES_DB}"
771:     configure_sandbox(LIVE_SERVICES_DB)
772:     live_service_preflight(LIVE_SERVICES_DB)
777:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
778:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
780:             print("Sandbox backup before permission seed:", backup)
788:     source, bot_changes = patch_bot_source()
799:         print("Bots\\parking_bot.py and config.py were not changed.")
805:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
812:     print("Starting live services sandbox bot.")
814:     print(" ", LIVE_SERVICES_DB)
825:         print("\nLive services sandbox bot stopped by Ctrl+C.")
828:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\run_bot_live_service_sandbox_v4.py`

- Score: `158`
- Kind: `py`
- SHA: `49721c32f14f`
- Size: `8293`
- Modified: `2026-07-02 22:59:39`
- Markers: `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_guard_workspace_v4.py`
- `G:\Programming\Py\OSBB\Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\patch_parking_bot_service_orders_ui_v1.py`
- `G:\Programming\Py\OSBB\service_orders_core.py`
- `guard_workspace.py`
- `client_portal_v3.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\install_service_orders_ui.py`
- `config.py or parking_bot.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from pathlib import Path`
- `from types import SimpleNamespace`
- `from typing import Any`
- `import config`

Interesting lines:
```text
2: Запуск изолированной live sandbox с кабинетами:
3: - житель: «Пульты и доступ»;
7: Все изменения Bots/parking_bot.py выполняются только в памяти текущего процесса.
8: Работает исключительно с указанной .db внутри Data\db\sandbox.
27: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
28: BOT_FILE = BOTS / "parking_bot.py"
30: GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v4.py"
31: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_ui_v1.py"
45: def inside_sandbox(path: Path) -> Path:
48:         resolved.relative_to(SANDBOX_DIR.resolve())
51:             "Для запуска разрешены только .db внутри Data\\db\\sandbox."
56: def clone_paths(original: Any, sandbox_db: Path):
70:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
74: def configure_sandbox(sandbox_db: Path) -> None:
81:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
83:     if sandbox_db in {original_test, original_prod}:
84:         raise RuntimeError("Отказ: указан путь рабочей базы, а не sandbox-копии.")
86:     config.paths = clone_paths(config.paths, sandbox_db)
88:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
89:     os.environ["OSBB_SANDBOX_MODE"] = "1"
92: def table_rows(sandbox_db: Path) -> dict[str, int]:
106:     conn = sqlite3.connect(sandbox_db)
129:         GUARD_PATCHER,
130:         SERVICE_PATCHER,
133:         BOTS / "handlers" / "client_portal_v3.py",
134:         BOTS / "handlers" / "service_orders_workspace.py",
138: def patched_source() -> tuple[str, list[str], list[str], list[str]]:
146:             "Сначала выполните install_service_orders_ui.py --apply."
149:     v2 = load_module(V2_SWITCHER, "_live_service_v2_switcher")
150:     guard = load_module(GUARD_PATCHER, "_live_service_guard_patcher")
151:     service = load_module(SERVICE_PATCHER, "_live_service_ui_patcher")
154:     source, v2_changes = v2.patch(source)
155:     source, guard_changes = guard.patch(source)
156:     source, service_changes = service.patch(source)
173:             "handlers.client_portal",
174:             "handlers.client_portal_v2",
175:             "handlers.client_portal_v3",
179:             "handlers.service_orders_workspace",
188:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
193:     parser.add_argument("--sandbox", required=True)
197:     sandbox_db = inside_sandbox(Path(args.sandbox))
198:     if not sandbox_db.exists():
199:         raise SystemExit(f"Не найдена sandbox-БД: {sandbox_db}")
202:     print("OSBB LIVE SERVICE SANDBOX BOT V4")
204:     print("Sandbox DB:", sandbox_db)
208:         summary = table_rows(sandbox_db)
212:                 "Sandbox не подготовлен для услуг/пультов. Нет таблиц: "
216:         print("\nSandbox rows:")
220:         configure_sandbox(sandbox_db)
221:         source, v2_changes, guard_changes, service_changes = patched_source()
222:         print("\nRuntime patches:")
230:             print("No database, config.py or parking_bot.py was changed.")
234:         print("All new records will be written only to:", sandbox_db)
235:         print("Stop this sandbox bot with Ctrl+C.\n")
240:         print("\nLive service sandbox bot stopped by Ctrl+C.")
243:         print("\nLIVE SERVICE SANDBOX LAUNCH FAILED")
```

### `Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\patch_parking_bot_service_orders_ui_v1.py`

- Score: `158`
- Kind: `py`
- SHA: `b14c6b81aa98`
- Size: `11423`
- Modified: `2026-07-02 22:59:39`
- Markers: `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `- leaves source parking_bot.py`
- `service_orders_workspace.py`
- `client_portal_v3.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
2: Runtime patch for the isolated live service sandbox.
4: The patch is applied to Bots/parking_bot.py in memory only:
5: - client_portal_v2 -> client_portal_v3 (combined resident button);
8: - leaves source parking_bot.py unchanged.
20: BOT_FILE = ROOT / "Bots" / "parking_bot.py"
21: WORKSPACE_FILE = ROOT / "Bots" / "handlers" / "service_orders_workspace.py"
22: PORTAL_FILE = ROOT / "Bots" / "handlers" / "client_portal_v3.py"
25:     "from handlers.service_orders_workspace import (\n"
145:     if "from handlers.service_orders_workspace import (" in source:
157:         raise RuntimeError("Не найден импортный якорь для service_orders_workspace.")
161: def swap_client_portal(source: str) -> tuple[str, bool]:
162:     old = "from handlers.client_portal_v2 import ("
163:     new = "from handlers.client_portal_v3 import ("
168:             "Ожидался импорт client_portal_v2 после v2-switcher. "
174: def patch_show_mode(source: str) -> tuple[str, bool]:
190: def patch_language_gates(source: str) -> tuple[str, bool]:
206:             "Ожидалось 3 language-gate после guard patch, найдено "
230:         "    # Клиентский кабинет / заявки на пульты\n"
235:             "Не найден клиентский router. Нужен существующий client portal patch."
249: def patch(source: str) -> tuple[str, list[str]]:
254:         (swap_client_portal, "client portal v3"),
255:         (patch_show_mode, "mode menu with service operator"),
256:         (patch_language_gates, "language gate for service operators"),
266:         "from handlers.service_orders_workspace import (",
267:         "from handlers.client_portal_v3 import (",
283:     parser.add_argument("--apply", action="store_true")
287:     print("PATCH PARKING BOT: SERVICE ORDERS UI V1")
289:     print("Apply:", args.apply)
298:         patched, changes = patch(original)
299:         compile(patched, str(BOT_FILE), "exec")
301:         print("Patch check FAILED:", exc)
304:     print("Changes:", "; ".join(changes or ["already patched"]))
305:     print("Changes needed:", patched != original)
306:     if not args.apply:
309:     if patched == original:
310:         print("ALREADY PATCHED - NO FILE CHANGE")
316:     BOT_FILE.write_text(patched, encoding="utf-8")
```

### `Recovered_Releases\2026-06-27__OSBB_profile_button_early_route_fix_v2\profile_button_early_route_payload\run_bot_live_services_sandbox_v1.py`

- Score: `158`
- Kind: `py`
- SHA: `c79dc72c59c7`
- Size: `31628`
- Modified: `2026-07-02 22:59:36`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
56: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
69: def clone_paths(original: Any, sandbox_db: Path) -> Any:
82:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
86: def configure_sandbox(sandbox_db: Path) -> None:
93:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
95:     if sandbox_db.resolve() in {original_test, original_prod}:
97:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
101:     config.paths = clone_paths(config.paths, sandbox_db)
103:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
104:     os.environ["OSBB_SANDBOX_MODE"] = "1"
105:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
157: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
159:     Give configured test operators only the sandbox permissions required by the
247:                 (str(user_id), SANDBOX_SERVICE_ROLE),
272:                     SANDBOX_SERVICE_ROLE,
308:                     (str(user_id), SANDBOX_SERVICE_ROLE),
320:                             SANDBOX_SERVICE_ROLE,
321:                             "Sandbox role for simplified service-workflow testing.",
348:                         SANDBOX_SERVICE_ROLE,
353:                         "Sandbox-only simplified-service workflow permission.",
393:             "В service_orders_workspace.py не установлена готовая версия "
407:         "handlers.client_portal",
408:         "handlers.client_portal_v2",
411:         "handlers.service_orders_workspace",
424:     """Patch profile verification into the bot source in memory only."""
451:         "uk": "📋 Перевірити мої дані",
535:         "    # Клиентский кабинет / заявки на пульты\n"
565: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
572:     sandbox launcher. Bots/parking_bot.py is not written to disk.
576:         "    # Клиентский кабинет / заявки на пульты\n"
591:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
601:             "Не найден следующий раздел навигации в parking_bot.py."
608:         "await handle_client_portal_text(",
618:             "В parking_bot.py не найдены обработчики для перестановки: "
632: def patch_bot_source() -> tuple[str, list[str]]:
634:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
637:     if not SERVICE_PATCHER.is_file():
638:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
645:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
646:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
648:     source, v2_changes = v2.patch(source)
649:     source, service_changes = service.patch(source)
651:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
670: def live_service_preflight(db_path: Path) -> None:
692:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
754:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
780:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
789:         help="Do not create sandbox-only service operator permissions.",
794:     print("OSBB LIVE SERVICES SANDBOX")
796:     print("Database:", LIVE_SERVICES_DB)
799:     if not LIVE_SERVICES_DB.is_file():
801:             "Не найдена live-services sandbox-БД:\n"
802:             f"  {LIVE_SERVICES_DB}"
805:     configure_sandbox(LIVE_SERVICES_DB)
806:     live_service_preflight(LIVE_SERVICES_DB)
811:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
812:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
814:             print("Sandbox backup before permission seed:", backup)
822:     source, bot_changes = patch_bot_source()
833:         print("Bots\\parking_bot.py and config.py were not changed.")
839:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
846:     print("Starting live services sandbox bot.")
848:     print(" ", LIVE_SERVICES_DB)
859:         print("\nLive services sandbox bot stopped by Ctrl+C.")
862:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\profile_verification_payload\run_bot_live_services_sandbox_v1.py`

- Score: `158`
- Kind: `py`
- SHA: `f7e5d56ecb68`
- Size: `30322`
- Modified: `2026-07-02 22:59:37`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\profile_verification_payload\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
56: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
69: def clone_paths(original: Any, sandbox_db: Path) -> Any:
82:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
86: def configure_sandbox(sandbox_db: Path) -> None:
93:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
95:     if sandbox_db.resolve() in {original_test, original_prod}:
97:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
101:     config.paths = clone_paths(config.paths, sandbox_db)
103:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
104:     os.environ["OSBB_SANDBOX_MODE"] = "1"
105:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
157: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
159:     Give configured test operators only the sandbox permissions required by the
247:                 (str(user_id), SANDBOX_SERVICE_ROLE),
272:                     SANDBOX_SERVICE_ROLE,
308:                     (str(user_id), SANDBOX_SERVICE_ROLE),
320:                             SANDBOX_SERVICE_ROLE,
321:                             "Sandbox role for simplified service-workflow testing.",
348:                         SANDBOX_SERVICE_ROLE,
353:                         "Sandbox-only simplified-service workflow permission.",
393:             "В service_orders_workspace.py не установлена готовая версия "
407:         "handlers.client_portal",
408:         "handlers.client_portal_v2",
411:         "handlers.service_orders_workspace",
424:     """Patch profile verification into the bot source in memory only."""
450:         "uk": "📋 Перевірити мої дані",
502:         "    # Клиентский кабинет / заявки на пульты\n"
531: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
538:     sandbox launcher. Bots/parking_bot.py is not written to disk.
542:         "    # Клиентский кабинет / заявки на пульты\n"
557:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
567:             "Не найден следующий раздел навигации в parking_bot.py."
574:         "await handle_client_portal_text(",
584:             "В parking_bot.py не найдены обработчики для перестановки: "
598: def patch_bot_source() -> tuple[str, list[str]]:
600:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
603:     if not SERVICE_PATCHER.is_file():
604:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
611:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
612:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
614:     source, v2_changes = v2.patch(source)
615:     source, service_changes = service.patch(source)
617:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
636: def live_service_preflight(db_path: Path) -> None:
658:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
720:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
746:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
755:         help="Do not create sandbox-only service operator permissions.",
760:     print("OSBB LIVE SERVICES SANDBOX")
762:     print("Database:", LIVE_SERVICES_DB)
765:     if not LIVE_SERVICES_DB.is_file():
767:             "Не найдена live-services sandbox-БД:\n"
768:             f"  {LIVE_SERVICES_DB}"
771:     configure_sandbox(LIVE_SERVICES_DB)
772:     live_service_preflight(LIVE_SERVICES_DB)
777:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
778:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
780:             print("Sandbox backup before permission seed:", backup)
788:     source, bot_changes = patch_bot_source()
799:         print("Bots\\parking_bot.py and config.py were not changed.")
805:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
812:     print("Starting live services sandbox bot.")
814:     print(" ", LIVE_SERVICES_DB)
825:         print("\nLive services sandbox bot stopped by Ctrl+C.")
828:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\parking_time_test_payload\run_bot_live_services_sandbox_v1.py`

- Score: `158`
- Kind: `py`
- SHA: `51e635b6958c`
- Size: `33905`
- Modified: `2026-07-02 22:59:36`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\parking_time_test_payload\profile_parking_time_test_core.py`
- `profile_parking_time_test_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
60: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
73: def clone_paths(original: Any, sandbox_db: Path) -> Any:
86:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
90: def configure_sandbox(sandbox_db: Path) -> None:
97:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
99:     if sandbox_db.resolve() in {original_test, original_prod}:
101:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
105:     config.paths = clone_paths(config.paths, sandbox_db)
107:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
108:     os.environ["OSBB_SANDBOX_MODE"] = "1"
109:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
161: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
163:     Give configured test operators only the sandbox permissions required by the
251:                 (str(user_id), SANDBOX_SERVICE_ROLE),
276:                     SANDBOX_SERVICE_ROLE,
312:                     (str(user_id), SANDBOX_SERVICE_ROLE),
324:                             SANDBOX_SERVICE_ROLE,
325:                             "Sandbox role for simplified service-workflow testing.",
352:                         SANDBOX_SERVICE_ROLE,
357:                         "Sandbox-only simplified-service workflow permission.",
397:             "В service_orders_workspace.py не установлена готовая версия "
411:         "handlers.client_portal",
412:         "handlers.client_portal_v2",
415:         "handlers.service_orders_workspace",
430:     """Patch profile verification into the bot source in memory only."""
468:         "uk": "📋 Перевірити мої дані",
581:         "    # Клиентский кабинет / заявки на пульты\n"
611: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
618:     sandbox launcher. Bots/parking_bot.py is not written to disk.
622:         "    # Клиентский кабинет / заявки на пульты\n"
637:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
647:             "Не найден следующий раздел навигации в parking_bot.py."
654:         "await handle_client_portal_text(",
664:             "В parking_bot.py не найдены обработчики для перестановки: "
678: def patch_bot_source() -> tuple[str, list[str]]:
680:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
683:     if not SERVICE_PATCHER.is_file():
684:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
697:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
698:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
700:     source, v2_changes = v2.patch(source)
701:     source, service_changes = service.patch(source)
703:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
722: def live_service_preflight(db_path: Path) -> None:
746:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
808:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
834:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
843:         help="Do not create sandbox-only service operator permissions.",
848:     print("OSBB LIVE SERVICES SANDBOX")
850:     print("Database:", LIVE_SERVICES_DB)
853:     if not LIVE_SERVICES_DB.is_file():
855:             "Не найдена live-services sandbox-БД:\n"
856:             f"  {LIVE_SERVICES_DB}"
859:     configure_sandbox(LIVE_SERVICES_DB)
860:     live_service_preflight(LIVE_SERVICES_DB)
865:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
866:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
868:             print("Sandbox backup before permission seed:", backup)
876:     source, bot_changes = patch_bot_source()
887:         print("Bots\\parking_bot.py and config.py were not changed.")
893:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
900:     print("Starting live services sandbox bot.")
902:     print(" ", LIVE_SERVICES_DB)
913:         print("\nLive services sandbox bot stopped by Ctrl+C.")
916:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `run_bot_live_services_sandbox_v1.py`

- Score: `158`
- Kind: `py`
- SHA: `51e635b6958c`
- Size: `33905`
- Modified: `2026-06-28 12:11:31`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, ukrainian_ui, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\profile_verification_core.py`
- `profile_verification_workspace.py`
- `G:\Programming\Py\OSBB\profile_parking_time_test_core.py`
- `profile_parking_time_test_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
60: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
73: def clone_paths(original: Any, sandbox_db: Path) -> Any:
86:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
90: def configure_sandbox(sandbox_db: Path) -> None:
97:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
99:     if sandbox_db.resolve() in {original_test, original_prod}:
101:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
105:     config.paths = clone_paths(config.paths, sandbox_db)
107:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
108:     os.environ["OSBB_SANDBOX_MODE"] = "1"
109:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
161: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
163:     Give configured test operators only the sandbox permissions required by the
251:                 (str(user_id), SANDBOX_SERVICE_ROLE),
276:                     SANDBOX_SERVICE_ROLE,
312:                     (str(user_id), SANDBOX_SERVICE_ROLE),
324:                             SANDBOX_SERVICE_ROLE,
325:                             "Sandbox role for simplified service-workflow testing.",
352:                         SANDBOX_SERVICE_ROLE,
357:                         "Sandbox-only simplified-service workflow permission.",
397:             "В service_orders_workspace.py не установлена готовая версия "
411:         "handlers.client_portal",
412:         "handlers.client_portal_v2",
415:         "handlers.service_orders_workspace",
430:     """Patch profile verification into the bot source in memory only."""
468:         "uk": "📋 Перевірити мої дані",
581:         "    # Клиентский кабинет / заявки на пульты\n"
611: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
618:     sandbox launcher. Bots/parking_bot.py is not written to disk.
622:         "    # Клиентский кабинет / заявки на пульты\n"
637:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
647:             "Не найден следующий раздел навигации в parking_bot.py."
654:         "await handle_client_portal_text(",
664:             "В parking_bot.py не найдены обработчики для перестановки: "
678: def patch_bot_source() -> tuple[str, list[str]]:
680:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
683:     if not SERVICE_PATCHER.is_file():
684:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
697:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
698:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
700:     source, v2_changes = v2.patch(source)
701:     source, service_changes = service.patch(source)
703:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
722: def live_service_preflight(db_path: Path) -> None:
746:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
808:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
834:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
843:         help="Do not create sandbox-only service operator permissions.",
848:     print("OSBB LIVE SERVICES SANDBOX")
850:     print("Database:", LIVE_SERVICES_DB)
853:     if not LIVE_SERVICES_DB.is_file():
855:             "Не найдена live-services sandbox-БД:\n"
856:             f"  {LIVE_SERVICES_DB}"
859:     configure_sandbox(LIVE_SERVICES_DB)
860:     live_service_preflight(LIVE_SERVICES_DB)
865:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
866:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
868:             print("Sandbox backup before permission seed:", backup)
876:     source, bot_changes = patch_bot_source()
887:         print("Bots\\parking_bot.py and config.py were not changed.")
893:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
900:     print("Starting live services sandbox bot.")
902:     print(" ", LIVE_SERVICES_DB)
913:         print("\nLive services sandbox bot stopped by Ctrl+C.")
916:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `patch_parking_bot_service_orders_ui_v1.py`

- Score: `150`
- Kind: `py`
- SHA: `b14c6b81aa98`
- Size: `11423`
- Modified: `2026-06-26 20:40:59`
- Markers: `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `- leaves source parking_bot.py`
- `service_orders_workspace.py`
- `client_portal_v3.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
2: Runtime patch for the isolated live service sandbox.
4: The patch is applied to Bots/parking_bot.py in memory only:
5: - client_portal_v2 -> client_portal_v3 (combined resident button);
8: - leaves source parking_bot.py unchanged.
20: BOT_FILE = ROOT / "Bots" / "parking_bot.py"
21: WORKSPACE_FILE = ROOT / "Bots" / "handlers" / "service_orders_workspace.py"
22: PORTAL_FILE = ROOT / "Bots" / "handlers" / "client_portal_v3.py"
25:     "from handlers.service_orders_workspace import (\n"
145:     if "from handlers.service_orders_workspace import (" in source:
157:         raise RuntimeError("Не найден импортный якорь для service_orders_workspace.")
161: def swap_client_portal(source: str) -> tuple[str, bool]:
162:     old = "from handlers.client_portal_v2 import ("
163:     new = "from handlers.client_portal_v3 import ("
168:             "Ожидался импорт client_portal_v2 после v2-switcher. "
174: def patch_show_mode(source: str) -> tuple[str, bool]:
190: def patch_language_gates(source: str) -> tuple[str, bool]:
206:             "Ожидалось 3 language-gate после guard patch, найдено "
230:         "    # Клиентский кабинет / заявки на пульты\n"
235:             "Не найден клиентский router. Нужен существующий client portal patch."
249: def patch(source: str) -> tuple[str, list[str]]:
254:         (swap_client_portal, "client portal v3"),
255:         (patch_show_mode, "mode menu with service operator"),
256:         (patch_language_gates, "language gate for service operators"),
266:         "from handlers.service_orders_workspace import (",
267:         "from handlers.client_portal_v3 import (",
283:     parser.add_argument("--apply", action="store_true")
287:     print("PATCH PARKING BOT: SERVICE ORDERS UI V1")
289:     print("Apply:", args.apply)
298:         patched, changes = patch(original)
299:         compile(patched, str(BOT_FILE), "exec")
301:         print("Patch check FAILED:", exc)
304:     print("Changes:", "; ".join(changes or ["already patched"]))
305:     print("Changes needed:", patched != original)
306:     if not args.apply:
309:     if patched == original:
310:         print("ALREADY PATCHED - NO FILE CHANGE")
316:     BOT_FILE.write_text(patched, encoding="utf-8")
```

### `cashier_route_repair_payload\run_bot_live_services_sandbox_v1.py`

- Score: `148`
- Kind: `py`
- SHA: `2c2db2c9c866`
- Size: `25095`
- Modified: `2026-06-27 20:00:41`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
54: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
67: def clone_paths(original: Any, sandbox_db: Path) -> Any:
80:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
84: def configure_sandbox(sandbox_db: Path) -> None:
91:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
93:     if sandbox_db.resolve() in {original_test, original_prod}:
95:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
99:     config.paths = clone_paths(config.paths, sandbox_db)
101:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
102:     os.environ["OSBB_SANDBOX_MODE"] = "1"
103:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
155: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
157:     Give configured test operators only the sandbox permissions required by the
245:                 (str(user_id), SANDBOX_SERVICE_ROLE),
270:                     SANDBOX_SERVICE_ROLE,
306:                     (str(user_id), SANDBOX_SERVICE_ROLE),
318:                             SANDBOX_SERVICE_ROLE,
319:                             "Sandbox role for simplified service-workflow testing.",
346:                         SANDBOX_SERVICE_ROLE,
351:                         "Sandbox-only simplified-service workflow permission.",
391:             "В service_orders_workspace.py не установлена готовая версия "
405:         "handlers.client_portal",
406:         "handlers.client_portal_v2",
409:         "handlers.service_orders_workspace",
418: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
425:     sandbox launcher. Bots/parking_bot.py is not written to disk.
429:         "    # Клиентский кабинет / заявки на пульты\n"
444:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
454:             "Не найден следующий раздел навигации в parking_bot.py."
461:         "await handle_client_portal_text(",
471:             "В parking_bot.py не найдены обработчики для перестановки: "
485: def patch_bot_source() -> tuple[str, list[str]]:
487:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
490:     if not SERVICE_PATCHER.is_file():
491:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
494:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
495:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
497:     source, v2_changes = v2.patch(source)
498:     source, service_changes = service.patch(source)
499:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
515: def live_service_preflight(db_path: Path) -> None:
535:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
597:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
623:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
632:         help="Do not create sandbox-only service operator permissions.",
637:     print("OSBB LIVE SERVICES SANDBOX")
639:     print("Database:", LIVE_SERVICES_DB)
642:     if not LIVE_SERVICES_DB.is_file():
644:             "Не найдена live-services sandbox-БД:\n"
645:             f"  {LIVE_SERVICES_DB}"
648:     configure_sandbox(LIVE_SERVICES_DB)
649:     live_service_preflight(LIVE_SERVICES_DB)
654:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
655:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
657:             print("Sandbox backup before permission seed:", backup)
665:     source, bot_changes = patch_bot_source()
676:         print("Bots\\parking_bot.py and config.py were not changed.")
682:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
689:     print("Starting live services sandbox bot.")
691:     print(" ", LIVE_SERVICES_DB)
702:         print("\nLive services sandbox bot stopped by Ctrl+C.")
705:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Data\backups\source_code\cashier_route_repair_2026-06-27_20-04-49\run_bot_live_services_sandbox_v1.py`

- Score: `148`
- Kind: `py`
- SHA: `def3aac9ee8e`
- Size: `24930`
- Modified: `2026-06-27 17:34:24`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: - uses only the known live-services sandbox database;
8: - switches the bot to cashier v2 in memory;
9: - connects service_orders_workspace to parking_bot in memory;
11: - prepares sandbox-only service permissions for test operators;
12: - never changes Bots\\parking_bot.py or config.py.
14: It is intentionally separate from the old Guard Sandbox runner.
36: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
37: BACKUP_DIR = SANDBOX_DIR / "backups"
39: LIVE_SERVICES_DB = (
40:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
43: BOT_FILE = BOTS_DIR / "parking_bot.py"
44: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
46: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
51: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
64: def clone_paths(original: Any, sandbox_db: Path) -> Any:
77:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
81: def configure_sandbox(sandbox_db: Path) -> None:
88:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
90:     if sandbox_db.resolve() in {original_test, original_prod}:
92:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
96:     config.paths = clone_paths(config.paths, sandbox_db)
98:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
99:     os.environ["OSBB_SANDBOX_MODE"] = "1"
100:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
152: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
154:     Give configured test operators only the sandbox permissions required by the
242:                 (str(user_id), SANDBOX_SERVICE_ROLE),
267:                     SANDBOX_SERVICE_ROLE,
303:                     (str(user_id), SANDBOX_SERVICE_ROLE),
315:                             SANDBOX_SERVICE_ROLE,
316:                             "Sandbox role for simplified service-workflow testing.",
343:                         SANDBOX_SERVICE_ROLE,
348:                         "Sandbox-only simplified-service workflow permission.",
388:             "В service_orders_workspace.py не установлена готовая версия "
402:         "handlers.client_portal",
403:         "handlers.client_portal_v2",
406:         "handlers.service_orders_workspace",
415: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
422:     sandbox launcher. Bots/parking_bot.py is not written to disk.
426:         "    # Клиентский кабинет / заявки на пульты\n"
441:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
451:             "Не найден следующий раздел навигации в parking_bot.py."
458:         "await handle_client_portal_text(",
468:             "В parking_bot.py не найдены обработчики для перестановки: "
482: def patch_bot_source() -> tuple[str, list[str]]:
484:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
487:     if not SERVICE_PATCHER.is_file():
488:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
491:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
492:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
494:     source, v2_changes = v2.patch(source)
495:     source, service_changes = service.patch(source)
496:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
512: def live_service_preflight(db_path: Path) -> None:
532:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
594:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
620:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
629:         help="Do not create sandbox-only service operator permissions.",
634:     print("OSBB LIVE SERVICES SANDBOX")
636:     print("Database:", LIVE_SERVICES_DB)
639:     if not LIVE_SERVICES_DB.is_file():
641:             "Не найдена live-services sandbox-БД:\n"
642:             f"  {LIVE_SERVICES_DB}"
645:     configure_sandbox(LIVE_SERVICES_DB)
646:     live_service_preflight(LIVE_SERVICES_DB)
651:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
652:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
654:             print("Sandbox backup before permission seed:", backup)
662:     source, bot_changes = patch_bot_source()
673:         print("Bots\\parking_bot.py and config.py were not changed.")
679:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
686:     print("Starting live services sandbox bot.")
688:     print(" ", LIVE_SERVICES_DB)
699:         print("\nLive services sandbox bot stopped by Ctrl+C.")
702:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Data\backups\source_code\profile_verification_2026-06-27_20-51-33\run_bot_live_services_sandbox_v1.py`

- Score: `148`
- Kind: `py`
- SHA: `2c2db2c9c866`
- Size: `25095`
- Modified: `2026-06-27 20:00:41`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
54: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
67: def clone_paths(original: Any, sandbox_db: Path) -> Any:
80:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
84: def configure_sandbox(sandbox_db: Path) -> None:
91:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
93:     if sandbox_db.resolve() in {original_test, original_prod}:
95:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
99:     config.paths = clone_paths(config.paths, sandbox_db)
101:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
102:     os.environ["OSBB_SANDBOX_MODE"] = "1"
103:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
155: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
157:     Give configured test operators only the sandbox permissions required by the
245:                 (str(user_id), SANDBOX_SERVICE_ROLE),
270:                     SANDBOX_SERVICE_ROLE,
306:                     (str(user_id), SANDBOX_SERVICE_ROLE),
318:                             SANDBOX_SERVICE_ROLE,
319:                             "Sandbox role for simplified service-workflow testing.",
346:                         SANDBOX_SERVICE_ROLE,
351:                         "Sandbox-only simplified-service workflow permission.",
391:             "В service_orders_workspace.py не установлена готовая версия "
405:         "handlers.client_portal",
406:         "handlers.client_portal_v2",
409:         "handlers.service_orders_workspace",
418: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
425:     sandbox launcher. Bots/parking_bot.py is not written to disk.
429:         "    # Клиентский кабинет / заявки на пульты\n"
444:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
454:             "Не найден следующий раздел навигации в parking_bot.py."
461:         "await handle_client_portal_text(",
471:             "В parking_bot.py не найдены обработчики для перестановки: "
485: def patch_bot_source() -> tuple[str, list[str]]:
487:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
490:     if not SERVICE_PATCHER.is_file():
491:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
494:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
495:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
497:     source, v2_changes = v2.patch(source)
498:     source, service_changes = service.patch(source)
499:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
515: def live_service_preflight(db_path: Path) -> None:
535:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
597:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
623:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
632:         help="Do not create sandbox-only service operator permissions.",
637:     print("OSBB LIVE SERVICES SANDBOX")
639:     print("Database:", LIVE_SERVICES_DB)
642:     if not LIVE_SERVICES_DB.is_file():
644:             "Не найдена live-services sandbox-БД:\n"
645:             f"  {LIVE_SERVICES_DB}"
648:     configure_sandbox(LIVE_SERVICES_DB)
649:     live_service_preflight(LIVE_SERVICES_DB)
654:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
655:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
657:             print("Sandbox backup before permission seed:", backup)
665:     source, bot_changes = patch_bot_source()
676:         print("Bots\\parking_bot.py and config.py were not changed.")
682:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
689:     print("Starting live services sandbox bot.")
691:     print(" ", LIVE_SERVICES_DB)
702:         print("\nLive services sandbox bot stopped by Ctrl+C.")
705:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__2c2db2c9c866.py`

- Score: `148`
- Kind: `py`
- SHA: `2c2db2c9c866`
- Size: `25095`
- Modified: `2026-07-02 22:59:37`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
54: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
67: def clone_paths(original: Any, sandbox_db: Path) -> Any:
80:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
84: def configure_sandbox(sandbox_db: Path) -> None:
91:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
93:     if sandbox_db.resolve() in {original_test, original_prod}:
95:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
99:     config.paths = clone_paths(config.paths, sandbox_db)
101:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
102:     os.environ["OSBB_SANDBOX_MODE"] = "1"
103:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
155: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
157:     Give configured test operators only the sandbox permissions required by the
245:                 (str(user_id), SANDBOX_SERVICE_ROLE),
270:                     SANDBOX_SERVICE_ROLE,
306:                     (str(user_id), SANDBOX_SERVICE_ROLE),
318:                             SANDBOX_SERVICE_ROLE,
319:                             "Sandbox role for simplified service-workflow testing.",
346:                         SANDBOX_SERVICE_ROLE,
351:                         "Sandbox-only simplified-service workflow permission.",
391:             "В service_orders_workspace.py не установлена готовая версия "
405:         "handlers.client_portal",
406:         "handlers.client_portal_v2",
409:         "handlers.service_orders_workspace",
418: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
425:     sandbox launcher. Bots/parking_bot.py is not written to disk.
429:         "    # Клиентский кабинет / заявки на пульты\n"
444:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
454:             "Не найден следующий раздел навигации в parking_bot.py."
461:         "await handle_client_portal_text(",
471:             "В parking_bot.py не найдены обработчики для перестановки: "
485: def patch_bot_source() -> tuple[str, list[str]]:
487:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
490:     if not SERVICE_PATCHER.is_file():
491:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
494:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
495:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
497:     source, v2_changes = v2.patch(source)
498:     source, service_changes = service.patch(source)
499:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
515: def live_service_preflight(db_path: Path) -> None:
535:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
597:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
623:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
632:         help="Do not create sandbox-only service operator permissions.",
637:     print("OSBB LIVE SERVICES SANDBOX")
639:     print("Database:", LIVE_SERVICES_DB)
642:     if not LIVE_SERVICES_DB.is_file():
644:             "Не найдена live-services sandbox-БД:\n"
645:             f"  {LIVE_SERVICES_DB}"
648:     configure_sandbox(LIVE_SERVICES_DB)
649:     live_service_preflight(LIVE_SERVICES_DB)
654:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
655:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
657:             print("Sandbox backup before permission seed:", backup)
665:     source, bot_changes = patch_bot_source()
676:         print("Bots\\parking_bot.py and config.py were not changed.")
682:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
689:     print("Starting live services sandbox bot.")
691:     print(" ", LIVE_SERVICES_DB)
702:         print("\nLive services sandbox bot stopped by Ctrl+C.")
705:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__def3aac9ee8e.py`

- Score: `148`
- Kind: `py`
- SHA: `def3aac9ee8e`
- Size: `24930`
- Modified: `2026-07-02 22:59:38`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: - uses only the known live-services sandbox database;
8: - switches the bot to cashier v2 in memory;
9: - connects service_orders_workspace to parking_bot in memory;
11: - prepares sandbox-only service permissions for test operators;
12: - never changes Bots\\parking_bot.py or config.py.
14: It is intentionally separate from the old Guard Sandbox runner.
36: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
37: BACKUP_DIR = SANDBOX_DIR / "backups"
39: LIVE_SERVICES_DB = (
40:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
43: BOT_FILE = BOTS_DIR / "parking_bot.py"
44: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
46: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
51: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
64: def clone_paths(original: Any, sandbox_db: Path) -> Any:
77:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
81: def configure_sandbox(sandbox_db: Path) -> None:
88:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
90:     if sandbox_db.resolve() in {original_test, original_prod}:
92:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
96:     config.paths = clone_paths(config.paths, sandbox_db)
98:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
99:     os.environ["OSBB_SANDBOX_MODE"] = "1"
100:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
152: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
154:     Give configured test operators only the sandbox permissions required by the
242:                 (str(user_id), SANDBOX_SERVICE_ROLE),
267:                     SANDBOX_SERVICE_ROLE,
303:                     (str(user_id), SANDBOX_SERVICE_ROLE),
315:                             SANDBOX_SERVICE_ROLE,
316:                             "Sandbox role for simplified service-workflow testing.",
343:                         SANDBOX_SERVICE_ROLE,
348:                         "Sandbox-only simplified-service workflow permission.",
388:             "В service_orders_workspace.py не установлена готовая версия "
402:         "handlers.client_portal",
403:         "handlers.client_portal_v2",
406:         "handlers.service_orders_workspace",
415: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
422:     sandbox launcher. Bots/parking_bot.py is not written to disk.
426:         "    # Клиентский кабинет / заявки на пульты\n"
441:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
451:             "Не найден следующий раздел навигации в parking_bot.py."
458:         "await handle_client_portal_text(",
468:             "В parking_bot.py не найдены обработчики для перестановки: "
482: def patch_bot_source() -> tuple[str, list[str]]:
484:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
487:     if not SERVICE_PATCHER.is_file():
488:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
491:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
492:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
494:     source, v2_changes = v2.patch(source)
495:     source, service_changes = service.patch(source)
496:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
512: def live_service_preflight(db_path: Path) -> None:
532:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
594:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
620:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
629:         help="Do not create sandbox-only service operator permissions.",
634:     print("OSBB LIVE SERVICES SANDBOX")
636:     print("Database:", LIVE_SERVICES_DB)
639:     if not LIVE_SERVICES_DB.is_file():
641:             "Не найдена live-services sandbox-БД:\n"
642:             f"  {LIVE_SERVICES_DB}"
645:     configure_sandbox(LIVE_SERVICES_DB)
646:     live_service_preflight(LIVE_SERVICES_DB)
651:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
652:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
654:             print("Sandbox backup before permission seed:", backup)
662:     source, bot_changes = patch_bot_source()
673:         print("Bots\\parking_bot.py and config.py were not changed.")
679:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
686:     print("Starting live services sandbox bot.")
688:     print(" ", LIVE_SERVICES_DB)
699:         print("\nLive services sandbox bot stopped by Ctrl+C.")
702:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\install_service_orders_ui.py`

- Score: `148`
- Kind: `py`
- SHA: `84a6bab32e35`
- Size: `13153`
- Modified: `2026-07-02 22:59:39`
- Markers: `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\service_orders_core.py`
- `service_orders_workspace.py`
- `client_portal_v3.py`
- `G:\Programming\Py\OSBB\Recovered_Releases\2026-06-26__OSBB_Live_Service_UI_v1\run_bot_live_service_sandbox_v4.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
2: Installer for the service-orders user interface.
4: It changes only source code and the isolated live-sandbox launcher:
6: - switches the live sandbox launcher from v3 to v4;
7: - does not modify Bots/parking_bot.py or any database.
20: HANDLER = ROOT / "Bots" / "handlers" / "service_orders_workspace.py"
21: PORTAL = ROOT / "Bots" / "handlers" / "client_portal_v3.py"
22: RUNNER = ROOT / "run_bot_live_service_sandbox_v4.py"
23: LIVE_LAUNCHER = ROOT / "Start_OSBB_Live_Service_Sandbox_Bot.bat"
39: def patch_core(source: str) -> tuple[str, bool]:
42:     patched = replace_between(
48:     if MARKER not in patched:
50:     return patched, True
53: def patch_live_launcher(source: str) -> tuple[str, bool]:
54:     old = "run_bot_guard_sandbox_v3.py"
55:     new = "run_bot_live_service_sandbox_v4.py"
60:             "В launcher не найден run_bot_guard_sandbox_v3.py. "
75:     parser.add_argument("--apply", action="store_true")
81:     print("Apply:", args.apply)
102:         core_patched, core_changed = patch_core(core_original)
103:         launcher_patched, launcher_changed = patch_live_launcher(launcher_original)
104:         compile(core_patched, str(CORE), "exec")
106:         print("Patch check FAILED:", exc)
110:     print("Payment safety patch:", "needed" if core_changed else "already installed")
113:     if not args.apply:
119:         CORE.write_text(core_patched, encoding="utf-8")
125:         LIVE_LAUNCHER.write_text(launcher_patched, encoding="utf-8-sig")
130:     print("Bots/parking_bot.py and all databases were not modified.")
```

### `Recovered_Releases\2026-06-27__OSBB_cashier_route_fix\run_bot_live_services_sandbox_v1.py`

- Score: `148`
- Kind: `py`
- SHA: `def3aac9ee8e`
- Size: `24930`
- Modified: `2026-07-02 22:59:38`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: - uses only the known live-services sandbox database;
8: - switches the bot to cashier v2 in memory;
9: - connects service_orders_workspace to parking_bot in memory;
11: - prepares sandbox-only service permissions for test operators;
12: - never changes Bots\\parking_bot.py or config.py.
14: It is intentionally separate from the old Guard Sandbox runner.
36: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
37: BACKUP_DIR = SANDBOX_DIR / "backups"
39: LIVE_SERVICES_DB = (
40:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
43: BOT_FILE = BOTS_DIR / "parking_bot.py"
44: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
46: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
51: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
64: def clone_paths(original: Any, sandbox_db: Path) -> Any:
77:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
81: def configure_sandbox(sandbox_db: Path) -> None:
88:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
90:     if sandbox_db.resolve() in {original_test, original_prod}:
92:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
96:     config.paths = clone_paths(config.paths, sandbox_db)
98:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
99:     os.environ["OSBB_SANDBOX_MODE"] = "1"
100:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
152: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
154:     Give configured test operators only the sandbox permissions required by the
242:                 (str(user_id), SANDBOX_SERVICE_ROLE),
267:                     SANDBOX_SERVICE_ROLE,
303:                     (str(user_id), SANDBOX_SERVICE_ROLE),
315:                             SANDBOX_SERVICE_ROLE,
316:                             "Sandbox role for simplified service-workflow testing.",
343:                         SANDBOX_SERVICE_ROLE,
348:                         "Sandbox-only simplified-service workflow permission.",
388:             "В service_orders_workspace.py не установлена готовая версия "
402:         "handlers.client_portal",
403:         "handlers.client_portal_v2",
406:         "handlers.service_orders_workspace",
415: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
422:     sandbox launcher. Bots/parking_bot.py is not written to disk.
426:         "    # Клиентский кабинет / заявки на пульты\n"
441:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
451:             "Не найден следующий раздел навигации в parking_bot.py."
458:         "await handle_client_portal_text(",
468:             "В parking_bot.py не найдены обработчики для перестановки: "
482: def patch_bot_source() -> tuple[str, list[str]]:
484:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
487:     if not SERVICE_PATCHER.is_file():
488:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
491:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
492:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
494:     source, v2_changes = v2.patch(source)
495:     source, service_changes = service.patch(source)
496:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
512: def live_service_preflight(db_path: Path) -> None:
532:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
594:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
620:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
629:         help="Do not create sandbox-only service operator permissions.",
634:     print("OSBB LIVE SERVICES SANDBOX")
636:     print("Database:", LIVE_SERVICES_DB)
639:     if not LIVE_SERVICES_DB.is_file():
641:             "Не найдена live-services sandbox-БД:\n"
642:             f"  {LIVE_SERVICES_DB}"
645:     configure_sandbox(LIVE_SERVICES_DB)
646:     live_service_preflight(LIVE_SERVICES_DB)
651:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
652:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
654:             print("Sandbox backup before permission seed:", backup)
662:     source, bot_changes = patch_bot_source()
673:         print("Bots\\parking_bot.py and config.py were not changed.")
679:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
686:     print("Starting live services sandbox bot.")
688:     print(" ", LIVE_SERVICES_DB)
699:         print("\nLive services sandbox bot stopped by Ctrl+C.")
702:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered_Releases\2026-06-27__OSBB_cashier_route_repair_after_phone_v2\cashier_route_repair_payload\run_bot_live_services_sandbox_v1.py`

- Score: `148`
- Kind: `py`
- SHA: `2c2db2c9c866`
- Size: `25095`
- Modified: `2026-07-02 22:59:37`
- Markers: `parking_bot, service_orders_workspace, client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: to guarantee that cashier v2 is dispatched before the broad client-portal fallback.
10: - uses only the known live-services sandbox database;
11: - switches the bot to cashier v2 in memory;
12: - connects service_orders_workspace to parking_bot in memory;
14: - prepares sandbox-only service permissions for test operators;
15: - never changes Bots\\parking_bot.py or config.py.
17: It is intentionally separate from the old Guard Sandbox runner.
39: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
40: BACKUP_DIR = SANDBOX_DIR / "backups"
42: LIVE_SERVICES_DB = (
43:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
46: BOT_FILE = BOTS_DIR / "parking_bot.py"
47: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
49: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
54: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
67: def clone_paths(original: Any, sandbox_db: Path) -> Any:
80:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
84: def configure_sandbox(sandbox_db: Path) -> None:
91:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
93:     if sandbox_db.resolve() in {original_test, original_prod}:
95:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
99:     config.paths = clone_paths(config.paths, sandbox_db)
101:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
102:     os.environ["OSBB_SANDBOX_MODE"] = "1"
103:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
155: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
157:     Give configured test operators only the sandbox permissions required by the
245:                 (str(user_id), SANDBOX_SERVICE_ROLE),
270:                     SANDBOX_SERVICE_ROLE,
306:                     (str(user_id), SANDBOX_SERVICE_ROLE),
318:                             SANDBOX_SERVICE_ROLE,
319:                             "Sandbox role for simplified service-workflow testing.",
346:                         SANDBOX_SERVICE_ROLE,
351:                         "Sandbox-only simplified-service workflow permission.",
391:             "В service_orders_workspace.py не установлена готовая версия "
405:         "handlers.client_portal",
406:         "handlers.client_portal_v2",
409:         "handlers.service_orders_workspace",
418: def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
425:     sandbox launcher. Bots/parking_bot.py is not written to disk.
429:         "    # Клиентский кабинет / заявки на пульты\n"
444:             "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
454:             "Не найден следующий раздел навигации в parking_bot.py."
461:         "await handle_client_portal_text(",
471:             "В parking_bot.py не найдены обработчики для перестановки: "
485: def patch_bot_source() -> tuple[str, list[str]]:
487:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
490:     if not SERVICE_PATCHER.is_file():
491:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
494:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
495:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
497:     source, v2_changes = v2.patch(source)
498:     source, service_changes = service.patch(source)
499:     source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
515: def live_service_preflight(db_path: Path) -> None:
535:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
597:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
623:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
632:         help="Do not create sandbox-only service operator permissions.",
637:     print("OSBB LIVE SERVICES SANDBOX")
639:     print("Database:", LIVE_SERVICES_DB)
642:     if not LIVE_SERVICES_DB.is_file():
644:             "Не найдена live-services sandbox-БД:\n"
645:             f"  {LIVE_SERVICES_DB}"
648:     configure_sandbox(LIVE_SERVICES_DB)
649:     live_service_preflight(LIVE_SERVICES_DB)
654:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
655:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
657:             print("Sandbox backup before permission seed:", backup)
665:     source, bot_changes = patch_bot_source()
676:         print("Bots\\parking_bot.py and config.py were not changed.")
682:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
689:     print("Starting live services sandbox bot.")
691:     print(" ", LIVE_SERVICES_DB)
702:         print("\nLive services sandbox bot stopped by Ctrl+C.")
705:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `install_service_orders_ui.py`

- Score: `140`
- Kind: `py`
- SHA: `84a6bab32e35`
- Size: `13153`
- Modified: `2026-06-26 20:40:59`
- Markers: `parking_bot, service_orders_workspace, client_portal, client_portal_v3, patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\service_orders_core.py`
- `service_orders_workspace.py`
- `client_portal_v3.py`
- `G:\Programming\Py\OSBB\run_bot_live_service_sandbox_v4.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
2: Installer for the service-orders user interface.
4: It changes only source code and the isolated live-sandbox launcher:
6: - switches the live sandbox launcher from v3 to v4;
7: - does not modify Bots/parking_bot.py or any database.
20: HANDLER = ROOT / "Bots" / "handlers" / "service_orders_workspace.py"
21: PORTAL = ROOT / "Bots" / "handlers" / "client_portal_v3.py"
22: RUNNER = ROOT / "run_bot_live_service_sandbox_v4.py"
23: LIVE_LAUNCHER = ROOT / "Start_OSBB_Live_Service_Sandbox_Bot.bat"
39: def patch_core(source: str) -> tuple[str, bool]:
42:     patched = replace_between(
48:     if MARKER not in patched:
50:     return patched, True
53: def patch_live_launcher(source: str) -> tuple[str, bool]:
54:     old = "run_bot_guard_sandbox_v3.py"
55:     new = "run_bot_live_service_sandbox_v4.py"
60:             "В launcher не найден run_bot_guard_sandbox_v3.py. "
75:     parser.add_argument("--apply", action="store_true")
81:     print("Apply:", args.apply)
102:         core_patched, core_changed = patch_core(core_original)
103:         launcher_patched, launcher_changed = patch_live_launcher(launcher_original)
104:         compile(core_patched, str(CORE), "exec")
106:         print("Patch check FAILED:", exc)
110:     print("Payment safety patch:", "needed" if core_changed else "already installed")
113:     if not args.apply:
119:         CORE.write_text(core_patched, encoding="utf-8")
125:         LIVE_LAUNCHER.write_text(launcher_patched, encoding="utf-8-sig")
130:     print("Bots/parking_bot.py and all databases were not modified.")
```

### `CHECK_guard_sandbox_service_orders.py`

- Score: `123`
- Kind: `py`
- SHA: `93460fdabb4f`
- Size: `15629`
- Modified: `2026-06-27 11:43:52`
- Markers: `parking_bot, service_orders_workspace, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `- parking_bot.py`
- `- config.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_guard_workspace_v4.py`
- `Raw parking_bot.py`
- `Patched parking_bot.py`

Imports:
- `from __future__ import annotations`
- `import importlib.util`
- `import re`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any, Iterable`

Interesting lines:
```text
3: OSBB — read-only diagnosis of the Guard Sandbox bot and service orders.
8: It reads the sandbox path from:
9:     Start_OSBB_Guard_Sandbox_Bot_v2.bat
12: - the sandbox database;
14: - parking_bot.py;
16: - any patcher or handler.
38: LAUNCHER_BAT = ROOT / "Start_OSBB_Guard_Sandbox_Bot_v2.bat"
39: RUNNER = ROOT / "run_bot_guard_sandbox_v3.py"
40: PARKING_BOT = BOTS_DIR / "parking_bot.py"
41: WORKSPACE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
43: GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v4.py"
72: def extract_sandbox_path() -> Path:
82:         r'(?im)^\s*set\s+"SANDBOX=(.*?)"\s*$',
87:             "Could not find the SANDBOX= line in "
96:             "The sandbox path contains an environment variable and cannot be "
190: def load_patch_module(path: Path, module_name: str):
193:         raise RuntimeError(f"Could not load patcher: {path}")
202:     say("BOT SOURCE AND IN-MEMORY PATCH CHECK")
204:     for path in (PARKING_BOT, V2_SWITCHER, GUARD_PATCHER, WORKSPACE, RUNNER):
212:     say(f"Raw parking_bot.py: {len(raw_source.splitlines())} lines")
214:     patched_source = None
215:     patch_messages: list[str] = []
216:     if V2_SWITCHER.is_file() and GUARD_PATCHER.is_file():
218:             v2 = load_patch_module(V2_SWITCHER, "_diagnosis_v2_switcher")
219:             guard = load_patch_module(GUARD_PATCHER, "_diagnosis_guard_patcher")
220:             patched_source, v2_changes = v2.patch(raw_source)
221:             patched_source, guard_changes = guard.patch(patched_source)
222:             compile(patched_source, str(PARKING_BOT), "exec")
223:             patch_messages.extend(
225:                     "v2 patch: " + ("; ".join(v2_changes) if v2_changes else "(no reported changes)"),
226:                     "guard patch: " + ("; ".join(guard_changes) if guard_changes else "(no reported changes)"),
227:                     f"Patched parking_bot.py: {len(patched_source.splitlines())} lines; compile PASS",
231:             patch_messages.append(f"PATCH ANALYSIS FAILED: {type(exc).__name__}: {exc}")
232:             patch_messages.append(traceback.format_exc())
234:         patch_messages.append("Patch analysis skipped because one or both patcher files are missing.")
236:     for message in patch_messages:
240:         "service_orders_workspace",
244:         "🔑 Заявки на пульты",
251:         ("PATCHED", patched_source),
269:     say("SANDBOX DATABASE CHECK")
442:         say("  - If 'service_orders_workspace' / 'handle_service_orders_text' is absent from PATCHED source,")
443:         say("    the sandbox bot cannot enter the new service-order interface.")
456:     report_path = LOG_DIR / f"guard_sandbox_service_orders_diagnosis_{stamp}.txt"
462:     say("OSBB Guard Sandbox — Service Orders Diagnosis")
467:     sandbox_db = extract_sandbox_path()
468:     say(f"Sandbox selected by BAT: {sandbox_db}")
471:     inspect_database(sandbox_db)
```

### `CHECK_guard_sandbox_service_orders_v2.py`

- Score: `123`
- Kind: `py`
- SHA: `97ef1dd399ce`
- Size: `14466`
- Modified: `2026-06-27 11:50:08`
- Markers: `parking_bot, service_orders_workspace, patches_in_memory, installer, sandbox_db, remote_button`

References:
- `- does not modify config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_guard_workspace_v4.py`
- `Raw parking_bot.py`
- `Patched parking_bot.py`

Imports:
- `from __future__ import annotations`
- `import importlib.util`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any, Iterable`

Interesting lines:
```text
3: OSBB — Guard Sandbox / Service Orders diagnostic, version 2.
8: This version does NOT need Start_OSBB_Guard_Sandbox_Bot_v2.bat.
9: It uses the exact sandbox database selected by that launcher on 27.06.2026.
33: # Exact sandbox selected by Start_OSBB_Guard_Sandbox_Bot_v2.bat.
34: SANDBOX_DB = (
38:     / "sandbox"
39:     / "osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09.db"
42: PARKING_BOT = BOTS_DIR / "parking_bot.py"
43: WORKSPACE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
45: GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v4.py"
179:     say("BOT SOURCE / RUNTIME PATCH CHECK")
181:     for path in (PARKING_BOT, WORKSPACE, V2_SWITCHER, GUARD_PATCHER):
189:     patched_source: str | None = None
192:     say(f"Raw parking_bot.py: {len(raw_source.splitlines())} lines")
194:     if V2_SWITCHER.is_file() and GUARD_PATCHER.is_file():
197:             guard = load_module_from_path(GUARD_PATCHER, "_guard_diagnosis_patcher")
199:             patched_source, v2_changes = v2.patch(raw_source)
200:             patched_source, guard_changes = guard.patch(patched_source)
201:             compile(patched_source, str(PARKING_BOT), "exec")
205:             say(f"Patched parking_bot.py: {len(patched_source.splitlines())} lines; compile PASS")
207:             say(f"PATCH ANALYSIS FAILED: {type(exc).__name__}: {exc}")
211:         "service_orders_workspace",
214:         "🔑 Заявки на пульты",
220:     for title, code in (("RAW SOURCE", raw_source), ("PATCHED SOURCE", patched_source)):
238:         say(f"service_orders_workspace.py: {len(workspace_source.splitlines())} lines")
241:             "🔑 Заявки на пульты",
252:     say("SANDBOX DATABASE CHECK")
253:     say(f"Sandbox DB: {SANDBOX_DB}")
254:     say(f"Exists: {SANDBOX_DB.is_file()}")
255:     if not SANDBOX_DB.is_file():
258:     conn = connect_readonly(SANDBOX_DB)
426:         say("  1) Whether the runtime-patched parking_bot imports and calls service_orders_workspace.")
427:         say("  2) Whether your sandbox contains the yesterday's reprogramming service order and its exact step.")
428:         say("  3) Whether the sandbox has payments.source_ref.")
437:     report_path = LOG_DIR / f"guard_sandbox_service_orders_diagnosis_v2_{stamp}.txt"
443:     say("OSBB Guard Sandbox — Service Orders Diagnosis V2")
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\run_bot_live_services_sandbox\run_bot_live_services_sandbox_v1__1fb99c606cdb.py`

- Score: `118`
- Kind: `py`
- SHA: `1fb99c606cdb`
- Size: `20258`
- Modified: `2026-07-02 22:59:39`
- Markers: `parking_bot, service_orders_workspace, client_portal, patches_in_memory, installer, sandbox_db`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: - uses only the known live-services sandbox database;
8: - switches the bot to cashier v2 in memory;
9: - connects service_orders_workspace to parking_bot in memory;
11: - prepares sandbox-only service permissions for test operators;
12: - never changes Bots\\parking_bot.py or config.py.
14: It is intentionally separate from the old Guard Sandbox runner.
36: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
37: BACKUP_DIR = SANDBOX_DIR / "backups"
39: LIVE_SERVICES_DB = (
40:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
43: BOT_FILE = BOTS_DIR / "parking_bot.py"
44: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
46: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
51: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
64: def clone_paths(original: Any, sandbox_db: Path) -> Any:
77:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
81: def configure_sandbox(sandbox_db: Path) -> None:
88:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
90:     if sandbox_db.resolve() in {original_test, original_prod}:
92:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
96:     config.paths = clone_paths(config.paths, sandbox_db)
98:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
99:     os.environ["OSBB_SANDBOX_MODE"] = "1"
100:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
152: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
154:     Give configured test operators sandbox-only permissions for service orders.
214:                 (str(user_id), SANDBOX_SERVICE_ROLE),
234:                     (SANDBOX_SERVICE_ROLE, resource, action, category),
255:                     (str(user_id), SANDBOX_SERVICE_ROLE),
267:                             SANDBOX_SERVICE_ROLE,
268:                             "Sandbox role for service-order workflow testing.",
288:                         (SANDBOX_SERVICE_ROLE, resource, action, category),
300:                                 SANDBOX_SERVICE_ROLE,
304:                                 "Sandbox-only service workflow permission.",
334:             "В service_orders_workspace.py не установлена готовая совместимая "
348:         "handlers.client_portal",
349:         "handlers.client_portal_v2",
352:         "handlers.service_orders_workspace",
360: def patch_bot_source() -> tuple[str, list[str]]:
362:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
365:     if not SERVICE_PATCHER.is_file():
366:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
369:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
370:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
372:     source, v2_changes = v2.patch(source)
373:     source, service_changes = service.patch(source)
384: def live_service_preflight(db_path: Path) -> None:
400:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
462:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
488:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
497:         help="Do not create sandbox-only service operator permissions.",
502:     print("OSBB LIVE SERVICES SANDBOX")
504:     print("Database:", LIVE_SERVICES_DB)
507:     if not LIVE_SERVICES_DB.is_file():
509:             "Не найдена live-services sandbox-БД:\n"
510:             f"  {LIVE_SERVICES_DB}"
513:     configure_sandbox(LIVE_SERVICES_DB)
514:     live_service_preflight(LIVE_SERVICES_DB)
519:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
520:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
522:             print("Sandbox backup before permission seed:", backup)
530:     source, bot_changes = patch_bot_source()
541:         print("Bots\\parking_bot.py and config.py were not changed.")
547:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
554:     print("Starting live services sandbox bot.")
556:     print(" ", LIVE_SERVICES_DB)
567:         print("\nLive services sandbox bot stopped by Ctrl+C.")
570:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `Recovered_Releases\2026-06-27__OSBB_live_services_sandbox_bundle\run_bot_live_services_sandbox_v1.py`

- Score: `118`
- Kind: `py`
- SHA: `1fb99c606cdb`
- Size: `20258`
- Modified: `2026-07-02 22:59:39`
- Markers: `parking_bot, service_orders_workspace, client_portal, patches_in_memory, installer, sandbox_db`

References:
- `- never changes Bots\\parking_bot.py or config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\Recovered_Releases\2026-06-27__OSBB_live_services_sandbox_bundle\patch_parking_bot_service_orders_v1.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `Bots\\parking_bot.py and config.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import shutil`
- `import sqlite3`
- `import subprocess`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import ModuleType, SimpleNamespace`
- `from typing import Any`
- `import config`
- `from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS`

Interesting lines:
```text
4: sandbox database.
7: - uses only the known live-services sandbox database;
8: - switches the bot to cashier v2 in memory;
9: - connects service_orders_workspace to parking_bot in memory;
11: - prepares sandbox-only service permissions for test operators;
12: - never changes Bots\\parking_bot.py or config.py.
14: It is intentionally separate from the old Guard Sandbox runner.
36: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
37: BACKUP_DIR = SANDBOX_DIR / "backups"
39: LIVE_SERVICES_DB = (
40:     SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
43: BOT_FILE = BOTS_DIR / "parking_bot.py"
44: WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
46: SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
51: SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"
64: def clone_paths(original: Any, sandbox_db: Path) -> Any:
77:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
81: def configure_sandbox(sandbox_db: Path) -> None:
88:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
90:     if sandbox_db.resolve() in {original_test, original_prod}:
92:             "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
96:     config.paths = clone_paths(config.paths, sandbox_db)
98:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
99:     os.environ["OSBB_SANDBOX_MODE"] = "1"
100:     os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"
152: def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
154:     Give configured test operators sandbox-only permissions for service orders.
214:                 (str(user_id), SANDBOX_SERVICE_ROLE),
234:                     (SANDBOX_SERVICE_ROLE, resource, action, category),
255:                     (str(user_id), SANDBOX_SERVICE_ROLE),
267:                             SANDBOX_SERVICE_ROLE,
268:                             "Sandbox role for service-order workflow testing.",
288:                         (SANDBOX_SERVICE_ROLE, resource, action, category),
300:                                 SANDBOX_SERVICE_ROLE,
304:                                 "Sandbox-only service workflow permission.",
334:             "В service_orders_workspace.py не установлена готовая совместимая "
348:         "handlers.client_portal",
349:         "handlers.client_portal_v2",
352:         "handlers.service_orders_workspace",
360: def patch_bot_source() -> tuple[str, list[str]]:
362:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
365:     if not SERVICE_PATCHER.is_file():
366:         raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
369:     v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
370:     service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")
372:     source, v2_changes = v2.patch(source)
373:     source, service_changes = service.patch(source)
384: def live_service_preflight(db_path: Path) -> None:
400:                 "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
462:         "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
488:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
497:         help="Do not create sandbox-only service operator permissions.",
502:     print("OSBB LIVE SERVICES SANDBOX")
504:     print("Database:", LIVE_SERVICES_DB)
507:     if not LIVE_SERVICES_DB.is_file():
509:             "Не найдена live-services sandbox-БД:\n"
510:             f"  {LIVE_SERVICES_DB}"
513:     configure_sandbox(LIVE_SERVICES_DB)
514:     live_service_preflight(LIVE_SERVICES_DB)
519:         users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
520:         print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
522:             print("Sandbox backup before permission seed:", backup)
530:     source, bot_changes = patch_bot_source()
541:         print("Bots\\parking_bot.py and config.py were not changed.")
547:         print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
554:     print("Starting live services sandbox bot.")
556:     print(" ", LIVE_SERVICES_DB)
567:         print("\nLive services sandbox bot stopped by Ctrl+C.")
570:         print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
```

### `prepare_live_service_test.py`

- Score: `113`
- Kind: `py`
- SHA: `38850209e90a`
- Size: `12718`
- Modified: `2026-06-26 20:40:59`
- Markers: `parking_bot, service_orders_workspace, patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\service_orders_core.py`
- `G:\Programming\Py\OSBB\service_catalog_admin_core.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\install_service_orders_ui.py`
- `G:\Programming\Py\OSBB\access_control.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import re`
- `import sqlite3`
- `import sys`
- `from datetime import date, datetime`
- `from pathlib import Path`
- `from types import SimpleNamespace`
- `from typing import Any`
- `import config`

Interesting lines:
```text
2: Подготовка изолированной live sandbox к кликабельному тесту услуг.
4: Создаёт ТОЛЬКО в указанной sandbox:
9: Ничего не меняет в osbb_test.db, osbb.db, parking_bot.py и прежних sandbox.
30: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
31: DEFAULT_LAUNCHER = ROOT / "Start_OSBB_Live_Service_Sandbox_Bot.bat"
44: def clone_paths(original: Any, sandbox_db: Path):
58:     setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
62: def inside_sandbox(value: str | Path) -> Path:
65:         path.relative_to(SANDBOX_DIR.resolve())
67:         raise ValueError("Разрешены только БД внутри Data\\db\\sandbox.") from exc
69:         raise FileNotFoundError(f"Не найдена sandbox-БД: {path}")
73: def sandbox_from_launcher() -> Path:
77:     match = re.search(r'^set\s+"SANDBOX=(.+?)"\s*$', raw, flags=re.MULTILINE | re.IGNORECASE)
79:         raise RuntimeError("В launcher не найдена строка set \"SANDBOX=...\".")
80:     return inside_sandbox(match.group(1))
96:         raise RuntimeError(f"В sandbox нет роли: {role_code}")
113:             "Только live sandbox: тест услуг/пультов.",
124:         VALUES (?, ?, 'ALL', '*', 1, 'LIVE_SERVICE_SANDBOX',
125:                 'Только live sandbox: тестовый оператор услуг.', ?, ?)
145:     target.add_argument("--sandbox")
149:     parser.add_argument("--apply", action="store_true")
152:     if not args.apply:
153:         print("Для записи в sandbox добавьте --apply. Без него изменения не выполняются.")
156:     sandbox = inside_sandbox(args.sandbox) if args.sandbox else sandbox_from_launcher()
160:         "workspace": BOTS / "handlers" / "service_orders_workspace.py",
169:         print("Не установлена безопасная политика оплаты. Сначала install_service_orders_ui.py --apply.")
177:     config.paths = clone_paths(config.paths, sandbox)
179:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox)
180:     os.environ["OSBB_SANDBOX_MODE"] = "1"
196:         print("Sandbox не готова:", reason)
245:     conn = sqlite3.connect(sandbox)
273:                 description="Только live sandbox. Не утверждённый тариф.",
289:                 note="Только live sandbox: тестовый складской пульт.",
301:             VALUES (?, 'LIVE_SERVICE_SANDBOX', 'service_test_setup',
327:     print("LIVE SERVICE SANDBOX PREPARED")
329:     print("Sandbox:", sandbox)
338:     print("APPLIED ONLY TO THIS SANDBOX")
```

### `FIND_actual_service_order_state.py`

- Score: `105`
- Kind: `py`
- SHA: `a23e9644c711`
- Size: `14151`
- Modified: `2026-06-27 11:56:43`
- Markers: `parking_bot, service_orders_workspace, patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `service_orders_workspace.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_guard_workspace_v4.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`

Imports:
- `from __future__ import annotations`
- `import os`
- `import sqlite3`
- `import subprocess`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any, Iterable`

Interesting lines:
```text
383:         ROOT / "Bots" / "parking_bot.py",
384:         ROOT / "Bots" / "handlers" / "service_orders_workspace.py",
385:         ROOT / "run_bot_guard_sandbox_v3.py",
386:         ROOT / "patch_parking_bot_guard_workspace_v4.py",
```

### `run_bot_guard_sandbox_v3.py`

- Score: `88`
- Kind: `py`
- SHA: `40cd02f33d4f`
- Size: `7553`
- Modified: `2026-06-26 17:27:16`
- Markers: `parking_bot, client_portal, patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\config.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_guard_workspace_v4.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from pathlib import Path`
- `from types import SimpleNamespace`
- `from typing import Any`
- `import config`

Interesting lines:
```text
2: Запуск Telegram-бота с отдельной guard sandbox-копией БД.
6: - исходный parking_bot.py только для чтения;
7: - v2-переключение и guard patch только в памяти;
8: - указанную .db исключительно из Data/db/sandbox.
10: Не изменяет config.py и не сохраняет патч в parking_bot.py.
32: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
33: BOT_FILE = BOTS / "parking_bot.py"
35: GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v4.py"
48: def inside_sandbox(path: Path) -> Path:
51:         resolved.relative_to(SANDBOX_DIR.resolve())
54:             "Для запуска разрешены только .db внутри Data\\db\\sandbox."
59: def clone_paths(original: Any, sandbox_db: Path):
74:         setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
76:         object.__setattr__(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
80: def configure_sandbox(sandbox_db: Path) -> None:
87:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
89:     if sandbox_db == original_test or sandbox_db == original_prod:
90:         raise RuntimeError("Отказ: указан путь рабочей БД, а не sandbox-копии.")
92:     config.paths = clone_paths(config.paths, sandbox_db)
94:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
95:     os.environ["OSBB_SANDBOX_MODE"] = "1"
98: def table_rows(sandbox_db: Path) -> dict[str, int]:
109:     conn = sqlite3.connect(sandbox_db)
128: def patched_source() -> tuple[str, list[str], list[str]]:
130:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
133:     if not GUARD_PATCHER.exists():
134:         raise FileNotFoundError(f"Не найден guard patcher: {GUARD_PATCHER}")
136:     v2 = load_module(V2_SWITCHER, "_sandbox_v2_switcher")
137:     guard = load_module(GUARD_PATCHER, "_sandbox_guard_patcher")
140:     source, v2_changes = v2.patch(source)
141:     source, guard_changes = guard.patch(source)
157:             "handlers.client_portal",
158:             "handlers.client_portal_v2",
170:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
175:     parser.add_argument("--sandbox", required=True)
179:     sandbox_db = inside_sandbox(Path(args.sandbox))
180:     if not sandbox_db.exists():
181:         raise SystemExit(f"Не найдена sandbox-БД: {sandbox_db}")
184:     print("OSBB GUARD SANDBOX BOT V3")
186:     print("Sandbox DB:", sandbox_db)
190:         summary = table_rows(sandbox_db)
194:                 "Sandbox не подготовлен для кабинета охраны. Нет таблиц: "
199:         print("Sandbox rows:")
203:         configure_sandbox(sandbox_db)
204:         source, v2_changes, guard_changes = patched_source()
206:         print("Runtime patches:")
219:         print("All test records will be written only to:", sandbox_db)
220:         print("Stop this sandbox bot with Ctrl+C.")
226:         print("\nGuard sandbox bot stopped by Ctrl+C.")
229:         print("\nGUARD SANDBOX LAUNCH FAILED")
```

### `run_bot_guard_sandbox.py`

- Score: `88`
- Kind: `py`
- SHA: `12bd4911eea4`
- Size: `7550`
- Modified: `2026-06-26 12:38:25`
- Markers: `parking_bot, client_portal, patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\config.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_guard_workspace_v2.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from pathlib import Path`
- `from types import SimpleNamespace`
- `from typing import Any`
- `import config`

Interesting lines:
```text
2: Запуск Telegram-бота с отдельной guard sandbox-копией БД.
6: - исходный parking_bot.py только для чтения;
7: - v2-переключение и guard patch только в памяти;
8: - указанную .db исключительно из Data/db/sandbox.
10: Не изменяет config.py и не сохраняет патч в parking_bot.py.
32: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
33: BOT_FILE = BOTS / "parking_bot.py"
35: GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v2.py"
48: def inside_sandbox(path: Path) -> Path:
51:         resolved.relative_to(SANDBOX_DIR.resolve())
54:             "Для запуска разрешены только .db внутри Data\\db\\sandbox."
59: def clone_paths(original: Any, sandbox_db: Path):
74:         setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
76:         object.__setattr__(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
80: def configure_sandbox(sandbox_db: Path) -> None:
87:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
89:     if sandbox_db == original_test or sandbox_db == original_prod:
90:         raise RuntimeError("Отказ: указан путь рабочей БД, а не sandbox-копии.")
92:     config.paths = clone_paths(config.paths, sandbox_db)
94:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
95:     os.environ["OSBB_SANDBOX_MODE"] = "1"
98: def table_rows(sandbox_db: Path) -> dict[str, int]:
109:     conn = sqlite3.connect(sandbox_db)
128: def patched_source() -> tuple[str, list[str], list[str]]:
130:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
133:     if not GUARD_PATCHER.exists():
134:         raise FileNotFoundError(f"Не найден guard patcher: {GUARD_PATCHER}")
136:     v2 = load_module(V2_SWITCHER, "_sandbox_v2_switcher")
137:     guard = load_module(GUARD_PATCHER, "_sandbox_guard_patcher")
140:     source, v2_changes = v2.patch(source)
141:     source, guard_changes = guard.patch(source)
157:             "handlers.client_portal",
158:             "handlers.client_portal_v2",
170:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
175:     parser.add_argument("--sandbox", required=True)
179:     sandbox_db = inside_sandbox(Path(args.sandbox))
180:     if not sandbox_db.exists():
181:         raise SystemExit(f"Не найдена sandbox-БД: {sandbox_db}")
184:     print("OSBB GUARD SANDBOX BOT")
186:     print("Sandbox DB:", sandbox_db)
190:         summary = table_rows(sandbox_db)
194:                 "Sandbox не подготовлен для кабинета охраны. Нет таблиц: "
199:         print("Sandbox rows:")
203:         configure_sandbox(sandbox_db)
204:         source, v2_changes, guard_changes = patched_source()
206:         print("Runtime patches:")
219:         print("All test records will be written only to:", sandbox_db)
220:         print("Stop this sandbox bot with Ctrl+C.")
226:         print("\nGuard sandbox bot stopped by Ctrl+C.")
229:         print("\nGUARD SANDBOX LAUNCH FAILED")
```

### `run_bot_guard_sandbox_v2.py`

- Score: `88`
- Kind: `py`
- SHA: `3fc3c15cb59b`
- Size: `7553`
- Modified: `2026-06-26 13:44:44`
- Markers: `parking_bot, client_portal, patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\config.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `G:\Programming\Py\OSBB\patch_parking_bot_guard_workspace_v3.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import importlib.util`
- `import os`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from pathlib import Path`
- `from types import SimpleNamespace`
- `from typing import Any`
- `import config`

Interesting lines:
```text
2: Запуск Telegram-бота с отдельной guard sandbox-копией БД.
6: - исходный parking_bot.py только для чтения;
7: - v2-переключение и guard patch только в памяти;
8: - указанную .db исключительно из Data/db/sandbox.
10: Не изменяет config.py и не сохраняет патч в parking_bot.py.
32: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
33: BOT_FILE = BOTS / "parking_bot.py"
35: GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v3.py"
48: def inside_sandbox(path: Path) -> Path:
51:         resolved.relative_to(SANDBOX_DIR.resolve())
54:             "Для запуска разрешены только .db внутри Data\\db\\sandbox."
59: def clone_paths(original: Any, sandbox_db: Path):
74:         setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
76:         object.__setattr__(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
80: def configure_sandbox(sandbox_db: Path) -> None:
87:     original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
89:     if sandbox_db == original_test or sandbox_db == original_prod:
90:         raise RuntimeError("Отказ: указан путь рабочей БД, а не sandbox-копии.")
92:     config.paths = clone_paths(config.paths, sandbox_db)
94:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
95:     os.environ["OSBB_SANDBOX_MODE"] = "1"
98: def table_rows(sandbox_db: Path) -> dict[str, int]:
109:     conn = sqlite3.connect(sandbox_db)
128: def patched_source() -> tuple[str, list[str], list[str]]:
130:         raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
133:     if not GUARD_PATCHER.exists():
134:         raise FileNotFoundError(f"Не найден guard patcher: {GUARD_PATCHER}")
136:     v2 = load_module(V2_SWITCHER, "_sandbox_v2_switcher")
137:     guard = load_module(GUARD_PATCHER, "_sandbox_guard_patcher")
140:     source, v2_changes = v2.patch(source)
141:     source, guard_changes = guard.patch(source)
157:             "handlers.client_portal",
158:             "handlers.client_portal_v2",
170:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
175:     parser.add_argument("--sandbox", required=True)
179:     sandbox_db = inside_sandbox(Path(args.sandbox))
180:     if not sandbox_db.exists():
181:         raise SystemExit(f"Не найдена sandbox-БД: {sandbox_db}")
184:     print("OSBB GUARD SANDBOX BOT V2")
186:     print("Sandbox DB:", sandbox_db)
190:         summary = table_rows(sandbox_db)
194:                 "Sandbox не подготовлен для кабинета охраны. Нет таблиц: "
199:         print("Sandbox rows:")
203:         configure_sandbox(sandbox_db)
204:         source, v2_changes, guard_changes = patched_source()
206:         print("Runtime patches:")
219:         print("All test records will be written only to:", sandbox_db)
220:         print("Stop this sandbox bot with Ctrl+C.")
226:         print("\nGuard sandbox bot stopped by Ctrl+C.")
229:         print("\nGUARD SANDBOX LAUNCH FAILED")
```

### `Recovered_Releases\2026-06-27__OSBB_live_services_sandbox_bundle\patch_parking_bot_service_orders_v1.py`

- Score: `83`
- Kind: `py`
- SHA: `07e623d30310`
- Size: `3161`
- Modified: `2026-07-02 22:59:39`
- Markers: `parking_bot, service_orders_workspace, patches_in_memory`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`

Imports:
- `from __future__ import annotations`
- `from pathlib import Path`

Interesting lines:
```text
3: Runtime patch for OSBB service orders / remotes / access.
5: The patch does not change Bots\\parking_bot.py by itself. It adds:
9: It is deliberately independent from the old guard-workspace patch.
18: BOT_FILE = ROOT / "Bots" / "parking_bot.py"
21:     "from handlers.service_orders_workspace import handle_service_orders_text\n"
29:     # service_orders_workspace хранит собственные состояния в user_states.
44:     if "from handlers.service_orders_workspace import handle_service_orders_text" in source:
56:         "Не найден безопасный якорь импорта для service_orders_workspace."
83: def patch(source: str) -> tuple[str, list[str]]:
88:         changes.append("service_orders_workspace import")
95:         "from handlers.service_orders_workspace import handle_service_orders_text",
```

### `cashier_v2_preflight.py`

- Score: `80`
- Kind: `py`
- SHA: `4b7af3d6ab60`
- Size: `16996`
- Modified: `2026-06-25 18:35:51`
- Markers: `parking_bot, client_portal, patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\config.py`
- `- migrate_cashier_operator_editor.py`
- `- migrate_cashier_v2.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\cashier_v2_preflight.py`
- `G:\Programming\Py\OSBB\migrate_cashier_operator_editor.py`
- `G:\Programming\Py\OSBB\migrate_cashier_v2.py`
- `G:\Programming\Py\OSBB\cashier_v2_core.py`
- `G:\Programming\Py\OSBB\Bots\handlers\cashier_operator_v2.py`
- `G:\Programming\Py\OSBB\Bots\handlers\client_portal_v2.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `client_portal.py`
- `G:\Programming\Py\OSBB\Bots\handlers\cashier_operator.py`
- `OK  cashier_v2_core.py`
- `Import cashier_v2_core.py`
- `ERR cashier_v2_core.py`
- `OK  cashier_operator_v2.py`
- `Import cashier_operator_v2.py`
- `ERR cashier_operator_v2.py`
- `OK  client_portal_v2.py`
- `Import client_portal_v2.py`
- `ERR client_portal_v2.py`
- `parking_bot_v2_in_memory.py`

Imports:
- `from __future__ import annotations`
- `import importlib.util`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any`
- `from config import paths, USE_TEST_DB`

Interesting lines:
```text
7: 2. Делает её SQLite-снимок в Data/db/sandbox/.
13: 6. Проверяет, можно ли переключить parking_bot.py на v2 в памяти,
14:    не записывая parking_bot.py.
16: Исходный osbb_test.db и osbb.db остаются только для чтения.
22:   - sandbox-копия БД;
23:   - отчёт в Data/db/sandbox/;
154: def apply_v1_to_clone(conn: sqlite3.Connection, m1: Any) -> dict[str, Any]:
242: def apply_v2_to_clone(conn: sqlite3.Connection, m2: Any) -> dict[str, Any]:
288:     db = paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
291:     sandbox_dir = db.parent / "sandbox"
292:     sandbox_dir.mkdir(parents=True, exist_ok=True)
293:     sandbox_db = sandbox_dir / f"{db.stem}_cashier_v2_check_{stamp()}{db.suffix}"
294:     report = sandbox_dir / f"cashier_v2_preflight_{stamp()}.txt"
301:         "client portal v2": HANDLERS_DIR / "client_portal_v2.py",
303:         "current parking_bot": BOTS_DIR / "parking_bot.py",
304:         "base client portal": HANDLERS_DIR / "client_portal.py",
310:         "CASHIER V2 PREFLIGHT — SAFE SANDBOX CHECK",
313:         f"Sandbox DB: {sandbox_db}",
369:         load_module(HANDLERS_DIR / "client_portal_v2.py", "_client_portal_v2_preflight")
370:         lines.append("   OK  client_portal_v2.py import")
373:         errors.append("Import client_portal_v2.py")
374:         lines.append("   ERR client_portal_v2.py import")
377:     # 3. Snapshot. From this moment only sandbox can be modified.
381:         copy_sqlite_snapshot(db, sandbox_db)
382:         lines.append(f"   OK  snapshot created: {sandbox_db.name}")
385:         errors.append("Не удалось создать sandbox-копию БД")
389:     # 4. Apply migrations to clone only.
390:     if sandbox_db.exists():
392:         lines.append("4. Применение миграций только к sandbox-копии")
396:             conn = sqlite3.connect(sandbox_db)
399:                 v1_result = apply_v1_to_clone(conn, m1)
400:                 v2_result = apply_v2_to_clone(conn, m2)
412:             errors.append("Миграция v1/v2 не прошла на sandbox-копии")
417:     if sandbox_db.exists():
419:         lines.append("5. Проверка структуры sandbox-копии")
421:             conn = sqlite3.connect(sandbox_db)
447:     # 6. In-memory patch validation for parking_bot.
449:     lines.append("6. Проверка переключения parking_bot.py в памяти")
452:         original = (BOTS_DIR / "parking_bot.py").read_text(encoding="utf-8")
453:         patched, changes = switch.patch(original)
454:         compile(patched, "parking_bot_v2_in_memory.py", "exec")
455:         lines.append("   OK  parking_bot v2 switch compiles in memory")
459:         errors.append("Переключение parking_bot.py на v2 не прошло в памяти")
460:         lines.append("   ERR switch in memory")
471:         lines.append("RESULT: READY FOR SANDBOX BOT TEST")
473:             "Active DB was not modified. Sandbox copy contains the migration result."
```

### `CHECK_profile_button_early_route_fix.py`

- Score: `80`
- Kind: `py`
- SHA: `ab47ded545cb`
- Size: `1914`
- Modified: `2026-06-27 21:42:12`
- Markers: `client_portal, handle_client_portal_text, patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\run_bot_live_services_sandbox_v1.py`

Imports:
- `from __future__ import annotations`
- `import sys`
- `from pathlib import Path`
- `import run_bot_live_services_sandbox_v1 as runner`

Interesting lines:
```text
24:     launcher = ROOT / "run_bot_live_services_sandbox_v1.py"
28:     import run_bot_live_services_sandbox_v1 as runner
30:     source, changes = runner.patch_bot_source()
39:     portal_index = source.find("if await handle_client_portal_text(")
```

### `INSTALL_profile_button_early_route_fix.py`

- Score: `80`
- Kind: `py`
- SHA: `fdadce23cbcd`
- Size: `2354`
- Modified: `2026-06-27 21:42:12`
- Markers: `parking_bot, client_portal, patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\run_bot_live_services_sandbox_v1.py`

Imports:
- `from __future__ import annotations`
- `import py_compile`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
6: Only the live-services sandbox launcher is replaced. It still patches
7: Bots/parking_bot.py in memory; Bots/parking_bot.py and the SQLite database
8: are never written by this installer.
22:     / "run_bot_live_services_sandbox_v1.py"
24: TARGET = ROOT / "run_bot_live_services_sandbox_v1.py"
38:         "def ensure_cashier_route_precedes_client_portal(",
```

### `Bots\handlers\client_portal.py`

- Score: `75`
- Kind: `py`
- SHA: `ff43b32733d3`
- Size: `98291`
- Modified: `2026-06-28 17:41:44`
- Markers: `parking_bot, client_portal, handle_client_portal_text, sandbox_db, ukrainian_ui, remote_button`

References:
- `Let the existing mode switch be processed by parking_bot.py`

Imports:
- `from __future__ import annotations`
- `from datetime import datetime`
- `from pathlib import Path`
- `import re`
- `import sqlite3`
- `import sys`
- `from typing import Any`
- `from telegram import Update, ReplyKeyboardMarkup`
- `from config import paths, USE_TEST_DB`
- `from audit_logger import audit_log`

Interesting lines:
```text
82:         "remote_list": "🔑 Заявки на пульты",
169:         "remote_admin_title": "🔑 Заявки на пульты — оператор",
189:     "uk": {
191:         "choose_menu": "Будь ласка, оберіть дію кнопкою українською мовою.",
198:         "remotes": "🔑 Пульти",
217:         "remote_list": "🔑 Заявки на пульти",
276:         "remotes_title": "🔑 Пульти шлагбаума",
304:         "remote_admin_title": "🔑 Заявки на пульти — оператор",
320:         "remote_missing_table": "Розділ заявок на пульти ще підключається. Зверніться до оператора.",
518:     return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
563:     if isinstance(value, dict) and value.get("_module") == "client_portal":
566:         value = {"_module": "client_portal", "mode": "client_home"}
575:         isinstance(value, dict) and value.get("_module") == "client_portal"
792:                 source_context="client_portal",
919:                     source_context="client_portal",
955:                 source_context="client_portal",
1270:         "PARKING_DAY": {"ru": "Парковка Day", "uk": "Паркування Day", "en": "Parking Day"},
1271:         "PARKING_NIGHT": {"ru": "Парковка Night", "uk": "Паркування Night", "en": "Parking Night"},
1470:                 source_context="client_portal",
1582:                 source_context="client_portal",
1654: async def show_client_portal(update: Update, user_states: dict, user_id: int, lang: str) -> None:
1677:         await show_client_portal(update, user_states, user_id, lang)
1745:         await show_client_portal(update, user_states, user_id, lang)
1760:         await show_client_portal(update, user_states, user_id, lang)
1776:         await show_client_portal(update, user_states, user_id, lang)
1840: async def handle_client_portal_text(
1859:     # Let the existing mode switch be processed by parking_bot.py.
1968:         if message_text == tr(lang, "remote_list") or message_text == "🔑 Заявки на пульты":
2060:         await show_client_portal(update, user_states, user_id, lang)
2078:             await show_client_portal(update, user_states, user_id, lang)
2099:         await show_client_portal(update, user_states, user_id, lang)
2104:         await show_client_portal(update, user_states, user_id, lang)
2158:             await show_client_portal(update, user_states, user_id, lang)
2168:             await show_client_portal(update, user_states, user_id, lang)
2233:             await show_client_portal(update, user_states, user_id, lang)
2267:     await show_client_portal(update, user_states, user_id, lang)
```

### `patch_parking_bot_service_orders_v1.py`

- Score: `75`
- Kind: `py`
- SHA: `07e623d30310`
- Size: `3161`
- Modified: `2026-06-27 12:15:01`
- Markers: `parking_bot, service_orders_workspace, patches_in_memory`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`

Imports:
- `from __future__ import annotations`
- `from pathlib import Path`

Interesting lines:
```text
3: Runtime patch for OSBB service orders / remotes / access.
5: The patch does not change Bots\\parking_bot.py by itself. It adds:
9: It is deliberately independent from the old guard-workspace patch.
18: BOT_FILE = ROOT / "Bots" / "parking_bot.py"
21:     "from handlers.service_orders_workspace import handle_service_orders_text\n"
29:     # service_orders_workspace хранит собственные состояния в user_states.
44:     if "from handlers.service_orders_workspace import handle_service_orders_text" in source:
56:         "Не найден безопасный якорь импорта для service_orders_workspace."
83: def patch(source: str) -> tuple[str, list[str]]:
88:         changes.append("service_orders_workspace import")
95:         "from handlers.service_orders_workspace import handle_service_orders_text",
```

### `INSTALL_PHONE_ACCESS_UI_FIX.bat`

- Score: `75`
- Kind: `bat`
- SHA: `75ad4a9b988f`
- Size: `1314`
- Modified: `2026-06-27 16:45:04`
- Markers: `service_orders_workspace, installer, sandbox_db`

References:
- `echo This installer replaces only Bots\handlers\service_orders_workspace.py`
- `dp0Bots\handlers\service_orders_workspace.py`
- `\Bots\handlers\service_orders_workspace.py`
- `echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

Interesting lines:
```text
6: echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C before continuing.
7: echo This installer replaces only Bots\handlers\service_orders_workspace.py.
11: set "SRC=%~dp0Bots\handlers\service_orders_workspace.py"
12: set "DST=%ROOT%\Bots\handlers\service_orders_workspace.py"
```

### `switch_parking_bot_to_cashier_v2.py`

- Score: `70`
- Kind: `py`
- SHA: `28dadc592b16`
- Size: `4455`
- Modified: `2026-06-25 17:44:55`
- Markers: `parking_bot, client_portal, patches_in_memory, installer`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `backup parking_bot.py`
- `G:\Programming\Py\OSBB\Bots\handlers\client_portal_v2.py`
- `G:\Programming\Py\OSBB\Bots\handlers\cashier_operator_v2.py`
- `G:\Programming\Py\OSBB\cashier_v2_core.py`

Imports:
- `from __future__ import annotations`
- `from datetime import datetime`
- `from pathlib import Path`
- `import argparse`
- `import shutil`

Interesting lines:
```text
4: Что меняется в Bots/parking_bot.py:
5: - handlers.client_portal -> handlers.client_portal_v2
10: Patcher создаёт backup parking_bot.py перед --apply.
22: BOT_FILE = ROOT / "Bots" / "parking_bot.py"
24:     ROOT / "Bots" / "handlers" / "client_portal_v2.py",
35: def patch(source: str) -> tuple[str, list[str]]:
38:     old = "from handlers.client_portal import ("
39:     new = "from handlers.client_portal_v2 import ("
42:         changes.append("client_portal -> client_portal_v2")
57:     client_v2 = "from handlers.client_portal_v2 import (" in source
62:     if client_v2 and not any("client_portal" in item for item in changes):
63:         changes.append("client_portal already v2")
69:             "Не найден импорт client_portal. "
70:             "В текущем parking_bot.py нет ожидаемого подключения клиентского кабинета."
75:             "В текущем parking_bot.py нет ожидаемого подключения кассы v1."
83:     parser.add_argument("--apply", action="store_true")
90:     print("Apply:", args.apply)
98:         raise SystemExit(f"Не найден parking_bot.py: {BOT_FILE}")
101:     patched, changes = patch(original)
104:         compile(patched, str(BOT_FILE), "exec")
114:     print("Changes needed:", patched != original)
116:     if not args.apply:
121:     if patched == original:
128:     BOT_FILE.write_text(patched, encoding="utf-8")
```

### `run_bot_sandbox_v2.py`

- Score: `68`
- Kind: `py`
- SHA: `1312e7f35e0b`
- Size: `9548`
- Modified: `2026-06-25 21:09:41`
- Markers: `parking_bot, client_portal, patches_in_memory, sandbox_db`

References:
- `G:\Programming\Py\config.py`
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\run_bot_sandbox_v2.py`
- `G:\Programming\Py\OSBB\switch_parking_bot_to_cashier_v2.py`
- `Must run before importing parking_bot.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import copy`
- `import os`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from pathlib import Path`
- `from types import SimpleNamespace`
- `from typing import Any`
- `import importlib.util`
- `import config`

Interesting lines:
```text
2: Безопасный запуск Telegram-бота с sandbox-копией БД и кассой v2.
6: - заменяет рабочий Bots/parking_bot.py;
7: - изменяет osbb_test.db или osbb.db.
9: Он запускает parking_bot.py только в памяти:
10: - подменяет путь TEST-БД на явно заданную копию из Data/db/sandbox;
11: - подменяет импорты client_portal/cashier_operator на v2 только в памяти;
20:   g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\run_bot_sandbox_v2.py ^
21:     --sandbox "G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db"
24:   g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\run_bot_sandbox_v2.py ^
25:     --sandbox "G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db" ^
44: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
45: BOT_FILE = BOTS_DIR / "parking_bot.py"
60: def ensure_inside_sandbox(path: Path) -> Path:
62:     sandbox = SANDBOX_DIR.resolve()
64:         resolved.relative_to(sandbox)
67:             "Разрешены только базы внутри папки Data\\db\\sandbox.\n"
69:             f"Разрешённая папка: {sandbox}"
74: def clone_paths_with_sandbox(original_paths: Any, sandbox_db: Path):
97:         setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
100:         object.__setattr__(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
140: def configure_runtime_database(sandbox_db: Path) -> None:
142:     Must run before importing parking_bot.py and its project modules.
150:     original_test = Path(config.paths.OSBB_TEST_DB_FILE)
153:     if same_path(sandbox_db, original_test) or same_path(sandbox_db, original_prod):
155:             "Отказ: передана рабочая БД, а не sandbox-копия."
158:     config.paths = clone_paths_with_sandbox(config.paths, sandbox_db)
162:     os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
163:     os.environ["OSBB_SANDBOX_MODE"] = "1"
166: def patched_bot_source() -> tuple[str, list[str]]:
172:     switcher = load_module(SWITCHER_FILE, "_osbb_sandbox_switcher")
174:     patched, changes = switcher.patch(source)
175:     compile(patched, str(BOT_FILE), "exec")
176:     return patched, changes
181:     parking_bot.py executed from its true path, but only the patched source
191:             "handlers.client_portal",
192:             "handlers.client_portal_v2",
205:     exec(compile(source, str(BOT_FILE), "exec"), namespace)
210:         description="Run OSBB bot v2 with a sandbox database only."
213:         "--sandbox",
215:         help="Absolute path to a .db file inside Data\\db\\sandbox",
224:     sandbox_db = ensure_inside_sandbox(Path(args.sandbox))
225:     if not sandbox_db.exists():
226:         raise SystemExit(f"Не найдена sandbox-копия БД: {sandbox_db}")
229:     print("OSBB SANDBOX BOT V2")
232:     print("Sandbox DB:", sandbox_db)
238:         summary = sqlite_summary(sandbox_db)
242:                 "Sandbox-копия не содержит таблицы v2: " + ", ".join(missing)
245:         print("Sandbox DB tables:")
249:         configure_runtime_database(sandbox_db)
250:         source, changes = patched_bot_source()
253:         print("Runtime patch:")
268:         print("   ", sandbox_db)
269:         print("3. Stop sandbox bot with Ctrl+C when testing is finished.")
271:         print("Starting sandbox bot...")
276:         print("\nSandbox bot stopped by Ctrl+C.")
279:         print("\nSANDBOX LAUNCH FAILED")
```

### `patch_parking_bot_guard_workspace_v4.py`

- Score: `65`
- Kind: `py`
- SHA: `0d8d4e9fb6b3`
- Size: `9165`
- Modified: `2026-06-26 17:25:49`
- Markers: `parking_bot, patches_in_memory, installer`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `guard_workspace.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
2: Подключение отдельного кабинета охраны к Bots/parking_bot.py — версия с выходом из кабинета.
11: Не меняет исходный parking_bot.py без --apply.
23: BOT_FILE = ROOT / "Bots" / "parking_bot.py"
157: def patch(source: str) -> tuple[str, list[str]]:
217:     parser.add_argument("--apply", action="store_true")
221:     print("PATCH PARKING BOT: GUARD WORKSPACE V4")
224:     print("Apply:", args.apply)
229:         raise SystemExit(f"Не найден parking_bot.py: {BOT_FILE}")
233:         patched, changes = patch(original)
234:         compile(patched, str(BOT_FILE), "exec")
238:             "Исходный parking_bot.py не изменён."
242:     for item in changes or ["already patched"]:
244:     print("Changes needed:", patched != original)
246:     if not args.apply:
250:     if patched == original:
251:         print("ALREADY PATCHED - NO FILE CHANGE")
259:     BOT_FILE.write_text(patched, encoding="utf-8")
```

### `patch_parking_bot_guard_workspace_v2.py`

- Score: `65`
- Kind: `py`
- SHA: `f76dd1f10258`
- Size: `9872`
- Modified: `2026-06-26 12:36:23`
- Markers: `parking_bot, patches_in_memory, installer`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `guard_workspace.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
2: Подключение отдельного кабинета охраны к Bots/parking_bot.py.
4: Изменяет только код бота при --apply:
24: BOT_FILE = ROOT / "Bots" / "parking_bot.py"
120: def patch(source: str) -> tuple[str, list[str]]:
231:     parser.add_argument("--apply", action="store_true")
235:     print("PATCH PARKING BOT: GUARD WORKSPACE")
238:     print("Apply:", args.apply)
243:         raise SystemExit(f"Не найден parking_bot.py: {BOT_FILE}")
247:         patched, changes = patch(original)
248:         compile(patched, str(BOT_FILE), "exec")
252:             "Исходный parking_bot.py не изменён."
256:     for item in changes or ["already patched"]:
258:     print("Changes needed:", patched != original)
260:     if not args.apply:
264:     if patched == original:
265:         print("ALREADY PATCHED - NO FILE CHANGE")
273:     BOT_FILE.write_text(patched, encoding="utf-8")
```

### `patch_parking_bot_guard_workspace_v3.py`

- Score: `65`
- Kind: `py`
- SHA: `6ae388f7041a`
- Size: `8636`
- Modified: `2026-06-26 12:52:06`
- Markers: `parking_bot, patches_in_memory, installer`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `guard_workspace.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
2: Подключение отдельного кабинета охраны к Bots/parking_bot.py — совместимая версия.
11: Не меняет исходный parking_bot.py без --apply.
23: BOT_FILE = ROOT / "Bots" / "parking_bot.py"
147: def patch(source: str) -> tuple[str, list[str]]:
207:     parser.add_argument("--apply", action="store_true")
211:     print("PATCH PARKING BOT: GUARD WORKSPACE V3")
214:     print("Apply:", args.apply)
219:         raise SystemExit(f"Не найден parking_bot.py: {BOT_FILE}")
223:         patched, changes = patch(original)
224:         compile(patched, str(BOT_FILE), "exec")
228:             "Исходный parking_bot.py не изменён."
232:     for item in changes or ["already patched"]:
234:     print("Changes needed:", patched != original)
236:     if not args.apply:
240:     if patched == original:
241:         print("ALREADY PATCHED - NO FILE CHANGE")
249:     BOT_FILE.write_text(patched, encoding="utf-8")
```

### `tools\harvest_lost_features_from_sandboxes.py`

- Score: `63`
- Kind: `py`
- SHA: `c2fb6916e07a`
- Size: `18163`
- Modified: `2026-07-02 18:35:54`
- Markers: `patches_in_memory, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\tools\harvest_lost_features_from_sandboxes.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import os`
- `import sqlite3`
- `from dataclasses import dataclass, field`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any`

Interesting lines:
```text
4: harvest_lost_features_from_sandboxes.py
6: Compares the current Golden/Working DB with sandbox DBs and reports "lost" or stronger
7: feature candidates: modules/data/code-era evidence that exist in sandbox DBs but are
15:     G:\Programming\Py\OSBB\Data\db\osbb_test.db
19:     G:\Programming\Py\OSBB\Data\db\sandbox
22:     G:\Programming\Py\OSBB\Data\exports\db_rank\LOST_FEATURES_FROM_SANDBOXES.md
26:   python .\OSBB\tools\harvest_lost_features_from_sandboxes.py
28:   python .\OSBB\tools\harvest_lost_features_from_sandboxes.py `
31:   python .\OSBB\tools\harvest_lost_features_from_sandboxes.py `
32:     --candidate-dir "G:\Programming\Py\OSBB\Data\db\sandbox" `
33:     --out "G:\Programming\Py\OSBB\Data\exports\db_rank\LOST_FEATURES_FROM_SANDBOXES.md"
48: DEFAULT_BASE_DB = DEFAULT_ROOT / "Data" / "db" / "osbb_test.db"
51:     DEFAULT_ROOT / "Data" / "db" / "sandbox",
53: DEFAULT_OUT = DEFAULT_ROOT / "Data" / "exports" / "db_rank" / "LOST_FEATURES_FROM_SANDBOXES.md"
374:     lines.append("# OSBB Lost / Stronger Feature Harvest from Sandbox DBs")
409:         lines.append("No obviously stronger sandbox feature candidates found.")
411:         lines.append("| Feature | Base score | Best sandbox score | Best DB | Candidates |")
439:             lines.append("No stronger sandbox candidate detected.")
443:         lines.append("Stronger sandbox candidates:")
467:     lines.append("3. Open the strongest sandbox candidate for that feature.")
470:     lines.append("6. Apply changes only through explicit migrations or patches.")
492:     print("OSBB harvest lost/stronger features from sandboxes")
```

### `INSTALL_service_code_compatibility_phone_v2.py`

- Score: `60`
- Kind: `py`
- SHA: `373835d6b404`
- Size: `3511`
- Modified: `2026-06-27 20:18:29`
- Markers: `service_orders_workspace, installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\service_orders_core.py`
- `G:\Programming\Py\OSBB\service_preorders_core.py`
- `service_orders_workspace.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import py_compile`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
3: Restore compatibility with sandbox databases that use base_service_code.
42:         help="OSBB root (default: folder containing this installer).",
50:         PAYLOAD / "Bots" / "handlers" / "service_orders_workspace.py":
51:             ROOT / "Bots" / "handlers" / "service_orders_workspace.py",
58:         ROOT / "Bots" / "handlers" / "service_orders_workspace.py": "def _current_offers()",
90:     print("This repair did not change the sandbox database.")
```

### `Bots\parking_bot.py`

- Score: `55`
- Kind: `py`
- SHA: `282fb147a8fc`
- Size: `48180`
- Modified: `2026-06-30 20:24:15`
- Markers: `client_portal, handle_client_portal_text, sandbox_db, ukrainian_ui, remote_button`

Imports:
- `from pathlib import Path`
- `import sys`
- `from telegram import Update, ReplyKeyboardMarkup`
- `from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters`
- `from handlers.vehicle_verification import handle_vehicle_verification_text`
- `from handlers.vehicle_card_editor import handle_vehicle_card_editor_text`
- `from handlers.vehicle_full_list import handle_vehicle_full_list_text`
- `from handlers.audit_viewer import handle_audit_viewer_text`
- `from handlers.client_portal import (`
- `from handlers.cashier_operator import handle_cashier_operator_text`
- `from handlers.unit_registry_editor import handle_unit_registry_editor_text`
- `from config import paths`
- `from telegram_osbb import (`
- `from Bots.db_access import (`
- `from Bots.handlers.agreement import (`
- `import os`
- `from config import paths, USE_TEST_DB`
- `import sqlite3`

Interesting lines:
```text
11: from handlers.client_portal import (
12:     handle_client_portal_text,
103:     "uk": {
110:         "remotes": "🔑 Пульти",
131:     ["🇺🇦 Українська"],
154:     ["🔑 Заявки на пульты"],
248:         return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
821:     if text == "🇺🇦 Українська":
822:         user_languages[user_id] = "uk"
823:         lang = "uk"
1106:     # Клиентский кабинет / заявки на пульты
1110:     # В admin-режиме обрабатывает только «Заявки на пульты».
1111:     if await handle_client_portal_text(
1340:     if text == "🔑 Заявки на пульты":
1342:             "🔑 Заявки на пульты\n\n"
```

### `Bots\handlers\client_portal_v2.py`

- Score: `55`
- Kind: `py`
- SHA: `8b23fc5687f3`
- Size: `29207`
- Modified: `2026-06-25 17:42:42`
- Markers: `parking_bot, client_portal, handle_client_portal_text, ukrainian_ui`

References:
- `G:\Programming\Py\OSBB\Bots\handlers\client_portal.py`
- `These two functions are used by parking_bot.py`

Imports:
- `from __future__ import annotations`
- `from pathlib import Path`
- `import sys`
- `from typing import Any`
- `from telegram import ReplyKeyboardMarkup, Update`
- `from handlers import client_portal as base`
- `from cashier_v2_core import (`

Interesting lines:
```text
4: Работает поверх действующего client_portal.py:
12: Этот модуль экспортирует те же три функции, что и прежний client_portal.py:
15:   handle_client_portal_text
34: from handlers import client_portal as base
104:     "uk": {
221: # These two functions are used by parking_bot.py after the import path is swapped.
243:     return isinstance(value, dict) and value.get("_module") == "client_portal"
269:         "uk": {
300:     for lang in ("ru", "uk", "en"):
365:         await base.show_client_portal(update, user_states, user_id, lang)
379:         await base.show_client_portal(update, user_states, user_id, lang)
458:         await base.show_client_portal(update, {}, user_id, lang)
478: async def handle_client_portal_text(
493:         return await base.handle_client_portal_text(
507:         return await base.handle_client_portal_text(
523:             await base.show_client_portal(update, user_states, user_id, lang)
```

### `INSTALL_PHONE_ACCESS_UI_FIX_v2.bat`

- Score: `45`
- Kind: `bat`
- SHA: `348f4ca1e243`
- Size: `379`
- Modified: `2026-06-27 16:50:16`
- Markers: `installer, sandbox_db`

References:
- `dp0INSTALL_PHONE_ACCESS_UI_FIX_v2.py`
- `stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

Interesting lines:
```text
7: echo OSBB phone-access UI fix — reliable installer
9: echo Before continuing, stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C.
11: "%PY%" "%~dp0INSTALL_PHONE_ACCESS_UI_FIX_v2.py" --root "%ROOT%" --python "%PY%"
```

### `INSTALL_PHONE_ACCESS_UI_FIX_v3.bat`

- Score: `45`
- Kind: `bat`
- SHA: `a77dbef10399`
- Size: `337`
- Modified: `2026-06-27 17:20:35`
- Markers: `installer, sandbox_db`

References:
- `dp0INSTALL_PHONE_ACCESS_UI_FIX_v3.py`
- `echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

Interesting lines:
```text
7: echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C first.
9: "%PY%" "%~dp0INSTALL_PHONE_ACCESS_UI_FIX_v3.py" --root "%ROOT%" --python "%PY%"
```

### `RUN_INSTALL_cashier_route_after_phone_v2.bat`

- Score: `45`
- Kind: `bat`
- SHA: `a60f1fe05e10`
- Size: `321`
- Modified: `2026-06-27 20:00:41`
- Markers: `installer, sandbox_db`

References:
- `\INSTALL_cashier_route_after_phone_v2.py`

Interesting lines:
```text
8: echo Stop the sandbox bot with Ctrl+C before continuing.
11: "%PY%" "%ROOT%\INSTALL_cashier_route_after_phone_v2.py"
```

### `RUN_INSTALL_phone_barrier_access_v2.bat`

- Score: `45`
- Kind: `bat`
- SHA: `47ff9e10d5a7`
- Size: `404`
- Modified: `2026-06-27 19:31:21`
- Markers: `installer, sandbox_db`

References:
- `\INSTALL_phone_barrier_access_v2.py`
- `echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

Interesting lines:
```text
7: echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat before continuing.
10: "%PY%" "%ROOT%\INSTALL_phone_barrier_access_v2.py"
```

### `RUN_INSTALL_profile_button_early_route_fix.bat`

- Score: `45`
- Kind: `bat`
- SHA: `741a23a50e94`
- Size: `310`
- Modified: `2026-06-27 21:42:12`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\INSTALL_profile_button_early_route_fix.py`

Interesting lines:
```text
7: echo Stop the sandbox bot with Ctrl+C before continuing.
9: "%PY%" "%ROOT%\INSTALL_profile_button_early_route_fix.py"
```

### `RUN_INSTALL_profile_confirmation_ready_visibility_fix.bat`

- Score: `45`
- Kind: `bat`
- SHA: `8f7cc69360c6`
- Size: `329`
- Modified: `2026-06-27 21:55:13`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\INSTALL_profile_confirmation_ready_visibility_fix.py`

Interesting lines:
```text
7: echo Stop the sandbox bot with Ctrl+C before continuing.
9: "%PY%" "%ROOT%\INSTALL_profile_confirmation_ready_visibility_fix.py"
```

### `RUN_INSTALL_profile_critical_codes_fix.bat`

- Score: `45`
- Kind: `bat`
- SHA: `f456e71c0a00`
- Size: `302`
- Modified: `2026-06-27 21:45:58`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\INSTALL_profile_critical_codes_fix.py`

Interesting lines:
```text
7: echo Stop the sandbox bot with Ctrl+C before continuing.
9: "%PY%" "%ROOT%\INSTALL_profile_critical_codes_fix.py"
```

### `RUN_INSTALL_profile_parking_time_test_v1.bat`

- Score: `45`
- Kind: `bat`
- SHA: `df9e25301e89`
- Size: `342`
- Modified: `2026-06-28 12:11:29`
- Markers: `installer, sandbox_db`

References:
- `\INSTALL_profile_parking_time_test_v1.py`
- `echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

Interesting lines:
```text
7: echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C first.
9: "%PY%" "%ROOT%\INSTALL_profile_parking_time_test_v1.py"
```

### `RUN_INSTALL_profile_verification_terminology_v2.bat`

- Score: `45`
- Kind: `bat`
- SHA: `34e655342372`
- Size: `327`
- Modified: `2026-06-27 21:22:51`
- Markers: `installer, sandbox_db`

References:
- `\INSTALL_profile_verification_terminology_v2.py`

Interesting lines:
```text
7: echo Stop the sandbox bot with Ctrl+C before continuing.
9: "%PY%" "%ROOT%\INSTALL_profile_verification_terminology_v2.py"
```

### `RUN_INSTALL_profile_verification_v1.bat`

- Score: `45`
- Kind: `bat`
- SHA: `e224114dac20`
- Size: `338`
- Modified: `2026-06-27 20:48:59`
- Markers: `installer, sandbox_db`

References:
- `\INSTALL_profile_verification_v1.py`
- `echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

Interesting lines:
```text
6: echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C first.
8: "%PY%" "%ROOT%\INSTALL_profile_verification_v1.py"
```

### `RUN_INSTALL_service_code_compatibility_phone_v2.bat`

- Score: `45`
- Kind: `bat`
- SHA: `45cec96c4559`
- Size: `341`
- Modified: `2026-06-27 20:18:30`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\INSTALL_service_code_compatibility_phone_v2.py`

Interesting lines:
```text
8: echo Stop the sandbox bot with Ctrl+C before continuing.
11: "%PY%" "%ROOT%\INSTALL_service_code_compatibility_phone_v2.py"
```

### `CHECK_service_code_compatibility_phone_v2.py`

- Score: `40`
- Kind: `py`
- SHA: `31a1838dbae4`
- Size: `3831`
- Modified: `2026-06-27 20:18:29`
- Markers: `service_orders_workspace, sandbox_db`

References:
- `G:\Programming\Py\OSBB\service_orders_core.py`
- `G:\Programming\Py\OSBB\service_preorders_core.py`
- `service_orders_workspace.py`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `from pathlib import Path`

Interesting lines:
```text
3: Read-only compatibility check for the two-barrier phone-access sandbox.
13: SANDBOX_DB = (
14:     ROOT / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
28:     if not SANDBOX_DB.is_file():
29:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
33:     workspace = ROOT / "Bots" / "handlers" / "service_orders_workspace.py"
57:     conn = sqlite3.connect(SANDBOX_DB)
78:         print("Database:", SANDBOX_DB)
```

### `create_clean_live_sandbox.py`

- Score: `38`
- Kind: `py`
- SHA: `1e76adf6c00e`
- Size: `15790`
- Modified: `2026-06-26 20:04:47`
- Markers: `parking_bot, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\create_clean_live_sandbox.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `\\run_bot_guard_sandbox_v3.py`
- `G:\Programming\Py\OSBB\migrate_cashier_operator_editor.py`
- `G:\Programming\Py\OSBB\migrate_cashier_v2_compat.py`
- `G:\Programming\Py\OSBB\migrate_access_control_and_guard.py`
- `G:\Programming\Py\OSBB\migrate_service_orders_and_fulfillment.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import importlib.util`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import SimpleNamespace`
- `from typing import Any`
- `import config`

Interesting lines:
```text
2: Создание следующей чистой sandbox-копии для живого теста.
5:   Data\db\osbb_test.db
6:   (основная тестовая база проекта, не текущая guard sandbox с квитанциями R2...)
11: - создаёт новую .db внутри Data\db\sandbox;
18:   sandbox-копии;
21: Исходная osbb_test.db, рабочая osbb.db, существующие sandbox-копии и
22: parking_bot.py не меняются.
25: g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\create_clean_live_sandbox.py --guard-user 210312208
43: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
215:             "Автоматическое назначение только в новой clean sandbox.",
227:                 'CREATE_CLEAN_LIVE_SANDBOX',
228:                 'Только для живого теста clean sandbox.', ?, ?)
241:     runner = ROOT / "run_bot_guard_sandbox_v3.py"
242:     launcher = ROOT / "Start_OSBB_Live_Service_Sandbox_Bot.bat"
249: rem Создан автоматически: чистая live sandbox для услуг / пультов.
254: set "RUNNER=%PROJECT%\\run_bot_guard_sandbox_v3.py"
255: set "SANDBOX={target_db}"
271: if not exist "%SANDBOX%" (
272:     echo [ERROR] Не найдена clean sandbox:
273:     echo %SANDBOX%
278: echo Запускаю новую clean sandbox в отдельном окне.
280: start "OSBB Live Service Sandbox" cmd.exe /k ""%PYTHON%" "%RUNNER%" --sandbox "%SANDBOX%" --run"
302:         help="Разрешить создание копии, даже если base osbb_test.db уже содержит workflow-записи.",
306:     base = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
309:         raise SystemExit("ОТКАЗ: OSBB_TEST_DB_FILE указывает на рабочую БД.")
313:     # Base must be the normal test DB, never an existing sandbox.
315:         base.relative_to(SANDBOX_DIR.resolve())
320:             "ОТКАЗ: базой должна быть osbb_test.db, а не старая sandbox-копия."
326:         print("Базовая osbb_test.db уже содержит workflow-записи:")
330:         print("Новая clean sandbox НЕ создана.")
342:         "guard runner": ROOT / "run_bot_guard_sandbox_v3.py",
351:     target = SANDBOX_DIR / f"osbb_test_live_services_{stamp}.db"
352:     report = SANDBOX_DIR / f"clean_live_sandbox_{stamp}.txt"
353:     SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
357:         "CLEAN LIVE SANDBOX CREATION",
360:         f"New sandbox: {target}",
435:             "6. Clean workflow counts in the NEW sandbox:",
441:             "RESULT: READY FOR LIVE SANDBOX TEST",
442:             "Base osbb_test.db and all previous sandbox copies were not modified.",
447:             "RESULT: FAILED — NEW SANDBOX WAS NOT APPROVED FOR TEST",
```

### `create_isolated_live_sandbox_v2.py`

- Score: `38`
- Kind: `py`
- SHA: `0bb5e5ebef65`
- Size: `16061`
- Modified: `2026-06-26 20:12:35`
- Markers: `parking_bot, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\parking_bot.py`
- `G:\Programming\Py\OSBB\create_clean_live_sandbox.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`
- `\\run_bot_guard_sandbox_v3.py`
- `G:\Programming\Py\OSBB\migrate_cashier_operator_editor.py`
- `G:\Programming\Py\OSBB\migrate_cashier_v2_compat.py`
- `G:\Programming\Py\OSBB\migrate_access_control_and_guard.py`
- `G:\Programming\Py\OSBB\migrate_service_orders_and_fulfillment.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import importlib.util`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from types import SimpleNamespace`
- `from typing import Any`
- `import config`

Interesting lines:
```text
2: Создание следующей изолированной sandbox-копии для живого теста.
5:   Data\db\osbb_test.db
6:   (основная тестовая база проекта, не текущая guard sandbox с квитанциями R2...)
9: - сохраняет исторический базовый остаток и существующие операции osbb_test.db
11: - создаёт новую .db внутри Data\db\sandbox;
18:   sandbox-копии;
21: Исходная osbb_test.db, рабочая osbb.db, существующие sandbox-копии и
22: parking_bot.py не меняются.
25: g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\create_clean_live_sandbox.py --guard-user 210312208
43: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
215:             "Автоматическое назначение только в новой clean sandbox.",
227:                 'CREATE_CLEAN_LIVE_SANDBOX',
228:                 'Только для живого теста clean sandbox.', ?, ?)
241:     runner = ROOT / "run_bot_guard_sandbox_v3.py"
242:     launcher = ROOT / "Start_OSBB_Live_Service_Sandbox_Bot.bat"
249: rem Создан автоматически: чистая live sandbox для услуг / пультов.
254: set "RUNNER=%PROJECT%\\run_bot_guard_sandbox_v3.py"
255: set "SANDBOX={target_db}"
271: if not exist "%SANDBOX%" (
272:     echo [ERROR] Не найдена clean sandbox:
273:     echo %SANDBOX%
278: echo Запускаю новую clean sandbox в отдельном окне.
280: start "OSBB Live Service Sandbox" cmd.exe /k ""%PYTHON%" "%RUNNER%" --sandbox "%SANDBOX%" --run"
306:     base = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
309:         raise SystemExit("ОТКАЗ: OSBB_TEST_DB_FILE указывает на рабочую БД.")
313:     # Base must be the normal test DB, never an existing sandbox.
315:         base.relative_to(SANDBOX_DIR.resolve())
320:             "ОТКАЗ: базой должна быть osbb_test.db, а не старая sandbox-копия."
324:     # osbb_test.db — не пустой шаблон, а базовый тестовый контур с
326:     # «мусором» и отбрасывать. Новая sandbox будет изолированной копией
336:         "guard runner": ROOT / "run_bot_guard_sandbox_v3.py",
345:     target = SANDBOX_DIR / f"osbb_test_live_services_{stamp}.db"
346:     report = SANDBOX_DIR / f"clean_live_sandbox_{stamp}.txt"
347:     SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
351:         "ISOLATED LIVE SANDBOX CREATION",
354:         f"New sandbox: {target}",
357:         "Baseline workflow counts inherited from osbb_test.db:",
431:             "6. Clean workflow counts in the NEW sandbox:",
437:             "RESULT: READY FOR ISOLATED LIVE SANDBOX TEST",
439:             "new test operations begin only in this new sandbox.",
440:             "Base osbb_test.db and all previous sandbox copies were not modified.",
445:             "RESULT: FAILED — NEW SANDBOX WAS NOT APPROVED FOR TEST",
```

### `MIGRATE_phone_barrier_access_operational_sandbox.py`

- Score: `38`
- Kind: `py`
- SHA: `488cb403453d`
- Size: `4797`
- Modified: `2026-06-27 19:31:21`
- Markers: `installer, sandbox_db`

References:
- `this script needs the updated phone_barrier_access_core.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
3: Apply the operational two-barrier phone-access tables ONLY to the designated
4: live-services sandbox.
41:         / "sandbox"
42:         / "osbb_test_live_services_2026-06-26_20-13-26.db"
44:     backups = root / "Data" / "db" / "sandbox" / "backups"
58:     print("Mode: SANDBOX ONLY")
62:         raise FileNotFoundError(f"Sandbox database not found:\n{db}")
63:     if db.resolve().parent != (root / "Data" / "db" / "sandbox").resolve():
64:         raise RuntimeError("Safety check failed: target is not the live-services sandbox.")
72:                 "V1 schema has not been applied. Run RUN_MIGRATE_phone_barrier_access_sandbox.bat first."
86:                 "This is not the expected live-services sandbox. Missing: "
113:             actor_id="sandbox_phone_barrier_access_operational_migration",
114:             sandbox_db_path=str(db),
127:         "Mode: SANDBOX ONLY",
```

### `MIGRATE_phone_barrier_access_sandbox.py`

- Score: `38`
- Kind: `py`
- SHA: `81c26d447942`
- Size: `4640`
- Modified: `2026-06-27 19:14:05`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import date, datetime`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
3: Apply the phone-barrier access schema ONLY to the designated live-services
4: sandbox database.
22: SANDBOX_DB = (
26:     / "sandbox"
27:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
29: BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
54:         description="OSBB phone-barrier access schema migration (sandbox only)."
59:         help="Initial sandbox tariff/policy date, YYYY-MM-DD.",
67:     print("Mode: SANDBOX ONLY")
68:     print("Database:", SANDBOX_DB)
71:     if not SANDBOX_DB.is_file():
72:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
74:     expected_parent = (ROOT / "Data" / "db" / "sandbox").resolve()
75:     if SANDBOX_DB.resolve().parent != expected_parent:
76:         raise RuntimeError("Safety check failed: database is not inside the sandbox directory.")
78:     conn = sqlite3.connect(SANDBOX_DB)
88:                 "This is not the expected live-services sandbox. "
102:         f"{SANDBOX_DB.stem}_before_phone_barrier_access_schema_{stamp}{SANDBOX_DB.suffix}"
104:     shutil.copy2(SANDBOX_DB, backup)
107:     conn = sqlite3.connect(SANDBOX_DB)
115:             actor_id="sandbox_phone_barrier_access_migration",
116:             sandbox_db_path=str(SANDBOX_DB),
127:         "Mode: SANDBOX ONLY",
128:         f"Database: {SANDBOX_DB}",
```

### `MIGRATE_profile_verification_sandbox.py`

- Score: `38`
- Kind: `py`
- SHA: `5a90e4cb254d`
- Size: `2576`
- Modified: `2026-06-27 20:48:58`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from profile_verification_core import ensure_profile_verification_schema`

Interesting lines:
```text
2: """Apply resident-profile verification schema ONLY to live-services sandbox."""
12: SANDBOX_DB = ROOT / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
13: BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
22:     print("Mode: SANDBOX ONLY")
23:     print("Database:", SANDBOX_DB)
24:     if not SANDBOX_DB.is_file():
25:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
26:     conn=sqlite3.connect(SANDBOX_DB)
31:             raise RuntimeError("This is not the expected OSBB sandbox. Missing: "+", ".join(sorted(missing)))
36:     backup=BACKUP_DIR/f"{SANDBOX_DB.stem}_before_profile_verification_{stamp}{SANDBOX_DB.suffix}"
37:     shutil.copy2(SANDBOX_DB,backup)
39:     conn=sqlite3.connect(SANDBOX_DB)
42:         changes=ensure_profile_verification_schema(conn,effective_from="2026-06-27",actor_id="sandbox_profile_verification_migration",sandbox_db_path=str(SANDBOX_DB))
50:     log.write_text("\n".join(["OSBB resident profile verification migration","Mode: SANDBOX ONLY",f"Database: {SANDBOX_DB}",f"Backup: {backup}","Changes:",*[f"- {x}" for x in changes],"MIGRATION COMPLETED"])+"\n",encoding="utf-8")
```

### `MIGRATE_simplified_services_sandbox.py`

- Score: `38`
- Kind: `py`
- SHA: `6557cb508eff`
- Size: `4511`
- Modified: `2026-06-27 14:09:06`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\config.py`
- `G:\Programming\Py\OSBB\service_preorders_core.py`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `import config`
- `from service_preorders_core import ensure_simplified_service_schema`

Interesting lines:
```text
3: Apply the simplified paid-preorder workflow only to the dedicated live-services
4: sandbox database. It does not touch osbb.db or other sandbox files.
24: SANDBOX = (
28:     / "sandbox"
29:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
31: BACKUPS = ROOT / "Data" / "db" / "sandbox" / "backups"
88:     print("Sandbox:", SANDBOX)
90:     if not SANDBOX.is_file():
92:             "Live-services sandbox DB was not found:\n"
93:             f"  {SANDBOX}"
103:         f"{SANDBOX.stem}_before_simplified_services_{stamp}{SANDBOX.suffix}"
105:     shutil.copy2(SANDBOX, backup)
108:     conn = sqlite3.connect(SANDBOX)
123:         "Simplified services sandbox migration",
125:         f"Sandbox: {SANDBOX}",
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_phone_barrier_access_operational_sandbox\MIGRATE_phone_barrier_access_operational_sandbox__488cb403453d.py`

- Score: `38`
- Kind: `py`
- SHA: `488cb403453d`
- Size: `4797`
- Modified: `2026-07-02 22:59:37`
- Markers: `installer, sandbox_db`

References:
- `this script needs the updated phone_barrier_access_core.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
3: Apply the operational two-barrier phone-access tables ONLY to the designated
4: live-services sandbox.
41:         / "sandbox"
42:         / "osbb_test_live_services_2026-06-26_20-13-26.db"
44:     backups = root / "Data" / "db" / "sandbox" / "backups"
58:     print("Mode: SANDBOX ONLY")
62:         raise FileNotFoundError(f"Sandbox database not found:\n{db}")
63:     if db.resolve().parent != (root / "Data" / "db" / "sandbox").resolve():
64:         raise RuntimeError("Safety check failed: target is not the live-services sandbox.")
72:                 "V1 schema has not been applied. Run RUN_MIGRATE_phone_barrier_access_sandbox.bat first."
86:                 "This is not the expected live-services sandbox. Missing: "
113:             actor_id="sandbox_phone_barrier_access_operational_migration",
114:             sandbox_db_path=str(db),
127:         "Mode: SANDBOX ONLY",
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_phone_barrier_access_sandbox\MIGRATE_phone_barrier_access_sandbox__81c26d447942.py`

- Score: `38`
- Kind: `py`
- SHA: `81c26d447942`
- Size: `4640`
- Modified: `2026-07-02 22:59:38`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import date, datetime`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
3: Apply the phone-barrier access schema ONLY to the designated live-services
4: sandbox database.
22: SANDBOX_DB = (
26:     / "sandbox"
27:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
29: BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
54:         description="OSBB phone-barrier access schema migration (sandbox only)."
59:         help="Initial sandbox tariff/policy date, YYYY-MM-DD.",
67:     print("Mode: SANDBOX ONLY")
68:     print("Database:", SANDBOX_DB)
71:     if not SANDBOX_DB.is_file():
72:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
74:     expected_parent = (ROOT / "Data" / "db" / "sandbox").resolve()
75:     if SANDBOX_DB.resolve().parent != expected_parent:
76:         raise RuntimeError("Safety check failed: database is not inside the sandbox directory.")
78:     conn = sqlite3.connect(SANDBOX_DB)
88:                 "This is not the expected live-services sandbox. "
102:         f"{SANDBOX_DB.stem}_before_phone_barrier_access_schema_{stamp}{SANDBOX_DB.suffix}"
104:     shutil.copy2(SANDBOX_DB, backup)
107:     conn = sqlite3.connect(SANDBOX_DB)
115:             actor_id="sandbox_phone_barrier_access_migration",
116:             sandbox_db_path=str(SANDBOX_DB),
127:         "Mode: SANDBOX ONLY",
128:         f"Database: {SANDBOX_DB}",
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_profile_verification_sandbox\MIGRATE_profile_verification_sandbox__5a90e4cb254d.py`

- Score: `38`
- Kind: `py`
- SHA: `5a90e4cb254d`
- Size: `2576`
- Modified: `2026-07-02 22:59:36`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from profile_verification_core import ensure_profile_verification_schema`

Interesting lines:
```text
2: """Apply resident-profile verification schema ONLY to live-services sandbox."""
12: SANDBOX_DB = ROOT / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
13: BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
22:     print("Mode: SANDBOX ONLY")
23:     print("Database:", SANDBOX_DB)
24:     if not SANDBOX_DB.is_file():
25:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
26:     conn=sqlite3.connect(SANDBOX_DB)
31:             raise RuntimeError("This is not the expected OSBB sandbox. Missing: "+", ".join(sorted(missing)))
36:     backup=BACKUP_DIR/f"{SANDBOX_DB.stem}_before_profile_verification_{stamp}{SANDBOX_DB.suffix}"
37:     shutil.copy2(SANDBOX_DB,backup)
39:     conn=sqlite3.connect(SANDBOX_DB)
42:         changes=ensure_profile_verification_schema(conn,effective_from="2026-06-27",actor_id="sandbox_profile_verification_migration",sandbox_db_path=str(SANDBOX_DB))
50:     log.write_text("\n".join(["OSBB resident profile verification migration","Mode: SANDBOX ONLY",f"Database: {SANDBOX_DB}",f"Backup: {backup}","Changes:",*[f"- {x}" for x in changes],"MIGRATION COMPLETED"])+"\n",encoding="utf-8")
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_simplified_services_sandbox\MIGRATE_simplified_services_sandbox__cb84fbcee38c.py`

- Score: `38`
- Kind: `py`
- SHA: `cb84fbcee38c`
- Size: `2221`
- Modified: `2026-07-02 22:59:39`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `from pathlib import Path`
- `from service_preorders_core import ensure_simplified_service_schema`

Interesting lines:
```text
3: Apply the simplified paid-preorder workflow only to the dedicated live-services
4: sandbox database. It does not touch osbb.db or other sandbox files.
19: SANDBOX = ROOT / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
20: BACKUPS = ROOT / "Data" / "db" / "sandbox" / "backups"
26:     print("Sandbox:", SANDBOX)
27:     if not SANDBOX.is_file():
28:         raise FileNotFoundError("Live-services sandbox DB was not found.")
31:     backup = BACKUPS / f"{SANDBOX.stem}_before_simplified_services_{stamp}{SANDBOX.suffix}"
32:     shutil.copy2(SANDBOX, backup)
38:     conn = sqlite3.connect(SANDBOX)
51:         "Simplified services sandbox migration\n"
52:         f"Sandbox: {SANDBOX}\n"
```

### `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_schema_migration\MIGRATE_phone_barrier_access_sandbox.py`

- Score: `38`
- Kind: `py`
- SHA: `81c26d447942`
- Size: `4640`
- Modified: `2026-07-02 22:59:38`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import date, datetime`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
3: Apply the phone-barrier access schema ONLY to the designated live-services
4: sandbox database.
22: SANDBOX_DB = (
26:     / "sandbox"
27:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
29: BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
54:         description="OSBB phone-barrier access schema migration (sandbox only)."
59:         help="Initial sandbox tariff/policy date, YYYY-MM-DD.",
67:     print("Mode: SANDBOX ONLY")
68:     print("Database:", SANDBOX_DB)
71:     if not SANDBOX_DB.is_file():
72:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
74:     expected_parent = (ROOT / "Data" / "db" / "sandbox").resolve()
75:     if SANDBOX_DB.resolve().parent != expected_parent:
76:         raise RuntimeError("Safety check failed: database is not inside the sandbox directory.")
78:     conn = sqlite3.connect(SANDBOX_DB)
88:                 "This is not the expected live-services sandbox. "
102:         f"{SANDBOX_DB.stem}_before_phone_barrier_access_schema_{stamp}{SANDBOX_DB.suffix}"
104:     shutil.copy2(SANDBOX_DB, backup)
107:     conn = sqlite3.connect(SANDBOX_DB)
115:             actor_id="sandbox_phone_barrier_access_migration",
116:             sandbox_db_path=str(SANDBOX_DB),
127:         "Mode: SANDBOX ONLY",
128:         f"Database: {SANDBOX_DB}",
```

### `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_v2_working_sandbox\MIGRATE_phone_barrier_access_operational_sandbox.py`

- Score: `38`
- Kind: `py`
- SHA: `488cb403453d`
- Size: `4797`
- Modified: `2026-07-02 22:59:37`
- Markers: `installer, sandbox_db`

References:
- `this script needs the updated phone_barrier_access_core.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
3: Apply the operational two-barrier phone-access tables ONLY to the designated
4: live-services sandbox.
41:         / "sandbox"
42:         / "osbb_test_live_services_2026-06-26_20-13-26.db"
44:     backups = root / "Data" / "db" / "sandbox" / "backups"
58:     print("Mode: SANDBOX ONLY")
62:         raise FileNotFoundError(f"Sandbox database not found:\n{db}")
63:     if db.resolve().parent != (root / "Data" / "db" / "sandbox").resolve():
64:         raise RuntimeError("Safety check failed: target is not the live-services sandbox.")
72:                 "V1 schema has not been applied. Run RUN_MIGRATE_phone_barrier_access_sandbox.bat first."
86:                 "This is not the expected live-services sandbox. Missing: "
113:             actor_id="sandbox_phone_barrier_access_operational_migration",
114:             sandbox_db_path=str(db),
127:         "Mode: SANDBOX ONLY",
```

### `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\MIGRATE_profile_verification_sandbox.py`

- Score: `38`
- Kind: `py`
- SHA: `5a90e4cb254d`
- Size: `2576`
- Modified: `2026-07-02 22:59:36`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from profile_verification_core import ensure_profile_verification_schema`

Interesting lines:
```text
2: """Apply resident-profile verification schema ONLY to live-services sandbox."""
12: SANDBOX_DB = ROOT / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
13: BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
22:     print("Mode: SANDBOX ONLY")
23:     print("Database:", SANDBOX_DB)
24:     if not SANDBOX_DB.is_file():
25:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
26:     conn=sqlite3.connect(SANDBOX_DB)
31:             raise RuntimeError("This is not the expected OSBB sandbox. Missing: "+", ".join(sorted(missing)))
36:     backup=BACKUP_DIR/f"{SANDBOX_DB.stem}_before_profile_verification_{stamp}{SANDBOX_DB.suffix}"
37:     shutil.copy2(SANDBOX_DB,backup)
39:     conn=sqlite3.connect(SANDBOX_DB)
42:         changes=ensure_profile_verification_schema(conn,effective_from="2026-06-27",actor_id="sandbox_profile_verification_migration",sandbox_db_path=str(SANDBOX_DB))
50:     log.write_text("\n".join(["OSBB resident profile verification migration","Mode: SANDBOX ONLY",f"Database: {SANDBOX_DB}",f"Backup: {backup}","Changes:",*[f"- {x}" for x in changes],"MIGRATION COMPLETED"])+"\n",encoding="utf-8")
```

### `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\profile_verification_payload\profile_verification_core.py`

- Score: `38`
- Kind: `py`
- SHA: `68b9c00f27e8`
- Size: `48300`
- Modified: `2026-07-02 22:59:37`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import hashlib`
- `import json`
- `import sqlite3`
- `from datetime import datetime`
- `from typing import Any`

Interesting lines:
```text
27: The module is additive and sandbox-safe. It creates profile-specific tables;
274:             sandbox_db_path TEXT,
500:         VALUES (?, ?, 'ACTIVE', ?, 'SANDBOX_INITIAL_SEED',
501:                 'Initial resident profile verification policy for sandbox.',
553:     sandbox_db_path: str = "",
648:                 sandbox_db_path, note
656:                 text(sandbox_db_path),
1406: def _apply_parking_time(
1460:         _apply_parking_time(
```

### `Recovered_Releases\2026-06-27__OSBB_simplified_services_preorders_bundle\MIGRATE_simplified_services_sandbox.py`

- Score: `38`
- Kind: `py`
- SHA: `cb84fbcee38c`
- Size: `2221`
- Modified: `2026-07-02 22:59:39`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `from pathlib import Path`
- `from service_preorders_core import ensure_simplified_service_schema`

Interesting lines:
```text
3: Apply the simplified paid-preorder workflow only to the dedicated live-services
4: sandbox database. It does not touch osbb.db or other sandbox files.
19: SANDBOX = ROOT / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
20: BACKUPS = ROOT / "Data" / "db" / "sandbox" / "backups"
26:     print("Sandbox:", SANDBOX)
27:     if not SANDBOX.is_file():
28:         raise FileNotFoundError("Live-services sandbox DB was not found.")
31:     backup = BACKUPS / f"{SANDBOX.stem}_before_simplified_services_{stamp}{SANDBOX.suffix}"
32:     shutil.copy2(SANDBOX, backup)
38:     conn = sqlite3.connect(SANDBOX)
51:         "Simplified services sandbox migration\n"
52:         f"Sandbox: {SANDBOX}\n"
```

### `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\parking_time_test_payload\profile_parking_time_test_core.py`

- Score: `38`
- Kind: `py`
- SHA: `45ab47b5a24a`
- Size: `25134`
- Modified: `2026-07-02 22:59:36`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import json`
- `import sqlite3`
- `from datetime import datetime`
- `from typing import Any`

Interesting lines:
```text
120:             sandbox_db_path TEXT,
251:     sandbox_db_path: str = "",
279:                 sandbox_db_path, note
287:                 text(sandbox_db_path),
730:     Approve/reject a TEST outcome without applying any real correction.
```

### `tools\promote_sandbox_to_training_db.py`

- Score: `38`
- Kind: `py`
- SHA: `82dec2cafaa3`
- Size: `6215`
- Modified: `2026-07-01 12:30:15`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\tools\promote_sandbox_to_training_db.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `import sqlite3`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
4: promote_sandbox_to_training_db.py
6: Promote selected strongest sandbox DB to working training DB: osbb_test.db.
10:   - --apply required to copy
11:   - creates timestamped backup of current osbb_test.db
17:   G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_live_services_2026-06-26_20-13-26.db
20:   G:\Programming\Py\OSBB\Data\db\osbb_test.db
32: DEFAULT_SOURCE = r"G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_live_services_2026-06-26_20-13-26.db"
33: DEFAULT_TARGET = r"G:\Programming\Py\OSBB\Data\db\osbb_test.db"
34: DEFAULT_REPORT = r"G:\Programming\Py\OSBB\Data\exports\db_rank\PROMOTE_SANDBOX_TO_TRAINING_DB.md"
107:     dst = backup_dir / f"{target.stem}_before_promote_live_services_{datetime.now():%Y-%m-%d_%H-%M-%S}{target.suffix}"
149:     ap.add_argument("--apply", action="store_true")
157:     print("OSBB promote sandbox to training DB")
159:     print("Mode:", "APPLY" if args.apply else "DRY RUN")
185:     if not args.apply:
188:         print("DRY RUN COMPLETED. Re-run with --apply to promote.")
204:     write_report(report, source, target, backup, "APPLY")
207:     print("APPLY COMPLETED")
208:     print("New osbb_test.db:", target)
```

### `tools\sandbox_switch_admin_apartment.py`

- Score: `38`
- Kind: `py`
- SHA: `da4c2bff61a0`
- Size: `11668`
- Modified: `2026-06-29 22:06:34`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\tools\sandbox_switch_admin_apartment.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import shutil`
- `import sqlite3`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any`

Interesting lines:
```text
4: sandbox_switch_admin_apartment.py
6: OSBB sandbox helper: temporarily switch the current sandbox admin/resident profile
12:   - writes only with --apply
13:   - creates DB backup before APPLY
14:   - intended for sandbox DB only
266:     ap.add_argument("--apply", action="store_true", help="Apply switch.")
274:     print("OSBB sandbox switch admin apartment")
276:     print("Mode:", "APPLY" if args.apply else "DRY RUN / READ ONLY")
281:     conn = connect(db_path, readonly=not args.apply)
299:         if not args.apply:
304:             print("DRY RUN COMPLETED. Re-run with --apply to switch.")
326:         print("APPLY COMPLETED")
330:         if args.apply:
```

### `tools\stop_live_services_bot.py`

- Score: `38`
- Kind: `py`
- SHA: `aabb1a7d11bb`
- Size: `2403`
- Modified: `2026-06-28 19:19:58`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\tools\stop_live_services_bot.py`
- `G:\Programming\Py\OSBB\run_bot_live_services_sandbox_v1.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import json`
- `import subprocess`

Interesting lines:
```text
4: stop_live_services_bot.py
6: Safely stops ONLY OSBB Live Services Sandbox bot processes:
7:   run_bot_live_services_sandbox_v1.py
10: Use --apply to stop them.
13:   python .\OSBB\tools\stop_live_services_bot.py
14:   python .\OSBB\tools\stop_live_services_bot.py --apply
24: TARGET = "run_bot_live_services_sandbox_v1.py"
59:     ap.add_argument("--apply", action="store_true", help="Actually stop matching bot processes.")
65:     print("Mode:", "APPLY" if args.apply else "DRY RUN")
81:     if not args.apply:
84:         print("python .\\OSBB\\tools\\stop_live_services_bot.py --apply")
```

### `RUN_CHECK_guard_sandbox_service_orders.bat`

- Score: `33`
- Kind: `bat`
- SHA: `e67e852d1396`
- Size: `951`
- Modified: `2026-06-27 11:44:42`
- Markers: `sandbox_db`

References:
- `G:\Programming\Py\OSBB\CHECK_guard_sandbox_service_orders.py`
- `echo Put this BAT and CHECK_guard_sandbox_service_orders.py`

Interesting lines:
```text
4: title OSBB - Guard Sandbox Service Orders Diagnosis
8: set "SCRIPT=%PROJECT%\CHECK_guard_sandbox_service_orders.py"
11: echo OSBB Guard Sandbox - Service Orders Diagnosis
27:     echo Put this BAT and CHECK_guard_sandbox_service_orders.py
```

### `RUN_CHECK_guard_sandbox_service_orders_v2.bat`

- Score: `33`
- Kind: `bat`
- SHA: `f79c84809c86`
- Size: `809`
- Modified: `2026-06-27 11:50:26`
- Markers: `sandbox_db`

References:
- `G:\Programming\Py\OSBB\CHECK_guard_sandbox_service_orders_v2.py`

Interesting lines:
```text
4: title OSBB - Guard Sandbox Diagnosis V2
8: set "SCRIPT=%PROJECT%\CHECK_guard_sandbox_service_orders_v2.py"
11: echo OSBB Guard Sandbox - Service Orders Diagnosis V2
```

### `RUN_CHECK_phone_barrier_access_operational_sandbox.bat`

- Score: `33`
- Kind: `bat`
- SHA: `9d5054423fec`
- Size: `294`
- Modified: `2026-06-27 19:31:23`
- Markers: `sandbox_db`

References:
- `\CHECK_phone_barrier_access_operational_sandbox.py`

Interesting lines:
```text
9: "%PY%" "%ROOT%\CHECK_phone_barrier_access_operational_sandbox.py"
```

### `RUN_CHECK_phone_barrier_access_sandbox_schema.bat`

- Score: `33`
- Kind: `bat`
- SHA: `caffbf887830`
- Size: `315`
- Modified: `2026-06-27 19:14:06`
- Markers: `sandbox_db`

References:
- `\CHECK_phone_barrier_access_sandbox_schema.py`

Interesting lines:
```text
7: echo OSBB phone-barrier access sandbox schema check
11: "%PY%" "%ROOT%\CHECK_phone_barrier_access_sandbox_schema.py"
```

### `RUN_CHECK_profile_parking_time_test_sandbox.bat`

- Score: `33`
- Kind: `bat`
- SHA: `eef720ccc049`
- Size: `267`
- Modified: `2026-06-28 12:11:30`
- Markers: `sandbox_db`

References:
- `\CHECK_profile_parking_time_test_sandbox.py`

Interesting lines:
```text
8: "%PY%" "%ROOT%\CHECK_profile_parking_time_test_sandbox.py"
```

### `RUN_CHECK_profile_verification_sandbox.bat`

- Score: `33`
- Kind: `bat`
- SHA: `c39c95fad8be`
- Size: `309`
- Modified: `2026-06-27 20:48:59`
- Markers: `sandbox_db`

References:
- `\CHECK_profile_verification_sandbox.py`

Interesting lines:
```text
5: echo OSBB resident profile verification V1 - sandbox check
8: "%PY%" "%ROOT%\CHECK_profile_verification_sandbox.py"
```

### `RUN_FIX_live_services_sandbox_payment_schema.bat`

- Score: `33`
- Kind: `bat`
- SHA: `8ef742cf5cf6`
- Size: `1101`
- Modified: `2026-06-27 12:24:42`
- Markers: `sandbox_db`

References:
- `G:\Programming\Py\OSBB\FIX_live_services_sandbox_payment_schema.py`
- `echo Put this BAT and FIX_live_services_sandbox_payment_schema.py`
- `echo 1. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

Interesting lines:
```text
4: title OSBB - Live Services Sandbox Payment Schema Fix
8: set "SCRIPT=%PROJECT%\FIX_live_services_sandbox_payment_schema.py"
11: echo OSBB LIVE SERVICES SANDBOX - PAYMENT SCHEMA FIX
14: echo 1. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat first with Ctrl+C.
15: echo 2. This repair changes only the live-services SANDBOX database.
29:     echo Put this BAT and FIX_live_services_sandbox_payment_schema.py
```

### `RUN_MIGRATE_phone_barrier_access_operational_sandbox.bat`

- Score: `33`
- Kind: `bat`
- SHA: `f021bfaf5110`
- Size: `353`
- Modified: `2026-06-27 19:31:22`
- Markers: `sandbox_db`

References:
- `\MIGRATE_phone_barrier_access_operational_sandbox.py`
- `echo SANDBOX ONLY. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

Interesting lines:
```text
7: echo SANDBOX ONLY. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat first.
9: "%PY%" "%ROOT%\MIGRATE_phone_barrier_access_operational_sandbox.py"
```

### `RUN_MIGRATE_phone_barrier_access_sandbox.bat`

- Score: `33`
- Kind: `bat`
- SHA: `641853fd8857`
- Size: `411`
- Modified: `2026-06-27 19:14:06`
- Markers: `sandbox_db`

References:
- `\MIGRATE_phone_barrier_access_sandbox.py`
- `echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

Interesting lines:
```text
8: echo This changes ONLY the live-services sandbox and creates a backup.
9: echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat before running this file.
12: "%PY%" "%ROOT%\MIGRATE_phone_barrier_access_sandbox.py"
```

### `RUN_MIGRATE_profile_parking_time_test_sandbox.bat`

- Score: `33`
- Kind: `bat`
- SHA: `81b1355766b8`
- Size: `321`
- Modified: `2026-06-28 12:11:30`
- Markers: `sandbox_db`

References:
- `\MIGRATE_profile_parking_time_test_sandbox.py`

Interesting lines:
```text
6: echo OSBB isolated parking_time TEST V1 - sandbox migration
9: "%PY%" "%ROOT%\MIGRATE_profile_parking_time_test_sandbox.py"
```

### `RUN_MIGRATE_profile_verification_sandbox.bat`

- Score: `33`
- Kind: `bat`
- SHA: `dbbf2c0ece24`
- Size: `348`
- Modified: `2026-06-27 20:48:59`
- Markers: `sandbox_db`

References:
- `\MIGRATE_profile_verification_sandbox.py`

Interesting lines:
```text
5: echo OSBB resident profile verification V1 - sandbox migration
6: echo This changes ONLY the live-services sandbox database and creates a backup.
8: "%PY%" "%ROOT%\MIGRATE_profile_verification_sandbox.py"
```

### `RUN_MIGRATE_simplified_services_sandbox.bat`

- Score: `33`
- Kind: `bat`
- SHA: `4cb3f9a902de`
- Size: `803`
- Modified: `2026-06-27 13:29:00`
- Markers: `sandbox_db`

References:
- `\MIGRATE_simplified_services_sandbox.py`

Interesting lines:
```text
4: title OSBB - Simplified Services Sandbox Migration
8: set "SCRIPT=%PROJECT%\MIGRATE_simplified_services_sandbox.py"
13: echo This changes ONLY the live-services sandbox and creates a backup.
14: echo Stop the live-services sandbox bot before running this file.
```

### `RUN_RETIRE_legacy_new_remote_test_orders_sandbox.bat`

- Score: `33`
- Kind: `bat`
- SHA: `55c44a814cc2`
- Size: `469`
- Modified: `2026-06-27 13:29:01`
- Markers: `sandbox_db`

References:
- `\RETIRE_legacy_new_remote_test_orders_sandbox.py`

Interesting lines:
```text
4: title OSBB - Retire Legacy New Remote Sandbox Tests
7: set "SCRIPT=%PROJECT%\RETIRE_legacy_new_remote_test_orders_sandbox.py"
9: echo Retires only unpaid old TEST new-remote sandbox orders.
11: echo Stop the live-services sandbox bot first.
```

### `Start_OSBB_Guard_Sandbox_Bot_v2.bat`

- Score: `33`
- Kind: `bat`
- SHA: `fdfc05def4bb`
- Size: `1276`
- Modified: `2026-06-26 17:28:19`
- Markers: `sandbox_db`

References:
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`

Interesting lines:
```text
5: rem OSBB — guard sandbox-бот в отдельном окне
12: set "RUNNER=%PROJECT%\run_bot_guard_sandbox_v3.py"
13: set "SANDBOX=%PROJECT%\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09.db"
29: if not exist "%SANDBOX%" (
30:     echo [ERROR] Не найдена guard sandbox-БД:
31:     echo %SANDBOX%
36: echo Запускаю OSBB Guard Sandbox Bot в отдельном окне.
38: start "OSBB Guard Sandbox Bot" cmd.exe /k ""%PYTHON%" "%RUNNER%" --sandbox "%SANDBOX%" --run"
```

### `Start_OSBB_Live_Service_Sandbox_Bot.bat`

- Score: `33`
- Kind: `bat`
- SHA: `c968b5c43bcf`
- Size: `1176`
- Modified: `2026-06-26 20:50:39`
- Markers: `sandbox_db`

References:
- `\run_bot_live_service_sandbox_v4.py`

Interesting lines:
```text
4: rem Создан автоматически: чистая live sandbox для услуг / пультов.
9: set "RUNNER=%PROJECT%\run_bot_live_service_sandbox_v4.py"
10: set "SANDBOX=G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_live_services_2026-06-26_20-13-26.db"
26: if not exist "%SANDBOX%" (
27:     echo [ERROR] Не найдена clean sandbox:
28:     echo %SANDBOX%
33: echo Запускаю новую clean sandbox в отдельном окне.
35: start "OSBB Live Service Sandbox" cmd.exe /k ""%PYTHON%" "%RUNNER%" --sandbox "%SANDBOX%" --run"
```

### `Start_OSBB_Live_Services_Sandbox_Bot_v1.bat`

- Score: `33`
- Kind: `bat`
- SHA: `9723d9d7c961`
- Size: `981`
- Modified: `2026-06-27 12:15:02`
- Markers: `sandbox_db`

References:
- `\run_bot_live_services_sandbox_v1.py`
- `echo Use STOP_old_guard_sandbox_bots.bat`

Interesting lines:
```text
4: title OSBB - Live Services Sandbox
8: set "SCRIPT=%PROJECT%\run_bot_live_services_sandbox_v1.py"
11: echo OSBB LIVE SERVICES SANDBOX
12: echo Database: osbb_test_live_services_2026-06-26_20-13-26.db
39:     echo Old Guard Sandbox bot windows are still running.
40:     echo Use STOP_old_guard_sandbox_bots.bat from this bundle, then start again.
```

### `STOP_old_guard_sandbox_bots.bat`

- Score: `33`
- Kind: `bat`
- SHA: `fd7887cdb161`
- Size: `727`
- Modified: `2026-06-27 12:15:02`
- Markers: `sandbox_db`

References:
- `echo run_bot_guard_sandbox_v3.py`
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`

Interesting lines:
```text
4: title OSBB - Stop Old Guard Sandbox Bots
8: echo run_bot_guard_sandbox_v3.py --run
12:   "$p = Get-CimInstance Win32_Process | Where-Object { ($_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe') -and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' }; if (-not $p) { Write-Host 'No old Guard Sandbox bot process was found.'; exit 0 }; $p | ForEach-Object { Write-Host ('Stopping PID ' + $_.ProcessId); Invoke-CimMethod -InputObject $_ -MethodName Terminate | Out-Null }; Write-Host 'Done.'"
```

### `Bots\handlers\cashier_operator.py`

- Score: `30`
- Kind: `py`
- SHA: `5b73b4c3a060`
- Size: `92137`
- Modified: `2026-06-25 14:39:13`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\migrate_cashier_operator_editor.py`

Imports:
- `from handlers.cashier_operator import handle_cashier_operator_text`
- `from __future__ import annotations`
- `from datetime import date, datetime`
- `from pathlib import Path`
- `import re`
- `import sqlite3`
- `import sys`
- `from typing import Any`
- `from uuid import uuid4`
- `from telegram import ReplyKeyboardMarkup, Update`
- `from config import paths, USE_TEST_DB`
- `from audit_logger import audit_log`
- `from unit_resolver import resolve_unit_ref`
- `from db_access import get_admin_record  # type: ignore`

Interesting lines:
```text
17:   migrate_cashier_operator_editor.py --apply
178:     return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
```

### `migrate_cashier_operator_editor.py`

- Score: `30`
- Kind: `py`
- SHA: `f9066052061a`
- Size: `19620`
- Modified: `2026-06-25 14:38:58`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\migrate_cashier_operator_editor.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `from pathlib import Path`
- `from config import paths, USE_TEST_DB`
- `from audit_logger import audit_log`

Interesting lines:
```text
113:     return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
371:     parser.add_argument("--apply", action="store_true")
473:         f"Apply: {args.apply}",
506:     if args.apply:
547:     print("Apply:", args.apply)
553:     print("APPLIED" if args.apply else "DRY RUN COMPLETED - NO CHANGES SAVED")
```

### `migrate_cashier_v2_compat.py`

- Score: `30`
- Kind: `py`
- SHA: `a3a2daac0227`
- Size: `24064`
- Modified: `2026-06-25 19:44:05`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\cashier_v2_preflight.py`
- `G:\Programming\Py\OSBB\migrate_cashier_v2.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any`
- `from config import paths, USE_TEST_DB`
- `from audit_logger import audit_log`

Interesting lines:
```text
10: - делает это только при --apply.
18: проверочным сценарием cashier_v2_preflight.py на sandbox-копии БД.
48:     return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
546:     sandbox-копии; CLI --apply — для активной базы.
593:     parser.add_argument("--apply", action="store_true")
614:         f"Apply: {args.apply}",
618:     if not args.apply:
```

### `migrate_cashier_v2.py`

- Score: `30`
- Kind: `py`
- SHA: `f46266059d0a`
- Size: `18071`
- Modified: `2026-06-25 17:39:59`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\migrate_cashier_v2.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `from pathlib import Path`
- `from config import paths, USE_TEST_DB`
- `from audit_logger import audit_log`

Interesting lines:
```text
47:     return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
385:     parser.add_argument("--apply", action="store_true")
433:         f"Apply: {args.apply}",
458:     if args.apply:
499:     print("Apply:", args.apply)
508:     print("APPLIED" if args.apply else "DRY RUN COMPLETED - NO CHANGES SAVED")
```

### `migrate_access_control_and_guard.py`

- Score: `30`
- Kind: `py`
- SHA: `2fb3c0073893`
- Size: `20953`
- Modified: `2026-06-26 12:32:09`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\manage_staff_access.py`
- `G:\Programming\Py\OSBB\migrate_access_control_and_guard.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any`
- `from config import paths, USE_TEST_DB`
- `from audit_logger import audit_log`

Interesting lines:
```text
49:     return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
480:     parser.add_argument("--apply", action="store_true")
501:             f"Apply: {args.apply}",
522:         if args.apply:
```

### `manage_staff_access.py`

- Score: `30`
- Kind: `py`
- SHA: `78723771b5d1`
- Size: `15382`
- Modified: `2026-06-26 12:32:58`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\migrate_access_control_and_guard.py`
- `G:\Programming\Py\OSBB\manage_staff_access.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any`
- `from config import paths, USE_TEST_DB`
- `from access_control import (`
- `from audit_logger import audit_log`

Interesting lines:
```text
5: По умолчанию ничего не меняет. Для записи добавьте --apply.
25: 4. После проверки выполнить именно такую же команду с --apply.
28: ... --grant 123456789 remote_handover_events CREATE --scope POST:O --apply
31: ... --deny 123456789 payment_notices CONFIRM --scope CASHBOX:O --apply
44: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
329:         "--sandbox",
330:         help="Необязательно: .db внутри Data\\db\\sandbox для безопасной проверки.",
339:     parser.add_argument("--apply", action="store_true")
342:     if args.sandbox:
343:         db = Path(args.sandbox).resolve()
345:             db.relative_to(SANDBOX_DIR.resolve())
347:             raise SystemExit("Для --sandbox разрешены только БД внутри Data\\db\\sandbox.")
434:         if args.apply:
```

### `migrate_service_orders_and_fulfillment.py`

- Score: `30`
- Kind: `py`
- SHA: `33ef6dda81b9`
- Size: `30195`
- Modified: `2026-06-26 19:39:26`
- Markers: `installer, sandbox_db`

References:
- `G:\Programming\Py\OSBB\migrate_service_orders_and_fulfillment.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any`
- `from config import paths, USE_TEST_DB`
- `from audit_logger import audit_log`

Interesting lines:
```text
24: Применение после sandbox-проверки:
25: g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\migrate_service_orders_and_fulfillment.py --apply
55:     return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
677:     parser.add_argument("--apply", action="store_true")
703:             f"Apply: {args.apply}",
733:         if args.apply:
```

### `profile_verification_core.py`

- Score: `30`
- Kind: `py`
- SHA: `d06fa33f0c95`
- Size: `49558`
- Modified: `2026-06-27 21:22:51`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import hashlib`
- `import json`
- `import sqlite3`
- `from datetime import datetime`
- `from typing import Any`

Interesting lines:
```text
27: The module is additive and sandbox-safe. It creates profile-specific tables;
274:             sandbox_db_path TEXT,
500:         VALUES (?, ?, 'ACTIVE', ?, 'SANDBOX_INITIAL_SEED',
501:                 'Initial resident profile verification policy for sandbox.',
553:     sandbox_db_path: str = "",
648:                 sandbox_db_path, note
656:                 text(sandbox_db_path),
1426: def _apply_parking_time(
1480:         _apply_parking_time(
```

### `parking_time_test_payload\profile_parking_time_test_core.py`

- Score: `30`
- Kind: `py`
- SHA: `45ab47b5a24a`
- Size: `25134`
- Modified: `2026-06-28 12:11:31`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import json`
- `import sqlite3`
- `from datetime import datetime`
- `from typing import Any`

Interesting lines:
```text
120:             sandbox_db_path TEXT,
251:     sandbox_db_path: str = "",
279:                 sandbox_db_path, note
287:                 text(sandbox_db_path),
730:     Approve/reject a TEST outcome without applying any real correction.
```

### `profile_verification_payload\profile_verification_core.py`

- Score: `30`
- Kind: `py`
- SHA: `68b9c00f27e8`
- Size: `48300`
- Modified: `2026-06-27 20:49:00`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import hashlib`
- `import json`
- `import sqlite3`
- `from datetime import datetime`
- `from typing import Any`

Interesting lines:
```text
27: The module is additive and sandbox-safe. It creates profile-specific tables;
274:             sandbox_db_path TEXT,
500:         VALUES (?, ?, 'ACTIVE', ?, 'SANDBOX_INITIAL_SEED',
501:                 'Initial resident profile verification policy for sandbox.',
553:     sandbox_db_path: str = "",
648:                 sandbox_db_path, note
656:                 text(sandbox_db_path),
1406: def _apply_parking_time(
1460:         _apply_parking_time(
```

### `profile_parking_time_test_core.py`

- Score: `30`
- Kind: `py`
- SHA: `45ab47b5a24a`
- Size: `25134`
- Modified: `2026-06-28 12:11:31`
- Markers: `installer, sandbox_db`

Imports:
- `from __future__ import annotations`
- `import json`
- `import sqlite3`
- `from datetime import datetime`
- `from typing import Any`

Interesting lines:
```text
120:             sandbox_db_path TEXT,
251:     sandbox_db_path: str = "",
279:                 sandbox_db_path, note
287:                 text(sandbox_db_path),
730:     Approve/reject a TEST outcome without applying any real correction.
```

### `fix_source_ref_schema.py`

- Score: `30`
- Kind: `py`
- SHA: `0b7c94b2f975`
- Size: `10500`
- Modified: `2026-06-27 10:40:17`
- Markers: `service_orders_workspace`

References:
- `1. Reads Bots\handlers\service_orders_workspace.py`
- `service_orders_workspace.py`

Imports:
- `from __future__ import annotations`
- `import re`
- `import shutil`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Iterable`

Interesting lines:
```text
6:   1. Reads Bots\handlers\service_orders_workspace.py.
30: HANDLER_PATH = PROJECT_ROOT / "Bots" / "handlers" / "service_orders_workspace.py"
```

### `Start_OSBB_Live_Service_Sandbox_Bot_before_service_ui_2026-06-26_20-50-39.bat`

- Score: `30`
- Kind: `bat`
- SHA: `426128b5c4f0`
- Size: `1169`
- Modified: `2026-06-26 20:13:28`
- Markers: `sandbox_db`

References:
- `G:\Programming\Py\OSBB\run_bot_guard_sandbox_v3.py`

Interesting lines:
```text
4: rem Создан автоматически: чистая live sandbox для услуг / пультов.
9: set "RUNNER=%PROJECT%\run_bot_guard_sandbox_v3.py"
10: set "SANDBOX=G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_live_services_2026-06-26_20-13-26.db"
26: if not exist "%SANDBOX%" (
27:     echo [ERROR] Не найдена clean sandbox:
28:     echo %SANDBOX%
33: echo Запускаю новую clean sandbox в отдельном окне.
35: start "OSBB Live Service Sandbox" cmd.exe /k ""%PYTHON%" "%RUNNER%" --sandbox "%SANDBOX%" --run"
```

### `CHECK_phone_barrier_access_sandbox_schema.py`

- Score: `28`
- Kind: `py`
- SHA: `8e4c82b70733`
- Size: `3761`
- Modified: `2026-06-27 19:14:06`
- Markers: `sandbox_db, ukrainian_ui`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
2: """Read-only verification of the phone-barrier access sandbox schema."""
12: SANDBOX_DB = (
16:     / "sandbox"
17:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
34:     if not SANDBOX_DB.is_file():
35:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
37:     conn = sqlite3.connect(SANDBOX_DB)
50:         print("OSBB phone-barrier access sandbox schema")
51:         print("Database:", SANDBOX_DB)
58:             SELECT access_point_code, display_name_uk, point_status, is_active
64:                 f" - {row['access_point_code']}: {row['display_name_uk']} "
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_phone_barrier_access_sandbox_schema\CHECK_phone_barrier_access_sandbox_schema__8e4c82b70733.py`

- Score: `28`
- Kind: `py`
- SHA: `8e4c82b70733`
- Size: `3761`
- Modified: `2026-07-02 22:59:38`
- Markers: `sandbox_db, ukrainian_ui`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
2: """Read-only verification of the phone-barrier access sandbox schema."""
12: SANDBOX_DB = (
16:     / "sandbox"
17:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
34:     if not SANDBOX_DB.is_file():
35:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
37:     conn = sqlite3.connect(SANDBOX_DB)
50:         print("OSBB phone-barrier access sandbox schema")
51:         print("Database:", SANDBOX_DB)
58:             SELECT access_point_code, display_name_uk, point_status, is_active
64:                 f" - {row['access_point_code']}: {row['display_name_uk']} "
```

### `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_schema_migration\CHECK_phone_barrier_access_sandbox_schema.py`

- Score: `28`
- Kind: `py`
- SHA: `8e4c82b70733`
- Size: `3761`
- Modified: `2026-07-02 22:59:38`
- Markers: `sandbox_db, ukrainian_ui`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
2: """Read-only verification of the phone-barrier access sandbox schema."""
12: SANDBOX_DB = (
16:     / "sandbox"
17:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
34:     if not SANDBOX_DB.is_file():
35:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
37:     conn = sqlite3.connect(SANDBOX_DB)
50:         print("OSBB phone-barrier access sandbox schema")
51:         print("Database:", SANDBOX_DB)
58:             SELECT access_point_code, display_name_uk, point_status, is_active
64:                 f" - {row['access_point_code']}: {row['display_name_uk']} "
```

### `CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.bat`

- Score: `25`
- Kind: `bat`
- SHA: `e6ca58918126`
- Size: `866`
- Modified: `2026-06-27 12:15:02`
- Markers: `sandbox_db`

References:
- `\CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.py`

Interesting lines:
```text
11: echo This creates ONE clearly marked TEST payment in the LIVE SERVICES SANDBOX only.
```

### `RUN_CHECK_cashier_route_after_phone_v2.bat`

- Score: `25`
- Kind: `bat`
- SHA: `25934662ba47`
- Size: `297`
- Modified: `2026-06-27 20:00:41`
- Markers: `sandbox_db`

References:
- `\run_bot_live_services_sandbox_v1.py`

Interesting lines:
```text
7: echo OSBB live-services sandbox launcher check
11: "%PY%" "%ROOT%\run_bot_live_services_sandbox_v1.py"
```

### `CHECK_phone_barrier_access_operational_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `c22827184b78`
- Size: `2921`
- Modified: `2026-06-27 19:31:22`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
17:     db = root / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
28:         raise FileNotFoundError(f"Sandbox database not found:\n{db}")
52:         print("OSBB two-barrier phone-access operational sandbox check")
```

### `CHECK_profile_parking_time_test_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `55c1f1aa3c66`
- Size: `2764`
- Modified: `2026-06-28 12:11:29`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from profile_parking_time_test_core import (`

Interesting lines:
```text
16: SANDBOX_DB = (
17:     ROOT / "Data" / "db" / "sandbox"
18:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
36:     print("Database:", SANDBOX_DB)
38:     if not SANDBOX_DB.is_file():
39:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
41:     uri = SANDBOX_DB.resolve().as_uri() + "?mode=ro"
```

### `CHECK_profile_verification_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `73286e2ac2f8`
- Size: `2596`
- Modified: `2026-06-27 20:48:58`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from profile_verification_core import PROFILE_POLICY_SET, PROFILE_SCHEMA_MIGRATION_CODE`

Interesting lines:
```text
2: """Read-only check for resident profile verification sandbox schema."""
8: SANDBOX_DB=ROOT/"Data"/"db"/"sandbox"/"osbb_test_live_services_2026-06-26_20-13-26.db"
13:     print("OSBB resident profile verification sandbox check")
15:     print("Database:",SANDBOX_DB)
16:     if not SANDBOX_DB.is_file(): raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
17:     conn=sqlite3.connect(SANDBOX_DB)
```

### `diagnose_sandbox_charges.py`

- Score: `18`
- Kind: `py`
- SHA: `452ce751f633`
- Size: `7277`
- Modified: `2026-06-25 22:20:08`
- Markers: `sandbox_db`

References:
- `G:\Programming\Py\OSBB\diagnose_sandbox_charges.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `from pathlib import Path`

Interesting lines:
```text
2: Диагностика начислений для sandbox-версии «Касса и платежи v2».
4: Только читает указанную sandbox-БД.
15: g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\diagnose_sandbox_charges.py --sandbox "G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db"
25: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
58:     parser.add_argument("--sandbox", required=True)
61:     sandbox = Path(args.sandbox).resolve()
63:         sandbox.relative_to(SANDBOX_DIR.resolve())
65:         raise SystemExit("Разрешены только БД внутри Data\\db\\sandbox.")
66:     if not sandbox.exists():
67:         raise SystemExit(f"Не найдена sandbox-БД: {sandbox}")
69:     conn = sqlite3.connect(sandbox)
74:         print("SANDBOX CHARGES DIAGNOSTIC — READ ONLY")
76:         print("DB:", sandbox)
```

### `find_sandbox_telegram_id.py`

- Score: `18`
- Kind: `py`
- SHA: `867a20b2903c`
- Size: `5204`
- Modified: `2026-06-26 13:45:55`
- Markers: `sandbox_db`

References:
- `G:\Programming\Py\OSBB\find_sandbox_telegram_id.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `from pathlib import Path`

Interesting lines:
```text
2: Найти Telegram ID, привязанный к квартире, в указанной sandbox-БД.
4: Скрипт только читает .db внутри Data\db\sandbox. Он не меняет базу,
8: g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\find_sandbox_telegram_id.py ^
9:   --sandbox "G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09.db" ^
20: SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
44:     parser.add_argument("--sandbox", required=True)
48:     db = Path(args.sandbox).resolve()
50:         db.relative_to(SANDBOX_DIR.resolve())
52:         raise SystemExit("Разрешены только базы внутри Data\\db\\sandbox.")
54:         raise SystemExit(f"Не найдена sandbox-БД: {db}")
117:         print("SANDBOX TELEGRAM ACCOUNT LOOKUP — READ ONLY")
```

### `FIX_live_services_sandbox_payment_schema.py`

- Score: `18`
- Kind: `py`
- SHA: `80264d1a0e65`
- Size: `11425`
- Modified: `2026-06-27 12:24:35`
- Markers: `sandbox_db`

References:
- `- config.py`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
3: OSBB — one-time compatibility repair for the LIVE SERVICES sandbox database.
6:   Data\db\sandbox\osbb_test_live_services_2026-06-26_20-13-26.db
10:   - any other sandbox database
15:   1. Creates a timestamped backup of this sandbox database.
23: Run only while the LIVE SERVICES sandbox bot is stopped.
41:     / "sandbox"
42:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
44: BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
160:     Fallback mapping for a service-order sandbox: use service_orders itself.
219:             f"Test order {TEST_ORDER_NUMBER} was not found in the selected sandbox."
244:             f"Test payment #{TEST_PAYMENT_ID} was not found in the selected sandbox."
282:         log_path = LOG_DIR / f"live_services_payment_schema_fix_{stamp}.txt"
290:     emit("OSBB LIVE SERVICES SANDBOX — PAYMENT SCHEMA FIX")
296:             "The expected live-services sandbox database was not found. "
308:                 "This repair must not run against the old guard sandbox."
332:     emit("DONE: the sandbox payment schema is compatible with the service-order link.")
333:     emit("Now restart Start_OSBB_Live_Services_Sandbox_Bot_v1.bat and repeat payment #93.")
```

### `MIGRATE_profile_parking_time_test_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `57324665edea`
- Size: `3108`
- Modified: `2026-06-28 12:11:28`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from profile_parking_time_test_core import ensure_test_schema`

Interesting lines:
```text
3: Create TEST-only parking_time session tables in the live-services sandbox.
19: SANDBOX_DB = (
20:     ROOT / "Data" / "db" / "sandbox"
21:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
23: BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
33:     print("Mode: SANDBOX ONLY")
35:     print("Database:", SANDBOX_DB)
37:     if not SANDBOX_DB.is_file():
38:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
40:     conn = sqlite3.connect(SANDBOX_DB)
50:                 "This is not the expected live-services sandbox. Missing: "
59:         f"{SANDBOX_DB.stem}_before_profile_parking_time_test_{stamp}{SANDBOX_DB.suffix}"
61:     shutil.copy2(SANDBOX_DB, backup)
64:     conn = sqlite3.connect(SANDBOX_DB)
69:             actor_id="sandbox_parking_time_test_migration",
70:             sandbox_db_path=str(SANDBOX_DB),
85:                 "Mode: SANDBOX ONLY",
86:                 f"Database: {SANDBOX_DB}",
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_phone_barrier_access_operational_sandbox\CHECK_phone_barrier_access_operational_sandbox__c22827184b78.py`

- Score: `18`
- Kind: `py`
- SHA: `c22827184b78`
- Size: `2921`
- Modified: `2026-07-02 22:59:38`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
17:     db = root / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
28:         raise FileNotFoundError(f"Sandbox database not found:\n{db}")
52:         print("OSBB two-barrier phone-access operational sandbox check")
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_profile_parking_time_test_sandbox\CHECK_profile_parking_time_test_sandbox__55c1f1aa3c66.py`

- Score: `18`
- Kind: `py`
- SHA: `55c1f1aa3c66`
- Size: `2764`
- Modified: `2026-07-02 22:59:35`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from profile_parking_time_test_core import (`

Interesting lines:
```text
16: SANDBOX_DB = (
17:     ROOT / "Data" / "db" / "sandbox"
18:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
36:     print("Database:", SANDBOX_DB)
38:     if not SANDBOX_DB.is_file():
39:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
41:     uri = SANDBOX_DB.resolve().as_uri() + "?mode=ro"
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\CHECK_profile_verification_sandbox\CHECK_profile_verification_sandbox__73286e2ac2f8.py`

- Score: `18`
- Kind: `py`
- SHA: `73286e2ac2f8`
- Size: `2596`
- Modified: `2026-07-02 22:59:36`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from profile_verification_core import PROFILE_POLICY_SET, PROFILE_SCHEMA_MIGRATION_CODE`

Interesting lines:
```text
2: """Read-only check for resident profile verification sandbox schema."""
8: SANDBOX_DB=ROOT/"Data"/"db"/"sandbox"/"osbb_test_live_services_2026-06-26_20-13-26.db"
13:     print("OSBB resident profile verification sandbox check")
15:     print("Database:",SANDBOX_DB)
16:     if not SANDBOX_DB.is_file(): raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
17:     conn=sqlite3.connect(SANDBOX_DB)
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\MIGRATE_profile_parking_time_test_sandbox\MIGRATE_profile_parking_time_test_sandbox__57324665edea.py`

- Score: `18`
- Kind: `py`
- SHA: `57324665edea`
- Size: `3108`
- Modified: `2026-07-02 22:59:35`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from profile_parking_time_test_core import ensure_test_schema`

Interesting lines:
```text
3: Create TEST-only parking_time session tables in the live-services sandbox.
19: SANDBOX_DB = (
20:     ROOT / "Data" / "db" / "sandbox"
21:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
23: BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
33:     print("Mode: SANDBOX ONLY")
35:     print("Database:", SANDBOX_DB)
37:     if not SANDBOX_DB.is_file():
38:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
40:     conn = sqlite3.connect(SANDBOX_DB)
50:                 "This is not the expected live-services sandbox. Missing: "
59:         f"{SANDBOX_DB.stem}_before_profile_parking_time_test_{stamp}{SANDBOX_DB.suffix}"
61:     shutil.copy2(SANDBOX_DB, backup)
64:     conn = sqlite3.connect(SANDBOX_DB)
69:             actor_id="sandbox_parking_time_test_migration",
70:             sandbox_db_path=str(SANDBOX_DB),
85:                 "Mode: SANDBOX ONLY",
86:                 f"Database: {SANDBOX_DB}",
```

### `Recovered\project_archaeology_2026-07-02_22-59-35\files_by_module\RETIRE_legacy_new_remote_test_orders_sandbox\RETIRE_legacy_new_remote_test_orders_sandbox__3a3bab1d10c1.py`

- Score: `18`
- Kind: `py`
- SHA: `3a3bab1d10c1`
- Size: `4377`
- Modified: `2026-07-02 22:59:39`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
3: Retire only obsolete, unpaid TEST new-remote orders in the live-services sandbox.
17: DB = ROOT / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
18: BACKUPS = ROOT / "Data" / "db" / "sandbox" / "backups"
67:                 note = COALESCE(note, 'Старий sandbox-тест резерву скасовано.'),
```

### `Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_v2_working_sandbox\CHECK_phone_barrier_access_operational_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `c22827184b78`
- Size: `2921`
- Modified: `2026-07-02 22:59:38`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from phone_barrier_access_core import (`

Interesting lines:
```text
17:     db = root / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
28:         raise FileNotFoundError(f"Sandbox database not found:\n{db}")
52:         print("OSBB two-barrier phone-access operational sandbox check")
```

### `Recovered_Releases\2026-06-27__OSBB_profile_verification_v1_sandbox_final\CHECK_profile_verification_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `73286e2ac2f8`
- Size: `2596`
- Modified: `2026-07-02 22:59:36`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from profile_verification_core import PROFILE_POLICY_SET, PROFILE_SCHEMA_MIGRATION_CODE`

Interesting lines:
```text
2: """Read-only check for resident profile verification sandbox schema."""
8: SANDBOX_DB=ROOT/"Data"/"db"/"sandbox"/"osbb_test_live_services_2026-06-26_20-13-26.db"
13:     print("OSBB resident profile verification sandbox check")
15:     print("Database:",SANDBOX_DB)
16:     if not SANDBOX_DB.is_file(): raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
17:     conn=sqlite3.connect(SANDBOX_DB)
```

### `Recovered_Releases\2026-06-27__OSBB_simplified_services_preorders_bundle\RETIRE_legacy_new_remote_test_orders_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `3a3bab1d10c1`
- Size: `4377`
- Modified: `2026-07-02 22:59:39`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
3: Retire only obsolete, unpaid TEST new-remote orders in the live-services sandbox.
17: DB = ROOT / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
18: BACKUPS = ROOT / "Data" / "db" / "sandbox" / "backups"
67:                 note = COALESCE(note, 'Старий sandbox-тест резерву скасовано.'),
```

### `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\CHECK_profile_parking_time_test_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `55c1f1aa3c66`
- Size: `2764`
- Modified: `2026-07-02 22:59:35`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from profile_parking_time_test_core import (`

Interesting lines:
```text
16: SANDBOX_DB = (
17:     ROOT / "Data" / "db" / "sandbox"
18:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
36:     print("Database:", SANDBOX_DB)
38:     if not SANDBOX_DB.is_file():
39:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
41:     uri = SANDBOX_DB.resolve().as_uri() + "?mode=ro"
```

### `Recovered_Releases\2026-06-28__OSBB_profile_parking_time_test_v1_sandbox\MIGRATE_profile_parking_time_test_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `57324665edea`
- Size: `3108`
- Modified: `2026-07-02 22:59:35`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `import sys`
- `import traceback`
- `from datetime import datetime`
- `from pathlib import Path`
- `from profile_parking_time_test_core import ensure_test_schema`

Interesting lines:
```text
3: Create TEST-only parking_time session tables in the live-services sandbox.
19: SANDBOX_DB = (
20:     ROOT / "Data" / "db" / "sandbox"
21:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
23: BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
33:     print("Mode: SANDBOX ONLY")
35:     print("Database:", SANDBOX_DB)
37:     if not SANDBOX_DB.is_file():
38:         raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
40:     conn = sqlite3.connect(SANDBOX_DB)
50:                 "This is not the expected live-services sandbox. Missing: "
59:         f"{SANDBOX_DB.stem}_before_profile_parking_time_test_{stamp}{SANDBOX_DB.suffix}"
61:     shutil.copy2(SANDBOX_DB, backup)
64:     conn = sqlite3.connect(SANDBOX_DB)
69:             actor_id="sandbox_parking_time_test_migration",
70:             sandbox_db_path=str(SANDBOX_DB),
85:                 "Mode: SANDBOX ONLY",
86:                 f"Database: {SANDBOX_DB}",
```

### `RETIRE_legacy_new_remote_test_orders_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `3a3bab1d10c1`
- Size: `4377`
- Modified: `2026-06-27 13:29:00`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import shutil`
- `import sqlite3`
- `from datetime import datetime`
- `from pathlib import Path`

Interesting lines:
```text
3: Retire only obsolete, unpaid TEST new-remote orders in the live-services sandbox.
17: DB = ROOT / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
18: BACKUPS = ROOT / "Data" / "db" / "sandbox" / "backups"
67:                 note = COALESCE(note, 'Старий sandbox-тест резерву скасовано.'),
```

### `tools\dump_service_codes_live_sandbox.py`

- Score: `18`
- Kind: `py`
- SHA: `4eb7b95ad64b`
- Size: `3503`
- Modified: `2026-06-28 21:28:54`
- Markers: `sandbox_db`

References:
- `G:\Programming\Py\OSBB\tools\dump_service_codes_live_sandbox.py`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `from pathlib import Path`

Interesting lines:
```text
4: dump_service_codes_live_sandbox.py
17: DEFAULT_DB = r"G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_live_services_2026-06-26_20-13-26.db"
38:     out = out_dir / "service_codes_live_sandbox.txt"
```

### `tools\start_live_services_bot.py`

- Score: `18`
- Kind: `py`
- SHA: `b818c2430c1f`
- Size: `1920`
- Modified: `2026-06-28 19:20:09`
- Markers: `sandbox_db`

References:
- `G:\Programming\Py\OSBB\tools\start_live_services_bot.py`
- `G:\Programming\Py\OSBB\run_bot_live_services_sandbox_v1.py`

Imports:
- `from __future__ import annotations`
- `import json`
- `import subprocess`
- `from pathlib import Path`

Interesting lines:
```text
4: start_live_services_bot.py
6: Starts OSBB Live Services Sandbox bot only if it is not already running.
9:   python .\OSBB\tools\start_live_services_bot.py
19: TARGET = "run_bot_live_services_sandbox_v1.py"
20: BAT = r"G:\Programming\Py\OSBB\Start_OSBB_Live_Services_Sandbox_Bot_v1.bat"
```

### `cashier_v2_core.py`

- Score: `15`
- Kind: `py`
- SHA: `e0a50264b274`
- Size: `56934`
- Modified: `2026-06-25 23:17:40`
- Markers: `client_portal, sandbox_db`

References:
- `G:\Programming\Py\OSBB\Bots\handlers\cashier_operator_v2.py`
- `G:\Programming\Py\OSBB\Bots\handlers\client_portal_v2.py`
- `G:\Programming\Py\config.py`

Imports:
- `from __future__ import annotations`
- `from datetime import date, datetime`
- `from pathlib import Path`
- `import re`
- `import sqlite3`
- `import sys`
- `from typing import Any`
- `from uuid import uuid4`
- `from config import paths, USE_TEST_DB`
- `from audit_logger import audit_log`
- `from unit_resolver import resolve_unit_ref`
- `from handlers import cashier_operator as v1`

Interesting lines:
```text
6: - клиентским кабинетом client_portal_v2.py.
129:     return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
961:             source_context="client_portal_v2",
```

### `RUN_CHECK_profile_button_early_route_fix.bat`

- Score: `15`
- Kind: `bat`
- SHA: `59782ec1dd02`
- Size: `332`
- Modified: `2026-06-27 21:42:13`
- Markers: `none`

References:
- `G:\Programming\Py\OSBB\CHECK_profile_button_early_route_fix.py`

### `RUN_CHECK_profile_confirmation_ready_visibility_fix.bat`

- Score: `15`
- Kind: `bat`
- SHA: `ee2ad5a2ce50`
- Size: `319`
- Modified: `2026-06-27 21:55:14`
- Markers: `none`

References:
- `G:\Programming\Py\OSBB\CHECK_profile_confirmation_ready_visibility_fix.py`

### `RUN_CHECK_profile_critical_codes_fix.bat`

- Score: `15`
- Kind: `bat`
- SHA: `c18229d452b7`
- Size: `296`
- Modified: `2026-06-27 21:45:58`
- Markers: `none`

References:
- `G:\Programming\Py\OSBB\CHECK_profile_critical_codes_fix.py`

### `RUN_CHECK_profile_test_candidate_apartment_40.bat`

- Score: `15`
- Kind: `bat`
- SHA: `c4b403c66187`
- Size: `331`
- Modified: `2026-06-27 22:23:23`
- Markers: `none`

References:
- `G:\Programming\Py\OSBB\CHECK_profile_test_candidate_apartment_40.py`

### `RUN_CHECK_profile_verification_terminology_v2.bat`

- Score: `15`
- Kind: `bat`
- SHA: `91a7950b9d89`
- Size: `321`
- Modified: `2026-06-27 21:22:51`
- Markers: `none`

References:
- `\CHECK_profile_verification_terminology_v2.py`

### `RUN_CHECK_service_code_compatibility_phone_v2.bat`

- Score: `15`
- Kind: `bat`
- SHA: `a510e56abde4`
- Size: `306`
- Modified: `2026-06-27 20:18:30`
- Markers: `none`

References:
- `G:\Programming\Py\OSBB\CHECK_service_code_compatibility_phone_v2.py`

### `RUN_FIND_actual_service_order_state.bat`

- Score: `15`
- Kind: `bat`
- SHA: `9b3a1956b363`
- Size: `795`
- Modified: `2026-06-27 11:56:04`
- Markers: `none`

References:
- `G:\Programming\Py\OSBB\FIND_actual_service_order_state.py`

### `RUN_fix_source_ref_schema.bat`

- Score: `15`
- Kind: `bat`
- SHA: `f45709673fcb`
- Size: `807`
- Modified: `2026-06-27 10:41:04`
- Markers: `none`

References:
- `G:\Programming\Py\OSBB\fix_source_ref_schema.py`

### `Bots\handlers\profile_verification_workspace.py`

- Score: `15`
- Kind: `py`
- SHA: `131afe386eac`
- Size: `30339`
- Modified: `2026-06-27 21:55:14`
- Markers: `client_portal, ukrainian_ui`

Imports:
- `from __future__ import annotations`
- `from pathlib import Path`
- `import sqlite3`
- `import sys`
- `from typing import Any`
- `from telegram import ReplyKeyboardMarkup, Update`
- `from handlers import client_portal as resident_portal`
- `from service_orders_core import get_conn, text`
- `from profile_verification_core import (`

Interesting lines:
```text
26: from handlers import client_portal as resident_portal
61:     "uk": "✅ Підтвердити обов’язкові дані",
66:     "uk": "🚫 Підтверджую: автомобіля немає",
71:     "uk": "🅿️ Уточнити тариф паркування",
76:     "uk": "✏️ Повідомити про неточність",
81:     "uk": "🔄 Оновити дані",
86:     "uk": "⬅️ До кабінету",
91:     "uk": "📋 Черга заявок",
96:     "uk": "✅ Підтвердити оператором",
101:     "uk": "❌ Відхилити",
106:     "uk": "⬅️ До перевірки даних",
321:             reply_markup=kb([[ _tr({"ru": "📋 Проверить мои данные", "uk": "📋 Перевірити мої дані", "en": "📋 Verify my data"}, lang) ], ["🏠 Главное меню"]]),
399:                 [_tr({"ru": "📋 Проверить мои данные", "uk": "📋 Перевірити мої дані", "en": "📋 Verify my data"}, lang)],
563:     lang = lang if lang in {"ru", "uk", "en"} else "ru"
```

### `G:\Programming\Py\config.py`

- Score: `10`
- Kind: `py`
- SHA: `84207464df23`
- Size: `5902`
- Modified: `2026-06-17 14:57:03`
- Markers: `sandbox_db`

References:
- `G:\Programming\Py\config.py`
- `telegram_osbb.py`

Imports:
- `import sys`
- `from pathlib import Path`
- `import platform`
- `import subprocess`
- `import re`
- `import json`
- `from datetime import datetime`

Interesting lines:
```text
85:         self.OSBB_TEST_DB_FILE = self.OSBB_DB_DIR / "osbb_test.db"
```

### `service_preorders_core.py`

- Score: `10`
- Kind: `py`
- SHA: `a67ea947627b`
- Size: `44217`
- Modified: `2026-07-02 22:59:37`
- Markers: `ukrainian_ui`

Imports:
- `from __future__ import annotations`
- `from datetime import datetime`
- `import sqlite3`
- `from typing import Any`
- `from service_orders_core import (`
- `from phone_barrier_access_service import promote_paid_phone_barrier_access_interest`

Interesting lines:
```text
297:             ("REMOTE_BATCH_ISSUED", "Пульти видано мешканцю", "ISSUE", 40),
```

### `service_orders_core.py`

- Score: `10`
- Kind: `py`
- SHA: `7c2d3ac6f66f`
- Size: `44925`
- Modified: `2026-07-02 22:59:37`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `from datetime import date, datetime`
- `from pathlib import Path`
- `import sqlite3`
- `import sys`
- `from typing import Any`
- `from config import paths, USE_TEST_DB`
- `from audit_logger import audit_log`
- `from access_control import has_permission`

Interesting lines:
```text
64:     return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
97:     Historic/current sandbox variants may store the broad service code in
```

### `access_control.py`

- Score: `10`
- Kind: `py`
- SHA: `e22bedb3aa11`
- Size: `11350`
- Modified: `2026-06-26 12:15:06`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import sqlite3`
- `import sys`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any`
- `from config import paths, USE_TEST_DB`
- `from audit_logger import audit_log`

Interesting lines:
```text
60:     return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
```

### `CHECK_profile_test_candidate_apartment_40.py`

- Score: `10`
- Kind: `py`
- SHA: `3df07d574dc8`
- Size: `10492`
- Modified: `2026-06-27 22:23:22`
- Markers: `sandbox_db`

Imports:
- `from __future__ import annotations`
- `import argparse`
- `import sqlite3`
- `import sys`
- `from pathlib import Path`
- `from typing import Any`

Interesting lines:
```text
7:     live-services sandbox database only
18: 1. Does apartment 40 exist in the sandbox?
21: 4. Is it suitable for the isolated operator sandbox test?
35:     ROOT / "Data" / "db" / "sandbox"
36:     / "osbb_test_live_services_2026-06-26_20-13-26.db"
107:         raise FileNotFoundError(f"Sandbox database not found:\n{db_path}")
263:         help="Sandbox SQLite path. Default: designated live-services sandbox.",
325:                 "Apartment 40 is suitable for the next isolated operator sandbox test."
```

### `Bots\handlers\cashier_operator_v2.py`

- Score: `0`
- Kind: `py`
- SHA: `a0cc7e357610`
- Size: `45714`
- Modified: `2026-06-25 17:41:58`
- Markers: `none`

References:
- `G:\Programming\Py\OSBB\Bots\handlers\cashier_operator.py`

Imports:
- `from __future__ import annotations`
- `from pathlib import Path`
- `import sys`
- `from typing import Any`
- `from telegram import Update, ReplyKeyboardMarkup`
- `from handlers import cashier_operator as v1`
- `from cashier_v2_core import (`

### `service_catalog_admin_core.py`

- Score: `0`
- Kind: `py`
- SHA: `9b34ba89291d`
- Size: `19165`
- Modified: `2026-06-26 19:39:26`
- Markers: `none`

Imports:
- `from __future__ import annotations`
- `from datetime import datetime, timedelta`
- `from pathlib import Path`
- `import sqlite3`
- `import sys`
- `from typing import Any`
- `from service_orders_core import (`
- `from access_control import has_permission`

### `CHECK_profile_confirmation_ready_visibility_fix.py`

- Score: `0`
- Kind: `py`
- SHA: `2f6acd85e87e`
- Size: `1095`
- Modified: `2026-06-27 21:55:13`
- Markers: `none`

References:
- `profile_verification_workspace.py`

Imports:
- `from pathlib import Path`

### `CHECK_profile_critical_codes_fix.py`

- Score: `0`
- Kind: `py`
- SHA: `48d683777040`
- Size: `1174`
- Modified: `2026-06-27 21:45:58`
- Markers: `none`

References:
- `profile_verification_workspace.py`

Imports:
- `from pathlib import Path`

### `INSTALL_profile_confirmation_ready_visibility_fix.py`

- Score: `0`
- Kind: `py`
- SHA: `1697bf1e439b`
- Size: `2272`
- Modified: `2026-06-27 21:55:12`
- Markers: `none`

References:
- `G:\Programming\Py\OSBB\Bots\handlers\profile_verification_workspace.py`
- `profile_verification_workspace.py`

Imports:
- `from __future__ import annotations`
- `import py_compile`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

### `INSTALL_profile_critical_codes_fix.py`

- Score: `0`
- Kind: `py`
- SHA: `29396ec18d50`
- Size: `2212`
- Modified: `2026-06-27 21:45:58`
- Markers: `none`

References:
- `G:\Programming\Py\OSBB\Bots\handlers\profile_verification_workspace.py`
- `profile_verification_workspace.py`

Imports:
- `from __future__ import annotations`
- `import py_compile`
- `import shutil`
- `from datetime import datetime`
- `from pathlib import Path`

