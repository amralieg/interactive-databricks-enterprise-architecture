import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    """Business tiles plus an explicit, industry-specific Technical group of 3."""
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_HEALTHCARE = {
    'healthcare': {
        "label": "Healthcare",
        "blurb": "Health systems and hospitals: EHR clinical data, revenue cycle, capacity management, population health and quality reporting.",
        "medallion": medallion(
            "Raw clinical feeds",
            "HL7 ADT and ORU messages, FHIR resources, charge master transactions, imaging DICOM metadata and device telemetry, landed exactly as received so a diagnosis or a charge can always be replayed.",
            "Conformed patient, encounter",
            "Patients, encounters, orders and charges resolved into single conformed entities across EHR, billing and ancillary systems, with MRNs reconciled and transfers stitched to one episode.",
            "LOS, margin, outcomes",
            "Contracted products clinical and finance leaders run on: length of stay, contribution margin by service line, readmission rates, and quality measure attainment.",
        ),
        "rails": {
            "src": [
                {"box": "EHR & Clinical", "ic": "erp", "tiles": [
                    tile("Epic Caboodle", "db", "Orders, results, notes and billing extracts from the hospital EHR of record.", "epic"),
                    tile("Oracle Health Millennium", "erp", "Inpatient and ambulatory clinical, scheduling and documentation for Cerner estates.", "oracle-millennium"),
                    tile("Meditech Expanse", "sheet", "Acute and post-acute clinical records for community hospital networks.", "meditech")
                ]},
                {"box": "Revenue Cycle", "ic": "market", "tiles": [
                    tile("R1 RCM Platform", "market", "Charge capture, claims scrubbing, denials and patient collections workflow.", "r1-rcm"),
                    tile("Waystar Claims", "api", "Eligibility, prior auth status and remittance advice across payers.", "waystar"),
                    tile("3M CodeAssist", "gavel", "CDI queries, DRG grouping and coding compliance suggestions.", "3m-codeassist")
                ]},
                {"box": "Imaging & Devices", "ic": "iot", "tiles": [
                    tile("Philips IntelliSpace", "stream", "Radiology worklists, study metadata and dose metrics from imaging PACS.", "philips-pacs"),
                    tile("Capsule Medical Device", "iot", "Bedside monitor vitals, ventilator settings and infusion pump alarms.", "capsule"),
                    tile("Masimo Patient SafetyNet", "gauge", "Continuous pulse oximetry and early warning scores from wearable sensors.", "masimo")
                ]},
                {"box": "Operations & Staffing", "ic": "people", "tiles": [
                    tile("TeleTracking Capacity", "gauge", "Bed requests, patient placement and transfer centre milestones.", "teletracking"),
                    tile("Kronos Workforce", "people", "Nurse schedules, acuity staffing and overtime by unit.", "kronos"),
                    tile("Press Ganey Experience", "partner", "HCAHPS and point-of-care patient satisfaction surveys.", "press-ganey")
                ]},
                fed_group(
                    "Affiliate EHR Feeds",
                    "Joint venture and affiliated clinic clinical summaries left at partner systems and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("HL7 FHIR Bulk Data", "api", "Patient, encounter and observation exports normalised on ingest for analytics.", "fhir-bulk"),
                tile("CMS Quality Reporting", "gavel", "Hospital compare and value-based programme specifications consumed inbound.", "cms-quality"),
                tile("Syndromic Surveillance", "stream", "Public health case feeds exchanged under state reporting agreements.")
            ]),
            "ppl": ppl2([
                biz("CEO, CNO & CMO", "Genie One", "The CEO on volume, contribution margin and quality scores; the CNO on staffing and patient safety; the CMO on outcomes and 30-day readmissions.",
                    [["Genie One", "Ask what yesterday's census and contribution margin were without waiting on finance."], ["AI/BI", "Volume, margin and quality on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"contribution margin\" means one thing across the health system."]]),
                biz("Clinical Operations", "Lakehouse//RT", "Bed management, ED throughput and OR scheduling on a typical inpatient day, moving boarding patients before diversion becomes necessary.",
                    [["Capacity Command Centre", "ED boarding and bed placement options costed in real time."], ["Lakehouse//RT", "Live census and acuity at hospital operational latency."], ["AI/BI", "LOS and throughput on governed definitions."]]),
                biz("Revenue Cycle", "AI/BI", "Denials, underpayments and CDI queries that decide whether documented care is actually paid, flagged before the claim leaves the building.",
                    [["Denial Prevention Workbench", "At-risk accounts flagged before claim submission."], ["AI/BI", "Net revenue and denial rate on certified Metric Views."], ["Unity Catalog", "One definition of charges and payments across EHR and RCM."]]),
                biz("Population Health", "Model Serving", "Care managers and physicians on attributed panels, open gaps in care and rising-risk patients before preventable utilisation spikes.",
                    [["Population Health Registry", "Attributed patients ranked by preventable utilisation risk."], ["Model Serving", "Readmission models scored at discharge."], ["CustomerLake", "Panel segments without copying payer files elsewhere."]]),
                biz("Quality & Safety", "AI/BI", "Infection prevention, sepsis-bundle compliance and hospital-acquired-condition reduction, catching the deterioration before the public measure does.",
                    [["Quality Dashboard", "Core measures and HAC rates before public reporting."], ["AI/BI", "Mortality and complication indices on governed definitions."], ["Genie One", "Ask which units drove last month's CLABSI count."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the EHR, revenue-cycle and device feeds; own the Bronze to Silver path and the pager when an HL7 or charge feed breaks.",
                    [["Lakeflow Connect", "Managed connectors for EHR, RCM and ancillary sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on ADT and charge feeds."], ["Lakewatch", "Freshness on the tables the command centre and finance read every morning."]]),
                biz("Data Scientists", "MLflow", "Readmission, sepsis and denial-risk models, and whether they still hold six months after deployment.",
                    [["Feature Store", "Patient and encounter features defined once for training and serving."], ["MLflow", "Every clinical model run tracked for audit and reproduction."], ["Model Serving", "Readmission and sepsis models scored at discharge and bedside."]]),
                biz("App Developers", "Apps", "Ship the capacity, denial-prevention and population-health applications the health system works in, hosted next to governed data.",
                    [["Apps", "Capacity and revenue screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for bed-placement and query writes."], ["Agent Bricks", "Agents that draft a CDI query or discharge plan against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and capacity alerts in the channel operations already works in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Clinical Writeback", "ic": "opdb", "tiles": [
                    tile("EHR Chart Queries", "db", "CDI and quality queries written back into the EHR inbox for physician response.", "epic"),
                    tile("Bed Placement Orders", "gauge", "Accepted bed assignments pushed to transport and nursing workflows.", "teletracking"),
                    tile("Care Gap Outreach", "apps", "Preventive care tasks pushed to ambulatory care teams from panel registries.")
                ]},
                {"box": "Payer & Community", "ic": "partner", "tiles": [
                    tile("Payer Risk Contracts", "share", "Quality and utilisation metrics shared with payers under value-based arrangements."),
                    tile("HIE Clinical Exchange", "api", "Summaries and referrals exchanged with regional health information exchanges.", "fhir-bulk"),
                    tile("Employer Reporting", "partner", "Occupational health and direct-contract outcomes reported to self-insured employers.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("CMS Quality Programs", "gavel", "HAC, readmission and MIPS measures produced from governed clinical tables.", "cms-quality"),
                    tile("State Reporting", "share", "Mandatory infection and utilization filings assembled from Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Researchers, payers and affiliates reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Capacity Command Centre", "Patient flow", "gauge", "ED boarding, bed placement and surgical holds costed in real time before diversion becomes necessary."),
                app("Denial Prevention Workbench", "Revenue integrity", "market", "Accounts at risk of denial flagged from documentation, coding and payer rules before claims submit."),
                app("Population Health Registry", "Attributed panels", "people", "Rising-risk patients and gaps in care ranked for outreach before utilisation spikes."),
                app("Sepsis Surveillance", "Patient safety", "iot", "Early warning from vitals, labs and nursing assessments before bundle compliance windows close."),
            ],
            [
                uc("Hospital Throughput", "Operations", "gauge", "ED boarding, discharge planning and OR turnover optimised as one patient-flow problem."),
                uc("Readmission Reduction", "Quality", "people", "Discharge risk scored and interventions triggered before the 30-day window opens."),
                uc("Denial Management", "Revenue", "market", "Root causes of denials traced to documentation, coding and authorization gaps."),
                uc("Sepsis Early Warning", "Safety", "iot", "Deterioration detected from streaming vitals and labs before codes are called."),
                uc("OR Utilisation", "Surgical", "sheet", "Block time, turnover and case mix analysed to recover lost surgical minutes."),
                uc("Nurse Staffing", "Workforce", "people", "Acuity-adjusted schedules that match census forecasts without chronic overtime."),
                uc("Clinical Documentation", "CDI", "gavel", "Queries raised where clinical truth and billed severity diverge before final coding."),
                uc("Imaging Utilisation", "Ancillary", "stream", "Appropriate use and turnaround analysed by modality and site."),
                uc("Patient Experience", "HCAHPS", "partner", "Satisfaction drivers linked to operational and clinical variables teams can act on."),
                uc("Research Cohorts", "Evidence", "notebook", "De-identified cohorts built from governed EHR data under IRB protocols."),
            ],
        ),
        "sources": {
            "epic": {"t": "Epic Systems EHR", "u": "https://www.epic.com/"},
            "oracle-millennium": {"t": "Oracle Health Millennium", "u": "https://www.oracle.com/industries/healthcare/"},
            "meditech": {"t": "Meditech Expanse", "u": "https://ehr.meditech.com/"},
            "r1-rcm": {"t": "R1 RCM revenue cycle", "u": "https://www.r1rcm.com/"},
            "waystar": {"t": "Waystar healthcare payments", "u": "https://www.waystar.com/"},
            "3m-codeassist": {"t": "3M CodeAssist CDI", "u": "https://www.3m.com/3M/en_US/health-information-systems-us/"},
            "philips-pacs": {"t": "Philips IntelliSpace PACS", "u": "https://www.philips.com/healthcare"},
            "capsule": {"t": "Capsule medical device integration", "u": "https://www.capsuletech.com/"},
            "masimo": {"t": "Masimo Patient SafetyNet", "u": "https://www.masimo.com/"},
            "teletracking": {"t": "TeleTracking capacity management", "u": "https://www.teletracking.com/"},
            "kronos": {"t": "UKG workforce management", "u": "https://www.ukg.com/workforce-management"},
            "press-ganey": {"t": "Press Ganey patient experience", "u": "https://www.pressganey.com/"},
            "fhir-bulk": {"t": "HL7 FHIR Bulk Data Access", "u": "https://hl7.org/fhir/uv/bulkdata/"},
            "cms-quality": {"t": "CMS hospital quality reporting", "u": "https://www.cms.gov/medicare/quality/initiatives/hospital-quality-initiative"}
        },
    },
}
