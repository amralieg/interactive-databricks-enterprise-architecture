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
                    [["Genie One", "Ask what last month's issued premium was by product without waiting on actuarial."], ["AI/BI", "Persistency, mortality and margin on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"in-force\" means one thing across admin and finance."]],
                    sub=[
                        ["Chief Executive", "new-business volume, embedded value and the growth-versus-capital trade across the book."],
                        ["Chief Financial Officer", "statutory reserves, risk-based capital and the expense ratio by product line."],
                        ["Treasury & Investments", "asset-liability matching and the investment income backing long-dated liabilities."],
                    ],
                    ucs=["Embedded Value", "New Business Strain", "Reserve Adequacy", "Reinsurance Recovery"]),
                biz("Actuarial & Reserving", "AI/BI", "Appointed actuaries on reserve adequacy, mortality and lapse experience studies and the model governance a statutory opinion depends on.",
                    [["Reserve Analytics Workbench", "Experience versus pricing assumptions before opinion sign-off."], ["AI/BI", "Reserve roll-forward and variance on certified Metric Views."], ["Unity Catalog", "One definition of claim and policy counts across systems."]],
                    sub=[
                        ["Appointed Actuary", "reserve adequacy and the statutory opinion that stands behind it."],
                        ["Experience Studies", "mortality, morbidity and lapse experience versus pricing assumptions."],
                        ["Model Governance", "assumption controls and the audit trail every valuation depends on."],
                    ],
                    ucs=["Reserve Adequacy", "New Business Strain", "Embedded Value"]),
                biz("Underwriting", "Model Serving", "Chief underwriters on straight-through-processing rates, evidence-ordering bottlenecks and mortality leakage before an offer expires.",
                    [["Underwriting Decision Hub", "Risk class and evidence status before offers expire."], ["Model Serving", "Mortality and lapse models scored at application."], ["MLflow", "Every underwriting model run tracked for audit."]],
                    sub=[
                        ["Chief Underwriter", "straight-through-processing rates and mortality leakage before offers expire."],
                        ["Case Underwriters", "evidence completeness and risk classification on individual applications."],
                        ["Underwriting Rules", "the automated rules and evidence-ordering logic behind accelerated issue."],
                    ],
                    ucs=["Mortality Underwriting", "Straight-Through Processing"]),
                biz("Claims", "Lakehouse//RT", "Claims operations on death verification, contestable-period review and beneficiary payout, ranking open claims by SLA and fraud signal before disbursement.",
                    [["Claims Adjudication Console", "Open claims ranked by SLA and fraud signals."], ["Lakehouse//RT", "Claim status at operational latency."], ["AI/BI", "Severity and cycle time on governed definitions."]],
                    sub=[
                        ["Claims Operations", "death and disability intake, cycle time and the payout SLA."],
                        ["Contestable Review", "early-duration and contestable-period investigation before benefit release."],
                        ["Claims Fraud & SIU", "fraud signals and referrals raised ahead of disbursement."],
                    ],
                    ucs=["Claims Fraud Detection", "Reinsurance Recovery", "Reserve Adequacy"]),
                biz("Distribution", "CustomerLake", "Agency leaders on producer productivity, block persistency and suitability compliance when a lapse or replacement spike shows up.",
                    [["Agent Performance Hub", "Production, persistency and complaints by channel."], ["CustomerLake", "Household segments without copying CRM exports elsewhere."], ["Genie One", "Ask which agents drove last month's lapse spike."]],
                    sub=[
                        ["Agency Leadership", "producer productivity, block persistency and channel mix."],
                        ["Suitability & Compliance", "replacement activity and suitable-sale monitoring across the field."],
                        ["Sales Enablement", "next-best-offer and cross-sell into in-force households."],
                    ],
                    ucs=["Lapse & Persistency", "Agent Suitability", "Cross-sell Propensity"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the policy-admin, underwriting and reinsurance feeds; own the Bronze to Silver path and the pager when a bordereau load breaks.",
                    [["Lakeflow Connect", "Managed connectors for FINEOS, underwriting and finance sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on policy and claims feeds."], ["Lakewatch", "Freshness on the tables actuarial and distribution read every morning."]],
                    sub=[
                        ["Ingestion Engineering", "the FINEOS, underwriting and reinsurance feeds and the bordereau loads."],
                        ["Pipeline Reliability", "Bronze-to-Silver expectations and the pager when a load breaks."],
                        ["Platform & Governance", "Unity Catalog structure and access across admin and finance data."],
                    ],
                    ucs=["Straight-Through Processing", "Reinsurance Recovery", "Reserve Adequacy"]),
                biz("Data Scientists", "MLflow", "Mortality, lapse and claims-fraud models, and whether they still hold across an experience study.",
                    [["Feature Store", "Policy and party features defined once for training and serving."], ["MLflow", "Every underwriting model run tracked for audit and reproduction."], ["Model Serving", "Mortality and lapse models scored at application and renewal."]],
                    sub=[
                        ["Mortality & Lapse Modelling", "the mortality, morbidity and lapse models scored at application and renewal."],
                        ["Claims Fraud Science", "the anomaly and network models behind claims referrals."],
                        ["Model Validation", "whether a model still holds across an experience study."],
                    ],
                    ucs=["Mortality Underwriting", "Lapse & Persistency", "Claims Fraud Detection", "Cross-sell Propensity"]),
                biz("App Developers", "Apps", "Ship the underwriting, claims and agent-performance applications the carrier works in, hosted next to governed data.",
                    [["Apps", "Underwriting and claims screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for servicing and claims writes."], ["Agent Bricks", "Agents that draft an underwriting or claims decision against governed tools."]],
                    sub=[
                        ["Underwriting & Claims Apps", "the decision hub and adjudication console underwriters and adjusters work in."],
                        ["Servicing & Writeback", "Lakebase-backed servicing and claims writes into admin."],
                        ["Agent Experience", "the producer-facing performance and suitability screens."],
                    ],
                    ucs=["Straight-Through Processing", "Claims Fraud Detection", "Agent Suitability"]),
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
                uc("Mortality Underwriting", "Risk selection", "people", "Applicant risk classified with evidence completeness tracked before bind.",
                    problem="Applications wait on labs, APS and exam evidence scattered across vendors, so cases sit for days and a mortality misread only surfaces after the offer is already bound.",
                    who="Underwriting",
                    how="Application, exam and MIB evidence land through Lakeflow, are conformed on Delta Lake and scored against mortality models in Model Serving from the Underwriting Decision Hub before bind.",
                    comps=["Underwriting Decision Hub", "Munich Re ALLFINANZ", "Model Serving", "MLflow", "Feature Store"],
                    stories=[
                        ["From static policies to autonomous insurance: how AI enables real-time coverage", "https://www.databricks.com/blog/static-policies-autonomous-insurance-how-ai-enables-real-time-coverage"],
                    ]),
                uc("Lapse & Persistency", "Retention", "gauge", "Policies at risk of lapse identified from payment, service and engagement signals.",
                    problem="Lapse signals sit in billing, servicing and contact-centre systems that never join up, so a policy is flagged only after the grace period closes and the block quietly erodes.",
                    who="Distribution",
                    how="Payment, servicing and engagement features are built in Feature Store and scored in Model Serving, surfacing at-risk policies by agent and channel in the Agent Performance Hub.",
                    comps=["Agent Performance Hub", "Model Serving", "Feature Store", "AI/BI", "CustomerLake"],
                    stories=[
                        ["Distribution optimization reference architecture for insurance", "https://www.databricks.com/resources/architectures/distribution-optimization-reference-architecture-for-insurance"],
                    ]),
                uc("Claims Fraud Detection", "Integrity", "stream", "Suspicious death and disability claims flagged before payout.",
                    problem="Death and disability claims run under payout SLAs, yet contestability checks and fraud signals sit in separate tools, so questionable claims are paid before anyone connects them.",
                    who="Claims",
                    how="Claims, policy and party feeds land in Lakehouse//RT and are scored with AI Functions and Model Serving, ranking suspect claims in the Claims Adjudication Console before disbursement.",
                    comps=["Claims Adjudication Console", "Sedgwick Life Claims", "Model Serving", "Lakehouse//RT", "AI Functions"],
                    stories=[
                        ["Smart Claims: automating claims processing on Databricks", "https://www.databricks.com/resources/demos/tutorials/lakehouse-platform/dbdemos-fsi-smart-claims"],
                        ["Navigating the impact of AI in insurance: opportunities and challenges", "https://www.databricks.com/blog/navigating-impact-ai-insurance-opportunities-and-challenges"],
                    ]),
                uc("Reserve Adequacy", "Actuarial", "chart", "Reserve roll-forward and experience variance explained before opinion sign-off.",
                    problem="Reserve roll-forwards lean on experience data stitched from admin, claims and actuarial systems by hand, so variance surfaces late and the opinion rests on numbers no one can quickly replay.",
                    who="Actuarial & Reserving",
                    how="Conformed policy and claims data feed the Reserve Analytics Workbench, with Unity Catalog holding one definition of counts and AI/BI showing reserve variance on Delta Lake before sign-off.",
                    comps=["Reserve Analytics Workbench", "Moody's Analytics AXIS", "Unity Catalog", "AI/BI", "Delta Lake"],
                    stories=[
                        ["Milliman modernizes actuarial data infrastructure and governance with Databricks", "https://www.databricks.com/customers/milliman"],
                    ]),
                uc("New Business Strain", "Finance", "market", "Acquisition costs and strain capital modelled by product and distribution channel.",
                    problem="Acquisition cost and reserve strain are modelled per product long after issue, so finance cannot see how a distribution push or a new rider drains capital until the quarter closes.",
                    who="CEO & CFO",
                    how="Issued-business, commission and reserve data are conformed on Delta Lake and modelled in the Reserve Analytics Workbench, so strain by product and channel is queryable in AI/BI and Genie One.",
                    comps=["Reserve Analytics Workbench", "Moody's Analytics AXIS", "AI/BI", "Unity Catalog", "Genie One"]),
                uc("Agent Suitability", "Compliance", "gavel", "Sales practices and replacement activity monitored against suitability rules.",
                    problem="Suitability and replacement rules are checked in periodic manual reviews, so a churning book or an unsuitable annuity sale is caught in audit rather than when the pattern first appears.",
                    who="Distribution",
                    how="Sales, replacement and complaint data are conformed under Unity Catalog and scored with AI Functions, surfacing suitability outliers by producer in the Agent Performance Hub for review.",
                    comps=["Agent Performance Hub", "Salesforce Financial Services", "AI Functions", "Unity Catalog", "AI/BI"]),
                uc("Reinsurance Recovery", "Treaty", "partner", "Ceded claims and experience reconciled to bordereaux without manual disputes.",
                    problem="Ceded premium and claims are reconciled to reinsurer bordereaux by hand across treaties, so recoveries are missed, disputes drag on and the net position is never quite trusted.",
                    who="CEO & CFO",
                    how="Bordereaux, ceded claims and treaty terms are conformed on Delta Lake under Unity Catalog and reconciled in AI/BI, then shared back to reinsurers over Open Sharing without file swaps.",
                    comps=["Reinsurance Bordereaux", "Unity Catalog", "Delta Lake", "Open Sharing", "AI/BI"]),
                uc("Cross-sell Propensity", "Growth", "custlake", "Annuity and supplemental offers scored from in-force household relationships.",
                    problem="In-force households hold obvious annuity and supplemental openings, but relationships are locked in CRM and admin silos, so agents chase cold lists instead of the next best offer.",
                    who="Distribution",
                    how="Household relationships from CustomerLake and admin feed propensity models in Model Serving, with scored offers surfaced by agent in the Agent Performance Hub and explored in Genie One.",
                    comps=["Agent Performance Hub", "CustomerLake", "Model Serving", "Feature Store", "Genie One"],
                    stories=[
                        ["Customer 360 reference architecture for insurance", "https://www.databricks.com/resources/architectures/c360-reference-architecture-for-insurance"],
                    ]),
                uc("Straight-Through Processing", "Operations", "api", "Clean applications issued without manual touch when evidence and rules align.",
                    problem="Clean applications still stop for manual touch because evidence, rules and admin systems never line up, so simple cases take as long as complex ones and applicants abandon.",
                    who="Underwriting",
                    how="ACORD messages land via Lakeflow, are evidence-checked with AI Functions and scored in Model Serving, then auto-issued from the Underwriting Decision Hub with servicing state on Lakebase.",
                    comps=["Underwriting Decision Hub", "ACORD Life Standards", "AI Functions", "Model Serving", "Lakebase"],
                    stories=[
                        ["AXA Japan modernizes data and analytics with Databricks", "https://www.databricks.com/customers/axa-japan"],
                        ["Navigating the impact of AI in insurance: opportunities and challenges", "https://www.databricks.com/blog/navigating-impact-ai-insurance-opportunities-and-challenges"],
                    ]),
                uc("Embedded Value", "Strategy", "product", "In-force value and new business contribution tracked for portfolio decisions.",
                    problem="Embedded value and new-business contribution are assembled from actuarial extracts quarters late, so portfolio and reinsurance decisions run on a picture of the book that is already stale.",
                    who="CEO & CFO",
                    how="In-force, reserve and margin data are conformed under Unity Catalog and rolled up in the Reserve Analytics Workbench, so embedded value by product is queryable in AI/BI and Genie One.",
                    comps=["Reserve Analytics Workbench", "Moody's Analytics AXIS", "AI/BI", "Genie One", "Unity Catalog"]),
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
