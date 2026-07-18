#!/usr/bin/env python
"""
Справочно-аналитические запросы к БД OSBB

Примеры:
  python -m OSBB_util.query_lib.cli find 8092
  python -m OSBB_util.query_lib.cli cars --min 2
  python -m OSBB_util.query_lib.cli missing-mode
  python -m OSBB_util.query_lib.cli debtors
  python -m OSBB_util.query_lib.cli debtors 07-2026
  python -m OSBB_util.query_lib.cli non-standard
  python -m OSBB_util.query_lib.cli apartment 167
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from OSBB_util.query_lib.queries import (
    find_by_plate_fragment,
    apartments_with_multiple_cars,
    apartments_with_missing_parking_mode,
    parking_debtors,
    non_standard_plates,
    vehicles_by_apartment,
)


def print_table(rows, headers=None):
    """Вывод таблицы (без tabulate)"""
    if not rows:
        print("Нет данных")
        return

    if isinstance(rows[0], dict):
        if headers is None:
            headers = list(rows[0].keys())
        print(" | ".join(str(h) for h in headers))
        print("-" * 60)
        for row in rows:
            print(" | ".join(str(row.get(h, "")) for h in headers))
        return

    # Если rows — список кортежей или sqlite3.Row
    if headers is None and hasattr(rows[0], 'keys'):
        headers = list(rows[0].keys())

    if headers:
        print(" | ".join(str(h) for h in headers))
        print("-" * 60)

    for row in rows:
        if hasattr(row, 'keys'):
            print(" | ".join(str(row[h]) for h in headers))
        else:
            print(" | ".join(str(x) for x in row))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0]

    if cmd == "find" and len(args) > 1:
        fragment = args[1]
        rows = find_by_plate_fragment(fragment)
        print_table(rows)

    elif cmd == "cars":
        min_count = 2
        if "--min" in args:
            idx = args.index("--min")
            if idx + 1 < len(args):
                min_count = int(args[idx + 1])
        rows = apartments_with_multiple_cars(min_count)
        print_table(rows, headers=["квартира", "количество_авто"])

    elif cmd == "missing-mode":
        rows = apartments_with_missing_parking_mode()
        print_table(rows, headers=["квартира", "номер", "марка", "режим"])

    elif cmd == "debtors":
        period = args[1] if len(args) > 1 else None
        rows = parking_debtors(period)
        print_table(rows, headers=["квартира", "фио", "начислено", "оплачено", "задолженность"])

    elif cmd == "non-standard":
        rows = non_standard_plates()
        print_table(rows, headers=["квартира", "номер", "марка"])

    elif cmd == "apartment":
        if len(args) < 2:
            print("Укажите номер квартиры: python -m OSBB_util.query_lib.cli apartment 111")
            return
        apt = args[1]
        rows = vehicles_by_apartment(apt)
        print_table(rows, headers=["номер", "марка", "режим"])

    else:
        print(f"Неизвестная команда: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()