import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl_rail2(business_tiles, tech_tiles):
    """People rail with per-industry Technical roles instead of shared TECH_PPL."""
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles},
    ]


INDUSTRIES_BATCH_PAYMENTS_FINTECH = {
    'payments_fintech': {
        "label": "Payments & Fintech",
        "blurb": "Card acquiring, digital wallets, lending and banking cores: authorisation streams, fraud, KYC and merchant lifecycle across regulated payment institutions.",
        "medallion": medallion(
            "Raw auth streams",
            "Authorisation requests, settlement files, core postings, KYC decisions and merchant onboarding events, landed exactly as received so a transaction or an account opening can always be replayed as it stood.",
            "Conformed account, txn",
            "Accounts, merchants, instruments and transactions resolved into single conformed entities across core, acquirer and fraud systems, with settlement batches reconciled and device fingerprints stitched to one identity graph.",
            "Volume, loss, NIM",
            "Contracted products product and risk run on: payment volume and take rate, fraud loss and chargeback rate, and net interest margin by product.",
        ),
        "rails": {
            "src": [
                {"box": "Core & Ledger", "ic": "erp", "tiles": [
                        tile("Temenos Transact", "erp", "Deposits, loans, GL and end-of-day across retail and commercial banking.", "temenos"),
                        tile("Mambu Core Banking", "db", "Cloud-native accounts, products and interest accrual for digital banks.", "mambu"),
                        tile("FIS Modern Banking", "erp", "Legacy core postings, statements and regulatory extracts.", "fis-core"),
                    ]},
                {"box": "Acquiring & Issuing", "ic": "market", "tiles": [
                        tile("Adyen Platform", "market", "Unified acquiring authorisations, settlements and dispute events.", "adyen"),
                        tile("Stripe Payments", "partner", "Merchant payment intents, connect payouts and radar fraud signals.", "stripe"),
                        tile("Marqeta Card Issuing", "api", "Card programmes, spend controls and tokenisation lifecycle.", "marqeta"),
                    ]},
                {"box": "Fraud & Compliance", "ic": "gavel", "tiles": [
                        tile("NICE Actimize", "gauge", "AML alerts, SAR workflows and transaction monitoring rules.", "actimize"),
                        tile("Onfido Identity", "people", "Document verification and biometric checks at onboarding.", "onfido"),
                        tile("AML Screening", "gavel", "Sanctions, PEP and adverse media screening on parties and merchants.", "complyadvantage"),
                    ]},
                {"box": "Merchant & CRM", "ic": "custlake", "tiles": [
                        tile("Salesforce Fintech CRM", "custlake", "Merchant sales pipeline, onboarding cases and support history.", "sf-fintech"),
                        tile("Zendesk Merchant Care", "chat", "Tickets, chat transcripts and refund disputes tied to merchant accounts.", "zendesk"),
                        tile("Braze Lifecycle", "partner", "Activation and retention campaigns with delivery and conversion events.", "braze"),
                    ]},
                fed_group("Card Network Mart", "Scheme reporting and interchange marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("SWIFT ISO 20022", "api", "Cross-border payment messages parsed into structured settlement events.", "swift-iso"),
                tile("Visa / Mastercard BIN", "partner", "Issuer and product metadata consumed inbound for routing and fraud.", "visa-developer"),
                tile("Open Banking Feeds", "stream", "Account aggregation and consent-based transaction imports for lending.", "open-banking"),
            ]),
            "ppl": ppl_rail2([
                biz("Payments Leadership", "Genie One", "The CEO on payment volume growth and take rate; the CFO on fraud loss and funding cost when interest rates and scheme fees move against the book.", [["Genie One", "Ask what yesterday's net payment volume was by product without waiting on finance."], ["AI/BI", "Volume, loss and margin on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"volume\" means one thing across core and acquirer."]]),
                biz("Product & Payments", "Model Serving", "Product managers on authorisation rates, routing cost and feature adoption, tracking take rate and activation across the payment products they own.", [["Payments Console", "Auth success and latency by route before a scheme change."], ["Model Serving", "Routing and fraud models scored in the auth path."], ["AI/BI", "Take rate and activation on governed definitions."]]),
                biz("Risk & Fraud", "AI/BI", "Fraud analysts on velocity rules, chargeback rate and AML alert queues, balancing fraud loss against the false-positive decline rate on good volume.", [["Fraud Command Centre", "Device clusters and mule patterns before payouts release."], ["AI/BI", "Loss and false-positive rates on certified Metric Views."], ["Unity Catalog", "One transaction definition across acquirer and core."]]),
                biz("Merchant Growth", "CustomerLake", "Sales and success on the onboarding funnel, merchant churn and support load, tracking activation and revenue per merchant account.", [["Merchant 360", "Onboarding status and revenue in one view."], ["CustomerLake", "Merchant segments without copying CRM elsewhere."], ["Genie One", "Ask which merchants spiked chargebacks last week."]]),
                biz("Finance & Treasury", "AI/BI", "Treasury on settlement floats, liquidity and scheme fee reconciliation, watching net interest margin and interchange revenue by product.", [["Treasury Workbench", "Float and funding scenarios before month-end close."], ["AI/BI", "NIM and interchange on certified Metric Views."], ["Unity Catalog", "One settlement definition across processors."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the core, acquirer, fraud and KYC feeds; own the Bronze to Silver path and the pager when an authorisation or settlement pipeline breaks.", [["Lakeflow Connect", "Managed connectors for core banking, acquirer and CRM sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on auth and settlement feeds."], ["Lakewatch", "Freshness on the volume and loss tables risk reads every morning."]]),
                biz("Data Scientists", "MLflow", "Real-time fraud, credit-underwriting, routing and merchant-churn models, and whether they still hold six months after deployment in the auth path.", [["Feature Store", "Transaction and device features read identically in training and serving."], ["MLflow", "Every fraud and credit run tracked for audit and reproduction."], ["Model Serving", "Fraud and routing models scored inside the authorisation path."]]),
                biz("App Developers", "Apps", "Ship the payments console, fraud command and merchant applications product and risk teams work in, hosted next to governed transaction data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for case state and governed writes."], ["Agent Bricks", "Agents that draft a dispute response against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                        tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                        tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and incident updates in the channel ops already works in (Beta)."),
                        tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code."),
                    ]},
                {"box": "Platform Writeback", "ic": "opdb", "tiles": [
                        tile("Fraud Block Lists", "gauge", "Device and instrument blocks pushed to authorisation in near real time.", "actimize"),
                        tile("Merchant Limit Updates", "market", "Spend and velocity limits adjusted from governed risk scores.", "stripe"),
                        tile("CRM Case Resolution", "custlake", "Dispute outcomes written back to merchant care workflows.", "zendesk"),
                    ]},
                {"box": "Partners & Schemes", "ic": "partner", "tiles": [
                        tile("Scheme Reporting API", "api", "Interchange and compliance files served to card networks from governed settlements.", "visa-developer"),
                        tile("Bank Sponsor Sharing", "share", "Programme performance shared to BIN sponsors over Delta Sharing.", "marqeta"),
                        tile("PSP Partner Portal", "partner", "Sub-merchant metrics exchanged without nightly flat files.", "adyen"),
                    ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                        tile("AML / SAR Reporting", "gavel", "Suspicious activity metrics filed from governed transaction monitoring.", "actimize"),
                        tile("PCI & Scheme Compliance", "share", "Control evidence and attestation data from contracted Gold products."),
                    ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                        tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                        tile("Sharing Recipients", "share", "Sponsors, auditors and partners reading live tables with no copy."),
                    ]},
            ]),
        },
        "top": top_band(
            [
                app("Payments Console", "Auth health", "gauge", "Authorisation success, latency and routing on Databricks Apps over Lakebase."),
                app("Fraud Command Centre", "Loss control", "gavel", "Velocity clusters and chargeback spikes before payouts release."),
                app("Merchant 360", "Onboarding", "custlake", "Pipeline, revenue and support history for every merchant account."),
                app("Treasury Workbench", "Float & NIM", "sheet", "Settlement floats and funding scenarios before month-end close."),
            ],
            [
                uc("Real-Time Fraud", "Authorisation", "gauge", "Mule and card-testing patterns blocked before settlement funds move."),
                uc("Chargeback Prevention", "Disputes", "gavel", "Dispute-prone merchants and instruments surfaced before scheme deadlines."),
                uc("Merchant Onboarding", "Growth", "partner", "KYB risk scored at signup so sales does not onboard bad actors."),
                uc("Credit Underwriting", "Lending", "sheet", "Cash-flow and behaviour models for BNPL and working-capital products."),
                uc("Payment Routing", "Optimisation", "market", "Auth routes chosen for success rate and cost not static BIN tables."),
                uc("AML Monitoring", "Compliance", "gavel", "Transaction monitoring tuned to reduce false positives without missing SARs."),
                uc("Merchant Churn", "Retention", "custlake", "At-risk merchants identified from volume dips and support signals."),
                uc("Interchange Optimisation", "Revenue", "chart", "MCC and routing choices maximising take rate within scheme rules."),
                uc("Open Banking Lending", "Data", "api", "Aggregated account data scored for affordability with consent lineage."),
                uc("Liquidity Forecasting", "Treasury", "erp", "Settlement floats and funding needs predicted before central bank windows."),
            ],
        ),
        "sources": {
            "temenos": {"t": "Temenos Transact", "u": "https://www.temenos.com/products/transact/"},
            "mambu": {"t": "Mambu", "u": "https://www.mambu.com/"},
            "fis-core": {"t": "FIS Modern Banking Platform", "u": "https://www.fisglobal.com/en/solutions/banking-core"},
            "adyen": {"t": "Adyen", "u": "https://www.adyen.com/"},
            "stripe": {"t": "Stripe", "u": "https://stripe.com/"},
            "marqeta": {"t": "Marqeta", "u": "https://www.marqeta.com/"},
            "actimize": {"t": "NICE Actimize", "u": "https://www.niceactimize.com/"},
            "onfido": {"t": "Onfido", "u": "https://onfido.com/"},
            "complyadvantage": {"t": "ComplyAdvantage", "u": "https://complyadvantage.com/"},
            "sf-fintech": {"t": "Salesforce Financial Services Cloud", "u": "https://www.salesforce.com/financial-services/"},
            "zendesk": {"t": "Zendesk", "u": "https://www.zendesk.com/"},
            "braze": {"t": "Braze", "u": "https://www.braze.com/"},
            "swift-iso": {"t": "SWIFT ISO 20022", "u": "https://www.swift.com/standards/iso-20022"},
            "visa-developer": {"t": "Visa Developer", "u": "https://developer.visa.com/"},
            "open-banking": {"t": "Open Banking standards", "u": "https://openbanking.org.uk/"},
        },
    },
}
