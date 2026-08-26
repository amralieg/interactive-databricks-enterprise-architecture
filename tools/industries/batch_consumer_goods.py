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


INDUSTRIES_BATCH_CONSUMER_GOODS = {
    'consumer_goods': {
        "label": "Consumer Goods",
        "blurb": "CPG manufacturing and distribution: demand planning, trade promotion, retail execution, and supply chain across brands and categories.",
        "medallion": medallion(
            "Raw sell-in and sell-out",
            "ERP shipments, retailer POS, syndicated scan and promo calendars landed exactly as received.",
            "Conformed products and markets",
            "SKUs, banners, geographies and promotions resolved across ERP, TPM and syndicated data.",
            "Shipments, share, promo ROI",
            "Contracted products sales and finance run on: shipment volume, market share, promo lift and trade spend ROI.",
        ),
        "rails": {
            "src": [
                {"box": "ERP & Manufacturing", "ic": "erp", "tiles": [
                    tile("SAP IBP / S/4", "erp", "Demand, supply and production planning with financials.", "sap-ibp"),
                    tile("Oracle JD Edwards", "erp", "Batch manufacturing, lot trace and DSD routes.", "jde"),
                    tile("Kinaxis RapidResponse", "sheet", "Concurrent planning and scenario simulation.", "kinaxis"),
                ]},
                {"box": "Retail & Syndicated", "ic": "market", "tiles": [
                    tile("NielsenIQ Connect", "market", "Syndicated scan and market share by category.", "nielseniq"),
                    tile("Circana Liquid Data", "chart", "Omni-channel consumption and household panels.", "circana"),
                    tile("IRI Market Advantage", "market", "Promo decomposition and competitive tracking.", "iri"),
                ]},
                {"box": "Trade Promotion", "ic": "partner", "tiles": [
                    tile("SAP TPM", "partner", "Promo planning, accruals and settlement.", "sap-tpm"),
                    tile("Vistex GTM", "market", "Chargebacks, rebates and contract compliance.", "vistex"),
                    tile("Blacksmith TPM", "chart", "ROI analytics and post-event evaluation.", "blacksmith"),
                ]},
                {"box": "Field & DSD", "ic": "stream", "tiles": [
                    tile("Salesforce Consumer Goods", "custlake", "Retail visits, audits and perfect store scores.", "sf-cg"),
                    tile("HighJump WMS", "stream", "Warehouse picking and DSD route sequencing.", "highjump"),
                    tile("o9 Demand Planning", "sheet", "Statistical and ML forecasts by SKU-region.", "o9"),
                ]},
                {"box": "E-commerce", "ic": "apps", "tiles": [
                    tile("Amazon Vendor Central", "partner", "Purchase orders, chargebacks and traffic.", "amazon-vc"),
                    tile("Instacart Ads & Data", "product", "Retail media and basket insights.", "instacart"),
                ]},
                fed_group("Finance Close Mart", "Trade spend accrual marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("Weather Source", "stream", "Weather-driven demand signals by market.", "weather-source"),
                tile("USDA ERS Food Data", "api", "Commodity input cost indices for margin planning.", "usda-ers"),
                tile("Google Trends", "observ", "Search interest proxies for emerging demand.", "google-trends"),
            ]),
            "ppl": ppl2([
                biz("Brand & Category", "Genie One",
                    "The CEO on category share and innovation pipeline; the CFO on trade-spend efficiency and gross margin against promo ROI.",
                    [["Genie One", "Ask what last promo's ROI was by retailer."], ["AI/BI", "Share and margin on certified Metric Views."], ["Unity Catalog", "One SKU definition across syndicated and ERP."]]),
                biz("Sales & Accounts", "AI/BI",
                    "Joint business plans, distribution and perfect store execution, judged on market share, on-shelf availability and distribution points.",
                    [["Perfect Store Scorecard", "On-shelf availability and compliance by banner."], ["AI/BI", "Sell-through and share on governed syndicated data."]]),
                biz("Demand Planning", "Model Serving",
                    "Statistical forecasts, consensus and supply alignment, tracked on forecast accuracy, bias and consensus attainment by SKU-region.",
                    [["Consensus Forecast", "Sales and finance aligned on one number."], ["Model Serving", "ML forecasts in the planning path."]]),
                biz("Trade Marketing", "Apps",
                    "Promo design, accrual management and post-event analytics, measured on promo lift, incrementality and trade-spend ROI.",
                    [["Promo ROI Analyzer", "Lift and incrementality by event."], ["Apps", "Field audit apps on governed visit data."]]),
                biz("Supply Chain", "Lakehouse//RT",
                    "Service levels, inventory and production scheduling, run on OTIF, case fill rate and days of inventory against demand across DCs and SKUs.",
                    [["Supply Command", "OTIF and fill rate by DC and SKU."], ["Lakehouse//RT", "Inventory positions at operational latency."]]),
            ], [
                biz("Data Engineers", "Lakeflow",
                    "Land ERP shipments, retailer POS, syndicated scan and promo calendars; own Bronze to Silver and the pager when the share and promo tables stall.",
                    [["Lakeflow Connect", "Managed connectors for ERP, TPM and syndicated-data sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on shipment and scan feeds."], ["Lakewatch", "Freshness on the share and promo tables account teams read weekly."]]),
                biz("Data Scientists", "MLflow",
                    "Demand-forecast, promo-lift and price-pack elasticity models, and whether they still hold across a new innovation launch and channel shift.",
                    [["Feature Store", "SKU and market features read identically in training and serving."], ["MLflow", "Every forecast and lift model tracked for audit and reproduction."], ["Model Serving", "Forecast and lift models scored in the planning path."]]),
                biz("App Developers", "Apps",
                    "Ship the perfect store scorecard, consensus forecast, promo ROI analyzer and supply command apps sales and planning work in, next to governed SKU data.",
                    [["Apps", "Field and planning screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for audit and accrual state."], ["Agent Bricks", "Agents that draft promo and allocation moves against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Category and finance dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for share and promo questions."),
                    tile("Notebooks & IDEs", "notebook", "Planning notebooks on governed syndicated data."),
                ]},
                {"box": "Retailers & Brokers", "ic": "partner", "tiles": [
                    tile("EDI 852/867", "api", "Store-level inventory and consumption to retailers.", "nielseniq"),
                    tile("Retailer Portals", "globe", "Promo calendars and deductions reconciled digitally.", "sap-tpm"),
                    tile("DSD Route Updates", "stream", "Delivery sequences pushed to driver devices.", "highjump"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Promo Accruals", "market", "Accrual rates updated in ERP from planned events.", "sap-tpm"),
                    tile("Allocation Releases", "stream", "Scarce SKU allocation to priority banners.", "kinaxis"),
                    tile("Perfect Store Tasks", "custlake", "Corrective actions assigned to field reps.", "sf-cg"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Nutrition Labeling", "gavel", "Label compliance tracked from recipe to package."),
                    tile("ESG Packaging Reports", "share", "Recycled content disclosures to retailers."),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Category insight products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Retail partners via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Perfect Store Scorecard", "Retail execution", "market", "On-shelf availability, facings and promo compliance by store."),
             app("Consensus Forecast", "Demand planning", "sheet", "Statistical, sales and finance inputs merged into one plan."),
             app("Promo ROI Analyzer", "Trade spend", "chart", "Lift, incrementality and payback by event and retailer."),
             app("Supply Command", "Service levels", "gauge", "OTIF, fill rate and inventory health by DC and SKU.")],
            [uc("Demand Forecasting", "Planning", "chart", "ML forecasts refreshed with syndicated and weather signals."),
             uc("Trade Promotion ROI", "Marketing", "partner", "Promo events evaluated on true incrementality."),
             uc("Perfect Store", "Sales", "custlake", "Store-level execution scored and actioned."),
             uc("Supply Allocation", "Operations", "stream", "Finite supply allocated to highest-value markets."),
             uc("Price Pack Architecture", "Strategy", "product", "SKU mix optimized by channel and elasticity."),
             uc("Retail Media", "Digital", "market", "Retail media spend tied to sell-through outcomes."),
             uc("Chargeback Recovery", "Finance", "erp", "Retailer deductions reconciled to shipment proof."),
             uc("New Product Intro", "Innovation", "ztarget", "Launch curves tracked against distribution targets."),
             uc("Sustainability Tracking", "ESG", "gavel", "Packaging and sourcing metrics by brand."),
             uc("Inventory Optimization", "Finance", "chart", "Safety stock right-sized by service and cost.")],
        ),
        "sources": {
            "sap-ibp": {"t": "SAP IBP", "u": "https://www.sap.com/products/scm/integrated-business-planning.html"},
            "jde": {"t": "Oracle JD Edwards", "u": "https://www.oracle.com/applications/"},
            "kinaxis": {"t": "Kinaxis", "u": "https://www.kinaxis.com/"},
            "nielseniq": {"t": "NielsenIQ", "u": "https://nielseniq.com/"},
            "circana": {"t": "Circana", "u": "https://www.circana.com/"},
            "iri": {"t": "Circana Market Advantage", "u": "https://www.circana.com/"},
            "sap-tpm": {"t": "SAP Trade Promotion Management", "u": "https://www.sap.com/products/scm/trade-promotion-management.html"},
            "vistex": {"t": "Vistex", "u": "https://www.vistex.com/"},
            "blacksmith": {"t": "Blacksmith Applications", "u": "https://www.blacksmithapplications.com/"},
            "sf-cg": {"t": "Salesforce Consumer Goods Cloud", "u": "https://www.salesforce.com/consumer-goods/"},
            "highjump": {"t": "Körber HighJump", "u": "https://koerber-supplychain.com/"},
            "o9": {"t": "o9 Solutions", "u": "https://o9solutions.com/"},
            "amazon-vc": {"t": "Amazon Vendor Central", "u": "https://vendorcentral.amazon.com/"},
            "instacart": {"t": "Instacart", "u": "https://www.instacart.com/company/business"},
            "weather-source": {"t": "Weather Source", "u": "https://weathersource.com/"},
            "usda-ers": {"t": "USDA ERS", "u": "https://www.ers.usda.gov/"},
            "google-trends": {"t": "Google Trends", "u": "https://trends.google.com/"},
        },
    },
}
