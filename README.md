
# Metabase SSO & Provisioning Demo (Python + Flask)

A self‑contained JWT Single‑Sign‑On (SSO) gateway that lets you embed Metabase dashboards with a **“one Metabase user per client, many real users per client”** model.

---
## ✨ Key Features
- **Automatic client provisioning** – the first time a client logs in, the app creates a dedicated Metabase user account.
- **Unlimited real users per client** – map real‑world users to clients with `user_map.json`.
- **Client ⇢ Metabase e‑mail mapping** – define in `client_map.json`.
- **Fresh JWT on every iframe visit** – keeps sessions short‑lived and secure.
- **Per‑user context** – role, locale, and any other metadata are delivered via `attr.*` JWT claims.
- **Opinionated demo UI** – show clients, users, and an “Open Dashboard” action for quick testing.

---
## 🚀 Quick Start

1. **Clone** the repository
   ```bash
   git clone https://github.com/ignacio-mb/Interactive-embedding-jwt-user-provisioning-and-mapping.git
   cd interactive_embedding_and_jwt_provissioning
   ```
2. **Install** dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. **Run** the gateway
   ```bash
   python flask_backend/server.py
   ```
4. **Open** the demo UI at `http://localhost:9090/`.

---
## 🖥️  Demo UI Guide

| Pane | Description | Backing file |
|------|-------------|--------------|
| **Client Accounts** | Lists the Metabase email for each client. | `client_map.json` |
| **Users** | Shows real users associated with the selected client. | `user_map.json` |
| **View Dashboard** | Generates a one‑time JWT and redirects to `/dashboard/134`. | Route: `/api/auth` |

> Metabase validates the token, creates the client account if required, and embeds dashboard **#134** in the iframe.

---
## 🔍  How It Works

1. **/api/auth** receives `user_id` and `return_to` (e.g. `/dashboard/134`).
2. The gateway looks up:
   - the **client** for that user (`user_map.json`)
   - the **Metabase email** for that client (`client_map.json`)
3. It mints a **new JWT** with:
   ```json
   {
     "sub": "<metabase-email>",
     "attr": {
       "role": "viewer",
       "locale": "en-US"
     },
     "exp": <unix-timestamp>
   }
   ```
4. It responds with `302` ➜ `https://metabase.example.com/auth/...token...#return_to`.

Metabase handles the rest—provisioning and signin—before landing on the requested dashboard.

---
## ⚙️  Configuration Notes
| File | Purpose |
|------|---------|
| `client_map.json` | `{ "<client_id>": "<metabase-email>" }` |
| `user_map.json`   | `{ "<user_id>": { "name": "...", "client_id": "...", "role": "..." } }` |

Adjust dashboard ID, host, and signing key in `flask_backend/server.py`.

---
## 📝  License
MIT
