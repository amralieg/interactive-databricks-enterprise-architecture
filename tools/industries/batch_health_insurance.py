import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    app, biz, cons_rail, dashboard, data_out, fed_group, flow, genie, ing_rail,
    medallion, tile, top_band, uc,
)


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
                    tile("Facets Core Admin", "erp", "Membership, benefits, premium billing and claims adjudication for commercial and government lines.", "facets",
                         cat="Payer Core Administration System",
                         what="System of record for membership, benefits, premium billing and claims adjudication across commercial and government lines, emitting member, enrollment and paid-claim transactions.",
                         users="Actuarial & Finance, claims operations and enrollment teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "50-200 GB/day", "Nightly adjudication cycle + intraday deltas"),
                             stream=flow(["semi-structured"], "hundreds of claims/sec at peak", "Continuous CDC"))),
                    tile("HealthEdge Source", "db", "Claims pricing, reimbursement and payment integrity for Medicare Advantage and Exchange plans.", "healthedge",
                         cat="Claims Pricing & Payment Engine",
                         what="Prices claims, applies reimbursement logic and payment integrity for Medicare Advantage and Exchange plans, emitting priced and edited claim lines.",
                         users="Payment integrity, Actuarial & Finance and claims operations teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "10-60 GB/day", "Nightly batch"),
                             stream=flow(["semi-structured"], "hundreds of claims/sec at peak", "Continuous (pre-pay edits)"))),
                    tile("Cotiviti Payment Integrity", "market", "Pre- and post-pay edits, DRG validation and recovery findings on paid claims.", "cotiviti",
                         cat="Payment Integrity Platform",
                         what="Applies pre- and post-pay edits, DRG validation and recovery findings on claims, emitting edit results and recovery findings.",
                         users="Fraud & Integrity, payment integrity and recovery teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "5-25 GB/day findings", "Daily edit + recovery cycle")))
                ]},
                {"box": "Clinical & UM", "ic": "people", "tiles": [
                    tile("Epic Payer Platform", "custlake", "Prior authorization, care management notes and member clinical summaries from provider connectivity.", "epic-payer",
                         cat="Payer Care Management Platform",
                         what="Carries prior authorization, care management notes and member clinical summaries from provider connectivity, emitting authorization and clinical-summary records.",
                         users="Care Management, utilization management and nurse care coordinators.",
                         data_out=data_out(
                             batch=flow(["structured", "unstructured"], "5-20 GB/day incl. notes", "Nightly batch"),
                             stream=flow(["semi-structured"], "tens of events/sec", "Continuous CDC"))),
                    tile("NaviNet Prior Auth", "api", "Authorization requests, determinations and appeal status exchanged with provider portals.", "navinet",
                         cat="Prior Authorization Exchange",
                         what="Exchanges authorization requests, determinations and appeal status with provider portals, emitting auth request and determination events.",
                         users="Utilization management, Care Management and provider-relations teams.",
                         data_out=data_out(
                             stream=flow(["semi-structured"], "tens of requests/sec at peak", "Continuous (portal / API)"))),
                    tile("Optum (Change Healthcare)", "stream", "Lab, imaging and ADT feeds supplementing claims with clinical context.", "change-healthcare",
                         cat="Clinical Connectivity Network",
                         what="Supplies lab, imaging and ADT feeds that supplement claims with clinical context for risk and care use cases.",
                         users="Care Management, risk-adjustment and clinical-data teams.",
                         data_out=data_out(
                             stream=flow(["semi-structured"], "hundreds of HL7 msgs/sec at peak", "Continuous HL7/clinical feed")))
                ]},
                {"box": "Pharmacy & Network", "ic": "product", "tiles": [
                    tile("CVS Caremark PBM", "market", "Pharmacy claims, formulary access edits, specialty dispensing and rebate accruals from the pharmacy benefit manager.", ["caremark", "mmit", "accredo"],
                         cat="Pharmacy Benefit Manager (PBM)",
                         what="Adjudicates pharmacy claims and carries formulary access edits, specialty dispensing and rebate accruals from the pharmacy benefit manager.",
                         users="Actuarial & Finance, pharmacy integrity and clinical-pharmacy teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "10-40 GB/day", "Daily pharmacy claims cycle"))),
                    tile("Symplr Provider Data", "people", "Credentialing, roster and directory accuracy for network adequacy.", "symplr",
                         cat="Provider Data Management System",
                         what="Manages credentialing, roster and directory accuracy for network adequacy, emitting provider, roster and credential records.",
                         users="Provider Relations, provider-data management and compliance teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "1-5 GB/day", "Daily roster refresh"))),
                    tile("CMS Encounter Data", "gavel", "Risk adjustment diagnoses and encounter records submitted for Medicare Advantage.", "cms-encounter",
                         cat="Risk Adjustment Submission System",
                         what="Holds risk-adjustment diagnoses and encounter records submitted for Medicare Advantage, emitting encounter and response files.",
                         users="Actuarial & Finance, risk-adjustment and regulatory teams.",
                         data_out=data_out(
                             batch=flow(["structured", "semi-structured"], "5-20 GB/submission", "Submission windows + response files")))
                ]},
                fed_group(
                    "TPA Sub-claims",
                    "Third-party administrator claim detail left at TPAs and queried in place under Unity Catalog.",
                    cat="Third-Party Administrator System",
                    what="Third-party-administrator claim detail kept at TPAs and queried in place through federation instead of being copied into the payer estate.",
                    users="Actuarial & Finance, claims operations and Fraud & Integrity teams.",
                    data_out=data_out(
                        batch=flow(["structured"], "GB-scale TPA marts", "Queried on demand (federated)")),
                ),
            ],
            "ing": ing_rail([
                tile("X12 EDI Clearinghouse", "stream", "837 institutional and professional claims normalised on ingest through the multi-payer network with companion guide validation.", ["x12-edi", "avality"],
                     cat="EDI Claims Clearinghouse",
                     what="Normalises 837 institutional and professional claims on ingest through the multi-payer network with companion-guide validation.",
                     users="Data Engineers, EDI and claims-operations teams.",
                     data_out=data_out(
                         stream=flow(["semi-structured"], "hundreds of 837s/sec at peak", "Continuous EDI feed"))),
                tile("NCQA HEDIS Measures", "gavel", "Measure specification updates consumed inbound before HEDIS season.", "ncqa-hedis",
                     cat="Quality Measure Specification",
                     what="Inbound HEDIS measure specification updates that define the quality measures the plan computes each season.",
                     users="Care Management, quality and Actuarial & Finance teams.",
                     data_out=data_out(
                         batch=flow(["structured", "semi-structured"], "MBs (specifications)", "Annual / on release"))),
                tile("CMS Risk Model Files", "chart", "HCC coefficients and model software updates for risk adjustment scoring.",
                     cat="Risk Adjustment Model Reference",
                     what="HCC coefficients and risk-model software updates from CMS used to score risk adjustment for Medicare Advantage.",
                     users="Actuarial & Finance, risk-adjustment and data-science teams.",
                     data_out=data_out(
                         batch=flow(["structured"], "MBs-GBs (coefficients)", "Annual model release")))
            ]),
            "ppl": ppl2([
                biz("CEO & CFO", "Genie One", "The CEO on membership growth and medical loss ratio; the CFO on risk-adjusted revenue, medical trend and reserve adequacy by line of business.",
                    [["Genie One", "Ask what medical trend was last month by line of business without waiting on actuarial."], ["AI/BI", "MLR, membership and quality on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"paid claim\" means one thing across admin systems."]],
                    sub=[
                        ["Chief Executive Officer", "membership growth, medical loss ratio and the margin that ultimately funds the plan."],
                        ["Chief Financial Officer", "risk-adjusted revenue, medical trend and reserve adequacy by line of business."],
                        ["VP Actuarial", "pricing discipline, IBNR reserves and whether this year's trend assumptions still hold."],
                    ],
                    ucs=["Medical Loss Ratio", "Risk Adjustment", "Member Retention", "Pharmacy Trend"]),
                biz("Actuarial & Finance", "AI/BI", "Pricing, reserving and risk-score reconciliation for Medicare and commercial blocks, chasing HCC completeness before the submission window closes.",
                    [["Risk Adjustment Workbench", "HCC gaps and encounter completeness before submission."], ["AI/BI", "MLR and trend on certified Metric Views the board reads."], ["Unity Catalog", "One definition of premium and claims across lines."]],
                    sub=[
                        ["Chief Actuary", "pricing, reserving and hitting the annual risk-score submission window cleanly."],
                        ["Risk Adjustment Lead", "HCC completeness and encounter accuracy before the CMS deadlines land."],
                        ["Financial Reporting", "medical loss ratio, medical trend and rebate accruals by line of business."],
                    ],
                    ucs=["Risk Adjustment", "Medical Loss Ratio", "Pharmacy Trend"]),
                biz("Care Management", "Model Serving", "Nurses and care coordinators on rising-risk members, open gaps in care and readmission prevention before an avoidable ED visit or admission.",
                    [["Care Manager Console", "Rising-risk members ranked before ED utilisation spikes."], ["Model Serving", "Risk models scored at enrollment and monthly refresh."], ["CustomerLake", "Member segments without copying clinical exports elsewhere."]],
                    sub=[
                        ["VP Care Management", "rising-risk members and avoidable admissions across the managed panel."],
                        ["Nurse Care Coordinators", "open gaps in care and which member to reach out to and call today."],
                        ["Utilization Management", "authorization turnaround and medical necessity without over-denying care."],
                    ],
                    ucs=["Care Management", "HEDIS Quality", "Prior Auth Optimisation"]),
                biz("Provider Relations", "AI/BI", "Contracting on network adequacy, value-based arrangement performance and out-of-network leakage when a provider dispute lands.",
                    [["Provider Scorecard", "Quality and cost metrics by TIN and contract."], ["AI/BI", "Network leakage and adequacy on governed definitions."], ["Genie One", "Ask which specialties drive out-of-network spend."]],
                    sub=[
                        ["VP Network", "network adequacy, contracting economics and out-of-network leakage."],
                        ["Value-Based Contracting", "shared-savings settlement and quality-bonus accuracy providers will trust."],
                        ["Provider Data Management", "directory accuracy and roster currency by TIN for compliance."],
                    ],
                    ucs=["Network Adequacy", "Value-Based Contracts", "HEDIS Quality"]),
                biz("Fraud & Integrity", "Lakehouse//RT", "SIU investigators on aberrant provider billing patterns, duplicate claims and pharmacy fraud, flagged pre-pay before dollars go out the door.",
                    [["FWA Command Centre", "Anomaly clusters flagged before payment releases."], ["Lakehouse//RT", "Pre-pay edits scored at adjudication latency."], ["AI/BI", "Recovery and avoidance on certified Metric Views."]],
                    sub=[
                        ["SIU Director", "aberrant billing patterns and the case pipeline from lead to recovery."],
                        ["Payment Integrity", "pre-pay edit yield and how much post-pay recovery is actually collectable."],
                        ["Pharmacy Integrity", "specialty and controlled-substance dispensing anomalies at the PBM."],
                    ],
                    ucs=["Fraud Waste & Abuse", "Pharmacy Trend"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the EDI claims, enrollment and clinical feeds; own the Bronze to Silver path and the pager when an 837 load breaks.",
                    [["Lakeflow Connect", "Managed connectors for core admin, clinical and pharmacy sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on claims and enrollment feeds."], ["Lakewatch", "Freshness on the tables actuarial and care teams read every morning."]],
                    sub=[
                        ["EDI & Claims Engineering", "the 837 and 835 loads and the pager when an EDI feed breaks overnight."],
                        ["Enrollment & Eligibility", "834 enrollment files and member-month reconciliation across lines."],
                        ["Clinical Data Integration", "lab, ADT and prior-auth feeds conformed into the Silver layer."],
                    ],
                    ucs=["Risk Adjustment", "HEDIS Quality", "Fraud Waste & Abuse"]),
                biz("Data Scientists", "MLflow", "Risk-adjustment, rising-risk and fraud-waste-and-abuse models, and whether they still hold across a plan year.",
                    [["Feature Store", "Member features defined once for training and serving."], ["MLflow", "Every risk model run tracked for audit and reproduction."], ["Model Serving", "Risk and FWA models scored at enrollment and adjudication."]],
                    sub=[
                        ["Risk Adjustment Modelling", "HCC suspecting and RAF-score gap models against clinical text."],
                        ["Clinical Risk Science", "rising-risk and readmission prediction across the whole plan year."],
                        ["FWA Modelling", "anomaly and provider-network models scored pre-pay at adjudication."],
                    ],
                    ucs=["Risk Adjustment", "Care Management", "Fraud Waste & Abuse"]),
                biz("App Developers", "Apps", "Ship the care manager, risk-adjustment and FWA applications the plan works in, hosted next to governed data.",
                    [["Apps", "Care and integrity screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for care-plan and claims-edit writes."], ["Agent Bricks", "Agents that draft an outreach or edit override against governed tools."]],
                    sub=[
                        ["Care & UM Apps", "the care manager and prior-auth review screens nurses work in daily."],
                        ["Integrity Apps", "the FWA command centre and the claims-edit override workflow."],
                        ["Member & Provider Apps", "member care-gap nudges and the provider scorecard experience."],
                    ],
                    ucs=["Care Management", "Prior Auth Optimisation", "Fraud Waste & Abuse"]),
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
            ], genie_spaces=[
                genie("Medical Cost & Trend", "Ask about medical loss ratio, trend drivers and membership by line of business.",
                      feeds=["Facets Core Admin", "HealthEdge Source", "MLR, risk, quality", "Conformed member, claim"],
                      teams=["CEO & CFO", "Actuarial & Finance", "Financial Reporting"],
                      questions=[
                          "What is our medical loss ratio by line of business this month?",
                          "Which categories are driving medical trend versus last year?",
                          "How has membership grown by market and product?",
                          "What is risk-adjusted revenue per member month by line?",
                          "Where are IBNR reserves moving against booked estimates?"]),
                genie("Risk Adjustment", "Explore HCC completeness, suspected gaps and encounter accuracy before submission.",
                      feeds=["CMS Encounter Data", "Optum (Change Healthcare)", "CMS Risk Model Files", "Conformed member, claim"],
                      teams=["Actuarial & Finance", "Risk Adjustment Lead", "Chief Actuary"],
                      questions=[
                          "Which members have suspected HCCs not yet captured this year?",
                          "What is our encounter data completeness before the submission window?",
                          "How does average RAF score compare to last plan year?",
                          "Which providers have the largest documentation gaps?",
                          "Where would recapture most improve risk-adjusted revenue?"]),
                genie("Care & Quality", "Answer rising-risk, gap-in-care and prior-auth questions in plain language.",
                      feeds=["Epic Payer Platform", "NaviNet Prior Auth", "NCQA HEDIS Measures", "MLR, risk, quality"],
                      teams=["Care Management", "Nurse Care Coordinators", "Utilization Management"],
                      questions=[
                          "Which members are rising-risk and should be outreached this week?",
                          "What is our HEDIS gap-closure rate by measure before season?",
                          "Where is prior-auth turnaround exceeding target?",
                          "Which members have open gaps in care across multiple measures?",
                          "What is the readmission rate for the managed panel?"]),
                genie("Payment Integrity & FWA", "Ask about edit yield, recoveries and pharmacy and provider anomalies.",
                      feeds=["Cotiviti Payment Integrity", "CVS Caremark PBM", "X12 EDI Clearinghouse", "Conformed member, claim"],
                      teams=["Fraud & Integrity", "Payment Integrity", "Pharmacy Integrity"],
                      questions=[
                          "Which providers show the most aberrant billing patterns this quarter?",
                          "What is pre-pay edit yield versus post-pay recovery by category?",
                          "Where are duplicate claims concentrated across the book?",
                          "Which pharmacies show specialty or controlled-substance anomalies?",
                          "How much FWA savings did we realise this month?"]),
            ], dashboards=[
                dashboard("MLR & Medical Trend", "Medical loss ratio, trend and risk-adjusted revenue on certified finance Metric Views.",
                          kpis=["Medical loss ratio", "Medical trend", "Risk-adjusted revenue", "IBNR reserves", "Membership"],
                          teams=["CEO & CFO", "Actuarial & Finance", "Financial Reporting"]),
                dashboard("Risk Adjustment & RAF", "RAF score, HCC recapture and encounter completeness before submission windows.",
                          kpis=["RAF score", "HCC recapture rate", "Encounter completeness", "Suspected gaps", "Submission accuracy"],
                          teams=["Actuarial & Finance", "Risk Adjustment Lead", "Chief Actuary"]),
                dashboard("Quality & Care", "HEDIS, Stars, gap closure and prior-auth turnaround across the managed panel.",
                          kpis=["HEDIS measure rate", "Star rating", "Gap-closure rate", "Readmission rate", "PA turnaround"],
                          teams=["Care Management", "Nurse Care Coordinators", "Utilization Management"]),
                dashboard("Payment Integrity & FWA", "Edit yield, recoveries and FWA savings across medical and pharmacy claims.",
                          kpis=["Pre-pay edit yield", "Post-pay recovery", "FWA savings", "Duplicate-claim rate", "Pharmacy anomaly rate"],
                          teams=["Fraud & Integrity", "Payment Integrity", "Pharmacy Integrity"]),
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
                uc("Risk Adjustment", "Medicare", "chart", "HCC capture and encounter data completeness maximised before annual risk model runs.",
                    problem="HCC-coded conditions sit unread across claims, encounters and clinical notes, so risk scores are submitted incomplete and the plan is paid below the true acuity of its members.",
                    who="Actuarial & Finance",
                    how="Claims and encounter feeds land through Lakeflow on Delta Lake; NLP and HCC models score suspected gaps in Model Serving, surfaced in the Risk Adjustment Workbench before submission.",
                    comps=["Risk Adjustment Workbench", "CMS Encounter Data", "Model Serving", "MLflow", "Delta Lake", "Unity Catalog"],
                    stories=[
                        ["Empowering smarter decisions to transform healthcare outcomes", "https://www.databricks.com/customers/abacus-insights"],
                    ]),
                uc("Medical Loss Ratio", "Finance", "market", "MLR tracked by line and market with trend drivers actuaries can explain to regulators.",
                    problem="Medical trend surfaces only after the quarter closes, stitched from actuarial spreadsheets, so finance sees a rising loss ratio too late to act on the drivers behind it.",
                    who="CEO & CFO",
                    how="Paid claims, premium and membership conform on Delta Lake and serve as certified Metric Views in AI/BI, with Genie One letting finance interrogate trend by line of business.",
                    comps=["AI/BI", "Genie One", "Unity Catalog", "Delta Lake", "Facets Core Admin"],
                    stories=[
                        ["Quality care is the mission. Finance protects the margin.", "https://www.databricks.com/blog/quality-care-mission-finance-protects-margin"],
                    ]),
                uc("HEDIS Quality", "Stars", "gavel", "Measure gaps closed through outreach before submission season, not after chart chase.",
                    problem="Care gaps are found in the retrospective chart chase after the measurement year, so outreach happens too late to close them and the plan's Stars rating and bonus slip.",
                    who="Care Management",
                    how="Claims, lab and clinical feeds conform on Delta Lake and run against certified HEDIS measures, so open gaps rank for outreach in AI/BI and the Care Manager Console before season.",
                    comps=["Care Manager Console", "NCQA HEDIS Measures", "AI/BI", "Delta Lake", "Unity Catalog"],
                    stories=[
                        ["Quality care is the mission. Finance protects the margin.", "https://www.databricks.com/blog/quality-care-mission-finance-protects-margin"],
                    ]),
                uc("Fraud Waste & Abuse", "Integrity", "gauge", "Billing patterns and pharmacy anomalies detected pre-pay and recovered post-pay.",
                    problem="Aberrant billing, duplicate claims and pharmacy schemes hide in millions of lines, and rule-only edits catch them after payment when recovery is slow, partial and often uncollectable.",
                    who="Fraud & Integrity",
                    how="Adjudicating claims stream into Lakehouse//RT where anomaly models tracked in MLflow score them pre-pay in Model Serving, clustering suspect providers in the FWA Command Centre.",
                    comps=["FWA Command Centre", "Cotiviti Payment Integrity", "Lakehouse//RT", "Model Serving", "MLflow"],
                    stories=[
                        ["Orizon commits to helping the healthcare system prevent fraud", "https://www.databricks.com/customers/orizon"],
                    ]),
                uc("Care Management", "Clinical", "people", "High-cost members identified and engaged before preventable admissions.",
                    problem="Rising-risk members are spotted only after an avoidable ED visit or admission, because claims, pharmacy and clinical signals live apart and nurses cannot see who is deteriorating now.",
                    who="Care Management",
                    how="Member features from claims and clinical feeds are built in Feature Store and scored monthly in Model Serving, ranking rising-risk members in the Care Manager Console for outreach.",
                    comps=["Care Manager Console", "Feature Store", "Model Serving", "Epic Payer Platform", "CustomerLake"],
                    stories=[
                        ["SCAN Health Plan improves member care with Databricks", "https://www.databricks.com/customers/scan-health"],
                    ]),
                uc("Network Adequacy", "Provider", "globe", "Directory accuracy and time-and-distance standards monitored for regulatory compliance.",
                    problem="Provider directories drift out of date across systems, so time-and-distance standards are proven with stale rosters and the plan risks a regulatory adequacy finding.",
                    who="Provider Relations",
                    how="Credentialing and roster feeds conform under Unity Catalog on Delta Lake and are measured against adequacy standards in AI/BI, with directory fixes written back after review.",
                    comps=["Symplr Provider Data", "Unity Catalog", "AI/BI", "Delta Lake", "Provider Scorecard"]),
                uc("Prior Auth Optimisation", "Utilisation", "api", "Authorization turnaround and denial overturn rates improved without loosening medical necessity.",
                    problem="Authorization requests pile up in manual queues, so turnaround drags, providers are abraded, and inconsistent evidence handling drives avoidable denials that resurface as costly appeals.",
                    who="Care Management",
                    how="Authorization and clinical documents land through connectors, and AI Functions rank approval likelihood and missing evidence in Model Serving, drafting determinations for nurse review.",
                    comps=["NaviNet Prior Auth", "AI Functions", "Model Serving", "Lakebase", "Unity Catalog"],
                    stories=[
                        ["Modernizing Prior Authorization with Advanced Analytics", "https://www.databricks.com/blog/modernizing-prior-authorization-advanced-analytics"],
                    ]),
                uc("Pharmacy Trend", "PBM", "product", "Specialty spend, formulary adherence and rebate performance reconciled to medical trend.",
                    problem="Pharmacy claims, rebates and specialty spend sit with the PBM on a lag, so the plan cannot reconcile drug trend to medical trend or catch rebate leakage until the accrual is booked.",
                    who="Actuarial & Finance",
                    how="PBM and medical claims conform on Delta Lake under Unity Catalog and reconcile as certified Metric Views in AI/BI, so specialty trend and rebate performance read against one set.",
                    comps=["CVS Caremark PBM", "AI/BI", "Unity Catalog", "Delta Lake", "Genie One"],
                    stories=[
                        ["How Caresource modernized its data architecture for better healthcare", "https://www.databricks.com/blog/2022/04/07/how-caresource-modernized-its-data-architecture-to-provide-better-healthcare-to-members.html"],
                    ]),
                uc("Member Retention", "Growth", "custlake", "Disenrollment risk scored from service complaints, claims gaps and digital engagement.",
                    problem="Members disenroll after a bad service experience or unmet care need, but the complaint, claims-gap and engagement signals that predict it are scattered and seen only after they leave.",
                    who="CEO & CFO",
                    how="Service, claims and engagement features are built in Feature Store and scored in Model Serving to flag disenrollment risk, driving retention outreach from governed member segments.",
                    comps=["Feature Store", "Model Serving", "AI/BI", "CustomerLake", "MLflow"],
                    stories=[
                        ["SCAN Health Plan improves member care with Databricks", "https://www.databricks.com/customers/scan-health"],
                    ]),
                uc("Value-Based Contracts", "Provider", "partner", "Shared savings and quality bonuses calculated from governed claims and clinical data.",
                    problem="Shared-savings and quality bonuses settle months late from claims and clinical data that never line up, so providers dispute the numbers and neither side trusts the scorecard.",
                    who="Provider Relations",
                    how="Claims, quality and attribution data are conformed as governed Data Products under Unity Catalog and shared with providers over Open Sharing, surfaced in the Provider Scorecard.",
                    comps=["Provider Scorecard", "Data Products", "Unity Catalog", "Open Sharing", "Delta Lake"],
                    stories=[
                        ["Empowering smarter decisions to transform healthcare outcomes", "https://www.databricks.com/customers/abacus-insights"],
                    ]),
            ],
        ),
        "sources": {
            "facets": {"t": "Oracle Health Facets", "u": "https://www.oracle.com/health/"},
            "healthedge": {"t": "HealthEdge Source", "u": "https://healthedge.com/solutions/source"},
            "cotiviti": {"t": "Cotiviti payment integrity", "u": "https://www.cotiviti.com/solutions/payment-accuracy"},
            "epic-payer": {"t": "Epic Payer Platform", "u": "https://www.epic.com/software/payer-platform"},
            "navinet": {"t": "NaviNet prior authorization", "u": "https://www.navinet.net/"},
            "change-healthcare": {"t": "Optum (Change Healthcare) clinical connectivity", "u": "https://business.optum.com/en/changehealthcare.html"},
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
