r"""
Минимальное исправление кассы v2 после первого живого sandbox-теста.

Исправляет только две вещи:
1) Таблица charges старой схемы использует apartment_number, а не apartment_id:
   сценарий «Бумажка → квартира 174» больше не падает.
2) Исторический составной период 2026-05_2026-06 принимается вручную,
   а не отклоняется как неверный формат.

Скрипт не меняет БД, config.py и parking_bot.py.
При --apply меняется только cashier_v2_core.py, перед этим создаётся backup.

Проверка на sandbox без записи:
g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\patch_cashier_v2_core_period_and_schemafix.py --sandbox "G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db"

Применение к коду:
g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\patch_cashier_v2_core_period_and_schemafix.py --apply
"""

from __future__ import annotations

import argparse
import base64
import copy
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
BOTS_DIR = ROOT / "Bots"
CORE_FILE = ROOT / "cashier_v2_core.py"
SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"

NORMALIZE_PERIOD = base64.b64decode("CmRlZiBub3JtYWxpemVfcGVyaW9kKHZhbHVlOiBBbnksICosIHJlcXVpcmVkOiBib29sID0gRmFsc2UpIC0+IHN0ciB8IE5vbmU6CiAgICAiIiIKICAgIEFjY2VwdHMgYSBub3JtYWwgbW9udGggKDIwMjYtMDcpIGFuZCBhIGNvbXBvdW5kIGFjY291bnRpbmcgcGVyaW9kCiAgICAoMjAyNi0wNV8yMDI2LTA2KS4gQ29tcG91bmQgaGlzdG9yaWNhbCBwZXJpb2RzIG11c3QgYmUgcHJlc2VydmVkIGV4YWN0bHkuCiAgICAiIiIKICAgIHJhdyA9IHRleHQodmFsdWUpCiAgICBpZiByYXcgaW4geyIiLCAiLSIsICLQvdC1INGD0LrQsNC30LDQvSJ9OgogICAgICAgIGlmIHJlcXVpcmVkOgogICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKAogICAgICAgICAgICAgICAgItCj0LrQsNC20LjRgtC1INC/0LXRgNC40L7QtDog0JPQk9CT0JMt0JzQnCDQuNC70Lgg0JPQk9CT0JMt0JzQnF/Qk9CT0JPQky3QnNCcLiIKICAgICAgICAgICAgKQogICAgICAgIHJldHVybiBOb25lCgogICAgcmF3ID0gcmF3LnJlcGxhY2UoIuKAkyIsICJfIikucmVwbGFjZSgi4oCUIiwgIl8iKS5yZXBsYWNlKCIvIiwgIl8iKQogICAgcmF3ID0gcmUuc3ViKHIiXHMrIiwgIiIsIHJhdykKCiAgICBzaW5nbGUgPSByZS5mdWxsbWF0Y2gociIoXGR7NH0pWy4tXShcZHsxLDJ9KSIsIHJhdykKICAgIGlmIHNpbmdsZToKICAgICAgICB5ZWFyLCBtb250aCA9IGludChzaW5nbGUuZ3JvdXAoMSkpLCBpbnQoc2luZ2xlLmdyb3VwKDIpKQogICAgICAgIGlmIDEgPD0gbW9udGggPD0gMTI6CiAgICAgICAgICAgIHJldHVybiBmInt5ZWFyOjA0ZH0te21vbnRoOjAyZH0iCgogICAgcGVyaW9kX3JhbmdlID0gcmUuZnVsbG1hdGNoKAogICAgICAgIHIiKFxkezR9KVsuLV0oXGR7MSwyfSlfKFxkezR9KVsuLV0oXGR7MSwyfSkiLAogICAgICAgIHJhdywKICAgICkKICAgIGlmIHBlcmlvZF9yYW5nZToKICAgICAgICB5MSwgbTEsIHkyLCBtMiA9IG1hcChpbnQsIHBlcmlvZF9yYW5nZS5ncm91cHMoKSkKICAgICAgICBpZiAxIDw9IG0xIDw9IDEyIGFuZCAxIDw9IG0yIDw9IDEyOgogICAgICAgICAgICByZXR1cm4gZiJ7eTE6MDRkfS17bTE6MDJkfV97eTI6MDRkfS17bTI6MDJkfSIKCiAgICByYWlzZSBWYWx1ZUVycm9yKAogICAgICAgICLQn9C10YDQuNC+0LQ6INCT0JPQk9CTLdCc0Jwg0LjQu9C4INCT0JPQk9CTLdCc0Jxf0JPQk9CT0JMt0JzQnCwgIgogICAgICAgICLQvdCw0L/RgNC40LzQtdGAIDIwMjYtMDVfMjAyNi0wNi4iCiAgICApCg==").decode("utf-8")
OPEN_CHARGES = base64.b64decode("CmRlZiBvcGVuX2NoYXJnZXMoCiAgICAqLAogICAgYXBhcnRtZW50X2lkOiBpbnQgfCBOb25lID0gTm9uZSwKICAgIGFwYXJ0bWVudF9udW1iZXI6IHN0ciB8IE5vbmUgPSBOb25lLAogICAgZW50cmFuY2VfbnVtYmVyOiBzdHIgfCBOb25lID0gTm9uZSwKICAgIHBlcmlvZF9jb2RlOiBzdHIgfCBOb25lID0gTm9uZSwKICAgIHNlcnZpY2VfY29kZTogc3RyIHwgTm9uZSA9IE5vbmUsCiAgICBzZXJ2aWNlX2l0ZW1fY29kZTogc3RyIHwgTm9uZSA9IE5vbmUsCikgLT4gbGlzdFtkaWN0XToKICAgICIiIgogICAgUmV0dXJuIG9wZW4gY2hhcmdlcyB1c2luZyB0aGUgc2NoZW1hIGFjdHVhbGx5IHByZXNlbnQgaW4gdGhlIGRhdGFiYXNlLgoKICAgIE9sZGVyIE9TQkIgYmlsbGluZyB0YWJsZXMgaWRlbnRpZnkgYSBjaGFyZ2Ugb25seSBieSBhcGFydG1lbnRfbnVtYmVyOwogICAgbmV3ZXIgb25lcyBtYXkgYWxzbyBoYXZlIGFwYXJ0bWVudF9pZC4gVGhpcyBmdW5jdGlvbiBzdXBwb3J0cyBib3RoLgogICAgIiIiCiAgICBjb25uID0gZ2V0X2Nvbm4oKQogICAgdHJ5OgogICAgICAgIGN1ciA9IGNvbm4uY3Vyc29yKCkKICAgICAgICBpZiBub3QgdGFibGVfZXhpc3RzKGN1ciwgImNoYXJnZXMiKSBvciBub3QgdGFibGVfZXhpc3RzKGN1ciwgInBheW1lbnRfYWxsb2NhdGlvbnMiKToKICAgICAgICAgICAgcmV0dXJuIFtdCgogICAgICAgIGNjb2xzID0gdGFibGVfY29sdW1ucyhjdXIsICJjaGFyZ2VzIikKICAgICAgICBhY29scyA9IHRhYmxlX2NvbHVtbnMoY3VyLCAiYXBhcnRtZW50cyIpCiAgICAgICAgYWxsb2NhdGlvbl9jb2wgPSBhbGxvY2F0aW9uX2Ftb3VudF9jb2x1bW4oY3VyKQogICAgICAgIGlmIG5vdCBhbGxvY2F0aW9uX2NvbCBvciAiYW1vdW50IiBub3QgaW4gY2NvbHM6CiAgICAgICAgICAgIHJldHVybiBbXQoKICAgICAgICBoYXNfY2hhcmdlX2FwYXJ0bWVudF9pZCA9ICJhcGFydG1lbnRfaWQiIGluIGNjb2xzCiAgICAgICAgaGFzX2NoYXJnZV9hcGFydG1lbnRfbnVtYmVyID0gImFwYXJ0bWVudF9udW1iZXIiIGluIGNjb2xzCiAgICAgICAgaGFzX2FwYXJ0bWVudF9udW1iZXIgPSAiYXBhcnRtZW50X251bWJlciIgaW4gYWNvbHMKCiAgICAgICAgam9pbl9zcWwgPSAiIgogICAgICAgIGpvaW5lZF9hcGFydG1lbnRzID0gRmFsc2UKICAgICAgICBpZiBoYXNfY2hhcmdlX2FwYXJ0bWVudF9pZDoKICAgICAgICAgICAgaWYgZW50cmFuY2VfbnVtYmVyOgogICAgICAgICAgICAgICAgam9pbl9zcWwgPSAiTEVGVCBKT0lOIGFwYXJ0bWVudHMgYSBPTiBhLmlkID0gYy5hcGFydG1lbnRfaWQiCiAgICAgICAgICAgICAgICBqb2luZWRfYXBhcnRtZW50cyA9IFRydWUKICAgICAgICBlbGlmIGhhc19jaGFyZ2VfYXBhcnRtZW50X251bWJlciBhbmQgaGFzX2FwYXJ0bWVudF9udW1iZXI6CiAgICAgICAgICAgIGpvaW5fc3FsID0gKAogICAgICAgICAgICAgICAgIkxFRlQgSk9JTiBhcGFydG1lbnRzIGEgIgogICAgICAgICAgICAgICAgIk9OIENBU1QoYS5hcGFydG1lbnRfbnVtYmVyIEFTIFRFWFQpID0gIgogICAgICAgICAgICAgICAgIkNBU1QoYy5hcGFydG1lbnRfbnVtYmVyIEFTIFRFWFQpIgogICAgICAgICAgICApCiAgICAgICAgICAgIGpvaW5lZF9hcGFydG1lbnRzID0gVHJ1ZQoKICAgICAgICBmaWx0ZXJzOiBsaXN0W3N0cl0gPSBbXQogICAgICAgIHBhcmFtczogbGlzdFtBbnldID0gW10KICAgICAgICB1bml0X2ZpbHRlcl9hZGRlZCA9IEZhbHNlCgogICAgICAgIGlmIGFwYXJ0bWVudF9pZCBpcyBub3QgTm9uZToKICAgICAgICAgICAgaWYgaGFzX2NoYXJnZV9hcGFydG1lbnRfaWQ6CiAgICAgICAgICAgICAgICBmaWx0ZXJzLmFwcGVuZCgiYy5hcGFydG1lbnRfaWQgPSA/IikKICAgICAgICAgICAgICAgIHBhcmFtcy5hcHBlbmQoaW50KGFwYXJ0bWVudF9pZCkpCiAgICAgICAgICAgICAgICB1bml0X2ZpbHRlcl9hZGRlZCA9IFRydWUKICAgICAgICAgICAgZWxpZiBqb2luZWRfYXBhcnRtZW50czoKICAgICAgICAgICAgICAgIGZpbHRlcnMuYXBwZW5kKCJhLmlkID0gPyIpCiAgICAgICAgICAgICAgICBwYXJhbXMuYXBwZW5kKGludChhcGFydG1lbnRfaWQpKQogICAgICAgICAgICAgICAgdW5pdF9maWx0ZXJfYWRkZWQgPSBUcnVlCgogICAgICAgIGlmIG5vdCB1bml0X2ZpbHRlcl9hZGRlZCBhbmQgYXBhcnRtZW50X251bWJlcjoKICAgICAgICAgICAgaWYgaGFzX2NoYXJnZV9hcGFydG1lbnRfbnVtYmVyOgogICAgICAgICAgICAgICAgZmlsdGVycy5hcHBlbmQoIkNBU1QoYy5hcGFydG1lbnRfbnVtYmVyIEFTIFRFWFQpID0gPyIpCiAgICAgICAgICAgICAgICBwYXJhbXMuYXBwZW5kKHRleHQoYXBhcnRtZW50X251bWJlcikpCiAgICAgICAgICAgICAgICB1bml0X2ZpbHRlcl9hZGRlZCA9IFRydWUKICAgICAgICAgICAgZWxpZiBqb2luZWRfYXBhcnRtZW50cyBhbmQgaGFzX2FwYXJ0bWVudF9udW1iZXI6CiAgICAgICAgICAgICAgICBmaWx0ZXJzLmFwcGVuZCgiQ0FTVChhLmFwYXJ0bWVudF9udW1iZXIgQVMgVEVYVCkgPSA/IikKICAgICAgICAgICAgICAgIHBhcmFtcy5hcHBlbmQodGV4dChhcGFydG1lbnRfbnVtYmVyKSkKICAgICAgICAgICAgICAgIHVuaXRfZmlsdGVyX2FkZGVkID0gVHJ1ZQoKICAgICAgICBpZiBlbnRyYW5jZV9udW1iZXI6CiAgICAgICAgICAgIGVudHJhbmNlX2NvbCA9ICgKICAgICAgICAgICAgICAgICJlbnRyYW5jZV9udW1iZXIiIGlmICJlbnRyYW5jZV9udW1iZXIiIGluIGFjb2xzCiAgICAgICAgICAgICAgICBlbHNlICJlbnRyYW5jZSIgaWYgImVudHJhbmNlIiBpbiBhY29scwogICAgICAgICAgICAgICAgZWxzZSBOb25lCiAgICAgICAgICAgICkKICAgICAgICAgICAgaWYgbm90IGpvaW5lZF9hcGFydG1lbnRzIG9yIG5vdCBlbnRyYW5jZV9jb2w6CiAgICAgICAgICAgICAgICByZXR1cm4gW10KICAgICAgICAgICAgZmlsdGVycy5hcHBlbmQoZiJDQVNUKGEue2VudHJhbmNlX2NvbH0gQVMgVEVYVCkgPSA/IikKICAgICAgICAgICAgcGFyYW1zLmFwcGVuZCh0ZXh0KGVudHJhbmNlX251bWJlcikpCiAgICAgICAgICAgIHVuaXRfZmlsdGVyX2FkZGVkID0gVHJ1ZQoKICAgICAgICBpZiBub3QgdW5pdF9maWx0ZXJfYWRkZWQ6CiAgICAgICAgICAgIHJldHVybiBbXQoKICAgICAgICBpZiBwZXJpb2RfY29kZSBhbmQgInBlcmlvZF9jb2RlIiBpbiBjY29sczoKICAgICAgICAgICAgZmlsdGVycy5hcHBlbmQoIkNBU1QoYy5wZXJpb2RfY29kZSBBUyBURVhUKSA9ID8iKQogICAgICAgICAgICBwYXJhbXMuYXBwZW5kKHRleHQocGVyaW9kX2NvZGUpKQogICAgICAgIGlmIHNlcnZpY2VfY29kZSBhbmQgInNlcnZpY2VfY29kZSIgaW4gY2NvbHM6CiAgICAgICAgICAgIGZpbHRlcnMuYXBwZW5kKCJjLnNlcnZpY2VfY29kZSA9ID8iKQogICAgICAgICAgICBwYXJhbXMuYXBwZW5kKHNlcnZpY2VfY29kZSkKICAgICAgICBpZiBzZXJ2aWNlX2l0ZW1fY29kZSBhbmQgInNlcnZpY2VfaXRlbV9jb2RlIiBpbiBjY29sczoKICAgICAgICAgICAgZmlsdGVycy5hcHBlbmQoImMuc2VydmljZV9pdGVtX2NvZGUgPSA/IikKICAgICAgICAgICAgcGFyYW1zLmFwcGVuZChzZXJ2aWNlX2l0ZW1fY29kZSkKCiAgICAgICAgc3RhdHVzX3NxbCA9ICgKICAgICAgICAgICAgIkFORCBDT0FMRVNDRShjLmNoYXJnZV9zdGF0dXMsICcnKSA8PiAnY2FuY2VsbGVkJyIKICAgICAgICAgICAgaWYgImNoYXJnZV9zdGF0dXMiIGluIGNjb2xzCiAgICAgICAgICAgIGVsc2UgKAogICAgICAgICAgICAgICAgIkFORCBDT0FMRVNDRShjLnN0YXR1cywgJycpIDw+ICdjYW5jZWxsZWQnIgogICAgICAgICAgICAgICAgaWYgInN0YXR1cyIgaW4gY2NvbHMgZWxzZSAiIgogICAgICAgICAgICApCiAgICAgICAgKQoKICAgICAgICBhcGFydG1lbnRfaWRfZXhwciA9ICgKICAgICAgICAgICAgImMuYXBhcnRtZW50X2lkIgogICAgICAgICAgICBpZiBoYXNfY2hhcmdlX2FwYXJ0bWVudF9pZAogICAgICAgICAgICBlbHNlICJhLmlkIgogICAgICAgICAgICBpZiBqb2luZWRfYXBhcnRtZW50cwogICAgICAgICAgICBlbHNlICJOVUxMIgogICAgICAgICkKICAgICAgICBhcGFydG1lbnRfbnVtYmVyX2V4cHIgPSAoCiAgICAgICAgICAgICJDT0FMRVNDRShhLmFwYXJ0bWVudF9udW1iZXIsIGMuYXBhcnRtZW50X251bWJlcikiCiAgICAgICAgICAgIGlmIGpvaW5lZF9hcGFydG1lbnRzIGFuZCBoYXNfY2hhcmdlX2FwYXJ0bWVudF9udW1iZXIKICAgICAgICAgICAgZWxzZSAiYy5hcGFydG1lbnRfbnVtYmVyIgogICAgICAgICAgICBpZiBoYXNfY2hhcmdlX2FwYXJ0bWVudF9udW1iZXIKICAgICAgICAgICAgZWxzZSAiYS5hcGFydG1lbnRfbnVtYmVyIgogICAgICAgICAgICBpZiBqb2luZWRfYXBhcnRtZW50cyBhbmQgaGFzX2FwYXJ0bWVudF9udW1iZXIKICAgICAgICAgICAgZWxzZSAiTlVMTCIKICAgICAgICApCiAgICAgICAgcGVyaW9kX2V4cHIgPSAiYy5wZXJpb2RfY29kZSIgaWYgInBlcmlvZF9jb2RlIiBpbiBjY29scyBlbHNlICJOVUxMIgogICAgICAgIHNlcnZpY2VfZXhwciA9ICJjLnNlcnZpY2VfY29kZSIgaWYgInNlcnZpY2VfY29kZSIgaW4gY2NvbHMgZWxzZSAiTlVMTCIKICAgICAgICBpdGVtX2V4cHIgPSAiYy5zZXJ2aWNlX2l0ZW1fY29kZSIgaWYgInNlcnZpY2VfaXRlbV9jb2RlIiBpbiBjY29scyBlbHNlICJOVUxMIgoKICAgICAgICBjdXIuZXhlY3V0ZSgKICAgICAgICAgICAgZiIiIgogICAgICAgICAgICBTRUxFQ1QKICAgICAgICAgICAgICAgIGMuaWQgQVMgY2hhcmdlX2lkLAogICAgICAgICAgICAgICAge2FwYXJ0bWVudF9pZF9leHByfSBBUyBhcGFydG1lbnRfaWQsCiAgICAgICAgICAgICAgICB7YXBhcnRtZW50X251bWJlcl9leHByfSBBUyBhcGFydG1lbnRfbnVtYmVyLAogICAgICAgICAgICAgICAge3BlcmlvZF9leHByfSBBUyBwZXJpb2RfY29kZSwKICAgICAgICAgICAgICAgIHtzZXJ2aWNlX2V4cHJ9IEFTIHNlcnZpY2VfY29kZSwKICAgICAgICAgICAgICAgIHtpdGVtX2V4cHJ9IEFTIHNlcnZpY2VfaXRlbV9jb2RlLAogICAgICAgICAgICAgICAgYy5hbW91bnQgQVMgY2hhcmdlX2Ftb3VudCwKICAgICAgICAgICAgICAgIENPQUxFU0NFKFNVTShwYS57YWxsb2NhdGlvbl9jb2x9KSwgMCkgQVMgYWxsb2NhdGVkX2Ftb3VudAogICAgICAgICAgICBGUk9NIGNoYXJnZXMgYwogICAgICAgICAgICB7am9pbl9zcWx9CiAgICAgICAgICAgIExFRlQgSk9JTiBwYXltZW50X2FsbG9jYXRpb25zIHBhIE9OIHBhLmNoYXJnZV9pZCA9IGMuaWQKICAgICAgICAgICAgV0hFUkUgeycgQU5EICcuam9pbihmaWx0ZXJzKX0KICAgICAgICAgICAge3N0YXR1c19zcWx9CiAgICAgICAgICAgIEdST1VQIEJZIGMuaWQKICAgICAgICAgICAgSEFWSU5HIGMuYW1vdW50IC0gQ09BTEVTQ0UoU1VNKHBhLnthbGxvY2F0aW9uX2NvbH0pLCAwKSA+IDAuMDAwMDEKICAgICAgICAgICAgT1JERVIgQlkgQ09BTEVTQ0Uoe2FwYXJ0bWVudF9udW1iZXJfZXhwcn0sICcnKSwgYy5pZAogICAgICAgICAgICAiIiIsCiAgICAgICAgICAgIHR1cGxlKHBhcmFtcyksCiAgICAgICAgKQoKICAgICAgICByZXN1bHQgPSBbXQogICAgICAgIGZvciByb3cgaW4gY3VyLmZldGNoYWxsKCk6CiAgICAgICAgICAgIGl0ZW0gPSBkaWN0KHJvdykKICAgICAgICAgICAgaXRlbVsiY2hhcmdlX2Ftb3VudCJdID0gZmxvYXQoaXRlbVsiY2hhcmdlX2Ftb3VudCJdIG9yIDApCiAgICAgICAgICAgIGl0ZW1bImFsbG9jYXRlZF9hbW91bnQiXSA9IGZsb2F0KGl0ZW1bImFsbG9jYXRlZF9hbW91bnQiXSBvciAwKQogICAgICAgICAgICBpdGVtWyJvdXRzdGFuZGluZ19hbW91bnQiXSA9IHJvdW5kKAogICAgICAgICAgICAgICAgbWF4KDAuMCwgaXRlbVsiY2hhcmdlX2Ftb3VudCJdIC0gaXRlbVsiYWxsb2NhdGVkX2Ftb3VudCJdKSwKICAgICAgICAgICAgICAgIDIsCiAgICAgICAgICAgICkKICAgICAgICAgICAgcmVzdWx0LmFwcGVuZChpdGVtKQogICAgICAgIHJldHVybiByZXN1bHQKICAgIGZpbmFsbHk6CiAgICAgICAgY29ubi5jbG9zZSgpCg==").decode("utf-8")


def replace_between(source: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = source.find(start_marker)
    if start < 0:
        raise RuntimeError(f"Не найден блок начала: {start_marker}")
    end = source.find(end_marker, start)
    if end < 0:
        raise RuntimeError(f"Не найден блок конца: {end_marker}")
    return source[:start] + replacement.rstrip() + "\n\n" + source[end:]


def patched_source(source: str) -> str:
    source = replace_between(
        source,
        "def normalize_period(",
        "def get_db_file(",
        NORMALIZE_PERIOD,
    )
    source = replace_between(
        source,
        "def open_charges(",
        "def suggested_charge(",
        OPEN_CHARGES,
    )
    return source


def clone_paths(original, sandbox_db: Path):
    try:
        cloned = copy.copy(original)
        if cloned is original:
            raise RuntimeError
    except Exception:
        fields = {}
        for name in dir(original):
            if name.startswith("_"):
                continue
            value = getattr(original, name)
            if not callable(value):
                fields[name] = value
        cloned = SimpleNamespace(**fields)
    try:
        setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
    except Exception:
        object.__setattr__(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
    return cloned


def run_sandbox_check(source: str, sandbox_db: Path) -> tuple[str, int]:
    try:
        sandbox_db.resolve().relative_to(SANDBOX_DIR.resolve())
    except ValueError as exc:
        raise ValueError("Разрешена только БД из Data\\db\\sandbox.") from exc

    for folder in (ROOT, BOTS_DIR, ROOT.parent):
        if str(folder) not in sys.path:
            sys.path.insert(0, str(folder))

    import config
    config.paths = clone_paths(config.paths, sandbox_db)
    config.USE_TEST_DB = True
    os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
    os.environ["OSBB_SANDBOX_MODE"] = "1"

    for module_name in [
        "cashier_v2_core",
        "handlers.cashier_operator",
        "db_access",
        "audit_logger",
    ]:
        sys.modules.pop(module_name, None)

    module = type(sys)("cashier_v2_core")
    module.__file__ = str(CORE_FILE)
    sys.modules["cashier_v2_core"] = module
    exec(compile(source, str(CORE_FILE), "exec"), module.__dict__)

    period = module.normalize_period("2026-05_2026-06", required=True)
    rows = module.open_charges(
        apartment_number="174",
        period_code=period,
    )
    return period, len(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sandbox", help="Путь к .db внутри Data\\db\\sandbox")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=" * 100)
    print("CASHIER V2 CORE: LEGACY CHARGES + COMPOUND PERIOD FIX")
    print("=" * 100)
    print("Core:", CORE_FILE)
    print("Apply:", args.apply)

    if not CORE_FILE.exists():
        print("Не найден файл:", CORE_FILE)
        return 1

    original = CORE_FILE.read_text(encoding="utf-8")
    try:
        fixed = patched_source(original)
        compile(fixed, str(CORE_FILE), "exec")
        print("Code patch: OK (compiled in memory)")
    except Exception:
        print("Code patch: FAILED")
        traceback.print_exc()
        return 1

    if args.sandbox:
        try:
            sandbox_db = Path(args.sandbox).resolve()
            if not sandbox_db.exists():
                raise FileNotFoundError(f"Не найдена sandbox-БД: {sandbox_db}")
            period, rows = run_sandbox_check(fixed, sandbox_db)
            print("Sandbox read-only smoke-test: OK")
            print("  compound period accepted:", period)
            print("  query for apartment 174 completed; open rows:", rows)
        except Exception:
            print("Sandbox read-only smoke-test: FAILED")
            traceback.print_exc()
            return 1

    if not args.apply:
        print("DRY RUN COMPLETED - NO FILES AND NO DATABASES WERE CHANGED")
        return 0

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = CORE_FILE.with_name(
        f"{CORE_FILE.stem}_before_period_schemafix_{stamp}{CORE_FILE.suffix}"
    )
    backup.write_text(original, encoding="utf-8")
    CORE_FILE.write_text(fixed, encoding="utf-8")
    print("APPLIED")
    print("Backup:", backup)
    print("Updated:", CORE_FILE)
    print("No database, config.py, or parking_bot.py was changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
