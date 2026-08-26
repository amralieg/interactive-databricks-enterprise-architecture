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


INDUSTRIES_BATCH_AGRICULTURE = {
    'agriculture': {
        "label": "Agriculture",
        "blurb": "Farm operations, crop planning, input supply, commodity trading, and sustainability reporting across grower networks and co-ops.",
        "medallion": medallion(
            "Raw field and market feeds",
            "Telemetry from equipment, weather stations, satellite imagery and exchange ticks, landed exactly as received so a yield estimate can be replayed.",
            "Conformed fields and assets",
            "Fields, parcels, equipment and contracts resolved into single entities across FMIS, ERP and trading systems.",
            "Yield, margin and carbon",
            "Contracted products agronomy and finance run on: yield per acre, input cost per bushel, basis and carbon intensity scores.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Farm Management",
                    "ic": "sheet",
                    "tiles": [
                        tile("John Deere Operations Center", "iot", "Machine telemetry, as-applied maps and field boundaries from connected equipment.", "john-deere"),
                        tile("Climate FieldView", "iot", "Planting, spraying and harvest layers with hybrid performance by field.", "climate-fieldview"),
                        tile("Granular FMIS", "sheet", "Field plans, input applications and profitability by acre.", "granular"),
                    ],
                },
                {
                    "box": "ERP & Supply Chain",
                    "ic": "erp",
                    "tiles": [
                        tile("SAP S/4HANA Agribusiness", "erp", "Grain contracts, settlements and inventory across elevators and processing.", "sap-agri"),
                        tile("Oracle Food & Beverage", "erp", "Procurement, production and lot traceability for processors.", "oracle-fb"),
                        tile("Bushel ERP", "erp", "Co-op accounting, patronage and grain accounting.", "bushel"),
                    ],
                },
                {
                    "box": "Commodity Markets",
                    "ic": "market",
                    "tiles": [
                        tile("CME Group Futures", "market", "Corn, soybean and wheat futures, options and settlement prices.", "cme"),
                        tile("DTN Prophet", "market", "Cash bids, basis and local elevator prices by location.", "dtn"),
                        tile("Barchart cmdty", "chart", "Historical cash and futures curves for hedging analysis.", "barchart"),
                    ],
                },
                {
                    "box": "Weather & Imagery",
                    "ic": "stream",
                    "tiles": [
                        tile("DTN Weather", "stream", "Hyperlocal forecasts, growing degree days and spray windows.", "dtn-weather"),
                        tile("Planet Labs Imagery", "iot", "Daily satellite NDVI and change detection by parcel.", "planet"),
                        tile("Sentinel Hub", "globe", "Copernicus optical and radar scenes for crop condition.", "sentinel"),
                    ],
                },
                {
                    "box": "Sustainability",
                    "ic": "gavel",
                    "tiles": [
                        tile("Regrow MRV", "gavel", "Practice verification and carbon quantification for regenerative programs.", "regrow"),
                        tile("Indigo Carbon", "partner", "Carbon credit issuance and soil carbon sampling workflows.", "indigo"),
                    ],
                },
                fed_group("Legacy Co-op Mart", "Patronage and historical elevator marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("USDA NASS QuickStats", "api", "County yield, acreage and production statistics ingested for benchmarking.", "usda-nass"),
                tile("USDA RMA Crop Insurance", "gavel", "Policy, acreage and indemnity files for risk programs.", "usda-rma"),
                tile("AgGateway ADAPT", "zplug", "Standardized machine and application data from mixed OEM fleets.", "aggateway"),
            ]),
            "ppl": ppl2([
                biz("Co-op Executive Board", "Genie One",
                    "The CEO on margin per bushel and land strategy; the COO on harvest logistics, elevator throughput and cost per acre.",
                    [["Genie One", "Ask what last harvest cost per acre without analyst delay."], ["AI/BI", "Margin and yield on certified Metric Views."], ["Unity Catalog", "One bushel definition across operations and finance."]]),
                biz("Agronomy", "AI/BI",
                    "Hybrid selection, variable-rate prescriptions and scouting priorities, judged on yield per acre, input cost per bushel and nitrogen use.",
                    [["Prescription Workbench", "VR seed and nitrogen plans by productivity zone."], ["AI/BI", "Yield response curves on governed trial data."]]),
                biz("Grain Merchandising", "Model Serving",
                    "Basis trading, hedging and origination against futures and local bids, managed on position, basis exposure and hedge P&L.",
                    [["Merchandising Desk", "Position and basis exposure by location."], ["Model Serving", "Basis forecast models in the pricing path."]]),
                biz("Sustainability", "Lakehouse//RT",
                    "Carbon programs, practice verification and Scope 3 reporting, tracked on carbon intensity, enrolled acres and credits issued per grower.",
                    [["Carbon Registry", "Issuance pipeline and practice compliance by grower."], ["Lakehouse//RT", "Practice events at operational latency."]]),
                biz("Finance & Risk", "AI/BI",
                    "Patronage, crop insurance and counterparty exposure, watching patronage pools, indemnity exposure and off-margin contracts.",
                    [["AI/BI", "Patronage and hedge P&L on certified views."], ["Genie One", "Ask which contracts are off-margin this week."]]),
            ], [
                biz("Data Engineers", "Lakeflow",
                    "Land equipment telemetry, satellite imagery, FMIS field plans and exchange ticks; own Bronze to Silver and the pager when the basis and yield tables stall.",
                    [["Lakeflow Connect", "Managed connectors for FMIS, ERP and commodity-market sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on machine and imagery feeds."], ["Lakewatch", "Freshness on the basis and yield tables merchandisers read at open."]]),
                biz("Data Scientists", "MLflow",
                    "Yield-forecast, basis and soil-carbon quantification models built from imagery and trial data, and whether they still hold across a shifting season.",
                    [["Feature Store", "Field and weather features read identically in training and serving."], ["MLflow", "Every yield and basis model tracked for audit and reproduction."], ["Model Serving", "Basis and yield models scored in the pricing and prescription path."]]),
                biz("App Developers", "Apps",
                    "Ship the harvest command, prescription workbench and carbon registry apps agronomy and merchandising work in, hosted next to governed field data.",
                    [["Apps", "Operational screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for prescription and contract state."], ["Agent Bricks", "Agents that draft prescriptions and offers against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Grower and elevator dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for basis and yield questions in the merchandising channel."),
                    tile("Notebooks & IDEs", "notebook", "Agronomy notebooks against governed field and trial data."),
                ]},
                {"box": "Grower & Retail", "ic": "partner", "tiles": [
                    tile("Deere Ops Center API", "api", "Prescriptions and harvest summaries shared back to grower accounts.", "john-deere"),
                    tile("FieldView Plus", "partner", "Field layers and recommendations delivered to farmer subscriptions.", "climate-fieldview"),
                    tile("Retail Input Portal", "product", "Seed and chemical orders tied to field-level plans."),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("VR Prescription Export", "iot", "Variable-rate files pushed to applicators before the window closes."),
                    tile("Contract Offers", "market", "Origination offers written to grower CRM at target basis.", "bushel"),
                    tile("Elevator Receiving", "stream", "Scale tickets and moisture discounts flowing to settlement."),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("USDA Reporting", "gavel", "Production and stocks reports filed from governed inventory.", "usda-nass"),
                    tile("Sustainability Disclosures", "share", "Carbon and water metrics shared to food company buyers."),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Yield and sustainability products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Food companies and lenders reading live tables via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Harvest Command", "Season operations", "gauge", "Live harvest progress, elevator queues and dryer capacity across the network."),
             app("Prescription Workbench", "Variable-rate plans", "iot", "Seed, nitrogen and chemical prescriptions by productivity zone before application."),
             app("Merchandising Desk", "Basis and hedges", "market", "Position, basis and hedge effectiveness by location and crop."),
             app("Carbon Registry", "MRV pipeline", "gavel", "Practice enrollment, verification status and credit issuance by grower.")],
            [uc("Yield Forecasting", "Production", "chart", "In-season yield estimates from imagery, weather and hybrid response."),
             uc("Variable-Rate Prescriptions", "Agronomy", "iot", "Input rates optimized by zone rather than flat application."),
             uc("Basis Trading", "Merchandising", "market", "Local basis positions managed against futures and storage."),
             uc("Harvest Logistics", "Operations", "stream", "Truck routing and elevator scheduling to minimize wait and shrink."),
             uc("Crop Insurance Analytics", "Risk", "gavel", "Acreage and indemnity exposure modeled before planting decisions."),
             uc("Carbon MRV", "Sustainability", "partner", "Practice verification and quantification for credit programs."),
             uc("Supply Chain Traceability", "Traceability", "product", "Lot lineage from field through elevator to customer."),
             uc("Input Cost Optimization", "Finance", "erp", "Seed and chemical spend per bushel against plan."),
             uc("Weather Risk Alerts", "Risk", "stream", "Frost, drought and spray window alerts pushed to operations."),
             uc("Patronage Planning", "Finance", "chart", "Patronage pools modeled before fiscal close.")],
        ),
        "sources": {
            "john-deere": {"t": "John Deere Operations Center", "u": "https://www.deere.com/en/technology-products/precision-ag-technology/operations-center/"},
            "climate-fieldview": {"t": "Climate FieldView", "u": "https://www.climate.com/"},
            "granular": {"t": "Granular", "u": "https://granular.ag/"},
            "sap-agri": {"t": "SAP Agribusiness", "u": "https://www.sap.com/industries/agribusiness.html"},
            "oracle-fb": {"t": "Oracle Food and Beverage", "u": "https://www.oracle.com/food-beverage/"},
            "bushel": {"t": "Bushel", "u": "https://bushelpowered.com/"},
            "cme": {"t": "CME Group", "u": "https://www.cmegroup.com/markets/agriculture.html"},
            "dtn": {"t": "DTN", "u": "https://www.dtn.com/"},
            "barchart": {"t": "Barchart", "u": "https://www.barchart.com/cmdty"},
            "dtn-weather": {"t": "DTN Weather", "u": "https://www.dtn.com/weather/"},
            "planet": {"t": "Planet Labs", "u": "https://www.planet.com/"},
            "sentinel": {"t": "Sentinel Hub", "u": "https://www.sentinel-hub.com/"},
            "regrow": {"t": "Regrow", "u": "https://www.regrow.ag/"},
            "indigo": {"t": "Indigo Ag", "u": "https://www.indigoag.com/"},
            "usda-nass": {"t": "USDA NASS", "u": "https://quickstats.nass.usda.gov/"},
            "usda-rma": {"t": "USDA RMA", "u": "https://www.rma.usda.gov/"},
            "aggateway": {"t": "AgGateway ADAPT", "u": "https://www.aggateway.org/"},
        },
    },
}
