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


INDUSTRIES_BATCH_ECOMMERCE = {
    'ecommerce': {
        "label": "E-Commerce",
        "blurb": "Digital commerce: catalog, orders, fulfillment, personalization, and marketplace operations across DTC and marketplace channels.",
        "medallion": medallion(
            "Raw clickstream and orders",
            "Web events, OMS orders, payment captures and WMS shipments landed exactly as received.",
            "Conformed customers and orders",
            "Customers, sessions, orders and SKUs resolved across storefront, OMS and fulfillment.",
            "Conversion, AOV, LTV",
            "Contracted products growth and ops run on: conversion rate, AOV, repeat rate and fulfillment SLA.",
        ),
        "rails": {
            "src": [
                {"box": "Commerce Platform", "ic": "apps", "tiles": [
                    tile("Shopify Plus", "apps", "Catalog, carts, checkouts and customer accounts.", "shopify-ec"),
                    tile("Salesforce Commerce Cloud", "partner", "B2C and B2B storefronts with promotions.", "sfcc"),
                    tile("Adobe Commerce", "product", "Magento catalog, pricing and multi-site config.", "adobe-commerce"),
                ]},
                {"box": "OMS & Payments", "ic": "erp", "tiles": [
                    tile("Manhattan Active Omni", "erp", "Order orchestration, promising and returns.", "manhattan"),
                    tile("Stripe Payments", "market", "Payment intents, disputes and payout reconciliation.", "stripe"),
                    tile("Adyen Platform", "partner", "Global acquiring, risk and settlement.", "adyen"),
                ]},
                {"box": "Fulfillment & WMS", "ic": "stream", "tiles": [
                    tile("ShipBob WMS", "stream", "Pick, pack and carrier manifests.", "shipbob"),
                    tile("Flexport Logistics", "globe", "Inbound containers, customs and drayage.", "flexport"),
                    tile("Narvar Post-Purchase", "partner", "Tracking, returns and WISMO experiences.", "narvar"),
                ]},
                {"box": "Marketing & CRM", "ic": "custlake", "tiles": [
                    tile("Klaviyo", "custlake", "Email, SMS and lifecycle segments.", "klaviyo"),
                    tile("Braze", "partner", "Cross-channel campaigns and canvas journeys.", "braze"),
                    tile("Google Analytics 4", "observ", "Session, funnel and attribution events.", "ga4"),
                ]},
                {"box": "Marketplaces", "ic": "market", "tiles": [
                    tile("Amazon Seller Central", "market", "Marketplace orders, fees and advertising.", "amazon-sc"),
                    tile("eBay Managed Payments", "partner", "Third-party marketplace transactions.", "ebay"),
                ]},
                fed_group("Finance Revenue Mart", "Revenue recognition marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("Similarweb Digital", "observ", "Competitive traffic and channel mix benchmarks.", "similarweb"),
                tile("Jungle Scout", "market", "Marketplace share and keyword intelligence.", "jungle-scout"),
                tile("ShipStation Rates", "api", "Carrier rate shopping and delivery promises.", "shipstation"),
            ]),
            "ppl": ppl2([
                biz("CEO & Growth CFO", "Genie One",
                    "The CEO on GMV and contribution margin; the CMO on CAC and LTV, watching conversion rate, AOV and repeat rate by channel.",
                    [["Genie One", "Ask what yesterday's conversion rate was by channel."], ["AI/BI", "Revenue and margin on certified Metric Views."], ["Unity Catalog", "One customer ID across storefront and CRM."]]),
                biz("Growth Marketing", "Model Serving",
                    "Paid acquisition, SEO and lifecycle campaigns, judged on blended CAC, LTV-to-CAC and return on ad spend against payback period by channel.",
                    [["Attribution Hub", "Multi-touch credit across paid and owned."], ["Model Serving", "Propensity models in the campaign path."]]),
                biz("Merchandising", "AI/BI",
                    "Assortment, pricing, bundles and on-site search relevance, tracked on attach rate, gross margin and competitive price gap.",
                    [["Pricing Workbench", "Elasticity and competitive price gaps."], ["AI/BI", "Basket and attach rate on governed orders."]]),
                biz("Operations", "Lakehouse//RT",
                    "Fulfillment SLA, inventory and returns processing, run on on-time delivery, fill rate and cost to serve per order.",
                    [["Fulfillment Command", "Promise vs actual delivery by node."], ["Lakehouse//RT", "Inventory ATP at cart latency."]]),
                biz("Customer Experience", "Apps",
                    "Support, reviews and loyalty program health, measured on CSAT, NPS and repeat purchase against return rate and contact rate by cohort.",
                    [["CX Console", "CSAT, NPS and repeat purchase by cohort."], ["Apps", "Support tools on governed order history."]]),
            ], [
                biz("Data Engineers", "Lakeflow",
                    "Land web clickstream, OMS orders, payment captures and WMS shipments; own Bronze to Silver and the pager when the revenue and ATP tables stall.",
                    [["Lakeflow Connect", "Managed connectors for commerce, OMS and payment sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on clickstream and order feeds."], ["Lakewatch", "Freshness on the revenue and conversion tables growth reads at standup."]]),
                biz("Data Scientists", "MLflow",
                    "Recommendation, propensity, dynamic-pricing and checkout-fraud models, and whether they still hold across a peak season and channel mix shift.",
                    [["Feature Store", "Customer and session features read identically in training and serving."], ["MLflow", "Every recommendation and fraud model tracked for audit and reproduction."], ["Model Serving", "Recommendation and fraud models scored in the checkout path."]]),
                biz("App Developers", "Apps",
                    "Ship the attribution hub, pricing workbench, fulfillment command and CX console apps growth and operations work in, next to governed order data.",
                    [["Apps", "Growth and operations screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for cart-recovery and inventory-hold state."], ["Agent Bricks", "Agents that draft pricing and recovery moves against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Looker", "chart", "Growth and ops dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for daily revenue in growth standups."),
                    tile("Notebooks & IDEs", "notebook", "Analyst notebooks on governed clickstream."),
                ]},
                {"box": "Channels & Partners", "ic": "partner", "tiles": [
                    tile("Marketplace Listings", "api", "Inventory and price sync to Amazon and eBay.", "amazon-sc"),
                    tile("3PL Status Feed", "stream", "Shipment events shared to Narvar and Klaviyo.", "narvar"),
                    tile("Affiliate Networks", "partner", "Commission and attribution to partners.", "braze"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Dynamic Pricing", "market", "Price updates pushed to commerce and marketplaces.", "sfcc"),
                    tile("Cart Recovery", "custlake", "Abandonment sequences triggered from session data.", "klaviyo"),
                    tile("Inventory Holds", "stream", "ATP reservations released or extended in OMS.", "manhattan"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Sales Tax Filing", "gavel", "Jurisdiction filings from governed transaction data."),
                    tile("PCI Scope Reports", "share", "Cardholder data environment attestations."),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Customer and order products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Brand partners via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Attribution Hub", "Marketing mix", "chart", "Multi-touch attribution across paid, owned and marketplace channels."),
             app("Pricing Workbench", "Elasticity", "market", "Price gaps and elasticity scenarios before changes go live."),
             app("Fulfillment Command", "Delivery SLA", "gauge", "Promise vs actual ship and delivery by node and carrier."),
             app("CX Console", "Customer health", "custlake", "CSAT, returns and repeat rate by cohort and segment.")],
            [uc("Personalization", "Growth", "custlake", "Product recommendations and content ranked per visitor."),
             uc("Cart Abandonment", "Lifecycle", "apps", "Recovery sequences timed to session behavior."),
             uc("Dynamic Pricing", "Merchandising", "market", "Prices adjusted to elasticity and competitive signals."),
             uc("Inventory ATP", "Operations", "stream", "Available-to-promise accurate at add-to-cart."),
             uc("Fraud Prevention", "Payments", "gavel", "Checkout fraud scored before capture."),
             uc("Search Relevance", "Discovery", "observ", "Query understanding and ranking tuned to conversion."),
             uc("Returns Optimization", "CX", "partner", "Return reasons analyzed to reduce preventable volume."),
             uc("Marketplace Sync", "Channels", "globe", "Listings, fees and ads optimized across marketplaces."),
             uc("LTV Segmentation", "CRM", "custlake", "Cohorts scored for retention and upsell campaigns."),
             uc("Fulfillment Network", "Logistics", "stream", "Orders routed to the lowest-cost node meeting SLA.")],
        ),
        "sources": {
            "shopify-ec": {"t": "Shopify Plus", "u": "https://www.shopify.com/plus"},
            "sfcc": {"t": "Salesforce Commerce Cloud", "u": "https://www.salesforce.com/commerce/"},
            "adobe-commerce": {"t": "Adobe Commerce", "u": "https://business.adobe.com/products/magento/magento-commerce.html"},
            "manhattan": {"t": "Manhattan Associates", "u": "https://www.manh.com/"},
            "stripe": {"t": "Stripe", "u": "https://stripe.com/"},
            "adyen": {"t": "Adyen", "u": "https://www.adyen.com/"},
            "shipbob": {"t": "ShipBob", "u": "https://www.shipbob.com/"},
            "flexport": {"t": "Flexport", "u": "https://www.flexport.com/"},
            "narvar": {"t": "Narvar", "u": "https://corp.narvar.com/"},
            "klaviyo": {"t": "Klaviyo", "u": "https://en.wikipedia.org/wiki/Klaviyo"},
            "braze": {"t": "Braze", "u": "https://www.braze.com/"},
            "ga4": {"t": "Google Analytics 4", "u": "https://marketingplatform.google.com/about/analytics/"},
            "amazon-sc": {"t": "Amazon Seller Central", "u": "https://sellercentral.amazon.com/"},
            "ebay": {"t": "eBay", "u": "https://www.ebay.com/"},
            "similarweb": {"t": "Similarweb", "u": "https://www.similarweb.com/"},
            "jungle-scout": {"t": "Jungle Scout", "u": "https://www.junglescout.com/"},
            "shipstation": {"t": "ShipStation", "u": "https://www.shipstation.com/"},
        },
    },
}
