import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    """People rail with per-industry Technical roles (never common.TECH_PPL)."""
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_CONSTRUCTION = {
    'construction': {
        "label": "Construction",
        "blurb": "Capital projects, job costing, field operations, subcontractor management, and BIM coordination across general contractors and owners.",
        "medallion": medallion(
            "Raw project and field feeds",
            "Procore daily logs, ERP job costs, BIM revisions and equipment telematics landed exactly as received.",
            "Conformed projects and WBS",
            "Projects, cost codes, subcontractors and assets resolved across ERP, PM and field systems.",
            "Margin, schedule, safety",
            "Contracted products executives and PMs run on: job margin, schedule variance, RFI aging and TRIR.",
        ),
        "rails": {
            "src": [
                {"box": "Project Management", "ic": "sheet", "tiles": [
                    tile("Procore", "sheet", "RFIs, submittals, daily logs and punch lists.", "procore"),
                    tile("Autodesk Build", "apps", "Issues, checklists and field photos on BIM context.", "autodesk-build"),
                    tile("Primavera P6", "sheet", "Master schedules, critical path and earned value.", "primavera"),
                ]},
                {"box": "ERP & Job Cost", "ic": "erp", "tiles": [
                    tile("Viewpoint Vista", "erp", "Job cost, AP, payroll and equipment billing.", "viewpoint"),
                    tile("Sage 300 CRE", "erp", "Project accounting, change orders and WIP.", "sage-cre"),
                    tile("Oracle Aconex", "share", "Document control and transmittals.", "aconex"),
                ]},
                {"box": "BIM & Design", "ic": "product", "tiles": [
                    tile("Autodesk Revit", "product", "Design models, quantities and clash contexts.", "revit"),
                    tile("Navisworks", "apps", "4D simulations and clash detection runs.", "navisworks"),
                    tile("Bentley iTwin", "globe", "Digital twin synchronization for infrastructure.", "itwin"),
                ]},
                {"box": "Field & Equipment", "ic": "iot", "tiles": [
                    tile("Samsara Fleet", "iot", "Equipment location, utilization and DVIR.", "samsara"),
                    tile("United Rentals Telematics", "stream", "Rental fleet hours and geofence alerts.", "united-rentals"),
                    tile("OpenSpace", "iot", "360 site capture with progress and safety analytics.", "openspace"),
                ]},
                {"box": "Safety & Quality", "ic": "gavel", "tiles": [
                    tile("ISNetworld", "gavel", "Contractor prequalification and safety scores.", "isnetworld"),
                    tile("HammerTech", "gavel", "Site inductions, permits and incident logs.", "hammertech"),
                ]},
                fed_group("Owner Reporting Mart", "Owner KPI and portfolio marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("Dodge Construction Network", "market", "Bid opportunities and project leads by geography.", "dodge"),
                tile("RSMeans Cost Data", "chart", "Unit cost benchmarks for estimating validation.", "rsmeans"),
                tile("OSHA Incident Data", "gavel", "Industry injury rates for safety benchmarking.", "osha"),
            ]),
            "ppl": ppl2([
                biz("GC President & COO", "Genie One",
                    "The CEO on backlog and margin; the COO on labor productivity, schedule variance and safety, watching forecast at completion and TRIR.",
                    [["Genie One", "Ask which jobs are below margin this month."], ["AI/BI", "WIP and margin on certified Metric Views."], ["Unity Catalog", "One cost code definition across ERP and field."]]),
                biz("Project Managers", "AI/BI",
                    "Schedule, budget, change orders and subcontractor performance, run on CPI, SPI, RFI aging and forecast at completion.",
                    [["Project Command", "Earned value and forecast at completion by job."], ["AI/BI", "RFI and CO aging on governed Procore data."]]),
                biz("Estimating", "Model Serving",
                    "Bid pricing, risk allowances and historical productivity, judged on win rate, margin sensitivity and unit-cost variance.",
                    [["Bid Analyzer", "Win probability and margin sensitivity."], ["Model Serving", "Productivity models in the estimating path."]]),
                biz("Field Superintendents", "Lakehouse//RT",
                    "Daily production, labor hours and safety observations, tracked on units per labor hour, equipment idle time and near-miss rate.",
                    [["Field Daily Log", "Production quantities vs plan in real time."], ["Lakehouse//RT", "Equipment utilization at site latency."]]),
                biz("Safety & Quality", "Apps",
                    "Incident prevention, inspections and closeout documentation, measured on TRIR, leading-indicator closure and punch-list burndown.",
                    [["Safety Dashboard", "Leading indicators before TRIR moves."], ["Apps", "Inspection apps on governed field data."]]),
            ], [
                biz("Data Engineers", "Lakeflow",
                    "Land Procore daily logs, ERP job costs, BIM revisions and equipment telematics; own Bronze to Silver and the pager when the WIP tables stall.",
                    [["Lakeflow Connect", "Managed connectors for ERP, project-management and field sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on cost and schedule feeds."], ["Lakewatch", "Freshness on the WIP and margin tables PMs read at month-end."]]),
                biz("Data Scientists", "MLflow",
                    "Bid win-probability, productivity-forecast and safety-leading-indicator models, and whether they still hold across a new project type and region.",
                    [["Feature Store", "Job and cost-code features read identically in training and serving."], ["MLflow", "Every bid and productivity model tracked for audit and reproduction."], ["Model Serving", "Productivity and risk models scored in the estimating path."]]),
                biz("App Developers", "Apps",
                    "Ship the project command, bid analyzer, field daily log and safety dashboard apps PMs and superintendents work in, next to governed job data.",
                    [["Apps", "Field and project screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for daily-log and inspection state."], ["Agent Bricks", "Agents that draft change orders and recovery plans against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Portfolio dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for job status in project channels."),
                    tile("Notebooks & IDEs", "notebook", "Estimating notebooks on historical cost data."),
                ]},
                {"box": "Owners & Subs", "ic": "partner", "tiles": [
                    tile("Owner Portal", "api", "Progress photos and earned value shared to owners.", "procore"),
                    tile("Subcontractor PO", "zplug", "Committed costs and pay apps to trade partners.", "viewpoint"),
                    tile("BIM Coordination", "product", "Clash reports pushed to design teams.", "navisworks"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Change Order Routing", "sheet", "Approved COs written to ERP job cost.", "sage-cre"),
                    tile("Schedule Updates", "gauge", "Percent complete fed back to P6 activities.", "primavera"),
                    tile("Equipment Dispatch", "iot", "Fleet assignments optimized and sent to yards.", "samsara"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("OSHA Logs", "gavel", "300 logs and incident summaries filed from field data.", "osha"),
                    tile("Prevailing Wage", "share", "Certified payroll reports for public works.", "viewpoint"),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Project performance products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Owners and JV partners via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Project Command", "Earned value", "gauge", "SPI, CPI and forecast at completion across the active portfolio."),
             app("Bid Analyzer", "Preconstruction", "market", "Historical productivity and risk allowances applied to new bids."),
             app("Field Daily Log", "Production tracking", "stream", "Installed quantities and labor hours vs daily plan."),
             app("Safety Dashboard", "Leading indicators", "gavel", "Observations, near-misses and training gaps before TRIR rises.")],
            [uc("Earned Value Mgmt", "Finance", "chart", "CPI and SPI integrated across ERP and schedule systems."),
             uc("Change Order Control", "Commercial", "erp", "Pending and approved COs tracked against margin impact."),
             uc("Labor Productivity", "Field", "people", "Units per labor hour benchmarked by trade and job."),
             uc("Equipment Utilization", "Fleet", "iot", "Owned and rented assets ranked by idle time and cost."),
             uc("BIM Clash Prevention", "Design", "product", "Clashes resolved before they become field rework."),
             uc("Subcontractor Risk", "Supply", "zplug", "Prequalification and performance scored before award."),
             uc("Schedule Recovery", "Planning", "sheet", "Recovery options costed when critical path slips."),
             uc("WIP Forecasting", "Finance", "erp", "Revenue and cost at completion before month-end close."),
             uc("Safety Analytics", "EHS", "gavel", "Leading indicators predicting recordable incidents."),
             uc("Portfolio Benchmarking", "Executive", "chart", "Job performance compared across regions and types.")],
        ),
        "sources": {
            "procore": {"t": "Procore", "u": "https://www.procore.com/"},
            "autodesk-build": {"t": "Autodesk Build", "u": "https://construction.autodesk.com/products/autodesk-build/"},
            "primavera": {"t": "Oracle Primavera P6", "u": "https://www.oracle.com/construction-engineering/primavera-p6/"},
            "viewpoint": {"t": "Viewpoint Vista", "u": "https://www.viewpoint.com/solutions/vista"},
            "sage-cre": {"t": "Sage 300 Construction", "u": "https://www.sage.com/en-us/industry/construction/"},
            "aconex": {"t": "Oracle Aconex", "u": "https://www.oracle.com/construction-engineering/aconex/"},
            "revit": {"t": "Autodesk Revit", "u": "https://www.autodesk.com/products/revit/"},
            "navisworks": {"t": "Autodesk Navisworks", "u": "https://www.autodesk.com/products/navisworks/"},
            "itwin": {"t": "Bentley iTwin", "u": "https://www.bentley.com/software/itwin/"},
            "samsara": {"t": "Samsara", "u": "https://www.samsara.com/"},
            "united-rentals": {"t": "United Rentals", "u": "https://www.unitedrentals.com/"},
            "openspace": {"t": "OpenSpace", "u": "https://www.openspace.ai/"},
            "isnetworld": {"t": "ISNetworld", "u": "https://www.isnetworld.com/"},
            "hammertech": {"t": "HammerTech", "u": "https://www.hammertech.com/"},
            "dodge": {"t": "Dodge Construction Network", "u": "https://www.construction.com/"},
            "rsmeans": {"t": "RSMeans", "u": "https://www.rsmeans.com/"},
            "osha": {"t": "OSHA", "u": "https://www.osha.gov/"},
        },
    },
}
