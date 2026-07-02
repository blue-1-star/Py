# MODULE: vehicle_verification

Status: draft
Handler: `vehicle_verification.py`
Created: 2026-07-02 19:49:55
Last reviewed: TODO
Code hash at creation: `1d475d42a3190db3`

## Purpose

TODO: describe module purpose.

## Business meaning

TODO: describe what real OSBB process this module supports.

Examples:

- resident self-service;
- operator workspace;
- payments/cashbox;
- remote/pult requests;
- phone access;
- vehicle registry;
- commercial contracts;
- guard workspace.

## Current implementation evidence

### Functions

- `consensus_action_menu`
- `kb`
- `get_db_file`
- `table_exists`
- `table_columns`
- `insert_operator_audit`
- `get_tie_tasks`
- `get_tasks_cached`
- `current_task`
- `source_label`
- `is_valid_ua_plate`
- `digits_count`
- `plate_warning`
- `get_plate_variants`
- `paper_fact_for_item`
- `format_consensus_task_for_operator`
- `format_dashboard`
- `parse_variant_index`
- `update_paper_vehicle_plate`
- `audit_no_change`
- `recount_after_change`
- `show_vehicle_verification_dashboard`
- `show_current_vehicle_task`
- `parse_selected_plate`
- `find_variant_index_by_plate`
- `choose_variant`
- `skip_task`
- `handle_vehicle_verification_text`

### Classes

- None detected.

### Database / schema keywords found

- `vehicles`
- `payments`
- `operator_audit_log`
- `audit_log`
- `apartments`

### User-facing text / buttons found

- `payments`
- `В бумажной базе нет автомобиля для автоматического исправления.\n`
- `Квартира: {`
- `Спорных задач проверки авто нет.`
- `▶️ Начать проверку авто`
- `✅ {variant[`
- `✅ Выбор зафиксирован.\n\n`
- `✅ Номер исправлен\n\n`
- `✅ Номер подтверждён без изменения базы.\n\n`
- `🏠 Главное меню`
- `📊 Сводка проверки авто`
- `🚗 Проверка авто`
- `🚗 Проверка авто {index}/{total}`

## Dependencies

TODO: list related handlers, services, tables, migrations.

## Entry points

TODO: list where this module is called from.

## Known legacy / risks

TODO: record confusing old flows, duplicates, copy-files, partial implementations.

## Acceptance tests

- [ ] Opens without error.
- [ ] Main menu path is known.
- [ ] Creates expected DB records.
- [ ] Operator/admin can see created records.
- [ ] Status change works.
- [ ] Audit trail is written where needed.
- [ ] Tested on Working DB, not Golden Master.

## Current notes

<!-- MODULE_NOTES:BEGIN -->
<!-- MODULE_NOTES:END -->

## Change log

<!-- MODULE_CHANGELOG:BEGIN -->
- 2026-07-02 19:49:55 - MODULE.md created by module_registry_manager.py.
<!-- MODULE_CHANGELOG:END -->
