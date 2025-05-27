"""
Flask SSO gateway for Metabase:
 - one MB account per client (via client_map.json)
 - many end-users per client (via user_map.json)
 - per-user context in JWT attributes

Env-vars in repo-root `.env`:
  METABASE_URL                          e.g. https://analytics.mycompany.com
  JWT_SIGNING_KEY_INTERACTIVE_EMBEDDING your Metabase JWT secret
"""

import os
import time
import json
from pathlib import Path
from typing import Dict, Any
from urllib.parse import urlencode

import jwt
from flask import Flask, request, redirect, abort, send_from_directory
from dotenv import load_dotenv

# ─────────────────── Load config & maps ─────────────────── #
load_dotenv()

PROJECT_ROOT = Path.cwd()
STATIC_PATH  = PROJECT_ROOT / "frontend"

METABASE_URL = os.getenv("METABASE_URL", "").rstrip("/")
JWT_SECRET   = os.getenv("JWT_SIGNING_KEY_INTERACTIVE_EMBEDDING")

if not (METABASE_URL and JWT_SECRET):
    raise RuntimeError(
        "Please set METABASE_URL and JWT_SIGNING_KEY_INTERACTIVE_EMBEDDING in .env"
    )

# load user→client map
USER_MAP_PATH = PROJECT_ROOT / "user_map.json"
if not USER_MAP_PATH.exists():
    raise RuntimeError(f"user_map.json not found at {USER_MAP_PATH}")
USER_TO_CLIENT: Dict[str, str] = json.loads(USER_MAP_PATH.read_text())

# load client→Metabase-email map
CLIENT_MAP_PATH = PROJECT_ROOT / "client_map.json"
if not CLIENT_MAP_PATH.exists():
    raise RuntimeError(f"client_map.json not found at {CLIENT_MAP_PATH}")
CLIENT_MAP: Dict[str, str] = json.loads(CLIENT_MAP_PATH.read_text())

# ─────────────────── Flask setup ─────────────────── #
app = Flask(__name__, static_folder=None)

# ─────────────────── JWT helper ─────────────────── #
def _issue_jwt(payload: Dict[str, Any]) -> str:
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# ─────────────────── Routes ─────────────────── #
@app.get("/api/health")
def health():
    return "OK", 200, {"Content-Type": "text/plain"}

@app.get("/api/auth")
def auth():
    """
    Query-params (whitespace stripped):
      user_id=alice123     ← required
      role=analyst         ← optional
      locale=es            ← optional
      return_to=/dash/42   ← optional
    """
    # helper to trim and require
    def getp(name: str, required=False, default=None):
        v = request.args.get(name, default)
        if required and (v is None or not v.strip()):
            abort(400, f"`{name}` required")
        return v.strip() if isinstance(v, str) else v

    user_id   = getp("user_id",   required=True)
    role      = getp("role",      default=None)
    locale    = getp("locale",    default=None)
    return_to = getp("return_to", default="/")

    # map user → client
    client_id = USER_TO_CLIENT.get(user_id)
    if not client_id:
        abort(400, f"Unknown user_id `{user_id}`; add to user_map.json")

    # map client → Metabase email
    mb_email = CLIENT_MAP.get(client_id)
    if not mb_email:
        abort(500, f"No email for client `{client_id}`; add to client_map.json")

    # build groups & attrs
    groups = [f"client_{client_id}"]
    attrs = {"user_id": user_id, "client_id": client_id}
    if role:   attrs["role"]   = role
    if locale: attrs["locale"] = locale

    # mint JWT
    payload: Dict[str, Any] = {
        "email":       mb_email,
        "first_name":  client_id.capitalize(),
        "last_name":   "Customer",
        "groups":      groups,
        **{f"attr.{k}": v for k, v in attrs.items()},
        "exp":         int(time.time()) + 3600
    }
    token = _issue_jwt(payload)

    # redirect into Metabase SSO
    redirect_url = f"{METABASE_URL}/auth/sso?" + urlencode({
        "jwt":        token,
        "return_to":  return_to
    })
    return redirect(redirect_url, 302)

# alias for legacy /sso/metabase path
@app.get("/sso/metabase")
def sso_alias():
    return auth()

# static-file fallback
@app.route("/", defaults={"req_path": ""})
@app.route("/<path:req_path>")
def static_files(req_path: str):
    file_path = STATIC_PATH / req_path
    if file_path.is_dir():
        file_path = file_path / "index.html"
    if not file_path.exists():
        file_path = STATIC_PATH / "404.html"
    return send_from_directory(file_path.parent, file_path.name)

# ─────────────────── entrypoint ─────────────────── #
if __name__ == "__main__":
    app.run(host="localhost", port=9090, debug=True)
