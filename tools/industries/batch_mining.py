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


INDUSTRIES_BATCH_MINING = {
    'mining': {
        "label": "Mining",
        "blurb": "Extraction and processing: pit and underground operations, fleet and plant telemetry, grade control, and export logistics for metals and bulk commodities.",
        "medallion": medallion(
            "Raw pit feeds",
            "Fleet dispatch, shovel and truck cycles, plant SCADA tags, lab assays and port load events, landed exactly as received so a ton or a grade can always be replayed as it stood.",
            "Conformed block, fleet",
            "Blocks, benches, equipment and shipments resolved into single conformed entities across dispatch, plant and commercial systems, with sample IDs reconciled and stockpile movements stitched to one inventory position.",
            "Grade, cost, recovery",
            "Contracted products operations and commercial teams run on: recovered metal per tonne milled, unit cash cost, fleet productivity and port demurrage exposure by cargo.",
        ),
        "rails": {
            "src": [
                {"box": "Fleet & Dispatch", "ic": "iot", "tiles": [
                        tile("Modular Mining DISPATCH", "iot", "Shovel-truck assignment, queue times and payload cycles from the open-pit dispatch system.", "modular"),
                        tile("Hexagon MineOperate", "stream", "Underground and surface fleet location, production reporting and operator logs.", "hexagon"),
                        tile("Maptek BlastLogic", "sheet", "Drill and blast designs, actuals and fragmentation linked to dig blocks.", "maptek"),
                    ]},
                {"box": "Plant & Processing", "ic": "stream", "tiles": [
                        tile("AVEVA PI System", "iot", "Mill throughput, reagent flows and recovery tags from concentrator historians.", "aveva-pi"),
                        tile("Metso PlantPerf", "gauge", "Crusher, mill and flotation KPIs against nameplate and maintenance windows.", "metso"),
                        tile("LIMS Assay Lab", "gavel", "Sample preparation, assay results and QA/QC duplicates for grade control.", "lims"),
                    ]},
                {"box": "Commercial & ERP", "ic": "erp", "tiles": [
                        tile("SAP IS-Mining", "erp", "Production orders, inventory, sales contracts and settlement postings.", "sap-mining"),
                        tile("Metal Bulletin", "market", "Benchmark prices and index curves the marketing desk hedges against.", "metal-bulletin"),
                        tile("Port Community System", "globe", "Vessel nominations, stow plans and weighbridge tickets at export terminals.", "pcs"),
                    ]},
                {"box": "Safety & Environment", "ic": "gavel", "tiles": [
                        tile("Intelex EHS", "gavel", "Incidents, near-misses and permit-to-work records tied to site and crew.", "intelex"),
                        tile("Envirosuite", "observ", "Dust, noise and blast vibration monitoring against community thresholds.", "envirosuite"),
                        tile("Wearable Proximity", "iot", "Tag collision and zone breach events from personnel and equipment proximity systems."),
                    ]},
                fed_group("Corporate Risk Ledger", "Hedging and working-capital marts queried in place under Unity Catalog for treasury reporting."),
            ],
            "ing": ing_rail([
                tile("High-Precision GPS", "iot", "RTK survey and machine guidance files normalised for block model updates.", "hexagon"),
                tile("Satellite Imagery", "globe", "Pit shell and stockpile volumetrics from periodic earth-observation feeds.", "planet"),
                tile("Rail Wagon Telemetry", "stream", "Load, location and brake events from outbound rail convoys to port.", "pcs"),
            ]),
            "ppl": ppl_rail2([
                biz("Site Leadership", "Genie One", "The general manager on tonnes milled, grade recovery and unit cash cost when weather or an unplanned equipment stop limits the month's plan.", [["Genie One", "Ask what yesterday's mill recovery was without waiting on the morning report."], ["AI/BI", "Grade, cost and fleet KPIs on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"head grade\" means one thing across mine and plant."]]),
                biz("Mine Operations", "Lakehouse//RT", "Pit sequencing, dig rates and truck queue times when a shovel goes down, protecting fleet productivity and unit cost per tonne moved.", [["Pit Control Tower", "Fleet reallocation options costed before the shift plan changes."], ["Lakehouse//RT", "Dispatch state at the latency a queue builds at."], ["AI/BI", "Payload and cycle time on governed definitions."]]),
                biz("Processing", "AI/BI", "Mill stability, reagent consumption and recovered metal per tonne milled when feed grade and ore hardness shift through the shift.", [["Plant Performance", "Recovery and throughput variance flagged before metal is lost."], ["Model Serving", "Grade-control models scored on blast and assay feeds."], ["Genie One", "Ask which circuit is constraining recovery today."]]),
                biz("Marketing & Sales", "AI/BI", "Contract delivery, assay disputes and hedge exposure against benchmark moves, tracked on realised price and TC/RC terms by cargo.", [["Shipment Tracker", "Cargo assay and moisture reconciled before invoice."], ["AI/BI", "Realised price and TC/RC on certified Metric Views."], ["Unity Catalog", "One definition of contained metal across mine and port."]]),
                biz("Safety & ESG", "Unity Catalog", "Fatal-risk protocols, Scope 1 emissions and community commitments the board signs, tracked on TRIFR and permit-breach counts before audit.", [["Safety Dashboard", "Leading indicators and permit breaches before audit."], ["Unity Catalog", "Lineage from sensor to regulatory disclosure."], ["AI/BI", "TRIFR and emissions on governed definitions."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the dispatch, plant SCADA, assay lab and port load feeds; own the Bronze to Silver path and the pager when a site pipeline breaks.", [["Lakeflow Connect", "Managed connectors for DISPATCH, historian and LIMS sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on cycle and assay feeds."], ["Lakewatch", "Freshness on the grade and fleet tables the morning report reads."]]),
                biz("Data Scientists", "MLflow", "Grade-control, recovery, haul-truck RUL and demurrage models, and whether they still hold six months after deployment across pit and plant.", [["Feature Store", "Blast and assay features read identically in training and serving."], ["MLflow", "Every grade and recovery run tracked for audit and reproduction."], ["Model Serving", "Grade-control models scored on blast and assay feeds."]]),
                biz("App Developers", "Apps", "Ship the pit control, plant performance and shipment applications operators and marketers work in, hosted next to governed mine data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for dispatch state and governed writes."], ["Agent Bricks", "Agents that draft a fleet reallocation against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                        tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                        tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and shift updates in the channel the pit already works in (Beta)."),
                        tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code."),
                    ]},
                {"box": "Operations Writeback", "ic": "opdb", "tiles": [
                        tile("DISPATCH Reassignment", "iot", "Truck and shovel assignments written back when the optimiser changes the shift plan.", "modular"),
                        tile("Plant Setpoint", "stream", "Approved reagent and density targets pushed to DCS within operating envelopes.", "aveva-pi"),
                        tile("Maintenance Work Order", "erp", "Predicted component failures raised in CMMS before the truck leaves service.", "metso"),
                    ]},
                {"box": "Customers & Port", "ic": "partner", "tiles": [
                        tile("Assay Certificate API", "api", "Cargo certificates served to smelters and traders from governed lab lineage.", "lims"),
                        tile("Trader Data Sharing", "share", "Stockpile and shipment positions shared to offtake partners over Delta Sharing.", "metal-bulletin"),
                        tile("Rail & Port Partners", "globe", "Nomination and stow data exchanged without nightly spreadsheet reconciliation.", "pcs"),
                    ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                        tile("Mine Safety Reporting", "gavel", "Regulator submissions produced from the same governed tables operations runs on.", "intelex"),
                        tile("Emissions & Tailings", "share", "Scope 1 and water disclosures filed from contracted Gold products.", "envirosuite"),
                    ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                        tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                        tile("Sharing Recipients", "share", "Traders, smelters and joint-venture partners reading live tables with no copy."),
                    ]},
            ]),
        },
        "top": top_band(
            [
                app("Pit Control Tower", "Fleet dispatch", "gauge", "Shovel queues, payload variance and reallocation options on Databricks Apps over Lakebase."),
                app("Plant Performance", "Recovery live", "stream", "Mill throughput and recovery against plan with constraint flags before metal is lost."),
                app("Grade Control", "Block model", "sheet", "Blast, dig and assay reconciled for short-term model updates before the shovel moves."),
                app("Shipment Tracker", "Export cargo", "globe", "Port stock, vessel laytime and assay disputes on one surface for marketing."),
            ],
            [
                uc("Grade Control", "Ore body", "sheet", "Short-term model updates from blast, dig and assay before material is misrouted."),
                uc("Fleet Optimisation", "Productivity", "iot", "Truck and shovel matching tuned to queue time and fuel not static rules."),
                uc("Mill Recovery", "Processing", "gauge", "Circuit recovery maximised when feed grade and hardness shift."),
                uc("Predictive Maintenance", "Assets", "stream", "Haul truck and mill failures predicted before they remove capacity from the plan."),
                uc("Stockpile Management", "Blending", "product", "Grade engineering across ROM and product piles to hit contract spec."),
                uc("Export Logistics", "Port", "globe", "Rail and vessel scheduling aligned to production and demurrage exposure."),
                uc("Safety Analytics", "Risk", "gavel", "Leading indicators and proximity events surfaced before a recordable occurs."),
                uc("Energy & Emissions", "ESG", "observ", "Diesel and electricity intensity per tonne for reporting and cost reduction."),
                uc("Mine Planning", "Sequence", "chart", "Pit phases scored on NPV with geotechnical and water constraints explicit."),
                uc("Commodity Hedging", "Treasury", "market", "Physical delivery marked to benchmark with hedge effectiveness in one view."),
            ],
        ),
        "sources": {
            "modular": {"t": "Modular Mining DISPATCH", "u": "https://www.modularmining.com/"},
            "hexagon": {"t": "Hexagon MineOperate", "u": "https://hexagon.com/products/product-groups/mineoperate"},
            "maptek": {"t": "Maptek BlastLogic", "u": "https://www.maptek.com/products/blastlogic/"},
            "aveva-pi": {"t": "AVEVA PI System", "u": "https://www.aveva.com/en/products/pi-system/"},
            "metso": {"t": "Metso PlantPerf", "u": "https://www.metso.com/"},
            "lims": {"t": "Laboratory information management", "u": "https://www.thermofisher.com/us/en/home/digital-solutions/lab-informatics.html"},
            "sap-mining": {"t": "SAP for mining", "u": "https://www.sap.com/industries/mining.html"},
            "metal-bulletin": {"t": "Fastmarkets Metal Bulletin", "u": "https://www.fastmarkets.com/"},
            "pcs": {"t": "Port community systems", "u": "https://ipcsa.international/"},
            "intelex": {"t": "Intelex EHS", "u": "https://www.intelex.com/"},
            "envirosuite": {"t": "Envirosuite", "u": "https://envirosuite.com/"},
            "planet": {"t": "Planet Labs", "u": "https://www.planet.com/"},
        },
    },
}
