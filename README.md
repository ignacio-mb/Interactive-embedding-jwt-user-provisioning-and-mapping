Metabase SSO & Provisioning Demo  (Python + Flask)
==================================================

This repo is a self-contained **JWT SSO gateway** that lets you embed Metabase
dashboards with a “one Metabase user per client, many real users per client”
model.

Key features
------------
• **Auto-provision** one Metabase account the first time a client logs in
• Map unlimited real users → clients via `user_map.json`
• Map clients → Metabase e-mails via `client_map.json`
• Every iframe visit mints a fresh JWT and lands on dashboard **#134**
• Per-user context (`role`, `locale`, etc.) is delivered as JWT `attr.*` claims

Run it
python flask_backend/server.py

Demo UI
Visit http://localhost:9090/

• Left pane: Client Accounts list (data from client_map.json)
• Right pane: Users table (rows from user_map.json)
• Each row has “View Dashboard” → calls
/api/auth?user_id=<row>&return_to=/dashboard/134

Metabase validates the JWT, creates the client account if needed, and shows
dashboard #134 inside the iframe.