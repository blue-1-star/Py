#!/usr/bin/env python
"""
Главный скрипт для генерации всей архитектурной документации OSBB.
Создаёт:
  - ROADMAP.md
  - Changelog (CHANGELOG_core_new.md)
  - ADR (Architecture Decision Records)
  - Data Dictionary (Data_Dictionary.md)
  - Документацию по доменным моделям (Domain/vehicles.md, residents.md, etc.)
  - Обновляет README.md в Docs/

Запуск: python OSBB_util/scripts/build_docs.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Добавляем корень проекта
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from local_config import local_config


def ensure_dir(path: Path) -> None:
    """Создаёт папку, если её нет"""
    path.mkdir(parents=True, exist_ok=True)


def write_file(filepath: Path, content: str) -> None:
    """Записывает содержимое в файл"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ {filepath.relative_to(local_config.py_root)}")


# ==========================================
# 1. ROADMAP
# ==========================================

def create_roadmap() -> None:
    content = '''# OSBB Roadmap

\<!-- RESIDENT_IDENTITY_REFACTOR_V1:BEGIN -->

## P1. Resident Identity Refactor

**Status:** planned  
**Date decided:** 2026-07-01  
**Reason:** current resident/client/admin flow mixes several different concepts and creates confusing behavior.

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
Real resident acts for themselves. Resident can:
- view and confirm their apartment;
- maintain personal contact data;
- add, edit, or request changes to vehicles;
- submit remote/pult requests;
- see charges, payments, and service history.

#### 2. Operator Workspace
Operator acts on request of a resident, but never becomes that resident. All actions must be auditable.

#### 3. Super-admin Diagnostic Resident View
Super-admin can temporarily view the bot as a chosen apartment/resident for diagnostics.

### Legacy rule
The existing flow around "Змінити квартиру" and "Режим мешканця" is considered legacy and should not be expanded.

\<!-- RESIDENT_IDENTITY_REFACTOR_V1:END -->

\<!-- CORE_NEW_LAYER_V1:BEGIN -->

## P2. New Architecture Layer (core_new)

**Status:** completed (2026-07-13)

### What was done

Created a new architectural layer `core_new/` that separates business logic from interface code.

#### 1. Adapters
Created `DBAdapter` — a wrapper around the legacy `Bots/db_access.py`.

#### 2. Domain Models

| Model | Status | Tests |
|-------|--------|-------|
| `Vehicle` | ✅ | ✅ |
| `Resident` | ✅ | ✅ |
| `Apartment` | ✅ | ✅ |
| `Payment` | ✅ | ✅ |
| `VehicleCandidate` | ✅ | ✅ |

#### 3. Testing

All models have working tests in `tests/`.

#### 4. Documentation

- [ADR-2026-07-13-core-new-layer.md](Architecture/ADR-2026-07-13-core-new-layer.md)
- [Domain models](../Domain/README.md)
- [core_new code docs](../Code/core_new.md)

### Next steps

1. Replace legacy calls with new domain models
2. Integrate all models into Telegram bot
3. Remove duplicate code

\<!-- CORE_NEW_LAYER_V1:END -->

\<!-- CASHIER_VEHICLE_CANDIDATE_V1:BEGIN -->

## P3. Cashier and Vehicle Candidate (В работе)

**Status:** in progress (2026-07-14)

### Problem

Cashier cannot accept payments for vehicles without an apartment.

### Decision

Create a new entity: `vehicle_candidates`.

### Lifecycle
PENDING → RESOLVED → vehicle created in vehicles
↘ REJECTED

text

### Next steps

1. Integrate `vehicle_candidates` into cashier UI
2. Add operator workspace for reviewing candidates
3. Link payments to candidates via `candidate_id`

\<!-- CASHIER_VEHICLE_CANDIDATE_V1:END -->
'''
    docs_dir = local_config.py_root / "OSBB" / "Docs"
    ensure_dir(docs_dir)
    write_file(docs_dir / "ROADMAP.md", content)
