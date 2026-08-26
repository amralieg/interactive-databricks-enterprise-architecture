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


INDUSTRIES_BATCH_WASTE_MANAGEMENT = {
    'waste_management': {
        "label": "Waste Management",
        "blurb": "Collection, transfer and disposal: route optimisation, scalehouse and landfill operations, customer billing, fleet telematics, and environmental compliance across municipal and commercial contracts.",
        "medallion": medallion(
            "Raw route and scale feeds",
            "Route completion events, scalehouse tickets, GPS and lift sensor reads, customer service orders and billing cycles, landed exactly as received so a missed stop or a tonnage line can always be replayed.",
            "Conformed customer, route",
            "Customers, routes, stops and disposal tickets resolved into single conformed entities across billing, dispatch and scale systems, with service history stitched to one account.",
            "Cost per ton, diversion",
            "Contracted products operations and sustainability teams run on: cost per ton, diversion rate, missed stops, landfill airspace and customer churn by segment.",
        ),
        "rails": {
            "src": [
                {"box": "Billing & CRM", "ic": "erp", "tiles": [
                    tile("AMCS Platform", "erp", "Customer accounts, service schedules, pricing and invoicing for haulers.", "amcs"),
                    tile("Routeware Account", "market", "Commercial and residential billing with container asset tracking.", "routeware"),
                    tile("Salesforce Service Cloud", "custlake", "Service cases, missed pickups and contract amendments.", "sf-service"),
                ]},
                {"box": "Dispatch & Routes", "ic": "sheet", "tiles": [
                    tile("RouteSmart", "sheet", "Route design, sequencing and balance for residential and commercial lines.", "routesmart"),
                    tile("AMCS Dispatch", "stream", "Daily dispatch, turn-by-turn and completion confirmation.", "amcs-dispatch"),
                    tile("Rubicon Route Assist", "partner", "Dynamic routing and contamination feedback from driver devices.", "rubicon"),
                ]},
                {"box": "Fleet & Telematics", "ic": "iot", "tiles": [
                    tile("Geotab Fleet", "iot", "Vehicle location, idle time, fuel and maintenance for collection fleets.", "geotab"),
                    tile("Motive ELD", "stream", "Hours of service and safety events for CDL drivers.", "motive"),
                    tile("Lift Sensors & RFID", "partner", "Automated lift counts and container identification on trucks.", "rubicon"),
                ]},
                {"box": "Disposal & MRF", "ic": "db", "tiles": [
                    tile("Scalehouse Pro", "db", "Inbound and outbound scale tickets, tare and moisture adjustments.", "scalehouse"),
                    tile("Landfill Gas Monitor", "iot", "Gas extraction, flare and wellfield readings for compliance.", "landfill-gas"),
                    tile("Machinex MRF SCADA", "stream", "Material recovery throughput, contamination and bale weights.", "machinex"),
                ]},
                {"box": "Compliance & ESG", "ic": "gavel", "tiles": [
                    tile("Enablon EHS", "gavel", "Permits, inspections and incident reporting for disposal sites.", "enablon"),
                    tile("Wastebits Reporting", "chart", "Diversion, recycling and landfill tonnage for municipal reporting.", "wastebits"),
                ]},
                fed_group("Municipal Contract Marts", "City tonnage and franchise fee marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("EPA LMOP Data", "gavel", "Landfill gas and emissions reference data for compliance benchmarking.", "epa-lmop"),
                tile("State Diversion Reports", "api", "Mandatory recycling reporting files consumed for municipal contracts.", "wastebits"),
                tile("Recycling Market Indices", "market", "Commodity bale price indices for MRF revenue planning.", "machinex"),
            ]),
            "ppl": ppl2([
                biz("CEO & Ops Office", "Genie One", "The CEO on margin per ton and contract renewal; the COO on route productivity, missed stops and the collection fleet's safety record.",
                    [["Genie One", "Ask what last month's diversion rate was without analyst delay."], ["AI/BI", "Cost per ton and missed stops on certified Metric Views."], ["Unity Catalog", "One ton definition across scale and billing."]]),
                biz("Collection Ops", "Lakehouse//RT", "Dispatchers on route completion, missed stops and contamination callbacks, re-sequencing trucks before a service gap becomes a credit.",
                    [["Dispatch Console", "Live trucks, stops and exceptions on one map."], ["Lakehouse//RT", "GPS and lift events at route latency."]]),
                biz("Disposal & MRF", "Apps", "Landfill and MRF managers on remaining airspace, throughput and commodity revenue, balancing inbound tons against permitted daily capacity.",
                    [["Scalehouse Dashboard", "Inbound tons, diversion and bale inventory in real time."], ["Apps", "Site apps hosted next to governed scale data."]]),
                biz("Commercial Sales", "AI/BI", "Account managers on pricing, service changes and churn risk, protecting margin per customer segment before a contract comes up for renewal.",
                    [["AI/BI", "Revenue and margin by customer segment on certified views."], ["Genie One", "Ask which accounts are below target margin."]]),
                biz("Sustainability", "Lakeflow", "ESG teams on diversion rate, circularity and municipal reporting, proving material flows by customer and site against franchise commitments.",
                    [["Diversion Registry", "Material flows and diversion evidence by customer and site."], ["Lakeflow", "Scale and route feeds conformed for ESG analytics."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land route completion events, scale tickets, GPS and lift sensor reads; own Bronze to Silver and the pager when a cost-per-ton table breaks.",
                    [["Lakeflow Connect", "Managed connectors for billing, dispatch and scale sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on route and scale feeds."], ["Lakewatch", "Freshness on the diversion tables operations reads each morning."]]),
                biz("Data Scientists", "MLflow", "Missed-stop, contamination-detection, churn and commodity-revenue models, and whether they still hold as routes and bale indices shift.",
                    [["Feature Store", "Route and customer features read identically in training and serving."], ["MLflow", "Every routing and churn experiment tracked for audit."], ["Model Serving", "Missed-stop and churn models scored in the dispatch path."]]),
                biz("App Developers", "Apps", "Ship the Dispatch Console, Scalehouse Dashboard and Diversion Registry apps operations and ESG teams work in, next to governed scale data.",
                    [["Apps", "Site and dispatch screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for stop and ticket state writes."], ["Agent Bricks", "Agents that draft route changes against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Operations and ESG dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for route and diversion questions in the dispatch channel."),
                    tile("Notebooks & IDEs", "notebook", "Route optimisation notebooks against governed telematics data."),
                ]},
                {"box": "Customer & Municipal", "ic": "partner", "tiles": [
                    tile("Customer Service Portal", "api", "Pickup status and billing inquiries served from governed data.", "amcs"),
                    tile("Municipal Reporting API", "share", "Diversion and tonnage reports shared to city contracts over Delta Sharing.", "wastebits"),
                    tile("Broker Bale Sales", "market", "Commodity availability shared to recycling brokers."),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Route Re-sequence", "sheet", "Optimised stop order written back to driver devices.", "routesmart"),
                    tile("Service Order Dispatch", "apps", "Extra pickups and container swaps dispatched to crews.", "amcs-dispatch"),
                    tile("Scale Ticket Posting", "db", "Tonnage and material class written to billing and inventory.", "scalehouse"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Landfill Compliance", "gavel", "Gas, leachate and cover inspection reports filed from site logs.", "enablon"),
                    tile("Extended Producer Resp", "share", "EPR tonnage evidence submitted from contracted Gold products.", "wastebits"),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Diversion and route performance products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Municipal clients reading live tonnage via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Dispatch Console", "Route execution", "gauge", "Live trucks, stop completion and exceptions on a map with driver messaging."),
             app("Scalehouse Dashboard", "Disposal ops", "db", "Inbound tons, material class and bale inventory for landfill and MRF sites."),
             app("Diversion Registry", "ESG reporting", "gavel", "Material flows and diversion evidence by customer, route and facility."),
             app("Commercial Pricing Hub", "Account margin", "market", "Service pricing and margin by customer segment before renewal.")],
            [uc("Route Optimization", "Collection", "sheet", "Residential and commercial routes rebalanced for miles, time and safety."),
             uc("Missed Stop Prediction", "Service", "stream", "Stops at risk of miss flagged from GPS and historical patterns."),
             uc("Contamination Detection", "Recycling", "iot", "Contamination events from lift sensors and MRF cameras."),
             uc("Landfill Airspace", "Disposal", "db", "Airspace consumption forecast against permitted capacity."),
             uc("Dynamic Pricing", "Commercial", "market", "Container and service fees adjusted to margin and churn risk."),
             uc("Fleet Maintenance", "Assets", "iot", "Predictive maintenance from telematics before breakdown on route."),
             uc("MRF Commodity Revenue", "Recycling", "market", "Bale revenue forecast against commodity index movements."),
             uc("Customer Churn", "Sales", "custlake", "Commercial account churn scored from service quality and price."),
             uc("Municipal Franchise", "Contracts", "gavel", "Franchise fee and service level evidence for city audits."),
             uc("Carbon & Methane", "ESG", "chart", "Landfill gas capture and fleet emissions for sustainability reporting.")],
        ),
        "sources": {
            "amcs": {"t": "AMCS Platform", "u": "https://www.amcsgroup.com/"},
            "routeware": {"t": "Routeware", "u": "https://www.routeware.com/"},
            "sf-service": {"t": "Salesforce Service Cloud", "u": "https://www.salesforce.com/service/"},
            "routesmart": {"t": "RouteSmart", "u": "https://www.routesmart.com/"},
            "amcs-dispatch": {"t": "AMCS Dispatch", "u": "https://www.amcsgroup.com/"},
            "rubicon": {"t": "Rubicon", "u": "https://www.rubicon.com/"},
            "geotab": {"t": "Geotab", "u": "https://www.geotab.com/"},
            "motive": {"t": "Motive", "u": "https://gomotive.com/"},
            "scalehouse": {"t": "Scalehouse software", "u": "https://www.amcsgroup.com/"},
            "landfill-gas": {"t": "Landfill gas monitoring", "u": "https://www.epa.gov/lmop"},
            "machinex": {"t": "Machinex MRF", "u": "https://www.machinexrecycling.com/"},
            "enablon": {"t": "Enablon EHS", "u": "https://www.wolterskluwer.com/en/solutions/enablon"},
            "wastebits": {"t": "Wastebits", "u": "https://www.wastebits.com/"},
            "epa-lmop": {"t": "EPA LMOP", "u": "https://www.epa.gov/lmop"},
        },
    },
}
