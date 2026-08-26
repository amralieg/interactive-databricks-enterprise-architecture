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
                    [["Genie One", "Ask what yesterday's ARPDAU was by title without waiting on analytics."], ["AI/BI", "Revenue, retention and fraud on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"active player\" means one thing across titles."]],
                    sub=[
                        ["CEO", "MAU, payer conversion and the studio ROI behind each live title."],
                        ["CFO & Finance", "gross gaming revenue, hold percentage and chargeback loss rate."],
                        ["Head of Studios", "which titles earn their live-ops investment and which to sunset."],
                    ],
                    ucs=["LTV & Monetisation", "Regulatory GGR", "Studio Royalty", "Chargeback Prevention"]),
                biz("Live Ops & Product", "Model Serving", "Live-ops managers on event-calendar performance, economy sink-and-source balance and how each content release moves retention and spend.",
                    [["Live Ops Console", "Event performance and economy sinks before the next patch ships."], ["Model Serving", "Churn and LTV models scored per cohort."], ["AI/BI", "Funnel and engagement on governed definitions."]],
                    sub=[
                        ["Live Ops Manager", "event calendars and how each release moves retention and spend."],
                        ["Economy Designer", "sink-and-source balance so the in-game economy stays healthy."],
                        ["Retention Lead", "cohort drop-off and the win-back that actually pulls players back."],
                    ],
                    ucs=["Live Ops Balancing", "Player Churn Prediction", "Content Personalisation", "Matchmaking Quality"]),
                biz("Player Experience", "CustomerLake", "Community and VIP host teams on player sentiment, complaint drivers and the high-value accounts worth saving before they churn.",
                    [["Player 360", "Support history, spend and play patterns in one view."], ["CustomerLake", "Segments and activations without copying profiles into a separate CDP."], ["Genie One", "Ask which VIP accounts opened tickets after the last update."]],
                    sub=[
                        ["Community Manager", "sentiment, complaint drivers and the health of the player base."],
                        ["VIP Host", "the high-value accounts worth saving before they churn."],
                        ["Player Support Lead", "ticket drivers, refunds and how fast harm signals escalate."],
                    ],
                    ucs=["Player Churn Prediction", "Content Personalisation", "Responsible Gaming"]),
                biz("Risk & Compliance", "AI/BI", "Fraud analysts and compliance officers on AML and SAR alerts, self-exclusion enforcement and jurisdictional filings before payouts release.",
                    [["Fraud Command Centre", "Velocity and device clusters flagged before payouts release."], ["AI/BI", "Chargeback and SAR metrics on certified Metric Views."], ["Unity Catalog", "One definition of GGR across platform and RGS."]],
                    sub=[
                        ["Fraud Analyst", "velocity, device clusters and bonus abuse before payouts release."],
                        ["Compliance Officer", "jurisdictional filings and licence conditions per market."],
                        ["AML & SAR Investigator", "suspicious activity and the evidence behind every report."],
                    ],
                    ucs=["Fraud & Bonus Abuse", "Responsible Gaming", "Chargeback Prevention", "Regulatory GGR"]),
                biz("Marketing & UA", "AI/BI", "User acquisition on CPI, ROAS and creative performance by channel and geography, reallocating spend before daily budgets exhaust.",
                    [["UA Optimiser", "Spend reallocation scenarios before daily budgets exhaust."], ["AI/BI", "ROAS and cohort payback the growth team reads."], ["Model Serving", "LTV models informing bid caps."]],
                    sub=[
                        ["UA Manager", "CPI, ROAS and where the next dollar of spend should go."],
                        ["Growth Marketer", "creative performance and cohort payback by channel and geo."],
                        ["CRM Lifecycle Lead", "win-back, VIP and lifecycle sends that lift retention."],
                    ],
                    ucs=["LTV & Monetisation", "Content Personalisation", "Player Churn Prediction"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the game platform, payments and CRM event streams; own the Bronze to Silver path and the pager when telemetry breaks.",
                    [["Lakeflow Connect", "Managed connectors for platform, payment and CRM sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on telemetry and payment feeds."], ["Lakewatch", "Freshness on the tables live ops and risk teams read every morning."]],
                    sub=[
                        ["Streaming Platform Eng", "the game, telemetry and event streams landing at tick scale."],
                        ["Payments Data Eng", "wallet, RGS and settlement feeds into governed tables."],
                        ["Reliability & On-call", "the pager when a feed live ops or risk depends on breaks."],
                    ],
                    ucs=["Live Ops Balancing", "Fraud & Bonus Abuse", "Regulatory GGR"]),
                biz("Data Scientists", "MLflow", "Churn, LTV, fraud and matchmaking models, and whether they still hold a season after each content patch.",
                    [["Feature Store", "Player features defined once and read identically in training and serving."], ["MLflow", "Every churn and fraud run tracked for audit and reproduction."], ["Model Serving", "LTV and fraud models scored in the live player path."]],
                    sub=[
                        ["Churn & LTV Scientist", "retention, payer conversion and lifetime-value models."],
                        ["Fraud & Risk Scientist", "collusion, bonus abuse and chargeback detection models."],
                        ["Matchmaking & Economy Scientist", "match fairness and in-game economy simulations."],
                    ],
                    ucs=["Player Churn Prediction", "LTV & Monetisation", "Fraud & Bonus Abuse", "Matchmaking Quality"]),
                biz("App Developers", "Apps", "Ship the live ops, player 360 and fraud command applications the studio works in, hosted next to governed data.",
                    [["Apps", "Live ops and risk screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for economy config and case writes."], ["Agent Bricks", "Agents that draft a live ops tweak or fraud case against governed tools."]],
                    sub=[
                        ["Live Ops App Dev", "the event, economy and cohort screens live-ops teams work in."],
                        ["Player 360 Dev", "the support and VIP view hosts and community teams rely on."],
                        ["Risk Tooling Dev", "the fraud and responsible-gaming case screens analysts action."],
                    ],
                    ucs=["Live Ops Balancing", "Content Personalisation", "Fraud & Bonus Abuse"]),
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
                uc("Player Churn Prediction", "Retention", "gauge", "Identifying players likely to lapse from session decay and economy frustration before they uninstall.",
                    problem="Session frequency and spend decay quietly, and by the time a dashboard shows a title bleeding players the churn has happened and winning them back costs far more than keeping them.",
                    who="Live Ops & Product",
                    how="Session, economy and payment signals land through Lakeflow and feed churn models in Feature Store and Model Serving, so at-risk cohorts surface in the Live Ops Console before they lapse.",
                    comps=["Live Ops Console", "Model Serving", "Feature Store", "MLflow", "Custom Game Servers", "Lakeflow"],
                    stories=[
                        ["Changing the game in player retention (SEGA Europe)", "https://www.databricks.com/customers/sega"],
                        ["FunPlus gains new player insights to optimize gaming", "https://www.databricks.com/customers/funplus"],
                    ]),
                uc("LTV & Monetisation", "Revenue", "market", "Cohort lifetime value and payer conversion scored per acquisition channel and title.",
                    problem="Acquisition is bought on installs, not value, so spend chases cheap users who never pay while genuinely high-value players go underbid and the payback on each channel stays a guess.",
                    who="Marketing & UA",
                    how="Cohort spend and behaviour are engineered in Feature Store and scored in Model Serving, and predicted LTV lands in the UA Optimiser and AI/BI so bids and offers align to value per channel.",
                    comps=["UA Optimiser", "Model Serving", "Feature Store", "AI/BI", "AppsFlyer Attribution", "Adyen Payments"],
                    stories=[
                        ["Personalizing players' experiences with recommendation systems", "https://www.databricks.com/blog/personalizing-players-experiences-recommendation-systems"],
                        ["Creating a player centric experience in games", "https://www.databricks.com/blog/creating-player-centric-experience-games"],
                    ]),
                uc("Live Ops Balancing", "Economy", "sheet", "Sink and source tuning tested against simulated economy health before patches ship.",
                    problem="Economy tuning ships on instinct: a drop-rate or price change can drain a currency sink or wreck retention, and the feedback only lands days later once the patch is already live.",
                    who="Live Ops & Product",
                    how="Session and economy events stream into Lakehouse//RT on Delta Lake, so sinks and sources are simulated in the Live Ops Console and balanced against cohort impact before a patch ships.",
                    comps=["Live Ops Console", "Lakehouse//RT", "Delta Lake", "AI/BI", "PlayFab Backend", "Apache Spark"],
                    stories=[
                        ["Sega delivers real-time gaming insights with Spark Declarative Pipelines", "https://www.databricks.com/customers/sega/spark-declarative-pipelines"],
                        ["Supercell masters the art and science of ForeverGames", "https://www.databricks.com/customers/supercell"],
                    ]),
                uc("Fraud & Bonus Abuse", "Risk", "stream", "Multi-accounting, collusion and promo abuse detected from device, payment and play graphs.",
                    problem="Multi-accounting, collusion and promo abuse hide across device, payment and play data, and siloed rules miss coordinated rings until the bonus and chargeback losses are already gone.",
                    who="Risk & Compliance",
                    how="Device, payment and session graphs are conformed on Delta Lake and scored in Model Serving, so velocity and collusion clusters surface in the Fraud Command Centre before withdrawals release.",
                    comps=["Fraud Command Centre", "Model Serving", "SEON Fraud Prevention", "GeoComply Location", "Delta Lake", "Feature Store"],
                    stories=[
                        ["Managing and analyzing game data at scale", "https://www.databricks.com/blog/managing-analyzing-game-data-scale"],
                    ]),
                uc("Responsible Gaming", "Compliance", "gavel", "Self-exclusion, deposit limits and harm markers enforced from governed player state.",
                    problem="Harm markers, deposit limits and self-exclusion live in separate systems, so intervention comes too late and regulators penalise operators who cannot prove they acted on the warning signs.",
                    who="Risk & Compliance",
                    how="Player state is conformed under Unity Catalog and scored in Model Serving for harm markers, so limits and self-exclusion enforce from governed data and every intervention is auditable.",
                    comps=["Fraud Command Centre", "Model Serving", "Unity Catalog", "GeoComply Location", "AI/BI", "Feature Store"],
                    stories=[
                        ["Responsible Gaming solution accelerator", "https://www.databricks.com/solutions/accelerators/responsible-gaming"],
                    ]),
                uc("Matchmaking Quality", "Engagement", "people", "Queue times and match fairness optimised without opening exploit vectors.",
                    problem="Long queues and lopsided matches push players away, but tuning for fairness can open exploit vectors, and studios rarely have the live signal to balance both without guesswork.",
                    who="Live Ops & Product",
                    how="Match, skill and session telemetry stream into Lakehouse//RT and feed matchmaking models in Model Serving, so queue time and fairness are tuned against real outcomes, not static brackets.",
                    comps=["Model Serving", "Lakehouse//RT", "Custom Game Servers", "Feature Store", "MLflow", "AI/BI"],
                    stories=[
                        ["Personalizing players' experiences with recommendation systems", "https://www.databricks.com/blog/personalizing-players-experiences-recommendation-systems"],
                    ]),
                uc("Content Personalisation", "Live ops", "custlake", "Offers and events targeted per player segment from in-game behaviour, not batch exports.",
                    problem="Offers and events are batched to broad segments from stale exports, so a player sees content that ignores what they just did in-game and the moment to convert or re-engage has passed.",
                    who="Player Experience",
                    how="In-game behaviour is resolved in CustomerLake and scored in Model Serving, so per-segment offers and events trigger through Braze Lifecycle from governed data without nightly exports.",
                    comps=["Player 360", "CustomerLake", "Model Serving", "Braze Lifecycle", "AI Functions", "Salesforce Gaming CRM"],
                    stories=[
                        ["Announcing Heroic Labs Satori integration with Databricks", "https://www.databricks.com/blog/announcing-heroic-labs-satori-integration-databricks"],
                        ["Creating a player centric experience in games", "https://www.databricks.com/blog/creating-player-centric-experience-games"],
                    ]),
                uc("Chargeback Prevention", "Payments", "market", "High-risk instruments and behaviours blocked before authorisation settles.",
                    problem="Chargebacks land weeks after the deposit, so a risky card or behaviour is only caught once the money and the goods are gone, and manual review cannot keep pace with authorisation volume.",
                    who="Risk & Compliance",
                    how="Payment, device and behaviour features are scored in Model Serving in the authorisation path, so high-risk instruments are blocked from the Fraud Command Centre before settlement completes.",
                    comps=["Fraud Command Centre", "Model Serving", "Adyen Payments", "SEON Fraud Prevention", "Feature Store", "Delta Lake"]),
                uc("Regulatory GGR", "Reporting", "gavel", "Jurisdiction-accurate gross gaming revenue reconciled across platform and RGS content.",
                    problem="Gross gaming revenue must reconcile across platform, wallet and remote game servers per jurisdiction, yet the numbers sit in separate systems and filing windows leave no room for manual fixes.",
                    who="Risk & Compliance",
                    how="Platform, RGS and payment feeds are conformed under Unity Catalog into contracted Gold products, so jurisdiction-accurate GGR reports are produced from one governed source, not a spreadsheet.",
                    comps=["Unity Catalog", "Data Products", "Pragmatic Play RGS", "Regulator GGR Feeds", "AI/BI", "Delta Lake"]),
                uc("Studio Royalty", "Partners", "product", "Third-party title revenue share calculated from governed round and jackpot data.",
                    problem="Third-party title revenue share is calculated from partner ledgers and manual round exports, so royalties are slow, disputed and hard to reconcile against what actually happened in the game.",
                    who="CEO & CFO",
                    how="Round and jackpot data are conformed on Delta Lake and shared as governed products over Open Sharing, so studio royalties compute from the platform's own record and reconcile with partners.",
                    comps=["Pragmatic Play RGS", "Publisher Revenue Share", "Delta Lake", "Open Sharing", "Data Products", "Unity Catalog"]),
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
