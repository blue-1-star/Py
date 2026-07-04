# db_inspector.py

## Purpose

`db_inspector.py` is the OSBB SQLite diagnostic tool.

It is not a Telegram bot interface. It is a developer/operator command-line tool and a future foundation for a web/admin dashboard.

## Run from project root

```powershell
python .\tools\db_inspector.py summary
```

## Default database

```text
Data\db\osbb_test.db
```

## Commands

```powershell
python .\tools\db_inspector.py summary
python .\tools\db_inspector.py tables
python .\tools\db_inspector.py schema payments
python .\tools\db_inspector.py admins
python .\tools\db_inspector.py roles
python .\tools\db_inspector.py cashier
python .\tools\db_inspector.py service-orders
python .\tools\db_inspector.py remotes
python .\tools\db_inspector.py vehicles
python .\tools\db_inspector.py search cash
```

## Design note

This tool belongs to the project maintenance layer.

It should grow into a reusable inspection API before any web dashboard is built.
