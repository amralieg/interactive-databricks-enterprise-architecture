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
                biz("Biopharma Leaders", "Genie One", "The CEO on pipeline milestones and supply readiness; the CFO on inventory and write-offs when a pivotal trial reads out or a launch scales.", [["Genie One", "Ask what enrollment pace is versus protocol without waiting on clinical ops."], ["AI/BI", "Enrollment, yield and safety on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"SAE\" means one thing across safety and clinical."]]),
                biz("Clinical Operations", "AI/BI", "Study managers on enrollment versus plan, data quality and monitoring backlog, watching the protocol deviation rate before database lock.", [["Trial Command Centre", "Site enrollment and query aging before database lock."], ["AI/BI", "Enrollment and protocol deviation on governed definitions."], ["Genie One", "Ask which sites are under-enrolling this month."]]),
                biz("Mfg & Supply", "Lakehouse//RT", "Plant and supply on batch release rate, yield and cold-chain integrity when a launch scales past the demand the supply plan forecast.", [["Batch Release Cockpit", "Open deviations blocking release before ship."], ["Lakehouse//RT", "Line state at the latency a batch runs at."], ["Model Serving", "Yield models scored on historian and LIMS feeds."]]),
                biz("Quality & Reg", "Unity Catalog", "QA and RA on deviations, submissions and inspection readiness, tracking batch release rate and CAPA aging before FDA and EMA audits.", [["Quality Command", "CAPA aging and repeat deviations before audits."], ["Unity Catalog", "Lineage from batch record to submission annex."], ["AI/BI", "Release rate and deviation rate on certified Metric Views."]]),
                biz("Medical & Comm", "CustomerLake", "Medical affairs and field teams on safety narratives and HCP engagement, watching serious adverse event rates and compliant outreach coverage.", [["Safety Signal Hub", "Emerging signals triaged before periodic reports."], ["CustomerLake", "HCP segments without copying CRM elsewhere."], ["Apps", "Medical inquiry workflows on governed data."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the EDC, LIMS, MES batch and safety-case feeds; own the Bronze to Silver path and the pager when a GxP pipeline breaks.", [["Lakeflow Connect", "Managed connectors for EDC, LIMS and MES sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on batch and safety-case feeds."], ["Lakewatch", "Freshness on the enrollment and release tables study teams read."]]),
                biz("Data Scientists", "MLflow", "Enrollment-forecast, yield, safety-signal and cold-chain models, and whether they still hold six months after deployment under GxP validation.", [["Feature Store", "Historian and LIMS features read identically in training and serving."], ["MLflow", "Every enrollment and yield run tracked for audit and reproduction."], ["Model Serving", "Yield and signal models scored on historian and ICSR feeds."]]),
                biz("App Developers", "Apps", "Ship the trial command, batch release and safety-signal applications clinical and quality teams work in, hosted next to governed GxP data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for release-decision state and governed writes."], ["Agent Bricks", "Agents that draft a deviation summary against governed tools."]]),
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
                uc("Enrollment Forecast", "Clinical", "chart", "Site and country enrollment predicted against protocol timelines."),
                uc("Protocol Deviation", "Data quality", "people", "Visit and dosing deviations surfaced before database lock."),
                uc("Safety Signal Detect", "PV", "gavel", "Disproportionality analysis on ICSRs before manual medical review queues swell."),
                uc("Batch Genealogy", "Traceability", "stream", "Raw material to finished dose traced in minutes during quality holds."),
                uc("Yield Optimisation", "Manufacturing", "iot", "Process parameters scored on yield using historian and LIMS history."),
                uc("Cold Chain Integrity", "Distribution", "observ", "Temperature excursions predicted and rerouted before product quality is lost."),
                uc("Demand & Supply", "Commercial", "sheet", "Launch supply aligned to enrollment and country approval waves."),
                uc("Inspection Readiness", "Quality", "gavel", "Repeat deviations and open CAPAs ranked before FDA or EMA visits."),
                uc("HCP Engagement", "Commercial", "custlake", "Field and medical touchpoints scored for compliant outreach prioritisation."),
                uc("Serialization Trace", "DSCSA", "api", "Saleable returns and suspect product investigations from EPCIS lineage."),
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
