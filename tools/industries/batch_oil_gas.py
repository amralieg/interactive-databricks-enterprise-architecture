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


INDUSTRIES_BATCH_OIL_GAS = {
    'oil_gas': {
        "label": "Oil & Gas",
        "blurb": "Upstream production, midstream logistics and downstream refining: reservoir and facility telemetry, trading, and regulatory emissions reporting.",
        "medallion": medallion(
            "Raw field and market",
            "SCADA tags, well test results, LIMS assays, pipeline SCADA and deal capture tickets, landed exactly as received so a barrel or a pressure reading can always be replayed as it stood.",
            "Conformed well, cargo",
            "Wells, facilities, pipelines and cargoes resolved into single conformed entities across production, operations and commercial systems, with allocation balances reconciled and nomination schedules stitched to one logistics record.",
            "Production, margin, loss",
            "Contracted products operations and trading run on: net production and uptime, unit lifting cost, crack spread margin and hydrocarbon loss rates.",
        ),
        "rails": {
            "src": [
                {"box": "Production & SCADA", "ic": "iot", "tiles": [
                        tile("AVEVA PI System", "iot", "Separator pressures, flow rates and compressor tags from upstream and midstream historians.", "aveva-pi"),
                        tile("Schlumberger OFM", "stream", "Well tests, decline curves and reservoir models the subsurface team updates.", "slb-ofm"),
                        tile("Honeywell Experion", "gauge", "DCS alarms, setpoints and batch sequences from refining units.", "honeywell-exp"),
                    ]},
                {"box": "Midstream & Logistics", "ic": "stream", "tiles": [
                        tile("Quorum PGAS", "erp", "Pipeline nominations, allocations and imbalance statements.", "quorum-pgas"),
                        tile("OpenText VIM", "sheet", "Vessel scheduling, terminal inventory and marine demurrage events.", "opentext-vim"),
                        tile("Kpler Cargo Tracking", "globe", "Tanker positions, port calls and cargo lineage for export marketing.", "kpler"),
                    ]},
                {"box": "Commercial & Trading", "ic": "market", "tiles": [
                        tile("ION Openlink Endur", "market", "Physical deals, hedges and MtM for crude and products desks.", "ion-endur"),
                        tile("SAP IS-Oil", "erp", "Joint-venture allocations, production accounting and tax royalty postings.", "sap-is-oil"),
                        tile("Platts Price Assess", "chart", "Benchmark curves and differential indices the marketing desk marks to.", "platts"),
                    ]},
                {"box": "Safety & Environment", "ic": "gavel", "tiles": [
                        tile("Sphera Risk Mgmt", "gavel", "Process safety, MOC and incident investigations tied to facilities.", "sphera"),
                        tile("Enablon EHS", "observ", "Emissions events, flare logs and regulatory permit limits.", "enablon"),
                        tile("FLIR Optical Gas Img", "iot", "Leak detection surveys and repair verification imagery."),
                    ]},
                fed_group("Corporate Treasury Mart", "Hedge effectiveness and working-capital marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("EPA GHGRP Templates", "gavel", "Greenhouse gas reporting layouts validated on ingest before filing windows.", "epa-ghgrp"),
                tile("AIS Vessel Tracks", "globe", "Marine AIS positions normalised for demurrage and cargo reconciliation.", "kpler"),
                tile("Weather & Ocean Data", "stream", "Storm and swell feeds for offshore production and marine scheduling."),
            ]),
            "ppl": ppl_rail2([
                biz("Corporate & Asset Leaders", "Genie One", "The CEO on net production and cash margin; the CFO on hedge exposure and unit lifting cost when crude and product benchmarks move.", [["Genie One", "Ask what yesterday's net production was by asset without waiting on operations reporting."], ["AI/BI", "Production, cost and margin on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"production\" means one thing across SCADA and accounting."]]),
                biz("Upstream Operations", "Lakehouse//RT", "Field superintendents on well uptime, deferment volume and artificial lift when alarms spike, protecting net production and hydrocarbon loss rate.", [["Production Control", "Deferment pareto and well ranking before the morning call."], ["Lakehouse//RT", "Live SCADA state at the latency a trip occurs at."], ["AI/BI", "Uptime and loss on governed definitions."]]),
                biz("Midstream & Terminals", "AI/BI", "Pipeline controllers on nominations, linepack and imbalance when schedules slip, watching hydrocarbon loss and marine demurrage exposure.", [["Logistics Console", "Cargo and linepack positions before nomination deadlines."], ["AI/BI", "Loss and imbalance on certified Metric Views."], ["Genie One", "Ask which terminal is constraining export this week."]]),
                biz("Trading & Marketing", "Model Serving", "Crude and products desks on deal capture, exposure and cargo optimisation, marking physical and paper books to crack-spread margin.", [["Trading Workbench", "Physical and paper positions marked consistently."], ["Model Serving", "Optimisation models scored on live nominations."], ["Unity Catalog", "One cargo definition across ops and finance."]]),
                biz("HSE & Compliance", "Unity Catalog", "Process safety and environmental teams on emissions, permits and incident trends, tracked on TRIR and flare volumes before regulator inspections.", [["HSE Dashboard", "Flare and leak trends before regulator inspections."], ["Unity Catalog", "Lineage from sensor to regulatory filing."], ["AI/BI", "TRIR and emissions on governed definitions."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the SCADA, well test, LIMS assay and deal-capture feeds; own the Bronze to Silver path and the pager when a field pipeline breaks.", [["Lakeflow Connect", "Managed connectors for historian, ETRM and accounting sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on SCADA and allocation feeds."], ["Lakewatch", "Freshness on the production and margin tables operations reads."]]),
                biz("Data Scientists", "MLflow", "Well-decline, facility-uptime, cargo-optimisation and leak-detection models, and whether they still hold six months after deployment across assets.", [["Feature Store", "Historian and test features read identically in training and serving."], ["MLflow", "Every decline and uptime run tracked for audit and reproduction."], ["Model Serving", "Optimisation and failure models scored in the operational path."]]),
                biz("App Developers", "Apps", "Ship the production control, logistics and trading applications field and desk teams work in, hosted next to governed asset data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for nomination state and governed writes."], ["Agent Bricks", "Agents that draft a deferment response against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                        tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                        tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and field updates in the channel operations already works in (Beta)."),
                        tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code."),
                    ]},
                {"box": "Operations Writeback", "ic": "opdb", "tiles": [
                        tile("DCS Setpoint Push", "stream", "Approved operating targets written back within safe envelopes.", "honeywell-exp"),
                        tile("Nomination Updates", "erp", "Revised pipeline and vessel nominations posted before gate close.", "quorum-pgas"),
                        tile("Work Permit System", "gavel", "Maintenance permits raised from predicted equipment risk.", "sphera"),
                    ]},
                {"box": "Customers & Partners", "ic": "partner", "tiles": [
                        tile("Cargo Assay API", "api", "Quality certificates served to traders and refiners from governed lab lineage.", "slb-ofm"),
                        tile("JV Partner Sharing", "share", "Production and cost allocations shared to non-operated partners over Delta Sharing.", "sap-is-oil"),
                        tile("Terminal Operator Feed", "globe", "Inventory positions exchanged without nightly spreadsheet reconciliation.", "opentext-vim"),
                    ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                        tile("GHG & Emissions Filing", "gavel", "Regulatory greenhouse submissions produced from governed sensor and flare data.", "epa-ghgrp"),
                        tile("Production Tax Royalty", "share", "Royalty and severance filings from contracted Gold products.", "enablon"),
                    ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                        tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                        tile("Sharing Recipients", "share", "JV partners, regulators and traders reading live tables with no copy."),
                    ]},
            ]),
        },
        "top": top_band(
            [
                app("Production Control", "Deferment live", "gauge", "Well uptime, deferment pareto and lift setpoints on Databricks Apps over Lakebase."),
                app("Logistics Console", "Cargo schedule", "globe", "Nominations, linepack and vessel positions before export windows close."),
                app("Trading Workbench", "Exposure view", "market", "Physical and paper positions marked to benchmark on one surface."),
                app("HSE Dashboard", "Emissions live", "gavel", "Flare, leak and permit exceedances before inspections and board review."),
            ],
            [
                uc("Well Performance", "Upstream", "iot", "Decline and artificial-lift optimisation when downhole conditions shift."),
                uc("Facility Uptime", "Reliability", "gauge", "Compressor and separator trips predicted before production is deferred."),
                uc("Pipeline Optimisation", "Midstream", "stream", "Linepack and nomination schedules tuned to minimise imbalance penalties."),
                uc("Cargo Scheduling", "Logistics", "globe", "Vessel and terminal slots aligned to production and demurrage exposure."),
                uc("Trading Optimisation", "Commercial", "market", "Physical and hedge books reconciled before exposure limits breach."),
                uc("Leak Detection", "HSE", "observ", "Optical gas imaging and sensor anomalies triaged to repair work orders."),
                uc("Emissions Reporting", "Regulatory", "gavel", "Flare and vent volumes filed from governed historian lineage."),
                uc("Reserves Reconciliation", "Subsurface", "sheet", "Production and test data reconciled to reservoir models for booking."),
                uc("Corrosion Monitoring", "Integrity", "stream", "Thickness and coupon data scored against inspection intervals."),
                uc("JV Allocation", "Finance", "erp", "Joint-venture splits validated before partner statements post."),
            ],
        ),
        "sources": {
            "aveva-pi": {"t": "AVEVA PI System", "u": "https://www.aveva.com/en/products/pi-system/"},
            "slb-ofm": {"t": "Schlumberger OFM", "u": "https://www.slb.com/"},
            "honeywell-exp": {"t": "Honeywell Experion PKS", "u": "https://process.honeywell.com/us/en/products/control-and-supervision/experion-pks"},
            "quorum-pgas": {"t": "Quorum PGAS", "u": "https://www.quorumsoftware.com/solutions/midstream/"},
            "opentext-vim": {"t": "OpenText Vessel Information Management", "u": "https://www.opentext.com/products/vessel-information-management"},
            "kpler": {"t": "Kpler", "u": "https://www.kpler.com/"},
            "ion-endur": {"t": "ION Openlink Endur", "u": "https://iongroup.com/commodities/"},
            "sap-is-oil": {"t": "SAP IS-Oil", "u": "https://www.sap.com/industries/oil-gas.html"},
            "platts": {"t": "S&P Global Platts", "u": "https://www.spglobal.com/commodityinsights/en/products-services/energy"},
            "sphera": {"t": "Sphera risk management", "u": "https://sphera.com/operational-risk-management-software/"},
            "enablon": {"t": "Wolters Kluwer Enablon", "u": "https://www.wolterskluwer.com/en/solutions/enablon"},
            "epa-ghgrp": {"t": "EPA GHGRP", "u": "https://www.epa.gov/ghgreporting"},
        },
    },
}
