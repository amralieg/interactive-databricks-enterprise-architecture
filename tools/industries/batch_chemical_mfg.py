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


INDUSTRIES_BATCH_CHEMICAL_MFG = {
    'chemical_mfg': {
        "label": "Chemical Manufacturing",
        "blurb": "Process manufacturing: batch recipes, plant operations, quality labs, regulatory compliance, and global supply chains for specialty and commodity chemicals.",
        "medallion": medallion(
            "Raw historian and LIMS feeds",
            "DCS tags, lab results, SAP postings and SDS documents landed exactly as received for batch genealogy replay.",
            "Conformed batches and materials",
            "Batches, materials, equipment and customers resolved across MES, ERP and LIMS.",
            "Yield, OEE, compliance",
            "Contracted products operations and EHS run on: batch yield, OEE, CoA compliance and emissions intensity.",
        ),
        "rails": {
            "src": [
                {"box": "ERP & Supply", "ic": "erp", "tiles": [
                    tile("SAP S/4HANA PP-PI", "erp", "Recipes, batch records, inventory and costing.", "sap-pppi"),
                    tile("Oracle Process Mfg", "erp", "Formula management, lot traceability and planning.", "oracle-pm"),
                    tile("AspenTech Supply", "sheet", "Planning, scheduling and network optimization.", "aspentech"),
                ]},
                {"box": "MES & Historian", "ic": "iot", "tiles": [
                    tile("AVEVA PI System", "iot", "Historian tags, events and asset framework.", "aveva-pi"),
                    tile("Honeywell Uniformance", "stream", "DCS data, alarms and batch phase records.", "honeywell"),
                    tile("Siemens Opcenter PSM", "zplug", "Electronic batch records and equipment logs.", "opcenter-psm"),
                ]},
                {"box": "Quality & LIMS", "ic": "gavel", "tiles": [
                    tile("LabWare LIMS", "gavel", "Sample plans, results and CoA release.", "labware"),
                    tile("LIMS", "product", "QC testing, stability and method compliance.", "samplemanager"),
                    tile("Sphera Product Steward", "gavel", "SDS, REACH and hazard classifications.", "sphera"),
                ]},
                {"box": "Maintenance", "ic": "zplug", "tiles": [
                    tile("IBM Maximo", "zplug", "Work orders, PM schedules and spare parts.", "maximo"),
                    tile("SAP PM", "erp", "Notification, maintenance plans and reliability.", "sap-pm"),
                ]},
                {"box": "Logistics", "ic": "stream", "tiles": [
                    tile("SAP TM", "stream", "Bulk tank scheduling and dangerous goods routing.", "sap-tm"),
                    tile("ORBCOMM Tank Monitoring", "iot", "Iso tank level and temperature telemetry.", "orbcomm"),
                ]},
                fed_group("Corporate Finance Mart", "Transfer pricing and segment P&L marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("ECHA REACH", "gavel", "Registration dossiers and substance volumes.", "echa"),
                tile("EPA TRI Reporting", "gavel", "Toxic release inventory thresholds and submissions.", "epa-tri"),
                tile("ICIS Pricing", "market", "Commodity chemical price assessments by region.", "icis"),
            ]),
            "ppl": ppl2([
                biz("CEO & EHS Council", "Genie One",
                    "The CEO on margin per ton and capacity utilization; the EHS officer on process-safety incident rate and emissions intensity.",
                    [["Genie One", "Ask what last month's yield was by plant."], ["AI/BI", "OEE and margin on certified Metric Views."], ["Unity Catalog", "One batch definition across MES and ERP."]]),
                biz("Plant Operations", "Lakehouse//RT",
                    "Shift handover, batch execution and abnormal situation management, run on OEE, first-pass yield and deviation count.",
                    [["Batch Cockpit", "Live phase progress and deviation flags."], ["Lakehouse//RT", "Historian tags at control-room latency."]]),
                biz("Process Engineering", "AI/BI",
                    "Recipe optimization, scale-up and golden batch comparison, judged on yield per batch, energy per ton and off-spec rate.",
                    [["Golden Batch Analytics", "Deviation from reference trajectories."], ["AI/BI", "Yield and energy per batch on governed tags."]]),
                biz("Quality & Regulatory", "Apps",
                    "CoA release, stability and regulatory submissions, tracked on CoA compliance, right-first-time release and REACH filing timeliness.",
                    [["CoA Workbench", "Release decisions with full genealogy."], ["Apps", "Lab review apps on governed LIMS data."]]),
                biz("Supply Chain", "Model Serving",
                    "Demand allocation, tank scheduling and customer prioritization, measured on on-time-in-full, margin per ton and contract-fill rate.",
                    [["Allocation Optimizer", "Scarce product ranked by margin and contract."], ["Model Serving", "Demand forecasts in the planning path."]]),
            ], [
                biz("Data Engineers", "Lakeflow",
                    "Land DCS historian tags, LIMS results, SAP postings and SDS documents; own Bronze to Silver and the pager when the batch and yield tables stall.",
                    [["Lakeflow Connect", "Managed connectors for ERP, MES and LIMS sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on historian and lab feeds."], ["Lakewatch", "Freshness on the batch and yield tables the control room reads."]]),
                biz("Data Scientists", "MLflow",
                    "Golden-batch, predictive-quality, energy-optimisation and predictive-maintenance models, and whether they still hold across a recipe scale-up.",
                    [["Feature Store", "Batch and asset features read identically in training and serving."], ["MLflow", "Every quality and RUL model tracked for audit and reproduction."], ["Model Serving", "Quality and setpoint models scored in the control path."]]),
                biz("App Developers", "Apps",
                    "Ship the batch cockpit, golden batch analytics, CoA workbench and allocation optimizer apps operations and quality work in, next to governed batch data.",
                    [["Apps", "Control-room and lab screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for release and allocation state."], ["Agent Bricks", "Agents that draft setpoints and work orders against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Spotfire", "chart", "Operations and quality dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for batch status in plant channels."),
                    tile("Notebooks & IDEs", "notebook", "Process engineering notebooks on historian data."),
                ]},
                {"box": "Customers & Partners", "ic": "partner", "tiles": [
                    tile("CoA Portal", "api", "Certificates of analysis delivered to customer portals.", "labware"),
                    tile("Vendor ASN", "zplug", "Raw material ASNs and COA from suppliers.", "sap-pppi"),
                    tile("Tank Telemetry Share", "iot", "Iso tank levels shared to logistics partners.", "orbcomm"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Setpoint Advisor", "gauge", "Optimized setpoints pushed to DCS within guardrails."),
                    tile("Batch Hold/Release", "gavel", "Quality holds propagated to MES and warehouse.", "opcenter-psm"),
                    tile("Maintenance Work Orders", "zplug", "Predicted failures raised in Maximo.", "maximo"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("REACH Submissions", "gavel", "Volume and exposure reports filed to ECHA.", "echa"),
                    tile("EPA TRI Filings", "share", "Release quantities reported from governed emissions.", "epa-tri"),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Batch genealogy products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Customers and auditors via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Batch Cockpit", "Live execution", "gauge", "Phase progress, deviations and predicted end times across reactors."),
             app("Golden Batch Analytics", "Process dev", "iot", "Trajectories compared to reference batches for yield and quality."),
             app("CoA Workbench", "Quality release", "gavel", "Release decisions with full material genealogy and stability."),
             app("Allocation Optimizer", "Scarce supply", "market", "Limited production ranked by margin, contract and strategic value.")],
            [uc("Predictive Quality", "Quality", "gavel", "Off-spec predicted from in-process tags before batch completion."),
             uc("Golden Batch", "Process", "iot", "Optimal trajectories identified and enforced on new runs."),
             uc("Energy Optimization", "Sustainability", "chart", "Steam and power consumption minimized per ton produced."),
             uc("Predictive Maintenance", "Reliability", "zplug", "Pump and agitator failures predicted before unplanned downtime."),
             uc("Batch Genealogy", "Traceability", "product", "Full lineage from raw lots through finished goods."),
             uc("Emissions Tracking", "EHS", "gavel", "Scope 1 and 2 intensity by plant and product."),
             uc("Demand Allocation", "Supply Chain", "sheet", "Finite capacity allocated to highest-value orders."),
             uc("Tank Scheduling", "Logistics", "stream", "Bulk movements scheduled against rail and vessel windows."),
             uc("Regulatory Submissions", "Compliance", "share", "REACH and TRI filings from governed operational data."),
             uc("Recipe Scale-Up", "R&D", "product", "Lab recipes translated to plant parameters with risk guards.")],
        ),
        "sources": {
            "sap-pppi": {"t": "SAP PP-PI", "u": "https://www.sap.com/products/scm/process-industries.html"},
            "oracle-pm": {"t": "Oracle Process Manufacturing", "u": "https://www.oracle.com/scm/manufacturing/"},
            "aspentech": {"t": "Aspen Technology", "u": "https://www.aspentech.com/"},
            "aveva-pi": {"t": "AVEVA PI System", "u": "https://www.aveva.com/en/products/pi-system/"},
            "honeywell": {"t": "Honeywell Forge", "u": "https://www.honeywell.com/us/en/products/automation"},
            "opcenter-psm": {"t": "Siemens Opcenter PSM", "u": "https://plm.sw.siemens.com/en-US/opcenter/"},
            "labware": {"t": "LabWare LIMS", "u": "https://www.labware.com/"},
            "samplemanager": {"t": "Thermo SampleManager", "u": "https://www.thermofisher.com/samplemanager"},
            "sphera": {"t": "Sphera", "u": "https://sphera.com/"},
            "maximo": {"t": "IBM Maximo", "u": "https://www.ibm.com/products/maximo"},
            "sap-pm": {"t": "SAP Plant Maintenance", "u": "https://www.sap.com/products/scm/asset-management.html"},
            "sap-tm": {"t": "SAP Transportation Management", "u": "https://www.sap.com/products/scm/transportation-logistics.html"},
            "orbcomm": {"t": "ORBCOMM", "u": "https://www.orbcomm.com/"},
            "echa": {"t": "ECHA REACH", "u": "https://echa.europa.eu/regulations/reach"},
            "epa-tri": {"t": "EPA TRI", "u": "https://www.epa.gov/toxics-release-inventory-tri-program"},
            "icis": {"t": "ICIS", "u": "https://www.icis.com/"},
        },
    },
}
