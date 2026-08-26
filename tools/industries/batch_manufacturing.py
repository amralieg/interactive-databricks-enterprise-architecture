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


INDUSTRIES_BATCH_MANUFACTURING = {
    'manufacturing': {
        "label": "Manufacturing",
        "blurb": "Discrete and process manufacturing: ERP and MES shop-floor execution, quality and traceability, supply chain planning, and asset maintenance.",
        "medallion": medallion(
            "Raw plant feeds",
            "ERP production orders, MES cycle and downtime events, SCADA historian tags, quality inspection results and supplier ASNs, landed exactly as received so a lot or a downtime code can always be replayed as it stood.",
            "Conformed order, lot",
            "Work orders, lots, equipment and materials resolved into single conformed entities across ERP, MES and quality estates, with serial and batch genealogy reconciled and multi-site BOM revisions stitched to one product definition.",
            "OEE, yield, OTIF",
            "Contracted products operations and supply chain leaders run on: overall equipment effectiveness by line, first-pass yield and scrap, on-time-in-full to customer promise, and maintenance cost per unit produced.",
        ),
        "rails": {
            "src": [
                {"box": "ERP & Planning", "ic": "erp", "tiles": [
                        tile("SAP S/4HANA", "erp", "Manufacturing orders, BOMs, routings, inventory and financial postings. The system of record for what was planned to be made and what was consumed.", "sap-s4"),
                        tile("Oracle SCM Cloud", "erp", "Supply planning, work definitions and costed transactions for plants on the Oracle manufacturing estate.", "oracle-scm"),
                        tile("Kinaxis Maestro", "sheet", "Concurrent S&OP scenarios, constraint-based planning and what-if responses when a supplier or line goes down.", "kinaxis"),
                    ]},
                {"box": "MES & Shop Floor", "ic": "stream", "tiles": [
                        tile("Siemens Opcenter", "stream", "Work instructions, cycle counts, downtime reason codes and WIP status from the MES the operators work in.", "opcenter"),
                        tile("Rockwell FactoryTalk", "iot", "Line state, OEE counters and recipe execution from Allen-Bradley controlled assets.", "factorytalk"),
                        tile("AVEVA MES", "db", "Batch records, electronic batch tickets and equipment logbooks for process manufacturing sites.", "aveva-mes"),
                    ]},
                {"box": "Quality & PLM", "ic": "gavel", "tiles": [
                        tile("PTC Windchill", "product", "Engineering BOMs, change orders and approved drawings the shop floor must build to.", "windchill"),
                        tile("MasterControl QMS", "gavel", "Non-conformance, CAPA and audit findings tied to lots and suppliers.", "mastercontrol"),
                        tile("ETQ Reliance", "gavel", "Inspection plans, SPC results and supplier quality scorecards for regulated industries.", "etq"),
                    ]},
                {"box": "IoT & Historians", "ic": "iot", "tiles": [
                        tile("AVEVA PI System", "iot", "High-frequency sensor and actuator tags from lines, utilities and environmental systems.", "aveva-pi"),
                        tile("AspenTech IP.21", "stream", "Process historian data for batch analytics, energy intensity and abnormal event detection.", "aspen-ip21"),
                        tile("Machine Vision QC", "observ", "Inline defect images and measurement vectors joined to lot and serial for root-cause analysis."),
                    ]},
                fed_group("Corporate Data Warehouse", "Finance and HR marts left where they are and queried in place under Unity Catalog, avoiding a second copy of audited cost allocations."),
            ],
            "ing": ing_rail([
                tile("OPC-UA Plant Gateway", "iot", "Shop-floor protocol bridges normalising PLC and robot telemetry on ingest before historian landing.", "opc-ua"),
                tile("EDI ASN / DESADV", "api", "Supplier advance ship notices and delivery confirmations parsed into structured receipt events.", "edi-asn"),
                tile("GS1 EPCIS Events", "stream", "Serialised product movement events for track-and-trace across plants, DCs and customers.", "gs1-epcis"),
            ]),
            "ppl": ppl_rail2([
                biz("Plant Leadership", "Genie One", "The plant manager and VP operations on OEE by line, cost per unit produced and OTIF service level when a line stalls or a key supplier slips.", [["Genie One", "Ask what yesterday's scrap cost or which customer orders are at risk without waiting on manufacturing IT."], ["AI/BI", "OEE, yield and OTIF on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"downtime\" means one thing across plants."]]),
                biz("Production & Scheduling", "AI/BI", "Finite scheduling, changeover sequencing and labour loading against orders commercial already promised, watched on schedule adherence and WIP ageing.", [["Production Scheduler", "Sequence and changeover plans scored before the shift board posts."], ["AI/BI", "Schedule adherence and WIP ageing on governed definitions."], ["Lakehouse//RT", "Live line state at the latency a bottleneck moves at."]]),
                biz("Quality & Compliance", "Model Serving", "Lot release, SPC violations and supplier corrective actions scored on first-pass yield and non-conformance rate before product leaves the site.", [["Quality Cockpit", "Hold and release decisions with genealogy back to supplier lot."], ["Model Serving", "Defect and drift models scored on inline vision and SPC signals."], ["Unity Catalog", "One definition of non-conformance across MES and QMS."]]),
                biz("Supply Chain", "AI/BI", "S&OP, inventory positioning and supplier OTIF when lead times stretch, balancing inventory turns against the customer service level finance commits.", [["Supply Control Tower", "Shortages and expedites costed across alternate BOMs and sites."], ["AI/BI", "Inventory turns and supplier OTIF on certified Metric Views."], ["Genie One", "Ask which SKUs will stock out before the next planning cycle."]]),
                biz("Maintenance & Reliability", "Lakeflow", "Planned downtime, spare parts and technician capacity tracked on MTBF and maintenance cost per unit so failures become scheduled work not line stops.", [["Maintenance Hub", "Work orders raised from predicted failures before the line stops."], ["Lakeflow", "Historian and CMMS feeds conformed for reliability analytics."], ["MLflow", "Remaining-useful-life models tracked for audit and reproduction."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the ERP order, MES cycle, SCADA historian and supplier ASN feeds; own the Bronze to Silver path and the pager when a plant pipeline breaks.", [["Lakeflow Connect", "Managed connectors for SAP, Opcenter MES and quality sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on downtime and inspection feeds."], ["Lakewatch", "Freshness on the OEE and inventory tables the shift board reads each morning."]]),
                biz("Data Scientists", "MLflow", "First-pass yield, remaining-useful-life, demand and defect-vision models, and whether they still hold six months after deployment on the floor.", [["Feature Store", "Historian and SPC features read identically in training and serving."], ["MLflow", "Every yield and RUL run tracked for audit and reproduction."], ["Model Serving", "Defect and failure models scored on inline vision and SPC signals."]]),
                biz("App Developers", "Apps", "Ship the plant performance, quality cockpit and maintenance applications operators and planners work in, hosted next to governed shop-floor data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for work-order state and governed writes."], ["Agent Bricks", "Agents that draft a maintenance work order against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                        tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                        tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse and floor andon updates in the channel the plant already works in (Beta)."),
                        tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code."),
                    ]},
                {"box": "Plant & ERP", "ic": "opdb", "tiles": [
                        tile("SAP Order Confirmation", "db", "Production confirmations and component backflush written back into ERP so finance sees reality.", "sap-s4"),
                        tile("MES Recipe Download", "stream", "Approved recipes and work instructions pushed to lines after engineering change release.", "opcenter"),
                        tile("CMMS Work Orders", "erp", "Predicted failures raised as maintenance work orders the technician crew already schedules."),
                    ]},
                {"box": "Customers & Suppliers", "ic": "partner", "tiles": [
                        tile("Customer ASN Portal", "api", "Shipment and lot certificates served to OEM customers from governed genealogy rather than emailed spreadsheets.", "gs1-epcis"),
                        tile("Supplier Scorecards", "share", "OTIF and quality metrics shared to tier-one suppliers over Delta Sharing.", "edi-asn"),
                        tile("Contract Manufacturer", "globe", "Co-man sites reading BOM and quality limits live instead of nightly flat files."),
                    ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                        tile("FDA / ISO Lot Trace", "gavel", "Lot genealogy and deviation records produced from the same governed tables production runs on.", "mastercontrol"),
                        tile("Carbon & ESG Reporting", "share", "Scope 1 and 2 intensity filed from contracted Gold products for buyer sustainability programs."),
                    ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                        tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                        tile("Sharing Recipients", "share", "Customers, co-mans and auditors reading live tables with no copy and no egress duplication."),
                    ]},
            ]),
        },
        "top": top_band(
            [
                app("Plant Performance", "Live OEE", "gauge", "The screen the shift supervisor runs the day from: downtime pareto, scrap by reason and orders at risk, on Databricks Apps over Lakebase."),
                app("Quality Cockpit", "Hold and release", "gavel", "Lot status, SPC violations and supplier genealogy on one surface before product ships."),
                app("Supply Control Tower", "Shortage response", "sheet", "Component shortages and alternate sourcing costed before customer OTIF is missed."),
                app("Maintenance Hub", "Asset health", "iot", "Predicted failures and spare parts by line so downtime becomes a planned window."),
            ],
            [
                uc("Predictive Maintenance", "Reliability", "iot", "Component failure predicted from historian and vibration signals before the line stops."),
                uc("OEE & Downtime", "Throughput", "gauge", "Loss buckets by line and shift attacked with pareto evidence rather than anecdote."),
                uc("S&OP / IBP", "Planning", "sheet", "Demand, supply and inventory balanced when a plant or supplier goes offline mid-quarter."),
                uc("Genealogy & Recall", "Traceability", "product", "Every serial traced from supplier lot through WIP to customer shipment in minutes not days."),
                uc("Yield Optimisation", "Scrap reduction", "chart", "Recipe and parameter sets scored on first-pass yield using historian and quality history."),
                uc("Energy Intensity", "Sustainability", "stream", "kWh per unit by line and product for carbon reporting and cost reduction."),
                uc("Supplier Risk", "Resilience", "partner", "Single-source and geographic concentration surfaced before a port or plant disruption."),
                uc("Digital Work Instructions", "Quality", "notebook", "Operator guidance version-controlled and joined to defect outcomes by step."),
                uc("Inventory Optimisation", "Working capital", "market", "Safety stock and reorder points tuned to actual lead-time variability not policy tables."),
                uc("New Product Intro", "NPI", "product", "Pilot builds scored on ramp yield and cost before volume cut-over."),
            ],
        ),
        "sources": {
            "sap-s4": {"t": "SAP S/4HANA", "u": "https://www.sap.com/products/erp/s4hana.html"},
            "oracle-scm": {"t": "Oracle SCM Cloud", "u": "https://www.oracle.com/scm/manufacturing/"},
            "kinaxis": {"t": "Kinaxis Maestro", "u": "https://www.kinaxis.com/"},
            "opcenter": {"t": "Siemens Opcenter MES", "u": "https://plm.sw.siemens.com/en-US/opcenter/"},
            "factorytalk": {"t": "Rockwell FactoryTalk", "u": "https://www.rockwellautomation.com/en-us/products/software/factorytalk.html"},
            "aveva-mes": {"t": "AVEVA MES", "u": "https://www.aveva.com/en/products/manufacturing-execution-system/"},
            "windchill": {"t": "PTC Windchill", "u": "https://www.ptc.com/en/products/windchill"},
            "mastercontrol": {"t": "MasterControl QMS", "u": "https://www.mastercontrol.com/"},
            "etq": {"t": "ETQ Reliance", "u": "https://www.etq.com/"},
            "aveva-pi": {"t": "AVEVA PI System", "u": "https://www.aveva.com/en/products/pi-system/"},
            "aspen-ip21": {"t": "AspenTech IP.21", "u": "https://www.aspentech.com/en/products/ip21"},
            "opc-ua": {"t": "OPC Unified Architecture", "u": "https://opcfoundation.org/about/opc-technologies/opc-ua/"},
            "edi-asn": {"t": "GS1 EDI DESADV", "u": "https://www.gs1.org/standards/edi"},
            "gs1-epcis": {"t": "GS1 EPCIS", "u": "https://www.gs1.org/standards/epcis"},
        },
    },
}
