"""
Arch2 — Databricks App backend for the Architecture Assistant.

Serves index.html and exposes the SAME /generate contract the local bridge.js
used ({system,user,model} -> {text}), but instead of shelling out to the local
`claude` CLI it calls a Databricks-hosted Claude Foundation Model serving
endpoint. The frontend's bridge path is unchanged.

Auth: in a Databricks App the injected service-principal OAuth credentials are
used automatically (WorkspaceClient()); locally it falls back to a CLI profile.
"""
import os

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from openai import OpenAI
from databricks.sdk import WorkspaceClient

HERE = os.path.dirname(__file__)
HTML_PATH = os.path.join(HERE, "index.html")

# Databricks-hosted model the assistant calls (Foundation Model API, pay-per-token).
SERVING_ENDPOINT = os.environ.get("SERVING_ENDPOINT", "databricks-claude-sonnet-5")
# Optional AI Gateway URL — when set, calls route through the Gateway so usage
# counters / inference tables register. Falls back to the serving-endpoints path.
AI_GATEWAY_URL = os.environ.get("AI_GATEWAY_URL", "")

IS_DATABRICKS_APP = bool(os.environ.get("DATABRICKS_APP_NAME"))

app = FastAPI(title="Arch2 Architecture Assistant")


def _content_text(content) -> str:
    """Flatten an assistant message's content to plain text.

    Reasoning models (e.g. databricks-claude-sonnet-5) return content as a list
    of typed blocks (reasoning, text, ...) rather than a string. Keep only the
    text blocks so the frontend receives the JSON string it expects.
    """
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") in (None, "text") and block.get("text"):
                    parts.append(block["text"])
            elif getattr(block, "type", None) in (None, "text"):
                parts.append(getattr(block, "text", "") or "")
        return "".join(parts)
    return str(content)


def _workspace_client() -> WorkspaceClient:
    if IS_DATABRICKS_APP:
        return WorkspaceClient()
    profile = os.environ.get("DATABRICKS_PROFILE", "DEFAULT")
    return WorkspaceClient(profile=profile)


def _oauth_token(w: WorkspaceClient) -> str:
    # w.config.token is None for OAuth/U2M; authenticate() returns the header.
    auth = w.config.authenticate()
    if auth and "Authorization" in auth:
        return auth["Authorization"].replace("Bearer ", "")
    return w.config.token or ""


def _llm_client() -> OpenAI:
    w = _workspace_client()
    token = _oauth_token(w)
    if AI_GATEWAY_URL:
        base_url = AI_GATEWAY_URL.rstrip("/")
    else:
        host = w.config.host
        if IS_DATABRICKS_APP:
            host = os.environ.get("DATABRICKS_HOST", host) or ""
            if host and not host.startswith("http"):
                host = f"https://{host}"
        base_url = f"{host.rstrip('/')}/serving-endpoints"
    return OpenAI(api_key=token, base_url=base_url)


@app.get("/health")
def health():
    return {"ok": True, "endpoint": SERVING_ENDPOINT}


@app.post("/generate")
async def generate(req: Request):
    try:
        payload = await req.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    user = (payload.get("user") or "").strip()
    if not user:
        return JSONResponse({"error": "Missing 'user' prompt"}, status_code=400)
    system = payload.get("system") or ""
    # The endpoint name is a server-side/deployment concern; ignore whatever the
    # frontend sends (it carries an Anthropic-API model name, not a DBX endpoint).
    model = SERVING_ENDPOINT

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    try:
        client = _llm_client()
        # Note: some Databricks-hosted Claude endpoints (e.g. sonnet-5) reject the
        # `temperature` parameter, so it is deliberately omitted.
        # max_tokens must cover the model's internal reasoning AND the visible
        # JSON: sonnet-5 is a reasoning model, so a small cap can be spent almost
        # entirely on reasoning, leaving the JSON truncated mid-string (the
        # client then throws "unterminated string in JSON"). Give ample headroom.
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=16000,
        )
        choice = resp.choices[0]
        text = _content_text(choice.message.content)
        # A length-capped response is truncated (often mid-JSON) — fail cleanly
        # instead of returning unparseable text the UI would choke on.
        if getattr(choice, "finish_reason", None) == "length":
            return JSONResponse(
                {"error": "The model response was cut off (token limit). Try a shorter "
                          "description or fewer data sources, then retry."},
                status_code=502,
            )
        return {"text": text}
    except Exception as err:  # surfaces cleanly in the chat UI as an error bubble
        return JSONResponse({"error": str(err)}, status_code=502)


# Serve the single-page app last so /health and /generate win.
@app.get("/")
def index():
    return FileResponse(HTML_PATH, media_type="text/html")


# ---------------------------------------------------------------------------
# Shared assets from the PARENT app/ dir so <base href="../"> fetches resolve
# when this backend is the origin.  Mounts are added AFTER the explicit routes
# above so those always win.
# ---------------------------------------------------------------------------
from fastapi.staticfiles import StaticFiles  # noqa: E402

PARENT = os.path.dirname(HERE)  # .../app

for _sub in ("architectures", "resources", "translations", "vendor", "assets", "share"):
    _p = os.path.join(PARENT, _sub)
    if os.path.isdir(_p):
        app.mount("/" + _sub, StaticFiles(directory=_p), name=_sub)


@app.get("/arch_schema.js")
def _arch_schema():
    return FileResponse(os.path.join(PARENT, "arch_schema.js"), media_type="application/javascript")


@app.get("/industry_icons.js")
def _industry_icons():
    return FileResponse(os.path.join(PARENT, "industry_icons.js"), media_type="application/javascript")
