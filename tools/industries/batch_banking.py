import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    """People rail with per-industry Technical roles (never common.TECH_PPL)."""
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_BANKING = {
    'banking': {
        "label": "Banking",
        "blurb": "Retail and commercial banking: core ledger, payments, lending, fraud, and regulatory reporting across branches and digital channels.",
        "medallion": medallion(
            "Raw core and channel logs",
            "Core banking postings, card authorizations, wire messages and CRM events landed exactly as received for audit replay.",
            "Conformed customers and accounts",
            "Customers, accounts, facilities and parties resolved into golden records across core, cards and channels.",
            "NIM, NPL, liquidity ratios",
            "Contracted products finance and risk run on: net interest margin, NPL ratio, LCR and customer profitability.",
        ),
        "rails": {
            "src": [
                {"box": "Core Banking", "ic": "erp", "tiles": [
                    tile("Temenos Transact", "erp", "Deposits, loans, GL and end-of-day across retail and commercial.", "temenos"),
                    tile("FIS Profile", "erp", "Account processing, interest accrual and regulatory extracts.", "fis-profile"),
                    tile("Finastra Fusion", "erp", "Lending origination, servicing and treasury interfaces.", "finastra"),
                ]},
                {"box": "Cards & Payments", "ic": "market", "tiles": [
                    tile("Visa DPS / Auth", "market", "Authorization, clearing and dispute messages.", "visa"),
                    tile("Mastercard Smart Data", "market", "Spend analytics and merchant category enrichment.", "mastercard"),
                    tile("SWIFT FIN Messages", "api", "Cross-border payment instructions and confirmations.", "swift"),
                ]},
                {"box": "Digital Channels", "ic": "apps", "tiles": [
                    tile("Temenos Infinity", "apps", "Mobile and web sessions, transfers and self-service events.", "temenos-infinity"),
                    tile("Salesforce FSC", "custlake", "Households, opportunities and service cases.", "sf-fsc"),
                    tile("NICE Actimize", "gavel", "AML alerts, cases and SAR workflow.", "actimize"),
                ]},
                {"box": "Risk & Finance", "ic": "chart", "tiles": [
                    tile("Moody's RiskCalc", "chart", "PD/LGD models and rating migrations for commercial names.", "moodys"),
                    tile("FIS Ambit Focus", "chart", "ALM, liquidity and interest rate risk measurement.", "fis-alm"),
                    tile("AxiomSL Reg Reporting", "gavel", "Basel, CCAR and local regulatory templates.", "axiomsl"),
                ]},
                {"box": "Open Banking", "ic": "api", "tiles": [
                    tile("Plaid Aggregation", "api", "External account verification and aggregation with consent.", "plaid"),
                    tile("Tink Open Banking", "partner", "AIS/PIS traffic and consent registry.", "tink"),
                ]},
                fed_group("Data Warehouse Mart", "Historical GL and risk marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("FICO Falcon", "gavel", "Card fraud scores and consortium intelligence.", "fico"),
                tile("LexisNexis Risk", "partner", "KYC, sanctions and adverse media screening.", "lexisnexis"),
                tile("Experian Bureau", "custlake", "Credit bureau pulls and attribute refreshes.", "experian"),
            ]),
            "ppl": ppl2([
                biz("Chief Credit Officer & CFO", "Genie One",
                    "The CEO on ROE and deposit growth; the CFO on net interest margin, cost-to-income and CET1 capital against NPL formation across the book.",
                    [["Genie One", "Ask what last quarter's NIM was by segment."], ["AI/BI", "Capital and liquidity on certified Metric Views."], ["Unity Catalog", "One customer definition across channels."]]),
                biz("Retail Banking", "AI/BI",
                    "Branch productivity, product penetration and attrition, judged on deposit and loan growth, household profitability and cross-sell.",
                    [["Branch Performance", "Household profitability by branch and RM."], ["AI/BI", "Deposit and loan growth on governed core data."]]),
                biz("Commercial Banking", "Model Serving",
                    "Relationship profitability, covenants and limit utilization, tracked on risk-adjusted return, exposure at default and rating migration.",
                    [["RM Workbench", "Exposure and cross-sell opportunities by relationship."], ["Model Serving", "Early warning models on commercial books."]]),
                biz("Risk & Compliance", "Lakehouse//RT",
                    "Credit, market and operational risk with regulatory reporting, run on PD/LGD, fraud loss rate and AML alert-to-SAR conversion.",
                    [["AML Investigator", "Alert prioritization and case narrative drafting."], ["Lakehouse//RT", "Fraud scores at authorization latency."]]),
                biz("Treasury & ALM", "AI/BI",
                    "Funding, liquidity buffers and hedge effectiveness, measured on LCR, NSFR and interest-rate gap under stress across the balance sheet.",
                    [["ALM Dashboard", "Gap and duration under rate scenarios."], ["AI/BI", "LCR and NSFR on certified regulatory views."]]),
            ], [
                biz("Data Engineers", "Lakeflow",
                    "Land core-banking postings, card-network authorizations, wire messages and market-data feeds; own Bronze to Silver and the pager when risk tables stall.",
                    [["Lakeflow Connect", "Managed connectors for core, cards and credit-bureau sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on posting and authorization feeds."], ["Lakewatch", "Freshness on the exposure and liquidity tables risk reads at open."]]),
                biz("Data Scientists", "MLflow",
                    "PD/LGD credit-risk, AML transaction-monitoring, card-fraud and next-best-action models, and whether they still hold through a rate cycle.",
                    [["Feature Store", "Customer and transaction features read identically in training and serving."], ["MLflow", "Every PD and fraud model tracked for audit and reproduction."], ["Model Serving", "Fraud and PD models scored in the authorization path."]]),
                biz("App Developers", "Apps",
                    "Ship the limit, case-management, RM workbench and AML investigator apps risk and RMs work in, hosted next to governed customer data.",
                    [["Apps", "Risk and RM screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for limit and case-management state."], ["Agent Bricks", "Agents that draft case narratives and limit changes against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Finance and risk dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for liquidity and exposure questions."),
                    tile("Notebooks & IDEs", "notebook", "Model development notebooks on governed customer data."),
                ]},
                {"box": "Partners & Networks", "ic": "partner", "tiles": [
                    tile("Card Network Files", "api", "Clearing and settlement files to Visa and Mastercard.", "visa"),
                    tile("Open Banking APIs", "api", "Account information and payment initiation to TPPs.", "tink"),
                    tile("Correspondent Banking", "globe", "SWIFT payment routing to correspondent banks.", "swift"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Limit Updates", "gauge", "Credit limits adjusted in core from early warning triggers."),
                    tile("Fraud Block Rules", "gavel", "Card blocks propagated to authorization switches.", "fico"),
                    tile("CRM Next-Best-Action", "custlake", "Offers pushed to digital channels from governed models.", "sf-fsc"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Basel III Returns", "gavel", "RWA and capital returns filed from contracted Gold tables.", "axiomsl"),
                    tile("FinCEN SAR Filing", "share", "Suspicious activity reports assembled from AML cases.", "actimize"),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Customer and exposure products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Partners and regulators via governed sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Branch Performance", "Household P&L", "chart", "Deposit, loan and fee profitability by branch and relationship manager."),
             app("RM Workbench", "Commercial CRM", "custlake", "Exposure, covenant status and cross-sell pipeline on governed relationship data."),
             app("AML Investigator", "Case prioritization", "gavel", "Alerts ranked and narratives drafted against transaction graphs."),
             app("ALM Dashboard", "Liquidity gaps", "gauge", "Rate and liquidity scenarios with hedge recommendations.")],
            [uc("Real-Time Fraud", "Payments", "gavel", "Authorization decisions scored before funds leave the account."),
             uc("AML Transaction Monitoring", "Compliance", "gavel", "Suspicious patterns surfaced across channels and entities."),
             uc("Credit Early Warning", "Risk", "chart", "Commercial deterioration flagged before covenant breach."),
             uc("Customer 360", "Retail", "custlake", "Household view across deposits, loans, cards and digital."),
             uc("Next-Best-Product", "Marketing", "market", "Offers ranked by propensity and profitability."),
             uc("Liquidity Forecasting", "Treasury", "gauge", "Cash and collateral projections under stress scenarios."),
             uc("Regulatory Reporting", "Finance", "erp", "Basel, CCAR and local returns from one governed model."),
             uc("Open Banking Analytics", "Digital", "api", "Consent, aggregation and payment initiation insights."),
             uc("Collections Optimization", "Lending", "people", "Treatment strategies ranked by recovery probability."),
             uc("Operational Loss", "Risk", "gavel", "Loss events captured and capitalized for AMA frameworks.")],
        ),
        "sources": {
            "temenos": {"t": "Temenos Transact", "u": "https://www.temenos.com/products/transact/"},
            "fis-profile": {"t": "FIS Profile", "u": "https://www.fisglobal.com/products/core-banking"},
            "finastra": {"t": "Finastra Fusion", "u": "https://www.finastra.com/solutions/lending"},
            "visa": {"t": "Visa", "u": "https://www.visa.com/"},
            "mastercard": {"t": "Mastercard", "u": "https://www.mastercard.com/"},
            "swift": {"t": "SWIFT", "u": "https://www.swift.com/"},
            "temenos-infinity": {"t": "Temenos Infinity", "u": "https://www.temenos.com/products/infinity/"},
            "sf-fsc": {"t": "Salesforce Financial Services Cloud", "u": "https://www.salesforce.com/financial-services/"},
            "actimize": {"t": "NICE Actimize", "u": "https://www.niceactimize.com/"},
            "moodys": {"t": "Moody's Analytics", "u": "https://www.moodys.com/"},
            "fis-alm": {"t": "FIS ALM", "u": "https://www.fisglobal.com/products/treasury-and-risk"},
            "axiomsl": {"t": "AxiomSL", "u": "https://www.axiomsl.com/"},
            "plaid": {"t": "Plaid", "u": "https://plaid.com/"},
            "tink": {"t": "Tink", "u": "https://tink.com/"},
            "fico": {"t": "FICO", "u": "https://www.fico.com/"},
            "lexisnexis": {"t": "LexisNexis Risk Solutions", "u": "https://risk.lexisnexis.com/"},
            "experian": {"t": "Experian", "u": "https://www.experian.com/business/"},
        },
    },
}
