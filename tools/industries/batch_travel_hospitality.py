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


INDUSTRIES_BATCH_TRAVEL_HOSPITALITY = {
    'travel_hospitality': {
        "label": "Travel & Hospitality",
        "blurb": "Hotels, resorts and travel sellers: property management, central reservations, revenue management, guest loyalty, and distribution across direct and OTA channels.",
        "medallion": medallion(
            "Raw guest and booking feeds",
            "PMS reservations, CRS availability, POS folios, loyalty transactions and OTA bookings, landed exactly as received so a rate or a stay can always be replayed.",
            "Conformed guest, stay, room",
            "Guests, stays, room nights and rate plans resolved into single conformed entities across PMS, CRS and loyalty, with multi-property journeys stitched to one profile.",
            "RevPAR, ADR, occupancy",
            "Contracted products commercial and operations teams run on: RevPAR and ADR by segment, occupancy forecast, guest satisfaction and ancillary attach rate.",
        ),
        "rails": {
            "src": [
                {"box": "PMS & Operations", "ic": "erp", "tiles": [
                    tile("Oracle OPERA Cloud", "erp", "Property management: reservations, housekeeping, folios and night audit.", "opera-cloud"),
                    tile("Mews PMS", "apps", "Cloud PMS for boutique and multi-property groups with open APIs.", "mews"),
                    tile("Infor HMS", "db", "Hotel operations, group blocks and event catering for full-service properties.", "infor-hms"),
                ]},
                {"box": "CRS & Distribution", "ic": "market", "tiles": [
                    tile("Amadeus iHotelier", "globe", "Central reservations, rate distribution and channel management.", "amadeus-ihotelier"),
                    tile("Sabre SynXis", "partner", "CRS, booking engine and GDS connectivity for hotel brands.", "sabre-synxis"),
                    tile("SiteMinder Channel", "api", "OTA and metasearch connectivity with parity monitoring.", "siteminder"),
                ]},
                {"box": "Revenue Management", "ic": "chart", "tiles": [
                    tile("IDeaS G3 RMS", "market", "Forecasting, price recommendations and length-of-stay controls.", "ideas-rms"),
                    tile("Duetto GameChanger", "sheet", "Open pricing and segment-level optimisation for casinos and resorts.", "duetto"),
                    tile("OTA Insight", "observ", "Competitive rate shopping and market demand indices.", "ota-insight"),
                ]},
                {"box": "Guest & Loyalty", "ic": "custlake", "tiles": [
                    tile("Salesforce Loyalty", "custlake", "Tier status, points accrual and partner earn across the portfolio.", "sf-loyalty"),
                    tile("Medallia Guest", "partner", "Post-stay surveys, sentiment and recovery workflows.", "medallia-guest"),
                    tile("SevenRooms CRM", "product", "Restaurant reservations and guest preferences for F&B outlets.", "sevenrooms"),
                ]},
                {"box": "Spa & Ancillary", "ic": "product", "tiles": [
                    tile("Book4Time Spa", "apps", "Spa and activity scheduling, therapist utilisation and retail attach.", "book4time"),
                    tile("Agilysys InfoGenesis", "erp", "Outlet POS for restaurants, bars and room charges to folio.", "agilysys-pos"),
                ]},
                fed_group("Ownership Group Marts", "Owner reporting and STR benchmark marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("STR Benchmark Feed", "chart", "Smith Travel Research comp set occupancy and rate benchmarks.", "str"),
                tile("GDS Booking Messages", "stream", "Amadeus and Sabre hotel booking notifications parsed on arrival.", "amadeus-ihotelier"),
                tile("Review Aggregator APIs", "observ", "TripAdvisor and Google review feeds for reputation monitoring.", "medallia-guest"),
            ]),
            "ppl": ppl2([
                biz("CEO & Brand Office", "Genie One", "The CEO on RevPAR and gross operating profit; the COO on guest satisfaction and labour productivity across the property portfolio.",
                    [["Genie One", "Ask what last weekend's RevPAR was without analyst delay."], ["AI/BI", "RevPAR and occupancy on certified Metric Views."], ["Unity Catalog", "One room night definition across PMS and finance."]]),
                biz("Revenue Management", "Model Serving", "Revenue managers on price ladders, overrides and group displacement, defending ADR and occupancy against the compset before rates publish.",
                    [["RMS Workbench", "Forecast, compset and recommendation history before override."], ["Model Serving", "Pricing models scored in the distribution path."]]),
                biz("Front Office & Ops", "Lakehouse//RT", "GMs and front office on arrivals, housekeeping turn and service recovery, clearing rooms and VIP flags before the guest reaches the desk.",
                    [["Property Command", "Arrivals, VIP flags and housekeeping status on one screen."], ["Lakehouse//RT", "Room and task state at front-desk latency."]]),
                biz("Sales & Groups", "AI/BI", "Sales directors on group blocks, catering revenue and conversion, watching pickup pace and wash against the block before the cutoff date.",
                    [["AI/BI", "Group pace and wash on certified views."], ["Genie One", "Ask which groups are below pickup pace."]]),
                biz("Marketing & Loyalty", "CustomerLake", "CRM teams on campaigns, tier economics and personalisation, scoring offer propensity and tier migration across the guest portfolio.",
                    [["Loyalty Console", "Offer propensity and tier migration by segment."], ["CustomerLake", "Guest profiles without copying into a separate CDP."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land PMS reservations, CRS availability, POS folios and loyalty transactions; own Bronze to Silver and the pager when a RevPAR table stalls.",
                    [["Lakeflow Connect", "Managed connectors for PMS, CRS and loyalty sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on reservation and folio feeds."], ["Lakewatch", "Freshness on the RevPAR tables the revenue meeting reads."]]),
                biz("Data Scientists", "MLflow", "Demand-forecast, dynamic-pricing, personalisation and group-displacement models, and whether they still hold as compset and channel mix shift.",
                    [["Feature Store", "Guest and rate features read identically in training and serving."], ["MLflow", "Every forecast and pricing experiment tracked for audit."], ["Model Serving", "Pricing and offer models scored in the distribution path."]]),
                biz("App Developers", "Apps", "Ship the Property Command, RMS Workbench and Loyalty Console apps revenue and front-office teams work in, next to governed PMS data.",
                    [["Apps", "Property screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for arrival and offer state writes."], ["Agent Bricks", "Agents that draft rate moves against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Portfolio and property dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for RevPAR and occupancy in the revenue meeting channel."),
                    tile("Notebooks & IDEs", "notebook", "Revenue science notebooks against governed PMS and RMS data."),
                ]},
                {"box": "Distribution & OTA", "ic": "partner", "tiles": [
                    tile("Channel Rate API", "api", "Rate and availability pushed to OTAs and metasearch.", "siteminder"),
                    tile("GDS Availability", "globe", "ARI updates to Amadeus and Sabre for travel agency bookings.", "sabre-synxis"),
                    tile("Corporate Travel Portal", "share", "Negotiated rates and booking rules shared to TMC partners."),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("RMS Price Push", "market", "Recommended rates written back to CRS and channel manager.", "ideas-rms"),
                    tile("Housekeeping Tasks", "apps", "Room status and task lists pushed to attendant devices.", "opera-cloud"),
                    tile("Guest Pre-arrival", "custlake", "Upsell offers and preferences written to the arrival profile.", "mews"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Tourism Tax Filings", "gavel", "Occupancy and tourism taxes filed from night audit.", "opera-cloud"),
                    tile("Franchise Reporting", "share", "Brand-mandated KPIs submitted from contracted Gold products."),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Portfolio performance products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Owners and brands reading live KPIs via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Property Command", "Front office", "gauge", "Arrivals, VIP flags, housekeeping and service issues on Databricks Apps over Lakebase."),
             app("RMS Workbench", "Pricing decisions", "market", "Forecast, compset position and override history before rates publish."),
             app("Loyalty Console", "Guest CRM", "custlake", "Tier status, offer propensity and stay history for personalised engagement."),
             app("Group Sales Hub", "Blocks & events", "sheet", "Group pickup, catering revenue and wash risk before the cutoff date.")],
            [uc("Dynamic Pricing", "Revenue", "market", "Open pricing by segment and channel rather than fixed BAR ladders."),
             uc("Occupancy Forecast", "Planning", "chart", "Demand forecast by property, segment and length of stay."),
             uc("Guest Personalization", "CRM", "custlake", "Pre-arrival upsell and in-stay offers scored per guest profile."),
             uc("Reputation Recovery", "Service", "partner", "Negative reviews and survey detractors routed to recovery workflows."),
             uc("Labour Scheduling", "Operations", "people", "Housekeeping and F&B labour matched to forecast occupancy."),
             uc("Channel Parity", "Distribution", "api", "Rate and availability parity monitored across OTA and direct."),
             uc("Group Displacement", "Sales", "sheet", "Group blocks evaluated against transient opportunity cost."),
             uc("Ancillary Attach", "F&B", "product", "Spa, dining and experience attach scored at booking and check-in."),
             uc("Loyalty Tier Migration", "Loyalty", "custlake", "Tier upgrade and churn risk scored before renewal windows."),
             uc("Owner Reporting", "Finance", "erp", "Owner statements and STR index position from governed night audit.")],
        ),
        "sources": {
            "opera-cloud": {"t": "Oracle OPERA Cloud", "u": "https://www.oracle.com/hospitality/hotel-property-management/"},
            "mews": {"t": "Mews PMS", "u": "https://www.mews.com/"},
            "infor-hms": {"t": "Infor HMS", "u": "https://www.infor.com/industries/hospitality"},
            "amadeus-ihotelier": {"t": "Amadeus iHotelier", "u": "https://amadeus.com/en/industries/hotels"},
            "sabre-synxis": {"t": "Sabre SynXis", "u": "https://www.sabrehospitality.com/"},
            "siteminder": {"t": "SiteMinder", "u": "https://www.siteminder.com/"},
            "ideas-rms": {"t": "IDeaS G3 RMS", "u": "https://ideas.com/"},
            "duetto": {"t": "Duetto", "u": "https://www.duettocloud.com/"},
            "ota-insight": {"t": "OTA Insight", "u": "https://www.otainsight.com/"},
            "sf-loyalty": {"t": "Salesforce Loyalty Management", "u": "https://www.salesforce.com/products/loyalty-management/"},
            "medallia-guest": {"t": "Medallia for hospitality", "u": "https://www.medallia.com/industries/hospitality/"},
            "sevenrooms": {"t": "SevenRooms", "u": "https://sevenrooms.com/"},
            "book4time": {"t": "Book4Time", "u": "https://www.book4time.com/"},
            "agilysys-pos": {"t": "Agilysys InfoGenesis", "u": "https://www.agilysys.com/"},
            "str": {"t": "STR benchmarks", "u": "https://str.com/"},
        },
    },
}
