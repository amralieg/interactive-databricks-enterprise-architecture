import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    """Business tiles plus an explicit, industry-specific Technical group of 3."""
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_FOOD_BEVERAGE = {
    'food_beverage': {
        "label": "Food & Beverage",
        "blurb": "CPG food and beverage manufacturers: recipe and batch production, quality and traceability, demand planning, and cold-chain logistics.",
        "medallion": medallion(
            "Raw plant and ERP",
            "MES batch records, ERP production orders, quality lab results, warehouse movements and retailer POS feeds, landed exactly as received so a lot code or a fill weight can always be replayed.",
            "Conformed SKU, batch",
            "SKUs, batches, plants and distribution nodes resolved into single conformed entities across ERP, MES and WMS, with lot genealogy reconciled from raw material to finished case.",
            "Yield, OTIF, quality",
            "Contracted products operations and sales run on: line yield and scrap, OTIF to retail customers, quality hold rates, and trade promotion ROI.",
        ),
        "rails": {
            "src": [
                {"box": "Manufacturing & MES", "ic": "erp", "tiles": [
                    tile("Rockwell FactoryTalk", "iot", "Line speeds, filler weights, CIP cycles and downtime reason codes from the plant floor.", "rockwell-ft"),
                    tile("Siemens Opcenter MES", "sheet", "Batch recipes, material consumption and electronic batch records for regulated plants.", "siemens-opcenter"),
                    tile("SAP S/4HANA PP", "erp", "Production orders, BOM explosions, confirmations and co-product yields.", "sap-s4")
                ]},
                {"box": "Quality & Safety", "ic": "gavel", "tiles": [
                    tile("Veeva QualityDocs", "gavel", "Specifications, deviations, CAPA and release documentation for food safety programs.", "veeva-quality"),
                    tile("SafetyChain Plant Mgmt", "gauge", "HACCP checks, temperature logs and sanitation records from production shifts.", "safetychain"),
                    tile("LIMS Lab Results", "db", "Microbiology, allergen and nutritional assay results tied to lot and line.")
                ]},
                {"box": "Supply & Logistics", "ic": "stream", "tiles": [
                    tile("Blue Yonder TMS", "stream", "Inbound raw material and outbound finished goods movements with carrier ETA and temperature probes.", "blue-yonder"),
                    tile("Manhattan WMS", "product", "Warehouse inventory, pick/pack and shipment confirmation against customer orders.", "manhattan-wms"),
                    tile("Sensitech TempTale", "iot", "Cold-chain logger readings from plant dock through DC to customer delivery.", "sensitech")
                ]},
                {"box": "Commercial & Retail", "ic": "market", "tiles": [
                    tile("NielsenIQ POS", "market", "Syndicated and direct retail sell-through by SKU, banner and geography.", "nielseniq"),
                    tile("Circana/IRI Panel", "chart", "Household panel and causal analytics for category and brand performance.", "circana"),
                    tile("Trade Promotion Mgmt", "partner", "Promotional calendars, scan data and accrual settlements with retail partners.")
                ]},
                fed_group(
                    "Co-manufacturer Inventory",
                    "Third-party production inventory and batch status left at co-packers and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("GS1 EPCIS Events", "api", "Serial shipping container and lot traceability events normalised on ingest for recall readiness.", "gs1-epcis"),
                tile("FDA FSMA 204 Trace", "gavel", "Key data elements for high-risk foods consumed inbound for compliance validation.", "fsma-204"),
                tile("Weather & Commodity", "globe", "Crop condition and commodity price feeds for agricultural input planning.")
            ]),
            "ppl": ppl2([
                biz("CEO & COO", "Genie One", "The CEO on volume, gross margin and category share; the COO on plant OEE, OTIF service level and recall exposure across the network.",
                    [["Genie One", "Ask what yesterday's OTIF was by customer without waiting on supply analytics."], ["AI/BI", "Volume, margin and quality on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"yield\" means one thing across plants."]]),
                biz("Plant Operations", "Lakehouse//RT", "Plant managers and line leads on changeover time, downtime reason codes and batch release, chasing line yield and scrap before the shift ends.",
                    [["Batch Genealogy Console", "Lot trace from raw material to pallet in one view."], ["Lakehouse//RT", "Live filler and CIP state at line speed."], ["AI/BI", "OEE and scrap on governed definitions."]]),
                biz("Quality & Food Safety", "AI/BI", "Quality managers on hold rate, open deviations, CAPA aging and sanitation compliance across sites when a supplier alert lands.",
                    [["Quality Hold Dashboard", "Open deviations and release status by plant and SKU."], ["AI/BI", "Hold rate and CAPA aging on certified Metric Views."], ["Unity Catalog", "One definition of lot status across MES and LIMS."]]),
                biz("Supply Chain", "Model Serving", "Planners on forecast accuracy and bias, inventory days of supply and which customer orders are at risk before the S&OP cycle locks.",
                    [["Demand Planning Workbench", "Consensus forecast scenarios before S&OP locks."], ["Model Serving", "Demand and service models scored against live orders."], ["AI/BI", "OTIF and inventory turns the sales team reads."]]),
                biz("Sales & Marketing", "CustomerLake", "Category managers on promotion lift versus cannibalised base, distribution voids and the retailer scorecards that decide the next line review.",
                    [["Trade ROI Analytics", "Promotion spend versus incremental volume by banner."], ["CustomerLake", "Retailer segments without copying syndicated data elsewhere."], ["Genie One", "Ask which SKUs lost distribution last month."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the MES, ERP, quality and retailer POS feeds; own the Bronze to Silver path and the pager when a plant or trace feed breaks.",
                    [["Lakeflow Connect", "Managed connectors for S/4HANA, MES and WMS sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on batch and POS feeds."], ["Lakewatch", "Freshness on the tables plant and supply teams read every morning."]]),
                biz("Data Scientists", "MLflow", "Demand, shelf-life and line-yield models, and whether they still hold six months after deployment.",
                    [["Feature Store", "SKU and plant features defined once for training and serving."], ["MLflow", "Every demand and yield run tracked for audit and reproduction."], ["Model Serving", "Forecast and quality models scored against live orders."]]),
                biz("App Developers", "Apps", "Ship the genealogy, demand-planning and quality-hold applications operations works in, hosted next to governed data.",
                    [["Apps", "Plant and quality screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for batch-release and hold writes."], ["Agent Bricks", "Agents that draft a recall trace or hold decision against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and quality alerts in the channel plants already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Plant Writeback", "ic": "opdb", "tiles": [
                    tile("MES Batch Release", "erp", "Quality release decisions written back into MES so pallets ship from governed lot status.", "siemens-opcenter"),
                    tile("SAP Order Reschedule", "db", "Production order dates adjusted from forecast consensus before materials are staged.", "sap-s4"),
                    tile("Floor Mobile Apps", "apps", "Sanitation tasks, line checks and downtime codes pushed to tablets on the line.")
                ]},
                {"box": "Retail & Co-pack", "ic": "partner", "tiles": [
                    tile("Retailer VMI Portal", "share", "Inventory and forecast positions shared with key retailers over Delta Sharing instead of weekly spreadsheets."),
                    tile("Co-manufacturer Portal", "partner", "Production schedules and lot genealogy exchanged with co-pack partners under contract."),
                    tile("3PL Cold Chain", "stream", "Temperature excursions and delivery proof shared back to carriers and customers.", "sensitech")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("FSMA Traceability", "gavel", "Traceability lot records and recall simulations produced from governed genealogy tables.", "fsma-204"),
                    tile("Nutrition Label Compliance", "share", "Label claims and allergen controls filed from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Retailers, co-packers and auditors reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Batch Genealogy Console", "Lot traceability", "stream", "Forward and backward trace from ingredient lot to retail case in seconds during a quality hold or recall."),
                app("Demand Planning Workbench", "S&OP consensus", "sheet", "Statistical and commercial forecast scenarios reconciled before production and procurement lock."),
                app("Quality Hold Dashboard", "Release control", "gauge", "Open deviations, lab results and sanitation checks blocking shipment by plant and SKU."),
                app("Trade ROI Analytics", "Promotion lift", "market", "Scan data and accruals reconciled to incremental volume and margin by retailer event."),
            ],
            [
                uc("Recall Readiness", "Traceability", "gauge", "Lot genealogy and distribution lists produced in minutes, not days, when a supplier alert arrives."),
                uc("Demand Forecasting", "Planning", "sheet", "SKU-location forecasts that blend syndicated POS, promotions and plant capacity constraints."),
                uc("Line Yield Optimisation", "Manufacturing", "iot", "Scrap and giveaway reduced by correlating filler drift, changeover time and operator crew."),
                uc("Cold Chain Integrity", "Logistics", "stream", "Temperature excursions predicted and rerouted before product quality is compromised."),
                uc("Trade Promotion ROI", "Commercial", "market", "Which promotions paid for themselves in incremental volume versus cannibalised base."),
                uc("Allergen Control", "Food safety", "gavel", "Cross-contact risk flagged from scheduling, cleaning records and shared equipment genealogy."),
                uc("Shelf-Life Optimisation", "Quality", "product", "FEFO allocation scored against remaining shelf life and customer distance."),
                uc("Co-pack Visibility", "Network", "partner", "Third-party production status and inventory reconciled without manual spreadsheet chases."),
                uc("OEE & Downtime", "Operations", "chart", "Top loss categories by line and shift with root cause tied to MES reason codes."),
                uc("Sustainable Sourcing", "ESG", "globe", "Ingredient provenance and carbon intensity traced from farm through finished goods."),
            ],
        ),
        "sources": {
            "rockwell-ft": {"t": "Rockwell FactoryTalk", "u": "https://www.rockwellautomation.com/en-us/products/software/factorytalk.html"},
            "siemens-opcenter": {"t": "Siemens Opcenter MES", "u": "https://plm.sw.siemens.com/en-US/opcenter/execution/"},
            "sap-s4": {"t": "SAP S/4HANA", "u": "https://www.sap.com/products/erp/s4hana.html"},
            "veeva-quality": {"t": "Veeva QualityDocs", "u": "https://www.veeva.com/products/qualitydocs/"},
            "safetychain": {"t": "SafetyChain plant management", "u": "https://safetychain.com/"},
            "blue-yonder": {"t": "Blue Yonder transportation management", "u": "https://blueyonder.com/solutions/transportation-management"},
            "manhattan-wms": {"t": "Manhattan Active Warehouse Management", "u": "https://www.manh.com/solutions/warehouse-management"},
            "sensitech": {"t": "Sensitech TempTale", "u": "https://www.sensitech.com/en/solutions/"},
            "nielseniq": {"t": "NielsenIQ retail measurement", "u": "https://nielseniq.com/global/en/solutions/"},
            "circana": {"t": "Circana market measurement", "u": "https://www.circana.com/"},
            "gs1-epcis": {"t": "GS1 EPCIS standard", "u": "https://www.gs1.org/standards/epcis"},
            "fsma-204": {"t": "FDA FSMA Rule 204", "u": "https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-requirements-additional-traceability-records-certain-foods"}
        },
    },
}
