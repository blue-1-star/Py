# User Onboarding v0.1

A Telegram user is not automatically a resident.

Lifecycle:

```text
UNKNOWN -> INVITED -> REGISTERED -> PENDING_ADMIN_CONFIRMATION -> ACTIVE resident
```

## Tables

- `resident_invitations`
- `resident_verification_requests`
- `resident_access_accounts`
- `operator_task_queue`

`operator_task_queue` is shared: it can later receive manual admin tasks and parking verification tasks.

## Commands

Dry run:

```powershell
python .\OSBB\tools\user_onboarding\create_onboarding_schema.py
```

Apply:

```powershell
python .\OSBB\tools\user_onboarding\create_onboarding_schema.py --apply
```

Apply mode creates a DB backup first.

## Next

1. Admin queue: pending resident confirmations.
2. Confirm resident button.
3. Correction path: create operator task if resident says data is wrong.
4. Role/access screens under Settings.
