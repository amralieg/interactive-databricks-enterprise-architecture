import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    """Business tiles plus an explicit, industry-specific Technical group of 3."""
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_GAMING = {
    'gaming': {
        "label": "Gaming",
        "blurb": "Interactive entertainment and iGaming: player lifecycle, in-game economy, live ops, fraud and responsible gaming compliance.",
        "medallion": medallion(
            "Raw event streams",
            "Client telemetry, payment authorisations, KYC decisions, game server events and marketing sends, landed exactly as received so a session or a wager can always be replayed.",
            "Conformed player, session",
            "Players, devices, sessions and titles resolved into single conformed entities across platform, payments and CRM, with cross-device identity stitched to one profile.",
            "ARPDAU, LTV, churn",
            "Contracted products product and finance run on: ARPDAU and payer conversion, cohort LTV, churn and reactivation, and fraud loss rate.",
        ),
        "rails": {
            "src": [
                {"box": "Game Platform & Live", "ic": "stream", "tiles": [
                    tile("Unity Gaming Services", "api", "Player authentication, economy transactions and live ops configuration events.", "unity-gaming"),
                    tile("PlayFab Backend", "db", "Title data, inventory, matchmaking and leaderboard state for cross-platform games.", "playfab"),
                    tile("Custom Game Servers", "iot", "Authoritative match and session logs from dedicated and listen servers at tick resolution.")
                ]},
                {"box": "Payments & Wallet", "ic": "market", "tiles": [
                    tile("Adyen Payments", "market", "Card, wallet and local payment method authorisations, chargebacks and settlements.", "adyen"),
                    tile("Paysafe Skrill", "partner", "Digital wallet deposits and withdrawals for regulated iGaming markets.", "paysafe"),
                    tile("Pragmatic Play RGS", "product", "Remote game server rounds, bet outcomes and jackpot contributions for casino content.", "pragmatic")
                ]},
                {"box": "Player CRM & Support", "ic": "custlake", "tiles": [
                    tile("Salesforce Gaming CRM", "custlake", "Player segments, campaign responses and VIP host notes.", "sf-gaming"),
                    tile("Zendesk Player Support", "chat", "Tickets, chat transcripts and refund disputes tied to player accounts.", "zendesk"),
                    tile("Braze Lifecycle", "partner", "Push, email and in-app message sends with delivery and conversion events.", "braze")
                ]},
                {"box": "Fraud & Compliance", "ic": "gavel", "tiles": [
                    tile("SEON Fraud Prevention", "gauge", "Device fingerprinting, velocity rules and chargeback signals at registration and deposit.", "seon"),
                    tile("Onfido Identity", "people", "Document verification and biometric checks for KYC and age gating.", "onfido"),
                    tile("GeoComply Location", "globe", "Geolocation compliance pings proving the player is in an permitted jurisdiction.", "geocomply")
                ]},
                fed_group(
                    "Publisher Revenue Share",
                    "Third-party title royalty ledgers left at partners and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("AppsFlyer Attribution", "api", "Install and in-app event attribution consumed inbound for UA spend optimisation.", "appsflyer"),
                tile("Steam & Console APIs", "partner", "Platform achievement, entitlement and sales reports normalised on ingest."),
                tile("Regulator GGR Feeds", "gavel", "Jurisdictional gross gaming revenue file layouts validated before submission windows.")
            ]),
            "ppl": ppl2([
                biz("CEO & CFO", "Genie One", "The CEO on MAU, payer conversion and studio ROI; the CFO on gross gaming revenue, hold percentage and chargeback loss rate.",
                    [["Genie One", "Ask what yesterday's ARPDAU was by title without waiting on analytics."], ["AI/BI", "Revenue, retention and fraud on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"active player\" means one thing across titles."]]),
                biz("Live Ops & Product", "Model Serving", "Live-ops managers on event-calendar performance, economy sink-and-source balance and how each content release moves retention and spend.",
                    [["Live Ops Console", "Event performance and economy sinks before the next patch ships."], ["Model Serving", "Churn and LTV models scored per cohort."], ["AI/BI", "Funnel and engagement on governed definitions."]]),
                biz("Player Experience", "CustomerLake", "Community and VIP host teams on player sentiment, complaint drivers and the high-value accounts worth saving before they churn.",
                    [["Player 360", "Support history, spend and play patterns in one view."], ["CustomerLake", "Segments and activations without copying profiles into a separate CDP."], ["Genie One", "Ask which VIP accounts opened tickets after the last update."]]),
                biz("Risk & Compliance", "AI/BI", "Fraud analysts and compliance officers on AML and SAR alerts, self-exclusion enforcement and jurisdictional filings before payouts release.",
                    [["Fraud Command Centre", "Velocity and device clusters flagged before payouts release."], ["AI/BI", "Chargeback and SAR metrics on certified Metric Views."], ["Unity Catalog", "One definition of GGR across platform and RGS."]]),
                biz("Marketing & UA", "AI/BI", "User acquisition on CPI, ROAS and creative performance by channel and geography, reallocating spend before daily budgets exhaust.",
                    [["UA Optimiser", "Spend reallocation scenarios before daily budgets exhaust."], ["AI/BI", "ROAS and cohort payback the growth team reads."], ["Model Serving", "LTV models informing bid caps."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the game platform, payments and CRM event streams; own the Bronze to Silver path and the pager when telemetry breaks.",
                    [["Lakeflow Connect", "Managed connectors for platform, payment and CRM sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on telemetry and payment feeds."], ["Lakewatch", "Freshness on the tables live ops and risk teams read every morning."]]),
                biz("Data Scientists", "MLflow", "Churn, LTV, fraud and matchmaking models, and whether they still hold a season after each content patch.",
                    [["Feature Store", "Player features defined once and read identically in training and serving."], ["MLflow", "Every churn and fraud run tracked for audit and reproduction."], ["Model Serving", "LTV and fraud models scored in the live player path."]]),
                biz("App Developers", "Apps", "Ship the live ops, player 360 and fraud command applications the studio works in, hosted next to governed data.",
                    [["Apps", "Live ops and risk screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for economy config and case writes."], ["Agent Bricks", "Agents that draft a live ops tweak or fraud case against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and live ops alerts in the channel teams already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Platform Writeback", "ic": "opdb", "tiles": [
                    tile("Economy Config Push", "api", "Live ops price and drop-rate changes written back into title configuration after simulation.", "playfab"),
                    tile("Fraud Block Lists", "gauge", "Device and payment instrument blocks pushed to the authorisation path in near real time.", "seon"),
                    tile("CRM Campaign Triggers", "custlake", "Win-back and VIP offers triggered from governed segments without nightly exports.", "braze")
                ]},
                {"box": "Studio & Platform", "ic": "partner", "tiles": [
                    tile("Publisher Analytics Share", "share", "Title performance and royalty positions shared with external studios over Delta Sharing."),
                    tile("RGS Content Partners", "product", "Round-level GGR and jackpot feeds exchanged with remote game server providers.", "pragmatic"),
                    tile("Affiliate Networks", "partner", "Acquisition partner reporting reconciled against attributed deposits and NGR.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("GGR Regulatory Filings", "gavel", "Jurisdictional gross gaming revenue and responsible gaming reports produced from governed tables."),
                    tile("AML & SAR Reporting", "share", "Suspicious activity metrics filed from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Studios, affiliates and regulators reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Live Ops Console", "Event management", "gauge", "Economy balance, event calendars and cohort impact before and after each content release."),
                app("Player 360", "Support & VIP", "custlake", "Play, spend, support and risk history on one screen for hosts and community managers."),
                app("Fraud Command Centre", "Risk operations", "stream", "Velocity clusters, bonus abuse and chargeback patterns flagged before withdrawals approve."),
                app("UA Optimiser", "Acquisition spend", "market", "Channel and creative performance scored against predicted LTV before daily budgets lock."),
            ],
            [
                uc("Player Churn Prediction", "Retention", "gauge", "Identifying players likely to lapse from session decay and economy frustration before they uninstall."),
                uc("LTV & Monetisation", "Revenue", "market", "Cohort lifetime value and payer conversion scored per acquisition channel and title."),
                uc("Live Ops Balancing", "Economy", "sheet", "Sink and source tuning tested against simulated economy health before patches ship."),
                uc("Fraud & Bonus Abuse", "Risk", "stream", "Multi-accounting, collusion and promo abuse detected from device, payment and play graphs."),
                uc("Responsible Gaming", "Compliance", "gavel", "Self-exclusion, deposit limits and harm markers enforced from governed player state."),
                uc("Matchmaking Quality", "Engagement", "people", "Queue times and match fairness optimised without opening exploit vectors."),
                uc("Content Personalisation", "Live ops", "custlake", "Offers and events targeted per player segment from in-game behaviour, not batch exports."),
                uc("Chargeback Prevention", "Payments", "market", "High-risk instruments and behaviours blocked before authorisation settles."),
                uc("Regulatory GGR", "Reporting", "gavel", "Jurisdiction-accurate gross gaming revenue reconciled across platform and RGS content."),
                uc("Studio Royalty", "Partners", "product", "Third-party title revenue share calculated from governed round and jackpot data."),
            ],
        ),
        "sources": {
            "unity-gaming": {"t": "Unity Gaming Services", "u": "https://unity.com/solutions/gaming-services"},
            "playfab": {"t": "Microsoft PlayFab", "u": "https://playfab.com/"},
            "adyen": {"t": "Adyen payments platform", "u": "https://www.adyen.com/"},
            "paysafe": {"t": "Paysafe digital wallets", "u": "https://www.paysafe.com/"},
            "pragmatic": {"t": "Pragmatic Play", "u": "https://www.pragmaticplay.com/"},
            "sf-gaming": {"t": "Salesforce for gaming", "u": "https://www.salesforce.com/solutions/industries/"},
            "zendesk": {"t": "Zendesk customer service", "u": "https://www.zendesk.com/"},
            "braze": {"t": "Braze customer engagement", "u": "https://www.braze.com/"},
            "seon": {"t": "SEON fraud prevention", "u": "https://seon.io/"},
            "onfido": {"t": "Onfido identity verification", "u": "https://onfido.com/"},
            "geocomply": {"t": "GeoComply geolocation compliance", "u": "https://www.geocomply.com/"},
            "appsflyer": {"t": "AppsFlyer mobile attribution", "u": "https://www.appsflyer.com/"}
        },
    },
}
