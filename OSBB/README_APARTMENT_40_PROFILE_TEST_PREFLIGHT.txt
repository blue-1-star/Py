OSBB — read-only preflight for profile test on apartment 40
=============================================================

Purpose
-------
This is the safe first step before testing the missing parking_time flow.

It examines apartment 40 in the live-services sandbox database only and
prints:
- the matched apartment record;
- linked vehicles;
- plate, model, colour and parking_time;
- whether apartment 40 is suitable for an isolated sandbox test.

Safety
------
The script opens the database with:

    mode=ro
    PRAGMA query_only = ON

Therefore it cannot:
- create a resident profile;
- create welcome_shown_at;
- create a profile confirmation;
- create a resident change request;
- create an order/payment/subscription;
- change vehicles.parking_time;
- create an audit event.

How to run
----------
1. You do not need to start the bot.
2. Unpack the archive directly into:

   G:\Programming\Py\OSBB\

3. Run:

   RUN_CHECK_profile_test_candidate_apartment_40.bat

Expected useful result
----------------------
If apartment 40 really has a linked vehicle with empty parking_time:

    Test suitability: SUITABLE_MISSING_PARKING_TIME

Then the next module will create an isolated operator TEST session for this
apartment. That session will be labelled TEST and will not touch the resident's
profile or original vehicle data unless you later explicitly approve a real
correction.

Do not use client mode / change apartment / verify my data for apartment 40.
