# Metabase SSO & Provisioning Demo (Python + Flask)

This project is a **self-contained SSO gateway** that lets you embed Metabase dashboards inside your app with **JWT SSO** and **per-client, per-user mapping**:

- **One Metabase account per client** (auto-provisioned on first SSO)
- **Many end-users per client** (mapped via `user_map.json`)
- **Per-user context** (role, locale, IDs) passed in JWT `attr.*` claims
- **Automatic redirect** into your Metabase dashboard (ID 134)

---

## ➤ What it does

1. **Loads two JSON maps** from your project root:
   - `user_map.json`: maps your real `user_id` → `client_id`
   - `client_map.json`: maps `client_id` → Metabase account email
2. **Exposes** a Flask endpoint:
   ```http
   GET /api/auth?
     user_id=<your_user>&
     [role=<analyst>]        ← optional
     [locale=<es>]           ← optional
     [return_to=/dash/134]   ← optional
