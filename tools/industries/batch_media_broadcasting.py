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


INDUSTRIES_BATCH_MEDIA_BROADCASTING = {
    'media_broadcasting': {
        "label": "Media & Broadcasting",
        "blurb": "Content production, rights and distribution: linear and streaming operations, ad sales and audience measurement across broadcasters and studios.",
        "medallion": medallion(
            "Raw audience feeds",
            "As-run logs, playout automation events, ad server impressions, subscriber transactions and social engagement, landed exactly as received so a rating or a spot can always be replayed as it stood.",
            "Conformed asset, viewer",
            "Programs, episodes, rights windows and viewer households resolved into single conformed entities across playout, OTT and ad systems, with cross-device identifiers reconciled and campaign delivery stitched to one audience.",
            "Reach, yield, churn",
            "Contracted products sales and programming leaders run on: reach and frequency by demo, ad yield by daypart, subscriber churn and content ROI by title and platform.",
        ),
        "rails": {
            "src": [
                {"box": "Playout & MAM", "ic": "stream", "tiles": [
                        tile("Dalet Galaxy", "stream", "Newsroom, MAM and playout scheduling: rundowns, media assets and as-run logs from linear operations.", "dalet"),
                        tile("Avid MediaCentral", "stream", "Edit decisions, proxy media and production metadata from craft editing and finishing.", "avid"),
                        tile("Imagine Nexio", "iot", "Channel playout automation, primary and backup chain state and splice events.", "imagine"),
                    ]},
                {"box": "OTT & Streaming", "ic": "partner", "tiles": [
                        tile("Brightcove", "stream", "VOD and live streaming delivery, QoE metrics and viewer engagement by title.", "brightcove"),
                        tile("Conviva Experience", "observ", "Startup time, rebuffering and device-level QoE for every stream session.", "conviva"),
                        tile("Zuora Media", "market", "Subscription plans, renewals and billing events for direct-to-consumer offers.", "zuora"),
                    ]},
                {"box": "Ad Sales & Traffic", "ic": "market", "tiles": [
                        tile("WideOrbit WO Traffic", "market", "Inventory, orders and makegoods for linear ad sales and traffic.", "wideorbit"),
                        tile("FreeWheel Ad Server", "stream", "Dynamic ad insertion, pod structure and impression delivery on streaming inventory.", "freewheel"),
                        tile("Operative One", "sheet", "Upfront deals, pacing and revenue recognition across linear and digital.", "operative"),
                    ]},
                {"box": "Audience & Rights", "ic": "custlake", "tiles": [
                        tile("Nielsen One", "chart", "Cross-platform audience measurement and demographic ratings the sales team prices against.", "nielsen"),
                        tile("Comscore", "chart", "Digital audience panels and campaign validation for addressable and CTV.", "comscore"),
                        tile("Rightsline", "gavel", "Title rights, windows and territory restrictions governing what can air where.", "rightsline"),
                    ]},
                fed_group("Studio Cost Ledger", "Production accounting and amortisation marts queried in place under Unity Catalog for title P&L."),
            ],
            "ing": ing_rail([
                tile("SCTE-35 Ad Markers", "stream", "Splice insert and cue-out events parsed from transport streams for ad pod reconciliation.", "scte35"),
                tile("Roku / Samsung ACR", "partner", "Automatic content recognition feeds for incremental reach on CTV.", "roku-acr"),
                tile("Social Platform APIs", "api", "Clip views, shares and comment sentiment from owned and talent accounts.", "meta-graph"),
            ]),
            "ppl": ppl_rail2([
                biz("Network & Studio Chiefs", "Genie One", "The CEO on portfolio ROI and subscriber growth; the CRO on ad yield by daypart and upfront commitments against the reach actually delivered.", [["Genie One", "Ask what last night's prime delivered in reach without waiting on research."], ["AI/BI", "Reach, yield and churn on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"impression\" means one thing across sales and ops."]],
                    sub=[
                        ["CEO", "portfolio ROI, subscriber growth and the mix of linear decline against streaming gain."],
                        ["Chief Revenue Officer", "ad yield by daypart and upfront commitments against the reach actually delivered."],
                        ["Head of Content", "greenlight and licensing bets and the return each title earns across platforms."],
                    ],
                    ucs=["Content ROI", "Ad Yield Optimisation", "Subscriber Churn", "Audience Measurement"]),
                biz("Programming", "AI/BI", "Schedule architecture, premiere windows and catalog rotation scored on audience retention, completion rate and content ROI by title and platform.", [["Schedule Optimizer", "Daypart and title mix scored on reach and cost before the grid locks."], ["AI/BI", "Content ROI and completion rate on governed definitions."], ["Genie One", "Ask which titles drove the most new subscribers last month."]],
                    sub=[
                        ["VP Programming", "the prime grid, premiere windows and catalog rotation against audience retention."],
                        ["Scheduling", "daypart mix and lead-in strategy before the grid locks for air."],
                        ["Content Strategy", "which titles and genres to commission from completion and ROI signals."],
                    ],
                    ucs=["Content ROI", "Personalised Recommend", "Audience Measurement"]),
                biz("Ad Sales", "CustomerLake", "Upfront guarantees, scatter pricing and makegood liability when delivery under-runs against the reach and frequency by demo the desk sold.", [["Yield Manager", "Rate cards and pacing exceptions before the quarter closes short."], ["CustomerLake", "Advertiser segments without copying CRM into a separate CDP."], ["AI/BI", "Delivery versus order on certified Metric Views."]],
                    sub=[
                        ["VP Ad Sales", "upfront guarantees and scatter pricing against the reach and frequency the desk sold."],
                        ["Yield & Pricing", "rate cards, pacing and makegood liability when delivery under-runs."],
                        ["Ad Operations", "pod structure, trafficking and delivery reconciliation across linear and streaming."],
                    ],
                    ucs=["Ad Yield Optimisation", "Makegood Automation", "Audience Measurement"]),
                biz("Distribution", "Lakehouse//RT", "MVPD carriage, OTT app QoE and CDN cost per stream when a marquee live event spikes concurrency past the forecast the network planned for.", [["Live Ops Console", "Stream health and failover state during marquee broadcasts."], ["Lakehouse//RT", "QoE and concurrency at the latency a live event moves at."], ["Model Serving", "Churn risk scored on viewing and billing signals."]],
                    sub=[
                        ["Head of Streaming", "OTT growth, concurrency and QoE during marquee live events."],
                        ["CDN & Delivery", "cost per stream and failover when concurrency spikes past forecast."],
                        ["Retention", "subscriber churn scored from viewing, billing and service signals."],
                    ],
                    ucs=["QoE Monitoring", "Subscriber Churn", "Live Event Scaling", "Personalised Recommend"]),
                biz("News & Production", "Apps", "Rundown execution, field feeds and rights clearance for breaking coverage, watched on time-to-air and the clearance exceptions that block a segment.", [["Newsroom Hub", "Story lifecycle from pitch through air with asset lineage."], ["Apps", "Assignment and approval screens on governed metadata."], ["Agent Bricks", "Agents that draft rundown suggestions from wire and social feeds."]],
                    sub=[
                        ["News Director", "time-to-air and the clearance exceptions that block a segment."],
                        ["Field & Assignment", "crew, feeds and rundown execution for breaking coverage."],
                        ["Social & Digital", "talent clips and owned-account reach scored back to parent titles."],
                    ],
                    ucs=["Rights Compliance", "Social Clip Analytics"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the playout, OTT, ad server and measurement feeds; own the Bronze to Silver path and the pager when an as-run or impression pipeline breaks.", [["Lakeflow Connect", "Managed connectors for MAM, ad server and subscription sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on as-run and impression feeds."], ["Lakewatch", "Freshness on the reach and yield tables sales reads every morning."]],
                    sub=[
                        ["Streaming Data Eng", "landing as-run, playout and impression feeds with expectations on freshness."],
                        ["Ad & Subscription Eng", "ingesting ad server, traffic and billing sources for reach and yield tables."],
                        ["Platform Eng", "the Bronze-to-Silver path and the pager when a pipeline breaks before morning."],
                    ],
                    ucs=["Audience Measurement", "QoE Monitoring", "Makegood Automation"]),
                biz("Data Scientists", "MLflow", "Subscriber churn, recommendation, ad-yield and reach-forecast models, and whether they still hold six months after deployment across linear and OTT.", [["Feature Store", "Viewing and billing features read identically in training and serving."], ["MLflow", "Every churn and yield run tracked for audit and reproduction."], ["Model Serving", "Recommendation and churn models scored in the streaming path."]],
                    sub=[
                        ["Churn & Retention Science", "cancel-risk models on viewing, billing and service contacts."],
                        ["Recommendation & Ranking", "affinity models ranking home-screen rails without copying profiles."],
                        ["Ad & Reach Forecasting", "yield and reach-forecast models across linear and OTT."],
                    ],
                    ucs=["Subscriber Churn", "Personalised Recommend", "Ad Yield Optimisation"]),
                biz("App Developers", "Apps", "Ship the live-ops, yield manager and newsroom applications programming and sales work in, hosted next to governed audience and rights data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for rundown state and governed writes."], ["Agent Bricks", "Agents that draft rundown suggestions against governed tools."]],
                    sub=[
                        ["Live Ops Dev", "stream-health and failover screens for marquee broadcasts."],
                        ["Yield & Newsroom Dev", "the yield manager and newsroom apps sales and news work in."],
                        ["Platform Dev", "governed writes and rundown state on serverless Postgres."],
                    ],
                    ucs=["Live Event Scaling", "Makegood Automation", "Social Clip Analytics"]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                        tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                        tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and live-event status in the channel news already works in (Beta)."),
                        tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code."),
                    ]},
                {"box": "Traffic & Playout", "ic": "opdb", "tiles": [
                        tile("WideOrbit Order Sync", "db", "Revised orders and makegoods written back into traffic before the log locks.", "wideorbit"),
                        tile("Playout Playlist", "stream", "Approved schedules pushed to automation after rights clearance.", "imagine"),
                        tile("Ad Decisioning", "api", "Dynamic pod fills updated from governed yield rules on streaming endpoints.", "freewheel"),
                    ]},
                {"box": "Partners & MVPDs", "ic": "partner", "tiles": [
                        tile("MVPD Schedule Exchange", "share", "Carriage schedules and metadata shared to distributors over Delta Sharing.", "dalet"),
                        tile("Agency Data Feeds", "api", "Post-campaign delivery and reach files served from governed products not email.", "nielsen"),
                        tile("Talent & Studio Portal", "globe", "Production status and rough-cut reviews on Apps reading governed MAM metadata."),
                    ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                        tile("FCC / Ofcom Filing", "gavel", "Children's programming, political and sponsorship disclosures filed from governed as-run logs.", "scte35"),
                        tile("Music Rights Reporting", "share", "Performance and mechanical usage reported to PROs from contracted Gold products."),
                    ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                        tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                        tile("Sharing Recipients", "share", "Agencies, studios and platforms reading live tables with no copy and no egress duplication."),
                    ]},
            ]),
        },
        "top": top_band(
            [
                app("Live Ops Console", "Stream health", "gauge", "Concurrency, rebuffering and CDN failover during marquee live events on Databricks Apps over Lakebase."),
                app("Yield Manager", "Ad pacing", "market", "Order delivery versus guarantee with makegood options before the quarter closes."),
                app("Schedule Optimizer", "Grid planning", "sheet", "Title and daypart mix scored on reach, cost and rights before the schedule publishes."),
                app("Newsroom Hub", "Story workflow", "notebook", "Assignments, assets and clearance status from pitch through on-air."),
            ],
            [
                uc("Audience Measurement", "Reach", "chart", "Cross-platform reach and frequency reconciled across linear, OTT and CTV panels.",
                   problem="Reach and frequency live in Nielsen, Comscore and ACR panels that never agree, so the sales desk prices upfronts and proves delivery against numbers that shift by source.",
                   who="Ad Sales",
                   how="Panel, as-run and ACR feeds are conformed on Delta Lake under Unity Catalog, so reach and frequency by demo read from one certified set of Metric Views in AI/BI.",
                   comps=["Nielsen One", "Comscore", "Roku / Samsung ACR", "AI/BI", "Unity Catalog"],
                   stories=[
                       ["Seven West Media fuels audience growth and ad revenue with AI", "https://www.databricks.com/customers/seven-west-media"],
                       ["First-party audience data is the ad sales relationship now", "https://www.databricks.com/blog/first-party-audience-data-ad-sales-relationship-now"],
                   ]),
                uc("Ad Yield Optimisation", "Revenue", "market", "Scatter pricing and pod structure tuned to delivery pace and audience composition.",
                   problem="Scatter pricing and pod structure are set from stale pacing reports, so inventory sells too cheap or under-delivers and the lost yield only surfaces after the quarter closes.",
                   who="Ad Sales",
                   how="Delivery pace and audience composition are scored in Model Serving and surfaced in the Yield Manager app, so the desk tunes rate cards and pod fills against live delivery.",
                   comps=["Yield Manager", "FreeWheel Ad Server", "Operative One", "Model Serving", "AI/BI"],
                   stories=[
                       ["Comcast Advertising powers campaign success with predictive insights", "https://www.databricks.com/customers/comcast/databricks-apps"],
                   ]),
                uc("Content ROI", "Programming", "product", "Title investment scored on acquisition, retention and licensing revenue.",
                   problem="Greenlight, licensing and marketing bets rest on gut and lagging ratings, so no one can say what a title truly returned in acquisition, retention and licensing across platforms.",
                   who="Network & Studio Chiefs",
                   how="Viewing, subscription and Studio Cost Ledger data are conformed under Unity Catalog and scored in Schedule Optimizer, so title P&L and content ROI read on governed definitions.",
                   comps=["Schedule Optimizer", "Studio Cost Ledger", "AI/BI", "Unity Catalog", "Genie One"],
                   stories=[
                       ["Warner Bros. Discovery curates the viewer experience", "https://www.databricks.com/customers/warner-bros-discovery"],
                       ["Condé Nast delivers personalized content at global scale", "https://www.databricks.com/customers/conde_nast"],
                   ]),
                uc("Subscriber Churn", "Retention", "custlake", "Cancel risk surfaced from viewing, billing and service contacts before renewal.",
                   problem="Cancel intent shows up in viewing dips, billing events and support contacts that sit in separate systems, so retention learns a subscriber is leaving only when the cancellation lands.",
                   who="Distribution",
                   how="Viewing, billing and service features are engineered in Feature Store and scored through Model Serving with runs tracked in MLflow, so cancel risk surfaces before renewal, not after.",
                   comps=["Model Serving", "CustomerLake", "Zuora Media", "Feature Store", "MLflow"],
                   stories=[
                       ["Showtime lowers churn with a view into the subscriber journey", "https://www.databricks.com/customers/showtime"],
                       ["Flagging at-risk subscribers for direct-to-consumer media", "https://www.databricks.com/blog/2020/08/18/flagging-at-risk-subscribers-for-direct-to-consumer-media-services.html"],
                   ]),
                uc("Rights Compliance", "Legal", "gavel", "Window and territory violations flagged before playout or syndication.",
                   problem="Rights windows and territory restrictions live in contracts apart from the schedule, so a title can be booked to air where or when a licence does not actually permit.",
                   who="News & Production",
                   how="Rightsline windows are conformed under Unity Catalog and checked with AI Functions in Schedule Optimizer, so window and territory violations flag before playout or syndication.",
                   comps=["Rightsline", "Unity Catalog", "AI Functions", "Delta Lake", "Schedule Optimizer"]),
                uc("QoE Monitoring", "Streaming", "stream", "Startup and rebuffer anomalies traced to CDN, device and title root cause.",
                   problem="When a stream buffers or fails to start, the cause hides across CDN, device and title, so viewers churn on a bad session before anyone traces which link in the delivery chain broke.",
                   who="Distribution",
                   how="Player and CDN telemetry stream into Lakehouse//RT and are scored in Model Serving, so the Live Ops Console traces startup and rebuffer anomalies to CDN, device and title root cause.",
                   comps=["Live Ops Console", "Conviva Experience", "Brightcove", "Lakehouse//RT", "Model Serving"],
                   stories=[
                       ["Building QoS analytics for streaming video services", "https://www.databricks.com/blog/2020/05/06/how-to-build-a-quality-of-service-qos-analytics-solution-for-streaming-video-services.html"],
                   ]),
                uc("Personalised Recommend", "Engagement", "partner", "Home screen rails ranked on affinity without copying profiles off-platform.",
                   problem="Home-screen rails default to editorial hunches or generic popularity, so viewers scroll past content they would watch and profiles get copied into outside tools to make it work.",
                   who="Programming",
                   how="Affinity models read viewing features from Feature Store and score in Model Serving on-platform, so home-screen rails rank to each household without copying profiles off the lakehouse.",
                   comps=["Model Serving", "Feature Store", "CustomerLake", "Brightcove", "AI Functions"],
                   stories=[
                       ["Viacom18 personalizes viewing for 600M+ viewers", "https://www.databricks.com/customers/viacom18"],
                       ["Personalization strategies for media companies", "https://www.databricks.com/blog/personalization-strategies-for-media"],
                   ]),
                uc("Makegood Automation", "Ad ops", "gauge", "Under-delivery offers priced and approved before account teams escalate.",
                   problem="When a campaign under-delivers, makegoods are worked by hand across traffic and ad-server data, so liability piles up and account teams escalate before a fair replacement is priced.",
                   who="Ad Sales",
                   how="Order and delivery data from WideOrbit and FreeWheel are scored in Model Serving and surfaced in Yield Manager on Lakebase, so under-delivery offers are priced and approved before escalation.",
                   comps=["Yield Manager", "WideOrbit WO Traffic", "FreeWheel Ad Server", "Model Serving", "Lakebase"]),
                uc("Social Clip Analytics", "Distribution", "observ", "Talent and brand clips scored on reach and sentiment tied back to parent titles.",
                   problem="Talent and brand clips scatter across social platforms with no line back to the titles they promote, so no one sees which clips drove reach or how sentiment moved around a show.",
                   who="News & Production",
                   how="Social feeds land through Social Platform APIs and are scored for reach and sentiment with AI Functions and Agent Bricks, so clip performance ties back to parent titles in AI/BI.",
                   comps=["Social Platform APIs", "AI Functions", "Agent Bricks", "AI/BI", "Delta Lake"],
                   stories=[
                       ["SEGA lifts player retention with sentiment analysis", "https://www.databricks.com/customers/sega"],
                   ]),
                uc("Live Event Scaling", "Operations", "iot", "Capacity and ad pod density planned from historical concurrency curves.",
                   problem="A marquee live event can spike concurrency far past forecast, so capacity and ad pod density are guessed and the network risks a buffering meltdown or unsold, wasted inventory.",
                   who="Distribution",
                   how="Historical concurrency curves are processed with Apache Spark in Lakehouse//RT and read in Live Ops Console, so capacity and SCTE-35 pod density are planned from real demand.",
                   comps=["Live Ops Console", "Conviva Experience", "SCTE-35 Ad Markers", "Lakehouse//RT", "Apache Spark"],
                   stories=[
                       ["FOX Sports reimagines the live fan experience", "https://www.databricks.com/customers/fox-sports"],
                   ]),
            ],
        ),
        "sources": {
            "dalet": {"t": "Dalet Galaxy", "u": "https://www.dalet.com/products/"},
            "avid": {"t": "Avid MediaCentral", "u": "https://www.avid.com/products/mediacentral"},
            "imagine": {"t": "Imagine Communications Nexio", "u": "https://www.imaginecommunications.com/"},
            "brightcove": {"t": "Brightcove", "u": "https://www.brightcove.com/"},
            "conviva": {"t": "Conviva", "u": "https://www.conviva.com/"},
            "zuora": {"t": "Zuora", "u": "https://www.zuora.com/"},
            "wideorbit": {"t": "WideOrbit WO Traffic", "u": "https://www.wideorbit.com/"},
            "freewheel": {"t": "FreeWheel", "u": "https://www.freewheel.com/"},
            "operative": {"t": "Operative One", "u": "https://www.operative.com/operative-one/"},
            "nielsen": {"t": "Nielsen One", "u": "https://www.nielsen.com/solutions/nielsen-one/"},
            "comscore": {"t": "Comscore", "u": "https://www.comscore.com/"},
            "rightsline": {"t": "Rightsline", "u": "https://www.rightsline.com/"},
            "scte35": {"t": "SCTE-35 digital program insertion", "u": "https://www.scte.org/standards/"},
            "roku-acr": {"t": "Roku advertising", "u": "https://advertising.roku.com/"},
            "meta-graph": {"t": "Meta Graph API", "u": "https://developers.facebook.com/docs/graph-api/"},
        },
    },
}
