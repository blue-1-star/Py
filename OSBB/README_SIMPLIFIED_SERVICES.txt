OSBB — simplified services / paid preorders
============================================

This bundle replaces the old “request -> manual payment link -> stock reserve”
route for NEW REMOTES with this operational route:

1. Resident selects new remote(s) and quantity.
2. The record is only an INTEREST until a cashier/bank payment is confirmed.
3. The resident creates one payment notice; the cashier confirms money in the
   existing cashier flow.
4. On the next entry to “Remotes and access” or “Service operator”, the system
   automatically promotes that paid interest to a real paid service order.
   There is NO “Link payment” button in the new flow.
5. Paid orders are aggregated by remote type in “Supplier demand”.
6. Operator creates one supplier batch covering all currently paid orders.
7. When delivery arrives, operator enters the received quantity.
8. An order becomes ready only when the delivery has enough remotes for its
   whole quantity. At issue time, physical assets are created and auditable
   movements are recorded.

Own remote reprogramming and phone access use the same simple principle:
- the operational order is made only after payment is confirmed;
- the operator then receives/reprograms/returns the resident remote, or
  activates phone access.

Important limitation of this edition
------------------------------------
This bundle removes manual payment linking from the services screen through
automatic reconciliation of the confirmed payment notice.

The final one-screen front-desk action “receive cash + take resident remote”
requires changes inside the cashier v2 module itself, so that its receipt
creation can call the service workflow in the same database transaction. That
cashier file was not available in this chat and is intentionally NOT guessed.
The current result already removes the resident-facing and service-operator
payment-link step safely.

INSTALL — live-services SANDBOX ONLY
-------------------------------------
1. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C.
2. Copy the contents of this archive directly into:
       G:\Programming\Py\OSBB\
   Confirm replacement of exactly:
       service_orders_core.py
       Bots\handlers\service_orders_workspace.py
3. Keep the new file:
       service_preorders_core.py
4. Run:
       RUN_MIGRATE_simplified_services_sandbox.bat
   It creates a backup of only:
       Data\db\sandbox\osbb_test_live_services_2026-06-26_20-13-26.db
5. Start the existing:
       Start_OSBB_Live_Services_Sandbox_Bot_v1.bat

DO NOT run the migration against osbb.db or the old Guard Sandbox.

Sandbox test sequence for new remotes x2
----------------------------------------
Resident:
  Client mode -> Remotes -> Get new remotes -> 2 -> Record intent
  -> Pay cash at O / Report bank payment.

Cashier:
  Confirm that one payment notice by the normal cashier v2 screen.

Then service operator:
  Service operator -> Paid orders.
  The paid order should exist automatically and show “Awaiting supplier order”.
  Supplier demand -> choose the remote type -> creates one supplier batch.
  Remote deliveries -> choose batch -> Receive delivery -> enter 2.
  Paid orders -> order -> Issue new remotes to resident.

Phone-access test
-----------------
Resident creates the intent and payment notice. After cash confirmation, the
real order is made automatically. The operator sees one remaining action:
“Activate phone access”. Use a dedicated test number, not a live resident
number, during sandbox testing.

Optional sandbox cleanup
------------------------
The old unfinished “TEST — new remote” orders use the abandoned per-unit
reservation workflow. Before the new test, run:
  RUN_RETIRE_legacy_new_remote_test_orders_sandbox.bat

It only retires UNPAID records from the old REMOTE_NEW_FROM_STOCK test path,
releases TEST-NEW-* reservations, never deletes history, and creates a backup.
