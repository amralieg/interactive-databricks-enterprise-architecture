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


INDUSTRIES_BATCH_SOFTWARE_TECHNOLOGY = {
    "software_technology": {
        "label": "Software & Technology",
        "blurb": "B2B and SaaS software: product-led activation and conversion, usage-based billing and metering, customer health and churn, developer velocity, and cloud cost and margin.",
        "medallion": medallion(
            "Raw product and billing events",
            "Product telemetry from the CDP and behavioural stack, Stripe and Zuora billing and metering records, CRM opportunities, support tickets and Git and CI events, landed exactly as received so a usage spike or an invoice can always be replayed as it stood.",
            "Conformed account, user, subscription",
            "Accounts, users, subscriptions and product entities resolved into single conformed entities across the CRM, billing and telemetry estates, with anonymous device ids stitched to known users and free and paid workspaces reconciled to one customer hierarchy.",
            "NRR, activation, health, margin",
            "Contracted products the revenue and product teams run on: net revenue retention and churn by cohort, PLG activation and conversion funnels, customer health scores, usage-based revenue and metering accuracy, and cloud cost of goods and gross margin by product.",
        ),
        "rails": {
            "src": [
                {
                    "box": "CRM & Sales",
                    "ic": "crm",
                    "tiles": [
                        tile(
                            "Salesforce Sales Cloud",
                            "crm",
                            "The system of record for accounts, opportunities and the pipeline, and the source of the customer hierarchy every revenue metric rolls up to.",
                            "salesforce",
                            cat="CRM / Sales Force Automation",
                            what="System of record for accounts, opportunities and pipeline, and the customer hierarchy every revenue metric rolls up to.",
                            users="Sales, RevOps and Finance teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-5 GB/day", "Hourly / nightly sync"),
                                stream=flow(["semi-structured"], "tens of events/sec", "Continuous CDC")),
                        ),
                        tile(
                            "HubSpot CRM",
                            "custlake",
                            "Contacts, deals and marketing engagement for the self-serve and mid-market motion, joined to product signups.",
                            "hubspot",
                            cat="CRM / Marketing Automation",
                            what="Contacts, deals and marketing engagement for the self-serve and mid-market motion, joined to product signups.",
                            users="Marketing, self-serve sales and RevOps.",
                            data_out=data_out(
                                batch=flow(["structured"], "0.5-2 GB/day", "Hourly sync"),
                                stream=flow(["semi-structured"], "tens of events/sec", "Continuous (webhook)")),
                        ),
                        tile(
                            "Gong Revenue AI",
                            "dial",
                            "Conversation intelligence on sales and renewal calls, the signal for deal risk and competitive mentions.",
                            "gong",
                            cat="Conversation Intelligence",
                            what="Records and analyzes sales and renewal calls, surfacing deal risk and competitive mentions.",
                            users="Sales leadership, RevOps and Enablement.",
                            data_out=data_out(
                                batch=flow(["structured", "unstructured"], "1-4 GB/day (transcripts + metadata)", "Daily")),
                        ),
                        tile(
                            "Outreach Engagement",
                            "market",
                            "Sales sequences, activity and reply data feeding rep productivity and pipeline-generation analysis.",
                            "outreach",
                            cat="Sales Engagement Platform",
                            what="Sales sequences, activity and reply data feeding rep productivity and pipeline-generation analysis.",
                            users="Sales development, RevOps and Enablement.",
                            data_out=data_out(
                                batch=flow(["structured"], "0.5-2 GB/day", "Hourly")),
                        ),
                    ],
                },
                {
                    "box": "Billing & Metering",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "Stripe Billing",
                            "market",
                            "Subscriptions, invoices, usage records and payment events, the source of MRR, ARR and collected revenue.",
                            "stripe",
                            cat="Subscription Billing & Payments",
                            what="Subscriptions, invoices, usage records and payment events, the source of MRR, ARR and collected revenue.",
                            users="Finance, RevOps and billing teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-5 GB/day", "Daily billing runs"),
                                stream=flow(["semi-structured"], "100s of events/sec", "Continuous (webhook)")),
                        ),
                        tile(
                            "Zuora Billing",
                            "erp",
                            "Recurring and usage-based billing, rating and revenue schedules for the enterprise subscription estate.",
                            "zuora",
                            cat="Recurring / Usage-Based Billing",
                            what="Recurring and usage-based billing, rating and revenue schedules for the enterprise subscription estate.",
                            users="Finance, revenue accounting and RevOps.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-3 GB/day", "Nightly billing cycles")),
                        ),
                        tile(
                            "Chargebee",
                            "product",
                            "Subscription lifecycle, dunning and revenue operations for the self-serve and PLG billing motion.",
                            "chargebee",
                            cat="Subscription Management",
                            what="Subscription lifecycle, dunning and revenue operations for the self-serve and PLG billing motion.",
                            users="RevOps, finance and growth billing teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "0.2-1 GB/day", "Daily")),
                        ),
                        tile(
                            "m3ter Metering",
                            "gauge",
                            "Usage metering and rating that turns raw consumption events into billable, reconcilable line items.",
                            "m3ter",
                            cat="Usage Metering & Rating",
                            what="Meters and rates raw consumption events into billable, reconcilable line items for usage-based pricing.",
                            users="RevOps, billing engineering and finance.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs/day rated rollups", "Hourly"),
                                stream=flow(["semi-structured"], "10-50k usage events/sec", "Continuous")),
                        ),
                    ],
                },
                {
                    "box": "Product Telemetry",
                    "ic": "stream",
                    "tiles": [
                        tile(
                            "Segment CDP",
                            "custlake",
                            "The customer data platform routing product, web and server events into one schema of identified and anonymous activity.",
                            "segment",
                            cat="Customer Data Platform (CDP)",
                            what="Routes product, web and server events into one schema of identified and anonymous activity.",
                            users="Growth, product analytics and lifecycle marketing.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "10-50k events/sec at peak", "Continuous clickstream")),
                        ),
                        tile(
                            "Amplitude Analytics",
                            "chart",
                            "Product analytics events, funnels and feature adoption, the source of activation and engagement measurement.",
                            "amplitude",
                            cat="Product Analytics",
                            what="Product analytics events, funnels and feature adoption, the source of activation and engagement measurement.",
                            users="Product analytics and growth teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "5-20k events/sec at peak", "Continuous")),
                        ),
                        tile(
                            "Snowplow Behavioral",
                            "stream",
                            "First-party behavioural event pipeline with a governed schema, the raw stream behind product and growth models.",
                            "snowplow",
                            cat="Behavioral Event Pipeline",
                            what="First-party behavioural event pipeline with a governed schema, the raw stream behind product and growth models.",
                            users="Data engineering, growth and product data science.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "10-100k events/sec at peak", "Continuous")),
                        ),
                    ],
                },
                {
                    "box": "Dev & Delivery",
                    "ic": "code",
                    "tiles": [
                        tile(
                            "GitHub",
                            "code",
                            "Commits, pull requests and Actions runs, the source of developer velocity and deployment-frequency signals.",
                            "github",
                            cat="Source Control / CI",
                            what="Commits, pull requests and Actions runs, the source of developer velocity and deployment-frequency signals.",
                            users="Engineering, platform and developer-experience teams.",
                            data_out=data_out(
                                batch=flow(["semi-structured"], "0.2-1 GB/day", "Daily + webhook"),
                                stream=flow(["semi-structured"], "tens of events/sec", "Continuous (webhook)")),
                        ),
                        tile(
                            "GitLab",
                            "cicd",
                            "Repositories, pipelines and merge requests where the delivery motion runs on a single DevOps platform.",
                            "gitlab",
                            cat="DevOps Platform",
                            what="Repositories, pipelines and merge requests where the delivery motion runs on a single DevOps platform.",
                            users="Engineering and platform teams.",
                            data_out=data_out(
                                batch=flow(["semi-structured"], "0.2-1 GB/day", "Daily + webhook")),
                        ),
                        tile(
                            "Jira Software",
                            "sheet",
                            "Issues, sprints and cycle time, the planning system of record joined to delivery and incident data.",
                            "jira",
                            cat="Project / Issue Tracking",
                            what="Issues, sprints and cycle time, the planning system of record joined to delivery and incident data.",
                            users="Engineering, product and program management.",
                            data_out=data_out(
                                batch=flow(["structured"], "0.2-1 GB/day", "Hourly / nightly")),
                        ),
                        tile(
                            "PagerDuty",
                            "observ",
                            "Incidents, on-call and escalation events, the source of reliability and mean-time-to-resolve measurement.",
                            "pagerduty",
                            cat="Incident Management / On-Call",
                            what="Incidents, on-call and escalation events, the source of reliability and mean-time-to-resolve measurement.",
                            users="SRE, platform engineering and on-call teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "tens of events/sec", "Continuous (webhook)")),
                        ),
                    ],
                },
                {
                    "box": "Support & Back Office",
                    "ic": "chat",
                    "tiles": [
                        tile(
                            "Zendesk Support",
                            "chat",
                            "Support tickets, CSAT and macros, a leading signal for churn risk and the corpus behind support deflection.",
                            "zendesk",
                            cat="Customer Support / Ticketing",
                            what="Support tickets, CSAT and macros, a leading signal for churn risk and the corpus behind support deflection.",
                            users="Support, customer success and product teams.",
                            data_out=data_out(
                                batch=flow(["structured", "unstructured"], "0.5-2 GB/day", "Hourly"),
                                stream=flow(["semi-structured"], "tens of events/sec", "Continuous (webhook)")),
                        ),
                        tile(
                            "Intercom",
                            "dial",
                            "In-product messaging, conversations and resolution data across the onboarding and support journey.",
                            "intercom",
                            cat="In-Product Messaging / Support",
                            what="In-product messaging, conversations and resolution data across the onboarding and support journey.",
                            users="Support, growth and lifecycle teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "100s of events/sec", "Continuous")),
                        ),
                        tile(
                            "Workday HCM",
                            "people",
                            "Headcount, roles and cost centres, the reference for engineering capacity and cost-of-delivery analysis.",
                            "workday",
                            cat="Human Capital Management (HCM)",
                            what="Headcount, roles and cost centres, the reference for engineering capacity and cost-of-delivery analysis.",
                            users="Finance, People and engineering leadership.",
                            data_out=data_out(
                                batch=flow(["structured"], "0.1-0.5 GB/day", "Nightly")),
                        ),
                        tile(
                            "NetSuite ERP",
                            "erp",
                            "General ledger, revenue and expense, the finance system of record reconciled against billing and metering.",
                            "netsuite",
                            cat="ERP / Financials",
                            what="General ledger, revenue and expense, the finance system of record reconciled against billing and metering.",
                            users="Finance and accounting teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "0.5-2 GB/day", "Nightly")),
                        ),
                    ],
                },
                fed_group(
                    "Cloud Warehouse Marts",
                    "Existing cloud data warehouse finance and analytics marts left where they are and queried in place under Unity Catalog, which avoids a second copy of the reported numbers.",
                    cat="Cloud Data Warehouse",
                    what="Existing finance and analytics marts kept in the incumbent cloud warehouse and queried in place through federation rather than copied.",
                    users="Finance, RevOps and analytics engineers.",
                    data_out=data_out(
                        batch=flow(["structured"], "TB-scale historical marts", "Queried on demand (federated)")),
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "Kafka Event Streams",
                        "eventbus",
                        "Product and billing event topics on Kafka or managed streaming, carrying signup, feature-usage and invoice events, parsed on arrival and landed as structured events.",
                        "kafka",
                        cat="Event Streaming Platform",
                        what="Product and billing event topics carrying signup, feature-usage and invoice events, parsed on arrival.",
                        users="Streaming and platform data engineers.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "20-100k events/sec at peak", "Continuous")),
                    ),
                    tile(
                        "Product Webhooks",
                        "api",
                        "Stripe, GitHub and Zendesk webhooks delivering near-real-time billing, commit and ticket events. Managed ELT connectors and existing streaming topics carrying usage and telemetry land here too, drawn generically on the reference board.",
                        cat="Webhook / ELT Ingest",
                        what="Stripe, GitHub and Zendesk webhooks and managed ELT connectors delivering near-real-time billing, commit and ticket events.",
                        users="Integration and platform data engineers.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "100s-1000s of events/sec", "Continuous (webhook)")),
                    ),
                    tile(
                        "FinOps Cost Exports",
                        "market",
                        "FOCUS-format cloud cost and usage exports feeding cloud COGS and gross-margin analysis by product and customer.",
                        "focus",
                        cat="Cloud Cost & Usage (FinOps)",
                        what="FOCUS-format cloud cost and usage exports feeding cloud COGS and gross-margin analysis by product and customer.",
                        users="FinOps, finance and platform teams.",
                        data_out=data_out(
                            batch=flow(["structured"], "1-10 GB/day", "Daily exports")),
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Exec & Product",
                        "Genie One",
                        "The CEO on growth, net revenue retention and the path to profitable scale; the Chief Product Officer on activation, engagement and the roadmap that actually moves retention.",
                        [
                            ["Genie One", "Ask what this month's NRR was by segment, or which features drive retention, without booking analyst time."],
                            ["AI/BI", "ARR, NRR, activation and engagement on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the business glossary, so \"active\" and \"retained\" mean one thing across the company."],
                        ],
                        sub=[
                            ["CEO", "growth, net revenue retention and the path to profitable scale."],
                            ["Chief Product Officer", "activation, engagement and the roadmap that moves retention."],
                        ],
                        ucs=["Product Usage Analytics", "Churn & NRR Prediction", "PLG Activation", "Cloud COGS & Margin"],
                    ),
                    biz(
                        "Revenue & Sales",
                        "Model Serving",
                        "The Chief Revenue Officer on pipeline coverage and win rate; sales leadership on forecast accuracy and expansion in the installed base; RevOps on territory, quota and the accuracy of the number.",
                        [
                            ["Revenue Cockpit", "Coverage, slip and win-rate on the same numbers the board sees."],
                            ["Model Serving", "Win-propensity and expansion-likelihood scored inside the CRM path."],
                            ["AI/BI", "Forecast, coverage and net expansion on governed pipeline data."],
                        ],
                        sub=[
                            ["Chief Revenue Officer", "pipeline coverage, win rate and net expansion."],
                            ["Sales leadership", "forecast accuracy and expansion in the installed base."],
                            ["RevOps", "territory, quota and the accuracy of the number."],
                        ],
                        ucs=["Sales Pipeline Forecast", "Customer Health Scoring", "Usage-Based Billing"],
                    ),
                    biz(
                        "Finance & RevOps",
                        "AI/BI",
                        "The CFO on gross margin, cash and the efficiency of growth; RevOps and finance on usage-based revenue recognition, metering accuracy and the reconciliation of billed to consumed.",
                        [
                            ["AI/BI", "Margin, the ARR bridge and cash efficiency on certified Metric Views."],
                            ["Metering Console", "Metered consumption reconciled to invoices before the close."],
                            ["Genie One", "Ask which accounts are under-billed this month without a finance pull."],
                        ],
                        sub=[
                            ["CFO", "gross margin, cash and the efficiency of growth."],
                            ["RevOps & billing", "usage-based revenue, metering accuracy and billed-to-consumed."],
                        ],
                        ucs=["Usage-Based Billing", "Cloud COGS & Margin", "Sales Pipeline Forecast"],
                    ),
                    biz(
                        "Growth & Analytics",
                        "Lakehouse//RT",
                        "Growth teams on activation, conversion and expansion loops; product analytics on funnels, feature adoption and experiment readouts; lifecycle marketing on onboarding and reactivation.",
                        [
                            ["Growth Command Center", "Onboarding funnels and activation nudges scored per account."],
                            ["AI/BI", "A/B readouts on governed event data with one metric definition."],
                            ["Lakehouse//RT", "Live product state at the latency an onboarding flow moves at."],
                        ],
                        sub=[
                            ["Growth", "activation, free-to-paid conversion and expansion loops."],
                            ["Product analytics", "funnels, feature adoption and experiment readouts."],
                            ["Lifecycle marketing", "onboarding, reactivation and in-product messaging."],
                        ],
                        ucs=["PLG Activation", "Product Usage Analytics", "Experimentation & A/B", "GenAI Support Deflection"],
                    ),
                    biz(
                        "Platform & Security",
                        "Lakeflow",
                        "The CTO on developer velocity and reliability; platform engineering on the pipelines and the golden signals; the security and trust team on entitlement drift and access telemetry.",
                        [
                            ["Lakeflow", "Product, billing and telemetry feeds conformed for analytics."],
                            ["Entitlement Sync", "Access and permission events monitored for drift and abuse."],
                            ["MLflow", "Reliability and anomaly models tracked for audit and reproduction."],
                        ],
                        sub=[
                            ["CTO", "developer velocity, reliability and platform cost."],
                            ["Platform engineering", "the pipelines, golden signals and incident response."],
                            ["Security & trust", "entitlement drift, access telemetry and abuse."],
                        ],
                        ucs=["Entitlement Telemetry", "Churn & NRR Prediction", "Product Usage Analytics"],
                    ),
                ],
                [
                    biz(
                        "Platform & Data Eng",
                        "Lakeflow",
                        "Land the CRM, billing, telemetry and Git feeds with Fivetran, Airbyte and Kafka; run dbt and Airflow on the Bronze to Silver path; own the pager when the activation and revenue tables stall.",
                        [
                            ["Lakeflow Connect", "Managed connectors for Salesforce, Stripe and SaaS telemetry sources."],
                            ["Lakeflow Designer", "Declarative pipelines with expectations on event and billing feeds."],
                            ["Lakewatch", "Freshness on the activation and revenue tables the business reads every morning."],
                        ],
                        sub=[
                            ["Ingestion engineers", "CRM, billing and telemetry feeds into Bronze."],
                            ["Streaming engineers", "Kafka product and usage events into Lakehouse//RT."],
                            ["Platform & governance", "Unity Catalog permissions and the pipeline SLAs."],
                        ],
                        ucs=["Product Usage Analytics", "Usage-Based Billing", "Entitlement Telemetry"],
                    ),
                    biz(
                        "Applied ML Scientists",
                        "MLflow",
                        "Churn, expansion, propensity and support-deflection models built in Python with PyTorch, scikit-learn and Hugging Face, and whether they still hold once pricing, packaging and the product change.",
                        [
                            ["Feature Store", "Account and usage features read identically in training and serving."],
                            ["MLflow", "Every churn and experiment run tracked for audit and reproduction."],
                            ["Model Serving", "Propensity and deflection models scored in the product and CRM path."],
                        ],
                        sub=[
                            ["Growth & churn modelers", "activation, conversion and churn-risk models."],
                            ["Applied GenAI", "support-deflection and copilot agents on governed data."],
                            ["MLOps", "tracking and serving models in the operational path."],
                        ],
                        ucs=["Churn & NRR Prediction", "Sales Pipeline Forecast", "GenAI Support Deflection"],
                    ),
                    biz(
                        "Analytics Engineers",
                        "AI/BI",
                        "Model the semantic layer in dbt and serve it to Looker, Hex and Mode; own the metric definitions behind NRR, activation and margin so every team reads the same number.",
                        [
                            ["AI/BI", "Certified Metric Views for NRR, activation and gross margin."],
                            ["Genie One", "Natural-language answers over the governed semantic layer."],
                            ["Unity Catalog", "One definition of active, retained and billed across the stack."],
                        ],
                        sub=[
                            ["Metrics engineers", "the NRR, activation and margin definitions."],
                            ["BI & enablement", "self-serve dashboards and Genie for the business teams."],
                        ],
                        ucs=["Product Usage Analytics", "Cloud COGS & Margin", "Customer Health Scoring"],
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
                                "Executive and board dashboards against serverless SQL warehouses, with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for Unity Catalog-governed answers from the lakehouse, in the channel product and revenue teams already work in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Analyst notebooks, VS Code and JetBrains against governed product and revenue data with Genie Code.",
                            ),
                        ],
                    },
                    {
                        "box": "Growth Activation",
                        "ic": "zfunnel",
                        "tiles": [
                            tile(
                                "Reverse ETL to CDP",
                                "reverse",
                                "Health scores and lifecycle segments synced back to Segment and the CRM for in-product and email activation.",
                                "segment",
                            ),
                            tile(
                                "In-Product Messaging",
                                "dial",
                                "Onboarding nudges and expansion prompts served into the app from governed activation scores.",
                                "intercom",
                            ),
                            tile(
                                "Marketing Automation",
                                "market",
                                "Lifecycle and reactivation campaigns triggered from governed cohorts in Braze and the marketing stack.",
                                "braze",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "CRM Health Writeback",
                                "crm",
                                "Customer health scores and churn risk written back to Salesforce so CSMs act in the system they live in.",
                                "salesforce",
                            ),
                            tile(
                                "Usage to Billing",
                                "gauge",
                                "Rated consumption written to Stripe and Zuora so invoices match what was actually used.",
                                "stripe",
                            ),
                            tile(
                                "Entitlement Sync",
                                "key",
                                "Plan limits and feature flags pushed back to the app so entitlements match the contract.",
                            ),
                        ],
                    },
                    {
                        "box": "Partners & Sharing",
                        "ic": "share",
                        "tiles": [
                            tile(
                                "Customer Data Products",
                                "product",
                                "Usage and benchmark products published in Unity Catalog Domains and shared over OpenSharing.",
                            ),
                            tile(
                                "Embedded Analytics",
                                "aibi",
                                "Customer-facing dashboards embedded in the product against governed tables with row-level isolation.",
                            ),
                            tile(
                                "Investor & Board Share",
                                "share",
                                "Board and investor metrics shared live over Delta Sharing rather than a quarterly spreadsheet.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Trust",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "SOC 2 & Audit Evidence",
                                "gavel",
                                "Access and change evidence for SOC 2 and ISO 27001 produced from the same governed tables the company runs on.",
                            ),
                            tile(
                                "Privacy & DSAR",
                                "zshield",
                                "GDPR and CCPA subject access and deletion requests fulfilled from one governed customer record.",
                            ),
                        ],
                    },
                ],
                genie_spaces=[
                    genie("Product & Growth", "Ask about activation, engagement and retention across the product in plain language.",
                          feeds=["Segment CDP", "Amplitude Analytics", "Snowplow Behavioral", "Conformed account, user, subscription"],
                          teams=["Growth & Analytics", "Exec & Product", "Analytics Engineers"],
                          questions=[
                              "What is activation rate by signup cohort this month?",
                              "Which features correlate most with 90-day retention?",
                              "Where in onboarding do free users most often stall?",
                              "Which accounts show rising engagement but no paid upgrade?",
                              "What is free-to-paid conversion by acquisition channel?"]),
                    genie("Revenue & Retention", "Explore ARR, net revenue retention and churn across segments and cohorts.",
                          feeds=["Salesforce Sales Cloud", "Stripe Billing", "Zuora Billing", "NRR, activation, health, margin"],
                          teams=["Revenue & Sales", "Finance & RevOps", "Exec & Product"],
                          questions=[
                              "What is net revenue retention by segment this quarter?",
                              "Which accounts are at highest churn risk right now?",
                              "How does ARR bridge from new, expansion and churn this month?",
                              "Which cohorts show the strongest expansion?",
                              "What is win rate and pipeline coverage this quarter?"]),
                    genie("Usage & Billing", "Answer metering, billing accuracy and usage-based revenue questions.",
                          feeds=["m3ter Metering", "Stripe Billing", "FinOps Cost Exports", "Conformed account, user, subscription"],
                          teams=["Finance & RevOps", "Revenue & Sales", "Platform & Data Eng"],
                          questions=[
                              "Which accounts are under-billed versus metered consumption this month?",
                              "What is metering-to-invoice accuracy by product?",
                              "Which customers are approaching their plan limits?",
                              "What is revenue at risk from metering discrepancies?",
                              "How much usage-based revenue is unbilled right now?"]),
                    genie("Platform & Reliability", "Ask about developer velocity, reliability and incident trends across teams.",
                          feeds=["GitHub", "Jira Software", "PagerDuty", "Raw product and billing events"],
                          teams=["Platform & Security", "Platform & Data Eng", "Applied ML Scientists"],
                          questions=[
                              "What is deployment frequency and change-failure rate by team?",
                              "Which services have the worst MTTR this quarter?",
                              "How does cycle time trend across squads?",
                              "Which incidents correlate with recent deploys?",
                              "Where are access or entitlement anomalies concentrated?"]),
                ],
                dashboards=[
                    dashboard("Growth & Activation", "PLG activation, conversion and engagement funnels on certified Metric Views.",
                              kpis=["Activation rate", "Free-to-paid conversion", "WAU/MAU", "Feature adoption", "Time-to-value"],
                              teams=["Growth & Analytics", "Exec & Product", "Analytics Engineers"]),
                    dashboard("Revenue & NRR", "ARR bridge, net revenue retention and churn by cohort and segment.",
                              kpis=["ARR", "NRR", "Gross churn", "Expansion rate", "Win rate"],
                              teams=["Revenue & Sales", "Finance & RevOps", "Exec & Product"]),
                    dashboard("Usage & Margin", "Metered consumption, billing accuracy and cloud COGS by product and account.",
                              kpis=["Usage-based revenue", "Metering accuracy", "Gross margin", "Cloud COGS", "Revenue at risk"],
                              teams=["Finance & RevOps", "Revenue & Sales", "Analytics Engineers"]),
                    dashboard("Engineering Delivery", "Developer velocity, reliability and incident metrics across teams.",
                              kpis=["Deployment frequency", "Change-failure rate", "MTTR", "Cycle time", "Open incidents"],
                              teams=["Platform & Security", "Platform & Data Eng", "Applied ML Scientists"]),
                ],
            ),
        },
        "top": top_band(
            [
                app(
                    "Growth Command Center",
                    "Activation & conversion",
                    "zfunnel",
                    "Live activation, free-to-paid conversion and expansion funnels across every account, flagging the onboarding steps where users stall before they ever reach value.",
                ),
                app(
                    "Revenue Cockpit",
                    "Pipeline & forecast",
                    "market",
                    "Pipeline coverage, slip and win-rate with expansion signals drawn from product usage, so the forecast reflects what the installed base is actually doing.",
                ),
                app(
                    "Customer Health Hub",
                    "Health & churn",
                    "gauge",
                    "Account health scores and churn risk composed from usage, support and billing signals, routed to the CSM who owns the renewal.",
                ),
                app(
                    "Metering Console",
                    "Usage-based billing",
                    "gauge",
                    "Rated consumption reconciled to invoices before the close, with metering accuracy and revenue-at-risk visible per account.",
                ),
            ],
            [
                uc(
                    "Product Usage Analytics",
                    "Product",
                    "chart",
                    "Feature adoption, funnels and engagement measured on one governed event stream so product, growth and finance read the same activity.",
                    problem="Product events sit in a CDP and three analytics tools that each define \"active\" differently, so no two teams agree on adoption or what actually drives retention.",
                    who="Growth & Analytics",
                    how="Segment and Snowplow events land through Lakeflow and are conformed to certified Metric Views; funnels and adoption are explored in AI/BI from the Growth Command Center.",
                    comps=["Amplitude Analytics", "Snowplow Behavioral", "AI/BI", "Growth Command Center", "Unity Catalog"],
                    stories=[
                        ["Grammarly scales product analytics on Databricks", "https://www.databricks.com/customers/grammarly"],
                        ["Adobe brings creativity to life with data intelligence", "https://www.databricks.com/customers/adobe"],
                    ],
                ),
                uc(
                    "PLG Activation",
                    "Activation",
                    "zfunnel",
                    "Product-led onboarding and free-to-paid conversion, with the activation moment identified and nudged per account rather than left to chance.",
                    problem="Most self-serve signups never reach the activation moment, and the teams that could intervene find out weeks later from a dashboard instead of in the flow.",
                    who="Growth & Analytics",
                    how="Product events are scored against activation and conversion models in Model Serving; nudges are pushed back through Reverse ETL to CDP and the Growth Command Center on Lakehouse//RT.",
                    comps=["Segment CDP", "Model Serving", "Reverse ETL to CDP", "Growth Command Center", "Lakehouse//RT"],
                    stories=[
                        ["Iterable activates lifecycle journeys on Databricks", "https://www.databricks.com/customers/iterable"],
                        ["Zapier powers real-time customer experiences", "https://www.databricks.com/customers/zapier"],
                    ],
                ),
                uc(
                    "Churn & NRR Prediction",
                    "Retention",
                    "people",
                    "Predicting churn and net revenue retention from product, support and billing signals so the save happens before the renewal, not at it.",
                    problem="Churn shows up in the renewal number when it is too late to act, while the leading signals sit unjoined across product usage, support tickets and billing.",
                    who="Exec & Product",
                    how="Usage, support and billing features feed churn and expansion models tracked in MLflow and scored in Model Serving; risk surfaces in the Customer Health Hub for the owning team.",
                    comps=["Segment CDP", "Model Serving", "Feature Store", "Customer Health Hub", "MLflow"],
                    stories=[
                        ["SciPlay lifts retention with churn prediction", "https://www.databricks.com/customers/sciplay"],
                        ["SEGA Europe improves player retention with AI", "https://www.databricks.com/customers/sega"],
                    ],
                ),
                uc(
                    "Usage-Based Billing",
                    "Monetization",
                    "gauge",
                    "Metered consumption rated and reconciled to invoices before the close, so the company bills exactly what customers actually used.",
                    problem="Usage-based pricing leaks revenue when metering, rating and the invoice disagree, and the reconciliation of consumed to billed only surfaces after the period closes.",
                    who="Finance & RevOps",
                    how="Raw usage from the metering layer is conformed in the lakehouse, rated against the plan, and written back to billing from the Metering Console so invoices match consumption.",
                    comps=["m3ter Metering", "Stripe Billing", "Usage to Billing", "Metering Console", "AI/BI"],
                ),
                uc(
                    "Customer Health Scoring",
                    "Success",
                    "custlake",
                    "A single account health score composed from product, support and billing signals and routed to the CSM in the CRM they already work in.",
                    problem="Customer success works from gut feel and a stale spreadsheet because the signals of health live in product, support and billing systems that never meet.",
                    who="Revenue & Sales",
                    how="Health features are assembled in the Feature Store and scored in Model Serving; the score and its drivers are written back to Salesforce through CRM Health Writeback and shown in the Customer Health Hub.",
                    comps=["Salesforce Sales Cloud", "Model Serving", "CRM Health Writeback", "Customer Health Hub", "Feature Store"],
                    stories=[
                        ["Calculate customer lifetime value on Databricks", "https://www.databricks.com/solutions/accelerators/customer-lifetime-value"],
                    ],
                ),
                uc(
                    "GenAI Support Deflection",
                    "Support",
                    "chat",
                    "A governed assistant that resolves common support questions from the product docs and ticket history, deflecting volume before it reaches an agent.",
                    problem="Support volume scales with the customer base, and the answers already exist in docs and past tickets, but agents re-solve the same questions by hand every day.",
                    who="Growth & Analytics",
                    how="Zendesk and Intercom history and product docs are governed in Unity Catalog and served to an Agent Bricks assistant with AI Functions and Model Serving, deflecting and summarising tickets.",
                    comps=["Zendesk Support", "Intercom", "Agent Bricks", "AI Functions", "Model Serving"],
                    stories=[
                        ["Lumen reaches 35% ticket deflection with GenAI", "https://www.databricks.com/customers/lumen-technologies"],
                        ["Lippert improves customer support with Agent Bricks", "https://www.databricks.com/customers/lippert"],
                    ],
                ),
                uc(
                    "Entitlement Telemetry",
                    "Security",
                    "key",
                    "Access, permission and feature-entitlement events monitored for drift and abuse, so what a customer can reach always matches what they bought.",
                    problem="Entitlements drift as plans change and integrations proliferate, and access anomalies hide in event logs no one joins to the contract or the customer record.",
                    who="Platform & Security",
                    how="Access and permission events stream into Lakehouse//RT; anomaly models in Model Serving flag drift and abuse, and corrected limits are pushed back through Entitlement Sync under Unity Catalog.",
                    comps=["Kafka Event Streams", "Lakehouse//RT", "Entitlement Sync", "Model Serving", "Unity Catalog"],
                ),
                uc(
                    "Experimentation & A/B",
                    "Experiments",
                    "ztarget",
                    "A/B and feature-flag experiments read out on one governed metric definition, so product ships on evidence rather than the loudest opinion.",
                    problem="Experiment readouts disagree with the analytics tool and with finance because each computes the metric its own way, so results are argued rather than trusted.",
                    who="Growth & Analytics",
                    how="Exposure and outcome events are conformed to certified Metric Views; experiments are analysed in AI/BI with runs tracked in MLflow and surfaced from the Growth Command Center.",
                    comps=["Amplitude Analytics", "AI/BI", "MLflow", "Growth Command Center", "Unity Catalog"],
                    stories=[
                        ["Statsig runs experimentation at scale on Databricks", "https://www.databricks.com/customers/statsig"],
                    ],
                ),
                uc(
                    "Sales Pipeline Forecast",
                    "Forecast",
                    "market",
                    "Pipeline coverage and win-rate forecast enriched with product-usage and conversation signals, so the number reflects what the installed base is doing.",
                    problem="The forecast is a rep-entered guess disconnected from how accounts actually use the product, so coverage looks healthy right up until the quarter misses.",
                    who="Revenue & Sales",
                    how="Salesforce pipeline and Gong conversation data are conformed and scored for win and expansion propensity in Model Serving; coverage and slip are read in the Revenue Cockpit on AI/BI.",
                    comps=["Salesforce Sales Cloud", "Gong Revenue AI", "Model Serving", "Revenue Cockpit", "AI/BI"],
                    stories=[
                        ["Sales forecasting and attribution solution accelerator", "https://www.databricks.com/solutions/accelerators/sales-forecasting"],
                    ],
                ),
                uc(
                    "Cloud COGS & Margin",
                    "Margin",
                    "zcloudgear",
                    "Cloud cost of goods allocated to product and customer so gross margin is known per account, not just at the company level.",
                    problem="Cloud spend is the largest line in COGS but lands as one undifferentiated bill, so no one can say which product or customer is actually margin-positive.",
                    who="Finance & RevOps",
                    how="FOCUS-format cost exports are joined to usage and the customer hierarchy in the lakehouse; margin by product and account is served in AI/BI and the Metering Console under one definition.",
                    comps=["FinOps Cost Exports", "AI/BI", "Cloud Warehouse Marts", "Metering Console", "Unity Catalog"],
                ),
            ],
        ),
        "sources": {
            "salesforce": {"t": "Salesforce Sales Cloud", "u": "https://www.salesforce.com/sales/"},
            "hubspot": {"t": "HubSpot CRM", "u": "https://www.hubspot.com/products/crm"},
            "gong": {"t": "Gong Revenue AI", "u": "https://www.gong.io/"},
            "outreach": {"t": "Outreach", "u": "https://www.outreach.io/"},
            "stripe": {"t": "Stripe Billing", "u": "https://stripe.com/billing"},
            "zuora": {"t": "Zuora Billing", "u": "https://www.zuora.com/"},
            "chargebee": {"t": "Chargebee", "u": "https://www.chargebee.com/"},
            "m3ter": {"t": "m3ter usage metering", "u": "https://www.m3ter.com/"},
            "segment": {"t": "Twilio Segment CDP", "u": "https://segment.com/"},
            "amplitude": {"t": "Amplitude product analytics", "u": "https://amplitude.com/"},
            "snowplow": {"t": "Snowplow behavioral data", "u": "https://snowplow.io/"},
            "github": {"t": "GitHub", "u": "https://github.com/features"},
            "gitlab": {"t": "GitLab", "u": "https://about.gitlab.com/"},
            "jira": {"t": "Atlassian Jira Software", "u": "https://www.atlassian.com/software/jira"},
            "pagerduty": {"t": "PagerDuty", "u": "https://www.pagerduty.com/"},
            "zendesk": {"t": "Zendesk", "u": "https://www.zendesk.com/"},
            "intercom": {"t": "Intercom", "u": "https://www.intercom.com/"},
            "workday": {"t": "Workday HCM", "u": "https://www.workday.com/"},
            "netsuite": {"t": "Oracle NetSuite ERP", "u": "https://www.netsuite.com/portal/products/erp.shtml"},
            "kafka": {"t": "Apache Kafka", "u": "https://kafka.apache.org/"},
            "focus": {"t": "FinOps FOCUS specification", "u": "https://focus.finops.org/"},
            "braze": {"t": "Braze customer engagement", "u": "https://www.braze.com/"},
        },
    }
}
