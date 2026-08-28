import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    app, biz, cons_rail, dashboard, data_out, fed_group, flow, genie, ing_rail,
    medallion, tile, top_band, uc,
)


def ppl2(business_tiles, tech_tiles):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_PUBLIC_SECTOR = {
    "public_sector": {
        "label": "Public Sector",
        "blurb": "Civilian government across federal, state and local agencies: benefits and eligibility, tax and revenue, permitting and licensing, case management, and constituent services.",
        "medallion": medallion(
            "Raw agency system feeds",
            "Eligibility determinations, tax filings, permit applications, case notes and GIS parcels landed exactly as received from the systems of record, so a determination or a filing can always be replayed as it stood for audit and appeal.",
            "Conformed constituent, case, parcel",
            "Constituents, cases, parcels and programs resolved into single conformed entities across the eligibility, tax, permitting and case estates, with identifiers reconciled and duplicate records matched across agencies under one governance model.",
            "Outcomes, integrity, service metrics",
            "Contracted products the program and finance teams run on: improper-payment rate and program outcomes by cohort, permit cycle time, tax compliance yield, and constituent service level by channel.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Benefits & Eligibility",
                    "ic": "erp",
                    "tiles": [
                        tile(
                            "Merative Cúram SPM",
                            "erp",
                            "Social program management: the system of record for eligibility rules, determinations and case management across benefits programs.",
                            "curam",
                            cat="Social Program Management / Eligibility System",
                            what="Holds the eligibility rules, determinations and benefits case records, so a determination can be replayed exactly as it stood for appeal and audit.",
                            users="Caseworkers, eligibility determination staff and program integrity teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "20-80 GB/day", "Nightly batch + hourly deltas"),
                                stream=flow(["semi-structured"], "tens of case events/sec", "Continuous CDC")),
                        ),
                        tile(
                            "Gainwell MMIS",
                            "db",
                            "Medicaid Management Information System: claims, provider and member data for state health and human-services programs.",
                            "gainwell",
                            cat="Medicaid Management Information System (MMIS)",
                            what="Processes Medicaid claims and holds provider and member records for state health and human-services programs.",
                            users="Medicaid program staff, provider enrollment and program integrity teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "50-200 GB/day claims + eligibility", "Nightly batch + weekly cycles")),
                        ),
                        tile(
                            "Conduent Benefits",
                            "people",
                            "Government benefits administration and EBT processing for food, cash and childcare assistance programs.",
                            "conduent",
                            cat="Benefits Administration & EBT Platform",
                            what="Administers benefits issuance and processes EBT card transactions for food, cash and childcare assistance programs.",
                            users="Benefits operations, EBT program managers and payment integrity teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-30 GB/day", "Nightly batch"),
                                stream=flow(["semi-structured"], "hundreds of EBT txns/sec at peak", "Continuous")),
                        ),
                    ],
                },
                {
                    "box": "Tax & Revenue",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "FAST GenTax",
                            "market",
                            "Integrated tax administration used by many state revenue departments: registration, returns, payments and audit case management.",
                            "fast",
                            cat="Integrated Tax Administration System",
                            what="Runs registration, returns, payments and audit case management as the system of record for a revenue department.",
                            users="Revenue and tax administration, audit selection and collections teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "10-60 GB/day", "Nightly batch + filing-season peaks")),
                        ),
                        tile(
                            "Tyler Property Tax",
                            "sheet",
                            "Computer-assisted mass appraisal and property tax billing: parcels, assessments, levies and collections.",
                            "tyler-ptax",
                            cat="Property Assessment & Tax (CAMA) System",
                            what="Values parcels through computer-assisted mass appraisal and bills, levies and collects property tax.",
                            users="Assessors, property tax billing and collections teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-20 GB/day parcels + assessments", "Nightly batch + assessment cycles")),
                        ),
                        tile(
                            "RSI Revenue Premier",
                            "market",
                            "Revenue management and discovery: compliance case selection, collections and audit workflows for tax agencies.",
                            "rsi",
                            cat="Revenue Management & Discovery System",
                            what="Selects compliance cases, drives collections and runs audit workflows to close the tax gap for a revenue agency.",
                            users="Compliance, collections and audit teams in revenue departments.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "2-10 GB/day cases + scores", "Nightly batch")),
                        ),
                    ],
                },
                {
                    "box": "Permitting & Licensing",
                    "ic": "gavel",
                    "tiles": [
                        tile(
                            "Accela Civic Platform",
                            "gavel",
                            "Land management, permitting, licensing and code enforcement: the workflow of record for applications and inspections.",
                            "accela",
                            cat="Permitting & Licensing System",
                            what="Runs land management, permitting, licensing and code enforcement as the workflow of record for applications and inspections.",
                            users="Permit technicians, plan reviewers, inspectors and code enforcement teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "3-15 GB/day", "Hourly / nightly sync"),
                                stream=flow(["semi-structured"], "tens of application events/sec", "Continuous")),
                        ),
                        tile(
                            "Tyler EnerGov",
                            "gavel",
                            "Enterprise permitting and licensing for community development, plan review and business licensing.",
                            "tyler-energov",
                            cat="Permitting & Licensing System",
                            what="Handles community-development permitting, plan review and business licensing across the application lifecycle.",
                            users="Community development, plan review and business licensing teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "3-12 GB/day", "Nightly batch + hourly deltas")),
                        ),
                        tile(
                            "OpenGov Permitting",
                            "appbuilder",
                            "Cloud permitting and licensing with online applications, plan review and citizen self-service.",
                            "opengov",
                            cat="Cloud Permitting & Licensing System",
                            what="Cloud permitting and licensing with online applications, plan review and citizen self-service portals.",
                            users="Community development staff, applicants and citizen self-service teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-6 GB/day", "Hourly / nightly sync"),
                                stream=flow(["semi-structured"], "tens of portal events/sec", "Continuous")),
                        ),
                    ],
                },
                {
                    "box": "Case & Constituent",
                    "ic": "crm",
                    "tiles": [
                        tile(
                            "Salesforce Pub Sector",
                            "crm",
                            "Public Sector Solutions: constituent case management, benefits intake and licensing on the government CRM.",
                            "sf-ps",
                            cat="Government CRM / Case Management",
                            what="Government CRM holding constituent case management, benefits intake and licensing interactions across channels.",
                            users="Caseworkers, contact centre and constituent services teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-5 GB/day", "Hourly / nightly sync"),
                                stream=flow(["semi-structured"], "tens of case events/sec", "Continuous CDC")),
                        ),
                        tile(
                            "ServiceNow Gov",
                            "apps",
                            "Digital government services and workflow: request intake, routing and resolution across agency processes.",
                            "servicenow",
                            cat="Digital Service Management / Workflow",
                            what="Runs digital government service workflows: request intake, routing and resolution across agency processes.",
                            users="Service desk, business process owners and IT operations teams.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "1-4 GB/day", "Hourly sync"),
                                stream=flow(["semi-structured"], "tens of workflow events/sec", "Continuous")),
                        ),
                        tile(
                            "SeeClickFix 311",
                            "chat",
                            "Constituent 311 request reporting and non-emergency service tracking across the city.",
                            "seeclickfix",
                            cat="311 / Constituent Request System",
                            what="Captures 311 non-emergency service requests from residents and tracks them to resolution across city departments.",
                            users="311 contact centre, public works and constituent services teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "hundreds of requests/hour", "Continuous (API / webhook)")),
                        ),
                    ],
                },
                {
                    "box": "GIS, HR & Grants",
                    "ic": "globe",
                    "tiles": [
                        tile(
                            "Esri ArcGIS",
                            "globe",
                            "The GIS of record: parcels, addresses, service geographies and the spatial layers behind siting and response.",
                            "arcgis",
                            cat="Geographic Information System (GIS)",
                            what="System of record for parcels, addresses and service geographies, and the spatial layers behind siting, equity and response.",
                            users="GIS analysts, planning and program teams.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "GB-scale spatial layers", "Nightly / on-change refresh")),
                        ),
                        tile(
                            "Workday HCM",
                            "people",
                            "Human capital and payroll for the government workforce: positions, hiring, time and personnel records.",
                            "workday",
                            cat="HCM / Payroll Suite",
                            what="Manages positions, hiring, time and payroll for the government workforce as the personnel system of record.",
                            users="Human resources, payroll and workforce planning teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-5 GB/day", "Nightly batch + payroll cycles")),
                        ),
                        tile(
                            "AmpliFund Grants",
                            "docs",
                            "Grants management: applications, awards, subrecipient monitoring and compliance reporting.",
                            "amplifund",
                            cat="Grants Management System",
                            what="Manages grant applications, awards, subrecipient monitoring and compliance reporting across the award lifecycle.",
                            users="Grants management, finance and compliance teams.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "0.5-3 GB/day", "Daily + reporting cycles")),
                        ),
                    ],
                },
                fed_group(
                    "State Data Warehouse",
                    "Legacy agency data marts and mainframe extracts left where they are and queried in place under Unity Catalog, which avoids a second copy of records still under retention.",
                    cat="Legacy Data Warehouse / Marts",
                    what="Historical agency marts and mainframe extracts kept in the incumbent warehouse and queried in place through federation instead of being copied.",
                    users="Program, finance and reporting analysts across agencies.",
                    data_out=data_out(
                        batch=flow(["structured"], "TB-scale historical marts", "Queried on demand (federated)")),
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "Socrata Open Data",
                        "globe",
                        "Open-data platform APIs carrying public datasets and portal content, ingested for reconciliation against the governed source.",
                        "socrata",
                        cat="Open Data Platform",
                        what="Serves public datasets and portal content over APIs, ingested to reconcile the published portal against the governed source.",
                        users="Open data, transparency and analytics teams.",
                        data_out=data_out(
                            batch=flow(["structured", "semi-structured"], "GBs across datasets", "Daily + on-demand API"),
                            stream=flow(["semi-structured"], "API calls on demand", "Continuous (API)")),
                    ),
                    tile(
                        "Census Bureau APIs",
                        "api",
                        "Demographic, economic and geographic reference data from the U.S. Census Bureau, joined for benchmarking and equity analysis.",
                        "census",
                        cat="Government Reference Data (Demographics)",
                        what="Supplies demographic, economic and geographic reference data joined for benchmarking, targeting and equity analysis.",
                        users="Policy analysts, equity and program planning teams.",
                        data_out=data_out(
                            batch=flow(["structured"], "GBs reference tables", "Periodic + on-demand API")),
                    ),
                    tile(
                        "Grants.gov / SAM.gov",
                        "gavel",
                        "Federal grant opportunity, award and entity registration feeds consumed for grants and subrecipient management.",
                        "grantsgov",
                        cat="Federal Grants & Entity Registry",
                        what="Carries federal grant opportunity, award and entity-registration feeds used for grants and subrecipient management.",
                        users="Grants management, compliance and subrecipient monitoring teams.",
                        data_out=data_out(
                            batch=flow(["structured", "semi-structured"], "0.2-2 GB/day", "Daily feed + on-demand")),
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Agency Leadership",
                        "Genie One",
                        "The agency director and CIO on mission outcomes and service levels; the chief financial officer on budget execution and cost per program; the performance office steering the agency on evidence rather than anecdote.",
                        [
                            ["Genie One", "Ask what a program delivered last quarter or where the budget is running hot without booking analyst time."],
                            ["AI/BI", "Mission outcomes, budget execution and service levels on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the glossary, so \"outcome\" and \"cost per case\" mean one thing across the agency."],
                        ],
                        sub=[
                            ["Agency Director & CIO", "mission outcomes, service levels and the modernisation agenda."],
                            ["Chief Financial Officer", "budget execution, cost per program and audit readiness."],
                            ["Performance Office", "the KPIs the agency defends to oversight and the public."],
                        ],
                        ucs=["Workforce Analytics", "Emergency Response", "Program Outcomes"],
                    ),
                    biz(
                        "Program Directors",
                        "AI/BI",
                        "The directors who run benefits, health and human-services programs: enrolment and eligibility, improper-payment exposure, and whether the program actually moves outcomes for the people it serves.",
                        [
                            ["AI/BI", "Enrolment, payment integrity and outcome cohorts on governed program data."],
                            ["Model Serving", "Improper-payment and eligibility-risk models scored before money leaves."],
                            ["Genie One", "Ask which caseload is growing or which cohort is falling behind without an analyst pull."],
                        ],
                        sub=[
                            ["Benefits & Eligibility", "enrolment, determinations and improper-payment exposure."],
                            ["Health & Human Services", "caseload, outcomes and social determinants of health."],
                            ["Program Integrity", "fraud, waste and abuse across the program estate."],
                        ],
                        ucs=["Improper Payments", "Program Outcomes", "Grants Management"],
                    ),
                    biz(
                        "Chief Data Officer",
                        "Unity Catalog",
                        "The office accountable for data governance, open-data publishing and cross-agency sharing: one catalogue, one set of access rules, and a public that can trust the numbers.",
                        [
                            ["Unity Catalog", "One governed catalogue and lineage across every agency domain."],
                            ["Open Sharing", "Cross-agency and public data shared live without copies or egress."],
                            ["AI/BI", "Published, certified products the portal and analysts read from the same source."],
                        ],
                        sub=[
                            ["Data Governance", "classification, lineage and access policy across agencies."],
                            ["Open Data & Transparency", "the public portal and the certified numbers behind it."],
                            ["Data Sharing", "secure cross-agency exchange without duplication."],
                        ],
                        ucs=["Open Data Platform", "Constituent 360", "Digital Services"],
                    ),
                    biz(
                        "Budget & Finance",
                        "AI/BI",
                        "The budget office and revenue teams on where money is raised and spent: budget execution against appropriation, grant compliance, and the tax and revenue that funds it all.",
                        [
                            ["AI/BI", "Budget execution, grant compliance and revenue yield on certified views."],
                            ["Genie One", "Ask which grants are near closeout or which returns look anomalous without a finance pull."],
                            ["Model Serving", "Audit-selection and revenue-risk models scored against filings."],
                        ],
                        sub=[
                            ["Budget Office", "execution against appropriation and cost per outcome."],
                            ["Revenue & Tax", "collections, compliance yield and audit selection."],
                            ["Grants & Compliance", "subrecipient monitoring, closeouts and single-audit readiness."],
                        ],
                        ucs=["Tax Compliance & Audit", "Grants Management", "Improper Payments"],
                    ),
                    biz(
                        "Constituent Services",
                        "Lakehouse//RT",
                        "The teams residents actually meet: 311 and contact centres, permitting and licensing counters, and the digital services meant to make all of it self-serve.",
                        [
                            ["Lakehouse//RT", "Live case, permit and 311 state at the latency a counter moves at."],
                            ["Apps", "Constituent-facing services next to governed data with no separate web tier."],
                            ["CustomerLake", "One resident profile stitched across case, benefits and 311 records."],
                        ],
                        sub=[
                            ["311 & Contact Centre", "request intake, routing and resolution time."],
                            ["Permitting & Licensing", "application throughput and cycle time."],
                            ["Digital Services", "self-service adoption and completion rates."],
                        ],
                        ucs=["Constituent 360", "Permit & Licensing", "Digital Services"],
                    ),
                ],
                [
                    biz(
                        "Gov Data Engineers",
                        "Lakeflow",
                        "Land the benefits, tax, permitting, case and GIS feeds from Cúram, GenTax, Accela and ArcGIS; own the Bronze to Silver path and the pager when an eligibility or payment table stalls.",
                        [
                            ["Lakeflow Connect", "Managed connectors for eligibility, tax, permitting and SaaS case systems."],
                            ["Lakeflow Designer", "Declarative pipelines with expectations on benefit and payment feeds."],
                            ["Lakewatch", "Freshness on the tables caseworkers and auditors read every morning."],
                        ],
                    ),
                    biz(
                        "GIS Analysts",
                        "Model Serving",
                        "Parcels, addresses and service geographies from Esri ArcGIS joined to program and permit data, and the spatial models behind siting, routing and disaster response.",
                        [
                            ["Model Serving", "Spatial risk and demand models scored in the operational path."],
                            ["Feature Store", "Parcel and geography features read identically in training and serving."],
                            ["AI Functions", "Geocoding and address matching run in SQL against governed data."],
                        ],
                    ),
                    biz(
                        "Policy Analysts",
                        "AI/BI",
                        "Program and policy analysts testing what works: linking service records to outcomes, sizing cohorts, and answering the question a legislator asked this morning.",
                        [
                            ["AI/BI", "Cohort and outcome analysis on certified, governed data."],
                            ["Genie", "Plain-language questions against linked program data without SQL."],
                            ["Document Intelligence", "Policy documents and case notes parsed into governed tables."],
                        ],
                    ),
                ],
            ),
            "cons": cons_rail(
                [
                    {
                        "box": "BI & Productivity",
                        "ic": "chart",
                        "from": "bi",
                        "tiles": [
                            tile(
                                "Tableau / Power BI",
                                "chart",
                                "Executive and program dashboards against serverless SQL with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for Unity Catalog-governed answers in the channel program teams already work in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Analyst notebooks, VS Code and JetBrains against governed program and case data.",
                            ),
                        ],
                    },
                    {
                        "box": "Constituent Channels",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "Open Data Portal",
                                "globe",
                                "Certified open data served to residents and journalists from governed Gold products.",
                                "socrata",
                            ),
                            tile(
                                "311 & Service Apps",
                                "apps",
                                "Self-service request and status apps built on Databricks Apps over Lakebase.",
                            ),
                            tile(
                                "Genie for Residents",
                                "genie",
                                "Plain-language answers about permits, benefits and services grounded in governed data.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "Case & Eligibility",
                                "db",
                                "Determinations and next actions written back into the case and eligibility systems constituents are served from.",
                                "curam",
                            ),
                            tile(
                                "Permit Status",
                                "stream",
                                "Cycle-time flags and re-sequencing written back to the permitting system before deadlines slip.",
                                "accela",
                            ),
                            tile(
                                "Do Not Pay Sync",
                                "gavel",
                                "Confirmed bad actors and payment holds synced to disbursement and Do Not Pay controls.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "Federal Reporting",
                                "gavel",
                                "Program, single-audit and improper-payment reporting produced from the same governed tables the agency runs on.",
                            ),
                            tile(
                                "Transparency Portals",
                                "share",
                                "Spending and performance transparency published from contracted Gold products.",
                            ),
                        ],
                    },
                    {
                        "box": "Published Products",
                        "ic": "product",
                        "tiles": [
                            tile(
                                "Data Products",
                                "product",
                                "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing.",
                            ),
                            tile(
                                "Sharing Recipients",
                                "share",
                                "Other agencies and researchers reading live tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ],
                genie_spaces=[
                    genie(
                        "Program Integrity",
                        "Ask about improper-payment exposure, eligibility risk and fraud signals across benefits programs in plain language.",
                        feeds=["Merative Cúram SPM", "Gainwell MMIS", "Conduent Benefits", "Outcomes, integrity, service metrics"],
                        teams=["Program Directors", "Budget & Finance", "Program Integrity"],
                        questions=[
                            "What is our improper-payment rate this quarter versus last, by program?",
                            "Which caseloads show the fastest growth in high-risk determinations?",
                            "How many payments are being held for review right now, and for which programs?",
                            "Which providers or cohorts drive the most flagged claims?",
                            "How has eligibility-risk exposure changed since last month and why?"]),
                    genie(
                        "Constituent 360",
                        "Answer whole-person questions across benefits, tax, permitting and 311 records for a resident.",
                        feeds=["Salesforce Pub Sector", "SeeClickFix 311", "Merative Cúram SPM", "Conformed constituent, case, parcel"],
                        teams=["Constituent Services", "Chief Data Officer", "311 & Contact Centre"],
                        questions=[
                            "What is the full history of this resident across benefits, permits and 311?",
                            "Which constituents have open cases across more than one agency?",
                            "What is average resolution time for 311 requests by category and neighbourhood?",
                            "Which residents are eligible for a benefit they have not enrolled in?",
                            "Where are service requests concentrating this month across the city?"]),
                    genie(
                        "Revenue & Tax",
                        "Explore filings, collections, audit selection and compliance yield across the revenue estate.",
                        feeds=["FAST GenTax", "RSI Revenue Premier", "Tyler Property Tax", "Outcomes, integrity, service metrics"],
                        teams=["Budget & Finance", "Revenue & Tax", "Agency Leadership"],
                        questions=[
                            "What is our tax compliance yield this cycle versus target?",
                            "Which returns look anomalous and should be selected for audit?",
                            "What is collections performance by tax type and region?",
                            "Which property assessments moved the most this cycle?",
                            "How much revenue is at risk in open compliance cases right now?"]),
                    genie(
                        "Permitting & Service",
                        "Ask about permit cycle time, backlogs and constituent service levels across channels.",
                        feeds=["Accela Civic Platform", "Tyler EnerGov", "OpenGov Permitting", "Outcomes, integrity, service metrics"],
                        teams=["Constituent Services", "Permitting & Licensing", "Digital Services"],
                        questions=[
                            "What is average permit cycle time by permit type and department?",
                            "Which applications are stalled between departments past their target date?",
                            "How does permit throughput compare this month versus last?",
                            "Where are the biggest bottlenecks in plan review right now?",
                            "What is self-service completion rate by channel?"]),
                ],
                dashboards=[
                    dashboard(
                        "Payment Integrity",
                        "Improper-payment rate, held payments and eligibility-risk exposure across benefits programs.",
                        kpis=["Improper-payment rate", "Payments held for review", "Eligibility-risk exposure", "Recovery rate", "Fraud loss avoided"],
                        teams=["Program Directors", "Budget & Finance", "Program Integrity"]),
                    dashboard(
                        "Program Outcomes",
                        "Program outcomes by cohort, cost per outcome and service level across the agency.",
                        kpis=["Outcome attainment", "Cost per outcome", "Cohort reach", "Service level", "Enrolment rate"],
                        teams=["Agency Leadership", "Program Directors", "Performance Office"]),
                    dashboard(
                        "Revenue & Compliance",
                        "Tax compliance yield, collections, audit selection and revenue at risk on certified views.",
                        kpis=["Compliance yield", "Collections rate", "Audit hit rate", "Revenue at risk", "Days to collect"],
                        teams=["Budget & Finance", "Revenue & Tax", "Agency Leadership"]),
                    dashboard(
                        "Permit & Service Delivery",
                        "Permit cycle time, backlog, 311 resolution and digital service adoption by channel.",
                        kpis=["Permit cycle time", "Application backlog", "311 resolution time", "Self-service adoption", "On-time rate"],
                        teams=["Constituent Services", "Permitting & Licensing", "Digital Services"]),
                ],
            ),
        },
        "top": top_band(
            [
                app(
                    "Improper Payment Radar",
                    "Payment integrity",
                    "gauge",
                    "The screen program integrity runs claims through: eligibility, identity and payment signals scored together so high-risk payments are held for review before disbursement, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Constituent 360 Hub",
                    "One resident view",
                    "custlake",
                    "One governed profile per resident stitched across case, benefits, tax and 311 records, so a caseworker sees the whole person instead of one agency's slice.",
                ),
                app(
                    "Permit Throughput",
                    "Cycle-time board",
                    "stream",
                    "Live permit and licence state against target dates, flagging the applications stalled between departments so reviews are re-sequenced before deadlines slip.",
                ),
                app(
                    "Program Outcome Studio",
                    "Evidence & cohorts",
                    "chart",
                    "Where policy analysts link service records to downstream outcomes and size cohorts on certified data, without a fresh data request for every question.",
                ),
            ],
            [
                uc(
                    "Improper Payments",
                    "Payment integrity",
                    "gauge",
                    "Scoring eligibility, identity and payment signals together so improper and fraudulent payments are prevented, not chased after the money is gone.",
                    problem="Benefits are optimised to pay quickly, so integrity checks run after the money is out the door and improper payments are chased through pay-and-chase rather than prevented.",
                    who="Program Directors",
                    how="Eligibility, claims and payment feeds land in Lakehouse//RT; entity resolution and risk models score each claim in Model Serving so high-risk payments are held before disbursement.",
                    comps=["Improper Payment Radar", "Lakehouse//RT", "Model Serving", "Merative Cúram SPM", "Unity Catalog"],
                    stories=[
                        ["Bringing real-time fraud prevention to government benefits", "https://www.databricks.com/blog/bringing-real-time-fraud-prevention-government-benefits"],
                        ["Operationalizing AI for public sector fraud prevention", "https://www.databricks.com/blog/operationalizing-ai-public-sector-fraud-prevention"],
                    ],
                ),
                uc(
                    "Constituent 360",
                    "Whole-person view",
                    "custlake",
                    "Resolving a resident's records across benefits, tax, permitting and 311 into one governed profile so caseworkers and services see the whole person.",
                    problem="A resident's records are scattered across benefits, tax, permitting and 311 systems, so no caseworker or service ever sees the whole person.",
                    who="Constituent Services",
                    how="Records from the case, benefits and 311 systems are conformed and resolved in CustomerLake, giving caseworkers one governed profile per constituent.",
                    comps=["Constituent 360 Hub", "CustomerLake", "Salesforce Pub Sector", "SeeClickFix 311", "Unity Catalog"],
                    stories=[
                        ["State of Washington builds data-driven government", "https://www.databricks.com/customers/state-of-washington"],
                        ["GovTech Singapore unlocks nationwide data insights", "https://www.databricks.com/customers/govtech"],
                    ],
                ),
                uc(
                    "Program Outcomes",
                    "Evidence & impact",
                    "chart",
                    "Linking service records to downstream results across agency silos so programs are judged on outcomes for residents, not activity counts.",
                    problem="Programs report activity, not outcomes, because linking service records to downstream results means crossing agency silos that rarely share data.",
                    who="Program Directors",
                    how="Cross-agency records are linked under Unity Catalog and shared via Open Sharing; outcome cohorts are built in AI/BI on certified Metric Views.",
                    comps=["Program Outcome Studio", "AI/BI", "Unity Catalog", "Open Sharing", "Genie One"],
                    stories=[
                        ["DC OCTO links education and workforce data for outcomes", "https://www.databricks.com/customers/dc-octo"],
                    ],
                ),
                uc(
                    "Tax Compliance & Audit",
                    "Revenue integrity",
                    "market",
                    "Targeting audit effort at the highest-risk returns with anomaly models rather than fixed rules, so underreporting and refund fraud are caught before refunds are paid.",
                    problem="Underreporting and refund fraud slip through fixed rules, and auditors work returns after refunds are already paid out.",
                    who="Budget & Finance",
                    how="Filing, payment and third-party data are conformed in the lakehouse; anomaly models score returns in Model Serving so audit effort targets the highest-risk cases.",
                    comps=["FAST GenTax", "Model Serving", "AI/BI", "MLflow", "Unity Catalog"],
                    stories=[
                        ["Operationalizing AI for public sector fraud prevention", "https://www.databricks.com/blog/operationalizing-ai-public-sector-fraud-prevention"],
                    ],
                ),
                uc(
                    "Permit & Licensing",
                    "Throughput",
                    "stream",
                    "Making the permit and licence backlog visible across departments so reviews are re-sequenced and cycle time falls before deadlines are missed.",
                    problem="Permit and licence applications stall between departments with no visibility into where the backlog sits or which reviews are late.",
                    who="Constituent Services",
                    how="Accela and EnerGov application events stream into Lakehouse//RT; cycle-time and bottleneck analytics surface in AI/BI so reviews are re-sequenced before deadlines slip.",
                    comps=["Permit Throughput", "Accela Civic Platform", "Tyler EnerGov", "Lakehouse//RT", "AI/BI"],
                    stories=[
                        ["Data governance and AI drive better living in Amsterdam", "https://www.databricks.com/customers/gemeente-amsterdam"],
                    ],
                ),
                uc(
                    "Open Data Platform",
                    "Transparency",
                    "globe",
                    "Publishing certified open data and answering the public from the governed source, so the portal never drifts from the numbers the agency runs on.",
                    problem="Publishing open data means hand-built extracts that go stale, and the public portal drifts from the governed source it was copied from.",
                    who="Chief Data Officer",
                    how="Curated Gold tables are published as data products and served to the portal and to residents through Genie and Public & Open Data, governed by Unity Catalog.",
                    comps=["Socrata Open Data", "Data Products", "Genie One", "Unity Catalog", "Open Sharing"],
                    stories=[
                        ["How World Bank Group uses Databricks to share knowledge", "https://www.databricks.com/blog/how-world-bank-group-uses-databricks-eradicate-poverty-through-shared-knowledge"],
                    ],
                ),
                uc(
                    "Workforce Analytics",
                    "Hiring & people",
                    "people",
                    "Making the hiring pipeline visible end to end so leadership sees where candidates stall and vacancies that put services at risk.",
                    problem="Hiring drags for months and leadership cannot see where in the pipeline candidates stall or which vacancies put services at risk.",
                    who="Agency Leadership",
                    how="Workday and applicant-tracking data are unified and analysed in AI/BI so hiring bottlenecks and vacancy risk are visible by department.",
                    comps=["Workday HCM", "AI/BI", "Genie One", "Unity Catalog"],
                    stories=[
                        ["LA County modernises hiring with Databricks", "https://www.databricks.com/customers/la-county"],
                    ],
                ),
                uc(
                    "Emergency Response",
                    "Live common picture",
                    "gauge",
                    "Building a live common operating picture from sensor, GIS and operational feeds so responders act on current ground truth rather than a hand-stitched view.",
                    problem="In a disaster the operational picture is stitched together by hand from feeds that arrive too late to act on.",
                    who="Agency Leadership",
                    how="Sensor, GIS and operational feeds stream into Lakehouse//RT and are mapped against Esri layers so responders act on a live common picture.",
                    comps=["Lakehouse//RT", "Esri ArcGIS", "Model Serving", "AI/BI", "Lakeflow"],
                    stories=[
                        ["U.S. Department of Transportation delivers real-time insight", "https://www.databricks.com/customers/us-department-of-transportation"],
                    ],
                ),
                uc(
                    "Grants Management",
                    "Awards & compliance",
                    "docs",
                    "Centralising grant, subrecipient and spend data so compliance reporting is automated and anomalies surface before closeout, not after.",
                    problem="Grant, subrecipient and spend data live in spreadsheets, so compliance reporting is slow and anomalies surface late in the award cycle.",
                    who="Budget & Finance",
                    how="Grant, finance and performance data are centralised in the lakehouse; AmpliFund and finance feeds are conformed for automated compliance reporting and anomaly alerts.",
                    comps=["AmpliFund Grants", "AI/BI", "Unity Catalog", "Lakeflow", "Genie One"],
                    stories=[
                        ["Data and AI solutions for federal government", "https://www.databricks.com/solutions/industries/federal-government"],
                    ],
                ),
                uc(
                    "Digital Services",
                    "Self-service delivery",
                    "apps",
                    "Building constituent-facing services on governed data so residents complete online what used to need a counter visit, with plain-language help.",
                    problem="Residents drop out of online services that are slow, fragmented and disconnected from the data behind them.",
                    who="Constituent Services",
                    how="Constituent-facing services are built as Databricks Apps over Lakebase next to governed data, with Genie answering resident questions in plain language.",
                    comps=["Constituent 360 Hub", "Apps", "Lakebase", "Genie One", "ServiceNow Gov"],
                    stories=[
                        ["GovTech Singapore improves nationwide services", "https://www.databricks.com/customers/govtech"],
                        ["Reinventing government with the Databricks platform", "https://www.databricks.com/blog/reinventing-government-databricks-data-intelligence-platform"],
                    ],
                ),
            ],
        ),
        "sources": {
            "curam": {"t": "Merative Cúram Social Program Management", "u": "https://www.merative.com/social-program-management"},
            "gainwell": {"t": "Gainwell Technologies (MMIS)", "u": "https://www.gainwelltechnologies.com/"},
            "conduent": {"t": "Conduent Government Solutions", "u": "https://www.conduent.com/government-solutions/"},
            "fast": {"t": "FAST Enterprises GenTax", "u": "https://www.fastenterprises.com/"},
            "tyler-ptax": {"t": "Tyler Technologies Property Tax", "u": "https://www.tylertech.com/products/property-tax"},
            "rsi": {"t": "Revenue Solutions, Inc.", "u": "https://www.revenuesolutionsinc.com/"},
            "accela": {"t": "Accela Civic Platform", "u": "https://www.accela.com/civic-platform/"},
            "tyler-energov": {"t": "Tyler Enterprise Permitting & Licensing (EnerGov)", "u": "https://www.tylertech.com/products/enterprise-permitting-licensing"},
            "opengov": {"t": "OpenGov Permitting & Licensing", "u": "https://opengov.com/products/permitting-and-licensing/"},
            "sf-ps": {"t": "Salesforce Public Sector Solutions", "u": "https://www.salesforce.com/solutions/industries/government/overview/"},
            "servicenow": {"t": "ServiceNow for Public Sector", "u": "https://www.servicenow.com/solutions/industry/public-sector.html"},
            "seeclickfix": {"t": "SeeClickFix 311", "u": "https://seeclickfix.com/"},
            "arcgis": {"t": "Esri ArcGIS", "u": "https://www.esri.com/en-us/arcgis/about-arcgis/overview"},
            "workday": {"t": "Workday for Government", "u": "https://www.workday.com/en-us/industries/government.html"},
            "amplifund": {"t": "AmpliFund Grants Management", "u": "https://www.amplifund.com/"},
            "socrata": {"t": "Tyler Data & Insights (Socrata)", "u": "https://www.tylertech.com/products/data-insights"},
            "census": {"t": "U.S. Census Bureau Developer APIs", "u": "https://www.census.gov/data/developers.html"},
            "grantsgov": {"t": "Grants.gov", "u": "https://www.grants.gov/"},
        },
    }
}
