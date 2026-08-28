import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    app, biz, cons_rail, dashboard, data_out, fed_group, flow, genie, ing_rail,
    medallion, tile, top_band, uc,
)


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
                        tile("NCR Aloha POS", "market", "Guest checks, modifiers, voids and payment tenders from dine-in and bar.", "ncr-aloha",
                             cat="Restaurant POS",
                             what="Captures guest checks, modifiers, voids, comps and payment tenders across dine-in, bar and counter service.",
                             users="Store operations, Shift managers and Loss prevention teams.",
                             data_out=data_out(
                                 stream=flow(["semi-structured"], "hundreds of checks/sec at peak", "Continuous (POS transactions)"),
                                 batch=flow(["structured"], "1-5 GB/day", "Nightly polling extracts"))),
                        tile("Toast Restaurant POS", "partner", "Full-service and QSR transactions with online ordering integration.", "toast",
                             cat="Restaurant POS",
                             what="Cloud POS for full-service and QSR that unifies in-store checks with online and app ordering on one platform.",
                             users="Store operations, Digital ordering and Menu management teams.",
                             data_out=data_out(
                                 stream=flow(["semi-structured"], "hundreds of orders/sec at peak", "Continuous (API / webhook)"))),
                        tile("QSR Automations KDS", "stream", "Kitchen display timing, bump events and course sequencing.", "qsr-automations",
                             cat="Kitchen Display System (KDS)",
                             what="Drives kitchen display timing, bump events and course sequencing so ticket and prep times can be measured.",
                             users="Kitchen operations, Speed-of-service and Operations teams.",
                             data_out=data_out(
                                 stream=flow(["semi-structured"], "thousands of bump events/min at peak", "Continuous (kitchen events)"))),
                    ]},
                {"box": "Back Office & ERP", "ic": "erp", "tiles": [
                        tile("Restaurant365", "erp", "AP, inventory, scheduling and store P&L for multi-unit operators.", "r365",
                             cat="Restaurant Back-Office / ERP",
                             what="Restaurant-specific ERP covering accounts payable, inventory, scheduling and store-level P&L for multi-unit operators.",
                             users="Finance, Controllers and Above-store operations teams.",
                             data_out=data_out(
                                 batch=flow(["structured"], "1-8 GB/day", "Nightly close + intraday deltas"))),
                        tile("CrunchTime Inventory", "sheet", "Food counts, theoretical usage and waste tracking by store.", "crunchtime",
                             cat="Inventory & Food-Cost Management",
                             what="Tracks food counts, theoretical versus actual usage and waste by store to drive food-cost control.",
                             users="Finance, Kitchen operations and Purchasing teams.",
                             data_out=data_out(
                                 batch=flow(["structured"], "1-4 GB/day counts + usage", "Daily counts + period close"))),
                        tile("SAP Business One", "db", "Franchise billing, royalties and consolidated financial close.", "sap-b1",
                             cat="Financial / ERP System",
                             what="Handles franchise billing, royalty accruals and the consolidated financial close for the operator.",
                             users="Finance, Franchise accounting and Treasury teams.",
                             data_out=data_out(
                                 batch=flow(["structured"], "1-5 GB/day", "Nightly batch + period close"))),
                    ]},
                {"box": "Labor & Scheduling", "ic": "people", "tiles": [
                        tile("HotSchedules", "people", "Shift schedules, punches and labor compliance across locations.", "hotschedules",
                             cat="Workforce Scheduling System",
                             what="Builds shift schedules, captures punches and enforces labor-compliance rules across store locations.",
                             users="Store managers, Above-store operations and HR compliance teams.",
                             data_out=data_out(
                                 batch=flow(["structured"], "sub-GB to 2 GB/day", "Hourly punch + schedule sync"))),
                        tile("Deputy Workforce", "chart", "Time and attendance, leave and wage rules for hourly teams.", "deputy",
                             cat="Time & Attendance Platform",
                             what="Records time and attendance, leave and wage rules for hourly teams and feeds payroll and labor analytics.",
                             users="Store managers, Payroll and HR teams.",
                             data_out=data_out(
                                 batch=flow(["structured"], "sub-GB/day", "Hourly / nightly sync"))),
                        tile("Harri Talent Platform", "custlake", "Hiring, onboarding and turnover metrics by store and role.", "harri",
                             cat="HR & Talent Management",
                             what="Manages hiring, onboarding and turnover tracking by store and role for high-churn hourly workforces.",
                             users="HR, Recruiting and Store operations teams.",
                             data_out=data_out(
                                 batch=flow(["structured"], "sub-GB/day", "Daily sync"))),
                    ]},
                {"box": "Delivery & Loyalty", "ic": "partner", "tiles": [
                        tile("DoorDash Marketplace", "partner", "Third-party delivery orders, fees and customer ratings by store.", "doordash",
                             cat="Delivery Marketplace",
                             what="Third-party delivery marketplace supplying orders, commission and fee detail, refunds and customer ratings per store.",
                             users="Digital & delivery, Store operations and Finance teams.",
                             data_out=data_out(
                                 batch=flow(["structured", "semi-structured"], "1-3 GB/day orders + payouts", "Hourly orders + daily payout files"))),
                        tile("Uber Eats Merchant", "api", "Delivery channel orders, adjustments and payout statements.", "uber-eats",
                             cat="Delivery Marketplace",
                             what="Delivery channel supplying orders, adjustments and payout statements reconciled against store sales.",
                             users="Digital & delivery, Store operations and Finance teams.",
                             data_out=data_out(
                                 batch=flow(["structured", "semi-structured"], "1-3 GB/day", "Hourly orders + daily payouts"))),
                        tile("Paytronix Loyalty", "custlake", "Guest profiles, offers redeemed and visit frequency.", "paytronix",
                             cat="Loyalty & Guest Engagement",
                             what="Holds guest profiles, offer redemptions and visit frequency behind loyalty and win-back programs.",
                             users="Marketing, Loyalty and CRM teams.",
                             data_out=data_out(
                                 batch=flow(["structured"], "1-4 GB/day", "Hourly / nightly sync"),
                                 stream=flow(["semi-structured"], "tens of events/sec", "Continuous (redemption events)"))),
                    ]},
                fed_group("Franchisee P&L Mart", "Franchise unit economics left at franchisees and queried in place under Unity Catalog.",
                          cat="Franchise Financial Data Warehouse",
                          what="Franchise unit-economics marts left at franchisees and queried in place through federation rather than centralised.",
                          users="Franchise business consultants, Finance and Franchise development teams.",
                          data_out=data_out(
                              batch=flow(["structured"], "GB-scale per franchisee", "Queried on demand (federated)"))),
            ],
            "ing": ing_rail([
                tile("Weather & Events API", "globe", "Local weather and event calendars consumed inbound for demand forecasting.",
                     cat="Weather & Events Data",
                     what="Supplies local forecasts and event calendars used as demand-forecasting features for prep, ordering and staffing.",
                     users="Operations, Forecasting scientists and Store managers.",
                     data_out=data_out(
                         batch=flow(["structured", "semi-structured"], "sub-GB/day", "Hourly / daily pulls"))),
                tile("Commodity Price Feeds", "market", "Protein and produce indices normalised for menu engineering alerts.", "usda-ams",
                     cat="Commodity Price Index",
                     what="Normalises protein and produce price indices into food-cost and menu-engineering alerts.",
                     users="Finance, Purchasing and Menu strategy teams.",
                     data_out=data_out(
                         batch=flow(["structured"], "sub-GB/day", "Daily index files"))),
                tile("Health Dept Inspections", "gavel", "Municipal inspection scores parsed for franchise compliance monitoring.",
                     cat="Regulatory Inspection Data",
                     what="Parses municipal health-inspection scores and violations for franchise food-safety and compliance monitoring.",
                     users="Franchise compliance, Food safety and Operations teams.",
                     data_out=data_out(
                         batch=flow(["semi-structured"], "sub-GB/day", "Weekly / on publication"))),
            ]),
            "ppl": ppl_rail2([
                biz("Brand Leadership", "Genie One", "The CEO on comparable sales and franchise growth; the CFO on food and labor cost percent when commodity prices and hourly wages spike.", [["Genie One", "Ask what yesterday's comp sales were by banner without waiting on operations."], ["AI/BI", "Sales, labor and margin on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"comp\" means one thing across POS and ERP."]], sub=[["CEO", "comparable sales, franchise growth and the trade between new units and unit margin."], ["CFO", "prime cost, cash and food and labor exposure when commodities and wages spike."], ["Chief Brand Officer", "menu strategy, LTO cadence and the guest brand promise across banners."]], ucs=["Menu Engineering", "Demand Forecasting", "New Store Analytics"]),
                biz("Operations", "Lakehouse//RT", "Regional directors on speed of service, void rates and shift execution, watching ticket times and order accuracy against the operations plan.", [["Store Performance", "Ticket times and void pareto before the ops call."], ["Lakehouse//RT", "Kitchen bump events at service latency."], ["AI/BI", "Speed and accuracy on governed definitions."]], sub=[["VP Operations", "speed of service, order accuracy and execution against the operations plan."], ["Regional Director", "store-level void rates, ticket times and shift execution on the ground."], ["Above-Store Coach", "coaching underperforming stores on labor deployment and throughput."]], ucs=["Demand Forecasting", "Labor Optimisation", "Speed of Service"]),
                biz("Finance & Accounting", "AI/BI", "Controllers on food cost percent, cash over-short and franchise royalties, tracking prime cost against budget before period close.", [["Food Cost Dashboard", "Theoretical versus actual usage before period close."], ["AI/BI", "P&L and prime cost on certified Metric Views."], ["Genie One", "Ask which stores missed food cost budget last week."]], sub=[["Controller", "food cost percent, prime cost and cash over-short against budget."], ["FP&A", "store P&L forecasting and the variance behind every margin miss."], ["Loss Prevention", "void, comp and refund patterns by employee and shift."]], ucs=["Food Cost Control", "Shrink & Void Control", "Menu Engineering"]),
                biz("Marketing & Loyalty", "CustomerLake", "Brand teams on offers, LTO performance and guest retention, tracking redemption lift and visit frequency across the loyalty base.", [["Loyalty Campaign Hub", "Offer redemption and lift before national promos launch."], ["CustomerLake", "Guest segments without copying loyalty DB elsewhere."], ["Model Serving", "Churn models scored on visit patterns."]], sub=[["CMO", "brand campaigns, LTO performance and national promo return."], ["Loyalty Manager", "redemption lift, visit frequency and points liability across the base."], ["Digital & Delivery", "app orders, marketplace mix and third-party channel economics."]], ucs=["Guest Churn", "Delivery Channel Mix", "Menu Engineering"]),
                biz("Franchise Development", "Apps", "Franchise leadership on unit economics, compliance and new store pipeline, tracking unit-level P&L and audit scores by franchisee.", [["Franchise Scorecard", "Unit P&L and audit scores by franchisee."], ["Apps", "Compliance workflows on governed operations data."], ["Unity Catalog", "One store definition across franchise and corporate."]], sub=[["VP Franchise Development", "the new-unit pipeline and franchisee selection and growth."], ["Franchise Business Consultant", "unit economics, audit scores and compliance by franchisee."], ["Site Selection", "trade-area analysis and the pro forma behind each new store."]], ucs=["Franchise Compliance", "New Store Analytics", "Food Cost Control"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the POS, KDS, inventory and delivery-platform feeds; own the Bronze to Silver path and the pager when a store pipeline breaks.", [["Lakeflow Connect", "Managed connectors for POS, back-office and delivery sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on check and punch feeds."], ["Lakewatch", "Freshness on the comp sales and food cost tables ops reads."]], sub=[["Ingestion Engineer", "POS, KDS, inventory and delivery connectors and the Bronze landing."], ["Pipeline Owner", "the Bronze to Silver path and the pager when a store feed breaks."], ["Platform Admin", "Unity Catalog permissions and cost across store and franchise data."]], ucs=["Demand Forecasting", "Speed of Service", "Delivery Channel Mix"]),
                biz("Data Scientists", "MLflow", "Demand-forecast, labor-optimisation, menu-engineering and guest-churn models, and whether they still hold six months after deployment across stores.", [["Feature Store", "Traffic and weather features read identically in training and serving."], ["MLflow", "Every forecast and churn run tracked for audit and reproduction."], ["Model Serving", "Demand and churn models scored in the scheduling and loyalty path."]], sub=[["Forecasting Scientist", "store and daypart demand and labor models tuned to weather and events."], ["Personalisation Scientist", "guest churn and offer models scored on visit patterns."], ["MLOps Engineer", "whether a forecast still holds six months on across hundreds of stores."]], ucs=["Demand Forecasting", "Labor Optimisation", "Guest Churn", "Menu Engineering"]),
                biz("App Developers", "Apps", "Ship the store performance, food cost and franchise applications operators and finance work in, hosted next to governed store data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for schedule state and governed writes."], ["Agent Bricks", "Agents that draft a purchase order against governed tools."]], sub=[["Full-Stack Developer", "the store performance, food cost and franchise screens teams work in."], ["Platform Engineer", "Lakebase schedule state and governed writeback to stores."], ["Agent Developer", "agents that draft a purchase order against governed tools."]], ucs=["Food Cost Control", "Franchise Compliance", "Speed of Service"]),
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
            ], genie_spaces=[
                genie("Store Performance", "Ask about comp sales, ticket times and daypart performance across stores in plain language.",
                      feeds=["NCR Aloha POS", "Toast Restaurant POS", "QSR Automations KDS", "Sales, labor, margin"],
                      teams=["Operations", "VP Operations", "Regional Director"],
                      questions=[
                          "What were comp sales by store and daypart yesterday versus last year?",
                          "Which stores have the slowest ticket times this week?",
                          "Which stores missed their speed-of-service target during the lunch rush?",
                          "How do voids and comps compare across stores this period?",
                          "Which regions are trending down on order accuracy?"]),
                genie("Food Cost & Margin", "Explore theoretical-versus-actual food cost, waste and prime cost across stores.",
                      feeds=["CrunchTime Inventory", "Restaurant365", "NCR Aloha POS", "Sales, labor, margin"],
                      teams=["Finance & Accounting", "Controller", "Loss Prevention"],
                      questions=[
                          "Which stores missed food-cost budget last week and by how much?",
                          "What is the theoretical-versus-actual usage variance by item?",
                          "Where is waste highest and which items drive it?",
                          "How is prime cost tracking against budget by store?",
                          "Which employees and shifts show unusual void and comp patterns?"]),
                genie("Delivery & Loyalty", "Answer questions on delivery channel mix, marketplace economics and guest loyalty.",
                      feeds=["DoorDash Marketplace", "Uber Eats Merchant", "Paytronix Loyalty", "Conformed store, item"],
                      teams=["Marketing & Loyalty", "Loyalty Manager", "Digital & Delivery"],
                      questions=[
                          "What is net margin per delivered check by channel and store?",
                          "Which delivery platform drives the most profitable orders this month?",
                          "Which loyalty members are lapsing before their points expire?",
                          "What is redemption lift on the current offer versus baseline?",
                          "How does visit frequency differ between loyalty and non-loyalty guests?"]),
                genie("Franchise & Brand", "Ask about franchise unit economics, audit scores and new-store performance.",
                      feeds=["Franchisee P&L Mart", "Health Dept Inspections", "Restaurant365", "Sales, labor, margin"],
                      teams=["Franchise Development", "Franchise Business Consultant", "Brand Leadership"],
                      questions=[
                          "Which franchisees are below system-average unit economics?",
                          "Which units are at risk on their next field or health audit?",
                          "How are new stores ramping against their pro forma?",
                          "Which banners are driving comparable-sales growth this quarter?",
                          "Where is franchisee compliance slipping across the system?"]),
            ], dashboards=[
                dashboard("Comp Sales & Operations", "Comparable sales, speed of service and order accuracy on certified Metric Views.",
                          kpis=["Comparable sales", "Ticket time", "Order accuracy", "Void rate", "Transactions per hour"],
                          teams=["Operations", "Brand Leadership", "Regional Director"]),
                dashboard("Prime Cost & Margin", "Food cost, labor percent and prime cost against budget by store and period.",
                          kpis=["Food cost percent", "Labor percent", "Prime cost", "Waste percent", "Theoretical variance"],
                          teams=["Finance & Accounting", "Controller", "FP&A"]),
                dashboard("Delivery & Loyalty", "Channel mix, marketplace margin and loyalty engagement across the base.",
                          kpis=["Delivery channel mix", "Net margin per check", "Redemption lift", "Visit frequency", "Points liability"],
                          teams=["Marketing & Loyalty", "Digital & Delivery", "Loyalty Manager"]),
                dashboard("Franchise Scorecard", "Unit economics, audit scores and new-store ramp by franchisee.",
                          kpis=["Unit-level P&L", "Audit score", "Compliance rate", "New-store ramp", "Comparable sales"],
                          teams=["Franchise Development", "Franchise Business Consultant", "Brand Leadership"]),
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
                uc("Demand Forecasting", "Planning", "chart", "Store-level sales forecast tuned to weather, events and promos.",
                    problem="Store managers guess covers from last year and gut feel, so prep, ordering and staffing are set blind to weather, local events and promotions, and every miss lands as waste or long waits.",
                    who="Operations",
                    how="POS sales, weather and event feeds land through Lakeflow, demand features are built in Feature Store and scored in Model Serving, and the forecast surfaces by store and daypart in Store Performance.",
                    comps=["Store Performance", "Weather & Events API", "Feature Store", "Model Serving", "MLflow"],
                    stories=[
                        ["Accelerate demand planning from 4.5 hours to under 1 hour with Databricks", "https://www.databricks.com/blog/2021/01/28/how-to-accelerate-demand-planning-from-4-5-hours-to-under-1-hour-with-azure-databricks.html"],
                    ]),
                uc("Labor Optimisation", "Scheduling", "people", "Shift plans matched to forecasted traffic without overtime creep.",
                    problem="Schedules are built on manager intuition days ahead, so peaks are understaffed and slow shifts carry idle labor, and overtime creeps in wherever the plan and real traffic drift apart.",
                    who="Operations",
                    how="Forecasted traffic scored in Model Serving drives shift plans that respect wage rules, written back to HotSchedules before the week locks with roster state held in Lakebase.",
                    comps=["Store Performance", "HotSchedules", "Model Serving", "Feature Store", "Lakebase"],
                    stories=[
                        ["Dave & Buster's modernizes analytics to align labor with demand", "https://www.databricks.com/blog/dave-and-busters-successful-analytics-platform-modernization"],
                    ]),
                uc("Food Cost Control", "Margin", "sheet", "Waste and portion variance attacked with theoretical usage evidence.",
                    problem="Food cost is reconciled long after the period closes, so waste, over-portioning and yield loss are found in hindsight when the money is gone and no one can trace which store or item drove it.",
                    who="Finance & Accounting",
                    how="Counts, theoretical usage and purchases from CrunchTime Inventory conform on Delta Lake under Unity Catalog, and the Food Cost Dashboard shows theoretical-versus-actual variance by store before close.",
                    comps=["Food Cost Dashboard", "CrunchTime Inventory", "AI/BI", "Delta Lake", "Unity Catalog"],
                    stories=[
                        ["Gousto gains near real-time inventory and fulfillment visibility on Databricks", "https://www.databricks.com/customers/gousto"],
                    ]),
                uc("Menu Engineering", "Profitability", "product", "Items ranked by contribution margin and popularity not gut feel.",
                    problem="Menu decisions lean on gut feel and last quarter's bestsellers, so low-margin items stay on the board and high-margin dishes go unpromoted because item sales and true recipe cost never meet in one place.",
                    who="Brand Leadership",
                    how="POS item sales joined to recipe cost on Delta Lake rank each item by contribution margin and popularity in AI/BI, so Genie One can answer which items to feature, reprice or cut.",
                    comps=["Food Cost Dashboard", "NCR Aloha POS", "AI/BI", "Genie One", "Delta Lake"],
                    stories=[
                        ["PAR Technology builds AI-powered restaurant intelligence on Databricks", "https://www.databricks.com/customers/par-technology/genie"],
                    ]),
                uc("Speed of Service", "Operations", "stream", "Kitchen and drive-thru times improved with bump-to-ticket analytics.",
                    problem="Slow tickets and drive-thru lanes are only felt at the register, so managers coach on anecdotes while the bump and timing data that shows where seconds are lost stays trapped in the kitchen display.",
                    who="Operations",
                    how="Kitchen bump and drive-thru timing events stream from QSR Automations KDS into Lakehouse//RT, and Store Performance tracks ticket and lane times by store and daypart against the service target.",
                    comps=["Store Performance", "QSR Automations KDS", "Lakehouse//RT", "AI/BI", "Delta Lake"],
                    stories=[
                        ["Dave & Buster's improves speed of service with unified analytics", "https://www.databricks.com/blog/dave-and-busters-successful-analytics-platform-modernization"],
                    ]),
                uc("Delivery Channel Mix", "Digital", "partner", "Marketplace fees and order mix optimised for net margin per store.",
                    problem="Third-party delivery adds orders but commissions, promos and refunds bury the real margin, so operators cannot see which channel or store actually makes money on a delivered check.",
                    who="Marketing & Loyalty",
                    how="Order, fee and payout feeds from DoorDash Marketplace and Uber Eats Merchant conform on Delta Lake, and margin per channel and store is modeled so operators shift mix toward the platforms that net most.",
                    comps=["DoorDash Marketplace", "Uber Eats Merchant", "AI/BI", "Delta Lake", "Model Serving"],
                    stories=[
                        ["iFood optimizes delivery economics with Databricks and Tableau", "https://www.databricks.com/customers/ifood"],
                    ]),
                uc("Guest Churn", "Loyalty", "custlake", "Lapsed guests identified before loyalty points expire.",
                    problem="Lapsing guests are noticed only once visits have already stopped, so loyalty points expire unredeemed and win-back offers land after the guest has moved on to a competitor.",
                    who="Marketing & Loyalty",
                    how="Visit and redemption history from Paytronix Loyalty land in CustomerLake, churn features are built in Feature Store and scored in Model Serving, and win-back offers fire from the Loyalty Campaign Hub before points lapse.",
                    comps=["Loyalty Campaign Hub", "Paytronix Loyalty", "CustomerLake", "Model Serving", "Feature Store"],
                    stories=[
                        ["Kard drives customer loyalty with hyper-personalized rewards", "https://www.databricks.com/customers/kard"],
                        ["Databricks and Stitch turn data into QSR marketing performance", "https://www.databricks.com/blog/databricks-and-stitch-marketing-activation"],
                    ]),
                uc("Franchise Compliance", "Audit", "gavel", "Food safety and ops standards scored before field audits.",
                    problem="Food-safety and brand-standard gaps surface at the field audit or the health inspection, when a failing store is already a liability and there was no early signal to fix it in time.",
                    who="Franchise Development",
                    how="Inspection scores, brand-standard checks and store operations conform under Unity Catalog, and the Franchise Scorecard flags at-risk units so issues are corrected before the field audit lands.",
                    comps=["Franchise Scorecard", "Health Dept Inspections", "Restaurant365", "Unity Catalog", "AI/BI"]),
                uc("Shrink & Void Control", "Loss prevention", "gauge", "Suspicious void and comp patterns surfaced by employee and shift.",
                    problem="Voids, comps and refunds are normal until they are not, so theft and sweethearting hide in the noise and a manager cannot tell an honest correction from a pattern worth investigating.",
                    who="Finance & Accounting",
                    how="Void, comp and refund events from NCR Aloha POS conform on Delta Lake and anomaly models in Model Serving surface suspicious patterns by employee, shift and store for loss-prevention review.",
                    comps=["Store Performance", "NCR Aloha POS", "Model Serving", "AI Functions", "Delta Lake"]),
                uc("New Store Analytics", "Growth", "globe", "Ramp curves and trade-area performance scored against pro forma.",
                    problem="New units are judged on a pro forma built before opening, so a site that under-ramps looks fine for months and the trade-area and cannibalization signals that would explain it are never assembled.",
                    who="Franchise Development",
                    how="Ramp curves, trade-area traffic and comparable-store data conform on Delta Lake and models score each opening against its pro forma in the Franchise Scorecard so a slow ramp is caught early.",
                    comps=["Franchise Scorecard", "Weather & Events API", "AI/BI", "Model Serving", "Delta Lake"]),
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
