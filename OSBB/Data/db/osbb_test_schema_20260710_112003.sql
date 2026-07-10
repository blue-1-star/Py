================================================================================
-- СТРУКТУРА БАЗЫ ДАННЫХ (SQL для восстановления)
-- Файл: osbb_test.db
-- Дата экспорта: 2026-07-10 11:20:03
================================================================================

-- Включаем поддержку внешних ключей
PRAGMA foreign_keys = OFF;

-- ==========================================
-- УДАЛЕНИЕ СУЩЕСТВУЮЩИХ ТАБЛИЦ (каскадное)
-- ==========================================

DROP TABLE IF EXISTS verification_tasks;
DROP TABLE IF EXISTS verification_log;
DROP TABLE IF EXISTS verification_evidence;
DROP TABLE IF EXISTS verification_candidates;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS unit_groups;
DROP TABLE IF EXISTS unit_group_members;
DROP TABLE IF EXISTS unit_group_aliases;
DROP TABLE IF EXISTS unit_contacts;
DROP TABLE IF EXISTS unit_aliases;
DROP TABLE IF EXISTS tbot_parking_import;
DROP TABLE IF EXISTS staff_principals;
DROP TABLE IF EXISTS service_workflow_steps;
DROP TABLE IF EXISTS service_workflow_profiles;
DROP TABLE IF EXISTS service_tariffs;
DROP TABLE IF EXISTS service_price_versions;
DROP TABLE IF EXISTS service_orders;
DROP TABLE IF EXISTS service_order_steps;
DROP TABLE IF EXISTS service_order_payment_links;
DROP TABLE IF EXISTS service_order_interests;
DROP TABLE IF EXISTS service_order_events;
DROP TABLE IF EXISTS service_order_charge_links;
DROP TABLE IF EXISTS service_items;
DROP TABLE IF EXISTS service_item_workflows;
DROP TABLE IF EXISTS service_interests;
DROP TABLE IF EXISTS service_catalog;
DROP TABLE IF EXISTS service_access_credentials;
DROP TABLE IF EXISTS schema_info;
DROP TABLE IF EXISTS resident_verification_requests;
DROP TABLE IF EXISTS resident_profile_verifications;
DROP TABLE IF EXISTS resident_profile_schema_migrations;
DROP TABLE IF EXISTS resident_profile_policy_versions;
DROP TABLE IF EXISTS resident_profile_policy_values;
DROP TABLE IF EXISTS resident_profile_operation_journal;
DROP TABLE IF EXISTS resident_profile_change_requests;
DROP TABLE IF EXISTS resident_invitations;
DROP TABLE IF EXISTS resident_accounts;
DROP TABLE IF EXISTS resident_access_accounts;
DROP TABLE IF EXISTS remote_supplier_batches;
DROP TABLE IF EXISTS remote_supplier_batch_links;
DROP TABLE IF EXISTS remote_requests;
DROP TABLE IF EXISTS remote_order_issued_assets;
DROP TABLE IF EXISTS remote_order_details;
DROP TABLE IF EXISTS remote_handover_events;
DROP TABLE IF EXISTS remote_assets;
DROP TABLE IF EXISTS remote_asset_movements;
DROP TABLE IF EXISTS raw_messages;
DROP TABLE IF EXISTS profile_parking_time_test_sessions;
DROP TABLE IF EXISTS profile_parking_time_test_schema_migrations;
DROP TABLE IF EXISTS profile_parking_time_test_events;
DROP TABLE IF EXISTS phone_barrier_access_points;
DROP TABLE IF EXISTS phone_barrier_access_order_points;
DROP TABLE IF EXISTS phone_barrier_access_interests;
DROP TABLE IF EXISTS phone_barrier_access_interest_points;
DROP TABLE IF EXISTS phone_access_subscriptions;
DROP TABLE IF EXISTS phone_access_subscription_points;
DROP TABLE IF EXISTS phone_access_subscription_charges;
DROP TABLE IF EXISTS phone_access_requests;
DROP TABLE IF EXISTS phone_access_request_points;
DROP TABLE IF EXISTS persons;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS payment_notices;
DROP TABLE IF EXISTS payment_allocations;
DROP TABLE IF EXISTS parking_time_review_tasks;
DROP TABLE IF EXISTS operator_task_queue;
DROP TABLE IF EXISTS operator_audit_log;
DROP TABLE IF EXISTS message_sources;
DROP TABLE IF EXISTS extracted_facts;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS contact_methods;
DROP TABLE IF EXISTS commercial_notifications;
DROP TABLE IF EXISTS commercial_contracts;
DROP TABLE IF EXISTS commercial_contract_recipients;
DROP TABLE IF EXISTS commercial_contract_items;
DROP TABLE IF EXISTS commercial_access_phones;
DROP TABLE IF EXISTS commercial_access_actions;
DROP TABLE IF EXISTS charges;
DROP TABLE IF EXISTS charge_adjustments;
DROP TABLE IF EXISTS cashier_settings;
DROP TABLE IF EXISTS cashier_reconciliation_cases;
DROP TABLE IF EXISTS cashier_receipts;
DROP TABLE IF EXISTS cashier_batches;
DROP TABLE IF EXISTS cashier_batch_items;
DROP TABLE IF EXISTS cashboxes;
DROP TABLE IF EXISTS cashbox_operations;
DROP TABLE IF EXISTS bot_user_sessions;
DROP TABLE IF EXISTS bot_admins;
DROP TABLE IF EXISTS barrier_phone_access;
DROP TABLE IF EXISTS bank_transactions;
DROP TABLE IF EXISTS audit_log;
DROP TABLE IF EXISTS apartments;
DROP TABLE IF EXISTS apartment_verification;
DROP TABLE IF EXISTS apartment_link_requests;
DROP TABLE IF EXISTS adjustment_catalog;
DROP TABLE IF EXISTS adjustment_assignments;
DROP TABLE IF EXISTS access_user_roles;
DROP TABLE IF EXISTS access_user_permissions;
DROP TABLE IF EXISTS access_tariff_versions;
DROP TABLE IF EXISTS access_schema_migrations;
DROP TABLE IF EXISTS access_roles;
DROP TABLE IF EXISTS access_role_permissions;
DROP TABLE IF EXISTS access_policy_versions;
DROP TABLE IF EXISTS access_policy_values;
DROP TABLE IF EXISTS access_points;
DROP TABLE IF EXISTS access_permissions;
DROP TABLE IF EXISTS access_operation_journal;
DROP TABLE IF EXISTS access_external_commands;
DROP TABLE IF EXISTS access_debt_warnings;
DROP TABLE IF EXISTS access_audit_log;

-- ==========================================
-- СОЗДАНИЕ ТАБЛИЦ
-- ==========================================

-- Таблица: access_audit_log
CREATE TABLE access_audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            actor_telegram_user_id TEXT NOT NULL,
            action_type TEXT NOT NULL,
            resource TEXT NOT NULL,
            action TEXT NOT NULL,
            scope_type TEXT NOT NULL DEFAULT 'ALL',
            scope_value TEXT NOT NULL DEFAULT '*',
            target_table TEXT,
            target_id TEXT,
            success INTEGER NOT NULL DEFAULT 1,
            details TEXT
        );

-- Таблица: access_debt_warnings
CREATE TABLE access_debt_warnings (
            id INTEGER PRIMARY KEY,
            warning_number TEXT NOT NULL UNIQUE,
            subscription_id INTEGER NOT NULL,
            debt_source TEXT NOT NULL
                CHECK(debt_source IN (
                    'PARKING_ARREARS',
                    'PHONE_ACCESS_SUBSCRIPTION_ARREARS'
                )),
            source_charge_id INTEGER,
            debt_amount_snapshot REAL NOT NULL CHECK(debt_amount_snapshot >= 0),
            currency TEXT NOT NULL DEFAULT 'UAH',
            source_reference TEXT,
            detected_at TEXT NOT NULL,
            warning_sent_at TEXT,
            grace_days_snapshot INTEGER NOT NULL CHECK(grace_days_snapshot >= 0),
            deactivate_due_at TEXT NOT NULL,
            policy_version_id INTEGER,
            warning_status TEXT NOT NULL DEFAULT 'OPEN'
                CHECK(warning_status IN (
                    'OPEN', 'RESOLVED', 'CANCELLED',
                    'DEACTIVATION_QUEUED', 'DEACTIVATED'
                )),
            resolved_at TEXT,
            resolution_note TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

-- Таблица: access_external_commands
CREATE TABLE access_external_commands (
            id INTEGER PRIMARY KEY,
            command_number TEXT NOT NULL UNIQUE,
            subscription_id INTEGER NOT NULL,
            subscription_point_id INTEGER NOT NULL,
            access_point_code TEXT NOT NULL,
            command_action TEXT NOT NULL
                CHECK(command_action IN ('ACTIVATE', 'DEACTIVATE')),
            phone_snapshot TEXT NOT NULL,
            command_status TEXT NOT NULL DEFAULT 'QUEUED'
                CHECK(command_status IN (
                    'QUEUED', 'SENT', 'CONFIRMED', 'FAILED',
                    'RETRY_SCHEDULED', 'CANCELLED'
                )),
            attempt_number INTEGER NOT NULL DEFAULT 0 CHECK(attempt_number >= 0),
            external_correlation_id TEXT,
            payload_json TEXT,
            last_error TEXT,
            queued_at TEXT NOT NULL,
            sent_at TEXT,
            confirmed_at TEXT,
            failed_at TEXT,
            retry_at TEXT,
            created_by TEXT,
            updated_at TEXT NOT NULL
        );

-- Таблица: access_operation_journal
CREATE TABLE access_operation_journal (
            id INTEGER PRIMARY KEY,
            event_number TEXT NOT NULL UNIQUE,
            subscription_id INTEGER,
            subscription_point_id INTEGER,
            access_point_code TEXT,
            event_type TEXT NOT NULL,
            old_status TEXT,
            new_status TEXT,
            actor_id TEXT,
            source_context TEXT,
            correlation_id TEXT,
            payload_json TEXT,
            created_at TEXT NOT NULL
        );

-- Таблица: access_permissions
CREATE TABLE access_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            permission_code TEXT UNIQUE NOT NULL,
            permission_name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT);

-- Таблица: access_points
CREATE TABLE access_points (
            id INTEGER PRIMARY KEY,
            access_point_code TEXT NOT NULL UNIQUE,
            display_name_uk TEXT NOT NULL,
            display_name_ru TEXT NOT NULL,
            display_name_en TEXT NOT NULL,
            point_status TEXT NOT NULL DEFAULT 'ACTIVE'
                CHECK(point_status IN ('DRAFT', 'ACTIVE', 'RETIRED', 'ARCHIVED')),
            controller_type TEXT,
            controller_reference TEXT,
            is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0, 1)),
            effective_from TEXT NOT NULL,
            effective_to TEXT,
            retired_at TEXT,
            retired_reason TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

-- Таблица: access_policy_values
CREATE TABLE access_policy_values (
            id INTEGER PRIMARY KEY,
            policy_version_id INTEGER NOT NULL,
            setting_code TEXT NOT NULL,
            value_type TEXT NOT NULL
                CHECK(value_type IN ('TEXT', 'INTEGER', 'BOOLEAN', 'JSON')),
            value_text TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(policy_version_id, setting_code)
        );

-- Таблица: access_policy_versions
CREATE TABLE access_policy_versions (
            id INTEGER PRIMARY KEY,
            policy_set_code TEXT NOT NULL,
            version_number INTEGER NOT NULL CHECK(version_number > 0),
            policy_status TEXT NOT NULL DEFAULT 'ACTIVE'
                CHECK(policy_status IN ('DRAFT', 'ACTIVE', 'RETIRED', 'ARCHIVED')),
            effective_from TEXT NOT NULL,
            effective_to TEXT,
            approved_by TEXT,
            approval_reference TEXT,
            change_reason TEXT,
            created_by TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(policy_set_code, version_number),
            UNIQUE(policy_set_code, effective_from)
        );

-- Таблица: access_role_permissions
CREATE TABLE access_role_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_code TEXT NOT NULL,
            resource TEXT NOT NULL,
            action TEXT NOT NULL,
            scope_type TEXT NOT NULL DEFAULT 'ALL',
            scope_value TEXT NOT NULL DEFAULT '*',
            effect TEXT NOT NULL DEFAULT 'ALLOW',
            is_active INTEGER NOT NULL DEFAULT 1,
            note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            UNIQUE(role_code, resource, action, scope_type, scope_value)
        );

-- Таблица: access_roles
CREATE TABLE access_roles (
            role_code TEXT PRIMARY KEY,
            role_name TEXT NOT NULL,
            description TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );

-- Таблица: access_schema_migrations
CREATE TABLE access_schema_migrations (
            migration_code TEXT PRIMARY KEY,
            schema_version TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            applied_by TEXT,
            sandbox_db_path TEXT,
            note TEXT
        );

-- Таблица: access_tariff_versions
CREATE TABLE access_tariff_versions (
            id INTEGER PRIMARY KEY,
            tariff_code TEXT NOT NULL,
            tariff_name_uk TEXT NOT NULL,
            tariff_name_ru TEXT NOT NULL,
            tariff_name_en TEXT NOT NULL,
            access_point_scope_code TEXT NOT NULL DEFAULT '*',
            charge_kind TEXT NOT NULL
                CHECK(charge_kind IN ('CONNECT', 'MONTHLY')),
            billing_period TEXT NOT NULL
                CHECK(billing_period IN ('ONE_TIME', 'MONTHLY')),
            unit_of_measure TEXT NOT NULL DEFAULT 'PER_ACCESS_POINT',
            amount REAL NOT NULL CHECK(amount >= 0),
            currency TEXT NOT NULL DEFAULT 'UAH',
            effective_from TEXT NOT NULL,
            effective_to TEXT,
            version_status TEXT NOT NULL DEFAULT 'ACTIVE'
                CHECK(version_status IN ('DRAFT', 'ACTIVE', 'RETIRED', 'ARCHIVED')),
            approved_by TEXT,
            approval_reference TEXT,
            change_reason TEXT,
            created_by TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(tariff_code, access_point_scope_code, effective_from)
        );

-- Таблица: access_user_permissions
CREATE TABLE access_user_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id TEXT NOT NULL,
            resource TEXT NOT NULL,
            action TEXT NOT NULL,
            scope_type TEXT NOT NULL DEFAULT 'ALL',
            scope_value TEXT NOT NULL DEFAULT '*',
            effect TEXT NOT NULL DEFAULT 'ALLOW',
            is_active INTEGER NOT NULL DEFAULT 1,
            valid_from TEXT,
            valid_to TEXT,
            granted_by TEXT,
            note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            UNIQUE(telegram_user_id, resource, action, scope_type, scope_value)
        );

-- Таблица: access_user_roles
CREATE TABLE access_user_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id TEXT NOT NULL,
            role_code TEXT NOT NULL,
            scope_type TEXT NOT NULL DEFAULT 'ALL',
            scope_value TEXT NOT NULL DEFAULT '*',
            is_active INTEGER NOT NULL DEFAULT 1,
            valid_from TEXT,
            valid_to TEXT,
            granted_by TEXT,
            note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            UNIQUE(telegram_user_id, role_code, scope_type, scope_value)
        );

-- Таблица: adjustment_assignments
CREATE TABLE adjustment_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            adjustment_code TEXT NOT NULL,
            adjustment_type TEXT NOT NULL,
            apartment_id INTEGER,
            apartment_number TEXT,
            contact_id INTEGER,
            vehicle_id INTEGER,
            base_service_code TEXT,
            service_item_code TEXT,
            calculation_kind TEXT NOT NULL,
            calculation_value REAL,
            credit_total_amount REAL,
            credit_remaining_amount REAL,
            valid_from TEXT,
            valid_to TEXT,
            status TEXT NOT NULL DEFAULT 'ACTIVE',
            approval_reference TEXT,
            public_note TEXT,
            internal_note TEXT,
            approved_by TEXT,
            created_by TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            FOREIGN KEY (adjustment_code) REFERENCES adjustment_catalog(adjustment_code)
        );

-- Таблица: adjustment_catalog
CREATE TABLE adjustment_catalog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            adjustment_code TEXT NOT NULL UNIQUE,
            adjustment_name TEXT NOT NULL,
            adjustment_type TEXT NOT NULL,
            default_calculation_kind TEXT,
            default_calculation_value REAL,
            is_sensitive INTEGER NOT NULL DEFAULT 0,
            is_active INTEGER NOT NULL DEFAULT 1,
            public_note_template TEXT,
            internal_description TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );

-- Таблица: apartment_link_requests
CREATE TABLE apartment_link_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident_account_id INTEGER NOT NULL,
            telegram_user_id TEXT NOT NULL,
            current_apartment_id INTEGER,
            current_apartment_number TEXT,
            requested_apartment_id INTEGER NOT NULL,
            requested_apartment_number TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'NEW',
            resident_comment TEXT,
            operator_id TEXT,
            operator_note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            reviewed_at TEXT,
            FOREIGN KEY(resident_account_id) REFERENCES resident_accounts(id),
            FOREIGN KEY(current_apartment_id) REFERENCES apartments(id),
            FOREIGN KEY(requested_apartment_id) REFERENCES apartments(id)
        );

-- Таблица: apartment_verification
CREATE TABLE apartment_verification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apartment_id INTEGER NOT NULL,
            apartment_number TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'new',
            comment TEXT,
            verified_by INTEGER,
            verified_at TEXT,
            created_at TEXT,
            updated_at TEXT,
            UNIQUE(apartment_id)
        );

-- Таблица: apartments
CREATE TABLE apartments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        apartment_number TEXT NOT NULL UNIQUE,
        entrance TEXT,
        entrance_source TEXT,
        total_area REAL,
        object_type TEXT,
        status TEXT DEFAULT 'active',
        source TEXT,
        notes TEXT,
        created_at TEXT,
        created_by TEXT,
        updated_at TEXT,
        updated_by TEXT
    , unit_type TEXT DEFAULT 'RESIDENTIAL', unit_code TEXT, entrance_number INTEGER, official_number TEXT, display_name TEXT, area_sqm REAL, record_status TEXT DEFAULT 'LEGACY', source_note TEXT, internal_note TEXT, unit_updated_at TEXT);

-- Таблица: audit_log
CREATE TABLE audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_time TEXT,
        username TEXT,
        table_name TEXT,
        record_id TEXT,
        action TEXT,
        field_name TEXT,
        old_value TEXT,
        new_value TEXT,
        comment TEXT
    , actor_role TEXT, actor_name TEXT, source TEXT DEFAULT 'bot', telegram_user_id INTEGER);

-- Таблица: bank_transactions
CREATE TABLE bank_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_ref TEXT UNIQUE,
            entry_status TEXT NOT NULL DEFAULT 'CONFIRMED',
            transaction_date TEXT NOT NULL,
            value_date TEXT,
            apartment_id INTEGER,
            apartment_number TEXT,
            period_code TEXT,
            service_code TEXT,
            service_item_code TEXT,
            amount REAL NOT NULL DEFAULT 0,
            currency TEXT NOT NULL DEFAULT 'UAH',
            payer_text TEXT,
            bank_name TEXT,
            source_type TEXT NOT NULL DEFAULT 'manual_operator',
            source_ref TEXT,
            payment_notice_id INTEGER,
            payment_id INTEGER,
            cashier_batch_id INTEGER,
            operator_id TEXT,
            operator_note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            FOREIGN KEY(apartment_id) REFERENCES apartments(id),
            FOREIGN KEY(payment_notice_id) REFERENCES payment_notices(id)
        );

-- Таблица: barrier_phone_access
CREATE TABLE barrier_phone_access (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apartment_number TEXT,
            contact_id INTEGER,
            phone_number TEXT,
            access_status TEXT NOT NULL DEFAULT 'ACTIVE',
            status_reason TEXT,
            blocked_by TEXT,
            blocked_at TEXT,
            unblocked_by TEXT,
            unblocked_at TEXT,
            debt_amount REAL DEFAULT 0,
            comment TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        , "service_order_id" INTEGER);

-- Таблица: bot_admins
CREATE TABLE bot_admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_user_id INTEGER UNIQUE,
        telegram_username TEXT,

        display_name TEXT,

        role TEXT DEFAULT 'viewer',

        can_read INTEGER DEFAULT 1,
        can_write INTEGER DEFAULT 0,
        can_manage_users INTEGER DEFAULT 0,
        can_manage_payments INTEGER DEFAULT 0,
        can_manage_bot INTEGER DEFAULT 0,

        is_active INTEGER DEFAULT 1,

        created_at TEXT,
        updated_at TEXT,

        notes TEXT
    );

-- Таблица: bot_user_sessions
CREATE TABLE bot_user_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_user_id INTEGER UNIQUE,

        current_state TEXT,
        context_json TEXT,

        updated_at TEXT
    );

-- Таблица: cashbox_operations
CREATE TABLE cashbox_operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation_date TEXT NOT NULL,
            cashbox_code TEXT NOT NULL,
            operation_type TEXT NOT NULL,
            direction TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT NOT NULL DEFAULT 'UAH',
            period_code TEXT,
            apartment_number TEXT,
            vehicle_id INTEGER,
            service_code TEXT,
            payment_id INTEGER,
            charge_id INTEGER,
            batch_id TEXT,
            source_type TEXT DEFAULT 'cashier_journal',
            source_ref TEXT,
            operator_id TEXT,
            actor_type TEXT DEFAULT 'operator',
            comment TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, service_item_code TEXT, base_service_code TEXT, service_type TEXT, "commercial_contract_id" INTEGER, "commercial_unit_id" INTEGER, "cashier_receipt_id" INTEGER, "transfer_group_ref" TEXT, "payment_notice_id" INTEGER, "cashier_batch_id" INTEGER,
            FOREIGN KEY (cashbox_code) REFERENCES cashboxes(cashbox_code),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
            FOREIGN KEY (payment_id) REFERENCES payments(id),
            FOREIGN KEY (charge_id) REFERENCES charges(id)
        );

-- Таблица: cashboxes
CREATE TABLE cashboxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cashbox_code TEXT NOT NULL UNIQUE,
            cashbox_name TEXT NOT NULL,
            currency TEXT NOT NULL DEFAULT 'UAH',
            initial_balance REAL NOT NULL DEFAULT 0,
            current_balance REAL NOT NULL DEFAULT 0,
            is_active INTEGER NOT NULL DEFAULT 1,
            comment TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );

-- Таблица: cashier_batch_items
CREATE TABLE cashier_batch_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id INTEGER NOT NULL,
            apartment_id INTEGER,
            apartment_number TEXT NOT NULL,
            charge_id INTEGER,
            receipt_id INTEGER,
            payment_id INTEGER,
            amount_expected REAL,
            amount_received REAL NOT NULL DEFAULT 0,
            cashbox_code TEXT,
            period_code TEXT,
            service_code TEXT,
            service_item_code TEXT,
            item_status TEXT NOT NULL DEFAULT 'PENDING',
            exception_note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            FOREIGN KEY(batch_id) REFERENCES cashier_batches(id),
            FOREIGN KEY(apartment_id) REFERENCES apartments(id)
        );

-- Таблица: cashier_batches
CREATE TABLE cashier_batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT NOT NULL UNIQUE,
            batch_type TEXT NOT NULL,
            period_code TEXT,
            cashbox_code TEXT,
            service_code TEXT,
            default_amount REAL,
            default_tariff TEXT,
            operator_id TEXT,
            actor_type TEXT DEFAULT 'operator',
            total_rows INTEGER DEFAULT 0,
            total_amount REAL DEFAULT 0,
            comment TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            applied_at TEXT,
            batch_status TEXT DEFAULT 'draft', "batch_number" TEXT, "batch_kind" TEXT, "entry_status" TEXT NOT NULL DEFAULT 'DRAFT', "entrance_number" TEXT, "service_item_code" TEXT, "receipt_date" TEXT, "included_count" INTEGER NOT NULL DEFAULT 0, "excluded_count" INTEGER NOT NULL DEFAULT 0, "currency" TEXT NOT NULL DEFAULT 'UAH', "source_text" TEXT, "confirmed_at" TEXT, "voided_at" TEXT, "void_reason" TEXT, "updated_at" TEXT,
            FOREIGN KEY (cashbox_code) REFERENCES cashboxes(cashbox_code)
        );

-- Таблица: cashier_receipts
CREATE TABLE cashier_receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_number TEXT NOT NULL UNIQUE,
            receipt_kind TEXT NOT NULL,
            entry_status TEXT NOT NULL DEFAULT 'DRAFT',
            cashbox_code TEXT,
            receipt_date TEXT NOT NULL,
            document_date TEXT,
            origin_kind TEXT NOT NULL DEFAULT 'HAND_TO_HAND',
            origin_cashbox_code TEXT,
            payer_name TEXT,
            apartment_id INTEGER,
            apartment_number TEXT,
            service_hint TEXT,
            period_code TEXT,
            amount REAL NOT NULL DEFAULT 0,
            currency TEXT NOT NULL DEFAULT 'UAH',
            evidence_type TEXT NOT NULL DEFAULT 'ORAL',
            paper_ref TEXT,
            source_text TEXT,
            designation_status TEXT NOT NULL DEFAULT 'UNSPECIFIED',
            allocation_status TEXT NOT NULL DEFAULT 'NOT_APPLICABLE',
            payment_id INTEGER,
            cashbox_operation_id INTEGER,
            void_payment_id INTEGER,
            void_cashbox_operation_id INTEGER,
            operator_id TEXT,
            confirmed_by TEXT,
            confirmed_at TEXT,
            voided_by TEXT,
            voided_at TEXT,
            void_reason TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        , "payment_notice_id" INTEGER, "cashier_batch_id" INTEGER, "service_item_code" TEXT, "review_status" TEXT);

-- Таблица: cashier_reconciliation_cases
CREATE TABLE cashier_reconciliation_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT NOT NULL,
            case_status TEXT NOT NULL DEFAULT 'OPEN',
            priority TEXT NOT NULL DEFAULT 'NORMAL',
            apartment_id INTEGER,
            apartment_number TEXT,
            amount REAL,
            currency TEXT NOT NULL DEFAULT 'UAH',
            period_code TEXT,
            service_code TEXT,
            related_payment_id INTEGER,
            related_receipt_id INTEGER,
            related_notice_id INTEGER,
            related_bank_transaction_id INTEGER,
            related_batch_id INTEGER,
            description TEXT NOT NULL,
            operator_id TEXT,
            resolution_note TEXT,
            resolved_at TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );

-- Таблица: cashier_settings
CREATE TABLE cashier_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );

-- Таблица: charge_adjustments
CREATE TABLE charge_adjustments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            charge_id INTEGER NOT NULL,
            adjustment_assignment_id INTEGER,
            adjustment_code TEXT NOT NULL,
            adjustment_type TEXT NOT NULL,
            calculation_kind TEXT NOT NULL,
            applied_amount REAL NOT NULL,
            public_note TEXT,
            internal_note TEXT,
            reason_snapshot TEXT,
            applied_by TEXT,
            source_context TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (charge_id) REFERENCES charges(id),
            FOREIGN KEY (adjustment_assignment_id) REFERENCES adjustment_assignments(id)
        );

-- Таблица: charges
CREATE TABLE charges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        period_code TEXT NOT NULL,
        apartment_number TEXT NOT NULL,
        vehicle_id INTEGER,
        service_code TEXT NOT NULL,
        quantity REAL NOT NULL DEFAULT 1,
        unit_price REAL NOT NULL,
        amount REAL NOT NULL,
        currency TEXT NOT NULL DEFAULT 'UAH',
        status TEXT NOT NULL DEFAULT 'unpaid',
        source TEXT,
        created_by TEXT,
        comment TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP, service_item_code TEXT, base_service_code TEXT, service_type TEXT, gross_amount REAL, adjustment_amount REAL NOT NULL DEFAULT 0, net_amount REAL, adjustment_public_note TEXT, adjustment_internal_note TEXT, adjustment_updated_at TEXT, "commercial_contract_id" INTEGER, "commercial_contract_item_id" INTEGER, "commercial_due_date" TEXT,
        FOREIGN KEY(vehicle_id)
            REFERENCES vehicles(id),
        FOREIGN KEY(service_code)
            REFERENCES service_catalog(service_code)
    );

-- Таблица: commercial_access_actions
CREATE TABLE commercial_access_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER NOT NULL,
                access_phone_id INTEGER,
                notification_id INTEGER,
                action_type TEXT NOT NULL,
                action_status TEXT NOT NULL DEFAULT 'OPEN',
                debt_amount_snapshot REAL NOT NULL DEFAULT 0,
                days_overdue_snapshot INTEGER NOT NULL DEFAULT 0,
                reason TEXT,
                operator_id TEXT,
                performed_at TEXT,
                comment TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                FOREIGN KEY(contract_id) REFERENCES commercial_contracts(id),
                FOREIGN KEY(access_phone_id) REFERENCES commercial_access_phones(id),
                FOREIGN KEY(notification_id) REFERENCES commercial_notifications(id)
            );

-- Таблица: commercial_access_phones
CREATE TABLE commercial_access_phones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER NOT NULL,
                phone_normalized TEXT NOT NULL,
                phone_display TEXT,
                access_purpose TEXT NOT NULL DEFAULT 'STAFF',
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                status_reason TEXT,
                status_changed_at TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                FOREIGN KEY(contract_id) REFERENCES commercial_contracts(id)
            );

-- Таблица: commercial_contract_items
CREATE TABLE commercial_contract_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER NOT NULL,
                item_code TEXT,
                item_name TEXT NOT NULL,
                reference_service_code TEXT,
                calculation_mode TEXT NOT NULL DEFAULT 'FIXED_MONTHLY',
                fixed_amount REAL,
                rate_amount REAL,
                quantity_default REAL NOT NULL DEFAULT 1,
                currency TEXT NOT NULL DEFAULT 'UAH',
                blocks_phone_access_on_debt INTEGER NOT NULL DEFAULT 0,
                is_active INTEGER NOT NULL DEFAULT 1,
                valid_from TEXT,
                valid_to TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                FOREIGN KEY(contract_id) REFERENCES commercial_contracts(id)
            );

-- Таблица: commercial_contract_recipients
CREATE TABLE commercial_contract_recipients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER NOT NULL,
                resident_account_id INTEGER,
                telegram_user_id TEXT,
                recipient_name TEXT,
                recipient_role TEXT NOT NULL DEFAULT 'REPRESENTATIVE',
                is_primary INTEGER NOT NULL DEFAULT 0,
                notification_enabled INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                FOREIGN KEY(contract_id) REFERENCES commercial_contracts(id),
                FOREIGN KEY(resident_account_id) REFERENCES resident_accounts(id)
            );

-- Таблица: commercial_contracts
CREATE TABLE commercial_contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unit_id INTEGER NOT NULL,
                contract_number TEXT,
                counterparty_type TEXT NOT NULL DEFAULT 'UNKNOWN',
                counterparty_name TEXT,
                status TEXT NOT NULL DEFAULT 'DRAFT',
                valid_from TEXT,
                valid_to TEXT,
                payment_due_day INTEGER NOT NULL DEFAULT 10,
                grace_days INTEGER NOT NULL DEFAULT 0,
                reminder_days_before_due INTEGER NOT NULL DEFAULT 3,
                warning_days_overdue INTEGER NOT NULL DEFAULT 3,
                suspension_candidate_days_overdue INTEGER NOT NULL DEFAULT 7,
                internal_note TEXT,
                created_by TEXT,
                updated_by TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                FOREIGN KEY(unit_id) REFERENCES apartments(id)
            );

-- Таблица: commercial_notifications
CREATE TABLE commercial_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER NOT NULL,
                recipient_id INTEGER,
                telegram_user_id TEXT,
                notification_type TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'DRAFT',
                dedupe_key TEXT NOT NULL,
                charge_ids_json TEXT,
                debt_amount_snapshot REAL NOT NULL DEFAULT 0,
                days_overdue_snapshot INTEGER NOT NULL DEFAULT 0,
                message_text TEXT NOT NULL,
                created_by TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                sent_at TEXT,
                failed_at TEXT,
                delivery_error TEXT,
                cancelled_at TEXT,
                cancelled_by TEXT,
                FOREIGN KEY(contract_id) REFERENCES commercial_contracts(id),
                FOREIGN KEY(recipient_id) REFERENCES commercial_contract_recipients(id)
            );

-- Таблица: contact_methods
CREATE TABLE contact_methods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        apartment_id INTEGER,
        person_id INTEGER,
        contact_type TEXT,
        contact_value TEXT,
        telegram_user_id TEXT,
        telegram_username TEXT,
        contact_owner TEXT,
        is_primary INTEGER DEFAULT 0,
        source TEXT,
        notes TEXT,
        created_at TEXT,
        created_by TEXT,
        updated_at TEXT,
        updated_by TEXT,
        FOREIGN KEY(apartment_id) REFERENCES apartments(id),
        FOREIGN KEY(person_id) REFERENCES persons(id)
    );

-- Таблица: events
CREATE TABLE events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        apartment_id INTEGER,
        event_time TEXT,
        event_group TEXT,
        event_type TEXT,
        amount REAL,
        status TEXT,
        source TEXT,
        related_table TEXT,
        related_record_id TEXT,
        file_path TEXT,
        comment TEXT,
        created_at TEXT,
        created_by TEXT,
        FOREIGN KEY(apartment_id) REFERENCES apartments(id)
    );

-- Таблица: extracted_facts
CREATE TABLE extracted_facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        raw_message_id INTEGER,
        apartment_number TEXT,
        fact_type TEXT,
        amount REAL,
        fact_date TEXT,
        confidence REAL,
        status TEXT DEFAULT 'new',
        comment TEXT,
        FOREIGN KEY(raw_message_id) REFERENCES raw_messages(id)
    );

-- Таблица: message_sources
CREATE TABLE message_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_type TEXT,
        source_name TEXT,
        source_id TEXT,
        notes TEXT
    );

-- Таблица: operator_audit_log
CREATE TABLE operator_audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            operator_id TEXT,
            user_id TEXT,
            actor_type TEXT,
            action_type TEXT,
            table_name TEXT,
            row_id TEXT,
            field_name TEXT,
            old_value TEXT,
            new_value TEXT,
            action_status TEXT DEFAULT 'applied',
            review_status TEXT DEFAULT 'pending',
            source_context TEXT,
            comment TEXT
        , db_mode TEXT, db_file TEXT, reviewed_by TEXT, reviewed_at TEXT, review_comment TEXT, extra_json TEXT);

-- Таблица: operator_task_queue
CREATE TABLE operator_task_queue (
id INTEGER PRIMARY KEY AUTOINCREMENT,
task_number TEXT UNIQUE,
priority TEXT NOT NULL DEFAULT 'NORMAL',
task_type TEXT NOT NULL,
status TEXT NOT NULL DEFAULT 'PENDING',
apartment_number TEXT,
vehicle_id INTEGER,
plate TEXT,
telegram_user_id TEXT,
title TEXT,
description TEXT,
origin TEXT NOT NULL DEFAULT 'SYSTEM',
created_by TEXT,
assigned_to TEXT,
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TEXT,
closed_at TEXT,
close_note TEXT
);

-- Таблица: parking_time_review_tasks
CREATE TABLE parking_time_review_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        apartment_number TEXT,

        vehicle_id INTEGER,
        license_plate TEXT,
        car_model TEXT,

        current_parking_time TEXT,

        suggested_day_count INTEGER,
        suggested_night_count INTEGER,

        task_type TEXT,
        priority INTEGER DEFAULT 50,

        source_name TEXT,
        source_details TEXT,

        status TEXT DEFAULT 'new',

        created_at TEXT,
        created_by TEXT,

        reviewed_at TEXT,
        reviewed_by TEXT,

        decision TEXT,
        decision_comment TEXT
    );

-- Таблица: payment_allocations
CREATE TABLE payment_allocations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_id INTEGER NOT NULL,
        charge_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP, service_item_code TEXT, base_service_code TEXT, service_type TEXT,
        FOREIGN KEY(payment_id)
            REFERENCES payments(id),
        FOREIGN KEY(charge_id)
            REFERENCES charges(id)
    );

-- Таблица: payment_notices
CREATE TABLE payment_notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            notice_number TEXT NOT NULL UNIQUE,
            notice_type TEXT NOT NULL,
            notice_status TEXT NOT NULL DEFAULT 'NEW',
            resident_account_id INTEGER NOT NULL,
            telegram_user_id TEXT NOT NULL,
            apartment_id INTEGER,
            apartment_number TEXT,
            declared_cashbox_code TEXT,
            declared_period_code TEXT,
            declared_service_code TEXT,
            declared_service_item_code TEXT,
            declared_amount REAL NOT NULL DEFAULT 0,
            currency TEXT NOT NULL DEFAULT 'UAH',
            declared_at TEXT NOT NULL,
            resident_comment TEXT,
            evidence_text TEXT,
            matched_cashier_receipt_id INTEGER,
            matched_bank_transaction_id INTEGER,
            matched_payment_id INTEGER,
            operator_id TEXT,
            operator_note TEXT,
            reviewed_at TEXT,
            confirmed_at TEXT,
            rejected_at TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            FOREIGN KEY(resident_account_id) REFERENCES resident_accounts(id),
            FOREIGN KEY(apartment_id) REFERENCES apartments(id)
        );

-- Таблица: payments
CREATE TABLE payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_date TEXT,
        period_code TEXT,
        apartment_number TEXT NOT NULL,
        vehicle_id INTEGER,
        amount REAL NOT NULL,
        currency TEXT NOT NULL DEFAULT 'UAH',
        payment_method TEXT,
        source TEXT,
        created_by TEXT,
        comment TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP, cashbox_code TEXT, cashbox_operation_id INTEGER, cashier_batch_id TEXT, operator_id TEXT, service_item_code TEXT, base_service_code TEXT, service_type TEXT, "commercial_contract_id" INTEGER, "commercial_unit_id" INTEGER, "cashier_receipt_id" INTEGER, "cashier_entry_status" TEXT, "payment_notice_id" INTEGER, "bank_transaction_id" INTEGER, "payment_channel" TEXT, "apartment_id" INTEGER, "source_ref" TEXT,
        FOREIGN KEY(vehicle_id)
            REFERENCES vehicles(id)
    );

-- Таблица: persons
CREATE TABLE persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        apartment_id INTEGER,
        full_name TEXT,
        phone_raw TEXT,
        ownership_type TEXT,
        person_role TEXT,
        source TEXT,
        notes TEXT,
        created_at TEXT,
        created_by TEXT,
        updated_at TEXT,
        updated_by TEXT,
        FOREIGN KEY(apartment_id) REFERENCES apartments(id)
    );

-- Таблица: phone_access_request_points
CREATE TABLE phone_access_request_points (
            id INTEGER PRIMARY KEY,
            request_id INTEGER NOT NULL,
            access_point_code TEXT NOT NULL,
            access_point_name_snapshot TEXT NOT NULL,
            connect_tariff_version_id INTEGER,
            connect_unit_price_snapshot REAL NOT NULL CHECK(connect_unit_price_snapshot >= 0),
            monthly_tariff_version_id INTEGER,
            monthly_unit_price_snapshot REAL NOT NULL CHECK(monthly_unit_price_snapshot >= 0),
            currency TEXT NOT NULL DEFAULT 'UAH',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(request_id, access_point_code)
        );

-- Таблица: phone_access_requests
CREATE TABLE phone_access_requests (
            id INTEGER PRIMARY KEY,
            request_number TEXT NOT NULL UNIQUE,
            interest_id INTEGER NOT NULL UNIQUE,
            service_order_id INTEGER UNIQUE,
            resident_account_id INTEGER,
            telegram_user_id TEXT,
            apartment_id INTEGER,
            apartment_number TEXT NOT NULL,
            phone_normalized TEXT NOT NULL,
            request_status TEXT NOT NULL DEFAULT 'INTEREST'
                CHECK(request_status IN (
                    'INTEREST', 'PAID_ORDER_CREATED', 'ACTIVE', 'CANCELLED'
                )),
            parking_debt_check_mode TEXT NOT NULL DEFAULT 'MANUAL_REVIEW'
                CHECK(parking_debt_check_mode IN (
                    'CHECK_LINKED_PARKING_ACCOUNT',
                    'NOT_APPLICABLE_NO_PARKING',
                    'MANUAL_REVIEW'
                )),
            parking_debt_check_note TEXT,
            policy_version_id INTEGER,
            quoted_at TEXT NOT NULL,
            registered_at TEXT,
            first_charge_period TEXT,
            paid_at TEXT,
            cancelled_at TEXT,
            cancellation_reason TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

-- Таблица: phone_access_subscription_charges
CREATE TABLE phone_access_subscription_charges (
            id INTEGER PRIMARY KEY,
            charge_number TEXT NOT NULL UNIQUE,
            subscription_id INTEGER NOT NULL,
            subscription_point_id INTEGER,
            access_point_code TEXT NOT NULL,
            charge_kind TEXT NOT NULL
                CHECK(charge_kind IN ('CONNECT', 'MONTHLY')),
            charge_period_key TEXT NOT NULL,
            billing_period TEXT,
            tariff_code TEXT NOT NULL,
            tariff_version_id INTEGER,
            quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
            unit_price_snapshot REAL NOT NULL CHECK(unit_price_snapshot >= 0),
            amount_due_snapshot REAL NOT NULL CHECK(amount_due_snapshot >= 0),
            currency TEXT NOT NULL DEFAULT 'UAH',
            due_date TEXT,
            charge_status TEXT NOT NULL DEFAULT 'DRAFT'
                CHECK(charge_status IN (
                    'DRAFT', 'OPEN', 'PAID', 'OVERDUE', 'WAIVED', 'CANCELLED'
                )),
            service_order_id INTEGER,
            payment_notice_id INTEGER,
            payment_id INTEGER,
            posted_at TEXT,
            paid_at TEXT,
            cancelled_at TEXT,
            cancellation_reason TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(subscription_point_id, charge_kind, charge_period_key)
        );

-- Таблица: phone_access_subscription_points
CREATE TABLE phone_access_subscription_points (
            id INTEGER PRIMARY KEY,
            subscription_id INTEGER NOT NULL,
            access_point_code TEXT NOT NULL,
            access_point_name_snapshot TEXT NOT NULL,
            point_status TEXT NOT NULL DEFAULT 'PENDING_ACTIVATION'
                CHECK(point_status IN (
                    'PENDING_ACTIVATION', 'ACTIVE', 'SUSPENDED_FOR_DEBT',
                    'DEACTIVATED_FOR_DEBT', 'DEACTIVATED_MANUAL',
                    'EXTERNAL_SYNC_ERROR', 'CANCELLED'
                )),
            activated_at TEXT,
            deactivated_at TEXT,
            deactivation_reason TEXT,
            external_controller_reference TEXT,
            last_external_sync_status TEXT,
            last_external_sync_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(subscription_id, access_point_code)
        );

-- Таблица: phone_access_subscriptions
CREATE TABLE phone_access_subscriptions (
            id INTEGER PRIMARY KEY,
            subscription_number TEXT NOT NULL UNIQUE,
            resident_account_id INTEGER,
            authorised_person_id INTEGER,
            unit_id INTEGER,
            apartment_id INTEGER,
            apartment_number TEXT,
            holder_type TEXT NOT NULL DEFAULT 'RESIDENT'
                CHECK(holder_type IN ('RESIDENT', 'TENANT', 'AUTHORISED_PERSON')),
            phone_normalized TEXT NOT NULL,
            subscription_status TEXT NOT NULL DEFAULT 'PENDING_ACTIVATION'
                CHECK(subscription_status IN (
                    'PENDING_ACTIVATION', 'ACTIVE', 'PARTIALLY_ACTIVE',
                    'DEBT_WARNING', 'DEACTIVATING', 'DEACTIVATED_FOR_DEBT',
                    'DEACTIVATED_MANUAL', 'CLOSED', 'CANCELLED'
                )),
            parking_debt_check_mode TEXT NOT NULL DEFAULT 'MANUAL_REVIEW'
                CHECK(parking_debt_check_mode IN (
                    'CHECK_LINKED_PARKING_ACCOUNT',
                    'NOT_APPLICABLE_NO_PARKING',
                    'MANUAL_REVIEW'
                )),
            parking_debt_check_note TEXT,
            parking_debt_mode_set_by TEXT,
            parking_debt_mode_set_at TEXT,
            activation_date TEXT,
            first_charge_period TEXT,
            monthly_start_policy_version_id INTEGER,
            connect_tariff_version_id INTEGER,
            monthly_tariff_version_id INTEGER,
            created_from_order_id INTEGER,
            created_from_interest_id INTEGER,
            closed_at TEXT,
            close_reason TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

-- Таблица: phone_barrier_access_interest_points
CREATE TABLE phone_barrier_access_interest_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_access_interest_id INTEGER NOT NULL,
    access_point_code TEXT NOT NULL,
    access_point_name_snapshot TEXT,
    status TEXT NOT NULL DEFAULT 'REQUESTED',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

-- Таблица: phone_barrier_access_interests
CREATE TABLE phone_barrier_access_interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_interest_id INTEGER NOT NULL,
    requested_phone TEXT,
    parking_debt_check_mode TEXT,
    parking_debt_check_note TEXT,
    status TEXT NOT NULL DEFAULT 'NEW',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

-- Таблица: phone_barrier_access_order_points
CREATE TABLE phone_barrier_access_order_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_order_id INTEGER NOT NULL,
    access_point_code TEXT NOT NULL,
    access_point_name_snapshot TEXT,
    requested_phone TEXT,
    status TEXT NOT NULL DEFAULT 'PENDING_ACTIVATION',
    activated_at TEXT,
    deactivated_at TEXT,
    actor_id INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

-- Таблица: phone_barrier_access_points
CREATE TABLE phone_barrier_access_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    access_point_code TEXT NOT NULL UNIQUE,
    access_point_name_uk TEXT,
    access_point_name_ru TEXT,
    access_point_name_en TEXT,
    geos_access_point_id TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    sort_order INTEGER NOT NULL DEFAULT 100,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

-- Таблица: profile_parking_time_test_events
CREATE TABLE profile_parking_time_test_events (
            id INTEGER PRIMARY KEY,
            event_number TEXT NOT NULL UNIQUE,
            session_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            actor_id TEXT,
            payload_json TEXT,
            created_at TEXT NOT NULL
        );

-- Таблица: profile_parking_time_test_schema_migrations
CREATE TABLE profile_parking_time_test_schema_migrations (
            migration_code TEXT PRIMARY KEY,
            schema_version TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            applied_by TEXT,
            sandbox_db_path TEXT,
            note TEXT
        );

-- Таблица: profile_parking_time_test_sessions
CREATE TABLE profile_parking_time_test_sessions (
            id INTEGER PRIMARY KEY,
            session_number TEXT NOT NULL UNIQUE,
            test_scope TEXT NOT NULL DEFAULT 'PARKING_TIME_NO_WRITE',
            target_apartment_id INTEGER,
            target_apartment_number TEXT NOT NULL,
            target_vehicle_id INTEGER NOT NULL,
            plate_snapshot TEXT,
            model_snapshot TEXT,
            color_snapshot TEXT,
            original_parking_time_snapshot TEXT,
            proposed_parking_time TEXT,
            test_status TEXT NOT NULL
                CHECK(test_status IN (
                    'OPEN',
                    'PENDING_OPERATOR',
                    'APPROVED_TEST_NO_WRITE',
                    'REJECTED_TEST_NO_WRITE',
                    'CLOSED_TEST_NO_WRITE'
                )),
            opened_by TEXT NOT NULL,
            opened_at TEXT NOT NULL,
            proposed_by TEXT,
            proposed_at TEXT,
            reviewed_by TEXT,
            reviewed_at TEXT,
            review_note TEXT,
            close_reason TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

-- Таблица: raw_messages
CREATE TABLE raw_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER,
        message_datetime TEXT,
        sender_name TEXT,
        sender_username TEXT,
        sender_user_id TEXT,
        message_text TEXT,
        has_photo INTEGER DEFAULT 0,
        file_path TEXT,
        imported_at TEXT,
        processed_status TEXT DEFAULT 'new',
        FOREIGN KEY(source_id) REFERENCES message_sources(id)
    );

-- Таблица: remote_asset_movements
CREATE TABLE remote_asset_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remote_asset_id INTEGER NOT NULL,
                service_order_id INTEGER,
                movement_type TEXT NOT NULL,
                from_state TEXT,
                to_state TEXT,
                apartment_id INTEGER,
                apartment_number TEXT,
                post_code TEXT,
                actor_id TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

-- Таблица: remote_assets
CREATE TABLE remote_assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_number TEXT NOT NULL UNIQUE,
                asset_type TEXT NOT NULL DEFAULT 'REMOTE',
                ownership_type TEXT NOT NULL,
                inventory_status TEXT NOT NULL DEFAULT 'AVAILABLE',
                condition_status TEXT NOT NULL DEFAULT 'UNKNOWN',
                hardware_model TEXT,
                serial_number TEXT,
                programming_identifier TEXT,
                apartment_id INTEGER,
                apartment_number TEXT,
                received_at TEXT,
                issued_at TEXT,
                retired_at TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );

-- Таблица: remote_handover_events
CREATE TABLE remote_handover_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_kind TEXT NOT NULL,
            event_status TEXT NOT NULL DEFAULT 'CONFIRMED',
            post_code TEXT NOT NULL DEFAULT 'O',
            remote_request_id INTEGER,
            apartment_id INTEGER,
            apartment_number TEXT,
            quantity INTEGER NOT NULL DEFAULT 1,
            operator_id TEXT NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        , "service_order_id" INTEGER, "remote_asset_id" INTEGER, "remote_asset_movement_id" INTEGER);

-- Таблица: remote_order_details
CREATE TABLE remote_order_details (
                service_order_id INTEGER PRIMARY KEY,
                resident_asset_id INTEGER,
                issued_asset_id INTEGER,
                remote_owner_mode TEXT NOT NULL DEFAULT 'NONE',
                reprogramming_required INTEGER NOT NULL DEFAULT 0,
                inventory_asset_required INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );

-- Таблица: remote_order_issued_assets
CREATE TABLE remote_order_issued_assets (
                id INTEGER PRIMARY KEY,
                service_order_id INTEGER NOT NULL,
                remote_asset_id INTEGER NOT NULL,
                supplier_batch_id INTEGER NOT NULL,
                issued_at TEXT NOT NULL,
                issued_by TEXT,
                note TEXT,
                UNIQUE(service_order_id, remote_asset_id)
            );

-- Таблица: remote_requests
CREATE TABLE remote_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident_account_id INTEGER NOT NULL,
            telegram_user_id TEXT NOT NULL,
            apartment_id INTEGER NOT NULL,
            apartment_number TEXT NOT NULL,
            request_kind TEXT NOT NULL DEFAULT 'FIRST',
            quantity INTEGER NOT NULL DEFAULT 1,
            resident_comment TEXT,
            status TEXT NOT NULL DEFAULT 'NEW',
            operator_id TEXT,
            operator_note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            reviewed_at TEXT,
            issued_at TEXT,
            closed_at TEXT, "service_order_id" INTEGER,
            FOREIGN KEY(resident_account_id) REFERENCES resident_accounts(id),
            FOREIGN KEY(apartment_id) REFERENCES apartments(id)
        );

-- Таблица: remote_supplier_batch_links
CREATE TABLE remote_supplier_batch_links (
                id INTEGER PRIMARY KEY,
                supplier_batch_id INTEGER NOT NULL,
                service_order_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                issued_quantity INTEGER NOT NULL DEFAULT 0 CHECK(issued_quantity >= 0),
                link_status TEXT NOT NULL DEFAULT 'PLANNED',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(supplier_batch_id, service_order_id)
            );

-- Таблица: remote_supplier_batches
CREATE TABLE remote_supplier_batches (
                id INTEGER PRIMARY KEY,
                batch_number TEXT NOT NULL UNIQUE,
                service_item_code TEXT NOT NULL,
                service_name_snapshot TEXT NOT NULL,
                quantity_requested INTEGER NOT NULL CHECK(quantity_requested > 0),
                quantity_received INTEGER NOT NULL DEFAULT 0 CHECK(quantity_received >= 0),
                quantity_issued INTEGER NOT NULL DEFAULT 0 CHECK(quantity_issued >= 0),
                batch_status TEXT NOT NULL DEFAULT 'DRAFT',
                supplier_name TEXT,
                supplier_reference TEXT,
                created_by TEXT,
                ordered_at TEXT,
                received_at TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                note TEXT
            );

-- Таблица: resident_access_accounts
CREATE TABLE resident_access_accounts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
telegram_user_id TEXT UNIQUE NOT NULL,
telegram_username TEXT,
resident_id INTEGER,
apartment_number TEXT,
role TEXT NOT NULL DEFAULT 'resident',
status TEXT NOT NULL DEFAULT 'ACTIVE',
confirmed_by_admin_id TEXT,
confirmed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
notes TEXT
);

-- Таблица: resident_accounts
CREATE TABLE resident_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_user_id INTEGER UNIQUE,
        telegram_username TEXT,

        telegram_first_name TEXT,
        telegram_last_name TEXT,

        apartment_id INTEGER,
        apartment_number TEXT,

        role TEXT DEFAULT 'resident',
        status TEXT DEFAULT 'new',

        language_code TEXT DEFAULT 'ru',

        created_at TEXT,
        updated_at TEXT,
        verified_at TEXT,
        last_seen_at TEXT,

        notes TEXT,

        FOREIGN KEY(apartment_id) REFERENCES apartments(id)
    );

-- Таблица: resident_invitations
CREATE TABLE resident_invitations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
invitation_code TEXT UNIQUE,
apartment_number TEXT NOT NULL,
expected_full_name TEXT,
expected_phone TEXT,
status TEXT NOT NULL DEFAULT 'INVITED',
created_by_admin_id TEXT,
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
accepted_by_telegram_id TEXT,
accepted_at TEXT,
notes TEXT
);

-- Таблица: resident_profile_change_requests
CREATE TABLE resident_profile_change_requests (
            id INTEGER PRIMARY KEY,
            request_number TEXT NOT NULL UNIQUE,
            resident_account_id INTEGER NOT NULL,
            apartment_id INTEGER,
            apartment_number TEXT,
            vehicle_id INTEGER,
            request_type TEXT NOT NULL
                CHECK(request_type IN ('PARKING_TIME', 'GENERAL_CORRECTION')),
            current_value_json TEXT,
            requested_value_json TEXT NOT NULL,
            resident_note TEXT,
            request_status TEXT NOT NULL DEFAULT 'PENDING_OPERATOR'
                CHECK(request_status IN (
                    'PENDING_OPERATOR', 'APPROVED', 'REJECTED',
                    'ACCEPTED_MANUAL', 'CANCELLED'
                )),
            submitted_at TEXT NOT NULL,
            resolved_at TEXT,
            resolved_by TEXT,
            resolution_note TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

-- Таблица: resident_profile_operation_journal
CREATE TABLE resident_profile_operation_journal (
            id INTEGER PRIMARY KEY,
            event_number TEXT NOT NULL UNIQUE,
            resident_account_id INTEGER,
            apartment_id INTEGER,
            apartment_number TEXT,
            request_id INTEGER,
            event_type TEXT NOT NULL,
            actor_id TEXT,
            payload_json TEXT,
            created_at TEXT NOT NULL
        );

-- Таблица: resident_profile_policy_values
CREATE TABLE resident_profile_policy_values (
            id INTEGER PRIMARY KEY,
            policy_version_id INTEGER NOT NULL,
            setting_code TEXT NOT NULL,
            value_type TEXT NOT NULL
                CHECK(value_type IN ('TEXT', 'INTEGER', 'BOOLEAN', 'JSON')),
            value_text TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(policy_version_id, setting_code)
        );

-- Таблица: resident_profile_policy_versions
CREATE TABLE resident_profile_policy_versions (
            id INTEGER PRIMARY KEY,
            policy_set_code TEXT NOT NULL,
            version_number INTEGER NOT NULL CHECK(version_number > 0),
            policy_status TEXT NOT NULL DEFAULT 'ACTIVE'
                CHECK(policy_status IN ('DRAFT', 'ACTIVE', 'RETIRED', 'ARCHIVED')),
            effective_from TEXT NOT NULL,
            effective_to TEXT,
            approved_by TEXT,
            approval_reference TEXT,
            change_reason TEXT,
            created_by TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(policy_set_code, version_number),
            UNIQUE(policy_set_code, effective_from)
        );

-- Таблица: resident_profile_schema_migrations
CREATE TABLE resident_profile_schema_migrations (
            migration_code TEXT PRIMARY KEY,
            schema_version TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            applied_by TEXT,
            sandbox_db_path TEXT,
            note TEXT
        );

-- Таблица: resident_profile_verifications
CREATE TABLE resident_profile_verifications (
            id INTEGER PRIMARY KEY,
            resident_account_id INTEGER NOT NULL UNIQUE,
            apartment_id INTEGER,
            apartment_number TEXT,
            verification_status TEXT NOT NULL DEFAULT 'NEEDS_REVIEW'
                CHECK(verification_status IN (
                    'NEEDS_REVIEW', 'READY', 'PENDING_OPERATOR', 'ARCHIVED'
                )),
            no_vehicle_declared INTEGER NOT NULL DEFAULT 0 CHECK(no_vehicle_declared IN (0, 1)),
            no_vehicle_declared_at TEXT,
            no_vehicle_declared_by TEXT,
            resident_confirmed_at TEXT,
            resident_confirmed_by TEXT,
            verified_snapshot_hash TEXT,
            last_snapshot_hash TEXT,
            parking_debt_check_mode TEXT NOT NULL DEFAULT 'MANUAL_REVIEW'
                CHECK(parking_debt_check_mode IN (
                    'CHECK_LINKED_PARKING_ACCOUNT',
                    'NOT_APPLICABLE_NO_PARKING',
                    'MANUAL_REVIEW'
                )),
            welcome_shown_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

-- Таблица: resident_verification_requests
CREATE TABLE resident_verification_requests (
id INTEGER PRIMARY KEY AUTOINCREMENT,
request_number TEXT UNIQUE,
invitation_id INTEGER,
telegram_user_id TEXT NOT NULL,
telegram_username TEXT,
apartment_number TEXT,
claimed_full_name TEXT,
claimed_phone TEXT,
resident_says_ok INTEGER NOT NULL DEFAULT 0,
status TEXT NOT NULL DEFAULT 'PENDING_ADMIN_CONFIRMATION',
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
reviewed_by_admin_id TEXT,
reviewed_at TEXT,
review_note TEXT,
FOREIGN KEY(invitation_id) REFERENCES resident_invitations(id)
);

-- Таблица: schema_info
CREATE TABLE schema_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        schema_version TEXT NOT NULL,
        created_at TEXT NOT NULL,
        comment TEXT
    );

-- Таблица: service_access_credentials
CREATE TABLE service_access_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_order_id INTEGER,
                credential_kind TEXT NOT NULL,
                credential_value TEXT NOT NULL,
                access_scope TEXT NOT NULL DEFAULT 'BARRIER',
                credential_status TEXT NOT NULL DEFAULT 'REQUESTED',
                external_reference TEXT,
                apartment_id INTEGER,
                apartment_number TEXT,
                activated_by TEXT,
                activated_at TEXT,
                disabled_at TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );

-- Таблица: service_catalog
CREATE TABLE service_catalog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_code TEXT NOT NULL UNIQUE,
        service_group TEXT NOT NULL,
        service_name TEXT NOT NULL,
        unit TEXT NOT NULL,
        is_active INTEGER NOT NULL DEFAULT 1,
        comment TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    , service_type TEXT, category TEXT, is_monthly INTEGER NOT NULL DEFAULT 0, is_fundraising INTEGER NOT NULL DEFAULT 0, is_commercial INTEGER NOT NULL DEFAULT 0, is_access_control INTEGER NOT NULL DEFAULT 0, is_cash_collectable INTEGER NOT NULL DEFAULT 1, access_policy_enabled INTEGER NOT NULL DEFAULT 0, access_policy_scope TEXT NOT NULL DEFAULT 'NONE', access_policy_mode TEXT NOT NULL DEFAULT 'NONE', access_policy_message TEXT, manual_review_required INTEGER NOT NULL DEFAULT 0, policy_updated_at TEXT, policy_updated_by TEXT);

-- Таблица: service_interests
CREATE TABLE service_interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    interest_number TEXT,
    resident_account_id INTEGER,
    telegram_user_id INTEGER,
    apartment_id INTEGER,
    apartment_number TEXT,
    service_code TEXT,
    service_item_code TEXT,
    service_name_snapshot TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price_snapshot REAL NOT NULL DEFAULT 0,
    amount_due_snapshot REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'UAH',
    status TEXT NOT NULL DEFAULT 'NEW',
    source_context TEXT,
    resident_comment TEXT,
    operator_comment TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

-- Таблица: service_item_workflows
CREATE TABLE service_item_workflows (
                service_item_code TEXT PRIMARY KEY,
                workflow_profile_code TEXT NOT NULL,
                resident_request_enabled INTEGER NOT NULL DEFAULT 0,
                operator_create_enabled INTEGER NOT NULL DEFAULT 1,
                requires_charge INTEGER NOT NULL DEFAULT 1,
                payment_timing TEXT NOT NULL DEFAULT 'BEFORE_FULFILLMENT',
                inventory_mode TEXT NOT NULL DEFAULT 'NONE',
                resident_asset_mode TEXT NOT NULL DEFAULT 'NONE',
                is_active INTEGER NOT NULL DEFAULT 1,
                retired_at TEXT,
                retired_reason TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );

-- Таблица: service_items
CREATE TABLE service_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_item_code TEXT NOT NULL UNIQUE,
            service_code TEXT NOT NULL,
            service_item_name TEXT NOT NULL,
            service_type TEXT NOT NULL,
            period_code TEXT,
            sequence_no INTEGER,
            amount_default REAL,
            currency TEXT NOT NULL DEFAULT 'UAH',
            date_from TEXT,
            date_to TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            is_active INTEGER NOT NULL DEFAULT 1,
            description TEXT,
            comment TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            FOREIGN KEY (service_code) REFERENCES service_catalog(service_code)
        );

-- Таблица: service_order_charge_links
CREATE TABLE service_order_charge_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_order_id INTEGER NOT NULL,
                charge_id INTEGER NOT NULL,
                linked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                linked_by TEXT,
                note TEXT,
                UNIQUE(service_order_id, charge_id)
            );

-- Таблица: service_order_events
CREATE TABLE service_order_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_order_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                actor_id TEXT,
                actor_role TEXT,
                source_context TEXT,
                details TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

-- Таблица: service_order_interests
CREATE TABLE service_order_interests (
                id INTEGER PRIMARY KEY,
                interest_number TEXT NOT NULL UNIQUE,
                resident_account_id INTEGER,
                telegram_user_id TEXT,
                apartment_id INTEGER,
                apartment_number TEXT NOT NULL,
                service_code TEXT,
                service_item_code TEXT NOT NULL,
                service_name_snapshot TEXT NOT NULL,
                workflow_profile_code TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_price_snapshot REAL NOT NULL,
                amount_due_snapshot REAL NOT NULL,
                currency TEXT NOT NULL DEFAULT 'UAH',
                interest_status TEXT NOT NULL DEFAULT 'INTEREST',
                payment_notice_id INTEGER,
                payment_notice_number TEXT,
                payment_id INTEGER,
                service_order_id INTEGER,
                resident_comment TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                paid_at TEXT
            );

-- Таблица: service_order_payment_links
CREATE TABLE service_order_payment_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_order_id INTEGER NOT NULL,
                payment_id INTEGER NOT NULL,
                amount REAL,
                linked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                linked_by TEXT,
                note TEXT,
                UNIQUE(service_order_id, payment_id)
            );

-- Таблица: service_order_steps
CREATE TABLE service_order_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_order_id INTEGER NOT NULL,
                step_code TEXT NOT NULL,
                step_name TEXT NOT NULL,
                step_kind TEXT NOT NULL,
                sequence_no INTEGER NOT NULL DEFAULT 1,
                is_required INTEGER NOT NULL DEFAULT 1,
                step_status TEXT NOT NULL DEFAULT 'WAITING',
                confirmed_by TEXT,
                confirmed_at TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                UNIQUE(service_order_id, step_code)
            );

-- Таблица: service_orders
CREATE TABLE service_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT NOT NULL UNIQUE,
                resident_account_id INTEGER,
                telegram_user_id TEXT,
                apartment_id INTEGER,
                apartment_number TEXT NOT NULL,
                service_code TEXT,
                service_item_code TEXT NOT NULL,
                service_name_snapshot TEXT NOT NULL,
                workflow_profile_code TEXT NOT NULL,
                quantity REAL NOT NULL DEFAULT 1,
                unit_price_snapshot REAL,
                amount_due_snapshot REAL,
                currency TEXT NOT NULL DEFAULT 'UAH',
                order_status TEXT NOT NULL DEFAULT 'REQUESTED',
                payment_status TEXT NOT NULL DEFAULT 'NOT_REQUIRED',
                fulfillment_status TEXT NOT NULL DEFAULT 'NOT_STARTED',
                resident_comment TEXT,
                operator_comment TEXT,
                requested_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                completed_at TEXT,
                cancelled_at TEXT,
                cancelled_reason TEXT
            );

-- Таблица: service_price_versions
CREATE TABLE service_price_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_item_code TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL DEFAULT 'UAH',
                effective_from TEXT NOT NULL,
                effective_to TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_by TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                UNIQUE(service_item_code, effective_from)
            );

-- Таблица: service_tariffs
CREATE TABLE service_tariffs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_code TEXT NOT NULL,
        amount REAL NOT NULL,
        currency TEXT NOT NULL DEFAULT 'UAH',
        valid_from TEXT NOT NULL,
        valid_to TEXT,
        is_active INTEGER NOT NULL DEFAULT 1,
        comment TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(service_code)
            REFERENCES service_catalog(service_code)
    );

-- Таблица: service_workflow_profiles
CREATE TABLE service_workflow_profiles (
                profile_code TEXT PRIMARY KEY,
                profile_name TEXT NOT NULL,
                service_category TEXT NOT NULL,
                description TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );

-- Таблица: service_workflow_steps
CREATE TABLE service_workflow_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_code TEXT NOT NULL,
                step_code TEXT NOT NULL,
                step_name TEXT NOT NULL,
                step_kind TEXT NOT NULL,
                sequence_no INTEGER NOT NULL DEFAULT 1,
                is_required INTEGER NOT NULL DEFAULT 1,
                is_active INTEGER NOT NULL DEFAULT 1,
                description TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                UNIQUE(profile_code, step_code)
            );

-- Таблица: staff_principals
CREATE TABLE staff_principals (
            telegram_user_id TEXT PRIMARY KEY,
            display_name TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );

-- Таблица: tbot_parking_import
CREATE TABLE tbot_parking_import (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        ownership_type TEXT,
        ownership_type_raw TEXT,

        full_name TEXT,
        phone_raw TEXT,
        apartment_number TEXT,

        car_model TEXT,
        car_color TEXT,
        license_plate TEXT,
        status_raw TEXT,

        source TEXT,
        imported_at TEXT,
        imported_by TEXT,

        notes TEXT
    );

-- Таблица: unit_aliases
CREATE TABLE unit_aliases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apartment_id INTEGER NOT NULL,
            alias_text TEXT NOT NULL,
            alias_normalized TEXT NOT NULL,
            alias_kind TEXT NOT NULL DEFAULT 'SEARCH',
            is_active INTEGER NOT NULL DEFAULT 1,
            note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            FOREIGN KEY (apartment_id) REFERENCES apartments(id)
        );

-- Таблица: unit_contacts
CREATE TABLE unit_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apartment_id INTEGER NOT NULL,
            contact_name TEXT,
            contact_phone TEXT,
            contact_role TEXT NOT NULL DEFAULT 'PRIMARY',
            is_primary INTEGER NOT NULL DEFAULT 1,
            record_status TEXT NOT NULL DEFAULT 'DRAFT',
            note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            FOREIGN KEY(apartment_id) REFERENCES apartments(id)
        );

-- Таблица: unit_group_aliases
CREATE TABLE unit_group_aliases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            alias_text TEXT NOT NULL,
            alias_normalized TEXT NOT NULL,
            alias_kind TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            source_note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            UNIQUE(alias_normalized, is_active),
            FOREIGN KEY(group_id) REFERENCES unit_groups(id)
        );

-- Таблица: unit_group_members
CREATE TABLE unit_group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            apartment_id INTEGER NOT NULL,
            member_order INTEGER NOT NULL DEFAULT 1,
            member_role TEXT NOT NULL DEFAULT 'MEMBER',
            source_note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            UNIQUE(group_id, apartment_id),
            FOREIGN KEY(group_id) REFERENCES unit_groups(id),
            FOREIGN KEY(apartment_id) REFERENCES apartments(id)
        );

-- Таблица: unit_groups
CREATE TABLE unit_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_code TEXT NOT NULL UNIQUE,
            group_type TEXT NOT NULL DEFAULT 'COMPOSITE_LOOKUP',
            display_name TEXT,
            legal_status TEXT NOT NULL DEFAULT 'UNKNOWN',
            record_status TEXT NOT NULL DEFAULT 'LEGACY_LOOKUP',
            source_note TEXT,
            internal_note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );

-- Таблица: vehicles
CREATE TABLE vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        apartment_id INTEGER,
        license_plate TEXT,
        car_model TEXT,
        car_color TEXT,
        parking_time TEXT,
        status TEXT,
        source TEXT,
        notes TEXT,
        created_at TEXT,
        created_by TEXT,
        updated_at TEXT,
        updated_by TEXT, license_plate_normalized TEXT, plate_format_status TEXT, car_model_normalized TEXT, car_color_normalized TEXT,
        FOREIGN KEY(apartment_id) REFERENCES apartments(id)
    );

-- Таблица: verification_candidates
CREATE TABLE verification_candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        task_id INTEGER,

        candidate_type TEXT,
        candidate_value TEXT,
        candidate_normalized TEXT,

        confidence_label TEXT,
        confidence_score INTEGER,

        source_names TEXT,
        match_types TEXT,

        reason TEXT,
        status TEXT DEFAULT 'new',

        created_at TEXT,
        created_by TEXT,

        decided_at TEXT,
        decided_by TEXT,
        decision TEXT,
        decision_comment TEXT,

        FOREIGN KEY(task_id) REFERENCES verification_tasks(id)
    );

-- Таблица: verification_evidence
CREATE TABLE verification_evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        task_id INTEGER,

        source_name TEXT,
        source_db TEXT,
        source_table TEXT,
        source_record_id TEXT,

        evidence_type TEXT,
        evidence_value TEXT,
        normalized_value TEXT,
        match_type TEXT,

        comment TEXT,
        created_at TEXT,

        FOREIGN KEY(task_id) REFERENCES verification_tasks(id)
    );

-- Таблица: verification_log
CREATE TABLE verification_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        apartment_number TEXT,
        field_name TEXT,
        paper_value TEXT,
        bot_value TEXT,
        final_value TEXT,
        status TEXT,
        verified_by TEXT,
        verified_at TEXT,
        comment TEXT
    );

-- Таблица: verification_tasks
CREATE TABLE verification_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        apartment_id INTEGER,
        apartment_number TEXT,

        task_group TEXT,
        task_type TEXT,

        priority INTEGER DEFAULT 100,
        status TEXT DEFAULT 'new',

        source_name TEXT,
        source_record_id TEXT,

        object_table TEXT,
        object_id INTEGER,
        field_name TEXT,

        main_value TEXT,
        candidate_value TEXT,
        normalized_main_value TEXT,
        normalized_candidate_value TEXT,

        suggestion TEXT,
        comment TEXT,

        created_at TEXT,
        created_by TEXT,

        resolved_at TEXT,
        resolved_by TEXT,
        resolution TEXT,
        resolution_comment TEXT,

        FOREIGN KEY(apartment_id) REFERENCES apartments(id)
    );

-- ==========================================
-- ПРЕДСТАВЛЕНИЯ (VIEWS)
-- ==========================================

-- View: v_commercial_contract_charge_debt
CREATE VIEW v_commercial_contract_charge_debt AS
        SELECT
            c.id AS charge_id,
            c.commercial_contract_id,
            c.commercial_contract_item_id,
            c.commercial_due_date,
            c.amount AS charge_amount,
            COALESCE(SUM(pa."amount"), 0) AS allocated_amount,
            CASE
                WHEN c.amount - COALESCE(SUM(pa."amount"), 0) > 0
                THEN c.amount - COALESCE(SUM(pa."amount"), 0)
                ELSE 0
            END AS outstanding_amount,
            COALESCE(i.blocks_phone_access_on_debt, 0) AS blocks_phone_access_on_debt
        FROM charges c
        LEFT JOIN payment_allocations pa ON pa.charge_id = c.id
        LEFT JOIN commercial_contract_items i
          ON i.id = c.commercial_contract_item_id
        WHERE c.commercial_contract_id IS NOT NULL
        AND COALESCE(c."status", '') <> 'cancelled'
        GROUP BY c.id;

-- View: v_commercial_contract_debt_summary
CREATE VIEW v_commercial_contract_debt_summary AS
        SELECT
            d.commercial_contract_id,
            COALESCE(SUM(d.outstanding_amount), 0) AS outstanding_amount,
            COALESCE(SUM(
                CASE
                    WHEN d.blocks_phone_access_on_debt = 1
                    THEN d.outstanding_amount
                    ELSE 0
                END
            ), 0) AS access_blocking_outstanding_amount,
            MIN(
                CASE
                    WHEN d.outstanding_amount > 0
                    THEN d.commercial_due_date
                    ELSE NULL
                END
            ) AS first_open_due_date
        FROM v_commercial_contract_charge_debt d
        GROUP BY d.commercial_contract_id;

-- View: v_unit_group_registry
CREATE VIEW v_unit_group_registry AS
        SELECT
            g.id AS group_id,
            g.group_code,
            g.group_type,
            g.display_name,
            g.legal_status,
            g.record_status,
            (
                SELECT GROUP_CONCAT(a.apartment_number, ' + ')
                FROM unit_group_members gm
                JOIN apartments a ON a.id = gm.apartment_id
                WHERE gm.group_id = g.id
                ORDER BY gm.member_order
            ) AS members,
            (
                SELECT GROUP_CONCAT(ga.alias_text, ' | ')
                FROM unit_group_aliases ga
                WHERE ga.group_id = g.id
                  AND ga.is_active = 1
            ) AS aliases
        FROM unit_groups g;

-- ==========================================
-- ИНДЕКСЫ
-- ==========================================

-- Индекс: idx_access_audit_actor
CREATE INDEX idx_access_audit_actor ON access_audit_log(actor_telegram_user_id, created_at);

-- Индекс: idx_access_debt_warnings_due
CREATE INDEX idx_access_debt_warnings_due
        ON access_debt_warnings(warning_status, deactivate_due_at, subscription_id)
        ;

-- Индекс: idx_access_external_commands_queue
CREATE INDEX idx_access_external_commands_queue
        ON access_external_commands(command_status, retry_at, access_point_code, id)
        ;

-- Индекс: idx_access_operation_journal_point
CREATE INDEX idx_access_operation_journal_point
        ON access_operation_journal(subscription_point_id, created_at, id)
        ;

-- Индекс: idx_access_operation_journal_subscription
CREATE INDEX idx_access_operation_journal_subscription
        ON access_operation_journal(subscription_id, created_at, id)
        ;

-- Индекс: idx_access_points_active
CREATE INDEX idx_access_points_active
        ON access_points(is_active, point_status, access_point_code)
        ;

-- Индекс: idx_access_policy_lookup
CREATE INDEX idx_access_policy_lookup
        ON access_policy_versions(policy_set_code, policy_status, effective_from, effective_to)
        ;

-- Индекс: idx_access_policy_values_code
CREATE INDEX idx_access_policy_values_code
        ON access_policy_values(setting_code, policy_version_id)
        ;

-- Индекс: idx_access_role_permissions_role
CREATE INDEX idx_access_role_permissions_role ON access_role_permissions(role_code, resource, action, is_active);

-- Индекс: idx_access_tariff_lookup
CREATE INDEX idx_access_tariff_lookup
        ON access_tariff_versions(
            tariff_code, access_point_scope_code, version_status, effective_from, effective_to
        )
        ;

-- Индекс: idx_access_user_permissions_user
CREATE INDEX idx_access_user_permissions_user ON access_user_permissions(telegram_user_id, resource, action, is_active);

-- Индекс: idx_access_user_roles_user
CREATE INDEX idx_access_user_roles_user ON access_user_roles(telegram_user_id, is_active);

-- Индекс: idx_adjust_assign_apt
CREATE INDEX idx_adjust_assign_apt ON adjustment_assignments(apartment_number);

-- Индекс: idx_adjust_assign_code
CREATE INDEX idx_adjust_assign_code ON adjustment_assignments(adjustment_code);

-- Индекс: idx_adjust_assign_status_dates
CREATE INDEX idx_adjust_assign_status_dates ON adjustment_assignments(status, valid_from, valid_to);

-- Индекс: idx_adjust_assign_vehicle
CREATE INDEX idx_adjust_assign_vehicle ON adjustment_assignments(vehicle_id);

-- Индекс: idx_adjustment_catalog_active
CREATE INDEX idx_adjustment_catalog_active ON adjustment_catalog(is_active);

-- Индекс: idx_adjustment_catalog_type
CREATE INDEX idx_adjustment_catalog_type ON adjustment_catalog(adjustment_type);

-- Индекс: idx_apartment_link_requests_requested_unit
CREATE INDEX idx_apartment_link_requests_requested_unit
            ON apartment_link_requests(requested_apartment_id, status)
            ;

-- Индекс: idx_apartment_link_requests_resident
CREATE INDEX idx_apartment_link_requests_resident
            ON apartment_link_requests(resident_account_id, status, created_at)
            ;

-- Индекс: idx_apartment_link_requests_status
CREATE INDEX idx_apartment_link_requests_status
            ON apartment_link_requests(status, created_at)
            ;

-- Индекс: idx_apartment_verification_apartment_number
CREATE INDEX idx_apartment_verification_apartment_number
        ON apartment_verification(apartment_number)
    ;

-- Индекс: idx_apartment_verification_status
CREATE INDEX idx_apartment_verification_status
        ON apartment_verification(status)
    ;

-- Индекс: idx_apartments_unit_code_unique
CREATE UNIQUE INDEX idx_apartments_unit_code_unique
        ON apartments(unit_code)
        WHERE unit_code IS NOT NULL
          AND TRIM(unit_code) <> ''
    ;

-- Индекс: idx_audit_log_actor
CREATE INDEX idx_audit_log_actor
    ON audit_log(telegram_user_id)
    ;

-- Индекс: idx_audit_log_event_time
CREATE INDEX idx_audit_log_event_time
        ON audit_log(event_time)
        ;

-- Индекс: idx_audit_log_table_record
CREATE INDEX idx_audit_log_table_record
    ON audit_log(table_name, record_id)
    ;

-- Индекс: idx_bank_transactions_ref
CREATE INDEX idx_bank_transactions_ref
            ON bank_transactions(transaction_ref)
            ;

-- Индекс: idx_bank_transactions_unit
CREATE INDEX idx_bank_transactions_unit
            ON bank_transactions(apartment_id, apartment_number, transaction_date)
            ;

-- Индекс: idx_barrier_phone_access_apt
CREATE INDEX idx_barrier_phone_access_apt ON barrier_phone_access(apartment_number);

-- Индекс: idx_barrier_phone_access_phone
CREATE INDEX idx_barrier_phone_access_phone ON barrier_phone_access(phone_number);

-- Индекс: idx_barrier_phone_access_status
CREATE INDEX idx_barrier_phone_access_status ON barrier_phone_access(access_status);

-- Индекс: idx_bot_admins_active
CREATE INDEX idx_bot_admins_active
    ON bot_admins(is_active)
    ;

-- Индекс: idx_bot_admins_role
CREATE INDEX idx_bot_admins_role
    ON bot_admins(role)
    ;

-- Индекс: idx_bot_admins_telegram_user
CREATE INDEX idx_bot_admins_telegram_user
    ON bot_admins(telegram_user_id)
    ;

-- Индекс: idx_bot_user_sessions_user
CREATE INDEX idx_bot_user_sessions_user
    ON bot_user_sessions(telegram_user_id)
    ;

-- Индекс: idx_cashbox_operations_apt
CREATE INDEX idx_cashbox_operations_apt ON cashbox_operations(apartment_number);

-- Индекс: idx_cashbox_operations_base_service
CREATE INDEX idx_cashbox_operations_base_service ON cashbox_operations(base_service_code);

-- Индекс: idx_cashbox_operations_batch
CREATE INDEX idx_cashbox_operations_batch ON cashbox_operations(batch_id);

-- Индекс: idx_cashbox_operations_cashbox
CREATE INDEX idx_cashbox_operations_cashbox ON cashbox_operations(cashbox_code);

-- Индекс: idx_cashbox_operations_cashier_receipt
CREATE INDEX idx_cashbox_operations_cashier_receipt
            ON cashbox_operations(cashier_receipt_id)
            ;

-- Индекс: idx_cashbox_operations_commercial_contract
CREATE INDEX idx_cashbox_operations_commercial_contract
            ON cashbox_operations(commercial_contract_id, commercial_unit_id)
            ;

-- Индекс: idx_cashbox_operations_date
CREATE INDEX idx_cashbox_operations_date ON cashbox_operations(operation_date);

-- Индекс: idx_cashbox_operations_operator
CREATE INDEX idx_cashbox_operations_operator ON cashbox_operations(operator_id);

-- Индекс: idx_cashbox_operations_payment
CREATE INDEX idx_cashbox_operations_payment ON cashbox_operations(payment_id);

-- Индекс: idx_cashbox_operations_service_item
CREATE INDEX idx_cashbox_operations_service_item ON cashbox_operations(service_item_code);

-- Индекс: idx_cashbox_operations_service_type
CREATE INDEX idx_cashbox_operations_service_type ON cashbox_operations(service_type);

-- Индекс: idx_cashbox_operations_transfer_group
CREATE INDEX idx_cashbox_operations_transfer_group
            ON cashbox_operations(transfer_group_ref)
            ;

-- Индекс: idx_cashbox_operations_vehicle
CREATE INDEX idx_cashbox_operations_vehicle ON cashbox_operations(vehicle_id);

-- Индекс: idx_cashbox_ops_batch_v2
CREATE INDEX idx_cashbox_ops_batch_v2 ON cashbox_operations(cashier_batch_id);

-- Индекс: idx_cashboxes_active
CREATE INDEX idx_cashboxes_active ON cashboxes(is_active);

-- Индекс: idx_cashboxes_code
CREATE INDEX idx_cashboxes_code ON cashboxes(cashbox_code);

-- Индекс: idx_cashier_batch_items_batch
CREATE INDEX idx_cashier_batch_items_batch
            ON cashier_batch_items(batch_id, item_status)
            ;

-- Индекс: idx_cashier_batch_items_unit
CREATE INDEX idx_cashier_batch_items_unit
            ON cashier_batch_items(apartment_id, apartment_number, period_code)
            ;

-- Индекс: idx_cashier_batches_batch_id
CREATE INDEX idx_cashier_batches_batch_id ON cashier_batches(batch_id);

-- Индекс: idx_cashier_batches_number
CREATE INDEX idx_cashier_batches_number ON cashier_batches(batch_number);

-- Индекс: idx_cashier_batches_operator
CREATE INDEX idx_cashier_batches_operator ON cashier_batches(operator_id);

-- Индекс: idx_cashier_batches_status
CREATE INDEX idx_cashier_batches_status ON cashier_batches(batch_status);

-- Индекс: idx_cashier_receipts_allocation
CREATE INDEX idx_cashier_receipts_allocation
            ON cashier_receipts(allocation_status, entry_status)
            ;

-- Индекс: idx_cashier_receipts_apartment
CREATE INDEX idx_cashier_receipts_apartment
            ON cashier_receipts(apartment_id, apartment_number, period_code)
            ;

-- Индекс: idx_cashier_receipts_cashbox
CREATE INDEX idx_cashier_receipts_cashbox
            ON cashier_receipts(cashbox_code, receipt_date)
            ;

-- Индекс: idx_cashier_receipts_status
CREATE INDEX idx_cashier_receipts_status
            ON cashier_receipts(entry_status, receipt_date, id)
            ;

-- Индекс: idx_cashier_reconciliation_status
CREATE INDEX idx_cashier_reconciliation_status
            ON cashier_reconciliation_cases(case_status, priority, created_at)
            ;

-- Индекс: idx_cashier_reconciliation_unit
CREATE INDEX idx_cashier_reconciliation_unit
            ON cashier_reconciliation_cases(apartment_id, apartment_number, case_status)
            ;

-- Индекс: idx_charge_adjustments_assignment
CREATE INDEX idx_charge_adjustments_assignment ON charge_adjustments(adjustment_assignment_id);

-- Индекс: idx_charge_adjustments_charge
CREATE INDEX idx_charge_adjustments_charge ON charge_adjustments(charge_id);

-- Индекс: idx_charge_adjustments_code
CREATE INDEX idx_charge_adjustments_code ON charge_adjustments(adjustment_code);

-- Индекс: idx_charges_adjustment_amount
CREATE INDEX idx_charges_adjustment_amount ON charges(adjustment_amount);

-- Индекс: idx_charges_apartment
CREATE INDEX idx_charges_apartment ON charges(apartment_number);

-- Индекс: idx_charges_base_service
CREATE INDEX idx_charges_base_service ON charges(base_service_code);

-- Индекс: idx_charges_commercial_contract
CREATE INDEX idx_charges_commercial_contract
                ON charges(commercial_contract_id, commercial_contract_item_id, commercial_due_date)
                ;

-- Индекс: idx_charges_period
CREATE INDEX idx_charges_period ON charges(period_code);

-- Индекс: idx_charges_service
CREATE INDEX idx_charges_service ON charges(service_code);

-- Индекс: idx_charges_service_item
CREATE INDEX idx_charges_service_item ON charges(service_item_code);

-- Индекс: idx_charges_service_type
CREATE INDEX idx_charges_service_type ON charges(service_type);

-- Индекс: idx_charges_status
CREATE INDEX idx_charges_status ON charges(status);

-- Индекс: idx_charges_vehicle
CREATE INDEX idx_charges_vehicle ON charges(vehicle_id);

-- Индекс: idx_commercial_access_phone_contract_status
CREATE INDEX idx_commercial_access_phone_contract_status
            ON commercial_access_phones(contract_id, status)
            ;

-- Индекс: idx_commercial_actions_contract_status
CREATE INDEX idx_commercial_actions_contract_status
            ON commercial_access_actions(contract_id, action_status, action_type)
            ;

-- Индекс: idx_commercial_contract_items_contract
CREATE INDEX idx_commercial_contract_items_contract
            ON commercial_contract_items(contract_id, is_active, valid_from, valid_to)
            ;

-- Индекс: idx_commercial_contracts_unit_status
CREATE INDEX idx_commercial_contracts_unit_status
            ON commercial_contracts(unit_id, status, valid_from, valid_to)
            ;

-- Индекс: idx_commercial_notifications_contract
CREATE INDEX idx_commercial_notifications_contract
            ON commercial_notifications(contract_id, notification_type)
            ;

-- Индекс: idx_commercial_notifications_queue
CREATE INDEX idx_commercial_notifications_queue
            ON commercial_notifications(status, created_at)
            ;

-- Индекс: idx_commercial_recipients_contract_status
CREATE INDEX idx_commercial_recipients_contract_status
            ON commercial_contract_recipients(contract_id, notification_enabled, status)
            ;

-- Индекс: idx_commercial_recipients_telegram
CREATE INDEX idx_commercial_recipients_telegram
            ON commercial_contract_recipients(telegram_user_id)
            ;

-- Индекс: idx_operator_audit_action
CREATE INDEX idx_operator_audit_action ON operator_audit_log(action_type);

-- Индекс: idx_operator_audit_actor
CREATE INDEX idx_operator_audit_actor ON operator_audit_log(actor_type);

-- Индекс: idx_operator_audit_created
CREATE INDEX idx_operator_audit_created ON operator_audit_log(created_at);

-- Индекс: idx_operator_audit_operator
CREATE INDEX idx_operator_audit_operator ON operator_audit_log(operator_id);

-- Индекс: idx_operator_audit_review
CREATE INDEX idx_operator_audit_review ON operator_audit_log(review_status);

-- Индекс: idx_operator_audit_table_row
CREATE INDEX idx_operator_audit_table_row ON operator_audit_log(table_name, row_id);

-- Индекс: idx_operator_audit_user
CREATE INDEX idx_operator_audit_user ON operator_audit_log(user_id);

-- Индекс: idx_operator_task_status
CREATE INDEX idx_operator_task_status ON operator_task_queue(status, priority);

-- Индекс: idx_payment_allocations_base_service
CREATE INDEX idx_payment_allocations_base_service ON payment_allocations(base_service_code);

-- Индекс: idx_payment_allocations_service_item
CREATE INDEX idx_payment_allocations_service_item ON payment_allocations(service_item_code);

-- Индекс: idx_payment_allocations_service_type
CREATE INDEX idx_payment_allocations_service_type ON payment_allocations(service_type);

-- Индекс: idx_payment_notices_status
CREATE INDEX idx_payment_notices_status
            ON payment_notices(notice_status, declared_at)
            ;

-- Индекс: idx_payment_notices_unit
CREATE INDEX idx_payment_notices_unit
            ON payment_notices(apartment_id, apartment_number, notice_status)
            ;

-- Индекс: idx_payments_apartment
CREATE INDEX idx_payments_apartment ON payments(apartment_number);

-- Индекс: idx_payments_apartment_id
CREATE INDEX idx_payments_apartment_id
                ON payments(apartment_id)
                ;

-- Индекс: idx_payments_bank_v2
CREATE INDEX idx_payments_bank_v2
            ON payments(bank_transaction_id)
            ;

-- Индекс: idx_payments_base_service
CREATE INDEX idx_payments_base_service ON payments(base_service_code);

-- Индекс: idx_payments_batch_v2
CREATE INDEX idx_payments_batch_v2 ON payments(cashier_batch_id);

-- Индекс: idx_payments_cashbox_code
CREATE INDEX idx_payments_cashbox_code ON payments(cashbox_code);

-- Индекс: idx_payments_cashbox_operation
CREATE INDEX idx_payments_cashbox_operation ON payments(cashbox_operation_id);

-- Индекс: idx_payments_cashier_batch
CREATE INDEX idx_payments_cashier_batch ON payments(cashier_batch_id);

-- Индекс: idx_payments_cashier_receipt
CREATE INDEX idx_payments_cashier_receipt
            ON payments(cashier_receipt_id)
            ;

-- Индекс: idx_payments_commercial_contract
CREATE INDEX idx_payments_commercial_contract
            ON payments(commercial_contract_id, commercial_unit_id)
            ;

-- Индекс: idx_payments_date
CREATE INDEX idx_payments_date ON payments(payment_date);

-- Индекс: idx_payments_notice_v2
CREATE INDEX idx_payments_notice_v2
            ON payments(payment_notice_id)
            ;

-- Индекс: idx_payments_operator
CREATE INDEX idx_payments_operator ON payments(operator_id);

-- Индекс: idx_payments_period
CREATE INDEX idx_payments_period ON payments(period_code);

-- Индекс: idx_payments_service_item
CREATE INDEX idx_payments_service_item ON payments(service_item_code);

-- Индекс: idx_payments_service_type
CREATE INDEX idx_payments_service_type ON payments(service_type);

-- Индекс: idx_payments_vehicle
CREATE INDEX idx_payments_vehicle ON payments(vehicle_id);

-- Индекс: idx_phone_access_charges_due
CREATE INDEX idx_phone_access_charges_due
        ON phone_access_subscription_charges(subscription_id, charge_status, due_date, billing_period)
        ;

-- Индекс: idx_phone_access_charges_payment
CREATE INDEX idx_phone_access_charges_payment
        ON phone_access_subscription_charges(payment_id, payment_notice_id)
        ;

-- Индекс: idx_phone_access_points_status
CREATE INDEX idx_phone_access_points_status
        ON phone_access_subscription_points(subscription_id, point_status, access_point_code)
        ;

-- Индекс: idx_phone_access_request_points_request
CREATE INDEX idx_phone_access_request_points_request
        ON phone_access_request_points(request_id, access_point_code)
        ;

-- Индекс: idx_phone_access_requests_order
CREATE INDEX idx_phone_access_requests_order
        ON phone_access_requests(service_order_id, request_status)
        ;

-- Индекс: idx_phone_access_requests_phone
CREATE INDEX idx_phone_access_requests_phone
        ON phone_access_requests(phone_normalized, apartment_id, request_status)
        ;

-- Индекс: idx_phone_access_subscriptions_phone
CREATE INDEX idx_phone_access_subscriptions_phone
        ON phone_access_subscriptions(phone_normalized, subscription_status)
        ;

-- Индекс: idx_phone_access_subscriptions_status
CREATE INDEX idx_phone_access_subscriptions_status
        ON phone_access_subscriptions(subscription_status, apartment_id, phone_normalized)
        ;

-- Индекс: idx_phone_interest_interest
CREATE INDEX idx_phone_interest_interest ON phone_barrier_access_interests(service_interest_id);

-- Индекс: idx_phone_interest_points_interest
CREATE INDEX idx_phone_interest_points_interest ON phone_barrier_access_interest_points(phone_access_interest_id);

-- Индекс: idx_phone_order_points_order
CREATE INDEX idx_phone_order_points_order ON phone_barrier_access_order_points(service_order_id);

-- Индекс: idx_phone_order_points_status
CREATE INDEX idx_phone_order_points_status ON phone_barrier_access_order_points(status);

-- Индекс: idx_profile_parking_time_test_events_session
CREATE INDEX idx_profile_parking_time_test_events_session
        ON profile_parking_time_test_events(session_id, created_at, id)
        ;

-- Индекс: idx_profile_parking_time_test_sessions_queue
CREATE INDEX idx_profile_parking_time_test_sessions_queue
        ON profile_parking_time_test_sessions(test_status, opened_at, id)
        ;

-- Индекс: idx_ptrt_apartment
CREATE INDEX idx_ptrt_apartment
    ON parking_time_review_tasks(apartment_number)
    ;

-- Индекс: idx_ptrt_status
CREATE INDEX idx_ptrt_status
    ON parking_time_review_tasks(status)
    ;

-- Индекс: idx_receipts_batch_v2
CREATE INDEX idx_receipts_batch_v2 ON cashier_receipts(cashier_batch_id);

-- Индекс: idx_receipts_notice_v2
CREATE INDEX idx_receipts_notice_v2
            ON cashier_receipts(payment_notice_id)
            ;

-- Индекс: idx_remote_asset_movements_asset
CREATE INDEX idx_remote_asset_movements_asset ON remote_asset_movements(remote_asset_id, created_at);

-- Индекс: idx_remote_assets_status
CREATE INDEX idx_remote_assets_status ON remote_assets(inventory_status, condition_status);

-- Индекс: idx_remote_handover_operator
CREATE INDEX idx_remote_handover_operator ON remote_handover_events(operator_id, created_at);

-- Индекс: idx_remote_handover_post
CREATE INDEX idx_remote_handover_post ON remote_handover_events(post_code, created_at);

-- Индекс: idx_remote_handover_request
CREATE INDEX idx_remote_handover_request ON remote_handover_events(remote_request_id);

-- Индекс: idx_remote_requests_apartment
CREATE INDEX idx_remote_requests_apartment
            ON remote_requests(apartment_id, created_at)
            ;

-- Индекс: idx_remote_requests_resident
CREATE INDEX idx_remote_requests_resident
            ON remote_requests(resident_account_id, status, created_at)
            ;

-- Индекс: idx_remote_requests_status
CREATE INDEX idx_remote_requests_status
            ON remote_requests(status, created_at)
            ;

-- Индекс: idx_remote_supplier_batches_status
CREATE INDEX idx_remote_supplier_batches_status
            ON remote_supplier_batches(batch_status, service_item_code, id)
            ;

-- Индекс: idx_resident_accounts_apartment
CREATE INDEX idx_resident_accounts_apartment
    ON resident_accounts(apartment_number)
    ;

-- Индекс: idx_resident_accounts_role
CREATE INDEX idx_resident_accounts_role
    ON resident_accounts(role)
    ;

-- Индекс: idx_resident_accounts_status
CREATE INDEX idx_resident_accounts_status
    ON resident_accounts(status)
    ;

-- Индекс: idx_resident_accounts_telegram_user
CREATE INDEX idx_resident_accounts_telegram_user
    ON resident_accounts(telegram_user_id)
    ;

-- Индекс: idx_resident_invitations_apartment
CREATE INDEX idx_resident_invitations_apartment ON resident_invitations(apartment_number);

-- Индекс: idx_resident_profile_journal_account
CREATE INDEX idx_resident_profile_journal_account
        ON resident_profile_operation_journal(resident_account_id, created_at, id)
        ;

-- Индекс: idx_resident_profile_requests_queue
CREATE INDEX idx_resident_profile_requests_queue
        ON resident_profile_change_requests(request_status, submitted_at, apartment_number)
        ;

-- Индекс: idx_resident_profile_verifications_status
CREATE INDEX idx_resident_profile_verifications_status
        ON resident_profile_verifications(verification_status, apartment_id, apartment_number)
        ;

-- Индекс: idx_resident_verification_status
CREATE INDEX idx_resident_verification_status ON resident_verification_requests(status);

-- Индекс: idx_service_access_credentials_value
CREATE INDEX idx_service_access_credentials_value ON service_access_credentials(credential_kind, credential_value, credential_status);

-- Индекс: idx_service_catalog_active
CREATE INDEX idx_service_catalog_active ON service_catalog(is_active);

-- Индекс: idx_service_catalog_code
CREATE INDEX idx_service_catalog_code ON service_catalog(service_code);

-- Индекс: idx_service_catalog_group
CREATE INDEX idx_service_catalog_group ON service_catalog(service_group);

-- Индекс: idx_service_catalog_type
CREATE INDEX idx_service_catalog_type ON service_catalog(service_type);

-- Индекс: idx_service_interest_payment_notice
CREATE INDEX idx_service_interest_payment_notice
            ON service_order_interests(payment_notice_id)
            ;

-- Индекс: idx_service_interest_resident
CREATE INDEX idx_service_interest_resident
            ON service_order_interests(resident_account_id, id)
            ;

-- Индекс: idx_service_interests_apartment
CREATE INDEX idx_service_interests_apartment ON service_interests(apartment_number);

-- Индекс: idx_service_interests_service_item
CREATE INDEX idx_service_interests_service_item ON service_interests(service_item_code);

-- Индекс: idx_service_interests_status
CREATE INDEX idx_service_interests_status ON service_interests(status);

-- Индекс: idx_service_item_workflows_profile
CREATE INDEX idx_service_item_workflows_profile ON service_item_workflows(workflow_profile_code, is_active);

-- Индекс: idx_service_items_active
CREATE INDEX idx_service_items_active ON service_items(is_active);

-- Индекс: idx_service_items_code
CREATE INDEX idx_service_items_code ON service_items(service_item_code);

-- Индекс: idx_service_items_period
CREATE INDEX idx_service_items_period ON service_items(period_code);

-- Индекс: idx_service_items_service
CREATE INDEX idx_service_items_service ON service_items(service_code);

-- Индекс: idx_service_items_type
CREATE INDEX idx_service_items_type ON service_items(service_type);

-- Индекс: idx_service_order_events_order
CREATE INDEX idx_service_order_events_order ON service_order_events(service_order_id, created_at);

-- Индекс: idx_service_order_steps_order
CREATE INDEX idx_service_order_steps_order ON service_order_steps(service_order_id, sequence_no, step_status);

-- Индекс: idx_service_orders_item
CREATE INDEX idx_service_orders_item ON service_orders(service_item_code, order_status, requested_at);

-- Индекс: idx_service_orders_unit
CREATE INDEX idx_service_orders_unit ON service_orders(apartment_id, order_status, requested_at);

-- Индекс: idx_service_price_versions_item
CREATE INDEX idx_service_price_versions_item ON service_price_versions(service_item_code, effective_from, effective_to, is_active);

-- Индекс: idx_service_tariffs_code_dates
CREATE INDEX idx_service_tariffs_code_dates ON service_tariffs(service_code, valid_from, valid_to);

-- Индекс: idx_supplier_batch_links_order
CREATE INDEX idx_supplier_batch_links_order
            ON remote_supplier_batch_links(service_order_id, link_status)
            ;

-- Индекс: idx_unit_aliases_apartment
CREATE INDEX idx_unit_aliases_apartment
        ON unit_aliases(apartment_id)
    ;

-- Индекс: idx_unit_aliases_unique_active
CREATE UNIQUE INDEX idx_unit_aliases_unique_active
        ON unit_aliases(alias_normalized)
        WHERE is_active = 1
    ;

-- Индекс: idx_unit_contacts_apartment
CREATE INDEX idx_unit_contacts_apartment
        ON unit_contacts(apartment_id)
    ;

-- Индекс: idx_unit_contacts_primary
CREATE UNIQUE INDEX idx_unit_contacts_primary
        ON unit_contacts(apartment_id)
        WHERE is_primary = 1
    ;

-- Индекс: idx_unit_group_aliases_group
CREATE INDEX idx_unit_group_aliases_group
        ON unit_group_aliases(group_id)
    ;

-- Индекс: idx_unit_group_members_apartment
CREATE INDEX idx_unit_group_members_apartment
        ON unit_group_members(apartment_id)
    ;

-- Индекс: idx_unit_groups_status
CREATE INDEX idx_unit_groups_status
        ON unit_groups(record_status, legal_status)
    ;

-- Индекс: idx_verification_candidates_status
CREATE INDEX idx_verification_candidates_status
    ON verification_candidates(status)
    ;

-- Индекс: idx_verification_candidates_task
CREATE INDEX idx_verification_candidates_task
    ON verification_candidates(task_id)
    ;

-- Индекс: idx_verification_evidence_task
CREATE INDEX idx_verification_evidence_task
    ON verification_evidence(task_id)
    ;

-- Индекс: idx_verification_tasks_apartment
CREATE INDEX idx_verification_tasks_apartment
    ON verification_tasks(apartment_number)
    ;

-- Индекс: idx_verification_tasks_status
CREATE INDEX idx_verification_tasks_status
    ON verification_tasks(status)
    ;

-- Индекс: idx_verification_tasks_type
CREATE INDEX idx_verification_tasks_type
    ON verification_tasks(task_type)
    ;

-- Индекс: ux_access_debt_warning_open
CREATE UNIQUE INDEX ux_access_debt_warning_open
        ON access_debt_warnings(subscription_id, debt_source)
        WHERE warning_status IN ('OPEN', 'DEACTIVATION_QUEUED')
        ;

-- Индекс: ux_commercial_notification_dedupe
CREATE UNIQUE INDEX ux_commercial_notification_dedupe
            ON commercial_notifications(dedupe_key)
        ;

-- Индекс: ux_commercial_one_active_contract_per_unit
CREATE UNIQUE INDEX ux_commercial_one_active_contract_per_unit
            ON commercial_contracts(unit_id)
            WHERE status = 'ACTIVE'
        ;

-- Индекс: ux_commercial_phone_per_contract
CREATE UNIQUE INDEX ux_commercial_phone_per_contract
            ON commercial_access_phones(contract_id, phone_normalized)
        ;

-- Индекс: ux_profile_parking_time_test_active_vehicle
CREATE UNIQUE INDEX ux_profile_parking_time_test_active_vehicle
        ON profile_parking_time_test_sessions(target_vehicle_id)
        WHERE test_status IN ('OPEN', 'PENDING_OPERATOR')
        ;

-- Индекс: ux_service_interest_payment
CREATE UNIQUE INDEX ux_service_interest_payment
            ON service_order_interests(payment_id)
            WHERE payment_id IS NOT NULL
            ;

-- ==========================================
-- ВОССТАНОВЛЕНИЕ НАСТРОЕК
-- ==========================================

PRAGMA foreign_keys = ON;
PRAGMA quick_check;

-- ==========================================
-- ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ
-- ==========================================

-- Всего таблиц: 109
-- Всего представлений: 3
-- Всего индексов: 193
-- Всего триггеров: 0
-- Размер БД: 2.06 MB

-- Восстановите БД командой:
-- sqlite3 new_database.db < osbb_test_schema_20260710_112003.sql
