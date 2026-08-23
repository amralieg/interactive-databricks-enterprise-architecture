"""Generate app-installer.ipynb from the cell sources below.

The notebook is the deliverable, but hand-editing 300 lines of Python inside
JSON string arrays is how escaping bugs get shipped. The source of truth is this
file; run it after any change to the installer.

    python3 tools/build_installer.py
"""

import json
import os

MD_INTRO = """# IDEA: workspace installer

**Interactive Databricks Enterprise Architecture.** Run All. Two widgets, one
deployed app.

This notebook creates a Databricks App in this workspace and deploys the diagram
into it. The app serves one self-contained HTML page from a Python standard
library web server, so there is no build step, no package install, no catalog,
no SQL warehouse and no data access. The app's service principal needs no
grants: it never reads anything.

**Where you use it afterwards:** *Compute -> Apps -> idea*, or the link this
notebook prints in its last cell.

**Prerequisites**

| | |
|---|---|
| Databricks Apps enabled | workspace admin can enable it under *Compute -> Apps* |
| Permission to create apps | `CAN_MANAGE` on Apps, which workspace admins hold by default |
| The `app/` folder | either sitting beside this notebook, or reachable on GitHub |

**Cost:** an app runs on its own small serverless compute. Stop it from
*Compute -> Apps* when you are not showing it.
"""

CODE_WIDGETS = '''# Widgets. Kept to three so Run All is a real option.
W_NAME, W_SOURCE, W_REPO = "01_app_name", "02_source", "03_github_repo"

SRC_BESIDE = "Beside this notebook (Git folder)"
SRC_GITHUB = "Download from GitHub"
DEFAULT_REPO = "amralieg/interactive-databricks-enterprise-architecture"

for _w in (W_NAME, W_SOURCE, W_REPO):
    try:
        dbutils.widgets.remove(_w)
    except Exception:
        pass

dbutils.widgets.text(W_NAME, "idea", "1) App name")
dbutils.widgets.dropdown(W_SOURCE, SRC_BESIDE, [SRC_BESIDE, SRC_GITHUB], "2) Where the app files are")
dbutils.widgets.text(W_REPO, DEFAULT_REPO, "3) GitHub repo (only used by option 2)")

print("Widgets ready. Run the last cell.")
'''

MD_GUIDE = """## Choosing the source

**Beside this notebook** is the normal path. Clone the repo into the workspace
as a Git folder (*Workspace -> Create -> Git folder*), open this notebook from
inside it, and the `app/` folder is already sitting next to it. Updating the app
later is `Pull` on the Git folder followed by Run All here.

**Download from GitHub** is for the case where only this one notebook was
imported. It pulls the repository archive over HTTPS and writes the `app/`
folder into your workspace home. It needs the workspace to have outbound
internet access, which some locked-down deployments do not.
"""

CODE_HELPERS = '''import base64, io, json, os, re, time, zipfile

import requests
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat

# Only these ever need to reach the app. Anything else in the folder (a README,
# a stray notebook) is repo furniture and would only slow the upload down.
APP_FILES = ("index.html", "main.py", "app.yaml")


def banner(kind, title, message):
    import html

    print(("[!] " if kind == "warn" else "[x] " if kind == "error" else "[ok] ") + title)
    print(message)
    tone = {"warn": ("#fff4e5", "#f5c26b", "#7a4b00"),
            "error": ("#fdecea", "#f0a9a2", "#7a1c12"),
            "ok": ("#eaf7ef", "#9ed7b4", "#14532d")}[kind]
    displayHTML(
        '<div style="padding:14px 18px;border-radius:12px;background:%s;'
        'border:1px solid %s;color:%s;margin:10px 0;font-family:system-ui,sans-serif">'
        "<b>%s</b><br>%s</div>"
        % (tone[0], tone[1], tone[2], html.escape(title), html.escape(message).replace("\\n", "<br>"))
    )


def valid_app_name(name):
    """Apps names are lowercase letters, digits and dashes, and must start with
    a letter. Failing here beats a 400 from the create call fifty lines later."""
    name = (name or "").strip().lower()
    if not re.fullmatch(r"[a-z][a-z0-9-]{1,29}", name):
        raise ValueError(
            "App name %r is not usable. Use 2-30 characters, lowercase letters, "
            "digits and dashes, starting with a letter." % name
        )
    return name


def notebook_dir():
    ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
    return os.path.dirname(ctx.notebookPath().get())


def api_headers(w):
    try:
        auth = w.config.authenticate()
        if isinstance(auth, dict):
            return auth
        return {"Authorization": "Bearer %s" % auth}
    except Exception:
        token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
        return {"Authorization": "Bearer %s" % token}


def source_beside(w):
    folder = notebook_dir() + "/app"
    try:
        w.workspace.get_status(folder + "/app.yaml")
    except Exception:
        raise RuntimeError(
            "No app/app.yaml next to this notebook (looked in %s).\\n"
            "Either clone the whole repo as a Git folder, or switch widget 2 to "
            "'Download from GitHub'." % folder
        )
    return folder


def source_github(w, repo, user_home):
    """Pull the repo archive and write only the app folder into the workspace."""
    repo = (repo or "").strip().strip("/")
    if not re.fullmatch(r"[\\w.-]+/[\\w.-]+", repo):
        raise ValueError("Repo %r should look like owner/name." % repo)

    last = None
    for branch in ("main", "master"):
        url = "https://github.com/%s/archive/refs/heads/%s.zip" % (repo, branch)
        try:
            resp = requests.get(url, timeout=120)
        except Exception as exc:
            raise RuntimeError(
                "Could not reach github.com from this workspace (%s). This "
                "workspace may have no outbound internet access; use the Git "
                "folder option instead." % exc
            )
        if resp.status_code == 200:
            last = resp.content
            break
        last = None
    if last is None:
        raise RuntimeError("No main or master branch archive found for %s." % repo)

    target = "%s/idea-app" % user_home
    w.workspace.mkdirs(target)
    written = 0
    with zipfile.ZipFile(io.BytesIO(last)) as zf:
        for info in zf.infolist():
            name = info.filename.split("/", 1)[-1]        # drop the <repo>-<branch>/ prefix
            if not name.startswith("app/"):
                continue
            leaf = name[len("app/"):]
            if leaf not in APP_FILES:
                continue
            w.workspace.upload(
                "%s/%s" % (target, leaf), zf.read(info),
                format=ImportFormat.AUTO, overwrite=True,
            )
            written += 1
            print("  wrote %s/%s" % (target, leaf))
    if written < len(APP_FILES):
        raise RuntimeError(
            "Archive for %s only contained %d of the %d expected app files."
            % (repo, written, len(APP_FILES))
        )
    return target


def wait_for(label, read, done, bad, timeout_s=600, every_s=10):
    """One wait loop for both compute and deployment: they poll different
    endpoints but the shape of the wait, and of getting it wrong, is identical."""
    deadline = time.time() + timeout_s
    seen = None
    while time.time() < deadline:
        state, detail = read()
        if state != seen:
            print("  %s: %s%s" % (label, state, (" - " + detail) if detail else ""))
            seen = state
        if state in done:
            return state
        if state in bad:
            raise RuntimeError("%s reached %s: %s" % (label, state, detail or "no detail given"))
        time.sleep(every_s)
    raise RuntimeError(
        "%s did not settle within %d seconds (last state %s). It may still be "
        "coming up: check Compute -> Apps and re-run." % (label, timeout_s, seen)
    )
'''

CODE_MAIN = '''def main():
    app_name = valid_app_name(dbutils.widgets.get(W_NAME))
    source = dbutils.widgets.get(W_SOURCE)
    repo = dbutils.widgets.get(W_REPO)

    w = WorkspaceClient()
    host = w.config.host.rstrip("/")
    headers = api_headers(w)
    me = w.current_user.me().user_name
    print("Workspace: %s\\nUser:      %s\\nApp:       %s\\n" % (host, me, app_name))

    def api(method, path, body=None):
        kw = {"headers": headers}
        if body is not None:
            kw["json"] = body
        return requests.request(method, host + path, timeout=120, **kw)

    def api_get(path):
        r = api("GET", path)
        r.raise_for_status()
        return r.json()

    print("1/4  Locating the app files")
    folder = (source_beside(w) if source.startswith("Beside")
              else source_github(w, repo, "/Users/%s" % me))
    source_code_path = "/Workspace" + folder if not folder.startswith("/Workspace") else folder
    print("     source_code_path = %s\\n" % source_code_path)

    print("2/4  Creating the app")
    resp = api("POST", "/api/2.0/apps", {"name": app_name,
                                         "description": "IDEA - Interactive Databricks Enterprise Architecture"})
    if resp.status_code in (200, 201):
        print("     created")
    elif "already exists" in resp.text.lower():
        print("     already exists, reusing it")
    else:
        raise RuntimeError("Create failed (%s): %s" % (resp.status_code, resp.text[:400]))

    state = api_get("/api/2.0/apps/%s" % app_name).get("compute_status", {}).get("state", "")
    if state in ("STOPPED", "ERROR"):
        # A reused app that someone stopped will never reach ACTIVE on its own,
        # so waiting on it without asking for a start is a guaranteed timeout.
        print("     compute is %s, starting it" % state)
        api("POST", "/api/2.0/apps/%s/start" % app_name)

    print("\\n3/4  Waiting for app compute")
    wait_for(
        "compute",
        lambda: (lambda d: (d.get("state", "?"), d.get("message", "")))(
            api_get("/api/2.0/apps/%s" % app_name).get("compute_status", {})),
        done={"ACTIVE"}, bad={"ERROR"},
    )

    print("\\n4/4  Deploying")
    resp = api("POST", "/api/2.0/apps/%s/deployments" % app_name,
               {"source_code_path": source_code_path})
    if resp.status_code not in (200, 201):
        raise RuntimeError("Deploy failed (%s): %s" % (resp.status_code, resp.text[:400]))
    deploy_id = resp.json().get("deployment_id", "")

    def read_deploy():
        data = api_get("/api/2.0/apps/%s" % app_name)
        pending, active = data.get("pending_deployment", {}), data.get("active_deployment", {})
        dep = (pending if pending.get("deployment_id") == deploy_id
               else active if active.get("deployment_id") == deploy_id
               else pending or active)
        status = dep.get("status", {})
        return status.get("state", "?"), status.get("message", "")

    wait_for("deployment", read_deploy, done={"SUCCEEDED"}, bad={"FAILED", "CANCELLED"})

    url = api_get("/api/2.0/apps/%s" % app_name).get("url", "")
    banner("ok", "IDEA is live", "Open %s\\n\\nOr find it under Compute -> Apps -> %s." % (url, app_name))
    displayHTML(
        '<p style="font-family:system-ui,sans-serif;font-size:15px">'
        '<a href="%s" target="_blank" style="display:inline-block;padding:10px 18px;'
        'border-radius:9px;background:#FF3621;color:#fff;text-decoration:none;'
        'font-weight:650">Open IDEA</a></p>' % url
    )
    return url


try:
    main()
except Exception as exc:
    banner("error", type(exc).__name__, str(exc))
    raise
'''

CELLS = [
    ("markdown", MD_INTRO),
    ("code", CODE_WIDGETS),
    ("markdown", MD_GUIDE),
    ("code", CODE_HELPERS),
    ("code", CODE_MAIN),
]


def cell(kind, text):
    lines = text.strip("\n").split("\n")
    src = [ln + "\n" for ln in lines[:-1]] + [lines[-1]]
    base = {"cell_type": kind, "metadata": {}, "source": src}
    if kind == "code":
        base["execution_count"] = None
        base["outputs"] = []
    return base


nb = {
    "cells": [cell(k, t) for k, t in CELLS],
    "metadata": {
        "application/vnd.databricks.v1+notebook": {
            "language": "python",
            "notebookName": "app-installer",
            "widgets": {},
        },
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app-installer.ipynb")
with open(out, "w") as fh:
    json.dump(nb, fh, indent=1)
    fh.write("\n")
print("wrote %s (%d cells)" % (out, len(CELLS)))
