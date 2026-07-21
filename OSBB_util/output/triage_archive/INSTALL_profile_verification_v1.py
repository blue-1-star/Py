# -*- coding: utf-8 -*-
"""Install profile-verification sources; database migration is separate."""
from __future__ import annotations
import py_compile
import shutil
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PAYLOAD=ROOT/"profile_verification_payload"

def backup_and_copy(source:Path,target:Path,backup_root:Path,must_exist:bool)->Path|None:
    if not source.is_file(): raise FileNotFoundError(f"Payload file missing:\n{source}")
    if must_exist and not target.is_file(): raise FileNotFoundError(f"Expected project source missing:\n{target}")
    backup=None
    if target.exists():
        backup=backup_root/target.relative_to(ROOT); backup.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(target,backup)
    target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(source,target); py_compile.compile(str(target),doraise=True)
    return backup

def main()->int:
    files=[
        (PAYLOAD/"profile_verification_core.py",ROOT/"profile_verification_core.py",False),
        (PAYLOAD/"Bots"/"handlers"/"profile_verification_workspace.py",ROOT/"Bots"/"handlers"/"profile_verification_workspace.py",False),
        (PAYLOAD/"Bots"/"handlers"/"service_orders_workspace.py",ROOT/"Bots"/"handlers"/"service_orders_workspace.py",True),
        (PAYLOAD/"run_bot_live_services_sandbox_v1.py",ROOT/"run_bot_live_services_sandbox_v1.py",True),
    ]
    checks={ROOT/"Bots"/"handlers"/"service_orders_workspace.py":"def handle_service_orders_text(",ROOT/"run_bot_live_services_sandbox_v1.py":"def patch_bot_source()"}
    for target,marker in checks.items():
        if not target.is_file() or marker not in target.read_text(encoding="utf-8"):
            raise RuntimeError("Project source has unexpected structure; installation refused:\n"+str(target))
    stamp=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_root=ROOT/"Data"/"backups"/"source_code"/f"profile_verification_{stamp}"
    backup_root.mkdir(parents=True,exist_ok=False)
    completed=[]
    try:
        for source,target,must_exist in files:
            backup=backup_and_copy(source,target,backup_root,must_exist); completed.append((target,backup))
    except Exception:
        for target,backup in reversed(completed):
            if backup and backup.is_file(): shutil.copy2(backup,target)
            elif target.exists(): target.unlink()
        raise
    print("PROFILE VERIFICATION UI INSTALLATION COMPLETED")
    print("Backups:",backup_root)
    print("Database was not changed.")
    print("Next: RUN_MIGRATE_profile_verification_sandbox.bat")
    return 0
if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as exc:
        print("PROFILE VERIFICATION UI INSTALLATION FAILED:",type(exc).__name__+":",exc); raise SystemExit(1)
