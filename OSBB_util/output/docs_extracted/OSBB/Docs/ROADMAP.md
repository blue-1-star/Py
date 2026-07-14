# OSBB Roadmap

<!-- RESIDENT_IDENTITY_REFACTOR_V1:BEGIN -->

## P1. Resident Identity Refactor

Status: planned
Date decided: 2026-07-01
Reason: current resident/client/admin flow mixes several different concepts and creates confusing behavior.

### Problem

The current legacy flow around "Режим мешканця", "Змінити квартиру", apartment binding, resident verification, and admin testing is mixed.

It currently blends together:

- resident self-service cabinet;
- apartment binding and verification;
- operator work on behalf of a resident;
- super-admin diagnostic view;
- real Telegram ID to apartment binding.

This creates unclear states, especially for super-admins and operators.

### Decision

Split the old mixed flow into three separate flows.

#### 1. Resident Cabinet

Real resident acts for themselves.

Resident can:

- view and confirm their apartment;
- maintain personal contact data;
- add, edit, or request changes to vehicles;
- update parking-related attributes when allowed;
- submit remote/pult requests;
- submit phone barrier access requests;
- see charges, payments, and service history;
- confirm current profile data.

Important rule:

Resident may edit ordinary profile data directly, but changes affecting access, payments, permissions, or legal responsibility may require operator review.

Examples:

- contact phone: direct edit or light confirmation;
- vehicle plate: review if it affects access/payment;
- parking mode: review;
- gate phone number: service request/review;
- binding to another apartment: strict operator verification.

#### 2. Operator Workspace

Operator acts on request of a resident, but never becomes that resident.

Operator opens a resident/apartment card and performs actions from the operator role:

- create pult request;
- create phone access request;
- register payment;
- correct vehicle data;
- open service history;
- manage commercial/non-residential units;
- create or update contracts;
- record the source/reason of the action.

All such actions must be auditable as operator actions.

#### 3. Super-admin Diagnostic Resident View

Super-admin can temporarily view the bot as a chosen apartment/resident for diagnostics.

This is only a diagnostic view.

Rules:

- does not change Telegram ID binding;
- does not change resident_account;
- does not create apartment binding requests;
- does not change verification status;
- must show a visible "diagnostic view" banner;
- must have explicit exit;
- /start must reset this mode;
- optional timeout should auto-expire the mode.

### Legacy rule

The existing flow around "Змінити квартиру" and "Режим мешканця" is considered legacy and should not be expanded.

Before replacing it, create a diagnostic map of:

- where apartment change is handled;
- where binding requests are created;
- where verification status is changed;
- where Telegram ID is connected to resident/apartment;
- where admin client/resident mode is entered and exited.

### Next implementation step

Create a diagnostic tool:

`OSBB/tools/diagnose_resident_identity_flow.py`

Its purpose is to find and report code entry points of the old resident identity flow before replacement.

<!-- RESIDENT_IDENTITY_REFACTOR_V1:END -->
