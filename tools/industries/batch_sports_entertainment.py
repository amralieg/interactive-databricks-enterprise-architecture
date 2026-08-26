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


INDUSTRIES_BATCH_SPORTS_ENTERTAINMENT = {
    'sports_entertainment': {
        "label": "Sports & Entertainment",
        "blurb": "Teams, venues and media rights: ticketing and fan engagement, game-day operations, broadcast and streaming, sponsorship activation, and athlete performance analytics.",
        "medallion": medallion(
            "Raw event and fan feeds",
            "Ticketing scans, POS concessions, broadcast logs, wearable tracking and CRM interactions, landed exactly as received so a attendance or a sponsorship impression can always be replayed.",
            "Conformed fan, event, asset",
            "Fans, events, seats and media assets resolved into single conformed entities across ticketing, CRM and broadcast estates, with identity stitched across channels.",
            "Attendance, yield, engagement",
            "Contracted products commercial and operations teams run on: ticket yield by section, F&B attach rate, sponsorship ROI, streaming concurrency and churn risk by segment.",
        ),
        "rails": {
            "src": [
                {"box": "Ticketing & CRM", "ic": "erp", "tiles": [
                    tile("Ticketmaster Archtics", "erp", "Primary ticketing, seat inventory, pricing and scan data from every event.", "ticketmaster"),
                    tile("Salesforce Sports Cloud", "custlake", "Fan profiles, membership tiers, service cases and campaign responses.", "sf-sports"),
                    tile("SeatGeek Enterprise", "market", "Secondary market listings, transfer activity and dynamic pricing signals.", "seatgeek"),
                ]},
                {"box": "Venue Operations", "ic": "stream", "tiles": [
                    tile("VenueNext", "apps", "Mobile ordering, wayfinding and in-seat service for arena and stadium guests.", "venuenext"),
                    tile("Genetec Security Center", "iot", "Access control, crowd density cameras and incident logs on game day.", "genetec"),
                    tile("Catapult Sports", "iot", "GPS and IMU player tracking: load, sprint distance and injury risk flags.", "catapult"),
                ]},
                {"box": "Broadcast & OTT", "ic": "partner", "tiles": [
                    tile("Grabyo Clipping", "stream", "Live clipping, highlights and social publishing from broadcast feeds.", "grabyo"),
                    tile("Deltatre OTT Platform", "api", "Streaming concurrency, start-over and device telemetry for direct-to-consumer.", "deltatre"),
                    tile("Nielsen Sports", "chart", "TV and digital audience measurement for rights valuation.", "nielsen-sports"),
                ]},
                {"box": "Sponsorship & Ads", "ic": "market", "tiles": [
                    tile("SponsorUnited", "partner", "Sponsorship inventory, activation tracking and competitive spend intelligence.", "sponsorunited"),
                    tile("The Trade Desk Sports", "market", "Programmatic inventory across league and team digital properties.", "trade-desk"),
                    tile("UKG Workforce", "people", "Staff scheduling, time and attendance for event and concessions crews.", "ukg"),
                ]},
                fed_group("League Data Marts", "Official league statistics and schedule marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("Stats Perform Feeds", "api", "Live play-by-play, rosters and official statistics ingested for analytics.", "stats-perform"),
                tile("Social Listening APIs", "observ", "Brand mention and sentiment feeds for sponsorship and crisis monitoring."),
                tile("Rights Holder Metadata", "zplug", "Media rights windows and blackout rules from league partners.", "stats-perform"),
            ]),
            "ppl": ppl2([
                biz("Ownership & Executive", "Genie One", "The CEO on revenue per fan and matchday P&L; the COO on ingress throughput, concessions flow and the safety record across the venue.",
                    [["Genie One", "Last home stand yield without analyst delay."], ["AI/BI", "Attendance and sponsorship ROI on Metric Views."]]),
                biz("Ticketing & Pricing", "Model Serving", "Pricing analysts on dynamic seat tiers, secondary-market pressure and sell-through pace against the demand curve before and during on-sale.",
                    [["Pricing Workbench", "Demand forecast before on-sale."], ["Model Serving", "Price models in the on-sale path."]]),
                biz("Fan Engagement", "CustomerLake", "CRM teams on membership growth, churn before renewal and personalised offers scored on spend stitched across ticketing and concessions.",
                    [["Fan 360 Console", "Spend stitched across ticketing and concessions."], ["CustomerLake", "Segments without a separate CDP."]]),
                biz("Game-Day Ops", "Lakehouse//RT", "Venue managers and medical staff on ingress flow, queue times, player load and incidents, moving crews before a bottleneck becomes a delay.",
                    [["Game-Day Command", "Live scans and queue times on one screen."], ["Load Management Hub", "Player workload before selection."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land ticketing scans, POS folios, wearable tracking and CRM feeds; own Bronze to Silver and the pager when a game-day attendance table stalls.",
                    [["Lakeflow Connect", "Managed connectors for ticketing, CRM and POS sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on scan and tracking feeds."], ["Lakewatch", "Freshness on the attendance tables commercial reads on game day."]]),
                biz("Data Scientists", "MLflow", "Dynamic-pricing, fan-churn, injury-risk and highlight-selection models, and whether they still hold as rosters, opponents and demand shift.",
                    [["Feature Store", "Fan and athlete features read identically in training and serving."], ["MLflow", "Every pricing and load experiment tracked for audit."], ["Model Serving", "Price and risk models scored in the on-sale and coaching path."]]),
                biz("App Developers", "Apps", "Ship the Game-Day Command, Pricing Workbench and Fan 360 apps commercial and venue teams work in, next to governed ticketing data.",
                    [["Apps", "Venue screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for offer and incident state writes."], ["Agent Bricks", "Agents that draft offers against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "League and team dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for attendance and sponsorship questions on game day."),
                    tile("Notebooks & IDEs", "notebook", "Analytics notebooks against governed ticketing and tracking data."),
                ]},
                {"box": "Fan & Partner", "ic": "partner", "tiles": [
                    tile("Mobile App Offers", "api", "Personalised upsell and parking offers served in the team app."),
                    tile("Sponsor Reporting API", "share", "Activation proof and impression delivery to sponsors over Delta Sharing."),
                    tile("Broadcaster Data Feed", "globe", "Official stats and graphics packages shared to rights holders."),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Dynamic Price Holds", "market", "Price tier adjustments written back to ticketing inventory.", "ticketmaster"),
                    tile("Staff Shift Dispatch", "people", "Concessions and security shift changes pushed to crew devices.", "ukg"),
                    tile("Coaching Clip Tags", "stream", "Tagged video moments written to the coaching platform.", "second-spectrum"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("League Revenue Share", "gavel", "Gate and local revenue reports filed to the league.", "stats-perform"),
                    tile("Safety Incident Reports", "share", "Crowd and medical incidents documented from governed logs.", "genetec"),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Fan and performance products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "League partners reading live attendance via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Game-Day Command", "Venue operations", "gauge", "Live ingress, concessions throughput and security incidents on Databricks Apps over Lakebase."),
             app("Pricing Workbench", "Ticket yield", "market", "Demand curves and price tiers before on-sale and throughout the sales window."),
             app("Fan 360 Console", "Engagement view", "custlake", "Ticketing, concessions and CRM activity stitched per fan segment."),
             app("Load Management Hub", "Athlete readiness", "iot", "Player workload, injury risk and selection recommendations for coaching staff.")],
            [uc("Dynamic Ticket Pricing", "Revenue", "market", "Price tiers adjusted to demand, inventory and secondary market pressure."),
             uc("Fan Churn Prediction", "CRM", "custlake", "Season ticket and membership churn scored before renewal windows."),
             uc("Concessions Optimization", "F&B", "product", "Stand staffing and menu mix tuned to expected attendance and weather."),
             uc("Sponsorship ROI", "Commercial", "partner", "Activation impressions and conversions attributed to sponsor inventory."),
             uc("Injury Risk Scoring", "Performance", "iot", "Load and biomechanical signals flagging elevated injury risk."),
             uc("Broadcast Highlights", "Media", "stream", "Automated clip selection and publishing from live feeds."),
             uc("Crowd Safety Analytics", "Operations", "gauge", "Density and ingress patterns flagged before capacity thresholds."),
             uc("Secondary Market Intel", "Ticketing", "chart", "Transfer and resale activity informing primary pricing."),
             uc("OTT Personalization", "Streaming", "api", "Content recommendations and offers scored per viewer segment."),
             uc("Merchandise Forecast", "Retail", "erp", "Event-level merch demand forecast tied to opponent and promotion.")],
        ),
        "sources": {
            "ticketmaster": {"t": "Ticketmaster Archtics", "u": "https://business.ticketmaster.com/"},
            "sf-sports": {"t": "Salesforce Sports Cloud", "u": "https://www.salesforce.com/"},
            "seatgeek": {"t": "SeatGeek Enterprise", "u": "https://seatgeek.com/enterprise"},
            "venuenext": {"t": "VenueNext", "u": "https://www.venuenext.com/"},
            "genetec": {"t": "Genetec Security Center", "u": "https://www.genetec.com/"},
            "ukg": {"t": "UKG workforce management", "u": "https://www.ukg.com/"},
            "grabyo": {"t": "Grabyo", "u": "https://about.grabyo.com/"},
            "deltatre": {"t": "Deltatre OTT", "u": "https://www.deltatre.com/"},
            "nielsen-sports": {"t": "Nielsen Sports", "u": "https://www.nielsen.com/"},
            "sponsorunited": {"t": "SponsorUnited", "u": "https://www.sponsorunited.com/"},
            "trade-desk": {"t": "The Trade Desk", "u": "https://www.thetradedesk.com/"},
            "catapult": {"t": "Catapult Sports", "u": "https://www.catapult.com/"},
            "second-spectrum": {"t": "Second Spectrum", "u": "https://www.secondspectrum.com/"},
            "stats-perform": {"t": "Stats Perform", "u": "https://www.statsperform.com/"},
        },
    },
}
