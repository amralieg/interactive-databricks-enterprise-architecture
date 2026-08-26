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


INDUSTRIES_BATCH_APPAREL_FASHION = {
    'apparel_fashion': {
        "label": "Apparel & Fashion",
        "blurb": "Seasonal collections, omnichannel retail, demand sensing, and sustainable sourcing across design, manufacturing, and direct-to-consumer channels.",
        "medallion": medallion(
            "Raw style and sales feeds",
            "POS, e-commerce, PLM and factory WIP events landed exactly as received so a markdown or a allocation can be replayed.",
            "Conformed styles and channels",
            "Styles, SKUs, stores and digital channels resolved into single entities across ERP, PLM and commerce platforms.",
            "Sell-through, margin, OTB",
            "Contracted products merchandising and finance run on: sell-through rate, full-price sell-through, OTB and margin by collection.",
        ),
        "rails": {
            "src": [
                {"box": "PLM & Design", "ic": "product", "tiles": [
                    tile("Centric PLM", "product", "Style masters, BOMs, colorways and sample approvals through development.", "centric-plm"),
                    tile("Adobe Substance", "apps", "Material libraries and 3D render assets linked to style records.", "adobe-substance"),
                    tile("CLO 3D", "apps", "Digital samples and fit iterations before physical proto.", "clo-3d"),
                ]},
                {"box": "ERP & Supply", "ic": "erp", "tiles": [
                    tile("Infor CloudSuite Fashion", "erp", "Seasonal collections, purchasing and factory allocations.", "infor-fashion"),
                    tile("SAP S/4HANA Retail", "erp", "Inventory, allocation and financial close for multi-brand houses.", "sap-retail"),
                    tile("Blue Yonder WMS", "stream", "Warehouse execution, pick paths and store replenishment.", "blue-yonder-wms"),
                ]},
                {"box": "Commerce & POS", "ic": "market", "tiles": [
                    tile("Shopify Plus", "partner", "DTC orders, returns and customer profiles across owned sites.", "shopify"),
                    tile("Salesforce Commerce Cloud", "partner", "Omnichannel carts, promotions and clienteling data.", "sf-commerce"),
                    tile("Oracle Xstore POS", "market", "Store transactions, associates and endless aisle lookups.", "oracle-xstore"),
                ]},
                {"box": "Manufacturing", "ic": "zplug", "tiles": [
                    tile("Lectra Fashion", "zplug", "Marker making, cutting room and factory KPIs.", "lectra"),
                    tile("Gerber Technology", "iot", "Spreading, cutting and unit production tracking.", "gerber"),
                    tile("Fast React Plan", "sheet", "Factory capacity, T&A calendars and critical path.", "fast-react"),
                ]},
                {"box": "Sustainability", "ic": "gavel", "tiles": [
                    tile("Higg Index MSI", "gavel", "Material sustainability scores and facility social audits.", "higg"),
                    tile("Textile Exchange", "partner", "Preferred fiber certifications and chain of custody.", "textile-exchange"),
                ]},
                fed_group("Wholesale Partner Mart", "Department store sell-in and chargeback marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("Edited Retail Intel", "market", "Competitor pricing, assortment and markdown signals by market.", "edited"),
                tile("WGSN Trend Forecast", "ztarget", "Macro trends, color and silhouette forecasts for line planning.", "wgsn"),
                tile("Open Supply Hub", "globe", "Factory disclosure and supplier mapping for due diligence.", "opensupplyhub"),
            ]),
            "ppl": ppl2([
                biz("Brand President & CFO", "Genie One",
                    "The CEO on brand heat and wholesale sell-in; the CFO on gross margin, full-price sell-through and inventory ownership.",
                    [["Genie One", "Ask what last collection's full-price sell-through was."], ["AI/BI", "Margin and OTB on certified Metric Views."], ["Unity Catalog", "One SKU definition across channels."]]),
                biz("Merchandising", "AI/BI",
                    "Assortment breadth, depth, pricing and markdown cadence by door and channel, judged on sell-through rate, weeks of supply and GMROI.",
                    [["Allocation Optimizer", "Size curves and door profiles before allocation locks."], ["AI/BI", "Sell-through and WOS on governed POS."]]),
                biz("Planning & Allocation", "Model Serving",
                    "Open-to-buy, size curves and replenishment against demand forecasts, balancing receipt plans, in-stock rate and markdown liability.",
                    [["OTB Workbench", "Receipt plans against sell-through scenarios."], ["Model Serving", "Demand forecasts in the allocation path."]]),
                biz("Sourcing & Production", "Lakehouse//RT",
                    "Factory capacity, time-and-action risk and cost negotiations, tracked on on-time delivery, WIP by PO and landed cost per unit.",
                    [["Factory Tracker", "WIP and delay risk by PO and factory."], ["Lakehouse//RT", "Production milestones at operational latency."]]),
                biz("Digital & CRM", "Apps",
                    "Clienteling, loyalty and personalization across stores and DTC, measured on repeat rate, clienteled revenue and conversion.",
                    [["Clienteling App", "Associate recommendations on governed customer profiles."], ["Apps", "Store apps hosted next to governed data."]]),
            ], [
                biz("Data Engineers", "Lakeflow",
                    "Land POS, e-commerce, PLM style masters and factory WIP; own Bronze to Silver and the pager when the sell-through tables merchandisers trade on stall.",
                    [["Lakeflow Connect", "Managed connectors for ERP, PLM and commerce sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on POS and production feeds."], ["Lakewatch", "Freshness on the sell-through tables the trading room reads every morning."]]),
                biz("Data Scientists", "MLflow",
                    "Short-lifecycle demand-sensing, size-curve and markdown-optimisation models, and whether they still hold across a new season's assortment.",
                    [["Feature Store", "Style and door features read identically in training and serving."], ["MLflow", "Every demand and markdown model tracked for audit and reproduction."], ["Model Serving", "Demand and markdown models scored in the allocation path."]]),
                biz("App Developers", "Apps",
                    "Ship the OTB workbench, allocation optimizer, factory tracker and clienteling apps merchandising and stores work in, next to governed style data.",
                    [["Apps", "Operational and store screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for allocation and clienteling state."], ["Agent Bricks", "Agents that draft receipt and markdown moves against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Looker", "chart", "Merchandising and finance dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for sell-through and OTB in the trading room."),
                    tile("Notebooks & IDEs", "notebook", "Planning notebooks against governed style and sales data."),
                ]},
                {"box": "Wholesale & Retail", "ic": "partner", "tiles": [
                    tile("EDI 850/856 ASN", "api", "Wholesale orders and advance ship notices to department store partners."),
                    tile("Endless Aisle API", "partner", "Store lookups against central inventory for clienteling.", "oracle-xstore"),
                    tile("Marketplace Feeds", "globe", "Assortment and inventory synced to Zalando and Farfetch.", "shopify"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Allocation Releases", "stream", "Door-level allocations pushed to WMS before pick waves."),
                    tile("Price & Markdown", "market", "Markdown recommendations written to POS and commerce.", "sf-commerce"),
                    tile("Factory PO Updates", "zplug", "Revised quantities and dates sent to vendor portals.", "fast-react"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("EU DPP Readiness", "gavel", "Digital product passport attributes assembled from PLM and supply chain."),
                    tile("Modern Slavery Reports", "share", "Supplier audit status filed from governed facility data.", "higg"),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Style and sell-through products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Wholesale partners reading inventory via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("OTB Workbench", "Receipt planning", "sheet", "Open-to-buy scenarios by collection before purchase orders are released."),
             app("Allocation Optimizer", "Door profiles", "market", "Size curves and door-level allocation against demand and constraints."),
             app("Factory Tracker", "Production WIP", "zplug", "PO milestones, delay risk and air-freight decisions before launch windows slip."),
             app("Clienteling App", "Store associate", "custlake", "Recommendations and endless aisle on governed customer and inventory data.")],
            [uc("Demand Sensing", "Planning", "chart", "Short-lifecycle forecasts updated from POS and digital signals."),
             uc("Size Curve Optimization", "Allocation", "product", "Size profiles tuned by door cluster and sell-through."),
             uc("Markdown Optimization", "Pricing", "market", "Markdown timing and depth maximizing margin recovery."),
             uc("Factory Risk Monitoring", "Sourcing", "zplug", "T&A delays flagged before launch dates are missed."),
             uc("Sustainable Sourcing", "ESG", "gavel", "Preferred materials and audited factories scored at style level."),
             uc("Omnichannel Fulfillment", "Operations", "stream", "Ship-from-store and BOPIS against unified inventory."),
             uc("Clienteling & CRM", "Retail", "custlake", "High-value customers recognized in every channel."),
             uc("Wholesale Chargebacks", "Finance", "erp", "Deductions reconciled to shipment and compliance data."),
             uc("3D Sample Reduction", "Design", "apps", "Physical samples replaced by digital fit approval."),
             uc("Inventory Right-Sizing", "Finance", "chart", "WOS targets by category before excess ownership builds.")],
        ),
        "sources": {
            "centric-plm": {"t": "Centric PLM", "u": "https://www.centricsoftware.com/"},
            "adobe-substance": {"t": "Adobe Substance 3D", "u": "https://www.adobe.com/products/substance3d.html"},
            "clo-3d": {"t": "CLO 3D", "u": "https://www.clo3d.com/"},
            "infor-fashion": {"t": "Infor CloudSuite Fashion", "u": "https://www.infor.com/industries/fashion"},
            "sap-retail": {"t": "SAP S/4HANA Retail", "u": "https://www.sap.com/industries/retail.html"},
            "blue-yonder-wms": {"t": "Blue Yonder WMS", "u": "https://blueyonder.com/solutions/warehouse-management"},
            "shopify": {"t": "Shopify Plus", "u": "https://www.shopify.com/plus"},
            "sf-commerce": {"t": "Salesforce Commerce Cloud", "u": "https://www.salesforce.com/commerce/"},
            "oracle-xstore": {"t": "Oracle Xstore", "u": "https://www.oracle.com/retail/"},
            "lectra": {"t": "Lectra", "u": "https://www.lectra.com/"},
            "gerber": {"t": "Gerber Technology", "u": "https://gerbertechnology.com/"},
            "fast-react": {"t": "Fast React", "u": "https://www.fastreact.com/"},
            "higg": {"t": "Higg Index", "u": "https://higg.com/"},
            "textile-exchange": {"t": "Textile Exchange", "u": "https://textileexchange.org/"},
            "edited": {"t": "Edited", "u": "https://edited.com/"},
            "wgsn": {"t": "WGSN", "u": "https://www.wgsn.com/"},
            "opensupplyhub": {"t": "Open Supply Hub", "u": "https://www.opensupplyhub.org/"},
        },
    },
}
