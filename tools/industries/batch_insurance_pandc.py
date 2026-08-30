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


INDUSTRIES_BATCH_INSURANCE_PANDC = {
    "insurance_pandc": {
        "label": "Insurance (P&C)",
        "blurb": "Property and casualty carriers: underwriting and rating, policy administration and billing, first notice of loss and claims, catastrophe exposure, fraud, and loss reserving.",
        "medallion": medallion(
            "Raw policy, claims, telematics",
            "Policy transactions from PolicyCenter and Duck Creek, first notice of loss and claim notes from ClaimCenter, telematics trips, ISO loss costs and cat-model exposure files, landed exactly as received so a rate or a reserve can always be replayed as it stood.",
            "Conformed policy, claim, party",
            "Policies, claims, coverages, exposures and parties resolved into single conformed entities across policy admin, claims and billing, with agents, insureds and third parties matched and coverage terms reconciled to one policy version.",
            "Loss ratio, reserves, cat PML",
            "Contracted products underwriting, actuarial and finance run on: loss and combined ratio by line and segment, IBNR and case reserves, catastrophe exposure and PML, and subrogation recovery.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Policy Administration",
                    "ic": "erp",
                    "tiles": [
                        tile(
                            "Guidewire PolicyCenter",
                            "erp",
                            "The policy administration system of record: submissions, quotes, endorsements and renewals across personal and commercial lines, and the source of the policy and coverage.",
                            "guidewire-pc",
                            cat="P&C Core / Policy Admin System",
                            what="Holds the system-of-record for submissions, quotes, endorsements and renewals across personal and commercial lines, and emits every policy and coverage transaction.",
                            users="Underwriting Office, policy operations and Distribution & Agency teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "20-80 GB/day", "Nightly batch + intraday deltas"),
                                stream=flow(["semi-structured"], "hundreds of transactions/sec at peak", "Continuous CDC (near real-time)")),
                        ),
                        tile(
                            "Duck Creek Policy",
                            "erp",
                            "Cloud policy administration for rating, product configuration and policy lifecycle, the incumbent core where Guidewire is not.",
                            "duck-creek",
                            cat="P&C Core / Policy Admin System",
                            what="Cloud-based policy administration for rating, product configuration and the policy lifecycle, feeding the same policy and coverage entities where Duck Creek is the core.",
                            users="Underwriting Office, product configuration and policy operations teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "10-50 GB/day", "Nightly batch"),
                                stream=flow(["semi-structured"], "tens of transactions/sec", "Continuous CDC")),
                        ),
                        tile(
                            "Majesco P&C Core",
                            "erp",
                            "P&C core suite for policy, billing and claims used by carriers and MGAs, feeding the same policy and coverage entities.",
                            "majesco",
                            cat="P&C Core / Policy Admin System",
                            what="P&C core suite covering policy, billing and claims for carriers and MGAs, emitting policy, coverage and premium transactions into the estate.",
                            users="Policy operations, MGA program managers and Finance & Reinsurance teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-30 GB/day", "Nightly batch")),
                        ),
                        tile(
                            "Earnix Rating",
                            "market",
                            "Rating and pricing engine where rate plans, algorithms and price optimisation are configured and served into the quote path.",
                            "earnix",
                            cat="Rating & Price Optimization Engine",
                            what="Configures and serves rate plans, rating algorithms and price-optimisation factors into the quote path, and emits the rate and factor tables behind each price.",
                            users="Actuarial & Pricing, pricing analytics and Underwriting Office teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-5 GB/day rate tables + factors", "Daily / on rate change")),
                        ),
                    ],
                },
                {
                    "box": "Claims Systems",
                    "ic": "opdb",
                    "tiles": [
                        tile(
                            "Guidewire ClaimCenter",
                            "erp",
                            "The claims system of record: first notice of loss, adjuster notes, reserves and payments across the claim lifecycle.",
                            "guidewire-cc",
                            cat="Claims Management System",
                            what="System of record for the claim lifecycle: first notice of loss, adjuster notes, reserves and payments, emitting claim, reserve and payment transactions.",
                            users="Claims Leadership, field adjusters and SIU & Fraud teams.",
                            data_out=data_out(
                                batch=flow(["structured", "unstructured"], "15-60 GB/day incl. notes", "Nightly batch + intraday deltas"),
                                stream=flow(["semi-structured"], "hundreds of events/sec at peak", "Continuous CDC")),
                        ),
                        tile(
                            "Duck Creek Claims",
                            "erp",
                            "Claims management for intake, assignment and settlement used where Duck Creek is the incumbent core.",
                            "duck-creek-claims",
                            cat="Claims Management System",
                            what="Handles claim intake, assignment and settlement where Duck Creek is the incumbent core, feeding claim, reserve and payment records.",
                            users="Claims Leadership, field adjusters and claims operations teams.",
                            data_out=data_out(
                                batch=flow(["structured", "unstructured"], "5-30 GB/day incl. notes", "Nightly batch"),
                                stream=flow(["semi-structured"], "tens of events/sec", "Continuous CDC")),
                        ),
                        tile(
                            "CCC Intelligent Sol.",
                            "product",
                            "Auto physical-damage estimating, repair network and total-loss valuation feeding claim severity and cycle time.",
                            "ccc",
                            cat="Auto Physical-Damage Estimating Platform",
                            what="Produces auto physical-damage estimates, repair-network assignments and total-loss valuations that drive claim severity and cycle time.",
                            users="Claims Leadership, auto adjusters and material-damage teams.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "2-10 GB/day estimates + photos", "Daily feed"),
                                stream=flow(["semi-structured"], "tens of estimates/sec", "Continuous (API)")),
                        ),
                        tile(
                            "Snapsheet Claims",
                            "apps",
                            "Virtual and self-service claims: mobile FNOL, photo estimating and digital payments across the claim journey.",
                            "snapsheet",
                            cat="Virtual Claims / Digital FNOL Platform",
                            what="Runs virtual and self-service claims with mobile first-notice-of-loss, photo estimating and digital payments, emitting FNOL, photo and payment events.",
                            users="Claims Leadership, digital claims and customer-experience teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured", "unstructured"], "hundreds of events/sec incl. photos", "Continuous (mobile / API)")),
                        ),
                    ],
                },
                {
                    "box": "Billing & Distribution",
                    "ic": "custlake",
                    "tiles": [
                        tile(
                            "Guidewire Billing",
                            "erp",
                            "BillingCenter: direct and agency bill, invoicing, commissions and delinquency across the book.",
                            "guidewire-bc",
                            cat="Insurance Billing System",
                            what="Runs direct and agency billing, invoicing, commissions and delinquency across the book, emitting billing, payment and commission transactions.",
                            users="Finance & Reinsurance, billing operations and Distribution & Agency teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "5-20 GB/day", "Nightly billing cycle + intraday deltas")),
                        ),
                        tile(
                            "Salesforce FSC",
                            "crm",
                            "Financial Services Cloud for policyholder and agency relationships, service cases and next-best-action.",
                            "salesforce-fsc",
                            cat="Insurance CRM",
                            what="Holds policyholder and agency relationships, service cases and next-best-action across channels, emitting account, case and activity events.",
                            users="Distribution & Agency, service teams and Marketing teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-4 GB/day", "Hourly / nightly sync"),
                                stream=flow(["semi-structured"], "tens of events/sec", "Continuous CDC")),
                        ),
                        tile(
                            "Vertafore AMS360",
                            "sheet",
                            "Agency management system carrying agency-side policies, downloads and commissions into the carrier estate.",
                            "vertafore",
                            cat="Agency Management System",
                            what="Agency-side management system carrying policies, carrier downloads and commissions into the carrier estate, feeding agency book-of-business data.",
                            users="Distribution & Agency, agency operations and commission-accounting teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-3 GB/day", "Daily agency downloads")),
                        ),
                        tile(
                            "Applied Epic",
                            "sheet",
                            "Agency and brokerage management platform feeding submissions, bind requests and book-of-business data.",
                            "applied-epic",
                            cat="Agency Management System",
                            what="Agency and brokerage management platform feeding submissions, bind requests and book-of-business data into the carrier estate.",
                            users="Distribution & Agency, brokerage operations and new-business teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-3 GB/day", "Daily agency downloads")),
                        ),
                    ],
                },
                {
                    "box": "Risk & External Data",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "Verisk ISO",
                            "market",
                            "Industry statistical, loss-cost and policy-form reference against which rate plans and coverage language are built and validated.",
                            "verisk",
                            cat="Insurance Statistical & Loss-Cost Bureau",
                            what="Supplies industry statistical data, advisory loss costs and standard policy forms against which rate plans and coverage language are built and validated.",
                            users="Actuarial & Pricing, product filing and Underwriting Office teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs (reference + loss costs)", "Periodic circular / on release")),
                        ),
                        tile(
                            "LexisNexis Risk",
                            "partner",
                            "Motor vehicle records, prior claims, credit-based insurance scores and identity signals used at quote and renewal.",
                            "lexisnexis",
                            cat="Insurance Risk Data & Scoring Provider",
                            what="Provides motor vehicle records, prior-claims history, credit-based insurance scores and identity signals used at quote and renewal.",
                            users="Underwriting Office, Actuarial & Pricing and SIU & Fraud teams.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "1-3 GB/day", "Daily + on-demand pulls"),
                                stream=flow(["semi-structured"], "100s of API calls/sec", "Continuous (API at quote)")),
                        ),
                        tile(
                            "ISO ClaimSearch",
                            "gavel",
                            "The contributory P&C claims database and fraud-scoring network SIU and adjusters check every loss against.",
                            "iso-claimsearch",
                            cat="Contributory Claims Database & Fraud Network",
                            what="Contributory P&C claims database and fraud-scoring network every loss is matched against for prior-claims links and organised-fraud detection.",
                            users="SIU & Fraud, Claims Leadership and special-investigation teams.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "1-4 GB/day matches + scores", "Daily + on-demand"),
                                stream=flow(["semi-structured"], "tens of match calls/sec", "Continuous (API at FNOL)")),
                        ),
                    ],
                },
                {
                    "box": "Catastrophe Models",
                    "ic": "iot",
                    "tiles": [
                        tile(
                            "Moody's RMS",
                            "iot",
                            "Catastrophe models for hurricane, earthquake and flood: event sets, exceedance curves and PML by peril and region.",
                            "moodys-rms",
                            cat="Catastrophe Modeling Platform",
                            what="Runs catastrophe models for hurricane, earthquake and flood, producing event sets, exceedance curves and PML by peril and region.",
                            users="Underwriting Office, cat modelling and Finance & Reinsurance teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "10-100 GB/model run", "Periodic model runs + on-event")),
                        ),
                        tile(
                            "Verisk Touchstone",
                            "market",
                            "Catastrophe risk modelling platform for exposure, loss estimation and portfolio accumulation across perils.",
                            "verisk-touchstone",
                            cat="Catastrophe Modeling Platform",
                            what="Models exposure, loss estimation and portfolio accumulation across perils, producing modelled losses and accumulation views for the book.",
                            users="Underwriting Office, cat modelling and portfolio management teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "10-80 GB/model run", "Periodic model runs + on-event")),
                        ),
                        tile(
                            "CoreLogic Hazard",
                            "globe",
                            "Property characteristics and peril hazard data used to underwrite exposure at the address and geocode level.",
                            "corelogic",
                            cat="Property & Hazard Data Provider",
                            what="Supplies property characteristics and peril hazard data used to underwrite exposure at the address and geocode level.",
                            users="Underwriting Office, cat modelling and property-underwriting teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "GBs (property + hazard reference)", "Periodic refresh + on-demand")),
                        ),
                    ],
                },
                fed_group(
                    "Actuarial & Reserving",
                    "Reserving triangles, actuarial marts and reinsurance bordereaux left where they are and queried in place under Unity Catalog, which avoids a second copy of the booked reserves.",
                    cat="Actuarial Data Warehouse",
                    what="Legacy reserving triangles, actuarial marts and reinsurance bordereaux kept in the incumbent warehouse and queried in place through federation instead of being copied.",
                    users="Actuarial & Pricing, reserving actuaries and Finance & Reinsurance teams.",
                    data_out=data_out(
                        batch=flow(["structured"], "TB-scale historical marts", "Queried on demand (federated)")),
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "CMT Telematics",
                        "iot",
                        "Streaming driving events from the telematics provider: trips, hard-braking and mileage powering usage-based rate and claims reconstruction.",
                        "cmt",
                        cat="Telematics Data Provider",
                        what="Streams driving events from the telematics provider, trips, hard-braking and mileage, powering usage-based rate and claims reconstruction.",
                        users="Actuarial & Pricing, telematics/UBI and Claims Leadership teams.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "2-10k trip events/sec at peak", "Continuous trip stream")),
                    ),
                    tile(
                        "NOAA Weather Data",
                        "stream",
                        "Storm events, radar and peril feeds joined to exposure for catastrophe response and parametric triggers.",
                        "noaa",
                        cat="Weather & Peril Data Feed",
                        what="Supplies storm events, radar and peril feeds joined to exposure for catastrophe response and parametric trigger evaluation.",
                        users="Underwriting Office, cat response and Claims Leadership teams.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "100s of events/sec during events", "Continuous feed (event-driven)")),
                    ),
                    tile(
                        "Xactimate Estimating",
                        "product",
                        "Property loss and restoration estimates from the industry estimating standard, feeding claim severity and reserves.",
                        "xactware",
                        cat="Property Claims Estimating Platform",
                        what="Produces property loss and restoration estimates from the industry estimating standard, feeding claim severity and reserve setting.",
                        users="Claims Leadership, property adjusters and reserving teams.",
                        data_out=data_out(
                            batch=flow(["structured", "semi-structured"], "1-5 GB/day estimates", "Daily feed")),
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Underwriting Office",
                        "Genie One",
                        "The Chief Underwriting Officer on portfolio mix, rate adequacy and the combined ratio; the head of portfolio management on accumulation and appetite; the reinsurance buyer on ceded structure and PML.",
                        [
                            ["Genie One", "Ask what a segment's loss ratio or PML is this quarter without booking analyst time."],
                            ["AI/BI", "Combined ratio, rate adequacy and exposure on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the business glossary, so \"combined ratio\" and \"exposure\" mean one thing across the carrier."],
                        ],
                        sub=[
                            ["Chief Underwriting Officer", "portfolio mix, rate adequacy and the combined ratio."],
                            ["Portfolio Management", "accumulation, appetite and line-of-business steering."],
                            ["Reinsurance Buyer", "ceded structure, PML and treaty economics."],
                        ],
                        ucs=["Underwriting Triage", "Catastrophe Risk", "Pricing & Rating"],
                    ),
                    biz(
                        "Claims Leadership",
                        "Lakehouse//RT",
                        "The VP of claims on cycle time, leakage and loss-adjustment expense; the SIU and fraud lead on referral quality and recovery; field adjusting on assignment, severity and reserve accuracy.",
                        [
                            ["Claims Command Center", "Severity and fraud scores on a claim before it is assigned."],
                            ["Lakehouse//RT", "Live claim, telematics and photo state at the latency a claim moves at."],
                            ["Model Serving", "Severity and fraud models scored inside the claims path."],
                        ],
                        sub=[
                            ["VP Claims", "cycle time, leakage and loss-adjustment expense."],
                            ["SIU & Fraud", "referral quality, recovery and organised-fraud rings."],
                            ["Field Adjusting", "assignment, severity and reserve accuracy."],
                        ],
                        ucs=["Claims Automation", "Fraud Detection (SIU)", "Subrogation Recovery"],
                    ),
                    biz(
                        "Actuarial & Pricing",
                        "Model Serving",
                        "Pricing actuaries setting rate plans against ISO loss costs and the filed rate; reserving actuaries booking IBNR and case reserves; the telematics team turning driving behaviour into usage-based rate.",
                        [
                            ["Pricing Workbench", "Rate adequacy and loss-cost trend before a rate change is filed."],
                            ["Model Serving", "GLM and willingness-to-pay models scored in the quote path."],
                            ["MLflow", "Every rate and reserving model versioned for the filing and audit."],
                        ],
                        sub=[
                            ["Chief Actuary", "rate adequacy, reserve strength and the filed rate plan."],
                            ["Pricing Actuary", "segment rate, loss cost and competitive position."],
                            ["Reserving Actuary", "IBNR, case reserves and development triangles."],
                        ],
                        ucs=["Pricing & Rating", "Loss Reserving", "Telematics & UBI"],
                    ),
                    biz(
                        "Distribution & Agency",
                        "AI/BI",
                        "The chief distribution officer on agency production and mix; agency managers on quote-to-bind, retention and loss ratio by agent; the direct and digital team on quote conversion and customer lifetime value.",
                        [
                            ["AI/BI", "Production, quote-to-bind and retention on certified Metric Views."],
                            ["Genie One", "Ask which agencies are growing off-appetite this month without a report pull."],
                            ["Model Serving", "Retention and cross-sell propensity scored per policyholder."],
                        ],
                        sub=[
                            ["Chief Distribution Officer", "agency production, mix and channel economics."],
                            ["Agency Managers", "quote-to-bind, retention and loss ratio by agent."],
                            ["Direct & Digital", "quote conversion and customer lifetime value."],
                        ],
                        ucs=["Customer 360", "Underwriting Triage", "Pricing & Rating"],
                    ),
                    biz(
                        "Finance & Reinsurance",
                        "AI/BI",
                        "The CFO on combined ratio, capital and investor reporting; the ceded-reinsurance team on treaty recoveries and bordereaux; investor reporting on statutory, IFRS 17 and solvency results.",
                        [
                            ["AI/BI", "Combined ratio, capital and ceded recoveries on certified views."],
                            ["Genie One", "Ask what ceded recoveries are outstanding this quarter without a finance pull."],
                            ["Unity Catalog", "One definition of premium, loss and reserve across finance and actuarial."],
                        ],
                        sub=[
                            ["CFO", "combined ratio, capital and the investor story."],
                            ["Ceded Reinsurance", "treaty recoveries, bordereaux and reinstatement."],
                            ["Investor Reporting", "statutory, IFRS 17 and solvency results."],
                        ],
                        ucs=["Reinsurance Analytics", "Loss Reserving", "Catastrophe Risk"],
                    ),
                ],
                [
                    biz(
                        "Actuarial Engineering",
                        "Lakeflow",
                        "Land policy, claims, billing and bordereaux extracts from Guidewire and Duck Creek, build loss-development triangles and exposure tables; own Bronze to Silver and the pager when the reserving and pricing tables stall.",
                        [
                            ["Lakeflow Connect", "Managed connectors for policy admin, claims and billing cores."],
                            ["Lakeflow Designer", "Declarative pipelines with expectations on premium and loss feeds."],
                            ["Lakewatch", "Freshness on the triangles and exposure tables actuaries read each close."],
                        ],
                    ),
                    biz(
                        "Claims ML Engineers",
                        "MLflow",
                        "Severity, fraud-propensity and image-damage models built from ClaimSearch, telematics and loss photos through CCC and Snapsheet; whether they still hold as fraud patterns and repair costs shift.",
                        [
                            ["Feature Store", "Claim, party and telematics features read identically in training and serving."],
                            ["MLflow", "Every severity and fraud model tracked for audit and reproduction."],
                            ["Model Serving", "Severity and fraud models scored inside the claims path."],
                        ],
                    ),
                    biz(
                        "Pricing Analytics",
                        "Model Serving",
                        "GLM and gradient-boosted pricing models built in the lakehouse and pushed into the Earnix rating engine, tested against ISO loss costs and the filed rate plan before a rate change is bound.",
                        [
                            ["Model Serving", "Rating and willingness-to-pay models scored in the quote path."],
                            ["MLflow", "Every rate model versioned against the filed plan for audit."],
                            ["AI/BI", "Rate adequacy and loss-cost trends on certified Metric Views."],
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
                                "Underwriting, claims and finance dashboards against serverless SQL with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for governed answers on loss ratio, reserves and cat exposure in the channel the business already works in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Actuarial and data-science notebooks and IDEs against governed policy, claim and exposure data.",
                            ),
                        ],
                    },
                    {
                        "box": "Distribution & Partners",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "Agent & Broker Portal",
                                "api",
                                "Quote status, appetite and book-of-business insight served to agencies and brokers over governed APIs.",
                            ),
                            tile(
                                "Reinsurer Data Sharing",
                                "share",
                                "Exposure, bordereaux and loss data shared to reinsurers and brokers over Delta Sharing rather than file exchange.",
                            ),
                            tile(
                                "Salesforce Activation",
                                "crm",
                                "Retention and cross-sell signals written back to Financial Services Cloud for service and sales action.",
                                "salesforce-fsc",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "PolicyCenter Writeback",
                                "erp",
                                "Rating, renewal and appetite decisions written back into the policy admin system so the answer reaches the quote path.",
                                "guidewire-pc",
                            ),
                            tile(
                                "ClaimCenter Writeback",
                                "erp",
                                "Severity, fraud and reserve recommendations written into the claims system engineering already works in.",
                                "guidewire-cc",
                            ),
                            tile(
                                "Rating Engine Sync",
                                "market",
                                "Model outputs and price-optimisation factors synced into the rating engine behind the quote.",
                                "earnix",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "Statutory & NAIC",
                                "gavel",
                                "Statutory statements and state rate and market-conduct filings produced from the same governed tables the carrier runs on.",
                            ),
                            tile(
                                "IFRS 17 & Solvency",
                                "sheet",
                                "Reserving, solvency and IFRS 17 reporting filed from contracted Gold products.",
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
                                "Reinsurers, MGAs and audit partners reading live tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ],
                genie_spaces=[
                    genie("Underwriting & Pricing", "Ask about portfolio mix, rate adequacy and loss ratio by segment in plain language.",
                          feeds=["Guidewire PolicyCenter", "Earnix Rating", "Verisk ISO", "Loss ratio, reserves, cat PML"],
                          teams=["Underwriting Office", "Actuarial & Pricing", "Chief Underwriting Officer"],
                          questions=[
                              "What is our loss ratio by line of business and segment this quarter?",
                              "Which segments are showing the weakest rate adequacy right now?",
                              "How has written premium grown by product versus last year?",
                              "Which agencies are binding business off our stated appetite?",
                              "What is the combined ratio trend by line over the last four quarters?"]),
                    genie("Claims & Fraud", "Explore cycle time, severity, leakage and SIU referrals across the claims book.",
                          feeds=["Guidewire ClaimCenter", "CCC Intelligent Sol.", "ISO ClaimSearch", "Conformed policy, claim, party"],
                          teams=["Claims Leadership", "SIU & Fraud", "Field Adjusting"],
                          questions=[
                              "What is average claim cycle time by line and severity band?",
                              "Which open claims have the highest fraud score right now?",
                              "Where is leakage running above target across the book?",
                              "How accurate are our initial reserves versus final paid by line?",
                              "Which claims have ClaimSearch links to prior losses on other policies?"]),
                    genie("Catastrophe & Reinsurance", "Ask about exposure, PML and ceded recoveries by peril and treaty.",
                          feeds=["Moody's RMS", "Verisk Touchstone", "CoreLogic Hazard", "Loss ratio, reserves, cat PML"],
                          teams=["Underwriting Office", "Finance & Reinsurance", "Reinsurance Buyer"],
                          questions=[
                              "What is our gross and net PML by peril and region today?",
                              "Which counties drive the most hurricane accumulation in the book?",
                              "How much ceded recovery is outstanding on the last cat event?",
                              "What is our net position after the current reinsurance program?",
                              "Where has exposure grown fastest against appetite this year?"]),
                    genie("Distribution & Retention", "Answer agency production, quote-to-bind and retention questions across channels.",
                          feeds=["Salesforce FSC", "Applied Epic", "Guidewire Billing", "Conformed policy, claim, party"],
                          teams=["Distribution & Agency", "Agency Managers", "Direct & Digital"],
                          questions=[
                              "What is quote-to-bind by agency and product this month?",
                              "Which agencies have the best retention and loss ratio combined?",
                              "Where are policies lapsing for billing or delinquency reasons?",
                              "Which policyholders look like cross-sell candidates by segment?",
                              "What is quote conversion in the direct and digital channel?"]),
                ],
                dashboards=[
                    dashboard("Combined Ratio & Rate Adequacy", "Loss and combined ratio, rate adequacy and premium on certified underwriting Metric Views.",
                              kpis=["Loss ratio", "Combined ratio", "Rate adequacy", "Written premium", "Retention rate"],
                              teams=["Underwriting Office", "Actuarial & Pricing", "Finance & Reinsurance"]),
                    dashboard("Claims Performance", "Cycle time, loss-adjustment expense, leakage and reserve accuracy across the claims book.",
                              kpis=["Cycle time", "Loss-adjustment expense", "Leakage", "Claim severity", "Reserve accuracy"],
                              teams=["Claims Leadership", "Field Adjusting", "SIU & Fraud"]),
                    dashboard("Catastrophe Exposure & PML", "Modelled PML, accumulation and ceded recoveries by peril and treaty.",
                              kpis=["Gross PML", "Net PML", "Accumulation", "Ceded recoveries", "Reinstatement cost"],
                              teams=["Underwriting Office", "Finance & Reinsurance", "Reinsurance Buyer"]),
                    dashboard("Distribution & Growth", "Agency production, quote-to-bind, retention and loss ratio by agent.",
                              kpis=["Quote-to-bind", "Retention rate", "Loss ratio by agent", "New business premium", "Customer lifetime value"],
                              teams=["Distribution & Agency", "Agency Managers", "Chief Distribution Officer"]),
                ],
            ),
        },
        "top": top_band(
            [
                app(
                    "Claims Command Center",
                    "Triage & severity",
                    "gauge",
                    "The screen the claims desk runs the day from: severity, fraud and subrogation scores on every open claim, next-best-action and reserve guidance, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Underwriting Workbench",
                    "Submission triage",
                    "market",
                    "Where underwriters see the submission scored against appetite, prior claims and exposure before they quote, with ISO and hazard data joined in one view.",
                ),
                app(
                    "Cat Response Console",
                    "Event exposure",
                    "iot",
                    "Live catastrophe exposure by peril and geography as a storm tracks, so claims, reinsurance and customer teams mobilise against the book actually in the footprint.",
                ),
                app(
                    "Fraud & SIU Console",
                    "Investigations",
                    "gavel",
                    "Referrals ranked by fraud score with the ClaimSearch and network links that support them, so SIU works the strongest cases first.",
                ),
            ],
            [
                uc(
                    "Claims Automation",
                    "Claims",
                    "gauge",
                    "Straight-through processing of low-complexity claims with severity scoring and next-best-action, so adjusters spend their time on the claims that need them.",
                    problem="Claims arrive as FNOL calls, photos, PDFs and telematics across different systems; triaged by hand, simple claims wait behind complex ones and leakage and cycle time run away.",
                    who="Claims Leadership",
                    how="Policy, claim and telematics feeds land through Lakeflow; severity is scored in Model Serving and documents parsed with Document Intelligence, and the Claims Command Center on Lakebase drives assignment and reserves.",
                    comps=["Claims Command Center", "Guidewire ClaimCenter", "AI Functions", "Model Serving", "Lakebase"],
                    stories=[
                        ["Smart Claims: automating P&C claims on Databricks", "https://www.databricks.com/solutions/accelerators/smart-claims-for-insurance"],
                        ["Smart Claims end-to-end processing demo", "https://www.databricks.com/resources/demos/tutorials/lakehouse-platform/dbdemos-fsi-smart-claims"],
                    ],
                ),
                uc(
                    "Fraud Detection (SIU)",
                    "Fraud",
                    "gavel",
                    "Scoring every loss against contributory claims history and network links so organised and opportunistic fraud is referred to SIU early, not after it is paid.",
                    problem="Fraud is caught late or by intuition; without checking each loss against the industry claims network and party links, rings pay out before a referral is ever raised.",
                    who="Claims Leadership",
                    how="Claims are matched against ISO ClaimSearch and LexisNexis signals in the lakehouse; fraud-propensity models score referrals in Model Serving and Lakehouse//RT feeds the Fraud & SIU Console.",
                    comps=["Fraud & SIU Console", "ISO ClaimSearch", "LexisNexis Risk", "Model Serving", "Lakehouse//RT"],
                    stories=[
                        ["Smart Claims: fraud scoring for insurers on Databricks", "https://www.databricks.com/solutions/accelerators/smart-claims-for-insurance"],
                    ],
                ),
                uc(
                    "Underwriting Triage",
                    "Underwriting",
                    "market",
                    "Scoring submissions against appetite, prior claims and exposure before quote, so underwriters spend time on the risks worth writing.",
                    problem="Submissions come in faster than they can be worked, and prior-claims, MVR and exposure context sits in separate systems, so good risks are missed and off-appetite risks bound.",
                    who="Underwriting Office",
                    how="PolicyCenter submissions are enriched with Verisk ISO and hazard data in the lakehouse; appetite and win-propensity are scored with AI Functions and Model Serving in the Underwriting Workbench.",
                    comps=["Underwriting Workbench", "Guidewire PolicyCenter", "Verisk ISO", "AI Functions", "Model Serving"],
                    stories=[
                        ["Gjensidige advances underwriting precision with Databricks", "https://www.databricks.com/customers/gjensidige"],
                    ],
                ),
                uc(
                    "Pricing & Rating",
                    "Pricing",
                    "chart",
                    "Moving from static annual rate tables to segmented, model-driven rate served into the quote, tested against loss costs and the filed plan.",
                    problem="Static rate plans cannot express true risk, so rate is inadequate on some segments and uncompetitive on others, and every change waits on a slow filing cycle.",
                    who="Actuarial & Pricing",
                    how="ISO loss costs and internal experience are conformed in the lakehouse; GLM and gradient-boosted models tracked in MLflow score through Model Serving into the Earnix rating engine, on definitions certified in Unity Catalog.",
                    comps=["Earnix Rating", "Model Serving", "MLflow", "AI/BI", "Unity Catalog"],
                    stories=[
                        ["Gjensidige runs one common pricing platform on Databricks", "https://www.databricks.com/customers/gjensidige"],
                    ],
                ),
                uc(
                    "Catastrophe Risk",
                    "Exposure",
                    "iot",
                    "Portfolio exposure and PML by peril from cat models and hazard data, so accumulation and reinsurance are managed before the season, not after the event.",
                    problem="Exposure sits in modelling silos and stale extracts; accumulation and PML cannot be seen across the live book, so the carrier learns its concentration only when the storm lands.",
                    who="Underwriting Office",
                    how="Moody's RMS and Verisk Touchstone event sets and CoreLogic hazard are joined to the live exposure in the lakehouse; PML and accumulation are explored in AI/BI and surfaced in the Cat Response Console.",
                    comps=["Cat Response Console", "Moody's RMS", "Verisk Touchstone", "CoreLogic Hazard", "AI/BI"],
                    stories=[
                        ["Catastrophe modeling reference architecture for insurance", "https://www.databricks.com/resources/architectures/catastrophe-modeling-reference-architecture-for-insurance"],
                    ],
                ),
                uc(
                    "Telematics & UBI",
                    "Usage-based",
                    "stream",
                    "Turning streaming driving behaviour into usage-based rate and claims reconstruction, priced on how a policyholder actually drives.",
                    problem="Usage-based programmes generate high-frequency trip data that batch pipelines cannot land cleanly or fast enough, so pricing signals arrive late and trip quality is unproven.",
                    who="Actuarial & Pricing",
                    how="Telematics trips stream into Lakehouse//RT with quality checks; behaviour features are defined once in Feature Store and scored through Model Serving for UBI rate, on pipelines built in Lakeflow.",
                    comps=["CMT Telematics", "Lakehouse//RT", "Model Serving", "Feature Store", "Lakeflow"],
                    stories=[
                        ["Smart Claims ingests telematics for usage-based insurance", "https://www.databricks.com/resources/demos/tutorials/lakehouse-platform/dbdemos-fsi-smart-claims"],
                    ],
                ),
                uc(
                    "Loss Reserving",
                    "Actuarial",
                    "sheet",
                    "Building development triangles and IBNR from conformed claims and premium, so reserves are strengthened or released on current data, not a quarter-old extract.",
                    problem="Reserving runs on hand-built triangles from stale extracts; by the time IBNR is booked the picture has moved, and the working is hard to audit or reproduce.",
                    who="Actuarial & Pricing",
                    how="Claims and premium are conformed to certified Gold; triangles and IBNR models tracked in MLflow run against the Actuarial & Reserving marts and are published through AI/BI on Unity Catalog definitions.",
                    comps=["Actuarial & Reserving", "MLflow", "AI/BI", "Unity Catalog", "Model Serving"],
                    stories=[
                        ["Milliman accelerates actuarial modeling on Databricks", "https://www.databricks.com/customers/milliman"],
                    ],
                ),
                uc(
                    "Subrogation Recovery",
                    "Recovery",
                    "partner",
                    "Finding the claims where a third party is liable and pursuing recovery, before the subrogation window closes and the money is lost.",
                    problem="Subrogation opportunities hide in adjuster notes and documents; identified late or missed, recoverable dollars are written off and never pursued.",
                    who="Claims Leadership",
                    how="Claim notes and documents are parsed with Document Intelligence and AI Functions; a recovery-propensity model scores each claim in Model Serving and flags candidates in the claims workflow on Lakebase.",
                    comps=["Guidewire ClaimCenter", "Agent Bricks", "AI Functions", "Model Serving", "Lakebase"],
                ),
                uc(
                    "Customer 360",
                    "Retention",
                    "custlake",
                    "One governed view of the policyholder across policy, billing, claims and service, so retention and cross-sell are proactive rather than guesswork.",
                    problem="Customer data is siloed across policy admin, billing, claims and CRM, so churn prediction is unreliable, service is reactive, and cross-sell is a guess.",
                    who="Distribution & Agency",
                    how="Policy, claim and service data are unified through CustomerLake without a separate CDP; retention and cross-sell propensity are scored in Model Serving and activated into Salesforce FSC, explored in AI/BI and Genie One.",
                    comps=["CustomerLake", "Salesforce FSC", "Model Serving", "AI/BI", "Genie One"],
                    stories=[
                        ["Allianz Direct improves customer satisfaction with Databricks", "https://www.databricks.com/customers/allianz-direct"],
                        ["Storebrand unifies customer data on Databricks", "https://www.databricks.com/customers/storebrand"],
                        ["Nationwide transforms data into member value", "https://www.databricks.com/customers/nationwide"],
                    ],
                ),
                uc(
                    "Reinsurance Analytics",
                    "Ceded risk",
                    "share",
                    "Measuring ceded structure, treaty recoveries and net PML, and sharing exposure with reinsurers on live tables rather than spreadsheets.",
                    problem="Ceded exposure and treaty recoveries live in spreadsheets and file exchanges, so net position is unclear at renewal and recoveries are chased manually after the loss.",
                    who="Finance & Reinsurance",
                    how="Gross exposure, cat output and recoveries are conformed in the lakehouse against the Actuarial & Reserving marts; net PML and treaty economics are analysed in AI/BI on Unity Catalog definitions and shared to reinsurers over OpenSharing.",
                    comps=["Actuarial & Reserving", "OpenSharing", "AI/BI", "Unity Catalog", "Moody's RMS"],
                    stories=[
                        ["Milliman powers actuarial and risk analytics on Databricks", "https://www.databricks.com/customers/milliman"],
                        ["Design patterns for batch processing in financial services", "https://www.databricks.com/blog/2023/01/09/design-patterns-batch-processing-financial-services.html"],
                    ],
                ),
            ],
        ),
        "sources": {
            "guidewire-pc": {"t": "Guidewire PolicyCenter", "u": "https://www.guidewire.com/products/policycenter"},
            "guidewire-cc": {"t": "Guidewire ClaimCenter", "u": "https://www.guidewire.com/products/claimcenter"},
            "guidewire-bc": {"t": "Guidewire BillingCenter", "u": "https://www.guidewire.com/products/billingcenter"},
            "duck-creek": {"t": "Duck Creek Policy", "u": "https://www.duckcreek.com/solutions/policy/"},
            "duck-creek-claims": {"t": "Duck Creek Claims", "u": "https://www.duckcreek.com/solutions/claims/"},
            "majesco": {"t": "Majesco P&C Core", "u": "https://www.majesco.com/property-casualty/"},
            "earnix": {"t": "Earnix rating and pricing", "u": "https://earnix.com/"},
            "ccc": {"t": "CCC Intelligent Solutions", "u": "https://www.cccis.com/"},
            "snapsheet": {"t": "Snapsheet virtual claims", "u": "https://www.snapsheetclaims.com/"},
            "salesforce-fsc": {"t": "Salesforce Financial Services Cloud", "u": "https://www.salesforce.com/financial-services/"},
            "vertafore": {"t": "Vertafore AMS360", "u": "https://www.vertafore.com/products/ams360"},
            "applied-epic": {"t": "Applied Epic", "u": "https://www1.appliedsystems.com/en-us/applied-epic/"},
            "verisk": {"t": "Verisk ISO", "u": "https://www.verisk.com/"},
            "lexisnexis": {"t": "LexisNexis Risk Solutions for insurance", "u": "https://risk.lexisnexis.com/insurance"},
            "iso-claimsearch": {"t": "Verisk ISO ClaimSearch", "u": "https://www.verisk.com/products/claimsearch/"},
            "verisk-touchstone": {"t": "Verisk Touchstone catastrophe modelling", "u": "https://www.verisk.com/products/touchstone/"},
            "moodys-rms": {"t": "Moody's RMS catastrophe models", "u": "https://www.rms.com/"},
            "corelogic": {"t": "CoreLogic property and hazard data", "u": "https://www.corelogic.com/"},
            "cmt": {"t": "Cambridge Mobile Telematics", "u": "https://www.cmtelematics.com/"},
            "noaa": {"t": "NOAA / National Weather Service", "u": "https://www.weather.gov/"},
            "xactware": {"t": "Verisk Xactimate estimating", "u": "https://www.xactware.com/"},
        },
    }
}
