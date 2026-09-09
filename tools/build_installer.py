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

**How Run All behaves:** the notebook launches the install as a **tagged
Databricks job**, prints the run URL, then waits for it and surfaces the app
link. The job carries `dbx_idea_installer_*` tags, so its serverless spend is
attributable in `system.billing.usage`, the same pattern the vibe-modelling
agent installer uses. If a job cannot be created (no permission, path not
resolvable), the notebook deploys inline instead so the install still works.

**Tagging the app itself:** a Databricks App has no custom-tag field. The
platform attributes an app's ongoing serverless spend through a **serverless
usage policy**, whose tags land in `system.billing.usage`. Set widget 4 to a
policy id to attach one on create; leave it blank to skip.

**Where you use it afterwards:** *Compute -> Apps -> idea*, or the link this
notebook prints in its last cell.

**Prerequisites**

| | |
|---|---|
| Databricks Apps enabled | workspace admin can enable it under *Compute -> Apps* |
| Permission to create apps | `CAN_MANAGE` on Apps, which workspace admins hold by default |
| Permission to create jobs | for the tagged install job; without it the notebook deploys inline |
| The `app/` folder | either sitting beside this notebook, or reachable on GitHub |

**Cost:** an app runs on its own small serverless compute. Stop it from
*Compute -> Apps* when you are not showing it.
"""

CODE_WIDGETS = '''# Widgets. Kept to four so Run All is a real option.
W_NAME, W_SOURCE, W_REPO, W_POLICY = "01_app_name", "02_source", "03_github_repo", "04_usage_policy_id"

SRC_BESIDE = "Beside this notebook (Git folder)"
SRC_GITHUB = "Download from GitHub"
DEFAULT_REPO = "amralieg/interactive-databricks-enterprise-architecture"

# Tags follow the vibe-modelling-agent pattern: a prefix and a version, applied to
# the install job so its serverless spend lands in system.billing.usage under a
# name a cost report can group on. Bump the version when the app changes shape.
INSTALLER_TAG_PREFIX = "dbx_idea_installer_"
INSTALLER_VERSION = "v1"

for _w in (W_NAME, W_SOURCE, W_REPO, W_POLICY):
    try:
        dbutils.widgets.remove(_w)
    except Exception:
        pass

dbutils.widgets.text(W_NAME, "idea", "1) App name")
dbutils.widgets.dropdown(W_SOURCE, SRC_BESIDE, [SRC_BESIDE, SRC_GITHUB], "2) Where the app files are")
dbutils.widgets.text(W_REPO, DEFAULT_REPO, "3) GitHub repo (only used by option 2)")
dbutils.widgets.text(W_POLICY, "", "4) Serverless usage policy id (optional)")

print("Widgets ready. Run the last cell.")
'''

MD_GUIDE = """## Choosing the source

**Beside this notebook** is the normal path. Clone the repo into the workspace
as a Git folder (*Workspace -> Create -> Git folder*), open this notebook from
inside it, and the `app/` folder is already sitting next to it. Updating the app
later is `Pull` on the Git folder followed by Run All here.

**Download from GitHub** is for the case where only this one notebook was
imported. It pulls the repository archive over HTTPS and writes the `app/`
folder into your workspace home. Two things have to be true for it to work: the
workspace needs outbound internet access, which some locked-down deployments do
not have, and the repository has to be readable without a token. This repository
is public, so it is. A fork you keep private returns 404 to an anonymous archive
request, so use the Git folder path for one of those.
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
        raise RuntimeError(
            "No readable main or master archive for %s. GitHub answers 404 to an "
            "anonymous request for a private repository, so if this one is "
            "private, clone it as a Git folder and use option 1 instead." % repo
        )

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

CODE_LAUNCHER = '''# === JobLauncher: run the deploy as a tagged Databricks job (agent pattern) ===
# The vibe-modelling-agent installer never installs in the notebook cell: it creates
# a tagged Databricks job, runs it, and waits. That is what puts dbx_* tags on the
# work in system.billing.usage. This is the same launcher, trimmed to one notebook
# task, so IDEA's install job is tagged and attributable the same way.
import re as _jl_re


class JobLauncher:
    _TAG_SAFE_RE = _jl_re.compile(r"[^A-Za-z0-9._-]")

    @staticmethod
    def _sanitize_tag(value):
        s = JobLauncher._TAG_SAFE_RE.sub("_", str(value))
        s = _jl_re.sub(r"_+", "_", s)
        return s.strip("_").strip(".").strip("-")

    def __init__(self, notebook_path, widget_key_values, job_tags=None):
        self.notebook_path = str(notebook_path)
        self.widget_key_values = {str(k): str(v) for k, v in widget_key_values.items()}
        raw = dict(job_tags or {})
        self.job_tags = {self._sanitize_tag(k): self._sanitize_tag(v) for k, v in raw.items()}

    @staticmethod
    def _detect_compute_type():
        """Serverless vs classic. A serverless workspace rejects an attached cluster,
        so a clusterId-only probe misfires: the reliable signals are IS_SERVERLESS and
        the absence of a cluster name. Returns (is_serverless, cluster_id)."""
        import os as _jl_os
        if _jl_os.environ.get("IS_SERVERLESS", "").upper() == "TRUE":
            return True, None
        try:
            spark.conf.get("spark.databricks.clusterUsageTags.clusterName")
        except Exception:
            return True, None
        try:
            _cid = spark.conf.get("spark.databricks.clusterUsageTags.clusterId", "")
            if _cid:
                return False, _cid
        except Exception:
            pass
        return True, None

    @staticmethod
    def _get_workspace_context():
        host, org = "", ""
        try:
            ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
            try:
                host = ctx.apiUrl().get()
            except Exception:
                pass
            try:
                org = ctx.workspaceId().get()
            except Exception:
                pass
        except Exception:
            pass
        if not host:
            try:
                from databricks.sdk import WorkspaceClient as _WC
                host = str(_WC().config.host)
            except Exception:
                pass
        return (host or "").rstrip("/"), org

    @staticmethod
    def get_current_notebook_path():
        try:
            ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
            try:
                p = ctx.notebookPath().get()
                if p:
                    return p
            except Exception:
                pass
            import json as _j
            c = _j.loads(ctx.toJson())
            for k in ("notebook_path", "notebookPath"):
                v = (c.get("extraContext") or {}).get(k, "") or (c.get("tags") or {}).get(k, "")
                if v:
                    return v
        except Exception:
            pass
        return ""

    def launch(self, job_name=None, run_name=None):
        import time as _t
        from databricks.sdk import WorkspaceClient as _WC
        from databricks.sdk.service import jobs as _jobs
        out = {"success": False, "job_id": None, "run_id": None, "job_url": "", "error": None}
        try:
            if not self.notebook_path:
                raise RuntimeError("could not resolve this notebook's path")
            w = _WC()
            job_name = job_name or ("dbx_idea_installer_%d" % int(_t.time()))
            is_serverless, cluster_id = self._detect_compute_type()

            def _build_task(attach_cluster):
                t = _jobs.Task(
                    task_key="deploy",
                    notebook_task=_jobs.NotebookTask(
                        notebook_path=self.notebook_path,
                        base_parameters=self.widget_key_values),
                    timeout_seconds=3600,
                )
                if attach_cluster and cluster_id:
                    t.existing_cluster_id = cluster_id
                return t

            existing = None
            try:
                for j in w.jobs.list(name=job_name):
                    if j.settings and j.settings.name == job_name:
                        existing = j.job_id
                        break
            except Exception:
                pass

            def _create_and_run(attach_cluster):
                task = _build_task(attach_cluster)
                if existing:
                    w.jobs.reset(job_id=existing,
                                 new_settings=_jobs.JobSettings(name=job_name, tags=self.job_tags, tasks=[task]))
                    jid = existing
                else:
                    jid = w.jobs.create(name=job_name, tags=self.job_tags, tasks=[task]).job_id
                r = w.jobs.run_now(job_id=jid)
                return jid, r

            try:
                job_id, run = _create_and_run(attach_cluster=(not is_serverless))
            except Exception as ce:
                # A serverless-only workspace rejects the attached cluster if detection
                # misfired: retry as a pure serverless task before giving up.
                if "serverless" in str(ce).lower() and not is_serverless:
                    job_id, run = _create_and_run(attach_cluster=False)
                else:
                    raise
            host, org = self._get_workspace_context()
            url = "%s/jobs/%s/runs/%s%s" % (host, job_id, run.run_id, ("?o=%s" % org if org else "")) if host else ""
            out.update({"success": True, "job_id": job_id, "run_id": run.run_id, "job_url": url})
        except Exception as e:
            out["error"] = str(e)
        return out

    @staticmethod
    def wait_for_run(run_id, job_url="", pulse_seconds=20, logger=None):
        import time as _t
        from databricks.sdk import WorkspaceClient as _WC
        log = logger or (lambda m: print(m, flush=True))
        w = _WC()
        terminal = {"TERMINATED", "INTERNAL_ERROR", "SKIPPED"}
        out = {"life_cycle_state": "", "result_state": "", "notebook_output": "", "error": None}
        start = _t.time()
        while True:
            try:
                run = w.jobs.get_run(run_id=run_id)
            except Exception as e:
                log("   poll error (%s) - retrying in %ds" % (str(e)[:120], pulse_seconds))
                _t.sleep(pulse_seconds)
                continue
            state = run.state if run else None
            st = state.life_cycle_state.value if (state and state.life_cycle_state) else ""
            rs = state.result_state.value if (state and state.result_state) else ""
            elapsed = int(_t.time() - start)
            if st in terminal:
                out["life_cycle_state"], out["result_state"] = st, rs
                try:
                    trid = run.tasks[0].run_id if (run and run.tasks) else run_id
                    ro = w.jobs.get_run_output(run_id=trid)
                    out["notebook_output"] = (ro.notebook_output.result if ro.notebook_output else "") or ""
                    if ro.error:
                        out["error"] = ro.error
                except Exception as e:
                    out["error"] = str(e)
                return out
            log("   [%s] deploy job still running [%s] %ds elapsed"
                % (_t.strftime("%H:%M:%S"), st or "PENDING", elapsed))
            _t.sleep(pulse_seconds)

    @staticmethod
    def update_job_tags(updated_tags):
        """Merge tags onto the job currently running this notebook (best effort)."""
        res = {"success": False, "error": None}
        if not updated_tags:
            res["error"] = "empty"
            return res
        try:
            ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
            job_id_str = ""
            try:
                job_id_str = ctx.jobId().get()
            except Exception:
                pass
            if not job_id_str:
                res["error"] = "not running as a job (no jobId)"
                return res
            from databricks.sdk import WorkspaceClient as _WC
            from databricks.sdk.service import jobs as _jobs
            w = _WC()
            job_id = int(job_id_str)
            info = w.jobs.get(job_id=job_id)
            existing = dict(info.settings.tags or {})
            new = {JobLauncher._sanitize_tag(k): JobLauncher._sanitize_tag(v) for k, v in updated_tags.items()}
            merged = {**existing, **new}
            w.jobs.update(job_id=job_id, new_settings=_jobs.JobSettings(tags=merged))
            res["success"] = True
        except Exception as e:
            res["error"] = str(e)
        return res
'''

CODE_MAIN = '''def deploy():
    """Create the app and deploy the diagram into it. This is the actual work; it
    runs inside the launched job (or inline if a job could not be created)."""
    app_name = valid_app_name(dbutils.widgets.get(W_NAME))
    source = dbutils.widgets.get(W_SOURCE)
    repo = dbutils.widgets.get(W_REPO)
    usage_policy = (dbutils.widgets.get(W_POLICY) or "").strip()

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
    # An app has no custom-tag field of its own: the platform attributes an app's
    # serverless spend through a usage policy, whose tags land in system.billing.usage.
    # So the policy id, when given, is what "tags" the app.
    create_body = {"name": app_name,
                   "description": "IDEA - Interactive Databricks Enterprise Architecture"}
    if usage_policy:
        create_body["usage_policy_id"] = usage_policy
    resp = api("POST", "/api/2.0/apps", create_body)
    if resp.status_code in (200, 201):
        print("     created" + (" with usage policy %s" % usage_policy if usage_policy else ""))
    elif "already exists" in resp.text.lower():
        print("     already exists, reusing it")
        if usage_policy:
            upd = api("PATCH", "/api/2.0/apps/%s?update_mask=usage_policy_id" % app_name,
                      {"name": app_name, "usage_policy_id": usage_policy})
            if upd.status_code in (200, 201):
                print("     attached usage policy %s" % usage_policy)
            else:
                print("     note: could not attach usage policy (%s): %s"
                      % (upd.status_code, upd.text[:200]))
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
    # Refine the job's tags with the deployed URL, mirroring the agent's post-install
    # tag update. A no-op when running inline (no job id).
    JobLauncher.update_job_tags({INSTALLER_TAG_PREFIX + "status": "deployed"})
    return url


def _running_as_job():
    """True when this notebook is executing inside a job run (jobId set). The backstop
    that stops a launched job from launching itself again."""
    try:
        ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
        return bool(ctx.jobId().get())
    except Exception:
        return False


def _finish(url, app_name):
    banner("ok", "IDEA is live", "Open %s\\n\\nOr find it under Compute -> Apps -> %s." % (url, app_name))
    displayHTML(
        '<p style="font-family:system-ui,sans-serif;font-size:15px">'
        '<a href="%s" target="_blank" style="display:inline-block;padding:10px 18px;'
        'border-radius:9px;background:#FF3621;color:#fff;text-decoration:none;'
        'font-weight:650">Open IDEA</a></p>' % url
    )


def run():
    app_name = valid_app_name(dbutils.widgets.get(W_NAME))

    # Inside the launched job: do the real deploy and hand the URL back to the
    # waiting notebook through the run output.
    if _running_as_job():
        url = deploy()
        try:
            dbutils.notebook.exit(url or "")
        except Exception:
            pass
        return url

    # Interactive Run All: launch a tagged job that does the deploy, then wait.
    tags = {
        INSTALLER_TAG_PREFIX + "app": app_name,
        INSTALLER_TAG_PREFIX + "kind": "enterprise_architecture",
        INSTALLER_TAG_PREFIX + "version": INSTALLER_VERSION,
    }
    widgets = {
        W_NAME: app_name,
        W_SOURCE: dbutils.widgets.get(W_SOURCE),
        W_REPO: dbutils.widgets.get(W_REPO),
        W_POLICY: dbutils.widgets.get(W_POLICY),
    }
    nb_path = JobLauncher.get_current_notebook_path()
    job_name = "dbx_idea_installer_%s_%s" % (JobLauncher._sanitize_tag(app_name), INSTALLER_VERSION)
    print("Launching the install as a Databricks job (%s) ...\\n" % job_name)
    res = JobLauncher(nb_path, widgets, tags).launch(job_name=job_name, run_name=job_name)

    if not res.get("success"):
        # No permission to create a job, or the path could not be resolved: the
        # install still has to work, so fall back to deploying inline (untagged).
        print("Could not launch a job (%s).\\nRunning the deploy inline instead; "
              "the install will not be tagged.\\n" % res.get("error"))
        url = deploy()
        _finish(url, app_name)
        return url

    if res.get("job_url"):
        print("   job run: %s\\n" % res["job_url"])
    r = JobLauncher.wait_for_run(res["run_id"], job_url=res.get("job_url", ""), pulse_seconds=20)
    if r.get("result_state") == "SUCCESS":
        url = (r.get("notebook_output") or "").strip()
        _finish(url, app_name)
        return url
    banner("error", "install job %s" % (r.get("result_state") or "?"),
           r.get("error") or ("See the job run: %s" % res.get("job_url", "")))
    raise RuntimeError("The install job did not succeed (%s)." % (r.get("result_state") or "unknown"))


try:
    run()
except Exception as exc:
    banner("error", type(exc).__name__, str(exc))
    raise
'''

CELLS = [
    ("markdown", MD_INTRO),
    ("code", CODE_WIDGETS),
    ("markdown", MD_GUIDE),
    ("code", CODE_HELPERS),
    ("code", CODE_LAUNCHER),
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
