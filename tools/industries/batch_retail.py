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
                biz("Merchant Leadership", "Genie One", "The CEO on comparable sales and market share; the CFO on gross margin and inventory ownership when a season turns and markdowns start to bite.", [["Genie One", "Ask what comp sales were yesterday by banner without waiting on retail analytics."], ["AI/BI", "Sales, margin and in-stock on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"comp\" means one thing across channels."]]),
                biz("Merchandising", "AI/BI", "Buyers on assortment, pricing and markdown cadence by category, tracking sell-through and weeks of supply against the merchandise plan.", [["Allocation Optimizer", "Size curves and door profiles before allocation locks."], ["AI/BI", "Sell-through and WOS on governed POS."], ["Genie One", "Ask which SKUs are overstocked before markdown season."]]),
                biz("Planning & Allocation", "Model Serving", "Planners on forecast accuracy, receipts and replenishment at risk, watching in-stock rate and inventory turns across the store network.", [["Demand Planning Hub", "Consensus forecast before buy meetings."], ["Model Serving", "Demand models scored in the allocation path."], ["Unity Catalog", "One SKU definition across ERP and commerce."]]),
                biz("Store Operations", "Lakehouse//RT", "Field leaders on labor, conversion and in-stock during peak weeks, watching sales per labor hour and how fast a stockout spreads across doors.", [["Store Command Centre", "Traffic, conversion and labor against plan."], ["Lakehouse//RT", "Inventory positions at the latency a stockout spreads at."], ["Apps", "Associate tasking on governed store data."]]),
                biz("Digital & CRM", "CustomerLake", "E-commerce and loyalty on traffic, conversion and retention, tracking customer lifetime value and churn across web, app and store.", [["Personalisation Studio", "Offers ranked on governed segments."], ["CustomerLake", "Household profiles without copying CDP elsewhere."], ["Model Serving", "Churn models in the marketing path."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the ERP item, commerce, WMS and loyalty feeds; own the Bronze to Silver path and the pager when a retail pipeline breaks.", [["Lakeflow Connect", "Managed connectors for retail ERP, commerce and WMS sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on POS and inventory feeds."], ["Lakewatch", "Freshness on the comp sales and in-stock tables merchants read."]]),
                biz("Data Scientists", "MLflow", "Demand-forecast, markdown, allocation and personalisation models, and whether they still hold six months after deployment across banners and channels.", [["Feature Store", "POS and web features read identically in training and serving."], ["MLflow", "Every forecast and markdown run tracked for audit and reproduction."], ["Model Serving", "Demand and offer models scored in the allocation and marketing path."]]),
                biz("App Developers", "Apps", "Ship the store command, demand planning and personalisation applications merchants and field teams work in, hosted next to governed retail data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for tasking state and governed writes."], ["Agent Bricks", "Agents that draft a replenishment order against governed tools."]]),
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
                uc("Demand Forecasting", "Planning", "chart", "SKU-store forecasts updated from POS, web and local signals."),
                uc("Markdown Optimisation", "Margin", "market", "Markdown timing and depth maximising margin recovery not calendar rules."),
                uc("Allocation Optimisation", "Inventory", "product", "Initial and replenishment allocation tuned to size and door profiles."),
                uc("Omnichannel Fulfillment", "Operations", "stream", "Ship-from-store and BOPIS against unified inventory positions."),
                uc("Personalisation", "Digital", "custlake", "Offers and recommendations ranked without copying profiles off-platform."),
                uc("In-Stock Optimisation", "Availability", "gauge", "Safety stock and replenishment tuned to actual demand variability."),
                uc("Promotion ROI", "Commercial", "partner", "Campaign lift measured on incremental sales not vanity traffic."),
                uc("Shrink Analytics", "Loss prevention", "observ", "Inventory shrink correlated to store, category and process gaps."),
                uc("Clienteling", "Store", "people", "High-value customers recognized in every channel with governed profiles."),
                uc("Supplier OTIF", "Supply", "globe", "Vendor fill rates and lead-time variability surfaced before stockouts."),
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
