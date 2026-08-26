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


INDUSTRIES_BATCH_LIFE_INSURANCE = {
    'life_insurance': {
        "label": "Life Insurance",
        "blurb": "Life and annuity carriers: policy administration, underwriting, claims, actuarial reserving, reinsurance and distribution across individual and group blocks.",
        "medallion": medallion(
            "Raw policy and claims feeds",
            "Policy administration transactions, underwriting evidence, claims files, agent commissions and reinsurance bordereaux, landed exactly as received so a premium or a reserve can always be replayed.",
            "Conformed policy, party",
            "Policies, insureds, agents and claims resolved into single conformed entities across admin, underwriting and finance systems, with rider and beneficiary relationships stitched to one contract.",
            "Persistency, mortality, margin",
            "Contracted products actuarial and distribution leaders run on: persistency and lapse rates, mortality and morbidity experience, new business strain, and embedded value by product.",
        ),
        "rails": {
            "src": [
                {"box": "Policy Administration", "ic": "erp", "tiles": [
                    tile("FINEOS Life", "erp", "Individual and group life policy issuance, servicing, billing and claims on one admin platform.", "fineos"),
                    tile("Majesco LifePlus", "db", "Policy, billing and claims for life, annuity and supplemental benefits.", "majesco"),
                    tile("Oracle Insurance Policy", "sheet", "Product configuration, policy transactions and financial integration for carriers.", "oracle-insurance")
                ]},
                {"box": "New Business & UW", "ic": "people", "tiles": [
                    tile("Munich Re ALLFINANZ", "partner", "Automated underwriting rules, evidence ordering and risk classification.", "munich-allfinanz"),
                    tile("ExamOne Lab Results", "stream", "Paramedical exams, labs and APS retrieval tied to application case IDs.", "examone"),
                    tile("MIB Underwriting Exchange", "gavel", "Industry application history and code hits at point of underwriting.", "mib")
                ]},
                {"box": "Claims & Customer", "ic": "market", "tiles": [
                    tile("Sedgwick Life Claims", "market", "Death, disability and waiver claims intake, adjudication and payment.", "sedgwick"),
                    tile("Salesforce Financial Services", "custlake", "Agent and policyholder relationships, service cases and cross-sell opportunities.", "sf-finserv"),
                    tile("Call Centre Telephony", "chat", "IVR, call recordings and disposition codes joined to policy and claim events.")
                ]},
                {"box": "Actuarial & Finance", "ic": "chart", "tiles": [
                    tile("Moody's Analytics AXIS", "chart", "Actuarial models, reserves, capital and asset-liability management projections.", "axis"),
                    tile("SAP S/4HANA Insurance", "erp", "General ledger, statutory reporting and investment accounting integration.", "sap-insurance"),
                    tile("Reinsurance Bordereaux", "partner", "Ceded premium, claims and experience reports exchanged with reinsurance partners.")
                ]},
                fed_group(
                    "MGU Admin Feeds",
                    "Managing general underwriter policy detail left at partners and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("ACORD Life Standards", "api", "Application, policy and claims XML messages normalised on ingest for straight-through processing.", "acord"),
                tile("NAIC Statutory Filings", "gavel", "Annual statement schedules and risk-based capital specifications consumed inbound.", "naic"),
                tile("Mortality Table Updates", "chart", "Industry mortality and lapse assumptions published by regulators and reinsurers.")
            ]),
            "ppl": ppl2([
                biz("CEO & CFO", "Genie One", "The CEO on new-business volume and embedded value; the CFO on statutory reserves, risk-based capital and the expense ratio by product line.",
                    [["Genie One", "Ask what last month's issued premium was by product without waiting on actuarial."], ["AI/BI", "Persistency, mortality and margin on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"in-force\" means one thing across admin and finance."]]),
                biz("Actuarial & Reserving", "AI/BI", "Appointed actuaries on reserve adequacy, mortality and lapse experience studies and the model governance a statutory opinion depends on.",
                    [["Reserve Analytics Workbench", "Experience versus pricing assumptions before opinion sign-off."], ["AI/BI", "Reserve roll-forward and variance on certified Metric Views."], ["Unity Catalog", "One definition of claim and policy counts across systems."]]),
                biz("Underwriting", "Model Serving", "Chief underwriters on straight-through-processing rates, evidence-ordering bottlenecks and mortality leakage before an offer expires.",
                    [["Underwriting Decision Hub", "Risk class and evidence status before offers expire."], ["Model Serving", "Mortality and lapse models scored at application."], ["MLflow", "Every underwriting model run tracked for audit."]]),
                biz("Claims", "Lakehouse//RT", "Claims operations on death verification, contestable-period review and beneficiary payout, ranking open claims by SLA and fraud signal before disbursement.",
                    [["Claims Adjudication Console", "Open claims ranked by SLA and fraud signals."], ["Lakehouse//RT", "Claim status at operational latency."], ["AI/BI", "Severity and cycle time on governed definitions."]]),
                biz("Distribution", "CustomerLake", "Agency leaders on producer productivity, block persistency and suitability compliance when a lapse or replacement spike shows up.",
                    [["Agent Performance Hub", "Production, persistency and complaints by channel."], ["CustomerLake", "Household segments without copying CRM exports elsewhere."], ["Genie One", "Ask which agents drove last month's lapse spike."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the policy-admin, underwriting and reinsurance feeds; own the Bronze to Silver path and the pager when a bordereau load breaks.",
                    [["Lakeflow Connect", "Managed connectors for FINEOS, underwriting and finance sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on policy and claims feeds."], ["Lakewatch", "Freshness on the tables actuarial and distribution read every morning."]]),
                biz("Data Scientists", "MLflow", "Mortality, lapse and claims-fraud models, and whether they still hold across an experience study.",
                    [["Feature Store", "Policy and party features defined once for training and serving."], ["MLflow", "Every underwriting model run tracked for audit and reproduction."], ["Model Serving", "Mortality and lapse models scored at application and renewal."]]),
                biz("App Developers", "Apps", "Ship the underwriting, claims and agent-performance applications the carrier works in, hosted next to governed data.",
                    [["Apps", "Underwriting and claims screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for servicing and claims writes."], ["Agent Bricks", "Agents that draft an underwriting or claims decision against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Actuarial and distribution dashboards on serverless SQL with Unity Catalog permissions."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and claims alerts in the channel teams already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Actuarial notebooks against governed policy and experience data.")
                ]},
                {"box": "Admin Writeback", "ic": "opdb", "tiles": [
                    tile("Policy Servicing Updates", "db", "Beneficiary and address changes written back into admin after verification.", "fineos"),
                    tile("Underwriting Decisions", "people", "Approved risk classes and requirements released to issuance workflows.", "munich-allfinanz"),
                    tile("Claims Payments", "market", "Adjudicated claim amounts released to disbursement after fraud review.", "sedgwick")
                ]},
                {"box": "Dist. & Reinsurance", "ic": "partner", "tiles": [
                    tile("Agent Portal Reporting", "share", "Production and persistency scorecards shared with agencies over Delta Sharing."),
                    tile("Reinsurer Bordereaux", "partner", "Ceded experience and claims detail exchanged under treaty agreements."),
                    tile("Broker Illustration Systems", "api", "Approved product illustrations and rates pushed to broker platforms.", "acord")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("NAIC Statutory Statements", "gavel", "Annual statement schedules produced from the same governed tables finance runs on.", "naic"),
                    tile("Experience Study Filing", "share", "Mortality and lapse studies filed from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Reinsurers, distributors and regulators reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Underwriting Decision Hub", "New business", "people", "Application evidence, risk class and straight-through eligibility on one screen before offers expire."),
                app("Claims Adjudication Console", "Benefit payout", "gauge", "Death and disability claims ranked by SLA, contestability and fraud signals before disbursement."),
                app("Reserve Analytics Workbench", "Actuarial", "chart", "Experience versus pricing assumptions reconciled before reserve opinion and statutory filing."),
                app("Agent Performance Hub", "Distribution", "custlake", "Production, persistency and complaint rates by agent and channel for compensation and compliance."),
            ],
            [
                uc("Mortality Underwriting", "Risk selection", "people", "Applicant risk classified with evidence completeness tracked before bind."),
                uc("Lapse & Persistency", "Retention", "gauge", "Policies at risk of lapse identified from payment, service and engagement signals."),
                uc("Claims Fraud Detection", "Integrity", "stream", "Suspicious death and disability claims flagged before payout."),
                uc("Reserve Adequacy", "Actuarial", "chart", "Reserve roll-forward and experience variance explained before opinion sign-off."),
                uc("New Business Strain", "Finance", "market", "Acquisition costs and strain capital modelled by product and distribution channel."),
                uc("Agent Suitability", "Compliance", "gavel", "Sales practices and replacement activity monitored against suitability rules."),
                uc("Reinsurance Recovery", "Treaty", "partner", "Ceded claims and experience reconciled to bordereaux without manual disputes."),
                uc("Cross-sell Propensity", "Growth", "custlake", "Annuity and supplemental offers scored from in-force household relationships."),
                uc("Straight-Through Processing", "Operations", "api", "Clean applications issued without manual touch when evidence and rules align."),
                uc("Embedded Value", "Strategy", "product", "In-force value and new business contribution tracked for portfolio decisions."),
            ],
        ),
        "sources": {
            "fineos": {"t": "FINEOS Life", "u": "https://www.fineos.com/"},
            "majesco": {"t": "Majesco LifePlus", "u": "https://www.majesco.com/solutions/life-insurance/"},
            "oracle-insurance": {"t": "Oracle Insurance Policy Administration", "u": "https://www.oracle.com/industries/financial-services/insurance/"},
            "munich-allfinanz": {"t": "Munich Re ALLFINANZ", "u": "https://www.munichre.com/automation-solutions/en.html"},
            "examone": {"t": "ExamOne paramedical services", "u": "https://www.examone.com/"},
            "mib": {"t": "MIB underwriting exchange", "u": "https://www.mib.com/"},
            "sedgwick": {"t": "Sedgwick claims management", "u": "https://www.sedgwick.com/"},
            "sf-finserv": {"t": "Salesforce Financial Services Cloud", "u": "https://www.salesforce.com/financial-services/"},
            "axis": {"t": "Moody's Analytics AXIS", "u": "https://www.moodysanalytics.com/product-list/axis"},
            "sap-insurance": {"t": "SAP for Insurance", "u": "https://www.sap.com/industries/insurance.html"},
            "acord": {"t": "ACORD standards", "u": "https://www.acord.org/"},
            "naic": {"t": "NAIC statutory reporting", "u": "https://www.naic.org/"},
        },
    },
}
