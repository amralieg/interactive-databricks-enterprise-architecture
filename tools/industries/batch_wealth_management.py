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


INDUSTRIES_BATCH_WEALTH_MANAGEMENT = {
    "wealth_management": {
        "label": "Wealth Management",
        "blurb": "Advisor-led wealth and private banking: custody and clearing, portfolio management and rebalancing, financial planning, performance reporting, and suitability across client households.",
        "medallion": medallion(
            "Raw custodial and CRM feeds",
            "Custodial position and transaction files from Pershing, Fidelity and Schwab, Addepar and Orion portfolio extracts, Salesforce FSC activity and eMoney financial plans, landed exactly as received so a holding or a fee can always be replayed as it stood.",
            "Conformed household, account, position",
            "Households, clients, accounts and positions resolved into single conformed entities across the custody, portfolio and CRM estates, with security identifiers reconciled and every account linked to one household and one advisor.",
            "AUM, fees, performance, flows",
            "Contracted products the wealth business runs on: AUM and net new assets by advisor and household, fee revenue and margin, time-weighted performance and attribution, and net flows by segment and channel.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Custody & Clearing",
                    "ic": "partner",
                    "tiles": [
                        tile(
                            "Pershing NetX360",
                            "partner",
                            "BNY Pershing's clearing and custody platform: the book of record for RIA and broker-dealer accounts, positions, cash and transactions.",
                            "pershing",
                            cat="Custody & Clearing Platform",
                            what="BNY Pershing's clearing and custody platform: the book of record for RIA and broker-dealer accounts, positions, cash and transactions.",
                            users="Investment operations, custody teams and advisors.",
                            data_out=data_out(
                                batch=flow(["structured"], "10-50 GB/day positions + transactions", "Nightly custodial files")),
                        ),
                        tile(
                            "Fidelity Wealthscape",
                            "partner",
                            "Fidelity Institutional's custody and brokerage platform holding accounts, positions and settlement for advisors and their clients.",
                            "fidelity-inst",
                            cat="Custody & Clearing Platform",
                            what="Fidelity Institutional's custody and brokerage platform holding accounts, positions and settlement records for advisors and their clients.",
                            users="Investment operations, custody teams and advisors.",
                            data_out=data_out(
                                batch=flow(["structured"], "10-50 GB/day positions + transactions", "Nightly custodial files")),
                        ),
                        tile(
                            "Schwab Advisor Svcs",
                            "partner",
                            "Charles Schwab's custody platform for independent advisors: account, position and cost-basis records feeding the wealth estate.",
                            "schwab-adv",
                            cat="Custody & Clearing Platform",
                            what="Charles Schwab's custody platform for independent advisors, carrying account, position and cost-basis records into the wealth estate.",
                            users="Investment operations, custody teams and advisors.",
                            data_out=data_out(
                                batch=flow(["structured"], "10-50 GB/day positions + cost basis", "Nightly custodial files")),
                        ),
                        tile(
                            "Apex Clearing",
                            "db",
                            "Digital-first clearing and custody powering robo and hybrid-advice platforms, the source of accounts and fractional-share positions.",
                            "apex",
                            cat="Custody & Clearing Platform",
                            what="API-first clearing and custody powering robo and hybrid-advice platforms, the source of digitally opened accounts and fractional-share positions.",
                            users="Digital advice teams, investment operations and platform engineering.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-20 GB/day accounts + positions", "Nightly custodial files"),
                                stream=flow(["semi-structured"], "Account + trade events", "Continuous (API/events)")),
                        ),
                    ],
                },
                {
                    "box": "Portfolio Management",
                    "ic": "chart",
                    "tiles": [
                        tile(
                            "Addepar",
                            "chart",
                            "Portfolio management, aggregation and reporting for HNW and multi-custodial books, the source of consolidated positions, performance and exposures.",
                            "addepar-vendor",
                            cat="Portfolio Management & Reporting",
                            what="Portfolio management, aggregation and reporting for HNW and multi-custodial books, the source of consolidated positions, performance and exposures across the household.",
                            users="Investments, performance reporting and advisors.",
                            data_out=data_out(
                                batch=flow(["structured"], "20-80 GB/day positions + performance", "Nightly portfolio extracts")),
                        ),
                        tile(
                            "Orion Advisor Tech",
                            "chart",
                            "Portfolio accounting, performance and rebalancing for RIAs: the reconciled position and transaction ledger advisors bill and report against.",
                            "orion",
                            cat="Portfolio Accounting & Rebalancing",
                            what="Portfolio accounting, performance and rebalancing for RIAs, the reconciled position and transaction ledger advisors bill and report against.",
                            users="Investment operations, portfolio construction and advisors.",
                            data_out=data_out(
                                batch=flow(["structured"], "20-80 GB/day positions + transactions", "Nightly portfolio extracts")),
                        ),
                        tile(
                            "Envestnet Tamarac",
                            "sheet",
                            "RIA portfolio management, trading and rebalancing with model portfolios, the source of target weights and drift against household accounts.",
                            "tamarac",
                            cat="Portfolio Management & Rebalancing",
                            what="RIA portfolio management, trading and rebalancing with model portfolios, the source of target weights and drift against household accounts.",
                            users="Portfolio construction, trading and advisors.",
                            data_out=data_out(
                                batch=flow(["structured"], "10-40 GB/day models + drift", "Nightly portfolio extracts")),
                        ),
                        tile(
                            "SS&C Black Diamond",
                            "chart",
                            "Portfolio management and client reporting platform holding performance, holdings and billing for advisory firms.",
                            "black-diamond",
                            cat="Portfolio Management & Reporting",
                            what="Portfolio management and client reporting platform holding performance, holdings and billing records for advisory firms.",
                            users="Performance reporting, billing operations and advisors.",
                            data_out=data_out(
                                batch=flow(["structured"], "10-40 GB/day performance + billing", "Nightly portfolio extracts")),
                        ),
                    ],
                },
                {
                    "box": "Advisor CRM",
                    "ic": "crm",
                    "tiles": [
                        tile(
                            "Salesforce FSC",
                            "crm",
                            "Salesforce Financial Services Cloud: the advisor desktop for households, relationships, activities and service cases across the book.",
                            "sfdc-fsc",
                            cat="Wealth CRM",
                            what="Salesforce Financial Services Cloud, the advisor desktop for households, relationships, activities and service cases across the book.",
                            users="Advisory field, relationship managers and client associates.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-30 GB/day accounts + activities", "Nightly CDC"),
                                stream=flow(["semi-structured"], "Activity + case events", "Continuous (API/events)")),
                        ),
                        tile(
                            "Redtail CRM",
                            "crm",
                            "Wealth-native CRM widely used by independent advisors: contacts, households, activities and workflow the practice runs on.",
                            "redtail",
                            cat="Wealth CRM",
                            what="Wealth-native CRM widely used by independent advisors, carrying contacts, households, activities and the workflow the practice runs on.",
                            users="Advisory field, client associates and practice managers.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-10 GB/day contacts + activities", "Nightly CDC")),
                        ),
                        tile(
                            "Practifi",
                            "crm",
                            "Practice-management platform on the Salesforce stack for advice firms: pipeline, onboarding and service workflow.",
                            "practifi",
                            cat="Practice Management (CRM)",
                            what="Practice-management platform on the Salesforce stack for advice firms, carrying pipeline, onboarding and service workflow.",
                            users="Practice managers, onboarding and advisory field.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-10 GB/day pipeline + workflow", "Nightly CDC")),
                        ),
                        tile(
                            "Wealthbox",
                            "crm",
                            "Modern advisor CRM for contacts, tasks and communications, feeding client activity and relationship context into the estate.",
                            "wealthbox",
                            cat="Wealth CRM",
                            what="Modern advisor CRM for contacts, tasks and communications, feeding client activity and relationship context into the estate.",
                            users="Advisory field, client associates and practice managers.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-10 GB/day contacts + tasks", "Nightly CDC")),
                        ),
                    ],
                },
                {
                    "box": "Financial Planning",
                    "ic": "sheet",
                    "tiles": [
                        tile(
                            "eMoney Advisor",
                            "sheet",
                            "Financial planning and client portal: goals, cash-flow plans, held-away accounts and net-worth aggregation for each household.",
                            "emoney",
                            cat="Financial Planning Software",
                            what="Financial planning and client portal carrying goals, cash-flow plans, held-away accounts and net-worth aggregation for each household.",
                            users="Financial advisors, planning specialists and clients.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "5-20 GB/day plans + held-away", "Nightly plan extracts")),
                        ),
                        tile(
                            "MoneyGuide",
                            "sheet",
                            "Envestnet MoneyGuide goals-based planning: retirement, education and income plans the advice conversation is built around.",
                            "moneyguide",
                            cat="Financial Planning Software",
                            what="Goals-based planning covering retirement, education and income plans the advice conversation is built around.",
                            users="Financial advisors and planning specialists.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "5-20 GB/day plans + goals", "Nightly plan extracts")),
                        ),
                        tile(
                            "RightCapital",
                            "sheet",
                            "Planning software for tax-efficient retirement and distribution strategies, the source of plan assumptions and goal progress.",
                            "rightcapital",
                            cat="Financial Planning Software",
                            what="Planning software for tax-efficient retirement and distribution strategies, the source of plan assumptions and goal progress.",
                            users="Financial advisors and planning specialists.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "1-10 GB/day plans + assumptions", "Nightly plan extracts")),
                        ),
                        tile(
                            "Morningstar Advisor",
                            "market",
                            "Morningstar research, ratings and analytics for fund selection, model construction and investment due diligence.",
                            "morningstar-adv",
                            cat="Investment Research & Analytics",
                            what="Research, ratings and analytics for fund selection, model construction and investment due diligence.",
                            users="Investment research, portfolio construction and advisors.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-30 GB/day ratings + analytics", "Daily research updates")),
                        ),
                    ],
                },
                {
                    "box": "Onboarding & Compliance",
                    "ic": "gavel",
                    "tiles": [
                        tile(
                            "DocuSign eSignature",
                            "docs",
                            "Electronic signature and agreement workflow for account opening, disclosures and advisory agreements across the household.",
                            "docusign",
                            cat="eSignature / Agreement Platform",
                            what="Electronic signature and agreement workflow for account opening, disclosures and advisory agreements across the household.",
                            users="Onboarding, operations and compliance.",
                            data_out=data_out(
                                batch=flow(["structured", "unstructured"], "Signed agreements + envelope status", "Nightly batch"),
                                stream=flow(["semi-structured"], "Envelope completion events", "Continuous (webhooks)")),
                        ),
                        tile(
                            "Fenergo Onboarding",
                            "identity",
                            "Client lifecycle management for KYC, entity data and account opening, the source of verified client and beneficial-owner records.",
                            "fenergo",
                            cat="Client Lifecycle Management (KYC)",
                            what="Client lifecycle management for KYC, entity data and account opening, the source of verified client and beneficial-owner records.",
                            users="Onboarding, financial crime and compliance.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-10 GB/day KYC + entity records", "Nightly batch")),
                        ),
                        tile(
                            "LexisNexis KYC",
                            "gavel",
                            "Identity verification, sanctions and PEP screening data used to onboard and periodically re-screen clients and their entities.",
                            "lexisnexis",
                            cat="KYC & Screening Provider",
                            what="Identity verification, sanctions and PEP screening data used to onboard and periodically re-screen clients and their entities.",
                            users="Financial crime, compliance and onboarding.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "Screening results + watchlist deltas", "Daily screening refresh"),
                                stream=flow(["semi-structured"], "Screening API responses", "Continuous (API)")),
                        ),
                        tile(
                            "Global Relay Archive",
                            "chat",
                            "Communications capture and archiving for email, chat and voice, the books-and-records source for supervision and surveillance.",
                            "global-relay",
                            cat="Communications Archiving & Surveillance",
                            what="Communications capture and archiving for email, chat and voice, the books-and-records source for supervision and surveillance.",
                            users="Supervision, compliance and surveillance.",
                            data_out=data_out(
                                batch=flow(["unstructured", "semi-structured"], "50-200 GB/day messages + metadata", "Continuous capture, batch load")),
                        ),
                    ],
                },
                fed_group(
                    "Custodial BoR",
                    "Portfolio accounting and the custodial book of record left where they are and queried in place under Unity Catalog, which avoids a second copy of the reconciled positions and cost basis.",
                    cat="Custodial Book of Record",
                    what="Portfolio accounting and the custodial book of record kept in the incumbent system and queried in place, giving one reconciled view of positions and cost basis.",
                    users="Investment operations, fund accounting and finance.",
                    data_out=data_out(
                        batch=flow(["structured"], "TB-scale historical positions + cost basis", "Queried on demand (federated)")),
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "Custodial Files",
                        "stream",
                        "NSCC Fund/SERV and Networking files and DTCC position and transaction feeds parsed on arrival and landed as structured events.",
                        "dtcc",
                        cat="Custodial File Feed (NSCC/DTCC)",
                        what="NSCC Fund/SERV and Networking files and DTCC position and transaction feeds parsed on arrival and landed as structured events.",
                        users="Investment operations and data engineering.",
                        data_out=data_out(
                            batch=flow(["structured", "semi-structured"], "10-50 GB/day files", "Multiple settlement cycles daily")),
                    ),
                    tile(
                        "Market & Fund Data",
                        "api",
                        "Pricing, quote and fund-reference APIs from Morningstar and market-data vendors consumed inbound through managed ELT connectors.",
                        cat="Market & Fund Data API",
                        what="Pricing, quote and fund-reference APIs from Morningstar and market-data vendors consumed inbound through managed ELT connectors.",
                        users="Investments, performance reporting and data engineering.",
                        data_out=data_out(
                            batch=flow(["structured"], "5-30 GB/day prices + reference", "Intraday and end-of-day"),
                            stream=flow(["semi-structured"], "Quote + price updates", "Continuous (API)")),
                    ),
                    tile(
                        "Advisor SaaS APIs",
                        "api",
                        "CRM, planning and custody request/response APIs, and existing Kafka topics carrying account and market events, land here and are drawn generically on the reference board.",
                        cat="Advisor SaaS / Streaming API",
                        what="CRM, planning and custody request/response APIs and existing Kafka topics carrying account and market events, landed generically on the reference board.",
                        users="Data engineering, app developers and platform teams.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "Account + market events", "Continuous (API/Kafka)")),
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Wealth Leadership",
                        "Genie One",
                        "The head of wealth on AUM, net new assets and advisor productivity; the CFO on fee revenue, margin and cost to serve; the COO on platform consolidation and the operating model across custodians and offices.",
                        [
                            ["Genie One", "Ask what net new assets an office brought in, or what a household is worth, without waiting on an analyst."],
                            ["AI/BI", "AUM, net flows, fee revenue and advisor productivity on one certified set of Metric Views."],
                            ["Unity Catalog", "One governed household and glossary, so \"AUM\" and \"net new assets\" mean one thing across the firm."],
                        ],
                        sub=[
                            ["Head of Wealth", "AUM growth, net new assets and advisor productivity."],
                            ["CFO", "fee revenue, margin and cost to serve across the book."],
                            ["COO", "platform consolidation and the operating model across custodians."],
                        ],
                        ucs=["Client Household 360", "Client Attrition Risk", "Performance Reporting"],
                    ),
                    biz(
                        "Advisory Field",
                        "Genie One",
                        "Financial advisors preparing for and running client reviews; relationship managers on HNW and private-banking relationships; client associates on meeting prep, service requests and follow-up.",
                        [
                            ["Genie One", "Ask a client's tax-loss opportunity or held-away balances in plain language, in seconds, before the meeting."],
                            ["Agent Bricks", "Agents that draft a meeting brief and next best action against governed household data."],
                            ["Model Serving", "Attrition and next-best-action scores surfaced on the advisor desktop."],
                        ],
                        sub=[
                            ["Financial advisors", "client conversations, reviews and next best action."],
                            ["Relationship managers", "HNW and private-banking relationships."],
                            ["Client associates", "meeting prep, service requests and follow-up."],
                        ],
                        ucs=["Advisor Meeting Prep", "Next Best Action", "Client Attrition Risk"],
                    ),
                    biz(
                        "Investments",
                        "AI/BI",
                        "The chief investment office on model portfolios and asset allocation; portfolio construction on rebalancing and tax-aware trading; investment research on fund selection and manager due diligence.",
                        [
                            ["AI/BI", "Performance, attribution and drift on the same definitions the advisor reads to the client."],
                            ["Model Serving", "Rebalancing and tax-optimisation scored across households, not one account at a time."],
                            ["Unity Catalog", "One governed security master and model library across research and trading."],
                        ],
                        sub=[
                            ["Chief investment office", "model portfolios and asset allocation."],
                            ["Portfolio construction", "rebalancing and tax-aware trading across households."],
                            ["Investment research", "fund selection and manager due diligence."],
                        ],
                        ucs=["Model Portfolio Rebal", "Tax-Loss Harvesting", "Performance Reporting"],
                    ),
                    biz(
                        "Client Experience",
                        "CustomerLake",
                        "Digital and robo-advice teams on self-directed and hybrid journeys; client marketing on segmentation and personalised outreach; the onboarding team on account opening and funding.",
                        [
                            ["CustomerLake", "Household, planning and clickstream activated for personalisation without a separate CDP."],
                            ["Model Serving", "Propensity, funding and next-best-conversation models scored in the client journey."],
                            ["Apps", "Client portal and onboarding screens hosted next to governed data."],
                        ],
                        sub=[
                            ["Digital & robo advice", "self-directed and hybrid-advice journeys."],
                            ["Client marketing", "segmentation and personalised outreach."],
                            ["Onboarding", "account opening and funding."],
                        ],
                        ucs=["Digital & Robo Advice", "Client Onboarding", "Next Best Action"],
                    ),
                    biz(
                        "Risk & Compliance",
                        "AI Functions",
                        "Compliance on suitability, Reg BI and books-and-records; financial crime on KYC, AML and transaction monitoring; supervision on advisor conduct and communications surveillance.",
                        [
                            ["AI Functions", "Communications and account activity screened for suitability and abuse patterns at scale."],
                            ["Genie One", "Investigators ask for a client's activity around an event in plain language."],
                            ["Unity Catalog", "Audit trails and lineage that satisfy a regulatory examination."],
                        ],
                        sub=[
                            ["Compliance", "suitability, Reg BI and books-and-records."],
                            ["Financial crime", "KYC, AML and transaction monitoring."],
                            ["Supervision", "advisor conduct and communications surveillance."],
                        ],
                        ucs=["KYC AML & Suitability", "Client Onboarding", "Client Household 360"],
                    ),
                ],
                [
                    biz(
                        "Data Engineers",
                        "Lakeflow",
                        "Land Pershing, Fidelity and Schwab custodial files, Addepar and Orion positions and Salesforce FSC activity; own the Bronze to Silver path and the pager when a feed breaks.",
                        [
                            ["Lakeflow Connect", "Managed connectors for custody, CRM, planning and portfolio sources."],
                            ["Lakeflow Designer", "Declarative pipelines with expectations on position, transaction and fee feeds."],
                            ["Lakewatch", "Freshness on the household and performance tables advisors open every morning."],
                        ],
                    ),
                    biz(
                        "Data Scientists",
                        "MLflow",
                        "Attrition, next-best-action, funding-propensity and tax-optimisation models, and whether they still hold six months after deployment.",
                        [
                            ["Feature Store", "Household and behaviour features defined once and read identically in training and serving."],
                            ["MLflow", "Every run tracked for audit and reproduction under supervision."],
                            ["Model Serving", "Attrition and next-best-action models scored on the advisor desktop."],
                        ],
                    ),
                    biz(
                        "App Developers",
                        "Apps",
                        "Ship the advisor desktop, review builder, rebalancing and onboarding applications the firm works in, hosted next to governed data.",
                        [
                            ["Apps", "Advisor and client screens with no separate web tier to run or secure."],
                            ["Lakebase", "Serverless Postgres for onboarding state and governed writes."],
                            ["Agent Bricks", "Agents that draft review packs and rebalance proposals against governed tools."],
                        ],
                    ),
                ],
            ),
            "cons": cons_rail(
                [
                    {
                        "box": "BI & Productivity",
                        "ic": "chart",
                        "tiles": [
                            tile(
                                "Tableau / Power BI",
                                "chart",
                                "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for governed answers, and household and pipeline updates in the channel advisors already work in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Notebooks, VS Code and JetBrains against governed data and Genie Code.",
                            ),
                        ],
                    },
                    {
                        "box": "Client & Partner Sharing",
                        "ic": "share",
                        "tiles": [
                            tile(
                                "Custodian Sharing",
                                "share",
                                "Positions, performance and billing shared with custodians and sub-advisors over Delta Sharing rather than nightly file exchange.",
                            ),
                            tile(
                                "TAMP & BD Partners",
                                "partner",
                                "Turnkey asset-management programs and broker-dealer partners reading live household and model state on governed tables.",
                            ),
                            tile(
                                "Data Marketplace",
                                "market",
                                "Curated market, fund and benchmark datasets consumed and published through Databricks Marketplace.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "CRM & FSC Writeback",
                                "crm",
                                "Next best actions, meeting briefs and household scores written back into Salesforce FSC so the answer reaches the advisor's desktop.",
                            ),
                            tile(
                                "Rebalancer Writeback",
                                "gauge",
                                "Target weights and tax-aware trade proposals pushed back into Tamarac and Orion so the decision reaches the trading path.",
                            ),
                            tile(
                                "Alert & Case Queue",
                                "gavel",
                                "Suitability and surveillance alerts pushed to the supervision queue compliance already works.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "SEC & FINRA Filings",
                                "gavel",
                                "Form ADV, Reg BI and books-and-records evidence produced from the same governed tables the firm runs on.",
                            ),
                            tile(
                                "Client Statements",
                                "share",
                                "Performance, holdings and fee statements and 1099 reporting generated from contracted Gold products.",
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
                                "Custodians, sub-advisors and partners reading live tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ],
                genie_spaces=[
                    genie("Household & Relationship", "Ask about a household's value, held-away assets and relationship context in plain language.",
                          feeds=["Salesforce FSC", "Addepar", "Pershing NetX360", "Conformed household, account, position"],
                          teams=["Wealth Leadership", "Advisory Field", "Financial advisors"],
                          questions=[
                              "What is this household worth across every account and custodian?",
                              "Which held-away assets could we bring onto the platform?",
                              "How many households does each advisor manage and how active are they?",
                              "Which relationships have grown or shrunk most this year?",
                              "What service cases are open for this client right now?"]),
                    genie("Performance & Fees", "Ask about returns, fee revenue and net flows across the book in plain language.",
                          feeds=["Addepar", "SS&C Black Diamond", "AUM, fees, performance, flows"],
                          teams=["Investments", "Wealth Leadership", "CFO"],
                          questions=[
                              "What did each household return last quarter after fees?",
                              "What net new assets did each office bring in this month?",
                              "Where is fee margin thinnest across the book?",
                              "Which households have the largest net outflows this year?",
                              "How does performance compare to benchmark by segment?"]),
                    genie("Rebalancing & Tax", "Ask about model drift, rebalancing needs and tax-loss opportunities in plain language.",
                          feeds=["Envestnet Tamarac", "Orion Advisor Tech", "Conformed household, account, position"],
                          teams=["Investments", "Portfolio construction", "Chief investment office"],
                          questions=[
                              "Which households have drifted furthest from their model?",
                              "Where are the largest tax-loss harvesting opportunities right now?",
                              "How much cash is sitting undeployed across the book?",
                              "Which accounts breach a concentration or mandate limit?",
                              "What trades would a model change generate across households?"]),
                    genie("Compliance & Suitability", "Ask about suitability exceptions, screening and surveillance alerts in plain language.",
                          feeds=["LexisNexis KYC", "Global Relay Archive", "Conformed household, account, position"],
                          teams=["Risk & Compliance", "Compliance", "Supervision"],
                          questions=[
                              "Which accounts show suitability exceptions this month?",
                              "What is a client's account activity around this event?",
                              "Which KYC refreshes are overdue across the book?",
                              "Where did communications surveillance flag conduct risk?",
                              "What is our Reg BI documentation coverage by advisor?"]),
                ],
                dashboards=[
                    dashboard("AUM & Net Flows", "AUM, net new assets and flows across offices and advisors on certified Metric Views.",
                              kpis=["AUM", "Net new assets", "Net flows", "Fee revenue", "Advisor productivity"],
                              teams=["Wealth Leadership", "Investments", "CFO"]),
                    dashboard("Advisor Productivity", "Advisor activity, book health and next-best-action conversion across the field.",
                              kpis=["Households per advisor", "Revenue per advisor", "Meeting cadence", "Next-best-action conversion", "Client attrition rate"],
                              teams=["Advisory Field", "Wealth Leadership", "Relationship managers"]),
                    dashboard("Performance & Attribution", "Time-weighted return, attribution and drift on the same definitions advisors read to clients.",
                              kpis=["Time-weighted return", "Attribution", "Benchmark tracking", "Model drift", "Fee margin"],
                              teams=["Investments", "Chief investment office", "Portfolio construction"]),
                    dashboard("Compliance & Suitability", "Suitability, screening and surveillance posture across the book.",
                              kpis=["Suitability exceptions", "Alert volume", "Case backlog", "KYC refresh rate", "Reg BI coverage"],
                              teams=["Risk & Compliance", "Compliance", "Supervision"]),
                ],
            ),
        },
        "top": top_band(
            [
                app(
                    "Advisor Desktop",
                    "Household cockpit",
                    "apps",
                    "The unified screen an advisor runs the book from: household 360, next best action and meeting prep in one view, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Client Review Builder",
                    "Meeting packs",
                    "docs",
                    "Auto-drafts traceable client review packs and meeting briefs from portfolio, planning and CRM data, so preparation takes minutes instead of hours.",
                ),
                app(
                    "Rebalancing Console",
                    "Tax-aware trading",
                    "gauge",
                    "Model-portfolio drift, tax-loss opportunities and trade proposals across every household, scored and reviewed before orders reach the custodian.",
                ),
                app(
                    "Onboarding Studio",
                    "Account opening",
                    "identity",
                    "Digital account opening, funding and KYC in one flow, with signature, screening and custodial account creation orchestrated over governed writes.",
                ),
            ],
            [
                uc(
                    "Advisor Meeting Prep",
                    "Productivity",
                    "docs",
                    "Assembling a traceable client review pack and meeting brief from portfolio, planning and CRM data, so advisors spend the time on the conversation, not the preparation.",
                    problem="Client data is scattered across custody, portfolio, planning and CRM systems, so advisors burn hours hand-building each review pack and the least-served clients get the thinnest preparation.",
                    who="Advisory Field",
                    how="Household, portfolio and planning data are unified in the lakehouse; the Client Review Builder drafts traceable packs with Agent Bricks and advisors query specifics in Genie before the meeting.",
                    comps=["Client Review Builder", "Genie", "Salesforce FSC", "Agent Bricks", "Unity Catalog"],
                    stories=[
                        ["Wealth advisor productivity starts with the client conversation", "https://www.databricks.com/blog/wealth-advisor-productivity-starts-client-conversation"],
                    ],
                ),
                uc(
                    "Client Household 360",
                    "Household view",
                    "people",
                    "Resolving every account, entity and held-away asset into one household view across custodians, so the advisor and the firm see the whole relationship.",
                    problem="Accounts sit across multiple custodians and legal entities with no shared household key, so the true relationship value and concentration are invisible and reporting never ties out.",
                    who="Wealth Leadership",
                    how="Custody, portfolio and CRM feeds are conformed against one household key in the lakehouse and served to the Advisor Desktop and AI/BI on certified Metric Views.",
                    comps=["Advisor Desktop", "Unity Catalog", "Pershing NetX360", "Addepar", "AI/BI"],
                    stories=[
                        ["Addepar unifies portfolio, market and custodial data on Databricks", "https://www.databricks.com/customers/addepar"],
                        ["Wealth advisor productivity starts with the client conversation", "https://www.databricks.com/blog/wealth-advisor-productivity-starts-client-conversation"],
                    ],
                ),
                uc(
                    "Next Best Action",
                    "Advice",
                    "aisvc",
                    "Surfacing the most relevant next conversation for each household, from a funding opportunity to a plan gap, ranked and explained on the advisor's desktop.",
                    problem="Advisors cannot review every household every week, so opportunities and risks surface late or by luck rather than by a ranked, explainable signal.",
                    who="Advisory Field",
                    how="Household, planning and behaviour features feed next-best-action models in Model Serving; ranked, explained actions are written back to Salesforce FSC and the Advisor Desktop.",
                    comps=["Advisor Desktop", "Model Serving", "Feature Store", "Salesforce FSC", "CustomerLake"],
                    stories=[
                        ["MCP-Powered Financial AI Workflows on Databricks", "https://www.databricks.com/blog/mcp-powered-financial-ai-workflows-databricks"],
                    ],
                ),
                uc(
                    "Model Portfolio Rebal",
                    "Trading",
                    "gauge",
                    "Rebalancing every household to its target model with tax and cash constraints respected, run across the book instead of one account at a time.",
                    problem="Rebalancing runs account by account in the portfolio tool, so drift, tax lots and household constraints are handled inconsistently and trading is slow to react to a model change.",
                    who="Investments",
                    how="Positions and model targets are conformed in the lakehouse; drift and tax-aware trades are scored in Model Serving and written back to Tamarac and Orion from the Rebalancing Console.",
                    comps=["Rebalancing Console", "Envestnet Tamarac", "Orion Advisor Tech", "Model Serving", "AI/BI"],
                    stories=[
                        ["Addepar achieves scalable, cost-efficient data operations", "https://www.databricks.com/customers/addepar"],
                        ["Financial Services Investment Management reference architecture", "https://www.databricks.com/resources/architectures/financial-services-investment-management-reference-architecture"],
                    ],
                ),
                uc(
                    "Tax-Loss Harvesting",
                    "Tax alpha",
                    "chart",
                    "Finding realised-loss opportunities across a household's taxable accounts given current lots and estimated tax rate, before the tax year closes.",
                    problem="Tax-loss opportunities hide in per-account cost-basis data that is never viewed at household level, so harvestable losses expire unclaimed and wash-sale rules are hard to police.",
                    who="Investments",
                    how="Cost-basis and lot data are conformed to Gold; harvest candidates are scored across the household and surfaced in the Rebalancing Console and to advisors in Genie.",
                    comps=["Rebalancing Console", "Addepar", "Model Serving", "Genie", "Gold"],
                    stories=[
                        ["Wealth advisor productivity starts with the client conversation", "https://www.databricks.com/blog/wealth-advisor-productivity-starts-client-conversation"],
                    ],
                ),
                uc(
                    "Performance Reporting",
                    "Reporting",
                    "chart",
                    "Producing accurate, timely time-weighted performance, attribution and fee reporting for every household from one governed source instead of reconciled extracts.",
                    problem="Performance is stitched from custodian, portfolio and billing extracts that never agree, so client statements are late, inconsistent between systems and expensive to audit.",
                    who="Investments",
                    how="Positions, prices and fees are conformed against the custodial book of record; time-weighted performance and attribution are served to certified Gold products and Client Statements.",
                    comps=["Client Statements", "Addepar", "SS&C Black Diamond", "Data Products", "AI/BI"],
                    stories=[
                        ["Addepar unifies portfolio and custodial data on Databricks", "https://www.databricks.com/customers/addepar"],
                    ],
                ),
                uc(
                    "Client Attrition Risk",
                    "Retention",
                    "observ",
                    "Predicting which households are at risk of leaving or moving assets away, early enough for the advisor to act rather than explain the outflow afterwards.",
                    problem="Outflows and advisor departures are seen after the assets move, so retention is reactive and the households most worth saving are identified too late.",
                    who="Advisory Field",
                    how="Household, activity and flow features feed attrition models tracked in MLflow and scored in Model Serving; at-risk households surface on the Advisor Desktop with the reason and a suggested action.",
                    comps=["Advisor Desktop", "Model Serving", "Feature Store", "Salesforce FSC", "MLflow"],
                    stories=[
                        ["Databricks for Financial Services", "https://www.databricks.com/solutions/industries/financial-services"],
                    ],
                ),
                uc(
                    "Digital & Robo Advice",
                    "Hybrid advice",
                    "model",
                    "Powering self-directed and hybrid-advice journeys with personalised guidance, portfolios and nudges, at a cost to serve that reaches smaller and next-generation clients.",
                    problem="Digital advice journeys are generic and disconnected from the advised relationship, so smaller and next-generation clients get commodity guidance and drift to competitors.",
                    who="Client Experience",
                    how="Household and behaviour data are activated through CustomerLake; portfolio and guidance recommendations are scored in Model Serving and served into the digital and robo journey over Apex Clearing accounts.",
                    comps=["CustomerLake", "Model Serving", "Apex Clearing", "AI/BI", "Lakehouse"],
                    stories=[
                        ["Customer Story: HSBC", "https://www.databricks.com/customers/hsbc"],
                    ],
                ),
                uc(
                    "Client Onboarding",
                    "Account opening",
                    "identity",
                    "Opening, verifying and funding a new household across signature, KYC and custodial account creation in one governed flow rather than a multi-week paper chase.",
                    problem="Account opening spans signature, screening and custodial systems with manual re-keying, so onboarding takes weeks, funding stalls and status is invisible to the advisor.",
                    who="Client Experience",
                    how="Onboarding state is orchestrated in the Onboarding Studio on Lakebase; Fenergo screening and DocuSign signature events are governed in Unity Catalog and custodial accounts created over managed writes.",
                    comps=["Onboarding Studio", "Fenergo Onboarding", "DocuSign eSignature", "Unity Catalog", "Lakebase"],
                    stories=[
                        ["Addepar accelerates client onboarding with Databricks", "https://www.databricks.com/customers/addepar"],
                    ],
                ),
                uc(
                    "KYC AML & Suitability",
                    "Compliance",
                    "gavel",
                    "Screening clients and monitoring account activity for KYC, AML and suitability with an audit trail a regulator will accept, without drowning supervisors in false positives.",
                    problem="Screening and suitability run across siloed compliance systems with gappy data, so alerts are noisy, investigations are slow and completeness cannot be proven to an examiner.",
                    who="Risk & Compliance",
                    how="Client, activity and communications data are unified in the lakehouse; AI Functions and models score suitability and abuse patterns with LexisNexis screening, and cases open in the supervision queue.",
                    comps=["AI Functions", "LexisNexis KYC", "Unity Catalog", "Model Serving", "Global Relay Archive"],
                    stories=[
                        ["Customer Story: HSBC", "https://www.databricks.com/customers/hsbc"],
                        ["MCP-Powered Financial AI Workflows on Databricks", "https://www.databricks.com/blog/mcp-powered-financial-ai-workflows-databricks"],
                    ],
                ),
            ],
        ),
        "sources": {
            "pershing": {"t": "BNY Pershing solutions", "u": "https://www.pershing.com/us/en/solutions.html"},
            "fidelity-inst": {"t": "Fidelity Institutional (Wealthscape)", "u": "https://institutional.fidelity.com/"},
            "schwab-adv": {"t": "Schwab Advisor Services", "u": "https://en.wikipedia.org/wiki/Charles_Schwab_Corporation"},
            "apex": {"t": "Apex Fintech Solutions", "u": "https://www.apexfintechsolutions.com/"},
            "addepar-vendor": {"t": "Addepar", "u": "https://www.addepar.com/"},
            "orion": {"t": "Orion Advisor Tech", "u": "https://orion.com/"},
            "tamarac": {"t": "Envestnet Tamarac", "u": "https://www.tamaracinc.com/"},
            "black-diamond": {"t": "SS&C Black Diamond (SS&C Technologies)", "u": "https://www.ssctech.com/"},
            "sfdc-fsc": {"t": "Salesforce Financial Services Cloud", "u": "https://www.salesforce.com/products/financial-services-cloud/overview/"},
            "redtail": {"t": "Redtail Technology CRM", "u": "https://www.redtailtechnology.com/"},
            "practifi": {"t": "Practifi", "u": "https://www.practifi.com/"},
            "wealthbox": {"t": "Wealthbox CRM", "u": "https://www.wealthbox.com/"},
            "emoney": {"t": "eMoney Advisor", "u": "https://emoneyadvisor.com/"},
            "moneyguide": {"t": "Envestnet MoneyGuide", "u": "https://www.moneyguide.com/"},
            "rightcapital": {"t": "RightCapital", "u": "https://www.rightcapital.com/"},
            "morningstar-adv": {"t": "Morningstar Advisor Workstation", "u": "https://www.morningstar.com/products/advisor-workstation"},
            "docusign": {"t": "DocuSign eSignature", "u": "https://www.docusign.com/"},
            "fenergo": {"t": "Fenergo client lifecycle management", "u": "https://www.fenergo.com/"},
            "lexisnexis": {"t": "LexisNexis Risk Solutions (Financial Services)", "u": "https://risk.lexisnexis.com/financial-services"},
            "global-relay": {"t": "Global Relay communications archiving", "u": "https://www.globalrelay.com/"},
            "dtcc": {"t": "DTCC clearing and settlement", "u": "https://www.dtcc.com/"},
        },
    }
}
