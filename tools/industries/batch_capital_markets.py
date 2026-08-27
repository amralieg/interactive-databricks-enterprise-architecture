import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


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
                        ),
                        tile(
                            "BlackRock Aladdin",
                            "erp",
                            "Portfolio, order and risk platform holding positions, exposures and the book of record across the investment process.",
                            "aladdin",
                        ),
                        tile(
                            "Bloomberg AIM",
                            "market",
                            "Buy-side order and investment management, trade capture and compliance feeding executions and positions into the estate.",
                            "bloomberg-aim",
                        ),
                        tile(
                            "FlexTrade EMS",
                            "stream",
                            "Multi-asset execution management: smart order routing, algo wheels and venue connectivity, the source of the child-order and fill stream.",
                            "flextrade",
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
                        ),
                        tile(
                            "LSEG Refinitiv",
                            "market",
                            "Real-time and historical pricing, tick history, fundamentals and reference data feeding valuation and analytics.",
                            "refinitiv",
                        ),
                        tile(
                            "ICE Data Services",
                            "market",
                            "Evaluated pricing, reference data and end-of-day feeds for fixed income and cross-asset valuation.",
                            "ice-data",
                        ),
                        tile(
                            "Security Master",
                            "db",
                            "The golden instrument and issuer record: identifiers, terms and corporate actions every position and trade resolves against.",
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
                        ),
                        tile(
                            "Nasdaq Calypso",
                            "gauge",
                            "Capital-markets and treasury platform for derivatives pricing, collateral and risk on the sell side.",
                            "calypso",
                        ),
                        tile(
                            "MSCI Barra",
                            "chart",
                            "Multi-asset factor models and risk analytics: factor exposures, attribution and portfolio risk decomposition.",
                            "msci-barra",
                        ),
                        tile(
                            "Numerix",
                            "market",
                            "Derivatives pricing and analytics library for structured products, curves and Monte Carlo valuation.",
                            "numerix",
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
                        ),
                        tile(
                            "SWIFT Network",
                            "stream",
                            "Interbank messaging for settlement, confirmations and custody instructions across counterparties and agents.",
                            "swift",
                        ),
                        tile(
                            "FIX Gateways",
                            "api",
                            "The FIX order and execution message bus with venues, brokers and counterparties, the ground truth for orders and fills.",
                            "fix",
                        ),
                        tile(
                            "Custodian Feeds",
                            "db",
                            "Position, cash and settlement records from the custodian, reconciled against the internal book of record.",
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
                        ),
                        tile(
                            "MSCI ESG Ratings",
                            "gavel",
                            "ESG ratings, controversies and carbon metrics scored against issuers for sustainable-investing mandates.",
                            "msci-esg",
                        ),
                        tile(
                            "Sustainalytics",
                            "gavel",
                            "Morningstar Sustainalytics ESG risk ratings and controversy research joined to holdings for mandate screening.",
                            "sustainalytics",
                        ),
                        tile(
                            "Morningstar Direct",
                            "chart",
                            "Fund, index and managed-investment data with performance and holdings for cross-fund analysis and reporting.",
                            "morningstar",
                        ),
                    ],
                },
                fed_group(
                    "Investment BoR (IBOR)",
                    "Portfolio accounting and the investment book of record left where they are and queried in place under Unity Catalog, which avoids a second copy of the audited positions.",
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "FIX Protocol Feeds",
                        "stream",
                        "Streaming FIX order, execution and market-data sessions parsed on arrival and landed as structured events.",
                        "fix",
                    ),
                    tile(
                        "Market Data Bus",
                        "stream",
                        "Existing Kafka and multicast market-data topics carrying ticks, quotes and reference updates land here and are drawn generically on the reference board.",
                    ),
                    tile(
                        "Vendor Data APIs",
                        "api",
                        "Bloomberg, LSEG and FactSet request/response and file APIs consumed inbound through managed ELT connectors.",
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
                ]
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
