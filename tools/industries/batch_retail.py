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


INDUSTRIES_BATCH_RETAIL = {
    'retail': {
        "label": "Retail",
        "blurb": "Omnichannel retail: merchandising, inventory and allocation, store operations and loyalty across banners, e-commerce and marketplaces.",
        "medallion": medallion(
            "Raw sales and stock",
            "POS transactions, e-commerce orders, inventory snapshots, markdown events and loyalty interactions, landed exactly as received so a basket or a stock position can always be replayed as it stood.",
            "Conformed SKU, store",
            "SKUs, stores, customers and channels resolved into single conformed entities across ERP, commerce and WMS, with returns reconciled and omnichannel orders stitched to one fulfillment record.",
            "Comp, margin, in-stock",
            "Contracted products merchandising and finance run on: comparable sales, gross margin after markdowns, in-stock rate and inventory turns.",
        ),
        "rails": {
            "src": [
                {"box": "ERP & Merchandising", "ic": "erp", "tiles": [
                        tile("SAP S/4HANA Retail", "erp", "Item masters, pricing, allocation and financial close for multi-banner retailers.", "sap-retail"),
                        tile("Oracle Retail Merch", "sheet", "Assortment planning, size profiles and PO lifecycle.", "oracle-retail"),
                        tile("Blue Yonder WMS", "stream", "Warehouse execution, pick paths and store replenishment.", "blue-yonder-wms"),
                    ]},
                {"box": "Commerce & POS", "ic": "market", "tiles": [
                        tile("Salesforce Commerce", "partner", "Omnichannel carts, promotions and clienteling across web and store.", "sf-commerce"),
                        tile("Shopify Plus", "api", "DTC orders, returns and marketplace connectors for owned brands.", "shopify"),
                        tile("NCR Voyix POS", "market", "Store transactions, endless aisle and associate workflows.", "ncr-voyix"),
                    ]},
                {"box": "Inventory & Supply", "ic": "product", "tiles": [
                        tile("Manhattan Active Omni", "stream", "Order orchestration, ship-from-store and BOPIS fulfillment.", "manhattan-omni"),
                        tile("E2open Supply Planning", "globe", "Vendor OTIF, inbound containers and allocation constraints.", "e2open"),
                        tile("SymphonyAI IRIS", "chart", "Promotion planning, markdown optimization and demand sensing.", "symphony-iris"),
                    ]},
                {"box": "Customer & Loyalty", "ic": "custlake", "tiles": [
                        tile("Salesforce Loyalty", "custlake", "Points, tiers and offer redemptions across channels.", "sf-loyalty"),
                        tile("Adobe Experience Plat", "partner", "Web behaviour, segments and consent for personalisation.", "adobe-aep"),
                        tile("Medallia Experience", "observ", "Store and digital survey scores tied to visit and order.", "medallia"),
                    ]},
                fed_group("Wholesale Partner Mart", "Department store sell-in marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("NielsenIQ POS", "market", "Syndicated sell-through consumed inbound for category benchmarking.", "nielseniq"),
                tile("Google Merchant Center", "api", "Product feed performance and local inventory ads parsed on ingest.", "google-merchant"),
                tile("Weather & Local Events", "globe", "Forecast feeds attached to stores for short-term demand models."),
            ]),
            "ppl": ppl_rail2([
                biz("Merchant Leadership", "Genie One", "The CEO on comparable sales and market share; the CFO on gross margin and inventory ownership when a season turns and markdowns start to bite.", [["Genie One", "Ask what comp sales were yesterday by banner without waiting on retail analytics."], ["AI/BI", "Sales, margin and in-stock on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"comp\" means one thing across channels."]],
                    sub=[
                        ["Chief Merchant / CEO", "comparable sales, market share and the health of the assortment across banners."],
                        ["CFO & Finance", "gross margin after markdowns and the cash tied up in inventory."],
                        ["Chief Marketing Officer", "promotion effectiveness, loyalty growth and customer acquisition cost."],
                    ],
                    ucs=["Promotion ROI", "Markdown Optimisation", "Demand Forecasting"]),
                biz("Merchandising", "AI/BI", "Buyers on assortment, pricing and markdown cadence by category, tracking sell-through and weeks of supply against the merchandise plan.", [["Allocation Optimizer", "Size curves and door profiles before allocation locks."], ["AI/BI", "Sell-through and WOS on governed POS."], ["Genie One", "Ask which SKUs are overstocked before markdown season."]],
                    sub=[
                        ["Buyers", "assortment breadth, sell-through and the open-to-buy against the merchandise plan."],
                        ["Pricing & Markdown", "price ladders, markdown cadence and margin recovery on aged stock."],
                        ["Category Managers", "space, range and vendor performance within the category."],
                    ],
                    ucs=["Markdown Optimisation", "Allocation Optimisation", "Promotion ROI"]),
                biz("Planning & Allocation", "Model Serving", "Planners on forecast accuracy, receipts and replenishment at risk, watching in-stock rate and inventory turns across the store network.", [["Demand Planning Hub", "Consensus forecast before buy meetings."], ["Model Serving", "Demand models scored in the allocation path."], ["Unity Catalog", "One SKU definition across ERP and commerce."]],
                    sub=[
                        ["Demand Planners", "consensus forecast accuracy and weeks of supply by SKU and door."],
                        ["Allocators", "size curves, door profiles and receipts flowing to the right stores."],
                        ["Supply Planners", "vendor fill, inbound flow and replenishment at risk."],
                    ],
                    ucs=["Demand Forecasting", "Allocation Optimisation", "Supplier OTIF", "In-Stock Optimisation"]),
                biz("Store Operations", "Lakehouse//RT", "Field leaders on labor, conversion and in-stock during peak weeks, watching sales per labor hour and how fast a stockout spreads across doors.", [["Store Command Centre", "Traffic, conversion and labor against plan."], ["Lakehouse//RT", "Inventory positions at the latency a stockout spreads at."], ["Apps", "Associate tasking on governed store data."]],
                    sub=[
                        ["Regional & District Managers", "sales per labor hour, conversion and in-stock across their doors."],
                        ["Store Managers", "labor, tasking and shelf availability during peak weeks."],
                        ["Loss Prevention", "shrink, register exceptions and process compliance on the floor."],
                    ],
                    ucs=["In-Stock Optimisation", "Omnichannel Fulfillment", "Shrink Analytics", "Clienteling"]),
                biz("Digital & CRM", "CustomerLake", "E-commerce and loyalty on traffic, conversion and retention, tracking customer lifetime value and churn across web, app and store.", [["Personalisation Studio", "Offers ranked on governed segments."], ["CustomerLake", "Household profiles without copying CDP elsewhere."], ["Model Serving", "Churn models in the marketing path."]],
                    sub=[
                        ["E-commerce", "site conversion, basket size and the fulfillment promise across channels."],
                        ["Loyalty & CRM", "retention, lifetime value and offer relevance by segment."],
                        ["Personalisation", "recommendation lift and the models ranking offers on-site."],
                    ],
                    ucs=["Personalisation", "Clienteling", "Promotion ROI"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the ERP item, commerce, WMS and loyalty feeds; own the Bronze to Silver path and the pager when a retail pipeline breaks.", [["Lakeflow Connect", "Managed connectors for retail ERP, commerce and WMS sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on POS and inventory feeds."], ["Lakewatch", "Freshness on the comp sales and in-stock tables merchants read."]],
                    sub=[
                        ["Platform Engineering", "the ERP, commerce, WMS and loyalty pipelines and the Bronze-to-Silver contracts."],
                        ["Streaming & Ingestion", "POS and inventory events landing at the latency stores read them."],
                        ["Data Quality & SRE", "freshness and expectations on the comp-sales and in-stock tables."],
                    ],
                    ucs=["Demand Forecasting", "Omnichannel Fulfillment", "In-Stock Optimisation"]),
                biz("Data Scientists", "MLflow", "Demand-forecast, markdown, allocation and personalisation models, and whether they still hold six months after deployment across banners and channels.", [["Feature Store", "POS and web features read identically in training and serving."], ["MLflow", "Every forecast and markdown run tracked for audit and reproduction."], ["Model Serving", "Demand and offer models scored in the allocation and marketing path."]],
                    sub=[
                        ["Forecasting & Optimization", "demand, markdown and allocation models and whether they still hold across banners."],
                        ["Personalisation Science", "recommendation and next-best-offer models on governed profiles."],
                        ["MLOps", "features read the same in training and serving, and every run reproducible."],
                    ],
                    ucs=["Demand Forecasting", "Markdown Optimisation", "Personalisation", "Allocation Optimisation"]),
                biz("App Developers", "Apps", "Ship the store command, demand planning and personalisation applications merchants and field teams work in, hosted next to governed retail data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for tasking state and governed writes."], ["Agent Bricks", "Agents that draft a replenishment order against governed tools."]],
                    sub=[
                        ["App Engineering", "the store command, planning and personalisation screens merchants work in."],
                        ["Backend & APIs", "governed writes and serverless Postgres state behind operational apps."],
                        ["Agent Builders", "agents that draft a replenishment order against governed tools."],
                    ],
                    ucs=["Omnichannel Fulfillment", "Clienteling", "Personalisation"]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                        tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                        tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and peak-week updates in the channel stores work in (Beta)."),
                        tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code."),
                    ]},
                {"box": "Store & ERP Writeback", "ic": "opdb", "tiles": [
                        tile("Allocation Releases", "stream", "Door-level allocations pushed to WMS before pick waves.", "blue-yonder-wms"),
                        tile("Price & Markdown", "market", "Markdown recommendations written to POS and commerce.", "sf-commerce"),
                        tile("Replenishment Orders", "erp", "Store replenishment POs raised from governed min-max rules.", "sap-retail"),
                    ]},
                {"box": "Marketplace Partners", "ic": "partner", "tiles": [
                        tile("Marketplace Inventory API", "api", "Available-to-promise synced to marketplaces from governed stock.", "shopify"),
                        tile("Wholesale EDI", "share", "850/856 orders and ASNs to department store partners over governed products."),
                        tile("3PL Fulfillment Feed", "globe", "Outbound shipment status from 3PLs without nightly spreadsheet chases.", "manhattan-omni"),
                    ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                        tile("Product Safety Recall", "gavel", "Lot and store distribution lists produced from governed inventory lineage."),
                        tile("ESG Product Passport", "share", "Sourcing and sustainability attributes filed from contracted Gold products."),
                    ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                        tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                        tile("Sharing Recipients", "share", "Suppliers, marketplaces and auditors reading live tables with no copy."),
                    ]},
            ]),
        },
        "top": top_band(
            [
                app("Store Command Centre", "Comp sales live", "gauge", "Traffic, conversion and labor against plan on Databricks Apps over Lakebase."),
                app("Demand Planning Hub", "Forecast consensus", "sheet", "Statistical and merchant forecasts reconciled before buy meetings lock."),
                app("Allocation Optimizer", "Door profiles", "product", "Size curves and door allocation against demand and constraints."),
                app("Personalisation Studio", "Offer targeting", "custlake", "Segments and offers ranked on governed loyalty and web behaviour."),
            ],
            [
                uc("Demand Forecasting", "Planning", "chart", "SKU-store forecasts updated from POS, web and local signals.",
                    problem="Category-level forecasts built on last year's averages miss local demand, so some doors overstock while others stock out before planners can react to what is actually selling.",
                    who="Planning & Allocation",
                    how="POS, e-commerce and local signals like weather land through Lakeflow, features are engineered in Feature Store, and SKU-store models scored in Model Serving feed the Demand Planning Hub.",
                    comps=["Demand Planning Hub", "Lakeflow", "Feature Store", "Model Serving", "Weather & Local Events"],
                    stories=[
                        ["ABFRL scales demand forecasting and allocation on Databricks", "https://www.databricks.com/customers/aditya-birla-fashion-and-retail-ltd"],
                        ["Walgreens forecasts inventory across nearly 9,000 pharmacies", "https://www.databricks.com/customers/walgreens"],
                    ]),
                uc("Markdown Optimisation", "Margin", "market", "Markdown timing and depth maximising margin recovery not calendar rules.",
                    problem="Markdowns follow a fixed calendar, so slow sellers are cut too late and healthy ones too deep, and margin leaks out of the season before the buyer sees the whole picture.",
                    who="Merchandising",
                    how="Sell-through and price history conformed on Delta Lake feed markdown-timing models in Model Serving, and recommended cuts are written back to POS and commerce through Price & Markdown.",
                    comps=["Model Serving", "MLflow", "Delta Lake", "Price & Markdown", "SymphonyAI IRIS"],
                    stories=[
                        ["ABFRL automates markdown recommendations with ML", "https://www.databricks.com/customers/aditya-birla-fashion-and-retail-ltd"],
                    ]),
                uc("Allocation Optimisation", "Inventory", "product", "Initial and replenishment allocation tuned to size and door profiles.",
                    problem="Initial and replenishment allocation lean on flat size curves and one national plan, so the wrong sizes land in the wrong doors and stores trade around the buy instead of to it.",
                    who="Planning & Allocation",
                    how="Demand signals and door profiles scored in Model Serving drive size curves in the Allocation Optimizer, and door-level allocations are released to the WMS through Allocation Releases.",
                    comps=["Allocation Optimizer", "Model Serving", "Allocation Releases", "Blue Yonder WMS", "Unity Catalog"],
                    stories=[
                        ["ABFRL scales store-level SKU assortment and allocation", "https://www.databricks.com/customers/aditya-birla-fashion-and-retail-ltd"],
                        ["Al-Futtaim forecasts seasonal orders for Marks & Spencer", "https://www.databricks.com/customers/al-futtaim"],
                    ]),
                uc("Omnichannel Fulfillment", "Operations", "stream", "Ship-from-store and BOPIS against unified inventory positions.",
                    problem="Web, store and warehouse stock live in separate systems, so orders route to the wrong node, ship-from-store picks what is already sold, and BOPIS promises break at the counter.",
                    who="Store Operations",
                    how="Manhattan and commerce feeds land in Lakehouse//RT to hold one live inventory position, so ship-from-store and BOPIS route against real availability from the Store Command Centre.",
                    comps=["Store Command Centre", "Lakehouse//RT", "Manhattan Active Omni", "Salesforce Commerce", "Delta Lake"]),
                uc("Personalisation", "Digital", "custlake", "Offers and recommendations ranked without copying profiles off-platform.",
                    problem="Offers are batched from stale segments and scattered across web, app and email, so shoppers see irrelevant messages while profiles get copied into yet another marketing tool.",
                    who="Digital & CRM",
                    how="Loyalty and web behaviour conformed in CustomerLake feed ranking models in Model Serving, and offers are served through Personalisation Studio without copying profiles off-platform.",
                    comps=["Personalisation Studio", "CustomerLake", "Model Serving", "Adobe Experience Plat", "Feature Store"],
                    stories=[
                        ["Skechers lifts click-through 324% with personalization", "https://www.databricks.com/customers/skechers"],
                        ["Wehkamp serves recommendations at scale and doubles revenue", "https://www.databricks.com/customers/wehkamp"],
                    ]),
                uc("In-Stock Optimisation", "Availability", "gauge", "Safety stock and replenishment tuned to actual demand variability.",
                    problem="Safety stock is set once by rule of thumb, so demand variability shows up as empty shelves on the fastest sellers and cash tied up in the slow ones, and nobody sees a stockout spread.",
                    who="Store Operations",
                    how="POS and inventory positions stream into Lakehouse//RT and replenishment models in Model Serving tune min-max by SKU and door, raising Replenishment Orders before a shelf goes empty.",
                    comps=["Store Command Centre", "Lakehouse//RT", "Model Serving", "Replenishment Orders", "SAP S/4HANA Retail"],
                    stories=[
                        ["Walgreens right-sizes inventory to avoid stockouts", "https://www.databricks.com/customers/walgreens"],
                        ["Top 7 ways AI in retail improves inventory availability", "https://www.databricks.com/blog/top-7-ways-ai-retail-enhances-customer-experience-and-operations"],
                    ]),
                uc("Promotion ROI", "Commercial", "partner", "Campaign lift measured on incremental sales not vanity traffic.",
                    problem="Campaigns are judged on traffic and redemptions, so promotions that pull demand forward or cannibalise full-price sales look like wins and the real margin impact is never measured.",
                    who="Merchant Leadership",
                    how="POS, promotion and loyalty data conformed on Delta Lake feed incremental-lift models in Model Serving, and campaign ROI lands on certified Metric Views merchants read in AI/BI.",
                    comps=["AI/BI", "Model Serving", "Delta Lake", "Salesforce Loyalty", "Unity Catalog"],
                    stories=[
                        ["Currys drives growth and retail media with data intelligence", "https://www.databricks.com/customers/currys"],
                    ]),
                uc("Shrink Analytics", "Loss prevention", "observ", "Inventory shrink correlated to store, category and process gaps.",
                    problem="Shrink surfaces once a year at physical count, so theft, process error and phantom inventory blur together and the store or workflow driving the loss stays invisible until margin is gone.",
                    who="Store Operations",
                    how="POS exceptions, inventory movements and WMS events conformed on Delta Lake are scored for anomalies in Model Serving, so shrink is attributed to store, category and process in AI/BI.",
                    comps=["Model Serving", "Delta Lake", "AI/BI", "NCR Voyix POS", "Unity Catalog"]),
                uc("Clienteling", "Store", "people", "High-value customers recognized in every channel with governed profiles.",
                    problem="Associates meet a high-value customer with no memory of the last visit, so online history, loyalty tier and preferences that would close the sale sit in systems the shop floor cannot reach.",
                    who="Digital & CRM",
                    how="Household profiles resolved in CustomerLake are served to associate apps through Databricks Apps on Lakebase, so every channel recognises the customer against one governed profile.",
                    comps=["Personalisation Studio", "CustomerLake", "Apps", "Lakebase", "Salesforce Loyalty"],
                    stories=[
                        ["PetSmart boosts engagement and loyalty with AI decisioning", "https://www.databricks.com/customers/petsmart/ai"],
                        ["From search to sale: AI-driven engagement and loyalty in retail", "https://www.databricks.com/blog/search-sale-how-ai-redefining-customer-engagement-and-loyalty-retail"],
                    ]),
                uc("Supplier OTIF", "Supply", "globe", "Vendor fill rates and lead-time variability surfaced before stockouts.",
                    problem="Vendor fill rates and lead times hide in EDI and email, so late or short deliveries are discovered only when a receipt fails to arrive and the stockout has already hit the shelf.",
                    who="Planning & Allocation",
                    how="PO, ASN and receipt data from ERP and EDI conformed on Delta Lake track fill rate and lead-time variability in AI/BI, flagging at-risk receipts before they become stockouts.",
                    comps=["AI/BI", "Delta Lake", "Unity Catalog", "E2open Supply Planning", "Wholesale EDI"],
                    stories=[
                        ["Al-Futtaim improves supply chain and cuts inventory holding cost", "https://www.databricks.com/customers/al-futtaim"],
                        ["Columbia Sportswear accelerates supply chain analytics on Databricks", "https://www.databricks.com/customers/columbia"],
                    ]),
            ],
        ),
        "sources": {
            "sap-retail": {"t": "SAP S/4HANA Retail", "u": "https://www.sap.com/industries/retail.html"},
            "oracle-retail": {"t": "Oracle Retail Merchandising", "u": "https://www.oracle.com/retail/merchandising/"},
            "blue-yonder-wms": {"t": "Blue Yonder WMS", "u": "https://blueyonder.com/solutions/warehouse-management"},
            "sf-commerce": {"t": "Salesforce Commerce Cloud", "u": "https://www.salesforce.com/commerce/"},
            "shopify": {"t": "Shopify Plus", "u": "https://www.shopify.com/plus"},
            "ncr-voyix": {"t": "NCR Voyix", "u": "https://www.ncr.com/retail"},
            "manhattan-omni": {"t": "Manhattan Active Omni", "u": "https://www.manh.com/solutions"},
            "e2open": {"t": "E2open", "u": "https://www.e2open.com/"},
            "symphony-iris": {"t": "SymphonyAI IRIS", "u": "https://www.symphonyai.com/retail/"},
            "sf-loyalty": {"t": "Salesforce Loyalty Management", "u": "https://www.salesforce.com/products/loyalty-management/"},
            "adobe-aep": {"t": "Adobe Experience Platform", "u": "https://business.adobe.com/products/experience-platform/adobe-experience-platform.html"},
            "medallia": {"t": "Medallia", "u": "https://www.medallia.com/"},
            "nielseniq": {"t": "NielsenIQ retail measurement", "u": "https://nielseniq.com/global/en/solutions/"},
            "google-merchant": {"t": "Google Merchant Center", "u": "https://merchants.google.com/"},
        },
    },
}
