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
                    tile("Paradigm Software", "db", "Inbound and outbound scale tickets, tare and moisture adjustments.", "scalehouse"),
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
                    [["Genie One", "Ask what last month's diversion rate was without analyst delay."], ["AI/BI", "Cost per ton and missed stops on certified Metric Views."], ["Unity Catalog", "One ton definition across scale and billing."]],
                    sub=[
                        ["CEO", "margin per ton, contract renewals and the growth-versus-cost trade across the book."],
                        ["Chief Operating Officer", "route productivity, missed stops and the collection fleet's safety record."],
                        ["VP Finance", "cost per ton, disposal spend and cash across municipal and commercial contracts."],
                    ],
                    ucs=["Route Optimization", "Missed Stop Prediction", "Dynamic Pricing", "Fleet Maintenance"]),
                biz("Collection Ops", "Lakehouse//RT", "Dispatchers on route completion, missed stops and contamination callbacks, re-sequencing trucks before a service gap becomes a credit.",
                    [["Dispatch Console", "Live trucks, stops and exceptions on one map."], ["Lakehouse//RT", "GPS and lift events at route latency."]],
                    sub=[
                        ["Dispatch Supervisors", "live route completion, exceptions and re-sequencing trucks before a service gap."],
                        ["Route Managers", "route balance, productivity and the miles and time each line runs."],
                        ["Fleet & Safety", "vehicle uptime, driver hours-of-service and the collection fleet's safety record."],
                    ],
                    ucs=["Route Optimization", "Missed Stop Prediction", "Fleet Maintenance"]),
                biz("Disposal & MRF", "Apps", "Landfill and MRF managers on remaining airspace, throughput and commodity revenue, balancing inbound tons against permitted daily capacity.",
                    [["Scalehouse Dashboard", "Inbound tons, diversion and bale inventory in real time."], ["Apps", "Site apps hosted next to governed scale data."]],
                    sub=[
                        ["Landfill Managers", "remaining permitted airspace, gas capture and inbound tons against daily capacity."],
                        ["MRF Plant Managers", "recovery throughput, bale quality and contamination in the recycling stream."],
                        ["Scalehouse Leads", "tare, moisture and material class on every inbound and outbound ticket."],
                    ],
                    ucs=["Landfill Airspace", "Contamination Detection", "MRF Commodity Revenue"]),
                biz("Commercial Sales", "AI/BI", "Account managers on pricing, service changes and churn risk, protecting margin per customer segment before a contract comes up for renewal.",
                    [["AI/BI", "Revenue and margin by customer segment on certified views."], ["Genie One", "Ask which accounts are below target margin."]],
                    sub=[
                        ["Account Managers", "service changes, churn risk and margin per commercial account."],
                        ["Pricing & Revenue", "container and service fees against cost-to-serve and the market."],
                        ["Contract Renewals", "at-risk accounts and the terms up for renewal this quarter."],
                    ],
                    ucs=["Dynamic Pricing", "Customer Churn", "Municipal Franchise"]),
                biz("Sustainability", "Lakeflow", "ESG teams on diversion rate, circularity and municipal reporting, proving material flows by customer and site against franchise commitments.",
                    [["Diversion Registry", "Material flows and diversion evidence by customer and site."], ["Lakeflow", "Scale and route feeds conformed for ESG analytics."]],
                    sub=[
                        ["ESG Reporting", "diversion rate, carbon and methane against franchise and corporate commitments."],
                        ["Diversion & Circularity", "material flows and recovered-tonnage evidence by customer and site."],
                        ["Regulatory Affairs", "permits, EPR obligations and the mandatory municipal reporting calendar."],
                    ],
                    ucs=["Carbon & Methane", "Municipal Franchise", "Contamination Detection"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land route completion events, scale tickets, GPS and lift sensor reads; own Bronze to Silver and the pager when a cost-per-ton table breaks.",
                    [["Lakeflow Connect", "Managed connectors for billing, dispatch and scale sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on route and scale feeds."], ["Lakewatch", "Freshness on the diversion tables operations reads each morning."]],
                    sub=[
                        ["Ingestion Engineers", "billing, dispatch, scale and telematics sources landed exactly as received."],
                        ["Pipeline & Streaming", "GPS and lift events at route latency and the Bronze-to-Silver path."],
                        ["Data Quality & SRE", "expectations and freshness on the cost-per-ton and diversion tables."],
                    ],
                    ucs=["Route Optimization", "Missed Stop Prediction", "MRF Commodity Revenue"]),
                biz("Data Scientists", "MLflow", "Missed-stop, contamination-detection, churn and commodity-revenue models, and whether they still hold as routes and bale indices shift.",
                    [["Feature Store", "Route and customer features read identically in training and serving."], ["MLflow", "Every routing and churn experiment tracked for audit."], ["Model Serving", "Missed-stop and churn models scored in the dispatch path."]],
                    sub=[
                        ["Routing & Ops ML", "miss-risk, route and remaining-life models scored in the dispatch path."],
                        ["Vision & Contamination", "camera and lift-sensor models flagging contaminated recycling loads."],
                        ["Churn & Pricing", "commercial churn and price-elasticity models against service and billing."],
                    ],
                    ucs=["Missed Stop Prediction", "Contamination Detection", "Customer Churn", "Fleet Maintenance"]),
                biz("App Developers", "Apps", "Ship the Dispatch Console, Scalehouse Dashboard and Diversion Registry apps operations and ESG teams work in, next to governed scale data.",
                    [["Apps", "Site and dispatch screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for stop and ticket state writes."], ["Agent Bricks", "Agents that draft route changes against governed tools."]],
                    sub=[
                        ["Dispatch & Ops Apps", "the Dispatch Console dispatchers and drivers run the day from."],
                        ["Scalehouse & Site Apps", "the Scalehouse Dashboard for inbound tons, material class and bale inventory."],
                        ["ESG & Registry Apps", "the Diversion Registry that assembles diversion and emissions evidence."],
                    ],
                    ucs=["Route Optimization", "Landfill Airspace", "Carbon & Methane"]),
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
            [uc("Route Optimization", "Collection", "sheet", "Residential and commercial routes rebalanced for miles, time and safety.",
                problem="Residential and commercial routes are planned on last year's map, so trucks run extra miles, miss time windows and burn fuel while dispatchers cannot see the day as it actually unfolds.",
                who="Collection Ops",
                how="GPS, lift and completion feeds land in Lakehouse//RT and feed routing models in Model Serving, with optimised stop order pushed to driver devices from the Dispatch Console.",
                comps=["Dispatch Console", "Lakehouse//RT", "Model Serving", "Geotab Fleet", "RouteSmart", "Delta Lake"],
                stories=[
                    ["Cleanaway champions a sustainable means to waste management", "https://www.databricks.com/customers/cleanaway"],
                    ["Fleet optimization with CARTO & Databricks", "https://www.databricks.com/blog/fleet-optimization-carto-databricks"],
                ]),
             uc("Missed Stop Prediction", "Service", "stream", "Stops at risk of miss flagged from GPS and historical patterns.",
                problem="Missed pickups surface only when the customer calls, and by then the crew has left the street, a service credit is owed and the route has to be sent back the next day.",
                who="Collection Ops",
                how="GPS traces, lift-sensor reads and service history land through Lakeflow and score a miss-risk model in Model Serving, raising exceptions on the Dispatch Console before the truck leaves the zone.",
                comps=["Dispatch Console", "Lakeflow", "Model Serving", "Lift Sensors & RFID", "Salesforce Service Cloud", "Feature Store"],
                stories=[
                    ["Cleanaway champions a sustainable means to waste management", "https://www.databricks.com/customers/cleanaway"],
                ]),
             uc("Contamination Detection", "Recycling", "iot", "Contamination events from lift sensors and MRF cameras.",
                problem="Contaminated loads are caught at the MRF or not at all, so bales are downgraded, customers keep filling bins wrong and the recycling stream loses value with no feedback to the route.",
                who="Disposal & MRF",
                how="Lift-sensor events and MRF camera streams feed vision models in Model Serving, and contamination flags are written back to the customer account and the driver's next visit via the Dispatch Console.",
                comps=["Dispatch Console", "Machinex MRF SCADA", "Model Serving", "Lift Sensors & RFID", "AI Functions", "Delta Lake"],
                stories=[
                    ["Cleanaway champions a sustainable means to waste management", "https://www.databricks.com/customers/cleanaway"],
                ]),
             uc("Landfill Airspace", "Disposal", "db", "Airspace consumption forecast against permitted capacity.",
                problem="Remaining permitted airspace is tracked in spreadsheets from occasional surveys, so the site cannot see how fast it is filling or price inbound tonnage against the capacity it has left.",
                who="Disposal & MRF",
                how="Scale tickets and survey volumes are conformed on Delta Lake under Unity Catalog and forecast against permitted capacity in the Scalehouse Dashboard, so airspace burn is visible daily.",
                comps=["Scalehouse Dashboard", "Paradigm Software", "Delta Lake", "Unity Catalog", "AI/BI", "Model Serving"]),
             uc("Dynamic Pricing", "Commercial", "market", "Container and service fees adjusted to margin and churn risk.",
                problem="Container and service fees are set once at contract and rarely revisited, so rising disposal and fuel cost quietly erodes margin and increases land as blunt across-the-board hikes.",
                who="Commercial Sales",
                how="Cost-to-serve, disposal and churn signals are conformed under Unity Catalog and scored in Model Serving, surfacing per-account price and margin guidance in the Commercial Pricing Hub.",
                comps=["Commercial Pricing Hub", "Model Serving", "Unity Catalog", "AMCS Platform", "AI/BI", "Delta Lake"]),
             uc("Fleet Maintenance", "Assets", "iot", "Predictive maintenance from telematics before breakdown on route.",
                problem="A truck that breaks down mid-route strands a full load and blows the day's schedule, yet maintenance runs on fixed mileage rather than the engine and idle data the fleet already streams.",
                who="Collection Ops",
                how="Geotab and ELD telemetry stream into Lakehouse//RT and feed remaining-life models tracked in MLflow and scored in Model Serving, so a service is booked before a breakdown lands on route.",
                comps=["Dispatch Console", "Geotab Fleet", "Motive ELD", "Lakehouse//RT", "Model Serving", "MLflow"],
                stories=[
                    ["What is Predictive Maintenance?", "https://www.databricks.com/blog/what-is-predictive-maintenance"],
                    ["Vinli: fleet optimization powered by AI", "https://www.databricks.com/customers/vinli"],
                ]),
             uc("MRF Commodity Revenue", "Recycling", "market", "Bale revenue forecast against commodity index movements.",
                problem="Bale revenue swings with volatile commodity indices, but throughput, quality and price sit in separate systems so the MRF cannot forecast revenue or decide when to sell against the market.",
                who="Disposal & MRF",
                how="MRF throughput and bale weights are conformed on Delta Lake and joined to commodity indices, with revenue forecast in the Scalehouse Dashboard and AI/BI so the site sells into strength.",
                comps=["Scalehouse Dashboard", "Machinex MRF SCADA", "Recycling Market Indices", "Delta Lake", "AI/BI", "Model Serving"],
                stories=[
                    ["Sustainability in Aluminum Production", "https://www.databricks.com/blog/sustainability-aluminum-production"],
                ]),
             uc("Customer Churn", "Sales", "custlake", "Commercial account churn scored from service quality and price.",
                problem="Commercial accounts leave after a run of missed pickups or a price rise, but service quality, billing and pricing live in separate systems so churn first shows as the cancellation notice.",
                who="Commercial Sales",
                how="Service, billing and interaction history are conformed under Unity Catalog and scored in Model Serving, with at-risk accounts surfaced in the Commercial Pricing Hub before renewal.",
                comps=["Commercial Pricing Hub", "Salesforce Service Cloud", "Model Serving", "Unity Catalog", "Feature Store", "AI/BI"]),
             uc("Municipal Franchise", "Contracts", "gavel", "Franchise fee and service level evidence for city audits.",
                problem="City franchise contracts demand tonnage, diversion and service-level evidence on schedule, and assembling it by hand from scale and route systems for each audit is slow and hard to defend.",
                who="Sustainability",
                how="Scale, route and diversion data are conformed into governed Gold products under Unity Catalog and published to city contracts over Open Sharing from the Diversion Registry.",
                comps=["Diversion Registry", "Wastebits Reporting", "Unity Catalog", "Open Sharing", "Data Products", "Delta Lake"]),
             uc("Carbon & Methane", "ESG", "chart", "Landfill gas capture and fleet emissions for sustainability reporting.",
                problem="Landfill gas capture and fleet emissions are reported from spreadsheets months late, so the team cannot show franchise partners live progress against methane and carbon commitments.",
                who="Sustainability",
                how="Landfill gas readings and fleet telemetry are conformed on Delta Lake under Unity Catalog and modelled for capture and emissions, with evidence assembled in the Diversion Registry and AI/BI.",
                comps=["Diversion Registry", "Landfill Gas Monitor", "EPA LMOP Data", "Unity Catalog", "Delta Lake", "AI/BI"],
                stories=[
                    ["How Dow Built a Carbon Footprint Ledger on Databricks", "https://www.databricks.com/blog/how-dow-built-carbon-footprint-ledger-databricks-accelerate-sustainability-scale"],
                    ["From emissions reporting to decarbonization decisions", "https://www.databricks.com/blog/emissions-reporting-decarbonization-decisions"],
                ])],
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
            "scalehouse": {"t": "Paradigm Software", "u": "https://www.paradigmsoftware.com/"},
            "landfill-gas": {"t": "Landfill gas monitoring", "u": "https://www.epa.gov/lmop"},
            "machinex": {"t": "Machinex MRF", "u": "https://www.machinexrecycling.com/"},
            "enablon": {"t": "Enablon EHS", "u": "https://www.wolterskluwer.com/en/solutions/enablon"},
            "wastebits": {"t": "Wastebits", "u": "https://www.wastebits.com/"},
            "epa-lmop": {"t": "EPA LMOP", "u": "https://www.epa.gov/lmop"},
        },
    },
}
