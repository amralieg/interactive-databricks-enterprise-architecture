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


INDUSTRIES_BATCH_HEALTH_INSURANCE = {
    'health_insurance': {
        "label": "Health Insurance",
        "blurb": "Health payers: member enrollment, claims adjudication, provider network, care management and regulatory reporting.",
        "medallion": medallion(
            "Raw claims and enrollment",
            "EDI 837/835 transactions, enrollment files, provider directories, prior auth decisions and pharmacy claims, landed exactly as received so a paid claim or a member month can always be replayed.",
            "Conformed member, claim",
            "Members, providers, claims and authorizations resolved into single conformed entities across core admin and clinical systems, with ICD and CPT codes reconciled to one service line.",
            "MLR, risk, quality",
            "Contracted products actuarial and quality teams run on: medical loss ratio, risk-adjusted revenue, HEDIS measure rates, and fraud waste and abuse savings.",
        ),
        "rails": {
            "src": [
                {"box": "Core Admin & Claims", "ic": "erp", "tiles": [
                    tile("Facets Core Admin", "erp", "Membership, benefits, premium billing and claims adjudication for commercial and government lines.", "facets"),
                    tile("HealthEdge Source", "db", "Enrollment, pricing and payment integrity for Medicare Advantage and Exchange plans.", "healthedge"),
                    tile("Cotiviti Payment Integrity", "market", "Pre- and post-pay edits, DRG validation and recovery findings on paid claims.", "cotiviti")
                ]},
                {"box": "Clinical & UM", "ic": "people", "tiles": [
                    tile("Epic Payer Platform", "custlake", "Prior authorization, care management notes and member clinical summaries from provider connectivity.", "epic-payer"),
                    tile("NaviNet Prior Auth", "api", "Authorization requests, determinations and appeal status exchanged with provider portals.", "navinet"),
                    tile("Change Healthcare Clinical", "stream", "Lab, imaging and ADT feeds supplementing claims with clinical context.", "change-healthcare")
                ]},
                {"box": "Pharmacy & Network", "ic": "product", "tiles": [
                    tile("CVS Caremark PBM", "market", "Pharmacy claims, formulary access edits, specialty dispensing and rebate accruals from the pharmacy benefit manager.", ["caremark", "mmit", "accredo"]),
                    tile("Symplr Provider Data", "people", "Credentialing, roster and directory accuracy for network adequacy.", "symplr"),
                    tile("CMS Encounter Data", "gavel", "Risk adjustment diagnoses and encounter records submitted for Medicare Advantage.", "cms-encounter")
                ]},
                fed_group(
                    "TPA Sub-claims",
                    "Third-party administrator claim detail left at TPAs and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("X12 EDI Clearinghouse", "stream", "837 institutional and professional claims normalised on ingest through the multi-payer network with companion guide validation.", ["x12-edi", "avality"]),
                tile("NCQA HEDIS Measures", "gavel", "Measure specification updates consumed inbound before HEDIS season.", "ncqa-hedis"),
                tile("CMS Risk Model Files", "chart", "HCC coefficients and model software updates for risk adjustment scoring.")
            ]),
            "ppl": ppl2([
                biz("CEO & CFO", "Genie One", "The CEO on membership growth and medical loss ratio; the CFO on risk-adjusted revenue, medical trend and reserve adequacy by line of business.",
                    [["Genie One", "Ask what medical trend was last month by line of business without waiting on actuarial."], ["AI/BI", "MLR, membership and quality on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"paid claim\" means one thing across admin systems."]]),
                biz("Actuarial & Finance", "AI/BI", "Pricing, reserving and risk-score reconciliation for Medicare and commercial blocks, chasing HCC completeness before the submission window closes.",
                    [["Risk Adjustment Workbench", "HCC gaps and encounter completeness before submission."], ["AI/BI", "MLR and trend on certified Metric Views the board reads."], ["Unity Catalog", "One definition of premium and claims across lines."]]),
                biz("Care Management", "Model Serving", "Nurses and care coordinators on rising-risk members, open gaps in care and readmission prevention before an avoidable ED visit or admission.",
                    [["Care Manager Console", "Rising-risk members ranked before ED utilisation spikes."], ["Model Serving", "Risk models scored at enrollment and monthly refresh."], ["CustomerLake", "Member segments without copying clinical exports elsewhere."]]),
                biz("Provider Relations", "AI/BI", "Contracting on network adequacy, value-based arrangement performance and out-of-network leakage when a provider dispute lands.",
                    [["Provider Scorecard", "Quality and cost metrics by TIN and contract."], ["AI/BI", "Network leakage and adequacy on governed definitions."], ["Genie One", "Ask which specialties drive out-of-network spend."]]),
                biz("Fraud & Integrity", "Lakehouse//RT", "SIU investigators on aberrant provider billing patterns, duplicate claims and pharmacy fraud, flagged pre-pay before dollars go out the door.",
                    [["FWA Command Centre", "Anomaly clusters flagged before payment releases."], ["Lakehouse//RT", "Pre-pay edits scored at adjudication latency."], ["AI/BI", "Recovery and avoidance on certified Metric Views."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the EDI claims, enrollment and clinical feeds; own the Bronze to Silver path and the pager when an 837 load breaks.",
                    [["Lakeflow Connect", "Managed connectors for core admin, clinical and pharmacy sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on claims and enrollment feeds."], ["Lakewatch", "Freshness on the tables actuarial and care teams read every morning."]]),
                biz("Data Scientists", "MLflow", "Risk-adjustment, rising-risk and fraud-waste-and-abuse models, and whether they still hold across a plan year.",
                    [["Feature Store", "Member features defined once for training and serving."], ["MLflow", "Every risk model run tracked for audit and reproduction."], ["Model Serving", "Risk and FWA models scored at enrollment and adjudication."]]),
                biz("App Developers", "Apps", "Ship the care manager, risk-adjustment and FWA applications the plan works in, hosted next to governed data.",
                    [["Apps", "Care and integrity screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for care-plan and claims-edit writes."], ["Agent Bricks", "Agents that draft an outreach or edit override against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and care team updates in the channel coordinators already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Admin Writeback", "ic": "opdb", "tiles": [
                    tile("Claims Edit Overrides", "db", "Medical director and SIU decisions written back into adjudication before payment.", "facets"),
                    tile("Care Plan Tasks", "apps", "Outreach and intervention tasks pushed to care manager workflows.", "epic-payer"),
                    tile("Provider Roster Updates", "people", "Directory corrections written back after credentialing review.", "symplr")
                ]},
                {"box": "Provider & Members", "ic": "partner", "tiles": [
                    tile("Provider Portal Data", "share", "Quality scorecards and remittance detail shared with provider groups over Delta Sharing."),
                    tile("Member App Personalisation", "custlake", "Benefit and care gap nudges triggered from governed member segments."),
                    tile("Broker & Employer Reporting", "partner", "Group renewal and experience metrics exchanged with distribution partners.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("CMS Star & HEDIS", "gavel", "HEDIS, Stars and MLR reports produced from the same governed tables operations runs on.", "ncqa-hedis"),
                    tile("State Filing Packages", "share", "Rate and form filings assembled from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Employers, providers and regulators reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Care Manager Console", "Population health", "people", "Rising-risk members, gaps in care and authorised interventions on one screen for nurse care managers."),
                app("Risk Adjustment Workbench", "Medicare revenue", "chart", "HCC capture gaps and encounter completeness scored before CMS submission windows close."),
                app("FWA Command Centre", "Payment integrity", "gauge", "Provider and pharmacy anomaly clusters flagged before claims pay or after for recovery."),
                app("Provider Scorecard", "Network value", "market", "Quality, cost and patient experience by TIN for value-based contract negotiations."),
            ],
            [
                uc("Risk Adjustment", "Medicare", "chart", "HCC capture and encounter data completeness maximised before annual risk model runs."),
                uc("Medical Loss Ratio", "Finance", "market", "MLR tracked by line and market with trend drivers actuaries can explain to regulators."),
                uc("HEDIS Quality", "Stars", "gavel", "Measure gaps closed through outreach before submission season, not after chart chase."),
                uc("Fraud Waste & Abuse", "Integrity", "gauge", "Billing patterns and pharmacy anomalies detected pre-pay and recovered post-pay."),
                uc("Care Management", "Clinical", "people", "High-cost members identified and engaged before preventable admissions."),
                uc("Network Adequacy", "Provider", "globe", "Directory accuracy and time-and-distance standards monitored for regulatory compliance."),
                uc("Prior Auth Optimisation", "Utilisation", "api", "Authorization turnaround and denial overturn rates improved without loosening medical necessity."),
                uc("Pharmacy Trend", "PBM", "product", "Specialty spend, formulary adherence and rebate performance reconciled to medical trend."),
                uc("Member Retention", "Growth", "custlake", "Disenrollment risk scored from service complaints, claims gaps and digital engagement."),
                uc("Value-Based Contracts", "Provider", "partner", "Shared savings and quality bonuses calculated from governed claims and clinical data."),
            ],
        ),
        "sources": {
            "facets": {"t": "Oracle Health Facets", "u": "https://www.oracle.com/health/"},
            "healthedge": {"t": "HealthEdge Source", "u": "https://healthedge.com/solutions/source"},
            "cotiviti": {"t": "Cotiviti payment integrity", "u": "https://www.cotiviti.com/solutions/payment-accuracy"},
            "epic-payer": {"t": "Epic Payer Platform", "u": "https://www.epic.com/software/payer-platform"},
            "navinet": {"t": "NaviNet prior authorization", "u": "https://www.navinet.net/"},
            "change-healthcare": {"t": "Change Healthcare clinical connectivity", "u": "https://www.changehealthcare.com/"},
            "caremark": {"t": "CVS Caremark pharmacy benefits", "u": "https://www.caremark.com/"},
            "accredo": {"t": "Accredo specialty pharmacy", "u": "https://www.accredo.com/"},
            "mmit": {"t": "MMIT formulary access", "u": "https://www.mmitnetwork.com/"},
            "symplr": {"t": "Symplr provider management", "u": "https://www.symplr.com/"},
            "avality": {"t": "Avality multi-payer network", "u": "https://www.availity.com/"},
            "cms-encounter": {"t": "CMS encounter data submission", "u": "https://www.cms.gov/medicare/payment/medicare-advantage-rates-statistics/risk-adjustment"},
            "x12-edi": {"t": "X12 EDI standards", "u": "https://x12.org/"},
            "ncqa-hedis": {"t": "NCQA HEDIS measures", "u": "https://www.ncqa.org/hedis/"}
        },
    },
}
