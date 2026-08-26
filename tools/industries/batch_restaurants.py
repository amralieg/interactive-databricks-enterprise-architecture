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


INDUSTRIES_BATCH_RESTAURANTS = {
    'restaurants': {
        "label": "Restaurants",
        "blurb": "Restaurant and foodservice operators: POS and kitchen execution, inventory and labor, franchise performance and delivery marketplace integration.",
        "medallion": medallion(
            "Raw ticket and labor",
            "POS checks, kitchen display events, inventory counts, timeclock punches and delivery platform orders, landed exactly as received so a ticket or a shift can always be replayed as it stood.",
            "Conformed store, item",
            "Stores, menu items, employees and shifts resolved into single conformed entities across POS, back-office and delivery systems, with voids and comps reconciled and channel orders stitched to one guest check.",
            "Sales, labor, margin",
            "Contracted products operations and finance run on: comparable sales, labor percent and food cost percent by store and daypart.",
        ),
        "rails": {
            "src": [
                {"box": "POS & Kitchen", "ic": "market", "tiles": [
                        tile("NCR Aloha POS", "market", "Guest checks, modifiers, voids and payment tenders from dine-in and bar.", "ncr-aloha"),
                        tile("Toast Restaurant POS", "partner", "Full-service and QSR transactions with online ordering integration.", "toast"),
                        tile("QSR Automations KDS", "stream", "Kitchen display timing, bump events and course sequencing.", "qsr-automations"),
                    ]},
                {"box": "Back Office & ERP", "ic": "erp", "tiles": [
                        tile("Restaurant365", "erp", "AP, inventory, scheduling and store P&L for multi-unit operators.", "r365"),
                        tile("CrunchTime Inventory", "sheet", "Food counts, theoretical usage and waste tracking by store.", "crunchtime"),
                        tile("SAP Business One", "db", "Franchise billing, royalties and consolidated financial close.", "sap-b1"),
                    ]},
                {"box": "Labor & Scheduling", "ic": "people", "tiles": [
                        tile("HotSchedules", "people", "Shift schedules, punches and labor compliance across locations.", "hotschedules"),
                        tile("Deputy Workforce", "chart", "Time and attendance, leave and wage rules for hourly teams.", "deputy"),
                        tile("Harri Talent Platform", "custlake", "Hiring, onboarding and turnover metrics by store and role.", "harri"),
                    ]},
                {"box": "Delivery & Loyalty", "ic": "partner", "tiles": [
                        tile("DoorDash Marketplace", "partner", "Third-party delivery orders, fees and customer ratings by store.", "doordash"),
                        tile("Uber Eats Merchant", "api", "Delivery channel orders, adjustments and payout statements.", "uber-eats"),
                        tile("Paytronix Loyalty", "custlake", "Guest profiles, offers redeemed and visit frequency.", "paytronix"),
                    ]},
                fed_group("Franchisee P&L Mart", "Franchise unit economics left at franchisees and queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("Weather & Events API", "globe", "Local weather and event calendars consumed inbound for demand forecasting."),
                tile("Commodity Price Feeds", "market", "Protein and produce indices normalised for menu engineering alerts.", "usda-ams"),
                tile("Health Dept Inspections", "gavel", "Municipal inspection scores parsed for franchise compliance monitoring."),
            ]),
            "ppl": ppl_rail2([
                biz("Brand Leadership", "Genie One", "The CEO on comparable sales and franchise growth; the CFO on food and labor cost percent when commodity prices and hourly wages spike.", [["Genie One", "Ask what yesterday's comp sales were by banner without waiting on operations."], ["AI/BI", "Sales, labor and margin on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"comp\" means one thing across POS and ERP."]]),
                biz("Operations", "Lakehouse//RT", "Regional directors on speed of service, void rates and shift execution, watching ticket times and order accuracy against the operations plan.", [["Store Performance", "Ticket times and void pareto before the ops call."], ["Lakehouse//RT", "Kitchen bump events at service latency."], ["AI/BI", "Speed and accuracy on governed definitions."]]),
                biz("Finance & Accounting", "AI/BI", "Controllers on food cost percent, cash over-short and franchise royalties, tracking prime cost against budget before period close.", [["Food Cost Dashboard", "Theoretical versus actual usage before period close."], ["AI/BI", "P&L and prime cost on certified Metric Views."], ["Genie One", "Ask which stores missed food cost budget last week."]]),
                biz("Marketing & Loyalty", "CustomerLake", "Brand teams on offers, LTO performance and guest retention, tracking redemption lift and visit frequency across the loyalty base.", [["Loyalty Campaign Hub", "Offer redemption and lift before national promos launch."], ["CustomerLake", "Guest segments without copying loyalty DB elsewhere."], ["Model Serving", "Churn models scored on visit patterns."]]),
                biz("Franchise Development", "Apps", "Franchise leadership on unit economics, compliance and new store pipeline, tracking unit-level P&L and audit scores by franchisee.", [["Franchise Scorecard", "Unit P&L and audit scores by franchisee."], ["Apps", "Compliance workflows on governed operations data."], ["Unity Catalog", "One store definition across franchise and corporate."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the POS, KDS, inventory and delivery-platform feeds; own the Bronze to Silver path and the pager when a store pipeline breaks.", [["Lakeflow Connect", "Managed connectors for POS, back-office and delivery sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on check and punch feeds."], ["Lakewatch", "Freshness on the comp sales and food cost tables ops reads."]]),
                biz("Data Scientists", "MLflow", "Demand-forecast, labor-optimisation, menu-engineering and guest-churn models, and whether they still hold six months after deployment across stores.", [["Feature Store", "Traffic and weather features read identically in training and serving."], ["MLflow", "Every forecast and churn run tracked for audit and reproduction."], ["Model Serving", "Demand and churn models scored in the scheduling and loyalty path."]]),
                biz("App Developers", "Apps", "Ship the store performance, food cost and franchise applications operators and finance work in, hosted next to governed store data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for schedule state and governed writes."], ["Agent Bricks", "Agents that draft a purchase order against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                        tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                        tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and shift updates in the channel ops already works in (Beta)."),
                        tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code."),
                    ]},
                {"box": "Store Writeback", "ic": "opdb", "tiles": [
                        tile("POS Menu Push", "market", "Approved menu and price changes distributed to stores from governed configs.", "toast"),
                        tile("Schedule Publish", "people", "Optimised shift plans written back to scheduling before the week locks.", "hotschedules"),
                        tile("Inventory Orders", "erp", "Suggested purchase orders raised from theoretical usage variances.", "crunchtime"),
                    ]},
                {"box": "Franchise & Delivery", "ic": "partner", "tiles": [
                        tile("Franchisee Portal", "share", "Scorecards and benchmarks shared to franchisees over Delta Sharing.", "r365"),
                        tile("Delivery Platform API", "api", "Menu availability and prep times synced to marketplaces from governed store state.", "doordash"),
                        tile("Supplier Portal", "partner", "Distributor case fills exchanged without emailed order spreadsheets."),
                    ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                        tile("Food Safety Audits", "gavel", "HACCP and health inspection records produced from governed operations tables."),
                        tile("Franchise Disclosure", "share", "Unit economic summaries filed from contracted Gold products.", "sap-b1"),
                    ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                        tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                        tile("Sharing Recipients", "share", "Franchisees, auditors and partners reading live tables with no copy."),
                    ]},
            ]),
        },
        "top": top_band(
            [
                app("Store Performance", "Comp sales live", "gauge", "Ticket times, voids and daypart sales on Databricks Apps over Lakebase."),
                app("Food Cost Dashboard", "Prime cost", "sheet", "Theoretical versus actual food cost before period close."),
                app("Loyalty Campaign Hub", "Offer lift", "custlake", "Redemption and incremental visits before national promos launch."),
                app("Franchise Scorecard", "Unit economics", "partner", "P&L, audit scores and compliance by franchisee on one surface."),
            ],
            [
                uc("Demand Forecasting", "Planning", "chart", "Store-level sales forecast tuned to weather, events and promos."),
                uc("Labor Optimisation", "Scheduling", "people", "Shift plans matched to forecasted traffic without overtime creep."),
                uc("Food Cost Control", "Margin", "sheet", "Waste and portion variance attacked with theoretical usage evidence."),
                uc("Menu Engineering", "Profitability", "product", "Items ranked by contribution margin and popularity not gut feel."),
                uc("Speed of Service", "Operations", "stream", "Kitchen and drive-thru times improved with bump-to-ticket analytics."),
                uc("Delivery Channel Mix", "Digital", "partner", "Marketplace fees and order mix optimised for net margin per store."),
                uc("Guest Churn", "Loyalty", "custlake", "Lapsed guests identified before loyalty points expire."),
                uc("Franchise Compliance", "Audit", "gavel", "Food safety and ops standards scored before field audits."),
                uc("Shrink & Void Control", "Loss prevention", "gauge", "Suspicious void and comp patterns surfaced by employee and shift."),
                uc("New Store Analytics", "Growth", "globe", "Ramp curves and trade-area performance scored against pro forma."),
            ],
        ),
        "sources": {
            "ncr-aloha": {"t": "NCR Aloha POS", "u": "https://www.ncr.com/restaurants/aloha-pos"},
            "toast": {"t": "Toast POS", "u": "https://pos.toasttab.com/"},
            "qsr-automations": {"t": "QSR Automations", "u": "https://www.qsrautomations.com/"},
            "r365": {"t": "Restaurant365", "u": "https://www.restaurant365.com/"},
            "crunchtime": {"t": "CrunchTime", "u": "https://www.crunchtime.com/"},
            "sap-b1": {"t": "SAP Business One", "u": "https://www.sap.com/products/erp/business-one.html"},
            "hotschedules": {"t": "HotSchedules", "u": "https://www.hotschedules.com/"},
            "deputy": {"t": "Deputy", "u": "https://www.deputy.com/"},
            "harri": {"t": "Harri", "u": "https://harri.com/"},
            "doordash": {"t": "DoorDash for Merchants", "u": "https://merchants.doordash.com/"},
            "uber-eats": {"t": "Uber Eats Manager", "u": "https://merchants.ubereats.com/"},
            "paytronix": {"t": "Paytronix", "u": "https://www.paytronix.com/"},
            "usda-ams": {"t": "USDA AMS Market News", "u": "https://www.ams.usda.gov/market-news"},
        },
    },
}
