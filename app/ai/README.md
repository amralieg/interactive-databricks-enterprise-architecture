# AI Architecture Assistant (`app/ai/`)

A chat-driven sub-app built on top of the IDEA modular reference explorer. Describe a
customer or use case in the chat input; the assistant detects the best-fit industry,
runs two-phase industry-grounded component selection, and generates a new editable,
persisted tab containing a tailored architecture — without touching the reference board.
The reference board stays live and unmodified throughout.

---

## Local development

**Prerequisites:** a Databricks CLI profile (`~/.databrickscfg`) with access to the
serving endpoint, and the packages from `requirements.txt` (`fastapi`, `uvicorn`,
`openai`, `databricks-sdk`).

```bash
# from app/ai/
pip install -r requirements.txt          # first time only
DATABRICKS_PROFILE=<profile> uvicorn app:app --port 8000
```

The server starts at `http://localhost:8000`. Health check: `GET /health`. Chat
requests go to `POST /generate` with body `{system, user, model}` and return `{text}`.

Override the serving endpoint (default `databricks-claude-sonnet-5`):

```bash
SERVING_ENDPOINT=my-endpoint DATABRICKS_PROFILE=<profile> uvicorn app:app --port 8000
```

---

## How shared templates are reached

`app/ai/index.html` sets `<base href="../">` so all relative fetches resolve one
directory up, against `app/`. The FastAPI server also mounts the parent `app/`
subdirectories (`architectures/`, `resources/`, `translations/`, `vendor/`) as static
paths so those fetches resolve correctly from this sub-app's own origin.

**Consequence:** any new industry template added to `app/architectures/` is immediately
available to the AI assistant — no changes to `app/ai/` are needed.

---

## Deploy as a Databricks App

`app/ai/app.yaml` declares the entry point:

```yaml
command: ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
env:
  - name: SERVING_ENDPOINT
    value: databricks-claude-sonnet-5
```

The **whole `app/` tree** must be present in the source path when deploying, because the
sub-app's static mounts reach into the parent directories for shared templates. Deploy
from the workspace path that contains the full `app/` directory (base explorer + `ai/`
subdirectory + shared templates), targeting the `app/ai` entry point.

To override the model, set `SERVING_ENDPOINT` in the app's environment configuration.
Authentication uses the app's injected service-principal OAuth credentials automatically;
no API key is needed.
