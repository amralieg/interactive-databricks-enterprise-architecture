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


INDUSTRIES_BATCH_MARKET_DATA_EXCHANGES = {
    "market_data_exchanges": {
        "label": "Market Data & Exchanges",
        "blurb": "Securities exchanges and market-data vendors: matching engines and order books, tick and reference data, index calculation, market surveillance, and data-product licensing.",
        "medallion": medallion(
            "Raw feeds and messages",
            "ITCH and OUCH order-book messages, OPRA and consolidated-tape ticks, matching-engine gateway logs, corporate-actions announcements and index constituent files, landed exactly as received so a print or a quote can always be replayed as it stood.",
            "Conformed books, instruments, indices",
            "Order books, executions, instruments and index constituents resolved into single conformed entities across the matching, reference and index estates, with FIGI, ISIN and LEI identifiers reconciled and every print stitched to one security.",
            "Latency, quality, index, usage",
            "Contracted products the venue and data teams run on: matching latency and fairness by symbol, quote and trade quality, index levels and rebalance impact, and market-data consumption by subscriber and entitlement.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Trading & Matching",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "Nasdaq Matching",
                            "market",
                            "Nasdaq's INET matching engine and marketplace technology: the order book, matching and gateway layer that is the source of every order, quote and fill on the venue.",
                            "nasdaq-inet",
                            cat="Matching Engine / Trading Platform",
                            what="Nasdaq's INET matching engine and marketplace technology: the order book, matching and gateway layer that is the source of every order, quote and fill on the venue.",
                            users="Matching-engine operations, market quality and trading systems teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "100k-1M order/quote/fill messages/sec at peak", "Continuous (microsecond)")),
                        ),
                        tile(
                            "Deutsche Börse T7",
                            "market",
                            "The T7 trading platform behind Xetra and Eurex: order entry, matching and market-data generation for cash equities and derivatives.",
                            "t7",
                            cat="Matching Engine / Trading Platform",
                            what="The T7 trading platform behind Xetra and Eurex: order entry, matching and market-data generation for cash equities and derivatives.",
                            users="Matching-engine operations, market quality and derivatives operations.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "100k-1M order/quote messages/sec at peak", "Continuous (microsecond)")),
                        ),
                        tile(
                            "LSEG Millennium",
                            "market",
                            "MillenniumIT's Millennium Exchange matching platform: the low-latency order book and matching engine running the trading venue.",
                            "millennium",
                            cat="Matching Engine / Trading Platform",
                            what="MillenniumIT's Millennium Exchange matching platform: the low-latency order book and matching engine running the trading venue.",
                            users="Matching-engine operations and market-quality teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "50k-500k order/quote messages/sec at peak", "Continuous (microsecond)")),
                        ),
                        tile(
                            "CME Globex",
                            "market",
                            "The Globex electronic trading platform for futures and options: the source of the order, quote and trade stream for the derivatives venue.",
                            "globex",
                            cat="Derivatives Trading Platform",
                            what="The Globex electronic trading platform for futures and options: the source of the order, quote and trade stream for the derivatives venue.",
                            users="Derivatives market operations, matching-engine ops and clearing teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "100k-1M order/quote/trade messages/sec at peak", "Continuous (microsecond)")),
                        ),
                    ],
                },
                {
                    "box": "Market Data Feeds",
                    "ic": "stream",
                    "tiles": [
                        tile(
                            "TotalView-ITCH",
                            "stream",
                            "Nasdaq's full order-by-order depth-of-book feed: every add, modify, cancel and execution, the raw ground truth for level 2 and level 3 market data.",
                            "itch",
                            cat="Direct Market Data Feed (Depth of Book)",
                            what="Nasdaq's full order-by-order depth-of-book feed carrying every add, modify, cancel and execution, the raw ground truth for level 2 and level 3 market data.",
                            users="Feed engineering, market quality and quant subscribers.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "1-5M messages/sec at peak", "Continuous (sub-millisecond)")),
                        ),
                        tile(
                            "OPRA Options Feed",
                            "stream",
                            "The Options Price Reporting Authority consolidated feed: quotes and trades across every US options exchange, the industry's highest-volume market-data stream.",
                            "opra",
                            cat="Consolidated Options Data Feed",
                            what="The Options Price Reporting Authority consolidated feed carrying quotes and trades across every US options exchange, the industry's highest-volume market-data stream.",
                            users="Feed engineering, market-data operations and subscribers.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "several million msgs/sec at peak", "Continuous (sub-millisecond)")),
                        ),
                        tile(
                            "CTA/UTP SIP",
                            "stream",
                            "The Securities Information Processors carrying the consolidated tape: best bid and offer and last sale across all US equity venues.",
                            "sip",
                            cat="Consolidated Tape (SIP)",
                            what="The Securities Information Processors carrying the consolidated tape: best bid and offer and last sale across all US equity venues.",
                            users="Feed engineering, market-data operations and compliance.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "hundreds of thousands of msgs/sec at peak", "Continuous streaming")),
                        ),
                        tile(
                            "LSEG Real-Time",
                            "stream",
                            "LSEG's real-time pricing and market-data platform distributing consolidated ticks, quotes and reference updates to subscribers worldwide.",
                            "rtds",
                            cat="Real-Time Market Data Platform",
                            what="LSEG's real-time pricing and market-data platform distributing consolidated ticks, quotes and reference updates to subscribers worldwide.",
                            users="Feed engineering, data business and subscribers.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "10k-100k ticks/sec", "Continuous streaming")),
                        ),
                    ],
                },
                {
                    "box": "Reference & Corp Actions",
                    "ic": "db",
                    "tiles": [
                        tile(
                            "SIX Reference Data",
                            "db",
                            "SIX Financial Information's instrument, pricing and corporate-actions reference data, a golden source for terms, identifiers and events.",
                            "six",
                            cat="Reference Data Provider",
                            what="SIX Financial Information's instrument, pricing and corporate-actions reference data, a golden source for terms, identifiers and events.",
                            users="Reference-data engineering, index calculation and operations.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "GBs of reference + corporate actions", "Daily + intraday corporate actions")),
                        ),
                        tile(
                            "ANNA DSB ISIN/UPI",
                            "db",
                            "The ANNA Derivatives Service Bureau: ISIN, CFI and UPI allocation for OTC derivatives, the reference every instrument resolves against.",
                            "dsb",
                            cat="Instrument Identifier Registry",
                            what="The ANNA Derivatives Service Bureau allocating ISIN, CFI and UPI for OTC derivatives, the reference every instrument resolves against.",
                            users="Reference-data engineering, regulatory reporting and operations.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of identifier records", "Daily + on-demand allocation")),
                        ),
                        tile(
                            "GLEIF LEI",
                            "identity",
                            "The Global LEI Foundation register: legal-entity identifiers linking issuers, counterparties and subscribers to one governed identity.",
                            "lei",
                            cat="Legal Entity Identifier Registry",
                            what="The Global LEI Foundation register of legal-entity identifiers linking issuers, counterparties and subscribers to one governed identity.",
                            users="Reference-data engineering, compliance and entitlements teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of LEI records", "Daily refresh")),
                        ),
                        tile(
                            "Bloomberg FIGI",
                            "db",
                            "Bloomberg's open symbology (FIGI): a permanent instrument identifier that stitches vendor, venue and internal symbols to one security.",
                            "figi",
                            cat="Instrument Symbology Provider",
                            what="Bloomberg's open symbology (FIGI): a permanent instrument identifier that stitches vendor, venue and internal symbols to one security.",
                            users="Reference-data engineering, feed engineering and data business.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of symbology mappings", "Daily refresh + on-demand")),
                        ),
                    ],
                },
                {
                    "box": "Index & Benchmarks",
                    "ic": "chart",
                    "tiles": [
                        tile(
                            "S&P DJI Indices",
                            "chart",
                            "S&P Dow Jones Indices methodology, constituents and levels, the benchmark franchise licensed to funds and ETFs.",
                            "spdji",
                            cat="Index Provider / Benchmark Administrator",
                            what="S&P Dow Jones Indices methodology, constituents and levels, the benchmark franchise licensed to funds and ETFs.",
                            users="Index product managers, index calculation and licensing teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of constituents + levels", "End-of-day + rebalance cycles")),
                        ),
                        tile(
                            "FTSE Russell",
                            "chart",
                            "FTSE Russell index methodology, constituent weights and rebalance schedules feeding the calculation and licensing estate.",
                            "ftse",
                            cat="Index Provider / Benchmark Administrator",
                            what="FTSE Russell index methodology, constituent weights and rebalance schedules feeding the calculation and licensing estate.",
                            users="Index product managers, index calculation and benchmark governance.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of constituents + weights", "End-of-day + rebalance cycles")),
                        ),
                        tile(
                            "MSCI Indexes",
                            "chart",
                            "MSCI global equity and factor indices: constituents, weights and review data behind benchmark and derivative products.",
                            "msci",
                            cat="Index Provider / Benchmark Administrator",
                            what="MSCI global equity and factor indices: constituents, weights and review data behind benchmark and derivative products.",
                            users="Index product managers, index calculation and benchmark governance.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of constituents + review data", "End-of-day + review cycles")),
                        ),
                        tile(
                            "Solactive",
                            "chart",
                            "Solactive's index engine for custom and thematic benchmarks: methodology and constituent data for bespoke index calculation.",
                            "solactive",
                            cat="Index Calculation Engine",
                            what="Solactive's index engine for custom and thematic benchmarks: methodology and constituent data for bespoke index calculation.",
                            users="Index product managers, index quants and calculation teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of methodology + constituents", "End-of-day + rebalance cycles")),
                        ),
                    ],
                },
                {
                    "box": "Surveillance & Clearing",
                    "ic": "gavel",
                    "tiles": [
                        tile(
                            "Nasdaq SMARTS",
                            "gavel",
                            "Nasdaq's SMARTS market-surveillance platform: cross-market alerts for manipulation, spoofing and abuse against the venue's order flow.",
                            "smarts",
                            cat="Market Surveillance Platform",
                            what="Nasdaq's SMARTS market-surveillance platform generating cross-market alerts for manipulation, spoofing and abuse against the venue's order flow.",
                            users="Market surveillance, market integrity and compliance analysts.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "GBs of alerts + cases/day", "Intraday + end-of-day")),
                        ),
                        tile(
                            "OCC Clearing",
                            "partner",
                            "The Options Clearing Corporation: clearing, margin and settlement for listed options and futures, the source of cleared-position and margin state.",
                            "occ",
                            cat="Central Counterparty (Clearing House)",
                            what="The Options Clearing Corporation clearing, margin and settlement for listed options and futures, the source of cleared-position and margin state.",
                            users="Clearing and settlement operations and risk teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of cleared positions + margin", "Multiple clearing cycles daily")),
                        ),
                        tile(
                            "LCH / CCP",
                            "partner",
                            "LCH and central counterparty clearing: novated trades, margin calls and default-fund state across cleared markets.",
                            "lch",
                            cat="Central Counterparty (Clearing House)",
                            what="LCH and central counterparty clearing carrying novated trades, margin calls and default-fund state across cleared markets.",
                            users="Clearing and settlement operations and risk teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of novated trades + margin", "Multiple clearing cycles daily")),
                        ),
                        tile(
                            "DTCC Settlement",
                            "partner",
                            "DTCC clearing, netting and settlement: matched trades, affirmations and settlement status for the post-trade lifecycle.",
                            "dtcc",
                            cat="Clearing & Settlement Utility",
                            what="DTCC clearing, netting and settlement carrying matched trades, affirmations and settlement status for the post-trade lifecycle.",
                            users="Clearing and settlement operations and post-trade teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of confirms + settlement/day", "Multiple settlement cycles daily")),
                        ),
                    ],
                },
                fed_group(
                    "Market Data Billing",
                    "The market-data billing and revenue-accounting mart left where it is and queried in place under Unity Catalog, which avoids a second copy of the audited subscription and usage numbers.",
                    cat="Revenue / Billing Data Mart",
                    what="The market-data billing and revenue-accounting mart kept in the incumbent warehouse and queried in place, giving one audited view of subscription and usage numbers.",
                    users="Licensing and entitlements, finance and the data business.",
                    data_out=data_out(
                        batch=flow(["structured"], "TB-scale billing + usage history", "Queried on demand (federated)")),
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "Multicast Feed Bus",
                        "stream",
                        "Exchange multicast market-data channels (ITCH, OUCH and vendor feeds) captured off the wire and landed as structured depth and trade events.",
                        "itch",
                        cat="Streaming Market Data Bus",
                        what="Exchange multicast market-data channels (ITCH, OUCH and vendor feeds) captured off the wire and landed as structured depth and trade events.",
                        users="Feed engineering and platform reliability.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "1-5M messages/sec at peak", "Continuous (sub-millisecond)")),
                    ),
                    tile(
                        "FIX / FAST Gateways",
                        "api",
                        "FIX order-entry and FAST-encoded market-data sessions with members and vendors parsed on arrival and landed as structured events.",
                        "fix",
                        cat="FIX/FAST Messaging Gateway",
                        what="FIX order-entry and FAST-encoded market-data sessions with members and vendors parsed on arrival and landed as structured events.",
                        users="Feed engineering and market operations.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "10k-100k messages/sec at peak", "Continuous (sub-second)")),
                    ),
                    tile(
                        "Vendor Data APIs",
                        "api",
                        "Reference, corporate-actions and index-constituent request/response and file APIs consumed inbound through managed ELT connectors.",
                        cat="Reference Data Vendor API",
                        what="Reference, corporate-actions and index-constituent request/response and file APIs consumed inbound through managed ELT connectors.",
                        users="Reference-data engineering and index calculation.",
                        data_out=data_out(
                            batch=flow(["structured", "semi-structured"], "1-5 GB/day", "Daily + on-demand pulls")),
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Exchange Exec",
                        "Genie One",
                        "The CEO on trading volumes, listings and the growth of the data and index franchise; the CFO on transaction, data and index revenue against the cost of running the venue; the Chief Commercial Officer on how market-data and index products are packaged, priced and sold.",
                        [
                            ["Genie One", "Ask what data and index revenue did last quarter, or which feed a client churned from, without booking an analyst."],
                            ["AI/BI", "Trading volume, data-subscription and index revenue on one certified set of Metric Views."],
                            ["Unity Catalog", "One governed glossary, so \"billable usage\" and \"active subscriber\" mean one thing across the group."],
                        ],
                        sub=[
                            ["CEO", "trading volumes, listings and the growth of the data and index franchise."],
                            ["CFO", "transaction, data and index revenue against the cost of running the venue."],
                            ["Chief Commercial Officer", "how market-data and index products are packaged, priced and sold."],
                        ],
                        ucs=["Data Monetization", "Market Data Feeds", "Index Calculation"],
                    ),
                    biz(
                        "Market Ops",
                        "Lakehouse//RT",
                        "Matching-engine operators watching fill rates, message rates and gateway health; the market-quality team on spreads, depth and fairness; the clearing and settlement operations team on margin, fails and settlement risk across the trading day.",
                        [
                            ["Lakehouse//RT", "Order-book, gateway and clearing state at the latency the matching engine actually runs at."],
                            ["Model Serving", "Fairness, anomaly and settlement-risk models scored inside the trading day."],
                            ["AI/BI", "Latency, spread, depth and fails on the same definitions the market-quality team defends."],
                        ],
                        sub=[
                            ["Matching-engine ops", "fill rates, message rates and gateway health."],
                            ["Market quality", "spreads, depth and execution fairness by symbol."],
                            ["Clearing & settlement ops", "margin, fails and settlement risk across the day."],
                        ],
                        ucs=["Matching & Fairness", "Clearing & Settlement", "Market Surveillance"],
                    ),
                    biz(
                        "Data Business",
                        "Data Products",
                        "The Chief Data Officer on the market-data and reference-data catalogue; data product managers packaging tick, depth and corporate-actions feeds; the licensing and entitlements team metering consumption and billing subscribers for what they actually use.",
                        [
                            ["Data Products", "Tick, depth, reference and corporate-actions feeds published as contracted, discoverable products."],
                            ["Open Sharing", "Live feeds delivered to subscribers and vendors with no copy and no egress duplication."],
                            ["Unity Catalog", "Entitlements, lineage and usage governed from the same catalogue the products live in."],
                        ],
                        sub=[
                            ["Chief Data Officer", "the market-data and reference-data catalogue end to end."],
                            ["Data product managers", "packaging tick, depth and corporate-actions feeds."],
                            ["Licensing & entitlements", "metering consumption and billing subscribers for actual use."],
                        ],
                        ucs=["Market Data Feeds", "Corporate Actions", "Data Entitlements", "Data Monetization", "Reference Data Master"],
                    ),
                    biz(
                        "Index Products",
                        "AI/BI",
                        "Index product managers launching and maintaining benchmarks; the index calculation team running real-time and end-of-day levels and rebalances; benchmark governance proving methodology, restatements and IOSCO compliance to regulators and licensees.",
                        [
                            ["AI/BI", "Index levels, constituent weights and rebalance impact on one certified set of Metric Views."],
                            ["MLflow", "Every index restatement and methodology change tracked for audit and reproduction."],
                            ["Unity Catalog", "Constituent data and methodology governed with lineage from source to published level."],
                        ],
                        sub=[
                            ["Index product managers", "launching and maintaining benchmarks and custom indices."],
                            ["Index calculation", "real-time and end-of-day levels and rebalances."],
                            ["Benchmark governance", "methodology, restatements and IOSCO compliance."],
                        ],
                        ucs=["Index Calculation", "Reference Data Master", "Data Monetization"],
                    ),
                    biz(
                        "Surveil & Reg",
                        "AI Functions",
                        "Market-surveillance analysts investigating spoofing, layering and manipulation across the venue's order flow; the market-integrity team on member conduct; the regulatory reporting team filing CAT, MiFID and transaction reports as the market operator.",
                        [
                            ["AI Functions", "Order and trade patterns screened for manipulation across the whole venue at scale."],
                            ["Genie One", "Investigators ask for a member's activity around a print in plain language."],
                            ["Unity Catalog", "Complete, auditable order-and-trade trails that satisfy a regulatory examination."],
                        ],
                        sub=[
                            ["Market surveillance", "spoofing, layering and manipulation across order flow."],
                            ["Market integrity", "member conduct and disciplinary referrals."],
                            ["Regulatory reporting", "CAT, MiFID and transaction reporting as operator."],
                        ],
                        ucs=["Market Surveillance", "Regulatory Reporting", "Matching & Fairness"],
                    ),
                ],
                [
                    biz(
                        "Feed Engineers",
                        "Lakeflow",
                        "Capture ITCH and OUCH multicast, OPRA and consolidated-tape feeds and Exegy-style feed handlers off Kafka, curate the depth and trade tables, and keep every tick feed fresh for calculation and distribution.",
                        [
                            ["Lakeflow Connect", "Managed connectors for matching-engine, reference and vendor sources."],
                            ["Auto Loader", "Continuous ingestion of multicast and file feeds into Bronze with schema evolution."],
                            ["Lakewatch", "Freshness on the tick and reference tables every desk and subscriber depends on."],
                        ],
                        sub=[
                            ["Ingestion Engineers", "ITCH and OUCH multicast, OPRA and consolidated-tape feeds captured off the wire on time."],
                            ["Pipeline Engineers", "depth and trade tables conformed with expectations on every tick feed."],
                            ["Platform Reliability", "freshness of the tick and reference tables every desk and subscriber depends on."],
                        ],
                    ),
                    biz(
                        "Index Quants",
                        "MLflow",
                        "Turn index methodology in Python and kdb+/q into production calculation, rebalancing and backtests, and own the libraries the index and benchmark teams run against.",
                        [
                            ["Feature Store", "Constituent and factor features defined once and read identically in research and calculation."],
                            ["MLflow", "Every index calculation, restatement and backtest versioned and reproducible for audit."],
                            ["Model Serving", "Index levels and rebalance impact computed in the live calculation path."],
                        ],
                        sub=[
                            ["Calculation Engineers", "index methodology turned into production calculation and rebalancing."],
                            ["Backtest Engineers", "index restatements and backtests versioned and reproducible for audit."],
                            ["Reference Data Engineers", "constituent, identifier and corporate-actions data conformed for calculation."],
                        ],
                    ),
                    biz(
                        "App Developers",
                        "Apps",
                        "Ship the market-quality, feed-operations, index and surveillance applications the venue works in, hosted next to governed data.",
                        [
                            ["Apps", "Operational screens with no separate web tier to run or secure."],
                            ["Lakebase", "Serverless Postgres for entitlement, case and index-publication state with governed writes."],
                            ["Agent Bricks", "Agents that draft a surveillance case or a feed-outage summary against governed tools."],
                        ],
                        sub=[
                            ["Full-Stack Engineers", "the market-quality, feed-operations and index screens the venue works in."],
                            ["Agent Developers", "agents that draft a surveillance case or feed-outage summary on governed tools."],
                            ["Integration Engineers", "entitlement, case and index-publication writeback into venue systems."],
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
                                "Genie in Teams for governed answers, and feed-outage and surveillance alerts in the channel operations already work in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Notebooks, VS Code and JetBrains against governed tick, reference and index data with Genie Code.",
                            ),
                        ],
                    },
                    {
                        "box": "Data Distribution",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "Delta Sharing Feeds",
                                "share",
                                "Tick, reference, corporate-actions and index feeds delivered to subscribers and vendors over Delta Sharing rather than file drops and FTP.",
                            ),
                            tile(
                                "Cloud Marketplaces",
                                "market",
                                "Curated data and index products listed and monetised through Databricks Marketplace and cloud data exchanges.",
                            ),
                            tile(
                                "Subscriber APIs",
                                "api",
                                "Entitled query and snapshot APIs serving reference, index and end-of-day products to licensed subscribers.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "Entitlement Writeback",
                                "db",
                                "Entitlement, usage and billing decisions written back into the data-access control and licensing systems so the answer reaches the delivery path.",
                            ),
                            tile(
                                "Surveillance Cases",
                                "gavel",
                                "Manipulation and abuse alerts pushed to the investigation and disciplinary case queue analysts already work.",
                            ),
                            tile(
                                "Index Publication",
                                "product",
                                "Calculated index levels and rebalance files published back to the dissemination and licensing systems that distribute them.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "CAT / MiFID Reports",
                                "gavel",
                                "Consolidated Audit Trail and MiFID order-and-trade reporting produced by the venue from the same governed tables it matches on.",
                                ["cat", "mifid"],
                            ),
                            tile(
                                "Reg Submissions",
                                "share",
                                "Market-operator, transparency and benchmark-administration submissions filed from contracted Gold products.",
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
                                "Published, contracted market-data and index products discoverable in Unity Catalog Domains and shared over Open Sharing.",
                            ),
                            tile(
                                "Sharing Recipients",
                                "share",
                                "Subscribers, vendors and index licensees reading live tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ],
                genie_spaces=[
                    genie("Market Quality & Latency", "Ask about matching latency, spreads, depth and fairness by symbol in plain language.",
                          feeds=["Nasdaq Matching", "TotalView-ITCH", "Latency, quality, index, usage"],
                          teams=["Market Ops", "Matching-engine ops", "Market quality"],
                          questions=[
                              "What is our matching latency by symbol right now versus yesterday?",
                              "Which symbols show the widest spreads and thinnest depth today?",
                              "Where did message rates spike and did any gateway degrade?",
                              "Are there fairness concerns in fill sequencing for any symbol?",
                              "Which gateways are closest to capacity at peak?"]),
                    genie("Data Revenue & Entitlements", "Explore data-subscription revenue, usage and entitlement coverage.",
                          feeds=["Market Data Billing", "LSEG Real-Time", "Latency, quality, index, usage"],
                          teams=["Data Business", "Exchange Exec", "Licensing & entitlements"],
                          questions=[
                              "What did data-subscription revenue do last quarter by product?",
                              "Which subscribers consume the most billable usage right now?",
                              "Where is usage exceeding entitlement, and by how much?",
                              "Which feeds have the strongest adoption this year?",
                              "Which clients recently churned from a feed and what did they consume?"]),
                    genie("Index & Benchmarks", "Ask about index levels, constituent weights and rebalance impact.",
                          feeds=["S&P DJI Indices", "FTSE Russell", "MSCI Indexes", "Conformed books, instruments, indices"],
                          teams=["Index Products", "Index calculation", "Benchmark governance"],
                          questions=[
                              "What are today's levels and the largest movers across our indices?",
                              "What is the projected turnover for the next rebalance?",
                              "Which constituents drive the most weight change this review?",
                              "How many restatements occurred this quarter and why?",
                              "Are all index calculations meeting their publication SLA?"]),
                    genie("Surveillance & Integrity", "Investigate manipulation, member conduct and order-trail completeness.",
                          feeds=["Nasdaq SMARTS", "CTA/UTP SIP", "Conformed books, instruments, indices"],
                          teams=["Surveil & Reg", "Market surveillance", "Regulatory reporting"],
                          questions=[
                              "Which members showed spoofing or layering patterns this week?",
                              "What was a member's activity around this print?",
                              "Which alert types have the worst false-positive rate?",
                              "How many surveillance cases are open past their SLA?",
                              "Is our order and trade trail complete for the reporting period?"]),
                ],
                dashboards=[
                    dashboard("Trading & Volume", "Matched volume, message rates and order-book health across the venue.",
                              kpis=["Matched volume", "Message rate", "Fill rate", "Order-to-trade ratio", "Spread"],
                              teams=["Exchange Exec", "Market Ops", "Chief Commercial Officer"]),
                    dashboard("Data Monetization", "Data-subscription revenue, active subscribers and entitlement coverage.",
                              kpis=["Data revenue", "Active subscribers", "Billable usage", "Entitlement coverage", "Feed adoption"],
                              teams=["Data Business", "Exchange Exec", "Licensing & entitlements"]),
                    dashboard("Index Operations", "Index levels, rebalance impact and calculation quality.",
                              kpis=["Index levels", "Rebalance impact", "Constituent turnover", "Restatement count", "Calculation SLA"],
                              teams=["Index Products", "Index calculation", "Benchmark governance"]),
                    dashboard("Surveillance & Regulatory", "Alert quality, case backlog and regulatory reporting timeliness.",
                              kpis=["Alert volume", "False-positive rate", "Case backlog", "Report timeliness", "Order-trail completeness"],
                              teams=["Surveil & Reg", "Market surveillance", "Regulatory reporting"]),
                ],
            ),
        },
        "top": top_band(
            [
                app(
                    "Market Quality",
                    "Order book health",
                    "gauge",
                    "The screen the market-quality team runs the venue from: spread, depth, message rates and matching latency by symbol, flagging fairness and outage risk before members notice, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Feed Ops Monitor",
                    "Feed dissemination",
                    "stream",
                    "Live health of every disseminated feed: gap detection, sequence integrity and subscriber delivery latency, so a dropped multicast channel is caught before the support calls start.",
                ),
                app(
                    "Index Cockpit",
                    "Index calculation",
                    "chart",
                    "Where index managers watch real-time levels, constituent weights and rebalance impact, and sign off restatements against a full methodology audit trail.",
                ),
                app(
                    "Surveillance Console",
                    "Market abuse",
                    "gavel",
                    "Manipulation, spoofing and layering alerts triaged with the member's full order and print context in one investigation view, with a case trail a regulator will accept.",
                ),
            ],
            [
                uc(
                    "Market Data Feeds",
                    "Distribution",
                    "stream",
                    "Capturing full order-by-order depth, consolidated ticks and quotes and republishing them to subscribers and internal analytics on one governed platform instead of a separate real-time silo.",
                    problem="Tick feeds land in a low-latency plant that analytics cannot touch, so the same ITCH and OPRA data is copied into a second estate for research, billing and distribution, and the copies never agree.",
                    who="Data Business",
                    how="ITCH, OPRA and SIP feeds land through the Multicast Feed Bus and Zerobus into Lakehouse//RT; conformed depth and trade products are served to internal teams and out to subscribers over Delta Sharing Feeds.",
                    comps=["Feed Ops Monitor", "Multicast Feed Bus", "Lakehouse//RT", "Delta Sharing Feeds", "Zerobus"],
                    stories=[
                        ["Nasdaq reinvents finance with Databricks", "https://www.databricks.com/customers/nasdaq"],
                        ["The boom of SOON: Coinbase streaming ingestion", "https://www.databricks.com/customers/coinbase/streaming"],
                    ],
                ),
                uc(
                    "Matching & Fairness",
                    "Market quality",
                    "gauge",
                    "Watching matching latency, spread, depth and fill fairness by symbol so market-quality problems and gateway issues are caught in the trading day rather than in a post-mortem.",
                    problem="Matching-engine and gateway telemetry sits in operational logs no analytics can reach, so latency drift and fairness questions are answered days later from partial exports.",
                    who="Market Ops",
                    how="Gateway logs and order-book events stream into Lakehouse//RT; latency, spread and fairness metrics are computed to Gold and watched in the Market Quality app on the market-quality team's own definitions.",
                    comps=["Market Quality", "Nasdaq Matching", "Lakehouse//RT", "TotalView-ITCH", "AI/BI"],
                    stories=[
                        ["Nasdaq reinvents finance with Databricks", "https://www.databricks.com/customers/nasdaq"],
                        ["Modernizing investment data platforms", "https://www.databricks.com/blog/2021/01/29/strategies-for-modernizing-investment-data-platforms.html"],
                    ],
                ),
                uc(
                    "Index Calculation",
                    "Benchmarks",
                    "chart",
                    "Running real-time and end-of-day index levels, weights and rebalances at the scale of thousands of benchmarks, with a methodology audit trail for every restatement.",
                    problem="Index calculation runs in bespoke engines that cannot scale to thousands of custom benchmarks or replay a methodology change, so launches are slow and restatements are hard to defend.",
                    who="Index Products",
                    how="Constituent, pricing and corporate-actions data are conformed in the lakehouse; levels and rebalance impact are computed in Model Serving and signed off in the Index Cockpit against certified Metric Views.",
                    comps=["Index Cockpit", "S&P DJI Indices", "Model Serving", "AI/BI", "Index Publication"],
                    stories=[
                        ["Nasdaq reinvents finance with Databricks", "https://www.databricks.com/customers/nasdaq"],
                        ["S&P Global unifies data intelligence", "https://www.databricks.com/customers/sp-global"],
                    ],
                ),
                uc(
                    "Market Surveillance",
                    "Market abuse",
                    "gavel",
                    "Detecting spoofing, layering, wash trades and manipulation across the venue's own order flow, with an audit trail and completeness a regulator will accept.",
                    problem="Surveillance runs in a vendor silo with gappy data, so alerts are noisy, investigations are slow, and completeness across the venue's order flow cannot be proven to an examiner.",
                    who="Surveil & Reg",
                    how="Orders, executions and messages are unified in the lakehouse with Unity Catalog completeness checks; detectors and AI Functions score patterns and cases open in the Surveillance Console.",
                    comps=["Surveillance Console", "Nasdaq SMARTS", "AI Functions", "Model Serving", "Lakehouse//RT"],
                    stories=[
                        ["FINRA: predictive fraud detection at scale", "https://www.databricks.com/blog/2019/06/05/customer-spotlight-finra.html"],
                        ["Real-time fraud detection at Coinbase", "https://www.databricks.com/customers/coinbase/lakeflow"],
                    ],
                ),
                uc(
                    "Data Monetization",
                    "Commercial",
                    "product",
                    "Packaging tick, reference, corporate-actions and index data as contracted products and selling them to subscribers over sharing and marketplaces instead of bespoke file feeds.",
                    problem="Every new data product is a custom extract-and-FTP build, so time-to-launch is long, copies proliferate, and the venue cannot see who consumes what or prove entitlement.",
                    who="Exchange Exec",
                    how="Curated feeds are published as contracted Data Products, discoverable in Unity Catalog and delivered over Open Sharing and Cloud Marketplaces to entitled Sharing Recipients with no copy.",
                    comps=["Data Products", "Sharing Recipients", "Open Sharing", "Cloud Marketplaces", "Unity Catalog"],
                    stories=[
                        ["LSEG and Databricks partner on AI-ready data via Delta Sharing", "https://www.lseg.com/en/media-centre/press-releases/2025/lseg-databricks-partner-bring-ai-ready-financial-data-natively-analytics-ai-apps-agents"],
                        ["S&P Global unifies data intelligence", "https://www.databricks.com/customers/sp-global"],
                    ],
                ),
                uc(
                    "Data Entitlements",
                    "Licensing",
                    "identity",
                    "Metering exactly which subscriber consumed which feed and republishing usage into billing, so market-data revenue is accurate and reporting to licensees is defensible.",
                    problem="Usage is reconstructed from delivery logs weeks after the fact, so under-reporting and over-entitlement go undetected and market-data revenue leaks between the feed and the invoice.",
                    who="Data Business",
                    how="Delivery and access events are conformed against entitlements in Unity Catalog; consumption is metered to Gold, reconciled against Market Data Billing and written back through Entitlement Writeback.",
                    comps=["Entitlement Writeback", "Unity Catalog", "Subscriber APIs", "AI/BI", "Market Data Billing"],
                    stories=[
                        ["Governing B-PIPE entitlements on Databricks (industry solution)", "https://github.com/databricks-industry-solutions/bpipe-spark"],
                    ],
                ),
                uc(
                    "Corporate Actions",
                    "Reference",
                    "cdc",
                    "Ingesting and normalising dividends, splits, mergers and re-organisations and applying them to instruments and index constituents so downstream products stay correct.",
                    problem="Corporate actions arrive from many sources in incompatible formats and must be applied point-in-time; a missed split or wrong ex-date silently corrupts prices, indices and client feeds.",
                    who="Data Business",
                    how="SIX and vendor corporate-actions feeds are ingested with Lakeflow and versioned as slowly-changing records in Delta Lake, applied to instruments under Unity Catalog lineage so history is replayable.",
                    comps=["SIX Reference Data", "Bloomberg FIGI", "Lakeflow", "Delta Lake", "Unity Catalog"],
                    stories=[
                        ["Investment management reference architecture", "https://www.databricks.com/resources/architectures/financial-services-investment-management-reference-architecture"],
                        ["Modernizing investment data platforms", "https://www.databricks.com/blog/2021/01/29/strategies-for-modernizing-investment-data-platforms.html"],
                    ],
                ),
                uc(
                    "Reference Data Master",
                    "Symbology",
                    "db",
                    "Mastering instruments, issuers and identifiers across FIGI, ISIN, LEI and internal symbols so every feed, index and report resolves to the same security.",
                    problem="Vendor, venue and internal symbologies disagree, so the same instrument appears under many keys and joins across feeds, indices and reports break in ways nobody can trace.",
                    who="Data Business",
                    how="FIGI, ISIN, LEI and vendor identifiers are conformed into one governed security master in Delta Lake, with Unity Catalog lineage so every product resolves to a single instrument.",
                    comps=["GLEIF LEI", "ANNA DSB ISIN/UPI", "Bloomberg FIGI", "Unity Catalog", "Delta Lake"],
                    stories=[
                        ["S&P Global unifies data intelligence", "https://www.databricks.com/customers/sp-global"],
                        ["Investment management reference architecture", "https://www.databricks.com/resources/architectures/financial-services-investment-management-reference-architecture"],
                    ],
                ),
                uc(
                    "Clearing & Settlement",
                    "Post-trade",
                    "partner",
                    "Reconciling matched trades, cleared positions and margin across the CCP and settlement systems so fails and margin risk are seen intraday, not at settlement.",
                    problem="Cleared-position, margin and settlement records live in separate CCP and settlement systems reconciled in batch, so fails and margin shortfalls surface late when they are expensive to fix.",
                    who="Market Ops",
                    how="Matched trades, OCC and LCH margin and DTCC settlement feeds stream into the lakehouse; reconciliation runs continuously and fails and margin risk are surfaced to AI/BI intraday.",
                    comps=["OCC Clearing", "DTCC Settlement", "LCH / CCP", "Lakeflow", "AI/BI"],
                    stories=[
                        ["Investment management reference architecture", "https://www.databricks.com/resources/architectures/financial-services-investment-management-reference-architecture"],
                    ],
                ),
                uc(
                    "Regulatory Reporting",
                    "Reporting",
                    "gavel",
                    "Producing CAT, MiFID and transparency reports as the market operator from the same governed data the venue matches on, complete and on time.",
                    problem="Operator reporting is assembled from reconciled extracts under deadline, so late fixes and re-submissions are routine and proving completeness and lineage to the regulator is hard.",
                    who="Surveil & Reg",
                    how="Order, trade and reference data are conformed to Gold with Unity Catalog lineage; CAT and MiFID submissions are generated and filed from contracted products with a full audit trail via Genie.",
                    comps=["CAT / MiFID Reports", "Reg Submissions", "Unity Catalog", "Data Products", "Genie"],
                    stories=[
                        ["FINRA: predictive fraud detection at scale", "https://www.databricks.com/blog/2019/06/05/customer-spotlight-finra.html"],
                        ["Modernizing investment data platforms", "https://www.databricks.com/blog/2021/01/29/strategies-for-modernizing-investment-data-platforms.html"],
                    ],
                ),
            ],
        ),
        "sources": {
            "nasdaq-inet": {"t": "Nasdaq Marketplace Technology", "u": "https://www.nasdaq.com/solutions/marketplace-technology"},
            "t7": {"t": "Deutsche Börse T7 (Xetra/Eurex)", "u": "https://www.xetra.com/xetra-en/technology/t7"},
            "millennium": {"t": "LSEG MillenniumIT matching", "u": "https://en.wikipedia.org/wiki/MillenniumIT"},
            "globex": {"t": "CME Globex", "u": "https://www.cmegroup.com/globex.html"},
            "itch": {"t": "Nasdaq TotalView-ITCH", "u": "https://en.wikipedia.org/wiki/TotalView"},
            "opra": {"t": "OPRA options price reporting", "u": "https://www.opraplan.com/"},
            "sip": {"t": "CTA consolidated tape (SIP)", "u": "https://www.ctaplan.com/"},
            "rtds": {"t": "LSEG pricing & market data", "u": "https://www.lseg.com/en/data-analytics/financial-data/pricing-and-market-data"},
            "six": {"t": "SIX financial information", "u": "https://www.six-group.com/en/products-services/financial-information.html"},
            "dsb": {"t": "ANNA Derivatives Service Bureau", "u": "https://www.anna-dsb.com/"},
            "lei": {"t": "GLEIF Legal Entity Identifier", "u": "https://www.gleif.org/"},
            "figi": {"t": "OpenFIGI (Bloomberg symbology)", "u": "https://www.openfigi.com/"},
            "spdji": {"t": "S&P Dow Jones Indices", "u": "https://www.spglobal.com/spdji/en/"},
            "ftse": {"t": "FTSE Russell indices", "u": "https://www.lseg.com/en/ftse-russell/indices"},
            "msci": {"t": "MSCI Indexes", "u": "https://www.msci.com/indexes"},
            "solactive": {"t": "Solactive index engine", "u": "https://www.solactive.com/"},
            "smarts": {"t": "Nasdaq Trade Surveillance (SMARTS)", "u": "https://www.nasdaq.com/solutions/nasdaq-trade-surveillance"},
            "occ": {"t": "OCC options clearing", "u": "https://www.theocc.com/"},
            "lch": {"t": "LCH clearing", "u": "https://www.lch.com/"},
            "dtcc": {"t": "DTCC clearing and settlement", "u": "https://www.dtcc.com/"},
            "fix": {"t": "FIX Trading Community", "u": "https://www.fixtrading.org/"},
            "cat": {"t": "Consolidated Audit Trail (CAT)", "u": "https://www.catnmsplan.com/"},
            "mifid": {"t": "MiFID II (ESMA)", "u": "https://en.wikipedia.org/wiki/Markets_in_Financial_Instruments_Directive_2014"},
        },
    }
}
