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


INDUSTRIES_BATCH_CLINICAL_TRIALS = {
    'clinical_trials': {
        "label": "Clinical Trials",
        "blurb": "Protocol design, site operations, patient recruitment, safety monitoring, and regulatory submissions across CROs and sponsors.",
        "medallion": medallion(
            "Raw eCRF and lab feeds",
            "EDC entries, lab results, imaging reads and safety narratives landed exactly as received for audit trail replay.",
            "Conformed subjects and visits",
            "Subjects, visits, sites and adverse events resolved across CTMS, EDC and safety systems.",
            "Enrollment, safety signals",
            "Contracted products clinical ops and medical run on: enrollment velocity, protocol deviation rate and SAE incidence.",
        ),
        "rails": {
            "src": [
                {"box": "EDC & eSource", "ic": "db", "tiles": [
                    tile("Medidata Rave EDC", "db", "Case report forms, queries and audit trails by subject.", "medidata-rave"),
                    tile("Veeva Vault CDMS", "db", "Unified clinical data management and remote monitoring.", "veeva-cdms"),
                    tile("Oracle Clinical One", "db", "Unified platform for randomization and data capture.", "oracle-clinical"),
                ]},
                {"box": "CTMS & Sites", "ic": "sheet", "tiles": [
                    tile("Veeva CTMS", "sheet", "Site feasibility, activation and enrollment tracking.", "veeva-ctms"),
                    tile("Medidata CTMS", "people", "Monitoring visits, action items and site payments.", "medidata-ctms"),
                    tile("Signant SmartSupplies", "product", "IRT, drug supply and depot inventory.", "signant"),
                ]},
                {"box": "Safety & PV", "ic": "gavel", "tiles": [
                    tile("Argus Safety", "gavel", "SAE processing, MedDRA coding and expedited reporting.", "argus"),
                    tile("Veeva Vault Safety", "gavel", "Case intake, narrative generation and submissions.", "veeva-safety"),
                    tile("WHO Drug Dictionary", "product", "Medication coding for concomitant therapies.", "who-dd"),
                ]},
                {"box": "Labs & Imaging", "ic": "stream", "tiles": [
                    tile("LabCorp Central Lab", "stream", "Central lab results with reference ranges by visit.", "labcorp"),
                    tile("Medidata Imaging", "iot", "DICOM reads and lesion measurements for oncology.", "medidata-imaging"),
                    tile("ERT eCOA", "apps", "Patient-reported outcomes and eDiary entries.", "ert-ecoa"),
                ]},
                {"box": "Regulatory", "ic": "share", "tiles": [
                    tile("Veeva RIM", "share", "Submissions, correspondence and health authority commitments.", "veeva-rim"),
                    tile("CDISC Standards", "api", "SDTM and ADaM datasets for regulatory packages.", "cdisc"),
                ]},
                fed_group("Legacy SDTM Mart", "Historical submission datasets queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("ClinicalTrials.gov", "api", "Public trial registry metadata for competitive intelligence.", "clinicaltrials-gov"),
                tile("IQVIA Real World", "partner", "External control arms and epidemiology for protocol design.", "iqvia-rwe"),
                tile("Flatiron Oncology EHR", "custlake", "De-identified oncology records for external comparators.", "flatiron"),
            ]),
            "ppl": ppl2([
                biz("Chief Medical & Clinical Ops", "Genie One",
                    "The CMO on pipeline milestones and study risk; the VP Clinical on enrollment velocity and budget burn against lock timelines.",
                    [["Genie One", "Ask how enrollment is tracking to plan by country."], ["AI/BI", "Milestone and spend on certified Metric Views."], ["Unity Catalog", "One subject definition across EDC and safety."]]),
                biz("Clinical Operations", "Lakehouse//RT",
                    "Site activation, monitoring and enrollment rescue, run on enrollment velocity, screen-failure rate and query aging by site.",
                    [["Enrollment Cockpit", "Site velocity and screen-failure drivers."], ["Lakehouse//RT", "Query aging at operational latency."]]),
                biz("Data Management", "AI/BI",
                    "Database lock readiness, query resolution and SDTM conversion, tracked on open-query aging, data completeness and lock cycle time.",
                    [["Lock Readiness", "Critical variables and open queries by site."], ["AI/BI", "Data quality metrics on governed EDC."]]),
                biz("Medical & Safety", "Model Serving",
                    "DSMB reviews, signal detection and medical monitoring, judged on SAE incidence, time-to-signal and expedited-report timeliness.",
                    [["Safety Signal Hub", "Emerging AE patterns across trials."], ["Model Serving", "Signal detection models on adverse events."]]),
                biz("Biostatistics", "Apps",
                    "Interim analyses, adaptive designs and TLF production, measured on interim-look turnaround, TLF cycle time and protocol-deviation rate.",
                    [["Interim Analysis Workbench", "Controlled access to unblinded results."], ["Apps", "Statistical review apps on governed ADaM."]]),
            ], [
                biz("Data Engineers", "Lakeflow",
                    "Land EDC eCRF entries, central-lab results, imaging reads and safety narratives; own Bronze to Silver and the pager when the enrollment tables stall.",
                    [["Lakeflow Connect", "Managed connectors for EDC, CTMS and safety sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on lab and eCRF feeds."], ["Lakewatch", "Freshness on the enrollment and query tables study teams read daily."]]),
                biz("Data Scientists", "MLflow",
                    "Enrollment-forecast, risk-based-monitoring and safety signal-detection models, and whether they still hold as sites and protocols amend.",
                    [["Feature Store", "Subject and site features read identically in training and serving."], ["MLflow", "Every enrollment and signal model tracked for audit and reproduction."], ["Model Serving", "Signal and monitoring models scored in the review path."]]),
                biz("App Developers", "Apps",
                    "Ship the enrollment cockpit, lock readiness, safety signal hub and interim analysis apps clinical ops and biostats work in, next to governed trial data.",
                    [["Apps", "Study screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for monitoring and review state."], ["Agent Bricks", "Agents that draft narratives and query resolutions against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Spotfire", "chart", "Enrollment and safety dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for enrollment status in study teams."),
                    tile("Notebooks & IDEs", "notebook", "Biostat notebooks on governed SDTM and ADaM."),
                ]},
                {"box": "Sites & CROs", "ic": "partner", "tiles": [
                    tile("Site Payment Portal", "api", "Visit-based payments released after data verification.", "medidata-ctms"),
                    tile("eConsent Platform", "apps", "Consent versions and re-consent pushed to sites.", "veeva-cdms"),
                    tile("IRT Supply Updates", "product", "Depot shipments triggered by enrollment forecasts.", "signant"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Query Auto-Resolution", "db", "Edit checks resolved back to EDC with audit trail.", "medidata-rave"),
                    tile("Safety Expedited Reports", "gavel", "E2B submissions generated from confirmed cases.", "argus"),
                    tile("Enrollment Caps", "gauge", "Country caps enforced in IRT when limits reached.", "signant"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("FDA eCTD Submissions", "share", "Regulatory packages assembled from governed datasets.", "veeva-rim"),
                    tile("DSUR/PSUR Production", "gavel", "Periodic safety reports from pooled safety data.", "veeva-safety"),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Trial and safety products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Partners and regulators via governed sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Enrollment Cockpit", "Site velocity", "gauge", "Screening, randomization and dropout rates by site and country against plan."),
             app("Lock Readiness", "Database lock", "db", "Open queries, missing visits and critical variables blocking lock."),
             app("Safety Signal Hub", "Pharmacovigilance", "gavel", "Emerging adverse event patterns ranked for medical review."),
             app("Interim Analysis Workbench", "Unblinded access", "chart", "Controlled interim looks with full audit trail.")],
            [uc("Enrollment Forecasting", "Operations", "people", "Site and country enrollment predicted against activation curves."),
             uc("Site Selection", "Feasibility", "globe", "Sites ranked by historical enrollment and data quality."),
             uc("Remote Monitoring", "Quality", "observ", "Risk-based monitoring triggers from centralized data review."),
             uc("Safety Signal Detection", "PV", "gavel", "Disproportionality and temporal clustering on adverse events."),
             uc("Protocol Deviation Mgmt", "Compliance", "gavel", "Deviations trended and remediated before inspection findings."),
             uc("SDTM Automation", "Data Mgmt", "db", "Study data converted to SDTM with traceable mappings."),
             uc("Adaptive Trial Design", "Biostats", "chart", "Interim results driving sample size or arm changes."),
             uc("Patient Recruitment", "Digital", "custlake", "Pre-screened cohorts identified from RWE and registries."),
             uc("Supply Forecasting", "IRT", "product", "Depot and site inventory against enrollment scenarios."),
             uc("Regulatory Submissions", "RIM", "share", "eCTD packages produced from governed clinical datasets.")],
        ),
        "sources": {
            "medidata-rave": {"t": "Medidata Rave EDC", "u": "https://www.medidata.com/"},
            "veeva-cdms": {"t": "Veeva Vault CDMS", "u": "https://www.veeva.com/products/vault-cdms/"},
            "oracle-clinical": {"t": "Oracle Clinical One", "u": "https://www.oracle.com/life-sciences/clinical-trials/"},
            "veeva-ctms": {"t": "Veeva CTMS", "u": "https://www.veeva.com/products/ctms/"},
            "medidata-ctms": {"t": "Medidata CTMS", "u": "https://www.medidata.com/"},
            "signant": {"t": "Signant Health", "u": "https://www.signanthealth.com/"},
            "argus": {"t": "Oracle Argus Safety", "u": "https://www.oracle.com/life-sciences/pharmacovigilance/"},
            "veeva-safety": {"t": "Veeva Vault Safety", "u": "https://www.veeva.com/products/vault-safety/"},
            "who-dd": {"t": "WHO Drug Dictionary", "u": "https://www.who-umc.org/"},
            "labcorp": {"t": "Labcorp Drug Development", "u": "https://www.labcorp.com/"},
            "medidata-imaging": {"t": "Medidata Imaging", "u": "https://www.medidata.com/"},
            "ert-ecoa": {"t": "ERT eCOA", "u": "https://www.ert.com/solutions/ecoa/"},
            "veeva-rim": {"t": "Veeva RIM", "u": "https://www.veeva.com/products/regulatory/"},
            "cdisc": {"t": "CDISC", "u": "https://www.cdisc.org/"},
            "clinicaltrials-gov": {"t": "ClinicalTrials.gov", "u": "https://clinicaltrials.gov/"},
            "iqvia-rwe": {"t": "IQVIA Real World Solutions", "u": "https://www.iqvia.com/solutions/real-world-evidence"},
            "flatiron": {"t": "Flatiron Health", "u": "https://flatiron.com/"},
        },
    },
}
