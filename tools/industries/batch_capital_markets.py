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


INDUSTRIES_BATCH_CAPITAL_MARKETS = {
    "capital_markets": {
        "label": "Capital Markets",
        "blurb": "Buy-side and sell-side markets: order and execution management, market and reference data, market and credit risk, post-trade settlement, surveillance, and regulatory reporting.",
        "medallion": medallion(
            "Raw trade and market feeds",
            "FIX order and execution messages, Bloomberg and LSEG market-data ticks, position and risk extracts from Aladdin and Charles River, and DTCC confirms, landed exactly as received so a fill or a price can always be replayed as it stood.",
            "Conformed trades, positions, instruments",
            "Orders, executions, positions and instruments resolved into single conformed entities across the OMS, risk and custody estates, with the security master and legal-entity identifiers reconciled and trades stitched to one lifecycle.",
            "P&L, risk, TCA, exposure",
            "Contracted products the desk, risk and compliance teams run on: P&L and attribution by book, VaR and exposure by factor and counterparty, transaction cost against benchmark, and regulatory positions.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Order & Execution",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "Charles River IMS",
                            "market",
                            "State Street's investment management system: orders, allocations, compliance rules and positions, the buy-side system of record for the order lifecycle.",
                            "charles-river",
                            cat="Investment Management System (OMS)",
                            what="State Street's buy-side investment and order management system: the system of record for the order lifecycle, allocations, compliance rules and positions.",
                            users="Portfolio managers, buy-side traders and investment operations.",
                            data_out=data_out(
                                batch=flow(["structured"], "10-40 GB/day positions + orders", "End-of-day batch"),
                                stream=flow(["semi-structured"], "hundreds of order events/sec", "Continuous CDC (near real-time)")),
                        ),
                        tile(
                            "BlackRock Aladdin",
                            "erp",
                            "Portfolio, order and risk platform holding positions, exposures and the book of record across the investment process.",
                            "aladdin",
                            cat="Portfolio & Risk Management Platform",
                            what="Holds positions, exposures and the book of record across the investment process, combining portfolio management, order flow and risk in one platform.",
                            users="Portfolio managers, risk teams and investment operations.",
                            data_out=data_out(
                                batch=flow(["structured"], "20-80 GB/day positions + exposures", "Daily + intraday snapshots"),
                                stream=flow(["semi-structured"], "hundreds of position events/sec", "Continuous CDC")),
                        ),
                        tile(
                            "Bloomberg AIM",
                            "market",
                            "Buy-side order and investment management, trade capture and compliance feeding executions and positions into the estate.",
                            "bloomberg-aim",
                            cat="Buy-Side Order Management System",
                            what="Bloomberg's Asset & Investment Manager: buy-side order and investment management, trade capture and compliance feeding executions and positions into the estate.",
                            users="Buy-side traders, portfolio managers and compliance.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-20 GB/day positions", "End-of-day batch"),
                                stream=flow(["semi-structured"], "hundreds of order/execution events/sec", "Continuous CDC")),
                        ),
                        tile(
                            "FlexTrade EMS",
                            "stream",
                            "Multi-asset execution management: smart order routing, algo wheels and venue connectivity, the source of the child-order and fill stream.",
                            "flextrade",
                            cat="Execution Management System (EMS)",
                            what="Multi-asset execution management with smart order routing, algo wheels and venue connectivity, the source of the child-order and fill stream.",
                            users="Execution traders and desk heads.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "1-10k child orders + fills/sec at peak", "Continuous (sub-second)")),
                        ),
                    ],
                },
                {
                    "box": "Market & Reference Data",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "Bloomberg B-PIPE",
                            "market",
                            "Consolidated real-time market-data feed: prices, quotes and corporate actions across venues and asset classes.",
                            "bloomberg-bpipe",
                            cat="Consolidated Market Data Feed",
                            what="Bloomberg's consolidated real-time market-data feed carrying prices, quotes and corporate actions across venues and asset classes.",
                            users="Trading desks, quant research and market-data engineering.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "50k-500k ticks/sec at peak", "Continuous streaming")),
                        ),
                        tile(
                            "LSEG Refinitiv",
                            "market",
                            "Real-time and historical pricing, tick history, fundamentals and reference data feeding valuation and analytics.",
                            "refinitiv",
                            cat="Market Data & Analytics Platform",
                            what="Real-time and historical pricing, tick history, fundamentals and reference data feeding valuation and analytics.",
                            users="Trading desks, quant research and valuation teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "TB-scale tick history", "Daily history loads"),
                                stream=flow(["semi-structured"], "10k-100k ticks/sec", "Continuous streaming")),
                        ),
                        tile(
                            "ICE Data Services",
                            "market",
                            "Evaluated pricing, reference data and end-of-day feeds for fixed income and cross-asset valuation.",
                            "ice-data",
                            cat="Evaluated Pricing & Reference Data",
                            what="Evaluated pricing, reference data and end-of-day feeds for fixed income and cross-asset valuation.",
                            users="Valuation, fixed-income desks and risk teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-20 GB/day evaluated prices", "End-of-day + intraday snaps")),
                        ),
                        tile(
                            "Security Master",
                            "db",
                            "The golden instrument and issuer record: identifiers, terms and corporate actions every position and trade resolves against.",
                            cat="Security Master / Reference Data",
                            what="The golden instrument and issuer record holding identifiers, terms and corporate actions that every position and trade resolves against.",
                            users="Reference-data engineers, operations and every downstream desk.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of reference + corporate actions", "Daily refresh + intraday updates")),
                        ),
                    ],
                },
                {
                    "box": "Risk & Pricing",
                    "ic": "gauge",
                    "tiles": [
                        tile(
                            "Murex MX.3",
                            "gauge",
                            "Cross-asset trading, valuation and risk platform: pricing, sensitivities and limit state for the trading book.",
                            "murex",
                            cat="Cross-Asset Trading & Risk Platform",
                            what="Cross-asset trading, valuation and risk platform providing pricing, sensitivities and limit state for the trading book.",
                            users="Market risk, the trading desk and product control.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-20 GB/day positions + sensitivities", "Daily + scenario runs")),
                        ),
                        tile(
                            "Nasdaq Calypso",
                            "gauge",
                            "Capital-markets and treasury platform for derivatives pricing, collateral and risk on the sell side.",
                            "calypso",
                            cat="Capital Markets Trading & Risk Platform",
                            what="Capital-markets and treasury platform for derivatives pricing, collateral and risk on the sell side.",
                            users="Sell-side trading, collateral management and risk.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-15 GB/day valuations + collateral", "Daily + intraday runs"),
                                stream=flow(["semi-structured"], "tens of trade events/sec", "Continuous CDC")),
                        ),
                        tile(
                            "MSCI Barra",
                            "chart",
                            "Multi-asset factor models and risk analytics: factor exposures, attribution and portfolio risk decomposition.",
                            "msci-barra",
                            cat="Factor Risk Model Library",
                            what="Multi-asset factor models and risk analytics: factor exposures, attribution and portfolio risk decomposition.",
                            users="Quant research, risk and portfolio managers.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of factor exposures + models", "Daily / monthly refresh")),
                        ),
                        tile(
                            "Numerix",
                            "market",
                            "Derivatives pricing and analytics library for structured products, curves and Monte Carlo valuation.",
                            "numerix",
                            cat="Derivatives Pricing & Analytics Library",
                            what="Derivatives pricing and analytics library for structured products, curves and Monte Carlo valuation.",
                            users="Quant developers, structuring and valuation teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of curves + valuations", "On demand + end-of-day")),
                        ),
                    ],
                },
                {
                    "box": "Post-Trade & Custody",
                    "ic": "partner",
                    "tiles": [
                        tile(
                            "DTCC",
                            "partner",
                            "Central clearing, settlement and trade-confirmation infrastructure: matched trades, affirmations and settlement status.",
                            "dtcc",
                            cat="Clearing & Settlement Utility",
                            what="Central clearing, settlement and trade-confirmation infrastructure carrying matched trades, affirmations and settlement status.",
                            users="Post-trade operations, settlements and clearing teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-25 GB/day confirms + settlement", "Multiple settlement cycles daily"),
                                stream=flow(["semi-structured"], "tens of status events/sec", "Continuous status flow")),
                        ),
                        tile(
                            "SWIFT Network",
                            "stream",
                            "Interbank messaging for settlement, confirmations and custody instructions across counterparties and agents.",
                            "swift",
                            cat="Interbank Messaging Network",
                            what="Interbank messaging for settlement, confirmations and custody instructions across counterparties and agents.",
                            users="Settlements, custody operations and treasury.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "tens-hundreds of messages/sec", "Continuous message flow")),
                        ),
                        tile(
                            "FIX Gateways",
                            "api",
                            "The FIX order and execution message bus with venues, brokers and counterparties, the ground truth for orders and fills.",
                            "fix",
                            cat="Order Routing Protocol Gateway",
                            what="The FIX order and execution message bus with venues, brokers and counterparties, the ground truth for orders and fills.",
                            users="Execution traders, desk operations and market-data engineering.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "1-10k order/exec messages/sec at peak", "Continuous (sub-second)")),
                        ),
                        tile(
                            "Custodian Feeds",
                            "db",
                            "Position, cash and settlement records from the custodian, reconciled against the internal book of record.",
                            cat="Custodian Book of Record",
                            what="Position, cash and settlement records from the custodian, reconciled against the internal book of record.",
                            users="Investment operations, reconciliation and fund accounting.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-10 GB/day positions + cash", "Daily custodian files")),
                        ),
                    ],
                },
                {
                    "box": "Analytics & ESG Data",
                    "ic": "chart",
                    "tiles": [
                        tile(
                            "FactSet",
                            "chart",
                            "Fundamentals, estimates, ownership and analytics feeding research, screening and portfolio analysis.",
                            "factset",
                            cat="Financial Data & Analytics Platform",
                            what="Fundamentals, estimates, ownership and analytics feeding research, screening and portfolio analysis.",
                            users="Research analysts, quant research and portfolio managers.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-5 GB/day fundamentals + estimates", "Daily feed")),
                        ),
                        tile(
                            "MSCI ESG Ratings",
                            "gavel",
                            "ESG ratings, controversies and carbon metrics scored against issuers for sustainable-investing mandates.",
                            "msci-esg",
                            cat="ESG Ratings Provider",
                            what="ESG ratings, controversies and carbon metrics scored against issuers for sustainable-investing mandates.",
                            users="ESG research, portfolio managers and client reporting.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "GBs of ratings + controversies", "Monthly + on-demand")),
                        ),
                        tile(
                            "Sustainalytics",
                            "gavel",
                            "Morningstar Sustainalytics ESG risk ratings and controversy research joined to holdings for mandate screening.",
                            "sustainalytics",
                            cat="ESG Ratings Provider",
                            what="Morningstar Sustainalytics ESG risk ratings and controversy research joined to holdings for mandate screening.",
                            users="ESG research, compliance and portfolio managers.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs of ESG risk ratings", "Monthly refresh")),
                        ),
                        tile(
                            "Morningstar Direct",
                            "chart",
                            "Fund, index and managed-investment data with performance and holdings for cross-fund analysis and reporting.",
                            "morningstar",
                            cat="Investment Research & Data Platform",
                            what="Fund, index and managed-investment data with performance and holdings for cross-fund analysis and reporting.",
                            users="Research, product and client reporting teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-3 GB/day fund + holdings data", "Daily feed")),
                        ),
                    ],
                },
                fed_group(
                    "Investment BoR (IBOR)",
                    "Portfolio accounting and the investment book of record left where they are and queried in place under Unity Catalog, which avoids a second copy of the audited positions.",
                    cat="Investment Book of Record (IBOR)",
                    what="Portfolio accounting and the investment book of record kept in the incumbent system and queried in place, giving one audited view of positions and cash.",
                    users="Investment operations, fund accounting and finance.",
                    data_out=data_out(
                        batch=flow(["structured"], "TB-scale historical positions", "Queried on demand (federated)")),
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "FIX Protocol Feeds",
                        "stream",
                        "Streaming FIX order, execution and market-data sessions parsed on arrival and landed as structured events.",
                        "fix",
                        cat="FIX Messaging Feed",
                        what="Streaming FIX order, execution and market-data sessions parsed on arrival and landed as structured events.",
                        users="Market-data engineering and execution operations.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "1-10k messages/sec at peak", "Continuous (sub-second)")),
                    ),
                    tile(
                        "Market Data Bus",
                        "stream",
                        "Existing Kafka and multicast market-data topics carrying ticks, quotes and reference updates land here and are drawn generically on the reference board.",
                        cat="Streaming Market Data Bus",
                        what="Existing Kafka and multicast market-data topics carrying ticks, quotes and reference updates consumed into the lakehouse.",
                        users="Market-data engineering and quant research.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "50k-500k ticks/sec at peak", "Continuous streaming")),
                    ),
                    tile(
                        "Vendor Data APIs",
                        "api",
                        "Bloomberg, LSEG and FactSet request/response and file APIs consumed inbound through managed ELT connectors.",
                        cat="Market Data Vendor API",
                        what="Bloomberg, LSEG and FactSet request/response and file APIs consumed inbound through managed ELT connectors.",
                        users="Market-data engineering and research.",
                        data_out=data_out(
                            batch=flow(["structured", "semi-structured"], "1-5 GB/day", "Daily + on-demand pulls")),
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "CIO & Portfolio Mgmt",
                        "Genie One",
                        "The CIO on total portfolio return, allocation and tracking error against mandate; portfolio managers on positioning, attribution and rebalancing; the head of asset allocation on the strategic mix across asset classes and regions.",
                        [
                            ["Genie One", "Ask what a book returned, or what drove attribution last quarter, without waiting on an analyst."],
                            ["AI/BI", "Return, attribution, exposure and tracking error on one certified set of Metric Views."],
                            ["Unity Catalog", "One governed security master and glossary, so \"exposure\" and \"return\" mean one thing across the firm."],
                        ],
                        sub=[
                            ["CIO", "total portfolio return, allocation and tracking error against mandate."],
                            ["Portfolio managers", "positioning, attribution and rebalancing across books."],
                            ["Asset allocation", "the strategic mix across asset classes and regions."],
                        ],
                        ucs=["Portfolio Analytics", "ESG Analytics", "Investor Reporting"],
                    ),
                    biz(
                        "Trading Desks",
                        "Lakehouse//RT",
                        "Desk heads on execution quality, venue routing and desk P&L; equity and FICC traders working orders against liquidity; execution traders proving best execution and analysing transaction cost after the fill.",
                        [
                            ["Lakehouse//RT", "Order, execution and market state at the latency a desk actually trades at."],
                            ["Model Serving", "Execution and venue models scored inside the routing decision."],
                            ["AI/BI", "TCA, slippage and fill quality on the same definitions the desk defends."],
                        ],
                        sub=[
                            ["Desk heads", "execution quality, venue routing and desk P&L."],
                            ["Equity & FICC traders", "working orders against available liquidity."],
                            ["Execution traders", "best execution and post-trade transaction cost."],
                        ],
                        ucs=["TCA & Best Execution", "Post-Trade Recon", "Market & Credit Risk"],
                    ),
                    biz(
                        "Risk Management",
                        "AI/BI",
                        "The CRO and market risk on VaR, stress and limit usage across books; credit risk on counterparty and issuer exposure; liquidity risk on funding and margin under stress.",
                        [
                            ["AI/BI", "VaR, exposure and limit usage across every book on certified Metric Views."],
                            ["Model Serving", "Stress, VaR and counterparty models scored on demand rather than overnight."],
                            ["Unity Catalog", "Governed, auditable risk numbers with lineage from feed to report."],
                        ],
                        sub=[
                            ["Chief Risk Officer", "VaR, stress and limit usage across the firm."],
                            ["Market risk", "exposure and sensitivities by book and factor."],
                            ["Credit risk", "counterparty and issuer exposure under stress."],
                        ],
                        ucs=["Market & Credit Risk", "Regulatory Reporting", "Post-Trade Recon"],
                    ),
                    biz(
                        "Quant Research",
                        "MLflow",
                        "Quant researchers building and testing alpha signals; the portfolio construction team turning signals into positions under constraints; the alpha research team mining alternative data for edge before it decays.",
                        [
                            ["Feature Store", "Signals and factors defined once and read identically in research and production."],
                            ["MLflow", "Every backtest and model run tracked for audit and reproduction."],
                            ["Model Serving", "Signals and optimisation scored in the live investment path."],
                        ],
                        sub=[
                            ["Quant researchers", "alpha signals, factor models and regime detection."],
                            ["Portfolio construction", "turning signals into positions under constraints."],
                            ["Alpha research", "mining alternative data for edge before it decays."],
                        ],
                        ucs=["Quant Backtesting", "Alt-Data Alpha", "Portfolio Analytics"],
                    ),
                    biz(
                        "Compliance & Surveil",
                        "AI Functions",
                        "Trade surveillance analysts investigating manipulation and spoofing alerts; compliance officers on restricted lists and personal-account dealing; the regulatory reporting team filing MiFID II, CAT and transaction reports on time.",
                        [
                            ["AI Functions", "Communications and trade data screened for manipulation patterns at scale."],
                            ["Genie One", "Investigators ask for a trader's activity around an event in plain language."],
                            ["Unity Catalog", "Audit trails and lineage that satisfy a regulatory examination."],
                        ],
                        sub=[
                            ["Surveillance", "manipulation, spoofing and wash-trade investigations."],
                            ["Compliance officers", "restricted lists and personal-account dealing."],
                            ["Regulatory reporting", "MiFID II, CAT and transaction reporting on time."],
                        ],
                        ucs=["Trade Surveillance", "Regulatory Reporting", "Investor Reporting"],
                    ),
                ],
                [
                    biz(
                        "Quant Developers",
                        "MLflow",
                        "Turn research notebooks in Python, R and kdb+/q into production signals and backtests, and own the libraries the desk and PMs run against.",
                        [
                            ["Notebooks & IDEs", "Python, R and VS Code against governed tick and reference data."],
                            ["MLflow", "Backtests and models versioned, tracked and reproducible for audit."],
                            ["Feature Store", "Factor and signal libraries shared across research and production."],
                        ],
                        sub=[
                            ["Signal Developers", "research notebooks turned into production signals the desk trades on."],
                            ["Backtest Engineers", "reproducible backtests and versioned models for audit."],
                            ["Quant Library Owners", "the factor and pricing libraries PMs and the desk run against."],
                        ],
                    ),
                    biz(
                        "Market Data Engineers",
                        "Lakeflow",
                        "Land Bloomberg B-PIPE, LSEG and ICE feeds and FIX order flow, curate the security master, and keep tick and reference tables fresh for every desk.",
                        [
                            ["Lakeflow Connect", "Managed connectors for market-data, OMS and custody sources."],
                            ["Lakeflow Designer", "Declarative pipelines with expectations on price and reference feeds."],
                            ["Lakewatch", "Freshness on the tick and reference tables the desks open at the bell."],
                        ],
                        sub=[
                            ["Ingestion Engineers", "Bloomberg, LSEG and ICE feeds and FIX order flow landed on time."],
                            ["Pipeline Engineers", "Bronze-to-Silver conforming and expectations on price and reference feeds."],
                            ["Platform Reliability", "freshness of the tick and reference tables the desks open at the bell."],
                        ],
                    ),
                    biz(
                        "Risk Systems Engineers",
                        "Model Serving",
                        "Wire Murex and Nasdaq Calypso valuations, Monte Carlo VaR and stress engines into governed pipelines so risk numbers are timely, explainable and reproducible.",
                        [
                            ["Model Serving", "VaR, stress and pricing models scored on demand at book scale."],
                            ["Apache Spark", "Distributed Monte Carlo and revaluation across the full position set."],
                            ["Unity Catalog", "Lineage from raw feed to reported risk number for the regulator."],
                        ],
                        sub=[
                            ["Risk Platform Engineers", "pricing and valuation engines wired into governed pipelines."],
                            ["Compute Engineers", "distributed Monte Carlo VaR and revaluation across the full position set."],
                            ["Model Ops", "risk numbers timely, explainable and reproducible for the regulator."],
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
                                "Genie in Teams for governed answers, and risk and surveillance alerts in the channel desks already work in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Notebooks, VS Code and JetBrains against governed data and Genie Code.",
                            ),
                        ],
                    },
                    {
                        "box": "Distribution & Partners",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "Delta Sharing to LPs",
                                "share",
                                "Fund performance and holdings shared to limited partners and allocators over Delta Sharing rather than file exchange.",
                            ),
                            tile(
                                "Prime Brokers",
                                "partner",
                                "Positions, margin and financing state exchanged with prime brokers and counterparties on live tables.",
                            ),
                            tile(
                                "Data Marketplace",
                                "market",
                                "Curated market and reference datasets consumed and published through Databricks Marketplace.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "OMS / EMS Writeback",
                                "db",
                                "Target positions, orders and restrictions written back into Charles River and Aladdin so the decision reaches the trading path.",
                            ),
                            tile(
                                "Risk Limit Writeback",
                                "gauge",
                                "Updated limits and exposure flags pushed back into the risk and OMS systems the desk trades against.",
                            ),
                            tile(
                                "Alert & Case Queue",
                                "gavel",
                                "Surveillance alerts and cases pushed to the investigation queue analysts already work.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "MiFID II / CAT Filings",
                                "gavel",
                                "Transaction and order-event reporting to the regulator produced from the same governed tables the firm trades on.",
                                ["mifid2", "cat"],
                            ),
                            tile(
                                "Regulatory Reporting",
                                "share",
                                "EMIR, SFTR and prudential submissions filed from contracted Gold products.",
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
                                "Allocators, administrators and partners reading live tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ],
                genie_spaces=[
                    genie("Portfolio & Performance", "Ask about returns, attribution and exposure across every book in plain language.",
                          feeds=["BlackRock Aladdin", "Security Master", "MSCI Barra", "Conformed trades, positions, instruments"],
                          teams=["CIO & Portfolio Mgmt", "Portfolio managers", "Quant Research"],
                          questions=[
                              "What did each book return last quarter, and what drove attribution?",
                              "What is our current factor exposure across the whole portfolio?",
                              "Which positions contribute most to tracking error against mandate?",
                              "How has allocation shifted across asset classes this year?",
                              "Which holdings breach a concentration or mandate limit?"]),
                    genie("Execution & TCA", "Explore slippage, venue performance and transaction cost against benchmark.",
                          feeds=["FIX Gateways", "FlexTrade EMS", "Bloomberg B-PIPE", "P&L, risk, TCA, exposure"],
                          teams=["Trading Desks", "Execution traders", "Desk heads"],
                          questions=[
                              "What was our implementation shortfall by desk this week?",
                              "Which venues delivered the best fill quality for large orders?",
                              "How does slippage compare against arrival-price benchmark by asset class?",
                              "Which algos are underperforming on market impact right now?",
                              "Where are we paying the most in spread by symbol?"]),
                    genie("Market & Credit Risk", "Ask about VaR, stress, sensitivities and counterparty exposure across books.",
                          feeds=["Murex MX.3", "Nasdaq Calypso", "MSCI Barra", "P&L, risk, TCA, exposure"],
                          teams=["Risk Management", "Chief Risk Officer", "Market risk"],
                          questions=[
                              "What is our firm-wide VaR today, and the trend this month?",
                              "How does the book behave under a rates +200bp stress scenario?",
                              "Which counterparties carry the largest exposure right now?",
                              "Which books are closest to a limit breach?",
                              "What are our largest factor sensitivities across the portfolio?"]),
                    genie("Trade Surveillance", "Investigate manipulation, spoofing and completeness across orders and trades.",
                          feeds=["FIX Gateways", "DTCC", "Conformed trades, positions, instruments"],
                          teams=["Compliance & Surveil", "Surveillance", "Regulatory reporting"],
                          questions=[
                              "Which traders showed spoofing-like order patterns this week?",
                              "What was a given trader's activity around this price move?",
                              "Which alert types have the worst false-positive rate?",
                              "How many surveillance cases are open past their SLA?",
                              "Is our order and trade data complete for the reporting period?"]),
                ],
                dashboards=[
                    dashboard("P&L & Attribution", "Return, attribution and exposure across every book on certified Metric Views.",
                              kpis=["Total return", "Attribution", "Tracking error", "Book P&L", "Exposure by factor"],
                              teams=["CIO & Portfolio Mgmt", "Trading Desks", "Portfolio managers"]),
                    dashboard("Firm Risk & Exposure", "VaR, stress, limit usage and counterparty exposure across the firm.",
                              kpis=["VaR", "Stress loss", "Limit utilization", "Counterparty exposure", "Sensitivities"],
                              teams=["Risk Management", "Chief Risk Officer", "Credit risk"]),
                    dashboard("Execution Quality (TCA)", "Slippage, venue performance and market impact against benchmark.",
                              kpis=["Implementation shortfall", "Slippage vs benchmark", "Venue fill rate", "Market impact", "Spread capture"],
                              teams=["Trading Desks", "Execution traders", "Desk heads"]),
                    dashboard("Surveillance & Regulatory", "Alert quality, case backlog and regulatory reporting timeliness.",
                              kpis=["Alert volume", "False-positive rate", "Case backlog", "Report timeliness", "Reporting completeness"],
                              teams=["Compliance & Surveil", "Surveillance", "Regulatory reporting"]),
                ],
            ),
        },
        "top": top_band(
            [
                app(
                    "TCA Workbench",
                    "Execution quality",
                    "market",
                    "Where execution traders see slippage, venue performance and cost against benchmark before and after every fill, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Risk Cockpit",
                    "Firm-wide exposure",
                    "gauge",
                    "VaR, stress and limit usage across every book on one screen, re-run intraday instead of waiting for the overnight batch.",
                ),
                app(
                    "Surveillance Console",
                    "Market abuse alerts",
                    "gavel",
                    "Manipulation, spoofing and wash-trade alerts triaged with the trader's full order and comms context in one investigation view.",
                ),
                app(
                    "Quant Research Lab",
                    "Backtesting",
                    "notebook",
                    "Where quants build, backtest and promote signals from notebook to monitored pipeline against governed tick and factor data.",
                ),
            ],
            [
                uc(
                    "Quant Backtesting",
                    "Alpha research",
                    "notebook",
                    "Building, testing and promoting alpha signals against decades of tick, fundamental and alternative data, on the same platform that later runs them in production.",
                    problem="Backtests run on extracts that never match production data, and a promising signal decays before the research-to-production handoff finishes, so edge is lost in the plumbing.",
                    who="Quant Research",
                    how="Tick, fundamental and factor data are conformed in the lakehouse; signals are backtested in the Quant Research Lab and promoted from notebook to monitored pipeline through MLflow and Feature Store.",
                    comps=["Quant Research Lab", "MLflow", "Feature Store", "LSEG Refinitiv", "Apache Spark"],
                    stories=[
                        ["Jefferies modernizes equity research with agentic analytics", "https://www.databricks.com/blog/jefferies-modernizes-equity-research-scale-databricks-and-agentic-analytics"],
                        ["Investment management reference architecture", "https://www.databricks.com/resources/architectures/financial-services-investment-management-reference-architecture"],
                    ],
                ),
                uc(
                    "TCA & Best Execution",
                    "Execution",
                    "market",
                    "Measuring slippage, venue performance and market impact against benchmark so execution improves and best execution can be proven to clients and regulators.",
                    problem="Execution cost is measured in spreadsheets days after the fill, so venue and algo choices are never corrected while they still matter, and best execution is asserted rather than shown.",
                    who="Trading Desks",
                    how="FIX order and execution events are joined to market data in the lakehouse; slippage and venue analytics are computed to Gold and explored in the TCA Workbench on the desk's own definitions.",
                    comps=["TCA Workbench", "FIX Gateways", "Bloomberg B-PIPE", "AI/BI", "Lakehouse//RT"],
                    stories=[
                        ["Investment management reference architecture", "https://www.databricks.com/resources/architectures/financial-services-investment-management-reference-architecture"],
                    ],
                ),
                uc(
                    "Market & Credit Risk",
                    "Risk",
                    "gauge",
                    "VaR, stress, sensitivities and counterparty exposure across every book, re-run intraday instead of waiting for an overnight batch that is stale by the open.",
                    problem="Risk is aggregated overnight in engines that cannot be re-run intraday, so a shock is seen the next morning and limit breaches are explained after the loss.",
                    who="Risk Management",
                    how="Murex and Nasdaq Calypso valuations and position feeds are conformed to Gold; VaR, stress and counterparty models are scored in Model Serving and read in the Risk Cockpit and AI/BI.",
                    comps=["Risk Cockpit", "Murex MX.3", "Model Serving", "MSCI Barra", "AI/BI"],
                    stories=[
                        ["S&P Global unifies data intelligence", "https://www.databricks.com/customers/sp-global"],
                        ["MCP-powered financial AI workflows on Databricks", "https://www.databricks.com/blog/mcp-powered-financial-ai-workflows-databricks"],
                    ],
                ),
                uc(
                    "Trade Surveillance",
                    "Market abuse",
                    "gavel",
                    "Detecting spoofing, layering, wash trades and insider patterns across orders, executions and communications, with an audit trail a regulator will accept.",
                    problem="Surveillance runs across siloed vendor systems with gappy data, so alerts are noisy, investigations are slow, and completeness cannot be proven to an examiner.",
                    who="Compliance & Surveil",
                    how="Orders, executions and comms are unified in the lakehouse with Unity Catalog completeness checks; detectors and AI Functions score patterns and cases open in the Surveillance Console.",
                    comps=["Surveillance Console", "AI Functions", "Unity Catalog", "Model Serving", "Lakehouse//RT"],
                    stories=[
                        ["FINRA: predictive fraud detection at scale", "https://www.databricks.com/blog/2019/06/05/customer-spotlight-finra.html"],
                        ["Coinbase scales real-time security", "https://www.databricks.com/customers/coinbase/lakeflow"],
                    ],
                ),
                uc(
                    "Portfolio Analytics",
                    "Attribution",
                    "chart",
                    "Performance attribution, factor exposure and scenario analysis across the whole book on one governed set of positions, prices and benchmarks.",
                    problem="Attribution and exposure are stitched from custodian, OMS and vendor extracts that never agree, so the CIO and PMs argue about the numbers instead of the positions.",
                    who="CIO & Portfolio Mgmt",
                    how="Positions, prices and benchmarks are conformed against one security master; attribution and factor analytics are served to certified Metric Views the CIO and PMs read in AI/BI and Genie One.",
                    comps=["Security Master", "AI/BI", "Genie One", "BlackRock Aladdin", "MSCI Barra"],
                    stories=[
                        ["S&P Global unifies data intelligence", "https://www.databricks.com/customers/sp-global"],
                    ],
                ),
                uc(
                    "Alt-Data Alpha",
                    "Alternative data",
                    "aisvc",
                    "Turning satellite, card, web and sentiment data into signals mapped to portfolio exposures before the edge is arbitraged away.",
                    problem="Alternative datasets arrive in dozens of formats and decay fast, and by the time they are cleaned and joined to positions the alpha is already gone.",
                    who="Quant Research",
                    how="Alternative datasets are ingested and standardised in the lakehouse and joined to holdings; signals are engineered in Feature Store and mapped to exposures with Agent Bricks.",
                    comps=["Vendor Data APIs", "Feature Store", "Agent Bricks", "FactSet", "MLflow"],
                    stories=[
                        ["Jefferies modernizes equity research with agentic analytics", "https://www.databricks.com/blog/jefferies-modernizes-equity-research-scale-databricks-and-agentic-analytics"],
                        ["Nasdaq reinvents finance with Databricks", "https://www.databricks.com/customers/nasdaq"],
                    ],
                ),
                uc(
                    "Regulatory Reporting",
                    "Reporting",
                    "gavel",
                    "Producing MiFID II, CAT, EMIR and transaction reports from the same governed data the firm trades on, complete and on time.",
                    problem="Regulatory reports are assembled from reconciled extracts under deadline, so late fixes and re-submissions are routine and lineage back to the source is hard to prove.",
                    who="Compliance & Surveil",
                    how="Trade, order and reference data are conformed to Gold with Unity Catalog lineage; MiFID II and CAT submissions are generated and filed from contracted products with a full audit trail.",
                    comps=["Regulatory Reporting", "Unity Catalog", "MiFID II / CAT Filings", "DTCC", "FIX Gateways"],
                    stories=[
                        ["FINRA: predictive fraud detection at scale", "https://www.databricks.com/blog/2019/06/05/customer-spotlight-finra.html"],
                        ["Nasdaq reinvents finance with Databricks", "https://www.databricks.com/customers/nasdaq"],
                    ],
                ),
                uc(
                    "Post-Trade Recon",
                    "Post-trade",
                    "cdc",
                    "Reconciling fills, allocations and positions across OMS, custodian and clearing so breaks are caught at T+0 rather than discovered at settlement.",
                    problem="Fills, allocations and custody records are reconciled in batch, so breaks surface at settlement when they are expensive and slow to resolve.",
                    who="Trading Desks",
                    how="FIX fills, DTCC confirms and custodian feeds stream into the lakehouse; matching runs continuously and breaks are flagged against the investment book of record before settlement.",
                    comps=["FIX Gateways", "DTCC", "Custodian Feeds", "Investment BoR (IBOR)", "Lakeflow"],
                    stories=[
                        ["Investment management reference architecture", "https://www.databricks.com/resources/architectures/financial-services-investment-management-reference-architecture"],
                    ],
                ),
                uc(
                    "ESG Analytics",
                    "Sustainability",
                    "gavel",
                    "Scoring portfolios against ESG ratings, controversies and carbon data so mandates are met and reporting to allocators is defensible.",
                    problem="ESG ratings and carbon data come from many vendors on different taxonomies, so portfolio-level scores are inconsistent and hard to defend to allocators and regulators.",
                    who="CIO & Portfolio Mgmt",
                    how="MSCI, Sustainalytics and Morningstar ESG data are conformed against the security master and joined to holdings; portfolio ESG scores are served to AI/BI and client reporting.",
                    comps=["MSCI ESG Ratings", "Sustainalytics", "Security Master", "AI/BI", "Morningstar Direct"],
                    stories=[
                        ["S&P Global unifies data intelligence", "https://www.databricks.com/customers/sp-global"],
                    ],
                ),
                uc(
                    "Investor Reporting",
                    "Client reporting",
                    "share",
                    "Producing accurate, timely performance, holdings and risk reports for investors and allocators from one governed source instead of a reporting team's spreadsheets.",
                    problem="Investor reports are rebuilt each period from extracts and manual checks, so they are late, inconsistent between clients, and expensive to audit.",
                    who="CIO & Portfolio Mgmt",
                    how="Performance, holdings and risk are served from certified Gold products; statements and allocator packs are generated and shared over Delta Sharing and governed apps.",
                    comps=["Data Products", "Sharing Recipients", "AI/BI", "Investment BoR (IBOR)", "Genie One"],
                    stories=[
                        ["Nasdaq reinvents finance with Databricks", "https://www.databricks.com/customers/nasdaq"],
                        ["MCP-powered financial AI workflows on Databricks", "https://www.databricks.com/blog/mcp-powered-financial-ai-workflows-databricks"],
                    ],
                ),
            ],
        ),
        "sources": {
            "charles-river": {"t": "Charles River Development (State Street)", "u": "https://www.crd.com/"},
            "aladdin": {"t": "BlackRock Aladdin", "u": "https://www.blackrock.com/aladdin"},
            "bloomberg-aim": {"t": "Bloomberg AIM", "u": "https://www.bloomberg.com/professional/products/asset-management/"},
            "flextrade": {"t": "FlexTrade EMS", "u": "https://flextrade.com/"},
            "bloomberg-bpipe": {"t": "Bloomberg B-PIPE market data", "u": "https://www.bloomberg.com/professional/products/data/enterprise-catalog/market/"},
            "refinitiv": {"t": "LSEG Data & Analytics (Refinitiv)", "u": "https://www.lseg.com/en/data-analytics"},
            "ice-data": {"t": "ICE Data Services", "u": "https://www.ice.com/market-data"},
            "factset": {"t": "FactSet", "u": "https://www.factset.com/"},
            "murex": {"t": "Murex MX.3", "u": "https://www.murex.com/"},
            "calypso": {"t": "Nasdaq Calypso (Adenza)", "u": "https://www.nasdaq.com/solutions/fintech/nasdaq-calypso/middle-office-trading-risk"},
            "msci-barra": {"t": "MSCI Barra factor models", "u": "https://www.msci.com/our-solutions/analytics/multi-asset-class-factor-models"},
            "numerix": {"t": "Numerix analytics", "u": "https://www.numerix.com/"},
            "dtcc": {"t": "DTCC clearing and settlement", "u": "https://www.dtcc.com/"},
            "swift": {"t": "SWIFT messaging network", "u": "https://en.wikipedia.org/wiki/SWIFT"},
            "fix": {"t": "FIX Trading Community", "u": "https://www.fixtrading.org/"},
            "msci-esg": {"t": "MSCI ESG Ratings", "u": "https://www.msci.com/sustainable-investing/esg-ratings"},
            "sustainalytics": {"t": "Morningstar Sustainalytics", "u": "https://www.sustainalytics.com/"},
            "morningstar": {"t": "Morningstar Direct", "u": "https://www.morningstar.com/products/direct"},
            "mifid2": {"t": "MiFID II (ESMA)", "u": "https://en.wikipedia.org/wiki/Markets_in_Financial_Instruments_Directive_2014"},
            "cat": {"t": "Consolidated Audit Trail (CAT)", "u": "https://www.catnmsplan.com/"},
        },
    }
}
