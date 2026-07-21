# OSBB Working DB Session

Created: 2026-07-02 17:18:39

Label: `pult_order_test`

Golden DB:

`G:\Programming\Py\OSBB\Data\db\osbb_test.db`

Working DB:

`G:\Programming\Py\OSBB\Data\db\working\osbb_working_pult_order_test_2026-07-02_17-18-39.db`

Purpose:

Acceptance test: resident orders remote/pult, operator processes request, cashier/payment path if needed.

## Rule

This DB is disposable.

Use it for acceptance testing only.

At the end run one of:

```powershell
python .\OSBB\tools\working_db_session.py finish --db "G:\Programming\Py\OSBB\Data\db\working\osbb_working_pult_order_test_2026-07-02_17-18-39.db" --delete --apply
```

or

```powershell
python .\OSBB\tools\working_db_session.py finish --db "G:\Programming\Py\OSBB\Data\db\working\osbb_working_pult_order_test_2026-07-02_17-18-39.db" --archive --apply
```
