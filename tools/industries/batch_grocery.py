import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    app, biz, cons_rail, dashboard, data_out, fed_group, flow, genie, ing_rail,
    medallion, tile, top_band, uc,
)


def ppl2(business_tiles, tech_tiles):
    """Business tiles plus an explicit, industry-specific Technical group of 3."""
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_GROCERY = {
    'grocery': {
        "label": "Grocery",
        "blurb": "Grocery retail and wholesale: store operations, replenishment, fresh perimeter, loyalty and supplier collaboration.",
        "medallion": medallion(
            "Raw POS and supply",
            "POS transactions, inventory snapshots, DC shipments, planogram compliance scans and loyalty swipes, landed exactly as received so a basket or a shrink event can always be replayed.",
            "Conformed SKU, store",
            "SKUs, stores, vendors and customers resolved into single conformed entities across POS, merchandising and supply systems, with promotion flags reconciled to the item sold.",
            "Shrink, fill rate, basket",
            "Contracted products merchandising and operations run on: shrink and waste by department, on-shelf availability, basket size and loyalty penetration.",
        ),
        "rails": {
            "src": [
                {"box": "Store & POS", "ic": "market", "tiles": [
                    tile("NCR Voyix POS", "market", "Lane transactions, tenders, voids and item-level scans from store registers.", "ncr-voyix",
                         cat="Point-of-Sale (POS) System",
                         what="Captures lane transactions, tenders, voids and item-level scans across store registers, the base signal for baskets, shrink and availability.",
                         users="Store Operations, Front-End teams and Loss Prevention.",
                         data_out=data_out(
                             batch=flow(["structured"], "20-80 GB/day", "End-of-day polling"),
                             stream=flow(["semi-structured"], "2-8k scans/sec at peak", "Continuous (near real-time)"))),
                    tile("Toshiba ACE POS", "erp", "Front-end and self-checkout events with department and weight-scale integration.", "toshiba-ace",
                         cat="Point-of-Sale (POS) System",
                         what="Runs front-end and self-checkout with department and weight-scale integration, emitting checkout and scale events per lane.",
                         users="Store Operations and Front-End teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "10-40 GB/day", "End-of-day batch"),
                             stream=flow(["semi-structured"], "1-5k events/sec at peak", "Continuous checkout events"))),
                    tile("Trax Shelf Analytics", "iot", "On-shelf availability and planogram compliance from in-aisle image recognition.", "trax",
                         cat="Shelf Monitoring / Computer Vision",
                         what="Reads on-shelf availability and planogram compliance from in-aisle image recognition, flagging gaps and phantom inventory.",
                         users="Store Operations, Merchandising and Space Planning teams.",
                         data_out=data_out(
                             batch=flow(["semi-structured", "unstructured"], "GBs/day images + reads", "Multiple scans per day"))),
                ]},
                {"box": "Merchandising & Promo", "ic": "sheet", "tiles": [
                    tile("Relex Space Planning", "sheet", "Planograms, facings and space-to-sales assignments by store cluster.", "relex",
                         cat="Space & Assortment Planning System",
                         what="Builds planograms, facings and space-to-sales assignments by store cluster so range matches local sell-through.",
                         users="Space Planners, Category Managers and Merchandising teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "2-8 GB/day", "Nightly batch + plan saves"))),
                    tile("SymphonyAI IRIS", "chart", "Promotion planning, lift forecasts and vendor funding accruals.", "symphony-iris",
                         cat="Retail AI / Promotion Analytics",
                         what="Plans promotions, forecasts lift and accrues vendor funding so category teams know which deals fund the next circular.",
                         users="Pricing & Promotions, Merchandising and Category teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "1-5 GB/day", "Daily model runs"))),
                    tile("Dunnhumby Customer Data", "custlake", "Loyalty baskets, segments and propensity scores from the science partner.", "dunnhumby",
                         cat="Customer Science / Loyalty Analytics",
                         what="Supplies loyalty baskets, segments and propensity scores from the customer-science partner for personalisation and category work.",
                         users="Loyalty & Marketing and Personalisation Science teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "5-20 GB/day", "Daily / weekly feed"))),
                ]},
                {"box": "Supply & Fresh", "ic": "stream", "tiles": [
                    tile("Blue Yonder Replenishment", "stream", "Store and DC orders, forecasts and service-level exceptions.", "blue-yonder-repl",
                         cat="Replenishment & Demand Planning System",
                         what="Generates store and DC orders, forecasts and service-level exceptions, the backbone of grocery replenishment.",
                         users="Replenishment Planners, DC Operations and Supply Chain teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "5-30 GB/day", "Multiple daily order cycles"))),
                    tile("Sensitech Fresh Chain", "iot", "Temperature monitoring for dairy, meat and produce from DC to store backroom.", "sensitech",
                         cat="Cold-Chain Monitoring Platform",
                         what="Monitors temperature for dairy, meat and produce from DC to store backroom, emitting the excursion signals behind fresh quality.",
                         users="Fresh Operations, Logistics and Food Safety teams.",
                         data_out=data_out(
                             stream=flow(["semi-structured"], "thousands of sensor reads/sec", "Continuous telemetry"))),
                    tile("Invafresh Fresh Platform", "product", "Markdown, production planning and waste tracking for bakery, deli and produce.", "invafresh",
                         cat="Fresh Item Management System",
                         what="Runs markdown, production planning and waste tracking for bakery, deli and produce against the code-date clock.",
                         users="Fresh Managers, Store Operations and Merchandising teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "1-5 GB/day", "Daily + intraday markdown runs"))),
                ]},
                {"box": "E-com & Fulfillment", "ic": "partner", "tiles": [
                    tile("Instacart Marketplace", "partner", "Third-party pick, substitution and delivery events attributed to store inventory.", "instacart",
                         cat="Grocery Delivery Marketplace",
                         what="Emits third-party pick, substitution and delivery events attributed to store inventory for online basket and substitution analytics.",
                         users="Digital & E-commerce and Loyalty & Marketing teams.",
                         data_out=data_out(
                             stream=flow(["semi-structured"], "hundreds of order events/sec", "Continuous order + pick events"))),
                    tile("Ocado Smart Platform", "api", "CFC pick accuracy, route density and on-time delivery for automated fulfillment.", "ocado",
                         cat="Automated Fulfillment Platform",
                         what="Provides customer-fulfillment-centre pick accuracy, route density and on-time delivery for automated online grocery fulfillment.",
                         users="E-commerce Operations and Logistics teams.",
                         data_out=data_out(
                             batch=flow(["structured"], "GBs/day", "Hourly batch"),
                             stream=flow(["semi-structured"], "hundreds of events/sec", "Continuous fulfillment events"))),
                    tile("Web & App Clickstream", "observ", "Digital basket builds, search and coupon clips joined to in-store loyalty ID.",
                         cat="Digital Clickstream Source",
                         what="Captures digital basket builds, search and coupon clips joined to the in-store loyalty ID to link online behaviour to the household.",
                         users="Digital & E-commerce, Loyalty & Marketing and Analytics teams.",
                         data_out=data_out(
                             stream=flow(["semi-structured"], "2-10k events/sec at peak", "Continuous clickstream"))),
                ]},
                fed_group(
                    "Franchisee POS",
                    "Licensed store sales and inventory left at franchise operators and queried in place under Unity Catalog.",
                    cat="Licensed Store Data Source",
                    what="Licensed-store sales and inventory left at franchise operators and queried in place through federation instead of nightly flat-file collection.",
                    users="Franchise Operations, Merchandising and Finance analysts.",
                    data_out=data_out(
                        batch=flow(["structured"], "10s-100s GB (federated)", "Queried on demand (federated)")),
                ),
            ],
            "ing": ing_rail([
                tile("GS1 GDSN Product Data", "api", "Synchronised item attributes and packaging hierarchies consumed inbound for master data.", "gs1-gdsn",
                     cat="Product Data Synchronisation Network",
                     what="Supplies synchronised item attributes and packaging hierarchies consumed inbound to keep master data aligned with suppliers.",
                     users="Master Data, Merchandising and Category teams.",
                     data_out=data_out(
                         batch=flow(["structured", "semi-structured"], "GBs/day attribute updates", "Daily / on-change sync"))),
                tile("NielsenIQ Store Read", "market", "Syndicated store-level performance for competitive benchmarking.", "nielseniq",
                     cat="Syndicated Market Data Provider",
                     what="Provides syndicated store-level performance so category teams can benchmark against the competitive market.",
                     users="Category Managers, Merchandising and Insights teams.",
                     data_out=data_out(
                         batch=flow(["structured"], "1-5 GB/week", "Weekly / monthly syndicated feed"))),
                tile("Weather & Local Events", "globe", "Forecast and event calendars for demand shaping on perishable categories.",
                     cat="External Signal / Weather Feed",
                     what="Attaches forecast and event calendars as exogenous signals for demand shaping on perishable categories.",
                     users="Demand Science, Replenishment and Store Operations teams.",
                     data_out=data_out(
                         batch=flow(["structured"], "MBs-GBs/day", "Daily forecast refresh"))),
            ]),
            "ppl": ppl2([
                biz("CEO & COO", "Genie One", "The CEO on comparable-store sales and market share; the COO on shrink, labor productivity and on-shelf availability through the peak trading weeks.",
                    [["Genie One", "Ask what comp sales were yesterday by banner without waiting on retail analytics."], ["AI/BI", "Sales, shrink and availability on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"comp\" means one thing across banners."]],
                    sub=[["CEO", "comparable-store sales, market share and the margin behind the banner's growth."], ["COO", "shrink, labor productivity and on-shelf availability through the peak trading weeks."], ["CFO", "gross margin, waste as a cost line and the cash tied up in store inventory."]],
                    ucs=["Shrink Attribution", "On-Shelf Availability", "Demand Forecasting"]),
                biz("Merchandising", "Model Serving", "Category managers on assortment localisation, price and the promotion lift that decides which vendor deals fund the next circular.",
                    [["Promo Planning Workbench", "Lift scenarios before vendor deals lock."], ["Model Serving", "Demand models scored per SKU-store."], ["AI/BI", "Category performance on governed definitions."]],
                    sub=[["Category Manager", "assortment, price and the vendor deals that fund the next circular."], ["Space Planner", "planograms and facings that match space to local sell-through."], ["Pricing & Promotions", "everyday price, markdown ladders and promotion lift by segment."]],
                    ucs=["Promotion Optimisation", "Assortment Localisation", "Demand Forecasting"]),
                biz("Store Operations", "Lakehouse//RT", "District managers on labor schedules, on-shelf gaps and fresh-department waste, timing markdowns before the perishable code date closes.",
                    [["Fresh Markdown Console", "Perishable markdown timing by sell-through curve."], ["Lakehouse//RT", "Live out-of-stock signals at store-hour granularity."], ["AI/BI", "Shrink and labor productivity the field reads."]],
                    sub=[["District Manager", "labor cost, on-shelf gaps and store execution across the district."], ["Fresh Manager", "bakery, deli and produce waste against the code-date clock."], ["Front-End Manager", "checkout throughput, scan accuracy and register shrink at the lane."]],
                    ucs=["Fresh Waste Reduction", "On-Shelf Availability", "Labor Scheduling", "Shrink Attribution"]),
                biz("Supply Chain", "AI/BI", "Replenishment planners on forecast bias, store and DC fill rate and days of supply against warehouse capacity constraints.",
                    [["Replenishment Optimiser", "Order proposals tested against service targets."], ["AI/BI", "Fill rate and days of supply on certified Metric Views."], ["Unity Catalog", "One definition of inventory across POS and WMS."]],
                    sub=[["Replenishment Planner", "forecast bias, store and DC fill rate and days of supply."], ["DC Operations", "warehouse capacity, throughput and outbound service levels."], ["Vendor Manager", "supplier fill, lead time and joint business planning."]],
                    ucs=["Demand Forecasting", "Vendor Collaboration", "Fresh Waste Reduction"]),
                biz("Loyalty & Marketing", "CustomerLake", "Personalised offers, fuel rewards and digital-coupon redemption scored per household to lift basket size and loyalty penetration.",
                    [["Loyalty Offer Engine", "Offers scored per household from basket history."], ["CustomerLake", "Segments without copying Dunnhumby exports elsewhere."], ["Genie One", "Ask which segments responded to last week's digital coupon."]],
                    sub=[["Loyalty Lead", "household penetration, offer response and fuel-reward redemption."], ["Personalisation Science", "propensity models and the segments behind each offer."], ["Digital & E-commerce", "online basket size, coupon clips and substitution acceptance."]],
                    ucs=["Loyalty Personalisation", "E-commerce Substitution", "Promotion Optimisation"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the POS, merchandising and replenishment feeds; own the Bronze to Silver path and the pager when a store feed breaks.",
                    [["Lakeflow Connect", "Managed connectors for POS, merchandising and supply sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on POS and inventory feeds."], ["Lakewatch", "Freshness on the tables merchandising and the field read every morning."]],
                    sub=[["Ingestion Engineering", "POS, merchandising and replenishment feeds landing on time."], ["Platform Engineering", "the Bronze-to-Silver path and the pager when a store feed breaks."], ["Data Quality", "expectations and freshness on POS and inventory tables."]],
                    ucs=["Demand Forecasting", "On-Shelf Availability", "Fresh Waste Reduction"]),
                biz("Data Scientists", "MLflow", "Demand, fresh-waste and loyalty-offer models, and whether they still hold a season after deployment.",
                    [["Feature Store", "SKU-store features defined once for training and serving."], ["MLflow", "Every demand and offer run tracked for audit and reproduction."], ["Model Serving", "Forecast and personalisation models scored per SKU-store."]],
                    sub=[["Demand Science", "SKU-store forecasts across weather, promo and local events."], ["Fresh & Waste Modelling", "markdown and production models that cut spoilage."], ["Personalisation Science", "household offer and substitution models that hold a season."]],
                    ucs=["Demand Forecasting", "Fresh Waste Reduction", "Loyalty Personalisation"]),
                biz("App Developers", "Apps", "Ship the replenishment, fresh-markdown and loyalty applications stores work in, hosted next to governed data.",
                    [["Apps", "Store and markdown screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for order and markdown writes."], ["Agent Bricks", "Agents that draft an order proposal or markdown against governed tools."]],
                    sub=[["Store Apps", "replenishment and markdown screens store teams work in."], ["Loyalty Apps", "the offer and coupon surfaces households see."], ["Platform & Agents", "governed writes and agents drafting orders and markdowns."]],
                    ucs=["Fresh Waste Reduction", "Loyalty Personalisation", "Labor Scheduling"]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and store alerts in the channel operations already works in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Store Writeback", "ic": "opdb", "tiles": [
                    tile("Replenishment Orders", "stream", "System-generated store orders written back into replenishment after planner review.", "blue-yonder-repl"),
                    tile("Fresh Markdown Prices", "market", "Dynamic markdowns pushed to POS labels for approaching sell-by inventory.", "invafresh"),
                    tile("Associate Task Mobile", "apps", "Gap scans, facing tasks and temperature checks pushed to handheld devices.")
                ]},
                {"box": "Supplier & Partners", "ic": "partner", "tiles": [
                    tile("Vendor VMI Portal", "share", "Inventory and forecast positions shared with key CPG suppliers over Delta Sharing."),
                    tile("Marketplace Pick Partners", "partner", "Substitution and fill-rate metrics exchanged with delivery marketplaces.", "instacart"),
                    tile("Franchise Reporting", "globe", "Licensed store KPIs aggregated without nightly flat-file collection.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Weights & Measures", "gavel", "Scale calibration and packaged goods compliance records from governed store audits."),
                    tile("Vendor Funding Audit", "share", "Promotion accruals and scan-based trade reconciliations filed from Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over OpenSharing."),
                    tile("Sharing Recipients", "share", "CPG vendors, franchisees and analysts reading live tables with no copy and no egress duplication.")
                ]},
            ], genie_spaces=[
                genie("Sales & Shrink", "Ask about comparable sales, shrink and margin by department in plain language.",
                      feeds=["NCR Voyix POS", "Toshiba ACE POS", "Shrink, fill rate, basket"],
                      teams=["CEO & COO", "Store Operations", "Merchandising"],
                      questions=[
                          "What were comparable sales yesterday by banner and department?",
                          "What is shrink and waste by department this period?",
                          "Which stores show the worst register and scan exceptions?",
                          "How is basket size trending versus last year?",
                          "Where is margin leaking against the plan by category?"]),
                genie("Availability & Fresh", "Explore on-shelf availability and fresh waste across stores and departments.",
                      feeds=["Trax Shelf Analytics", "Invafresh Fresh Platform", "Blue Yonder Replenishment", "Conformed SKU, store"],
                      teams=["Store Operations", "Supply Chain", "Merchandising"],
                      questions=[
                          "What is on-shelf availability by store and category right now?",
                          "Which fresh departments are driving the most waste?",
                          "Where are out-of-stocks hiding behind phantom inventory?",
                          "Which SKUs need a markdown before the code date closes?",
                          "What is store and DC fill rate this week?"]),
                genie("Replenishment & Supply", "Answer forecast, fill rate and days-of-supply questions across the network.",
                      feeds=["Blue Yonder Replenishment", "NielsenIQ Store Read", "Franchisee POS"],
                      teams=["Supply Chain", "Merchandising", "CEO & COO"],
                      questions=[
                          "Where is forecast bias worst by SKU and store?",
                          "What is days of supply by category and DC?",
                          "Which vendors are missing fill and lead-time targets?",
                          "Where is DC capacity constraining replenishment?",
                          "Which franchise stores diverge most from the banner?"]),
                genie("Loyalty & Offers", "Ask about household penetration, offer response and substitution across channels.",
                      feeds=["Dunnhumby Customer Data", "Instacart Marketplace", "Web & App Clickstream"],
                      teams=["Loyalty & Marketing", "Merchandising", "Store Operations"],
                      questions=[
                          "What is loyalty penetration and offer response by segment?",
                          "Which segments responded to last week's digital coupon?",
                          "What is online basket size versus in-store by household?",
                          "Which substitutions are customers rejecting most?",
                          "Which households are cross-sell candidates for fresh?"]),
            ], dashboards=[
                dashboard("Sales, Shrink & Margin", "Comparable sales, shrink, waste and margin by department on certified Metric Views.",
                          kpis=["Comparable sales", "Shrink rate", "Waste cost", "Basket size", "Gross margin"],
                          teams=["CEO & COO", "Store Operations", "Merchandising"]),
                dashboard("Availability & Fresh", "On-shelf availability, fresh waste and markdown recovery across stores.",
                          kpis=["On-shelf availability", "Fresh waste", "Markdown recovery", "Out-of-stock rate", "Code-date compliance"],
                          teams=["Store Operations", "Supply Chain", "Merchandising"]),
                dashboard("Replenishment & Fill", "Forecast accuracy, fill rate and days of supply across stores and DCs.",
                          kpis=["Forecast bias", "Store fill rate", "DC fill rate", "Days of supply", "Vendor OTIF"],
                          teams=["Supply Chain", "Merchandising", "CEO & COO"]),
                dashboard("Loyalty & Personalisation", "Household penetration, offer response and online basket across channels.",
                          kpis=["Loyalty penetration", "Offer response rate", "Online basket size", "Substitution acceptance", "Fuel reward redemption"],
                          teams=["Loyalty & Marketing", "Merchandising", "Store Operations"]),
            ]),
        },
        "top": top_band(
            [
                app("Replenishment Optimiser", "Store orders", "stream", "SKU-store order proposals scored against service level, capacity and spoilage risk before the cut-off."),
                app("Fresh Markdown Console", "Perishable waste", "gauge", "Markdown timing and depth optimised from sell-through curves and hours-to-code by department."),
                app("Promo Planning Workbench", "Vendor deals", "market", "Lift forecasts and funding accruals reconciled before circular and digital ads lock."),
                app("Loyalty Offer Engine", "Personalisation", "custlake", "Household offers scored from basket history and channel preference on governed segments."),
            ],
            [
                uc("Demand Forecasting", "Replenishment", "sheet", "SKU-store forecasts that blend loyalty baskets, weather and local events for perishables and center store.",
                   problem="Store orders lean on last year and a planner's gut, so weather, promotions and local-event swings are missed and the same SKU is short in one store and overstocked in the next.",
                   who="Supply Chain",
                   how="POS, inventory and weather feeds land through Lakeflow, are conformed on Delta Lake, and SKU-store demand is scored in Model Serving to drive proposals in the Replenishment Optimiser.",
                   comps=["Replenishment Optimiser", "Model Serving", "Feature Store", "Weather & Local Events", "Blue Yonder Replenishment", "AI/BI"],
                   stories=[
                       ["Albert Heijn reduces waste and transport costs with data insights", "https://www.databricks.com/customers/albert-heijn"],
                       ["Ahold Delhaize builds a self-service data platform for 60M weekly customers", "https://www.databricks.com/customers/ahold-delhaize"],
                   ]),
                uc("Fresh Waste Reduction", "Shrink", "gauge", "Markdown and production planning that cuts spoilage without sacrificing on-shelf availability.",
                   problem="Perishables are marked down too late or too deep, so bakery, deli and produce spoil in the backroom or lose margin to blanket discounts, with the code-date clock tracked on clipboards.",
                   who="Store Operations",
                   how="Sell-through, production and temperature feeds are conformed on Delta Lake and scored in Model Serving, so the Fresh Markdown Console times each markdown against hours-to-code by department.",
                   comps=["Fresh Markdown Console", "Invafresh Fresh Platform", "Model Serving", "Lakehouse//RT", "Delta Lake"],
                   stories=[
                       ["Albert Heijn cuts food waste and transport costs with data insights", "https://www.databricks.com/customers/albert-heijn"],
                       ["How Jumbo transformed the grocery shopping experience with data and AI", "https://www.databricks.com/blog/2022/06/07/jumbo-transforms-how-they-delight-customers-with-data-driven-personalized-experiences.html"],
                   ]),
                uc("On-Shelf Availability", "Operations", "iot", "Gaps detected from POS voids, inventory and shelf vision before customers leave empty-handed.",
                   problem="A shelf gap is found only when a customer leaves empty-handed, because POS voids, backroom stock and shelf scans live in separate systems and phantom inventory hides the real out-of-stock.",
                   who="Store Operations",
                   how="POS, inventory and shelf-vision signals stream into Lakehouse//RT and are scored against expected sell-down, so store teams get out-of-stock alerts at shelf level before the customer notices.",
                   comps=["Lakehouse//RT", "Trax Shelf Analytics", "NCR Voyix POS", "AI/BI", "Model Serving"],
                   stories=[
                       ["How Jumbo transformed the grocery shopping experience with data and AI", "https://www.databricks.com/blog/2022/06/07/jumbo-transforms-how-they-delight-customers-with-data-driven-personalized-experiences.html"],
                   ]),
                uc("Promotion Optimisation", "Merchandising", "market", "Which deals drove incremental units versus subsidised baseline sales.",
                   problem="Deals are judged on total units sold, so subsidised baseline sales look like wins, true incremental lift stays unknown, and the next vendor deal is negotiated on last quarter's noise.",
                   who="Merchandising",
                   how="Basket and promotion data are conformed on Delta Lake and lift is modelled in Model Serving, so the Promo Planning Workbench reconciles incremental units against funding before a circular locks.",
                   comps=["Promo Planning Workbench", "SymphonyAI IRIS", "Model Serving", "AI/BI", "Delta Lake"],
                   stories=[
                       ["84.51° powers Kroger price, promotions and loyalty with Databricks", "https://www.databricks.com/customers/8451"],
                       ["Ahold Delhaize analyses promotions and sales across customer segments", "https://www.databricks.com/customers/ahold-delhaize"],
                   ]),
                uc("Assortment Localisation", "Space", "sheet", "Cluster-specific assortments scored on velocity, margin and local demographic fit.",
                   problem="One national planogram ignores that a store's shoppers differ block to block, so slow SKUs hold shelf space local demand never wanted and the range that would sell never makes the set.",
                   who="Merchandising",
                   how="Sales, demographic and space data are conformed under Unity Catalog and stores are clustered in Model Serving, so localised ranges are scored on velocity, margin and local fit and read in AI/BI.",
                   comps=["Relex Space Planning", "Model Serving", "AI/BI", "Unity Catalog", "NielsenIQ Store Read"],
                   stories=[
                       ["John Keells clusters stores to localise supermarket assortments", "https://www.databricks.com/customers/john-keells-holdings"],
                       ["How Jumbo transformed the grocery shopping experience with data and AI", "https://www.databricks.com/blog/2022/06/07/jumbo-transforms-how-they-delight-customers-with-data-driven-personalized-experiences.html"],
                   ]),
                uc("Labor Scheduling", "Store ops", "people", "Shift plans aligned to forecast traffic and fresh production workloads.",
                   problem="Shift plans are built on a fixed template, so registers are overstaffed on a slow morning and the fresh counter is short when a forecast peak and a production run land at the same hour.",
                   who="Store Operations",
                   how="Forecast traffic and fresh-production workload are scored in Model Serving on conformed Delta Lake data, so shift plans are built to demand and published to store screens on Apps.",
                   comps=["Model Serving", "AI/BI", "Lakehouse//RT", "Apps", "Delta Lake"]),
                uc("E-commerce Substitution", "Digital", "partner", "Pick accuracy and substitution rules tuned from historical customer acceptance.",
                   problem="When a picked item is out, the substitution is a guess, so shoppers get a swap they reject, refunds climb and the store loses the basket and the trust behind the next online order.",
                   who="Loyalty & Marketing",
                   how="Pick, substitution and acceptance history are engineered in Feature Store and scored with Model Serving and AI Functions, so substitution rules are tuned to what each household will actually accept.",
                   comps=["Instacart Marketplace", "Ocado Smart Platform", "Model Serving", "Feature Store", "AI Functions"]),
                uc("Loyalty Personalisation", "CRM", "custlake", "Offers and fuel rewards targeted per household without batch list exports.",
                   problem="Offers and fuel rewards go out as batch list pulls that are stale on arrival, so households get coupons for items they never buy and the partner's segments never reach the live channel.",
                   who="Loyalty & Marketing",
                   how="Basket history and segments land in CustomerLake and offers are scored per household in Model Serving, so the Loyalty Offer Engine targets each household without exporting lists to another tool.",
                   comps=["Loyalty Offer Engine", "CustomerLake", "Dunnhumby Customer Data", "Model Serving", "Genie One"],
                   stories=[
                       ["84.51° improves customer loyalty for Kroger shoppers with Databricks", "https://www.databricks.com/customers/8451"],
                       ["Ahold Delhaize drives personalization for 60M weekly customers", "https://www.databricks.com/customers/ahold-delhaize"],
                   ]),
                uc("Vendor Collaboration", "CPG", "share", "Joint business planning on shared forecast and inventory positions.",
                   problem="Joint business planning runs on emailed spreadsheets, so grocer and CPG supplier argue over whose forecast and inventory numbers are right instead of planning the promotion or the fill.",
                   who="Supply Chain",
                   how="Conformed forecast and inventory positions are published as governed Data Products and shared to suppliers over OpenSharing, so both sides plan against one live set of numbers with no file exchange.",
                   comps=["OpenSharing", "Data Products", "Delta Lake", "Unity Catalog", "Blue Yonder Replenishment"]),
                uc("Shrink Attribution", "Loss prevention", "chart", "Theft, spoilage and scanning errors separated by department and store pattern.",
                   problem="Shrink shows up as one lump on the P&L, so theft, spoilage and scan errors are impossible to separate and the store never knows which lever, security, process or training, actually moves it.",
                   who="CEO & COO",
                   how="POS, inventory and audit data are conformed on Delta Lake under Unity Catalog and scored in Model Serving, so shrink is split by cause and department and read by store and pattern in AI/BI.",
                   comps=["AI/BI", "Model Serving", "NCR Voyix POS", "Delta Lake", "Unity Catalog"]),
            ],
        ),
        "sources": {
            "ncr-voyix": {"t": "NCR Voyix retail platform", "u": "https://www.ncr.com/retail"},
            "toshiba-ace": {"t": "Toshiba Global Commerce ACE", "u": "https://www.toshibacommerce.com/"},
            "trax": {"t": "Trax retail shelf analytics", "u": "https://www.traxretail.com/"},
            "relex": {"t": "Relex space planning", "u": "https://www.relexsolutions.com/solutions/"},
            "symphony-iris": {"t": "SymphonyAI IRIS promotion planning", "u": "https://www.symphonyai.com/retail/"},
            "dunnhumby": {"t": "Dunnhumby customer data science", "u": "https://www.dunnhumby.com/"},
            "blue-yonder-repl": {"t": "Blue Yonder demand planning", "u": "https://blueyonder.com/solutions"},
            "invafresh": {"t": "Invafresh fresh food retail", "u": "https://invafresh.com/"},
            "sensitech": {"t": "Sensitech cold-chain monitoring", "u": "https://www.sensitech.com/en/solutions/"},
            "nielseniq": {"t": "NielsenIQ retail measurement", "u": "https://nielseniq.com/global/en/solutions/"},
            "instacart": {"t": "Instacart marketplace", "u": "https://www.instacart.com/company/business"},
            "ocado": {"t": "Ocado Smart Platform", "u": "https://ocadointelligentautomation.com/"},
            "gs1-gdsn": {"t": "GS1 Global Data Synchronisation Network", "u": "https://www.gs1.org/services/gdsn"}
        },
    },
}
