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


INDUSTRIES_BATCH_MORTGAGE_LENDING = {
    "mortgage_lending": {
        "label": "Mortgage & Lending",
        "blurb": "Mortgage origination, servicing and consumer lending: point-of-sale and underwriting, secondary marketing and GSE delivery, servicing and default, and HMDA fair-lending compliance.",
        "medallion": medallion(
            "Raw loan and servicing feeds",
            "Loan files and conditions from Encompass, MSP servicing and payment records, DU and Loan Product Advisor findings, tri-merge credit pulls and Optimal Blue lock data, landed exactly as received so a rate lock or a decision can always be replayed as it stood.",
            "Conformed loan, borrower, property",
            "Loans, borrowers, properties and investors resolved into single conformed entities across the origination, servicing and secondary estates, with loan numbers, MERS MINs and borrower identity reconciled and each loan stitched to one lifecycle.",
            "Margin, delinquency, prepayment risk",
            "Contracted products the production, servicing and secondary teams run on: gain-on-sale margin by channel and product, delinquency and roll-rate by vintage, prepayment and MSR valuation, and HMDA and fair-lending fields.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Origination & POS",
                    "ic": "erp",
                    "tiles": [
                        tile(
                            "ICE Encompass LOS",
                            "erp",
                            "ICE Mortgage Technology Encompass, the dominant loan origination system and the system of record for loan files, borrower data, conditions and the origination workflow from application to closing.",
                            "encompass",
                            cat="Loan Origination System (LOS)",
                            what="The dominant loan origination system and the system of record for loan files, borrower data, conditions and the origination workflow from application to closing.",
                            users="Loan officers, processors and underwriters.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "20-80 GB/day loan files + conditions", "Continuous CDC (near real-time)")),
                        ),
                        tile(
                            "Blend POS",
                            "appbuilder",
                            "Consumer point-of-sale front end capturing the application, document upload and status, and feeding the loan file into the origination system.",
                            "blend",
                            cat="Mortgage Point-of-Sale (POS)",
                            what="Consumer point-of-sale front end capturing the application, document upload and status, and feeding the loan file into the origination system.",
                            users="POS and channel teams, loan officers and borrowers.",
                            data_out=data_out(
                                batch=flow(["structured", "unstructured"], "5-20 GB/day applications + docs", "Nightly batch"),
                                stream=flow(["semi-structured"], "Application + status events", "Continuous (events)")),
                        ),
                        tile(
                            "nCino Mortgage",
                            "product",
                            "nCino Mortgage Suite (SimpleNexus) point-of-sale and origination, capturing borrower intent, disclosures and closing collaboration across the loan team.",
                            "ncino",
                            cat="Mortgage Point-of-Sale / Origination",
                            what="Point-of-sale and origination suite capturing borrower intent, disclosures and closing collaboration across the loan team.",
                            users="Loan officers, processors and POS teams.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "5-20 GB/day applications + disclosures", "Nightly batch")),
                        ),
                        tile(
                            "MeridianLink LOS",
                            "erp",
                            "Consumer and mortgage loan origination for banks and credit unions, the system of record for applications, decisions and funding on the consumer-lending side.",
                            "meridianlink",
                            cat="Loan Origination System (LOS)",
                            what="Consumer and mortgage loan origination for banks and credit unions, the system of record for applications, decisions and funding on the consumer-lending side.",
                            users="Loan officers, processors and consumer lending teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-20 GB/day applications + decisions", "Nightly batch")),
                        ),
                    ],
                },
                {
                    "box": "Servicing Platforms",
                    "ic": "db",
                    "tiles": [
                        tile(
                            "Black Knight MSP",
                            "erp",
                            "The ICE Black Knight MSP servicing system of record: loan boarding, payment processing, escrow administration, investor accounting and default across the servicing book.",
                            "bkmsp",
                            cat="Mortgage Servicing System",
                            what="The servicing system of record covering loan boarding, payment processing, escrow administration, investor accounting and default across the servicing book.",
                            users="Servicing operations, default and investor accounting.",
                            data_out=data_out(
                                batch=flow(["structured"], "50-200 GB/day payments + escrow", "Nightly batch + intraday CDC")),
                        ),
                        tile(
                            "Sagent LoanServ",
                            "db",
                            "Sagent's real-time servicing platform for banks and non-banks: payment, escrow and default servicing with a consumer-grade experience.",
                            "sagent",
                            cat="Mortgage Servicing System",
                            what="Real-time servicing platform for banks and non-banks covering payment, escrow and default servicing with a consumer-grade experience.",
                            users="Servicing operations, default and retention.",
                            data_out=data_out(
                                batch=flow(["structured"], "20-80 GB/day payments + escrow", "Continuous CDC (near real-time)")),
                        ),
                        tile(
                            "Servicing Digital",
                            "apps",
                            "Borrower self-service channel for statements, payments, payoff and escrow, the servicing-side customer front end joined to the loan of record.",
                            cat="Borrower Self-Service Portal",
                            what="Borrower self-service channel for statements, payments, payoff and escrow, the servicing-side customer front end joined to the loan of record.",
                            users="Retention, servicing operations and borrowers.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "Portal + payment events", "Continuous (events)")),
                        ),
                        tile(
                            "Investor Accounting",
                            "sheet",
                            "Investor remittance and loan-level reporting to Fannie Mae, Freddie Mac and Ginnie Mae, cash and accounting against each pool and custodial account.",
                            cat="Investor Accounting / Remittance",
                            what="Investor remittance and loan-level reporting to Fannie Mae, Freddie Mac and Ginnie Mae, cash and accounting against each pool and custodial account.",
                            users="Investor accounting, finance and servicing operations.",
                            data_out=data_out(
                                batch=flow(["structured"], "Remittance + loan-level reporting", "Multiple remittance cycles monthly")),
                        ),
                    ],
                },
                {
                    "box": "Underwriting & Credit",
                    "ic": "gavel",
                    "tiles": [
                        tile(
                            "Fannie Mae DU",
                            "govcat",
                            "Desktop Underwriter, Fannie Mae's automated underwriting system, returning eligibility and findings against the selling guide for each application.",
                            "du",
                            cat="Automated Underwriting System (AUS)",
                            what="Automated underwriting system returning eligibility and findings against the selling guide for each application.",
                            users="Underwriters, credit policy and processors.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "Findings responses", "Continuous (API, per application)")),
                        ),
                        tile(
                            "Freddie Mac LPA",
                            "govcat",
                            "Loan Product Advisor, Freddie Mac's automated underwriting engine, returning risk and eligibility assessments used to make and support the credit decision.",
                            "lpa",
                            cat="Automated Underwriting System (AUS)",
                            what="Automated underwriting engine returning risk and eligibility assessments used to make and support the credit decision.",
                            users="Underwriters, credit policy and processors.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "Assessment responses", "Continuous (API, per application)")),
                        ),
                        tile(
                            "Tri-Merge Credit",
                            "identity",
                            "Merged Experian, Equifax and TransUnion credit reports and scores pulled at application and re-pulled before closing, the basis of the credit decision.",
                            "bureaus",
                            cat="Credit Bureau Data (Tri-Merge)",
                            what="Merged Experian, Equifax and TransUnion credit reports and scores pulled at application and re-pulled before closing, the basis of the credit decision.",
                            users="Underwriters, credit risk ML and credit policy.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "Credit report + score pulls", "Continuous (API, per pull)")),
                        ),
                        tile(
                            "Income & Asset Verif",
                            "file",
                            "The Work Number and asset-verification services confirming employment, income and deposits so underwriting works from verified rather than stated figures.",
                            "twn",
                            cat="Income & Asset Verification Service",
                            what="Employment, income and deposit verification services so underwriting works from verified rather than stated figures.",
                            users="Underwriters, processors and credit policy.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "Verification responses", "Continuous (API, per request)")),
                        ),
                    ],
                },
                {
                    "box": "Pricing & Secondary",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "Optimal Blue PPE",
                            "market",
                            "The product and pricing engine returning eligible products and locked rates against investor guidelines and margin, the source of the rate lock.",
                            "ob",
                            cat="Product & Pricing Engine (PPE)",
                            what="Product and pricing engine returning eligible products and locked rates against investor guidelines and margin, the source of the rate lock.",
                            users="Secondary marketing, loan officers and pricing.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "Lock + pricing events", "Continuous (real-time)")),
                        ),
                        tile(
                            "MCT Secondary",
                            "chart",
                            "Mortgage Capital Trading pipeline hedging and best-execution analytics for the secondary desk, sizing loan sales and TBA positions.",
                            "mct",
                            cat="Secondary / Hedging Platform",
                            what="Pipeline hedging and best-execution analytics for the secondary desk, sizing loan sales and TBA positions.",
                            users="Secondary marketing, hedging desk and MSR managers.",
                            data_out=data_out(
                                batch=flow(["structured"], "Hedge positions + best-ex analytics", "Intraday + end-of-day")),
                        ),
                        tile(
                            "GSE Loan Delivery",
                            "partner",
                            "Fannie Mae Loan Delivery and Freddie Mac Loan Selling Advisor: loan delivery, pooling and commitment against agency programs and pricing.",
                            "gse",
                            cat="GSE Loan Delivery System",
                            what="Loan delivery, pooling and commitment against agency programs and pricing for Fannie Mae and Freddie Mac.",
                            users="Secondary marketing, investor delivery and finance.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "Delivery + pool + commitment files", "Multiple delivery cycles daily")),
                        ),
                        tile(
                            "MERS Registry",
                            "govcat",
                            "Mortgage Electronic Registration Systems tracking servicing rights and note ownership as loans and MSRs transfer between parties.",
                            "mers",
                            cat="Mortgage Registry (MERS)",
                            what="Electronic registry tracking servicing rights and note ownership as loans and MSRs transfer between parties.",
                            users="Secondary marketing, servicing operations and MSR managers.",
                            data_out=data_out(
                                batch=flow(["structured"], "MIN + transfer records", "Daily batch")),
                        ),
                    ],
                },
                {
                    "box": "Default & Compliance",
                    "ic": "gavel",
                    "tiles": [
                        tile(
                            "Default & Collections",
                            "opdb",
                            "Loss mitigation, collections and foreclosure workflow for delinquent loans, the servicing-side default estate with borrower outreach and workout state.",
                            cat="Default & Collections System",
                            what="Loss mitigation, collections and foreclosure workflow for delinquent loans, the servicing-side default estate with borrower outreach and workout state.",
                            users="Default and loss mitigation, collections and servicing operations.",
                            data_out=data_out(
                                batch=flow(["structured"], "Delinquency + workout state", "Nightly batch")),
                        ),
                        tile(
                            "HMDA / LAR",
                            "gavel",
                            "The Home Mortgage Disclosure Act loan application register: the fields and reporting that expose fair-lending and disparate-impact exposure.",
                            "hmda",
                            cat="Regulatory Reporting Register (HMDA)",
                            what="The Home Mortgage Disclosure Act loan application register, the fields and reporting that expose fair-lending and disparate-impact exposure.",
                            users="Fair lending and compliance, credit policy and legal.",
                            data_out=data_out(
                                batch=flow(["structured"], "LAR records", "Periodic (regulatory cycle)")),
                        ),
                        tile(
                            "CoreLogic Property",
                            "globe",
                            "CoreLogic (Cotality) property, valuation and AVM data plus flood and hazard, joined to the collateral behind every loan.",
                            "corelogic",
                            cat="Property & Valuation Data Provider",
                            what="Property, valuation and AVM data plus flood and hazard, joined to the collateral behind every loan.",
                            users="Underwriters, collateral risk and secondary marketing.",
                            data_out=data_out(
                                batch=flow(["structured"], "Property + AVM + hazard data", "Daily/weekly updates")),
                        ),
                        tile(
                            "Title & Closing",
                            "docs",
                            "Qualia and ICE closing systems producing title, settlement and closing-disclosure documents at the end of the origination workflow.",
                            "qualia",
                            cat="Title & Closing Platform",
                            what="Title, settlement and closing-disclosure documents produced at the end of the origination workflow.",
                            users="Closing teams, processors and compliance.",
                            data_out=data_out(
                                batch=flow(["structured", "unstructured"], "Title + settlement + CD documents", "Nightly batch")),
                        ),
                    ],
                },
                fed_group(
                    "Loan & Finance Marts",
                    "Enterprise loan, servicing and general-ledger marts left where they are and queried in place under Unity Catalog, which avoids a second copy of the audited book of record.",
                    cat="Loan & Finance Data Mart",
                    what="Enterprise loan, servicing and general-ledger marts kept in the incumbent warehouses and queried in place, avoiding a second copy of the audited book of record.",
                    users="Finance, risk and servicing operations.",
                    data_out=data_out(
                        batch=flow(["structured"], "TB-scale loan + GL history", "Queried on demand (federated)")),
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "MISMO Data Feeds",
                        "api",
                        "MISMO-standard XML loan data exchanged with investors, insurers and vendors, parsed on arrival and landed as structured events.",
                        "mismo",
                        cat="Mortgage Data Standard (MISMO)",
                        what="MISMO-standard XML loan data exchanged with investors, insurers and vendors, parsed on arrival and landed as structured events.",
                        users="Loan data engineering, secondary marketing and investors.",
                        data_out=data_out(
                            batch=flow(["semi-structured"], "MISMO XML loan files", "Multiple batches daily"),
                            stream=flow(["semi-structured"], "MISMO message events", "Continuous (events)")),
                    ),
                    tile(
                        "Doc & OCR Stream",
                        "docs",
                        "Scanned income, asset and closing documents streamed in for classification and extraction as they arrive at the loan file.",
                        cat="Document / OCR Stream",
                        what="Scanned income, asset and closing documents streamed in for classification and extraction as they arrive at the loan file.",
                        users="Origination, document intelligence and underwriting.",
                        data_out=data_out(
                            stream=flow(["unstructured", "semi-structured"], "Document images + extracts", "Continuous (as received)")),
                    ),
                    tile(
                        "Bureau & Vendor APIs",
                        "api",
                        "Credit, verification, pricing and property request/response APIs consumed inbound through managed ELT connectors and existing event topics.",
                        cat="Bureau & Vendor Streaming API",
                        what="Credit, verification, pricing and property request/response APIs consumed inbound through managed ELT connectors and existing event topics.",
                        users="Loan data engineering, underwriting and secondary marketing.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "Vendor API responses", "Continuous (API/events)")),
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Lending Exec",
                        "Genie One",
                        "The CEO and Chief Lending Officer on origination volume, gain-on-sale margin and the balance between production and credit quality; the CFO on funding cost, MSR value and cost-to-originate; the Chief Risk Officer on portfolio credit and fair-lending exposure.",
                        [
                            ["Genie One", "Ask what a channel originated last month, or where margin compressed, without booking analyst time."],
                            ["AI/BI", "Volume, margin, delinquency and fair-lending exposure on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the business glossary, so \"margin\" and \"delinquency\" mean one thing across origination and servicing."],
                        ],
                        sub=[
                            ["CEO & CLO", "origination volume, gain-on-sale margin and the production-versus-quality trade."],
                            ["CFO", "funding cost, MSR valuation and cost-to-originate across channels."],
                            ["Chief Risk Officer", "portfolio credit risk and fair-lending exposure across the book."],
                        ],
                        ucs=["Portfolio Credit Risk", "Fair Lending & HMDA", "Pipeline Hedging"],
                    ),
                    biz(
                        "Origination",
                        "AI/BI",
                        "Retail and wholesale production leaders on lead conversion and pull-through; loan officers and processors moving files from application to clear-to-close; the POS and channel team on borrower experience and time-to-close.",
                        [
                            ["AI/BI", "Pull-through, cycle time and cost per funded loan on the definitions production defends."],
                            ["Model Serving", "Lead, conversion and pull-through models scored inside the origination path."],
                            ["CustomerLake", "Borrower and lead profile activated for outreach without a separate CDP."],
                        ],
                        sub=[
                            ["Production leaders", "lead conversion and pull-through by channel and loan officer."],
                            ["Loan officers & processors", "moving files from application to clear-to-close."],
                            ["POS & channel", "borrower experience and time-to-close across the funnel."],
                        ],
                        ucs=["Document Intelligence", "Lead & Pull-Through", "Automated Underwriting"],
                    ),
                    biz(
                        "Underwriting",
                        "AI Functions",
                        "Underwriters clearing conditions and rendering the credit decision; credit-policy owners setting overlays above DU and LPA; the fair-lending and compliance team proving decisions are consistent and defensible under ECOA and HMDA.",
                        [
                            ["AI Functions", "Income, asset and condition documents classified and extracted at scale."],
                            ["Model Serving", "Credit and eligibility models scored alongside DU and LPA findings."],
                            ["Unity Catalog", "Auditable decision lineage and reason codes a regulator will accept."],
                        ],
                        sub=[
                            ["Underwriters", "clearing conditions and rendering the credit decision."],
                            ["Credit policy", "overlays and eligibility rules above the automated systems."],
                            ["Fair lending & compliance", "consistency, adverse-action reason codes and HMDA exposure."],
                        ],
                        ucs=["Automated Underwriting", "Credit Decisioning", "Fair Lending & HMDA"],
                    ),
                    biz(
                        "Servicing Ops",
                        "Lakehouse//RT",
                        "Servicing operations on payment, escrow and investor accounting; the default and loss-mitigation team on delinquency, workouts and foreclosure; the retention team on payoff risk and recapture before a borrower refinances away.",
                        [
                            ["Lakehouse//RT", "Payment, escrow and delinquency state at the latency servicing acts on."],
                            ["Model Serving", "Delinquency, loss-mitigation and recapture models scored in the servicing path."],
                            ["AI/BI", "Roll rate, cure rate and retention on the servicing team's own definitions."],
                        ],
                        sub=[
                            ["Servicing operations", "payment, escrow and investor accounting on the book."],
                            ["Default & loss mitigation", "delinquency, workouts and foreclosure timelines."],
                            ["Retention", "payoff risk and recapture before a refinance leaves."],
                        ],
                        ucs=["Default & Loss Mit", "Borrower Retention", "Portfolio Credit Risk"],
                    ),
                    biz(
                        "Secondary Desk",
                        "Model Serving",
                        "Secondary marketing on rate-lock pipeline and best execution; the hedging desk managing TBA and pull-through risk to the trade; MSR and portfolio managers on prepayment behaviour and servicing-rights valuation.",
                        [
                            ["Model Serving", "Prepayment and pull-through models scored into hedge and lock decisions."],
                            ["Lakehouse//RT", "Lock pipeline and market state at the latency the desk hedges at."],
                            ["AI/BI", "Best execution, hedge P&L and MSR value on certified Metric Views."],
                        ],
                        sub=[
                            ["Secondary marketing", "rate-lock pipeline and best-execution loan sale."],
                            ["Hedging desk", "TBA and pull-through risk managed to the trade."],
                            ["MSR & portfolio", "prepayment behaviour and servicing-rights valuation."],
                        ],
                        ucs=["Prepayment & MSR", "Pipeline Hedging", "Portfolio Credit Risk"],
                    ),
                ],
                [
                    biz(
                        "Loan Data Eng",
                        "Lakeflow",
                        "Land Encompass loan files, Black Knight MSP servicing feeds, DU and LPA findings and Optimal Blue locks, parse MISMO, and own the Bronze to Silver path and the pager when a feed breaks.",
                        [
                            ["Lakeflow Connect", "Managed connectors for the LOS, servicing and vendor sources."],
                            ["Lakeflow Designer", "Declarative pipelines with expectations on loan, credit and lock feeds."],
                            ["Lakewatch", "Freshness on the tables underwriting and the secondary desk read every morning."],
                        ],
                    ),
                    biz(
                        "Risk & Credit ML",
                        "MLflow",
                        "Build credit, prepayment, default and pull-through models on borrower, bureau and performance data, and prove they still hold and stay fair after deployment.",
                        [
                            ["Feature Store", "Borrower and loan features defined once and read identically in training and serving."],
                            ["MLflow", "Every run and model card tracked for audit, reproduction and fair-lending review."],
                            ["Model Serving", "Credit, prepayment and default models scored in the decision path."],
                        ],
                    ),
                    biz(
                        "Lending App Dev",
                        "Apps",
                        "Ship the underwriting, loss-mitigation, lock-desk and monitoring applications the lender works in, hosted next to governed loan data.",
                        [
                            ["Apps", "Underwriting and servicing screens with no separate web tier to run or secure."],
                            ["Lakebase", "Serverless Postgres for decision, workout and lock state with governed writes."],
                            ["Agent Bricks", "Agents that draft a condition set or a workout plan against governed tools."],
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
                                "Genie in Teams for governed answers, and delinquency and pipeline alerts in the channel the team already works in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Notebooks, VS Code and JetBrains against governed loan data and Genie Code.",
                            ),
                        ],
                    },
                    {
                        "box": "Distribution & Partners",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "Investor Delta Sharing",
                                "share",
                                "Loan tapes and performance shared to investors, aggregators and warehouse lenders over Delta Sharing rather than file exchange.",
                            ),
                            tile(
                                "GSE & Aggregators",
                                "partner",
                                "Delivery, pooling and repurchase state exchanged with Fannie Mae, Freddie Mac, Ginnie Mae and correspondent aggregators on live tables.",
                            ),
                            tile(
                                "Data Marketplace",
                                "market",
                                "Curated property, credit and market datasets consumed and published through Databricks Marketplace.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "LOS Writeback",
                                "db",
                                "Cleared conditions, decisions and pricing written back into Encompass so the answer reaches the origination path.",
                            ),
                            tile(
                                "Servicing Writeback",
                                "erp",
                                "Loss-mitigation offers and workout decisions pushed back into Black Knight MSP where servicing already works.",
                            ),
                            tile(
                                "Case & Task Queue",
                                "gavel",
                                "Fair-lending and default cases pushed to the review queue analysts already work.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "HMDA / LAR Filings",
                                "gavel",
                                "HMDA loan application register and fair-lending reporting produced from the same governed tables the lender originates on.",
                                "hmda",
                            ),
                            tile(
                                "Regulatory Reporting",
                                "share",
                                "CFPB, investor and CECL submissions filed from contracted Gold products with lineage back to the source.",
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
                                "Published, contracted products discoverable in Unity Catalog Domains and shared over OpenSharing.",
                            ),
                            tile(
                                "Sharing Recipients",
                                "share",
                                "Investors, servicers and partners reading live tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ],
                genie_spaces=[
                    genie("Production & Pipeline", "Ask about origination volume, margin and pull-through by channel in plain language.",
                          feeds=["ICE Encompass LOS", "Optimal Blue PPE", "Margin, delinquency, prepayment risk"],
                          teams=["Origination", "Production leaders", "Lending Exec"],
                          questions=[
                              "What did each channel originate last month?",
                              "Where has gain-on-sale margin compressed this quarter?",
                              "What is pull-through by loan officer and product?",
                              "Which loans are stuck in the pipeline and why?",
                              "How does cycle time to clear-to-close compare across branches?"]),
                    genie("Credit & Underwriting", "Ask about credit decisions, findings and conditions across the book in plain language.",
                          feeds=["Fannie Mae DU", "Tri-Merge Credit", "Conformed loan, borrower, property"],
                          teams=["Underwriting", "Underwriters", "Credit policy"],
                          questions=[
                              "What is our approval rate by product and channel this month?",
                              "Which conditions most often delay a clear-to-close?",
                              "How do DU and LPA findings differ on our applications?",
                              "Where are overlays above the agency systems costing volume?",
                              "Which applications were denied and for what reason codes?"]),
                    genie("Servicing & Default", "Ask about delinquency, roll rates and workouts across the servicing book in plain language.",
                          feeds=["Black Knight MSP", "Default & Collections", "Margin, delinquency, prepayment risk"],
                          teams=["Servicing Ops", "Default & loss mitigation", "Retention"],
                          questions=[
                              "What is delinquency and roll rate by vintage right now?",
                              "Which loans are most likely to roll to foreclosure this month?",
                              "What is our cure rate by workout type?",
                              "Which borrowers are at highest payoff and refinance risk?",
                              "Where are escrow shortfalls concentrated across the book?"]),
                    genie("Secondary & MSR", "Ask about the lock pipeline, best execution and MSR valuation in plain language.",
                          feeds=["MCT Secondary", "Optimal Blue PPE", "Margin, delinquency, prepayment risk"],
                          teams=["Secondary Desk", "Secondary marketing", "MSR & portfolio"],
                          questions=[
                              "What is our current rate-lock pipeline and pull-through?",
                              "Where is best execution strongest across investors today?",
                              "What is our hedge position against the pipeline right now?",
                              "How have prepayment speeds moved on the MSR book?",
                              "What is the MSR valuation by investor and vintage?"]),
                ],
                dashboards=[
                    dashboard("Production & Margin", "Origination volume, margin and pull-through across channels on certified Metric Views.",
                              kpis=["Origination volume", "Gain-on-sale margin", "Pull-through", "Cycle time", "Cost per funded loan"],
                              teams=["Lending Exec", "Origination", "Production leaders"]),
                    dashboard("Credit & Fair Lending", "Approval, denial and pricing outcomes tested for disparate impact.",
                              kpis=["Approval rate", "Denial rate", "Disparate impact", "Adverse-action reason codes", "HMDA completeness"],
                              teams=["Underwriting", "Fair lending & compliance", "Chief Risk Officer"]),
                    dashboard("Servicing & Delinquency", "Delinquency, roll rate and workout performance across the servicing book.",
                              kpis=["Delinquency rate", "Roll rate", "Cure rate", "Foreclosure timeline", "Recapture rate"],
                              teams=["Servicing Ops", "Default & loss mitigation", "Retention"]),
                    dashboard("Secondary & MSR", "Lock pipeline, best execution and MSR valuation across investors and vintages.",
                              kpis=["Lock pipeline", "Best execution", "Hedge P&L", "Prepayment speed (CPR)", "MSR valuation"],
                              teams=["Secondary Desk", "Hedging desk", "MSR & portfolio"]),
                ],
            ),
        },
        "top": top_band(
            [
                app(
                    "Underwriting Copilot",
                    "Decision support",
                    "gauge",
                    "Where underwriters see extracted income and asset data, DU and LPA findings and a scored recommendation with reason codes on one screen, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Loss Mit Console",
                    "Default management",
                    "opdb",
                    "Delinquency risk, workout eligibility and outreach status by loan, so servicing acts before a delinquency rolls to foreclosure.",
                ),
                app(
                    "Hedge & Lock Desk",
                    "Secondary marketing",
                    "market",
                    "The rate-lock pipeline, pull-through and hedge position on one screen so the secondary desk sizes the trade against live risk.",
                ),
                app(
                    "Fair Lending Monitor",
                    "Compliance oversight",
                    "gavel",
                    "Approval, pricing and denial patterns tested for disparate impact across protected classes, with the evidence pack an examiner will ask for.",
                ),
            ],
            [
                uc(
                    "Automated Underwriting",
                    "Underwriting",
                    "gauge",
                    "Assembling the full loan file, running it against DU and LPA and a scored recommendation, and surfacing only the exceptions that need human judgment.",
                    problem="Underwriters re-key data from pay stubs, bank statements and bureau pulls across five systems, so files sit in queues and straight-through cases still wait behind manual review.",
                    who="Underwriting",
                    how="Documents are extracted with AI Functions and joined to DU and LPA findings in the lakehouse; a scored recommendation and reason codes are served to the Underwriting Copilot for exception-only review.",
                    comps=["Underwriting Copilot", "Fannie Mae DU", "Freddie Mac LPA", "AI Functions", "Model Serving"],
                    stories=[
                        ["Vantage Bank Texas accelerates loan processing with AI", "https://www.databricks.com/blog/accelerating-loan-processing-ai-databricks-how-vantage-bank-texas-transformed-lending"],
                        ["AI applications in finance: credit and underwriting", "https://www.databricks.com/blog/ai-applications-in-finance"],
                    ],
                ),
                uc(
                    "Credit Decisioning",
                    "Credit risk",
                    "identity",
                    "Scoring creditworthiness on bureau, income, asset and alternative data with models that are accurate, explainable and defensible for every applicant.",
                    problem="Traditional scorecards decline thin-file and non-traditional borrowers a lender could safely approve, and the models are hard to explain when the decision is challenged.",
                    who="Underwriting",
                    how="Bureau, income and cash-flow data are conformed and engineered in Feature Store; credit models are trained and versioned in MLflow and scored in Model Serving with Unity Catalog lineage.",
                    comps=["Tri-Merge Credit", "Model Serving", "Feature Store", "MLflow", "Unity Catalog"],
                    stories=[
                        ["Finda delivers faster, informed loans on Databricks", "https://www.databricks.com/customers/finda"],
                        ["Vivriti Capital scales real-time lending and credit", "https://www.databricks.com/customers/vivriti-capital"],
                    ],
                ),
                uc(
                    "Fair Lending & HMDA",
                    "Compliance",
                    "gavel",
                    "Monitoring approval, pricing and denial outcomes for disparate impact and producing HMDA and adverse-action evidence a regulator will accept.",
                    problem="Fair-lending testing runs quarterly on extracts in spreadsheets, so disparate impact is found after loans are booked and completeness is hard to prove to the CFPB.",
                    who="Underwriting",
                    how="Decision, pricing and HMDA fields are conformed to Gold with Unity Catalog lineage; fairness metrics and reason codes are computed with AI Functions and read in the Fair Lending Monitor.",
                    comps=["Fair Lending Monitor", "HMDA / LAR", "AI/BI", "Unity Catalog", "AI Functions"],
                    stories=[
                        ["Databricks for Financial Services: lending and risk", "https://www.databricks.com/solutions/industries/financial-services"],
                    ],
                ),
                uc(
                    "Document Intelligence",
                    "Docs",
                    "docs",
                    "Classifying and extracting income, asset, title and closing documents into structured loan data as soon as they arrive, instead of a stipulation queue.",
                    problem="Borrower documents arrive as phone photos and mixed-quality scans in the POS, and manual indexing and re-keying is the slowest, most error-prone step in the file.",
                    who="Origination",
                    how="Documents stream in from Blend and the POS and are classified and extracted with AI Functions and Agent Bricks, then written back into Encompass as structured, verified fields.",
                    comps=["Doc & OCR Stream", "AI Functions", "Agent Bricks", "Blend POS", "ICE Encompass LOS"],
                    stories=[
                        ["Vantage Bank Texas accelerates loan processing with AI", "https://www.databricks.com/blog/accelerating-loan-processing-ai-databricks-how-vantage-bank-texas-transformed-lending"],
                    ],
                ),
                uc(
                    "Lead & Pull-Through",
                    "Production",
                    "aisvc",
                    "Scoring which leads convert and which locked loans actually fund, so loan officers and marketing spend on the applications that will close.",
                    problem="Leads and locked pipeline are worked on gut feel, so marketing dollars chase applications that never fund and pull-through is only known after the month closes.",
                    who="Origination",
                    how="Lead, application and lock data are activated through CustomerLake; conversion and pull-through models are scored in Model Serving and read against pricing in AI/BI.",
                    comps=["CustomerLake", "Model Serving", "AI/BI", "ICE Encompass LOS", "Optimal Blue PPE"],
                ),
                uc(
                    "Prepayment & MSR",
                    "Servicing rights",
                    "chart",
                    "Modelling prepayment behaviour from loan, rate and borrower data so mortgage servicing rights are valued and hedged rather than marked to a vendor curve.",
                    problem="MSR value swings with prepayment speeds a lender models on stale vendor assumptions, so hedges lag the rate move and the balance-sheet mark is late.",
                    who="Secondary Desk",
                    how="Servicing, rate and borrower data are conformed to Gold; prepayment and CPR models are tracked in MLflow and scored in Model Serving to value and hedge the MSR book.",
                    comps=["MCT Secondary", "Model Serving", "MLflow", "Black Knight MSP", "AI/BI"],
                    stories=[
                        ["Credit loss forecasting reference architecture (CECL)", "https://www.databricks.com/resources/architectures/credit-loss-forecasting-reference-architecture"],
                    ],
                ),
                uc(
                    "Pipeline Hedging",
                    "Secondary",
                    "market",
                    "Hedging the rate-lock pipeline to the TBA market against pull-through risk so gain-on-sale margin survives the move between lock and sale.",
                    problem="Locks are hedged on a spreadsheet snapshot of pull-through, so a rate move between lock and delivery erodes margin before the desk can adjust the position.",
                    who="Secondary Desk",
                    how="Lock, pricing and market data land in Lakehouse//RT; pull-through models score each lock in Model Serving and the net position is sized in the Hedge & Lock Desk.",
                    comps=["Hedge & Lock Desk", "Optimal Blue PPE", "MCT Secondary", "Model Serving", "Lakehouse//RT"],
                ),
                uc(
                    "Default & Loss Mit",
                    "Servicing",
                    "opdb",
                    "Predicting which loans will roll to delinquency and matching each borrower to the right workout before a cure becomes a foreclosure.",
                    problem="Default teams react to missed payments after the roll, so the cheapest workout window is gone and foreclosure timelines and losses run up.",
                    who="Servicing Ops",
                    how="Payment, escrow and borrower data land in Lakehouse//RT; delinquency and loss-mitigation models are scored in Model Serving and worked from the Loss Mit Console.",
                    comps=["Loss Mit Console", "Black Knight MSP", "Model Serving", "Default & Collections", "Lakehouse//RT"],
                    stories=[
                        ["HDFC Bank modernizes credit risk analytics", "https://www.databricks.com/customers/hdfc-bank"],
                    ],
                ),
                uc(
                    "Borrower Retention",
                    "Personalisation",
                    "custlake",
                    "Spotting the borrowers most likely to refinance or pay off, and recapturing them with the right offer before they leave for another lender.",
                    problem="Payoff risk is only visible when the payoff request arrives, by which point the borrower has already locked with a competitor and the servicing asset is lost.",
                    who="Servicing Ops",
                    how="Servicing, rate and behaviour data are activated through CustomerLake; recapture models are scored in Model Serving and offers surfaced in Servicing Digital and AI/BI.",
                    comps=["CustomerLake", "Model Serving", "Servicing Digital", "AI/BI", "Genie One"],
                    stories=[
                        ["Discovery Bank personalizes banking with data and ML", "https://www.databricks.com/customers/discovery-bank"],
                    ],
                ),
                uc(
                    "Portfolio Credit Risk",
                    "Risk",
                    "gauge",
                    "Loan-level credit loss, CECL reserves and stress across the whole book on one governed set of loans, so risk and finance argue about the scenario, not the numbers.",
                    problem="CECL and stress are stitched from servicing, GL and macro extracts that never agree, so reserves are assembled under deadline and lineage back to the loan is hard to prove.",
                    who="Lending Exec",
                    how="Loan, GL and macro-scenario data are conformed to Gold; credit-loss and stress models are scored in Model Serving and read in AI/BI and Genie One with full lineage.",
                    comps=["AI/BI", "Genie One", "Unity Catalog", "Investor Accounting", "Model Serving"],
                    stories=[
                        ["Credit loss forecasting reference architecture (CECL)", "https://www.databricks.com/resources/architectures/credit-loss-forecasting-reference-architecture"],
                        ["Databricks for Financial Services: lending and risk", "https://www.databricks.com/solutions/industries/financial-services"],
                    ],
                ),
            ],
        ),
        "sources": {
            "encompass": {"t": "ICE Mortgage Technology (Encompass LOS)", "u": "https://www.icemortgagetechnology.com/"},
            "blend": {"t": "Blend point-of-sale", "u": "https://blend.com/"},
            "ncino": {"t": "nCino Mortgage Suite", "u": "https://www.ncino.com/products/mortgage"},
            "meridianlink": {"t": "MeridianLink lending", "u": "https://www.meridianlink.com/"},
            "bkmsp": {"t": "Black Knight MSP servicing", "u": "https://en.wikipedia.org/wiki/Black_Knight,_Inc."},
            "sagent": {"t": "Sagent LoanServ", "u": "https://sagent.com/"},
            "du": {"t": "Fannie Mae Desktop Underwriter", "u": "https://singlefamily.fanniemae.com/applications-technology/desktop-underwriter-desktop-originator"},
            "lpa": {"t": "Freddie Mac Loan Product Advisor", "u": "https://sf.freddiemac.com/tools-learning/loan-advisor/our-solutions/loan-product-advisor"},
            "bureaus": {"t": "Credit bureau (tri-merge)", "u": "https://en.wikipedia.org/wiki/Credit_bureau"},
            "twn": {"t": "The Work Number (income and employment)", "u": "https://theworknumber.com/"},
            "ob": {"t": "Optimal Blue product and pricing engine", "u": "https://www.optimalblue.com/"},
            "mct": {"t": "Mortgage Capital Trading (MCT)", "u": "https://mct-trading.com/"},
            "gse": {"t": "Fannie Mae Loan Delivery", "u": "https://singlefamily.fanniemae.com/applications-technology/loan-delivery"},
            "mers": {"t": "MERS registry", "u": "https://www.mersinc.org/"},
            "hmda": {"t": "HMDA (CFPB)", "u": "https://www.consumerfinance.gov/data-research/hmda/"},
            "corelogic": {"t": "CoreLogic (Cotality) property data", "u": "https://www.corelogic.com/"},
            "qualia": {"t": "Qualia title and closing", "u": "https://www.qualia.com/"},
            "mismo": {"t": "MISMO data standards", "u": "https://www.mismo.org/"},
        },
    }
}
