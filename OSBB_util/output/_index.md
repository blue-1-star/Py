# 📊 Документация проекта OSBB

**Дата сборки:** 2026-07-13 20:50:56

---

## 📁 Глобальный vs Локальный

| Файл | Расположение | Назначение |
|------|--------------|------------|
| `config.py` | `G:/Programming/Py/` | **ГЛОБАЛЬНЫЙ** — для всего 프로екта |
| `local_config.py` | `G:/Programming/Py/OSBB_util/` | **ЛОКАЛЬНЫЙ** — только для утилит |

---

## 📁 Структура документации

### [01_project_tree](01_project_tree/)
Дерево каталогов проекта:
- [Полное дерево](01_project_tree/tree_full.txt) — все файлы с размерами и датами
- [Ограниченное дерево](01_project_tree/tree_limited.txt) — только структура
- [По глубине 2](01_project_tree/tree_depth_2.txt) — первые 2 уровня
- [По глубине 3](01_project_tree/tree_depth_3.txt) — первые 3 уровня

### [02_database](02_database/)
Документация базы данных:
- [Полная схема SQL](02_database/schema_full.sql) — CREATE TABLE
- [Сводная информация](02_database/schema_summary.txt) — список таблиц, связи
- [Связи между таблицами](02_database/relationships.txt) — внешние ключи
- [Документация таблиц](02_database/tables/) — по каждой таблице

### [03_code_analysis](03_code_analysis/)
Анализ кода (в разработке)

### [04_api_docs](04_api_docs/)
Документация API (в разработке)

### [05_reports](05_reports/)
Отчеты и анализ (в разработке)

### [06_archive](06_archive/)
Архив предыдущих версий

---

## 🚀 Как обновить документацию

```bash
cd G:/Programming/Py/OSBB_util
python scripts/build_report.py
```
