# OSBB Assistant Framework v1.0

Готовый пакет служебного инструмента OSBB. Сохраняет команды версии 0.3 и добавляет:

```text
assistant export resolver
```

## Установка

Скопируйте содержимое архива в:

```text
G:\Programming\Py\OSBB_util\
```

В результате должны появиться:

```text
OSBB_util\
├── Scripts\
│   ├── Assistant.py
│   └── osbb_assistant\
└── Exports\
```

Старый `Scripts\Assistant.py` будет заменён новым главным файлом. Перед заменой можно сохранить резервную копию.

## Запуск

Из `G:\Programming\Py`:

```powershell
python .\OSBB_util\Scripts\Assistant.py export resolver
```

Если у вас уже настроена команда `assistant`:

```powershell
assistant export resolver
```

Отчёт появится в:

```text
G:\Programming\Py\OSBB_util\Exports\resolver_export_YYYY-MM-DD_HHMMSS.md
```

## Параметры

```powershell
assistant export resolver --full
assistant export resolver --no-data
assistant export resolver --samples 10
assistant export resolver --db .\OSBB\path\database.db
assistant export resolver --output C:\Temp\OSBB
```

По умолчанию потенциально чувствительные поля в образцах (`phone`, `email`, `password`, `token` и подобные) скрываются. Для осознанного включения:

```powershell
assistant export resolver --include-sensitive
```

## Как выбирается база

Assistant рекурсивно ищет в `OSBB` файлы:

- `*.db`
- `*.sqlite`
- `*.sqlite3`

Из доступных SQLite-баз выбирается база с наибольшим количеством пользовательских таблиц. В отчёте сохраняется список всех найденных кандидатов и отмечается выбранная база.

## Сохранённые команды

```text
assistant check
assistant doctor
assistant report
assistant hash [файл]
assistant compare [файл]
assistant help
```
