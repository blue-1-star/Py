#!/usr/bin/env python
"""
Добавляет сегодняшнюю запись в Project Log.
Запуск: python OSBB_util/scripts/build_log.py
"""

import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import paths


def main():
    docs_dir = paths.OSBB_ROOT / "Docs"
    log_path = docs_dir / "Project_Log.md"
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    entry = f"""## {today}

### ✅ Что сделано
- Касса (`Cashbox.register_payment`) прошла тест: создан кандидат и платёж.
- Исправлен `service_catalog` (добавлены категории COMMERCIAL/FUNDRAISING).
- Проведена миграция БД: разрешён NULL в `payments.apartment_number`.

### 📝 Обновлены документы
- [ADR-2026-07-14-vehicle-candidate.md](Architecture/ADR-2026-07-14-vehicle-candidate.md)
- [Data Dictionary — vehicle_candidates](Database/Data_Dictionary.md#6-таблица-vehicle_candidates)
- [Changelog](Changelog/CHANGELOG_core_new.md)

### 🆕 Новые сущности
- **Таблица `vehicle_candidates`** — для хранения "недоавтомобилей".
- **Модель `VehicleCandidate`** — в `core_new/domain/vehicle_candidate.py`.
- **Таблица `service_items`** — теперь используется для получения тарифов.

### 📌 Следующие шаги
- Упростить UX кассы (подстановка суммы из `service_items`).
- Создать интерфейс для подтверждения кандидатов оператором.

---
"""
    
    if log_path.exists():
        with open(log_path, 'r', encoding='utf-8') as f:
            old = f.read()
    else:
        old = "# Project Log\n\n"
    
    with open(log_path, 'w', encoding='utf-8') as f:
        if old.startswith("# Project Log"):
            f.write("# Project Log\n\n" + entry + old[len("# Project Log\n\n"):])
        else:
            f.write("# Project Log\n\n" + entry + old)
    
    print(f"✅ Project Log обновлён: {log_path}")


if __name__ == "__main__":
    main()