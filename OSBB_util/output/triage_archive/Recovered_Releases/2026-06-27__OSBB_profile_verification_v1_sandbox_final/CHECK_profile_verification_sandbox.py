# -*- coding: utf-8 -*-
"""Read-only check for resident profile verification sandbox schema."""
from __future__ import annotations
import sqlite3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SANDBOX_DB=ROOT/"Data"/"db"/"sandbox"/"osbb_test_live_services_2026-06-26_20-13-26.db"

def main() -> int:
    if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
    from profile_verification_core import PROFILE_POLICY_SET, PROFILE_SCHEMA_MIGRATION_CODE
    print("OSBB resident profile verification sandbox check")
    print("Read-only check.")
    print("Database:",SANDBOX_DB)
    if not SANDBOX_DB.is_file(): raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")
    conn=sqlite3.connect(SANDBOX_DB)
    try:
        tables={r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        required={"resident_profile_schema_migrations","resident_profile_policy_versions","resident_profile_policy_values","resident_profile_verifications","resident_profile_change_requests","resident_profile_operation_journal"}
        missing=required-tables
        if missing: raise RuntimeError("Missing tables: "+", ".join(sorted(missing)))
        marker=conn.execute("SELECT migration_code FROM resident_profile_schema_migrations WHERE migration_code=?",(PROFILE_SCHEMA_MIGRATION_CODE,)).fetchone()
        if not marker: raise RuntimeError("Migration marker is absent.")
        policy=conn.execute("SELECT id,version_number,effective_from FROM resident_profile_policy_versions WHERE policy_set_code=? AND policy_status='ACTIVE' ORDER BY effective_from DESC,version_number DESC LIMIT 1",(PROFILE_POLICY_SET,)).fetchone()
        if not policy: raise RuntimeError("Active resident-profile policy is absent.")
        print("Result: schema and migration marker present")
        print()
        print(f"Active policy: {PROFILE_POLICY_SET} v{policy[1]} | from {policy[2]}")
        for row in conn.execute("SELECT setting_code,value_text FROM resident_profile_policy_values WHERE policy_version_id=? ORDER BY setting_code",(int(policy[0]),)):
            print(f" - {row[0]} = {row[1]}")
        print()
        print("Profile rows:",conn.execute("SELECT COUNT(*) FROM resident_profile_verifications").fetchone()[0])
        print("Open correction requests:",conn.execute("SELECT COUNT(*) FROM resident_profile_change_requests WHERE request_status='PENDING_OPERATOR'").fetchone()[0])
        print()
        print("CHECK COMPLETED")
        return 0
    finally: conn.close()
if __name__=="__main__": raise SystemExit(main())
