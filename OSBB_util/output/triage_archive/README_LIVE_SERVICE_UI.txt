OSBB — live sandbox UI for services, remotes and phone access

Extract this archive into:
G:\Programming\Py\OSBB

It will place:
- root scripts in the project root;
- client_portal_v3.py and service_orders_workspace.py in Bots\handlers.

Then, in this exact order:
1) stop any Telegram bot instance;
2) run install_service_orders_ui.py --apply once;
3) run prepare_live_service_test.py --from-launcher --user 210312208 --apply once;
4) start Start_OSBB_Live_Service_Sandbox_Bot.bat.

This package is only for the isolated live sandbox created previously.
The test catalog uses clearly marked TEST services with prices 1/2/3/4 UAH.
No production or base test database is changed by the installer or runner.
