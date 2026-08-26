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
                biz("Network & Studio Chiefs", "Genie One", "The CEO on portfolio ROI and subscriber growth; the CRO on ad yield by daypart and upfront commitments against the reach actually delivered.", [["Genie One", "Ask what last night's prime delivered in reach without waiting on research."], ["AI/BI", "Reach, yield and churn on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"impression\" means one thing across sales and ops."]]),
                biz("Programming", "AI/BI", "Schedule architecture, premiere windows and catalog rotation scored on audience retention, completion rate and content ROI by title and platform.", [["Schedule Optimizer", "Daypart and title mix scored on reach and cost before the grid locks."], ["AI/BI", "Content ROI and completion rate on governed definitions."], ["Genie One", "Ask which titles drove the most new subscribers last month."]]),
                biz("Ad Sales", "CustomerLake", "Upfront guarantees, scatter pricing and makegood liability when delivery under-runs against the reach and frequency by demo the desk sold.", [["Yield Manager", "Rate cards and pacing exceptions before the quarter closes short."], ["CustomerLake", "Advertiser segments without copying CRM into a separate CDP."], ["AI/BI", "Delivery versus order on certified Metric Views."]]),
                biz("Distribution", "Lakehouse//RT", "MVPD carriage, OTT app QoE and CDN cost per stream when a marquee live event spikes concurrency past the forecast the network planned for.", [["Live Ops Console", "Stream health and failover state during marquee broadcasts."], ["Lakehouse//RT", "QoE and concurrency at the latency a live event moves at."], ["Model Serving", "Churn risk scored on viewing and billing signals."]]),
                biz("News & Production", "Apps", "Rundown execution, field feeds and rights clearance for breaking coverage, watched on time-to-air and the clearance exceptions that block a segment.", [["Newsroom Hub", "Story lifecycle from pitch through air with asset lineage."], ["Apps", "Assignment and approval screens on governed metadata."], ["Agent Bricks", "Agents that draft rundown suggestions from wire and social feeds."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the playout, OTT, ad server and measurement feeds; own the Bronze to Silver path and the pager when an as-run or impression pipeline breaks.", [["Lakeflow Connect", "Managed connectors for MAM, ad server and subscription sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on as-run and impression feeds."], ["Lakewatch", "Freshness on the reach and yield tables sales reads every morning."]]),
                biz("Data Scientists", "MLflow", "Subscriber churn, recommendation, ad-yield and reach-forecast models, and whether they still hold six months after deployment across linear and OTT.", [["Feature Store", "Viewing and billing features read identically in training and serving."], ["MLflow", "Every churn and yield run tracked for audit and reproduction."], ["Model Serving", "Recommendation and churn models scored in the streaming path."]]),
                biz("App Developers", "Apps", "Ship the live-ops, yield manager and newsroom applications programming and sales work in, hosted next to governed audience and rights data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for rundown state and governed writes."], ["Agent Bricks", "Agents that draft rundown suggestions against governed tools."]]),
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
                uc("Audience Measurement", "Reach", "chart", "Cross-platform reach and frequency reconciled across linear, OTT and CTV panels."),
                uc("Ad Yield Optimisation", "Revenue", "market", "Scatter pricing and pod structure tuned to delivery pace and audience composition."),
                uc("Content ROI", "Programming", "product", "Title investment scored on acquisition, retention and licensing revenue."),
                uc("Subscriber Churn", "Retention", "custlake", "Cancel risk surfaced from viewing, billing and service contacts before renewal."),
                uc("Rights Compliance", "Legal", "gavel", "Window and territory violations flagged before playout or syndication."),
                uc("QoE Monitoring", "Streaming", "stream", "Startup and rebuffer anomalies traced to CDN, device and title root cause."),
                uc("Personalised Recommend", "Engagement", "partner", "Home screen rails ranked on affinity without copying profiles off-platform."),
                uc("Makegood Automation", "Ad ops", "gauge", "Under-delivery offers priced and approved before account teams escalate."),
                uc("Social Clip Analytics", "Distribution", "observ", "Talent and brand clips scored on reach and sentiment tied back to parent titles."),
                uc("Live Event Scaling", "Operations", "iot", "Capacity and ad pod density planned from historical concurrency curves."),
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
