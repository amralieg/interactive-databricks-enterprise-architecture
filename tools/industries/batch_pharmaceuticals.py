import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl_rail2(business_tiles, tech_tiles):
    """People rail with per-industry Technical roles instead of shared TECH_PPL."""
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles},
    ]


INDUSTRIES_BATCH_PHARMACEUTICALS = {
    'pharmaceuticals': {
        "label": "Pharmaceuticals",
        "blurb": "Drug discovery through commercial: clinical trials, GxP manufacturing, regulatory submissions and pharmacovigilance for biopharma and generics.",
        "medallion": medallion(
            "Raw trial and plant",
            "EDC case reports, lab LIMS results, MES batch records, safety cases and distribution shipments, landed exactly as received so a subject visit or a batch lot can always be replayed as it stood.",
            "Conformed subject, batch",
            "Patients, sites, batches and products resolved into single conformed entities across clinical, quality and supply systems, with randomisation and genealogy reconciled and adverse events stitched to one safety record.",
            "Enrollment, yield, safety",
            "Contracted products clinical and commercial leaders run on: enrollment versus plan, batch yield and release rate, and serious adverse event rates by product.",
        ),
        "rails": {
            "src": [
                {"box": "Clinical & EDC", "ic": "people", "tiles": [
                        tile("Medidata Rave EDC", "people", "Case report forms, visit schedules and query management from pivotal trials.", "medidata-rave"),
                        tile("Veeva Vault CTMS", "sheet", "Site feasibility, monitoring visits and enrollment tracking.", "veeva-ctms"),
                        tile("Oracle Clinical One", "db", "Unified clinical data hub for trials across modalities and regions.", "oracle-clinical"),
                    ]},
                {"box": "GxP Manufacturing", "ic": "stream", "tiles": [
                        tile("Siemens Opcenter Pharma", "stream", "Electronic batch records, dispensing and equipment logs from GMP suites.", "opcenter-pharma"),
                        tile("Rockwell PharmaSuite", "iot", "Packaging line events, serialization and line clearance records.", "pharmasuite"),
                        tile("SAP S/4HANA PP", "erp", "Production orders, material consumption and co-product yields.", "sap-s4"),
                    ]},
                {"box": "Quality & LIMS", "ic": "gavel", "tiles": [
                        tile("LabWare LIMS", "gavel", "Stability, release and environmental monitoring assay results.", "labware"),
                        tile("MasterControl QMS", "gavel", "Deviations, CAPA and change control tied to batches and sites.", "mastercontrol"),
                        tile("Veeva QualityDocs", "product", "Specifications, SOPs and approved label artwork.", "veeva-quality"),
                    ]},
                {"box": "Safety & Commercial", "ic": "custlake", "tiles": [
                        tile("ArisGlobal LifeSphere", "gavel", "Individual case safety reports, signal detection and regulatory submissions.", "arisglobal"),
                        tile("IQVIA OCE", "partner", "Field force activity, sample accountability and call notes.", "iqvia-oce"),
                        tile("Veeva CRM", "custlake", "HCP engagement, consent and medical inquiry workflows.", "veeva-crm"),
                    ]},
                fed_group("Partner CMO Inventory", "Contract manufacturer batch status queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("CDISC SDTM / ADaM", "api", "Clinical datasets validated on ingest against CDISC standards before submission builds.", "cdisc"),
                tile("FDA FAERS Feeds", "gavel", "Public safety reference cases consumed inbound for signal triage.", "fda-faers"),
                tile("GS1 EPCIS Pharma", "stream", "Serialization and distribution events for DSCSA traceability.", "gs1-epcis"),
            ]),
            "ppl": ppl_rail2([
                biz("Biopharma Leaders", "Genie One", "The CEO on pipeline milestones and supply readiness; the CFO on inventory and write-offs when a pivotal trial reads out or a launch scales.", [["Genie One", "Ask what enrollment pace is versus protocol without waiting on clinical ops."], ["AI/BI", "Enrollment, yield and safety on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"SAE\" means one thing across safety and clinical."]],
                    sub=[
                        ["CEO", "the pipeline milestones and whether supply is ready when a launch scales."],
                        ["CFO & Treasury", "inventory, write-offs and the capital a launch and its trials consume."],
                        ["Chief Commercial Officer", "launch uptake, country sequencing and revenue against forecast."],
                    ],
                    ucs=["Enrollment Forecast", "Demand & Supply", "Safety Signal Detect"]),
                biz("Clinical Operations", "AI/BI", "Study managers on enrollment versus plan, data quality and monitoring backlog, watching the protocol deviation rate before database lock.", [["Trial Command Centre", "Site enrollment and query aging before database lock."], ["AI/BI", "Enrollment and protocol deviation on governed definitions."], ["Genie One", "Ask which sites are under-enrolling this month."]],
                    sub=[
                        ["Clinical Trial Managers", "enrollment versus plan, site activation and monitoring backlog."],
                        ["Clinical Data Management", "query aging and data quality before database lock."],
                        ["Clinical Supply", "drug supply forecast against enrollment and protocol demand."],
                    ],
                    ucs=["Enrollment Forecast", "Protocol Deviation", "Demand & Supply"]),
                biz("Mfg & Supply", "Lakehouse//RT", "Plant and supply on batch release rate, yield and cold-chain integrity when a launch scales past the demand the supply plan forecast.", [["Batch Release Cockpit", "Open deviations blocking release before ship."], ["Lakehouse//RT", "Line state at the latency a batch runs at."], ["Model Serving", "Yield models scored on historian and LIMS feeds."]],
                    sub=[
                        ["Manufacturing Operations", "batch release rate and yield across the GMP suites."],
                        ["Supply Chain Planning", "launch supply, cold-chain lanes and shortage risk."],
                        ["Serialization & Distribution", "DSCSA trace and saleable returns across partners."],
                    ],
                    ucs=["Yield Optimisation", "Batch Genealogy", "Cold Chain Integrity", "Serialization Trace"]),
                biz("Quality & Reg", "Unity Catalog", "QA and RA on deviations, submissions and inspection readiness, tracking batch release rate and CAPA aging before FDA and EMA audits.", [["Quality Command", "CAPA aging and repeat deviations before audits."], ["Unity Catalog", "Lineage from batch record to submission annex."], ["AI/BI", "Release rate and deviation rate on certified Metric Views."]],
                    sub=[
                        ["Quality Assurance", "deviations, CAPA aging and repeat findings before inspections."],
                        ["Regulatory Affairs", "submissions and inspection readiness across FDA and EMA."],
                        ["Quality Control", "release and stability testing turnaround from the LIMS."],
                    ],
                    ucs=["Inspection Readiness", "Batch Genealogy", "Serialization Trace"]),
                biz("Medical & Comm", "CustomerLake", "Medical affairs and field teams on safety narratives and HCP engagement, watching serious adverse event rates and compliant outreach coverage.", [["Safety Signal Hub", "Emerging signals triaged before periodic reports."], ["CustomerLake", "HCP segments without copying CRM elsewhere."], ["Apps", "Medical inquiry workflows on governed data."]],
                    sub=[
                        ["Pharmacovigilance", "adverse-event signals and SAE rates before periodic reports."],
                        ["Medical Affairs", "medical inquiries and scientific engagement with HCPs."],
                        ["Commercial Field", "compliant outreach coverage and the next action per HCP."],
                    ],
                    ucs=["Safety Signal Detect", "HCP Engagement", "Demand & Supply"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the EDC, LIMS, MES batch and safety-case feeds; own the Bronze to Silver path and the pager when a GxP pipeline breaks.", [["Lakeflow Connect", "Managed connectors for EDC, LIMS and MES sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on batch and safety-case feeds."], ["Lakewatch", "Freshness on the enrollment and release tables study teams read."]],
                    sub=[
                        ["Ingestion Engineering", "the EDC, LIMS, MES and safety-case connectors and their freshness."],
                        ["GxP Validation Engineering", "validated pipelines and expectations that hold under audit."],
                        ["Streaming Platform", "cold-chain and packaging-line events landed at batch latency."],
                    ],
                    ucs=["Batch Genealogy", "Protocol Deviation", "Cold Chain Integrity"]),
                biz("Data Scientists", "MLflow", "Enrollment-forecast, yield, safety-signal and cold-chain models, and whether they still hold six months after deployment under GxP validation.", [["Feature Store", "Historian and LIMS features read identically in training and serving."], ["MLflow", "Every enrollment and yield run tracked for audit and reproduction."], ["Model Serving", "Yield and signal models scored on historian and ICSR feeds."]],
                    sub=[
                        ["Clinical Modelling", "enrollment-forecast and protocol-deviation models per site."],
                        ["Manufacturing Modelling", "yield and cold-chain models on historian and LIMS history."],
                        ["Safety Signal Science", "disproportionality and NLP models over ICSR and case text."],
                    ],
                    ucs=["Enrollment Forecast", "Yield Optimisation", "Safety Signal Detect"]),
                biz("App Developers", "Apps", "Ship the trial command, batch release and safety-signal applications clinical and quality teams work in, hosted next to governed GxP data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for release-decision state and governed writes."], ["Agent Bricks", "Agents that draft a deviation summary against governed tools."]],
                    sub=[
                        ["Clinical & Safety Apps", "the Trial Command Centre and Safety Signal Hub screens."],
                        ["Quality & Release Apps", "the Batch Release Cockpit and Quality Command workflows."],
                        ["Commercial Apps", "the HCP engagement and medical-inquiry screens over governed data."],
                    ],
                    ucs=["Batch Genealogy", "Safety Signal Detect", "Inspection Readiness", "HCP Engagement"]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                        tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                        tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and trial updates in the channel study teams work in (Beta)."),
                        tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code."),
                    ]},
                {"box": "GxP Writeback", "ic": "opdb", "tiles": [
                        tile("MES Batch Release", "stream", "Quality release decisions written back into MES before pallets ship.", "opcenter-pharma"),
                        tile("EDC Query Resolution", "people", "Data queries closed in EDC from governed discrepancy reports.", "medidata-rave"),
                        tile("CAPA Work Orders", "gavel", "Corrective actions assigned in QMS from trending deviations.", "mastercontrol"),
                    ]},
                {"box": "Partners & CMO", "ic": "partner", "tiles": [
                        tile("CMO Batch Exchange", "share", "Batch genealogy and release status shared to contract manufacturers over Delta Sharing."),
                        tile("CRO Data Transfer", "api", "Clinical datasets exchanged with audit trail not unsecured email.", "medidata-rave"),
                        tile("Wholesaler Trace API", "stream", "DSCSA transaction statements served from governed serialization events.", "gs1-epcis"),
                    ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                        tile("FDA / EMA Submissions", "gavel", "eCTD packages and periodic safety reports from governed clinical and safety tables.", "cdisc"),
                        tile("GxP Audit Evidence", "share", "Batch and clinical lineage evidence filed from contracted Gold products."),
                    ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                        tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                        tile("Sharing Recipients", "share", "CROs, CMOs and regulators reading live tables with no copy."),
                    ]},
            ]),
        },
        "top": top_band(
            [
                app("Trial Command Centre", "Enrollment live", "people", "Site enrollment, queries and monitoring backlog on Databricks Apps over Lakebase."),
                app("Batch Release Cockpit", "GxP release", "gavel", "Open deviations and LIMS results blocking shipment before pallets leave."),
                app("Safety Signal Hub", "Pharmacovigilance", "gauge", "Emerging adverse event signals triaged before periodic safety reports."),
                app("Quality Command", "CAPA control", "product", "Deviation trends and CAPA aging before regulatory inspections."),
            ],
            [
                uc("Enrollment Forecast", "Clinical", "chart", "Site and country enrollment predicted against protocol timelines.",
                    problem="Enrollment slips against protocol timelines and nobody sees it until a site is months behind, so rescue sites and budget are approved late and the readout date drifts.",
                    who="Clinical Operations",
                    how="EDC and CTMS feeds land through Lakeflow and enrollment is modelled in Model Serving, surfaced site by site in the Trial Command Centre on Lakebase before database lock.",
                    comps=["Trial Command Centre", "Medidata Rave EDC", "Lakeflow", "Model Serving", "AI/BI"],
                    stories=[
                        ["Novo Nordisk transforms clinical trials with AI", "https://www.databricks.com/customers/novo-nordisk"],
                        ["How Amgen modernized analytics to speed drug development", "https://www.databricks.com/blog/2022/03/22/amgen-modernizes-analytics-with-a-unified-data-lakehouse-to-speed-drug-development-delivery.html"],
                    ]),
                uc("Protocol Deviation", "Data quality", "people", "Visit and dosing deviations surfaced before database lock.",
                    problem="Visit-window and dosing deviations hide inside EDC queries and monitoring notes, so data managers find them at database lock when a fix means reopening the study and re-monitoring sites.",
                    who="Clinical Operations",
                    how="Query, visit and dosing data are conformed on Delta Lake under Unity Catalog with expectations in Lakeflow, so deviations surface in the Trial Command Centre while the visit can still be fixed.",
                    comps=["Trial Command Centre", "Medidata Rave EDC", "Veeva Vault CTMS", "Lakeflow", "Unity Catalog", "Delta Lake"],
                    stories=[
                        ["Novo Nordisk transforms clinical trials with AI", "https://www.databricks.com/customers/novo-nordisk"],
                    ]),
                uc("Safety Signal Detect", "PV", "gavel", "Disproportionality analysis on ICSRs before manual medical review queues swell.",
                    problem="Adverse events arrive as free text in calls, emails and literature and manual review queues swell, so a real signal can sit unseen while case volume climbs faster than reviewers can read.",
                    who="Medical & Comm",
                    how="ICSR and case text are processed with AI Functions and disproportionality models in Model Serving, ranked in the Safety Signal Hub so reviewers triage emerging signals before periodic reports.",
                    comps=["Safety Signal Hub", "ArisGlobal LifeSphere", "FDA FAERS Feeds", "AI Functions", "Model Serving", "Unity Catalog"],
                    stories=[
                        ["Improving drug safety with adverse event detection using NLP", "https://www.databricks.com/blog/2022/01/17/improving-drug-safety-with-adverse-event-detection-using-nlp.html"],
                    ]),
                uc("Batch Genealogy", "Traceability", "stream", "Raw material to finished dose traced in minutes during quality holds.",
                    problem="When a quality hold hits, tracing raw-material lots to finished doses across MES, LIMS and ERP takes days of manual reconciliation, and every hour the batch sits is cost and supply risk.",
                    who="Mfg & Supply",
                    how="Batch records, LIMS results and material moves are conformed on Delta Lake under Unity Catalog, so genealogy from raw lot to finished dose resolves in minutes in the Batch Release Cockpit.",
                    comps=["Batch Release Cockpit", "Siemens Opcenter Pharma", "LabWare LIMS", "SAP S/4HANA PP", "Unity Catalog", "Delta Lake"],
                    stories=[
                        ["Managing recalls with barcode traceability in the data lakehouse", "https://www.databricks.com/blog/managing-recalls-barcode-traceability-delta-lake"],
                        ["How TetraScience accelerates biopharma with production-ready data", "https://www.databricks.com/blog/how-tetrascience-accelerates-biopharma-production-ready-data-and-scientific-intelligence"],
                    ]),
                uc("Yield Optimisation", "Manufacturing", "iot", "Process parameters scored on yield using historian and LIMS history.",
                    problem="Batch yield swings with process parameters nobody can correlate in time, so investigations run weeks after a low-yield lot and the same loss repeats on the next campaign.",
                    who="Mfg & Supply",
                    how="Historian and LIMS history feed yield models in Feature Store and Model Serving, with runs tracked in MLflow, so process parameters are scored against yield before the next batch runs.",
                    comps=["Batch Release Cockpit", "Siemens Opcenter Pharma", "LabWare LIMS", "Feature Store", "Model Serving", "MLflow"],
                    stories=[
                        ["Smart Manufacturing Command Center by Tredence and Databricks", "https://www.databricks.com/company/partners/consulting-and-si/partner-solutions/tredence-smart-manufacturing-command-center"],
                        ["Agents for production lines: trusted decisions in real time", "https://www.databricks.com/blog/agents-production-lines-trusted-decisions-real-time"],
                    ]),
                uc("Cold Chain Integrity", "Distribution", "observ", "Temperature excursions predicted and rerouted before product quality is lost.",
                    problem="Temperature excursions in transit are found after delivery when a shipment is already spoiled, so product is written off and patients wait while lanes that keep failing go unfixed.",
                    who="Mfg & Supply",
                    how="Shipment sensor and logistics events stream into Lakehouse//RT and excursion-risk models in Model Serving flag lanes early, so distribution reroutes before product quality is lost.",
                    comps=["Lakehouse//RT", "Model Serving", "GS1 EPCIS Pharma", "SAP S/4HANA PP", "Delta Lake"],
                    stories=[
                        ["How Johnson & Johnson uses data to optimize its supply chain", "https://www.databricks.com/blog/2022/04/25/democratizing-data-for-supply-chain-optimization.html"],
                    ]),
                uc("Demand & Supply", "Commercial", "sheet", "Launch supply aligned to enrollment and country approval waves.",
                    problem="Launch demand and country approvals move faster than the supply plan, so a scaling launch either stocks out in a new market or writes off product the forecast never needed.",
                    who="Biopharma Leaders",
                    how="Enrollment, approval and commercial signals are conformed under Unity Catalog and demand models in Model Serving align launch supply to approval waves, read in AI/BI by planning and finance.",
                    comps=["SAP S/4HANA PP", "Model Serving", "Unity Catalog", "AI/BI", "Genie One"],
                    stories=[
                        ["How Amgen modernized analytics to speed drug development", "https://www.databricks.com/blog/2022/03/22/amgen-modernizes-analytics-with-a-unified-data-lakehouse-to-speed-drug-development-delivery.html"],
                        ["Integra Life Sciences gains supply and demand visibility", "https://www.databricks.com/customers/integra-life-sciences"],
                    ]),
                uc("Inspection Readiness", "Quality", "gavel", "Repeat deviations and open CAPAs ranked before FDA or EMA visits.",
                    problem="Repeat deviations and open CAPAs scatter across QMS and quality systems, so audit prep is a fire drill and a finding a prior inspection raised is still open when the next one lands.",
                    who="Quality & Reg",
                    how="Deviation, CAPA and batch data are conformed under Unity Catalog and ranked in the Quality Command app on Lakebase, so repeat issues and audit exposure are visible before FDA or EMA visits.",
                    comps=["Quality Command", "MasterControl QMS", "Veeva QualityDocs", "Unity Catalog", "AI/BI", "Lakebase"],
                    stories=[
                        ["Partner solutions built on Databricks Genie for pharma operations", "https://www.databricks.com/blog/transforming-industries-conversational-ai-partner-solutions-built-databricks-genie"],
                        ["How TetraScience accelerates biopharma with production-ready data", "https://www.databricks.com/blog/how-tetrascience-accelerates-biopharma-production-ready-data-and-scientific-intelligence"],
                    ]),
                uc("HCP Engagement", "Commercial", "custlake", "Field and medical touchpoints scored for compliant outreach prioritisation.",
                    problem="Field, medical and digital touchpoints sit in separate systems, so HCPs get uncoordinated, non-compliant outreach and reps cannot see which next action actually matters for each physician.",
                    who="Medical & Comm",
                    how="CRM, prescription and engagement signals are unified in CustomerLake and next-best-action models in Model Serving prioritise compliant outreach delivered into the field workflow.",
                    comps=["Veeva CRM", "IQVIA OCE", "CustomerLake", "Model Serving", "AI Functions"],
                    stories=[
                        ["Elevating customer experience with AI-enabled omnichannel Next Best Action", "https://www.databricks.com/blog/elevating-customer-experience-ai-enabled-omnichannel-next-best-action"],
                        ["Next Best Action for healthcare and life sciences", "https://www.databricks.com/solutions/accelerators/next-best-action-healthcare-and-life-sciences"],
                    ]),
                uc("Serialization Trace", "DSCSA", "api", "Saleable returns and suspect product investigations from EPCIS lineage.",
                    problem="Saleable-return verification and suspect-product checks need item-level history, but serialization events sit in the packaging line and partner systems, so a DSCSA query is a manual hunt.",
                    who="Mfg & Supply",
                    how="EPCIS serialization events are conformed on Delta Lake under Unity Catalog and served as transaction statements over Open Sharing, so returns and suspect-product traces resolve from one lineage.",
                    comps=["GS1 EPCIS Pharma", "Rockwell PharmaSuite", "Unity Catalog", "Delta Lake", "Open Sharing"],
                    stories=[
                        ["How Johnson & Johnson uses data to optimize its supply chain", "https://www.databricks.com/blog/2022/04/25/democratizing-data-for-supply-chain-optimization.html"],
                        ["Managing recalls with barcode traceability in the data lakehouse", "https://www.databricks.com/blog/managing-recalls-barcode-traceability-delta-lake"],
                    ]),
            ],
        ),
        "sources": {
            "medidata-rave": {"t": "Medidata Rave EDC", "u": "https://www.medidata.com/en/clinical-trial-products/clinical-data-management/"},
            "veeva-ctms": {"t": "Veeva Vault CTMS", "u": "https://www.veeva.com/products/vault-ctms/"},
            "oracle-clinical": {"t": "Oracle Clinical One", "u": "https://www.oracle.com/life-sciences/clinical-trials/"},
            "opcenter-pharma": {"t": "Siemens Opcenter Pharma", "u": "https://plm.sw.siemens.com/en-US/opcenter/"},
            "pharmasuite": {"t": "Rockwell PharmaSuite", "u": "https://www.rockwellautomation.com/en-us/industries/life-sciences.html"},
            "sap-s4": {"t": "SAP S/4HANA", "u": "https://www.sap.com/products/erp/s4hana.html"},
            "labware": {"t": "LabWare LIMS", "u": "https://www.labware.com/"},
            "mastercontrol": {"t": "MasterControl QMS", "u": "https://www.mastercontrol.com/"},
            "veeva-quality": {"t": "Veeva QualityDocs", "u": "https://www.veeva.com/products/qualitydocs/"},
            "arisglobal": {"t": "ArisGlobal LifeSphere", "u": "https://www.arisglobal.com/lifesphere/"},
            "iqvia-oce": {"t": "IQVIA OCE", "u": "https://www.iqvia.com/solutions/commercialization"},
            "veeva-crm": {"t": "Veeva CRM", "u": "https://www.veeva.com/products/crm/"},
            "cdisc": {"t": "CDISC standards", "u": "https://www.cdisc.org/"},
            "fda-faers": {"t": "FDA FAERS", "u": "https://www.fda.gov/drugs/surveillance/questions-and-answers-fdas-adverse-event-reporting-system-faers"},
            "gs1-epcis": {"t": "GS1 EPCIS", "u": "https://www.gs1.org/standards/epcis"},
        },
    },
}
