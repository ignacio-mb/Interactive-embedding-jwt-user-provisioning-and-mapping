# Metabase SSO Demo (Python + Flask)

End-to-end example that **provisions users**, **adds them to groups**, **sets user attributes**, and **signs them straight into Metabase** via JWT SSO—all in a single redirect.

> Tested with Metabase 0.48 and later (open-source, Pro, and Enterprise).

---

## ➤ Quick start

```bash

# create your secret config
cp .env.example .env          # then edit .env

# install backend deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# run it
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python flask_backend/server.py   # http://localhost:9090
# Interactive-embedding-jwt-user-provisioning-and-mapping
