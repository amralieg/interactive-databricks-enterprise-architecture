import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_CRYPTO_DIGITAL_ASSETS = {
    "crypto_digital_assets": {
        "label": "Crypto & Digital Assets",
        "blurb": "Crypto exchanges, custodians and digital-asset firms: on-chain indexing, trading and matching, wallet custody, blockchain analytics and AML, market surveillance, and treasury and settlement.",
        "medallion": medallion(
            "Raw on-chain and trade feeds",
            "Node and RPC blocks, mempool and decoded contract events, exchange order and trade messages, wallet and custody transactions, market-data ticks and blockchain-analytics screening results, landed exactly as received in open Delta and Iceberg formats so any transfer or trade can be replayed as it stood, chain reorgs and all.",
            "Conformed wallet, asset, trade",
            "Wallets, addresses, tokens, customers and trades resolved into single conformed entities across the on-chain, exchange and custody estates, chain reorganisations reconciled, token contracts decoded, and internal accounts stitched to the on-chain addresses they control.",
            "Risk, liquidity, compliance",
            "Contracted products the trading, risk and compliance teams run on: real-time risk and counterparty exposure, order-book depth and liquidity, wallet and transaction risk scores, proof-of-reserves attestations, and regulator-ready AML and market-surveillance reporting.",
        ),
        "rails": {
            "src": [
                {
                    "box": "On-Chain & Nodes",
                    "ic": "network",
                    "tiles": [
                        tile(
                            "Alchemy Node RPC",
                            "network",
                            "Managed node and RPC access across Ethereum, Layer-2s and other chains, the source of block, transaction and log data without running the full node estate in-house.",
                            "alchemy",
                        ),
                        tile(
                            "Infura RPC",
                            "network",
                            "ConsenSys node infrastructure serving JSON-RPC and WebSocket access to Ethereum and IPFS, a common redundant path for on-chain reads and transaction broadcast.",
                            "infura",
                        ),
                        tile(
                            "The Graph Indexer",
                            "spark",
                            "Subgraph indexing of smart-contract events into queryable entities, the decoded, protocol-level view of DeFi and token activity across chains.",
                            "thegraph",
                        ),
                        tile(
                            "QuickNode Streams",
                            "stream",
                            "Low-latency node access and streaming of blocks, mempool and contract events, the real-time on-chain feed for trading and surveillance.",
                            "quicknode",
                        ),
                    ],
                },
                {
                    "box": "Trading & Market Data",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "AlphaPoint Exchange",
                            "market",
                            "Digital-asset exchange and matching-engine platform: order books, trade execution and inventory, the system of record for on-venue trading activity.",
                            "alphapoint",
                        ),
                        tile(
                            "Kaiko Market Data",
                            "market",
                            "Institutional crypto market data: trades, order books and reference rates across centralised and decentralised venues, the benchmark feed for liquidity and pricing analytics.",
                            "kaiko",
                        ),
                        tile(
                            "CoinGecko API",
                            "api",
                            "Broad price, volume and asset-metadata coverage across thousands of tokens and venues, used for market context and coverage checks.",
                            "coingecko",
                        ),
                        tile(
                            "CF Benchmarks",
                            "market",
                            "Regulated crypto reference rates and indices, including the underlying rates for listed crypto futures and ETFs, the reference against which marks and settlements are validated.",
                            "cfbenchmarks",
                        ),
                    ],
                },
                {
                    "box": "Custody & Wallets",
                    "ic": "key",
                    "tiles": [
                        tile(
                            "Fireblocks Custody",
                            "key",
                            "MPC-based wallet infrastructure and transfer policy engine: key shares, whitelists and signed withdrawals, the source of truth for custodied balances and movement.",
                            "fireblocks",
                        ),
                        tile(
                            "BitGo Custody",
                            "key",
                            "Qualified custody and multi-signature wallets with settlement and staking, the record of institutional holdings and their approval workflow.",
                            "bitgo",
                        ),
                        tile(
                            "Ledger Enterprise",
                            "key",
                            "Hardware-secured enterprise custody and key management, the governed device layer behind cold-storage balances and withdrawal ceremonies.",
                            "ledger",
                        ),
                        tile(
                            "Copper Custody",
                            "key",
                            "Custody, collateral and off-exchange settlement for institutions, the record of segregated holdings pledged against trading exposure.",
                            "copper",
                        ),
                    ],
                },
                {
                    "box": "Compliance & Analytics",
                    "ic": "zshield",
                    "tiles": [
                        tile(
                            "Chainalysis KYT",
                            "zshield",
                            "Know-Your-Transaction screening and address risk scoring across chains, the wallet and transaction risk signal every AML disposition is built on.",
                            "chainalysis",
                        ),
                        tile(
                            "Elliptic Analytics",
                            "zshield",
                            "Blockchain analytics and exposure tracing for digital-asset compliance, the source of wallet risk, exposure paths and illicit-activity indicators.",
                            "elliptic",
                        ),
                        tile(
                            "TRM Labs",
                            "globe",
                            "Blockchain intelligence for transaction monitoring, sanctions and investigation, a second risk feed enriched onto addresses and counterparties.",
                            "trm",
                        ),
                        tile(
                            "Notabene Travel Rule",
                            "gavel",
                            "FATF Travel Rule messaging: originator and beneficiary information exchanged with counterparty VASPs on qualifying transfers, the compliance layer over on-chain settlement.",
                            "notabene",
                        ),
                    ],
                },
                {
                    "box": "Ledger & Settlement",
                    "ic": "erp",
                    "tiles": [
                        tile(
                            "Core Ledger",
                            "db",
                            "The internal double-entry ledger of customer balances, fees and internal transfers, the accounting record every on-chain balance is reconciled against.",
                        ),
                        tile(
                            "Circle / USDC",
                            "product",
                            "Stablecoin issuance, minting and redemption flows, the fiat-backed settlement rail whose reserves and movements feed treasury and liquidity.",
                            "circle",
                        ),
                        tile(
                            "Fireblocks Network",
                            "partner",
                            "Off-exchange settlement and transfer network between counterparties, the record of institutional settlement instructions and confirmations.",
                            "fireblocks",
                        ),
                        tile(
                            "Fedwire / SWIFT",
                            "erp",
                            "Fiat banking rails for deposits, withdrawals and settlement with partner banks, reconciled against crypto movement for the full cash and coin position.",
                            "swift",
                        ),
                    ],
                },
                fed_group(
                    "Finance & Risk Marts",
                    "Finance, treasury and risk marts left in their existing warehouses and queried in place under Unity Catalog, so the audited books and risk exposures enrich analytics without a second copy of the numbers.",
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "Kafka Trade Events",
                        "eventbus",
                        "Exchange order, trade and account events carried on existing Kafka topics, consumed continuously into the lakehouse for near-real-time risk and surveillance.",
                        "kafka",
                    ),
                    tile(
                        "Node RPC Streams",
                        "stream",
                        "Block, mempool and decoded contract events streamed from node and indexer endpoints, landed as governed on-chain tables without bespoke per-chain plumbing.",
                    ),
                    tile(
                        "FIX Market Data",
                        "market",
                        "FIX and WebSocket market-data and execution feeds from venues and prime brokers, parsed on arrival and conformed to the same trade and quote entities.",
                        "fix",
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Exec & Finance",
                        "Genie One",
                        "The CEO on growth against regulatory cost and the trade between listings and risk; the CFO and treasury on liquidity, stablecoin reserves and fiat and crypto exposure; the Chief Risk Officer on counterparty, market and financial-crime risk across the book.",
                        [
                            ["Genie One", "Ask what the firm's exposure or yesterday's trading revenue was without booking analyst time."],
                            ["AI/BI", "Trading revenue, liquidity, reserves and risk exposure on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the business glossary, so \"exposure\" and \"reserves\" mean one thing across the firm."],
                        ],
                        sub=[
                            ["CEO", "growth, listings and the trade between volume and regulatory risk."],
                            ["CFO & Treasury", "liquidity, stablecoin reserves and fiat and crypto exposure."],
                            ["Chief Risk Officer", "counterparty, market and financial-crime risk across the book."],
                        ],
                        ucs=["Treasury & Settlement", "Market Analytics", "Customer 360"],
                    ),
                    biz(
                        "Trading Desk",
                        "AI/BI",
                        "Market makers and liquidity providers quoting across venues, trading operations watching order books and spreads, and the market-data team joining on-chain flow to exchange activity.",
                        [
                            ["Market Analytics", "Order-book depth, spreads and liquidity across venues on governed data."],
                            ["Lakehouse//RT", "Trade, quote and on-chain events at the latency a market moves at."],
                            ["AI/BI", "Volume, liquidity and PnL on the same definitions the executive team reads."],
                        ],
                        sub=[
                            ["Market makers", "quoting and inventory across trading pairs and venues."],
                            ["Trading operations", "order-book health, spreads and venue connectivity."],
                            ["Market data", "joining on-chain flow to exchange trades and reference rates."],
                        ],
                        ucs=["On-Chain Data Platform", "Market Analytics", "DeFi Analytics"],
                    ),
                    biz(
                        "Compliance & AML",
                        "Agent Bricks",
                        "The MLRO and financial-crime team screening wallets and transactions, sanctions and PEP analysts clearing alerts, and the Travel Rule team exchanging originator and beneficiary data with counterparty VASPs.",
                        [
                            ["Agent Bricks", "A compliance copilot that explains wallet risk and drafts report-ready narratives from governed on-chain evidence."],
                            ["AI Functions", "Alert triage and SAR narrative drafting run in SQL against governed transaction data."],
                            ["Unity Catalog", "Lineage and access controls so every screening decision is traceable for the examiner."],
                        ],
                        sub=[
                            ["MLRO & financial crime", "wallet and transaction screening and SAR filing."],
                            ["Sanctions & PEP", "alert clearing against sanctioned addresses and lists."],
                            ["Travel Rule", "originator and beneficiary exchange with counterparty VASPs."],
                        ],
                        ucs=["AML Wallet Screening", "Travel Rule Compliance", "Market Surveillance"],
                    ),
                    biz(
                        "Custody Ops",
                        "Lakehouse//RT",
                        "Custody operations reconciling on-chain balances to the ledger, wallet-security teams governing key ceremonies and withdrawal approvals, and the proof-of-reserves team attesting holdings to clients and auditors.",
                        [
                            ["Lakehouse//RT", "On-chain balances and withdrawal events reconciled at settlement speed."],
                            ["Custody Control", "Wallet balances, key operations and withdrawal approvals on one governed screen."],
                            ["Unity Catalog", "Governed, audited access to the balances proof-of-reserves is attested from."],
                        ],
                        sub=[
                            ["Custody operations", "balance reconciliation between chain and ledger."],
                            ["Wallet security", "key ceremonies, whitelists and withdrawal approvals."],
                            ["Proof of reserves", "attesting holdings to clients, auditors and regulators."],
                        ],
                        ucs=["Proof of Reserves", "AML Wallet Screening"],
                    ),
                    biz(
                        "Risk & Fraud",
                        "Model Serving",
                        "Real-time fraud and account-takeover teams scoring transactions inline, market-surveillance analysts detecting manipulation and wash trading, and credit-risk teams sizing counterparty and liquidation exposure.",
                        [
                            ["Model Serving", "Fraud, surveillance and risk models scored inside the transaction path in milliseconds."],
                            ["Feature Store", "Trade and wallet features defined once and read identically in training and serving."],
                            ["Lakehouse//RT", "Transaction and order events at the sub-second latency fraud moves at."],
                        ],
                        sub=[
                            ["Fraud & ATO", "real-time scoring of deposits, withdrawals and logins."],
                            ["Market surveillance", "manipulation, spoofing and wash-trading detection."],
                            ["Credit & liquidation", "counterparty and margin exposure across the book."],
                        ],
                        ucs=["Real-Time Fraud", "Market Surveillance", "Customer 360"],
                    ),
                ],
                [
                    biz(
                        "Blockchain Eng",
                        "Lakeflow",
                        "Run node clients and indexers across Bitcoin, Ethereum and Layer-2s, decode smart-contract and ERC-20 events, and land on-chain, mempool and exchange feeds through Auto Loader and Lakeflow into the medallion.",
                        [
                            ["Lakeflow Connect", "Managed connectors for exchange, market-data and SaaS sources."],
                            ["Auto Loader", "Incremental ingestion of node, mempool and market-data files as they land."],
                            ["Lakehouse//RT", "CEX, DEX and blockchain events streamed for near-real-time analytics."],
                        ],
                    ),
                    biz(
                        "Quant & ML",
                        "MLflow",
                        "Build fraud, market-surveillance, willingness-to-trade and liquidation-risk models on Kaiko and on-chain data, and check whether they still hold once market regimes shift.",
                        [
                            ["Feature Store", "Trade, wallet and order-book features shared across models."],
                            ["MLflow", "Every run tracked and evaluated for audit and reproduction."],
                            ["Model Serving", "Fraud, surveillance and pricing models scored in the operational path."],
                        ],
                    ),
                    biz(
                        "Platform Eng",
                        "Apps",
                        "Ship the surveillance, AML, custody and treasury applications the firm works in, backed by governed data and serverless Postgres, with agents drafting alerts and case narratives.",
                        [
                            ["Apps", "Trading, custody and compliance screens with no separate web tier to secure."],
                            ["Lakebase", "Serverless Postgres for case state, approvals and governed writes."],
                            ["Agent Bricks", "Agents that draft a SAR narrative or a surveillance case against governed tools."],
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
                                "Trading, risk and compliance dashboards against serverless SQL warehouses, with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and risk and surveillance alerts in the channel the desk already works in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Quant and analyst notebooks, VS Code and JetBrains against governed on-chain and market data and Genie Code.",
                            ),
                        ],
                    },
                    {
                        "box": "Client & Partner APIs",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "Institutional Data API",
                                "api",
                                "Curated market, on-chain and risk data served to institutional clients and prime-brokerage partners through governed API endpoints.",
                            ),
                            tile(
                                "Market Data Sharing",
                                "share",
                                "Enriched trade, order-book and on-chain datasets shared with funds and partners over Open Sharing rather than copied file exports.",
                            ),
                            tile(
                                "Client Portals",
                                "apps",
                                "Institutional client dashboards for balances, statements and risk built on Databricks Apps over governed data.",
                            ),
                        ],
                    },
                    {
                        "box": "Ops Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "Risk Limits Writeback",
                                "gauge",
                                "Position limits and circuit-breaker decisions written back into the matching and risk engines so the answer reaches the trading path.",
                            ),
                            tile(
                                "Custody Writeback",
                                "key",
                                "Freeze, whitelist and withdrawal-hold decisions pushed back to Fireblocks and custody so a risk call is enforced where funds move.",
                                "fireblocks",
                            ),
                            tile(
                                "Ledger Postings",
                                "db",
                                "Reconciled settlement and fee postings written to the core ledger in the system finance already closes the books in.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "SAR & Regulatory",
                                "gavel",
                                "Suspicious Activity Reports and regulator filings produced from the same governed tables the compliance team investigates on.",
                            ),
                            tile(
                                "Travel Rule Msgs",
                                "share",
                                "Originator and beneficiary messages exchanged with counterparty VASPs through Notabene from governed transfer records.",
                                "notabene",
                            ),
                            tile(
                                "PoR Attestations",
                                "docs",
                                "Proof-of-reserves and MiCA-style disclosures produced from reconciled on-chain and ledger balances for clients and auditors.",
                            ),
                        ],
                    },
                    {
                        "box": "Data Products",
                        "ic": "product",
                        "tiles": [
                            tile(
                                "Data Products",
                                "product",
                                "Published, contracted market, on-chain and risk products discoverable in Unity Catalog Domains and shared over Open Sharing.",
                            ),
                            tile(
                                "Sharing Recipients",
                                "share",
                                "Funds, regulators and partner venues reading live governed tables with no copy and no egress duplication.",
                            ),
                            tile(
                                "On-Chain Data Sets",
                                "network",
                                "Decoded, enriched on-chain datasets monetised to the wider ecosystem as governed, contracted products.",
                            ),
                        ],
                    },
                ]
            ),
        },
        "top": top_band(
            [
                app(
                    "Surveillance Desk",
                    "Market abuse",
                    "gauge",
                    "The screen a surveillance analyst runs the market from: spoofing, wash-trading and cross-venue manipulation alerts with full order-book and on-chain context, on Databricks Apps over Lakebase.",
                ),
                app(
                    "AML Case Manager",
                    "Wallet risk & SAR",
                    "gavel",
                    "Where compliance analysts triage wallet and transaction alerts, trace exposure paths and draft neutral, report-ready SAR narratives with an Agent Bricks copilot, every step traced for the examiner.",
                ),
                app(
                    "Custody Control",
                    "Balances & keys",
                    "key",
                    "Wallet balances, key operations and withdrawal approvals reconciled to the ledger on one governed screen, with proof-of-reserves attestations produced from the same numbers.",
                ),
                app(
                    "Treasury Cockpit",
                    "Liquidity & exposure",
                    "market",
                    "Fiat and crypto liquidity, stablecoin reserves and settlement exposure across venues, banks and custodians in near real time, so treasury moves funds before a shortfall.",
                ),
            ],
            [
                uc(
                    "On-Chain Data Platform",
                    "Data foundation",
                    "network",
                    "Ingesting and decoding block, mempool and smart-contract data across chains into governed tables, joined to exchange and off-chain data as one queryable estate.",
                    problem="On-chain data is high-volume, deeply nested and forever changing across chains and Layer-2s; teams rebuild brittle indexers per chain and still cannot join it to exchange or customer data.",
                    who="Trading Desk",
                    how="Node, mempool and market-data feeds land through Auto Loader and Lakeflow into a Bronze-to-Gold medallion; decoded events are conformed in Delta Lake and streamed in Lakehouse//RT for near-real-time analytics.",
                    comps=["Alchemy Node RPC", "Lakeflow", "Auto Loader", "Delta Lake", "Lakehouse//RT"],
                    stories=[
                        ["The boom of SOON: near-real-time data at Coinbase", "https://www.databricks.com/customers/coinbase/streaming"],
                        ["Streaming CEX, DEX and blockchain events for Web3 analytics", "https://community.databricks.com/t5/technical-blog/streaming-cex-dex-and-blockchain-events-in-databricks-for-web3/ba-p/120503"],
                    ],
                ),
                uc(
                    "Real-Time Fraud",
                    "Fraud & ATO",
                    "gauge",
                    "Scoring deposits, withdrawals and logins inline for fraud and account takeover, with sub-second features computed on live transaction data.",
                    problem="Crypto fraud and account takeover move in seconds and are irreversible once a withdrawal confirms; microbatch feature pipelines add latency that costs accuracy and money.",
                    who="Risk & Fraud",
                    how="Transaction and login events stream into Lakehouse//RT; features from Feature Store are scored through Model Serving in milliseconds behind the withdrawal path.",
                    comps=["Model Serving", "Feature Store", "Lakehouse//RT", "Kafka Trade Events", "Delta Lake"],
                    stories=[
                        ["Real-time fraud detection at Coinbase", "https://www.databricks.com/customers/coinbase/lakeflow"],
                        ["Ultra-fast anomaly detection on Ethereum with Spark Real-Time Mode", "https://www.databricks.com/blog/ultra-fast-anomaly-detection-using-apache-spark-real-time-mode"],
                    ],
                ),
                uc(
                    "AML Wallet Screening",
                    "Financial crime",
                    "zshield",
                    "Screening wallets and transactions against blockchain-analytics risk, tracing exposure paths, and drafting report-ready narratives for compliance analysts.",
                    problem="Analysts manually stitch Chainalysis and Elliptic screening to internal history, and every high-risk disposition and SAR is drafted by hand under regulatory scrutiny.",
                    who="Compliance & AML",
                    how="Screening results and on-chain evidence are conformed in the lakehouse; an Agent Bricks copilot explains wallet risk and drafts neutral narratives, traced and evaluated in MLflow, from the AML Case Manager.",
                    comps=["Agent Bricks", "AML Case Manager", "Chainalysis KYT", "Elliptic Analytics", "MLflow"],
                    stories=[
                        ["Elliptic: protect crypto assets with governed AI", "https://www.databricks.com/customers/elliptic"],
                        ["Modern BSA/AML compliance on Databricks", "https://www.databricks.com/blog/modern-bsaaml-compliance-databricks"],
                    ],
                ),
                uc(
                    "Travel Rule Compliance",
                    "VASP data",
                    "gavel",
                    "Exchanging originator and beneficiary information with counterparty VASPs on qualifying transfers, matched to on-chain settlement and screening.",
                    problem="The FATF Travel Rule forces VASPs to exchange originator and beneficiary data on transfers, but that data lives apart from the on-chain settlement and screening it must be reconciled against.",
                    who="Compliance & AML",
                    how="Notabene Travel Rule messages are joined to on-chain transfers and screening results in the lakehouse; matches and exceptions are governed in Unity Catalog and worked from the AML Case Manager.",
                    comps=["Notabene Travel Rule", "AML Case Manager", "Unity Catalog", "AI Functions", "Delta Lake"],
                    stories=[
                        ["AML solutions at scale with Databricks", "https://www.databricks.com/blog/2021/07/16/aml-solutions-at-scale-using-databricks-lakehouse-platform.html"],
                    ],
                ),
                uc(
                    "Market Surveillance",
                    "Manipulation",
                    "observ",
                    "Detecting spoofing, wash trading and cross-venue manipulation from order-book, trade and on-chain flow, and building the case an investigator can defend.",
                    problem="Manipulation hides across order books, venues and wallets; rule-only surveillance floods analysts with false positives and misses the coordinated, cross-venue patterns that matter.",
                    who="Risk & Fraud",
                    how="Order-book, trade and on-chain events are conformed in Lakehouse//RT; behaviour models in Model Serving score manipulation patterns surfaced with full context on the Surveillance Desk.",
                    comps=["Surveillance Desk", "Model Serving", "Lakehouse//RT", "Kaiko Market Data", "AI/BI"],
                    stories=[
                        ["Ultra-fast anomaly detection on blockchain data with Real-Time Mode", "https://www.databricks.com/blog/ultra-fast-anomaly-detection-using-apache-spark-real-time-mode"],
                    ],
                ),
                uc(
                    "Market Analytics",
                    "Liquidity & books",
                    "market",
                    "Order-book depth, spreads, liquidity and reference rates across venues and pairs, from multi-terabyte tick history queryable at low cost.",
                    problem="Order-book and tick data arrives from a dozen venues at multi-terabyte scale; teams cannot ingest, join and query it fast enough to run liquidity and pricing analytics.",
                    who="Trading Desk",
                    how="Tick and order-book data from Kaiko and exchange feeds land through Auto Loader into Delta Lake, partitioned and Z-ordered, and queried at scale on SQL Warehouses with AI/BI.",
                    comps=["Kaiko Market Data", "Auto Loader", "Delta Lake", "SQL Warehouses", "AI/BI"],
                    stories=[
                        ["How Gemini built a cryptocurrency analytics platform on the lakehouse", "https://www.databricks.com/blog/2022/02/15/how-gemini-built-a-cryptocurrency-analytics-platform-using-lakehouse-for-financial-services.html"],
                        ["Delta Sharing with Nasdaq's digital assets market data", "https://www.databricks.com/blog/using-delta-sharing-accelerate-insights-nasdaqs-digital-assets-market-data"],
                    ],
                ),
                uc(
                    "Proof of Reserves",
                    "Custody assurance",
                    "key",
                    "Reconciling on-chain wallet balances to the internal ledger and attesting holdings to clients, auditors and regulators from governed data.",
                    problem="After exchange collapses, clients and regulators demand provable reserves, but on-chain balances and the internal ledger live in separate systems reconciled by hand.",
                    who="Custody Ops",
                    how="On-chain balances from custody wallets and Core Ledger postings are reconciled in Lakehouse//RT; the Custody Control app produces governed, audited proof-of-reserves attestations.",
                    comps=["Custody Control", "Fireblocks Custody", "Core Ledger", "Lakehouse//RT", "Unity Catalog"],
                ),
                uc(
                    "Treasury & Settlement",
                    "Liquidity",
                    "db",
                    "Managing fiat and crypto liquidity, stablecoin reserves and settlement exposure across venues, banks and custodians in near real time.",
                    problem="Liquidity and settlement exposure sit across exchanges, banks, stablecoins and custodians; treasury sees it too late to move funds before a shortfall or a stuck settlement.",
                    who="Exec & Finance",
                    how="Ledger, custody and settlement feeds are conformed to Gold; exposure and liquidity are surfaced in the Treasury Cockpit with Genie and AI/BI on certified Metric Views.",
                    comps=["Treasury Cockpit", "Circle / USDC", "Core Ledger", "Genie", "AI/BI"],
                ),
                uc(
                    "DeFi Analytics",
                    "On-chain protocols",
                    "spark",
                    "Tracking TVL, liquidity-pool flows, lending positions and wallet behaviour across DeFi protocols, correlated to centralised-exchange activity.",
                    problem="DeFi activity spans protocols, pools and Layer-2s with no common schema; correlating it to exchange flow for trading and risk means decoding raw contract events chain by chain.",
                    who="Trading Desk",
                    how="Decoded DeFi and DEX events land in Delta Lake and are conformed to Silver; wallet-behaviour features feed Model Serving and are explored in AI/BI alongside CEX flow.",
                    comps=["The Graph Indexer", "Delta Lake", "Feature Store", "Model Serving", "AI/BI"],
                    stories=[
                        ["Streaming CEX, DEX and blockchain events for Web3 trading analytics", "https://community.databricks.com/t5/technical-blog/streaming-cex-dex-and-blockchain-events-in-databricks-for-web3/ba-p/120503"],
                    ],
                ),
                uc(
                    "Customer 360",
                    "Personalization",
                    "custlake",
                    "Resolving identity across on-chain wallets, exchange accounts and products to power personalization, retention and lifetime-value models, with fraud signals shared.",
                    problem="A customer's wallets, accounts and product activity are scattered across services, so personalization, retention and risk each rebuild a partial view and none is complete.",
                    who="Risk & Fraud",
                    how="Identity is resolved across wallets and accounts with CustomerLake and graph analytics; personalization and churn models in Model Serving are governed in Unity Catalog.",
                    comps=["CustomerLake", "Model Serving", "Unity Catalog", "Feature Store", "AI/BI"],
                    stories=[
                        ["Block redefines financial services with Unity Catalog", "https://www.databricks.com/customers/block/unity-catalog"],
                    ],
                ),
            ],
        ),
        "sources": {
            "alchemy": {"t": "Alchemy blockchain node infrastructure", "u": "https://www.alchemy.com/"},
            "infura": {"t": "Infura (ConsenSys) RPC", "u": "https://www.infura.io/"},
            "thegraph": {"t": "The Graph indexing protocol", "u": "https://thegraph.com/"},
            "quicknode": {"t": "QuickNode blockchain infrastructure", "u": "https://www.quicknode.com/"},
            "alphapoint": {"t": "AlphaPoint digital-asset exchange platform", "u": "https://alphapoint.com/"},
            "kaiko": {"t": "Kaiko crypto market data", "u": "https://www.kaiko.com/"},
            "coingecko": {"t": "CoinGecko API", "u": "https://www.coingecko.com/en/api"},
            "cfbenchmarks": {"t": "CF Benchmarks crypto reference rates", "u": "https://www.cfbenchmarks.com/"},
            "fireblocks": {"t": "Fireblocks custody and transfer network", "u": "https://www.fireblocks.com/"},
            "bitgo": {"t": "BitGo qualified custody", "u": "https://www.bitgo.com/"},
            "ledger": {"t": "Ledger Enterprise custody", "u": "https://www.ledger.com/enterprise"},
            "copper": {"t": "Copper custody and settlement", "u": "https://copper.co/"},
            "chainalysis": {"t": "Chainalysis KYT and blockchain intelligence", "u": "https://www.chainalysis.com/"},
            "elliptic": {"t": "Elliptic blockchain analytics", "u": "https://www.elliptic.co/"},
            "trm": {"t": "TRM Labs blockchain intelligence", "u": "https://www.trmlabs.com/"},
            "notabene": {"t": "Notabene FATF Travel Rule", "u": "https://notabene.id/"},
            "circle": {"t": "Circle USDC stablecoin", "u": "https://www.circle.com/usdc"},
            "swift": {"t": "SWIFT interbank messaging", "u": "https://en.wikipedia.org/wiki/SWIFT"},
            "kafka": {"t": "Apache Kafka", "u": "https://kafka.apache.org/"},
            "fix": {"t": "FIX Trading Community", "u": "https://www.fixtrading.org/"},
        },
    }
}
