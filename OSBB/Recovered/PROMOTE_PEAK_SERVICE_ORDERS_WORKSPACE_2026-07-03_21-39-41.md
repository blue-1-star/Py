# Promote peak service_orders_workspace

Generated: `2026-07-03 21:39:41`
Applied: `False`

## Source

`G:\Programming\Py\OSBB\Recovered_Releases\2026-06-27__OSBB_phone_barrier_access_v2_working_sandbox\phone_barrier_access_v2_payload\Bots\handlers\service_orders_workspace.py`
- SHA: `f28aa0d210f7`
- Size: `74980` bytes
- Syntax: `True` / `OK`

## Target

`G:\Programming\Py\OSBB\Bots\handlers\service_orders_workspace.py`
- SHA: `9f1d009c5525`
- Size: `83822` bytes

## Diff

`G:\Programming\Py\OSBB\Recovered\PROMOTE_PEAK_SERVICE_ORDERS_WORKSPACE_2026-07-03_21-39-41.patch`

## Markers in source

| Marker | Present |
|---|---:|
| `NEW_REMOTE_PROFILE` | yes |
| `REMOTE_NEW_PREORDER` | no |
| `choose_quantity` | yes |
| `supplier_batches` | yes |
| `issue_new_remotes_from_batch` | yes |
| `REMOTE_BATCH_ISSUED` | yes |
| `Заявки на пульты` | yes |
| `Телефонный доступ` | yes |
| `PHONE_ACCESS_CONNECT` | yes |
| `remote_supplier_batches` | no |
| `remote_supplier_batch_links` | no |
| `remote_order_issued_assets` | no |
| `service_preorders_core` | yes |

## Markers in target after operation

| Marker | Present |
|---|---:|
| `NEW_REMOTE_PROFILE` | yes |
| `REMOTE_NEW_PREORDER` | no |
| `choose_quantity` | yes |
| `supplier_batches` | yes |
| `issue_new_remotes_from_batch` | yes |
| `REMOTE_BATCH_ISSUED` | yes |
| `Заявки на пульты` | yes |
| `Телефонный доступ` | yes |
| `PHONE_ACCESS_CONNECT` | yes |
| `remote_supplier_batches` | no |
| `remote_supplier_batch_links` | no |
| `remote_order_issued_assets` | no |
| `service_preorders_core` | yes |

## Next checks

```powershell
python -m py_compile .\OSBB\Bots\handlers\service_orders_workspace.py
git diff -- OSBB/Bots/handlers/service_orders_workspace.py
git status --short
```

