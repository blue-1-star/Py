#!/usr/bin/env python3
"""
osbb_cleanup_triage.py
=======================

Инструмент для наведения порядка в проекте OSBB.

НИЧЕГО не удаляет. Он только:
  1) В режиме DRY-RUN (по умолчанию) — сканирует дерево проекта и печатает
     / сохраняет в CSV отчёт: какие файлы похожи на бэкапы/копии/мусор,
     по какому правилу они попали в отчёт, и куда их предлагается перенести.
  2) В режиме --apply — реально ПЕРЕНОСИТ (не удаляет!) найденные файлы
     в отдельную папку архива рядом с проектом, сохраняя относительную
     структуру путей, и пишет лог перемещений (чтобы можно было откатить
     вручную).

Как запускать (Windows, из папки со скриптом):

    py osbb_cleanup_triage.py --root "G:\\Programming\\Py\\OSBB"

Это только отчёт (ничего не трогает). Отчёт сохранится рядом со скриптом
в файл osbb_triage_report.csv — откройте его в Excel и проверьте.

Когда убедитесь, что отчёт адекватный, переносите файлы командой:

    py osbb_cleanup_triage.py --root "G:\\Programming\\Py\\OSBB" --apply

По умолчанию файлы переносятся в:
    G:\\Programming\\Py\\OSBB_util\\output\\triage_archive
(служебный каталог рядом с проектом, не внутри самого OSBB).
Можно переопределить через --archive-dir.

По умолчанию переносятся только файлы с "высокой уверенностью" (см. ниже).
Файлы категории "на ревью" (REVIEW) не переносятся даже в --apply,
пока вы явно не добавите --include-review.

Категории:
  HIGH  (переносятся в --apply по умолчанию):
    - backup_folder      : лежит внутри папки backups/backup (любой глубины)
    - timestamped_name    : в имени файла/папки есть штамп времени
                             вида 2026-06-27_20-04-49 или 20260627_142150
    - before_prefix        : имя содержит "before_" (снимок "до правки")
    - manual_copy          : имя содержит " - Copy" / "_copy" (ручная копия)
    - db_backup             : файл .db лежит в папке backups/
    - generated_doc_export  : .md внутри Data/exports/* — авто-сгенерированный
                                отчёт/аудит, не документация для чтения людьми
    - recovered_report       : .md внутри Recovered/ или Recovered_Releases/ —
                                разовый восстановительный/следственный отчёт
    - confirmed_duplicate    : путь явно подтверждён пользователем как дубль
                                (см. EXPLICIT_DUPLICATE_DIRS в начале файла)
    - patch_script            : корневой patch_*.py — одноразовый скрипт,
                                 когда-то модифицировавший исходники (история)
    - one_off_fix_bundle       : корневые INSTALL_*.py/.bat, заглавные MIGRATE_*.py,
                                 RUN_*.bat, README_*.txt — связка одного фикса
    - root_zip_bundle          : OSBB_*.zip в корне — готовый архив патча
    - old_suffix                : явный суффикс _old при наличии файла без него

  REVIEW (только в отчёте, не переносятся без --include-review):
    - check_script          : имя начинается с CHECK_ (разовая диагностика)
    - sandbox_name           : в имени/пути встречается sandbox
    - versioned_duplicate    : похоже на старую версию при наличии файла
                                 без суффикса версии (_v2, _v3 и т.п.)
    - variant_suffix          : папка/файл с суффиксом _0, _p, _prev и т.п.
                                 при наличии "базового" имени без суффикса
    - duplicate_doc_name      : .md с необычным именем (не MODULE.md/README.md/
                                 CHANGELOG.md/INSTALL.md) встречается в
                                 нескольких разных папках проекта — возможен
                                 конфликт содержимого, а не просто дубль
    - data_pipeline_history    : корневые скрипты оцифровки/переноса данных
                                 (Collect_sheets*, import_*, extract_telegram_*,
                                 build_plate_*, plate_consensus_*, report_* и т.п.)
                                 — историческая ценность, не рабочий код

Ничего не удаляется. Худший случай ошибки — файл окажется в архиве,
откуда его легко вернуть обратно.
"""

import argparse
import csv
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

TIMESTAMP_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})|(\d{8}_\d{6})"
)
BEFORE_RE = re.compile(r"before_", re.IGNORECASE)
COPY_RE = re.compile(r"(\s-\s?copy|_copy)\b", re.IGNORECASE)
CHECK_RE = re.compile(r"^CHECK_", re.IGNORECASE)
SANDBOX_RE = re.compile(r"sandbox", re.IGNORECASE)
VERSION_SUFFIX_RE = re.compile(r"^(?P<base>.+?)_v(?P<num>\d+)$", re.IGNORECASE)
VARIANT_SUFFIX_RE = re.compile(r"^(?P<base>.+?)_(?:0|p|prev)$", re.IGNORECASE)
OLD_SUFFIX_RE = re.compile(r"^(?P<base>.+?)_old$", re.IGNORECASE)

# Разовые скрипты-патчи, применённые к исходникам один раз в прошлом —
# ценны как история, но не рабочий код.
PATCH_SCRIPT_RE = re.compile(r"^patch_\w+\.py$", re.IGNORECASE)

# Связки одного точечного фикса: INSTALL_*, заглавные MIGRATE_*, RUN_*.bat,
# README_*.txt — обычно расходятся по 3-5 файлов на один и тот же фикс.
INSTALL_SCRIPT_RE = re.compile(r"^INSTALL_.+\.(py|bat)$")
MIGRATE_UPPER_RE = re.compile(r"^MIGRATE_.+\.py$")  # заглавные — одноразовые, не путать с migrate_*.py (история миграций)
RUN_SCRIPT_RE = re.compile(r"^RUN_.+\.bat$")
FIX_README_RE = re.compile(r"^README_.+\.txt$")

# Готовые бандлы точечных патчей, лежащие в корне.
ROOT_ZIP_RE = re.compile(r"^OSBB_.+\.zip$")

# Пайплайн оцифровки/переноса данных (бумага -> Word -> Excel -> БД) —
# исторически ценно, но не часть работающего приложения. REVIEW, не HIGH.
DATA_PIPELINE_RE = re.compile(
    r"^(Collect_sheets\d*|Collect_word_tables|Word_table_to_Excel|Generate_Stetement|"
    r"build_plate_\w+|plate_consensus_\w+|extract_telegram_\w+|import_\w+|report_\w+)\.py$",
    re.IGNORECASE,
)

# .md-файлы внутри этих подпапок (относительно root) — авто-сгенерированные
# отчёты/аудиты/раскопки, не "документация" в смысле "почитать человеку".
GENERATED_DOC_DIR_PREFIXES = ("Data/exports",)
RECOVERED_DOC_DIR_PREFIXES = ("Recovered", "Recovered_Releases")

# Стандартные поручные имена доков рядом с кодом — их повторение в разных
# папках ОЖИДАЕМО и не является конфликтом, поэтому исключаем из проверки
# на "совпадение имени файла в разных местах".
COMMON_MODULE_DOC_NAMES = {"MODULE.md", "README.md", "CHANGELOG.md", "INSTALL.md"}

# Папки/файлы, явно подтверждённые пользователем как дубли — переносятся в
# архив целиком, без дополнительных признаков. Пути — относительно root,
# разделитель "/", регистронезависимо.
EXPLICIT_DUPLICATE_DIRS = (
    "tools/cashier_v2_telegram_p",
)

SKIP_DIR_NAMES = {".git", "__pycache__", ".venv", "venv", "node_modules"}


def try_load_config(py_root: Path):
    """Пытается импортировать config.py из каталога py_root (там, где лежат
    все проекты — например, G:\\Programming\\Py). Возвращает объект `paths`
    (экземпляр ProjectPaths) или None, если не получилось — это не ошибка,
    скрипт просто будет работать без авто-определения путей."""
    py_root = Path(py_root)
    config_file = py_root / "config.py"
    if not config_file.exists():
        return None
    sys.path.insert(0, str(py_root))
    try:
        import config  # type: ignore
        return config.paths
    except Exception as e:
        print(f"Предупреждение: не удалось импортировать config.py: {e}", file=sys.stderr)
        return None


def get_protected_paths(cfg_paths) -> set:
    """Собирает все пути, на которые config.py явно ссылается как на рабочие
    файлы/папки проекта. Такие пути никогда не отправляются в архив, даже
    если их имя формально совпадает с 'мусорным' паттерном (пример из жизни:
    OSBB_HOUSE_REGISTRY_FILE называется '... - Copy.xlsx', но это боевой
    файл, а не случайная копия)."""
    protected = set()
    if cfg_paths is None:
        return protected
    for value in vars(cfg_paths).values():
        if isinstance(value, Path):
            try:
                protected.add(value.resolve())
            except Exception:
                pass
    return protected


def is_in_backup_folder(path: Path, root: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    return any(p.lower() in ("backups", "backup") for p in rel_parts[:-1])


def classify(path: Path, root: Path, sibling_stems: set, protected: set, doc_name_collisions: set) -> list[tuple[str, str]]:
    """Возвращает список (категория, причина) — файл может попасть
    сразу в несколько категорий, репорт покажет все."""
    hits = []
    rel = path.relative_to(root)
    rel_str = str(rel).replace("\\", "/")
    name = path.name
    stem = path.stem

    if is_in_backup_folder(path, root):
        hits.append(("HIGH:backup_folder", f"внутри папки backups/: {rel}"))

    if TIMESTAMP_RE.search(str(rel)):
        m = TIMESTAMP_RE.search(str(rel))
        hits.append(("HIGH:timestamped_name", f"штамп времени в пути: {m.group(0)}"))

    if BEFORE_RE.search(name):
        hits.append(("HIGH:before_prefix", "содержит 'before_' (снимок до правки)"))

    if COPY_RE.search(name):
        hits.append(("HIGH:manual_copy", "похоже на ручную копию (' - Copy' / '_copy')"))

    if path.suffix.lower() == ".db" and is_in_backup_folder(path, root):
        hits.append(("HIGH:db_backup", "снапшот базы данных внутри backups/"))

    if path.suffix.lower() == ".md" and rel_str.startswith(GENERATED_DOC_DIR_PREFIXES):
        hits.append(("HIGH:generated_doc_export", f"авто-сгенерированный отчёт в {rel.parts[0]}/{rel.parts[1]}/..."))

    if path.suffix.lower() == ".md" and rel_str.startswith(RECOVERED_DOC_DIR_PREFIXES):
        hits.append(("HIGH:recovered_report", "разовый восстановительный/следственный отчёт"))

    is_at_root = len(rel.parts) == 1  # файл лежит прямо в корне root, без подпапок

    if is_at_root and PATCH_SCRIPT_RE.match(name):
        hits.append(("HIGH:patch_script", "одноразовый скрипт-патч исходников (история применения, не рабочий код)"))

    if is_at_root and INSTALL_SCRIPT_RE.match(name):
        hits.append(("HIGH:one_off_fix_bundle", "часть связки INSTALL_*/MIGRATE_*/RUN_*/README_* одного точечного фикса"))

    if is_at_root and MIGRATE_UPPER_RE.match(name):
        hits.append(("HIGH:one_off_fix_bundle", "одноразовый MIGRATE_* (заглавный) — часть связки точечного фикса, не история миграций БД"))

    if is_at_root and RUN_SCRIPT_RE.match(name):
        hits.append(("HIGH:one_off_fix_bundle", "RUN_*.bat — запускатель одноразового фикса"))

    if is_at_root and FIX_README_RE.match(name):
        hits.append(("HIGH:one_off_fix_bundle", "README_*.txt — описание одноразового фикса"))

    if is_at_root and ROOT_ZIP_RE.match(name):
        hits.append(("HIGH:root_zip_bundle", "готовый zip-бандл точечного патча в корне проекта"))

    om = OLD_SUFFIX_RE.match(stem)
    if om and om.group("base") in sibling_stems:
        hits.append(("HIGH:old_suffix", f"явный суффикс _old при наличии файла без него: {om.group('base')}{path.suffix}"))

    if DATA_PIPELINE_RE.match(name):
        hits.append((
            "REVIEW:data_pipeline_history",
            "часть пайплайна оцифровки/переноса данных (бумага → Word → Excel → БД) — "
            "исторически ценно, но не часть работающего приложения",
        ))

    if any(rel_str.lower().startswith(d.lower() + "/") or rel_str.lower() == d.lower() for d in EXPLICIT_DUPLICATE_DIRS):
        hits.append(("HIGH:confirmed_duplicate", "подтверждено пользователем как дубль, см. EXPLICIT_DUPLICATE_DIRS"))

    if CHECK_RE.match(name):
        hits.append(("REVIEW:check_script", "разовый диагностический скрипт CHECK_*"))

    if SANDBOX_RE.search(str(rel)):
        hits.append(("REVIEW:sandbox_name", "в пути встречается 'sandbox'"))

    if name in doc_name_collisions and name not in COMMON_MODULE_DOC_NAMES:
        hits.append((
            "REVIEW:duplicate_doc_name",
            f"файл с именем '{name}' встречается в нескольких папках проекта — "
            f"возможен конфликт содержимого, а не просто дубль (проверьте вручную)",
        ))

    vmatch = VERSION_SUFFIX_RE.match(stem)
    if vmatch:
        base = vmatch.group("base")
        if base in sibling_stems:
            hits.append((
                "REVIEW:versioned_duplicate",
                f"есть версия с суффиксом (_v{vmatch.group('num')}), "
                f"и рядом существует файл без суффикса: {base}{path.suffix}",
            ))

    vsmatch = VARIANT_SUFFIX_RE.match(stem)
    if vsmatch:
        base = vsmatch.group("base")
        if base in sibling_stems:
            hits.append((
                "REVIEW:variant_suffix",
                f"похоже на вариант/дубль базового модуля: {base}",
            ))

    if hits and path.resolve() in protected:
        hits = [
            (
                "REVIEW:config_referenced",
                f"путь явно упомянут в config.py (paths.*) — похоже на "
                f"мусор по имени, но это активный файл проекта; "
                f"исходное правило: {cat} ({reason})",
            )
            for cat, reason in hits
        ]

    return hits


def scan(root: Path, protected: set):
    all_files = [
        p for p in root.rglob("*")
        if p.is_file() and not any(part in SKIP_DIR_NAMES for part in p.parts)
    ]

    # для versioned_duplicate / variant_suffix нужно знать "соседей" по имени
    # в пределах той же папки
    by_dir_stems = {}
    for p in all_files:
        by_dir_stems.setdefault(p.parent, set()).add(p.stem)

    # для duplicate_doc_name — одинаковые имена .md в РАЗНЫХ папках проекта
    md_name_dirs = {}
    for p in all_files:
        if p.suffix.lower() == ".md":
            md_name_dirs.setdefault(p.name, set()).add(p.parent)
    doc_name_collisions = {name for name, dirs in md_name_dirs.items() if len(dirs) > 1}

    report_rows = []
    for p in all_files:
        stems_here = by_dir_stems.get(p.parent, set())
        hits = classify(p, root, stems_here, protected, doc_name_collisions)
        if not hits:
            continue
        size_kb = round(p.stat().st_size / 1024, 1)
        for category, reason in hits:
            report_rows.append({
                "path": str(p.relative_to(root)),
                "size_kb": size_kb,
                "category": category,
                "reason": reason,
            })
    return report_rows


def write_report(rows, out_path: Path):
    with out_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "size_kb", "category", "reason"])
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows):
    by_cat = {}
    size_by_cat = {}
    seen_paths_by_cat = {}
    for r in rows:
        cat = r["category"]
        seen_paths_by_cat.setdefault(cat, set()).add(r["path"])
    for cat, paths in seen_paths_by_cat.items():
        by_cat[cat] = len(paths)
    print("\n=== СВОДКА ===")
    total_unique = len({r["path"] for r in rows})
    print(f"Всего файлов, попавших под какое-то правило: {total_unique}")
    for cat in sorted(by_cat):
        print(f"  {cat:35s} {by_cat[cat]:5d} файлов")
    print()


def apply_moves(rows, root: Path, archive_root: Path, include_review: bool, log_path: Path):
    # один файл переносим один раз, даже если попал под несколько категорий
    unique_paths = {}
    for r in rows:
        is_high = r["category"].startswith("HIGH:")
        is_review = r["category"].startswith("REVIEW:")
        if is_high or (is_review and include_review):
            unique_paths.setdefault(r["path"], []).append(r["category"])

    moved = 0
    with log_path.open("w", encoding="utf-8") as log:
        log.write(f"# Перенос выполнен: {datetime.now().isoformat()}\n")
        log.write(f"# root={root} archive_root={archive_root}\n\n")
        for rel_path, cats in unique_paths.items():
            src = root / rel_path
            if not src.exists():
                continue
            dst = archive_root / rel_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            log.write(f"MOVED  {rel_path}  <- categories: {', '.join(cats)}\n")
            moved += 1
    print(f"Перенесено файлов: {moved}")
    print(f"Лог перемещений: {log_path}")
    print(f"Архив: {archive_root}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--root",
        default=None,
        help=(
            r'Путь к проекту, например "G:\Programming\Py\OSBB". '
            r"Можно не указывать, если задан --py-root с рабочим config.py — "
            r"тогда root возьмётся из paths.OSBB_ROOT."
        ),
    )
    ap.add_argument(
        "--py-root",
        default=r"G:\Programming\Py",
        help=(
            r'Каталог, где лежит ваш config.py (по умолчанию "G:\Programming\Py"). '
            r"Используется для авто-определения --root и для защиты файлов, "
            r"на которые config.py явно ссылается (paths.*), от переноса в архив."
        ),
    )
    ap.add_argument("--apply", action="store_true", help="Реально перенести файлы (по умолчанию — только отчёт)")
    ap.add_argument("--include-review", action="store_true", help="В --apply также переносить файлы категории REVIEW")
    ap.add_argument(
        "--archive-dir",
        default=None,
        help=(
            "Куда переносить. По умолчанию: "
            r'"<родитель root>\OSBB_util\output\triage_archive" '
            r'(например, для --root "G:\Programming\Py\OSBB" '
            r'это будет "G:\Programming\Py\OSBB_util\output\triage_archive")'
        ),
    )
    ap.add_argument("--report", default="osbb_triage_report.csv", help="Имя CSV-отчёта")
    args = ap.parse_args()

    cfg_paths = try_load_config(args.py_root)
    if cfg_paths is not None:
        print(f"config.py найден и загружен из: {args.py_root}")
    else:
        print(f"config.py не найден/не загрузился в: {args.py_root} (это не ошибка)")

    if args.root:
        root = Path(args.root).resolve()
    elif cfg_paths is not None:
        root = Path(cfg_paths.OSBB_ROOT).resolve()
        print(f"--root не задан, беру из config.py: {root}")
    else:
        print(
            "Не указан --root, и не удалось определить его автоматически из config.py.\n"
            r'Укажите явно: --root "G:\Programming\Py\OSBB"',
            file=sys.stderr,
        )
        sys.exit(1)

    if not root.exists():
        print(f"Папка не найдена: {root}", file=sys.stderr)
        sys.exit(1)

    protected = get_protected_paths(cfg_paths)
    if protected:
        print(f"Защищено от переноса (упомянуто в config.py): {len(protected)} путей")

    print(f"Сканирую: {root}")
    rows = scan(root, protected)

    report_path = Path(args.report).resolve()
    write_report(rows, report_path)
    print(f"Отчёт сохранён: {report_path}")
    summarize(rows)

    if not args.apply:
        print("Это был DRY-RUN. Файлы не тронуты.")
        print("Проверьте CSV-отчёт. Когда всё устроит — запустите с флагом --apply.")
        return

    if args.archive_dir:
        archive_root = Path(args.archive_dir).resolve()
    else:
        archive_root = root.parent / "OSBB_util" / "output" / "triage_archive"
    archive_root.mkdir(parents=True, exist_ok=True)
    log_path = archive_root / f"move_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    print(f"\nПрименяю перенос в: {archive_root}")
    if args.include_review:
        print("include-review включён: REVIEW-файлы тоже будут перенесены.")
    else:
        print("REVIEW-файлы НЕ переносятся (нужен флаг --include-review).")

    apply_moves(rows, root, archive_root, args.include_review, log_path)


if __name__ == "__main__":
    main()