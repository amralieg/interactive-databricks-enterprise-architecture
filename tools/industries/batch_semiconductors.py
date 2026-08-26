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


INDUSTRIES_BATCH_SEMICONDUCTORS = {
    'semiconductors': {
        "label": "Semiconductors",
        "blurb": "Fab and foundry operations: wafer manufacturing execution, yield and test analytics, design-to-silicon traceability, and supply chain resilience across the semiconductor value chain.",
        "medallion": medallion(
            "Raw fab and test feeds",
            "SECS/GEM equipment events, MES lot and step history, ATE parametric dumps and WIP snapshots, landed exactly as received so a yield excursion can always be replayed.",
            "Conformed lot, wafer, die",
            "Lots, wafers, dies and equipment resolved into single conformed entities across MES, test and ERP, with die IDs reconciled and rework genealogy stitched to one trace.",
            "Yield, cycle time, OEE",
            "Contracted products engineering runs on: yield and bin pareto by layer and tool, cycle time and WIP ageing, OEE and downtime attribution, and cost per good die.",
        ),
        "rails": {
            "src": [
                {"box": "Fab & MES", "ic": "erp", "tiles": [
                    tile("Applied E3 MES", "erp", "Manufacturing execution for wafer fabs: lot tracking, recipe management, equipment dispatch and hold/release.", "applied-e3"),
                    tile("Camstar Semiconductor", "sheet", "MES routings, BOMs, component traceability and quality holds against each lot.", "camstar"),
                    tile("Brooks PFAB", "db", "Fab automation and material control: carrier tracking, reticle management and tool loading state.", "brooks-pfab"),
                ]},
                {"box": "Design & IP", "ic": "sheet", "tiles": [
                    tile("Synopsys Fusion Design", "sheet", "RTL through sign-off: synthesis, place-and-route and timing closure feeding the tape-out record.", "synopsys-fusion"),
                    tile("Cadence Virtuoso", "code", "Custom and analog design: schematic, layout and LVS for IP blocks on each die.", "cadence-virtuoso"),
                    tile("Siemens Calibre", "gavel", "DRC, LVS and OPC verification against foundry rules before mask order.", "calibre"),
                ]},
                {"box": "Yield & Test", "ic": "iot", "tiles": [
                    tile("Teradyne UltraFLEX", "iot", "ATE parametric and functional test: bin maps, shmoo plots and bin history per die.", "teradyne"),
                    tile("PDF Solutions Exensio", "chart", "Yield management: defect classification, spatial signatures and excursion detection.", "pdf-exensio"),
                    tile("KLA 5D Analyzer", "stream", "Inspection and metrology: defect maps, overlay and CD measurements by tool and recipe.", "kla-5d"),
                ]},
                {"box": "Equipment & Sensors", "ic": "stream", "tiles": [
                    tile("SECS/GEM Tool Interface", "stream", "Equipment events, alarms and trace data from lithography, etch and deposition tools.", "secs-gem"),
                    tile("ASML YieldStar", "iot", "In-line overlay and CD metrology from the scanner feeding litho feedback.", "asml-yieldstar"),
                    tile("Lam Equipment Analytics", "partner", "Chamber health, RF matching and preventive maintenance signals from process tools.", "lam-analytics"),
                ]},
                {"box": "Supply & Materials", "ic": "market", "tiles": [
                    tile("SAP S/4HANA", "erp", "Procurement, inventory and cost accounting for wafers, chemicals and substrates.", "sap-s4"),
                    tile("Resilinc Supply Risk", "globe", "Multi-tier supplier mapping and disruption alerts for critical materials.", "resilinc"),
                ]},
                fed_group("Partner Foundry Marts", "Yield and capacity marts left at the foundry and queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("SEMI E134 Data Collection", "stream", "Industry data collection standard for equipment and MES events parsed on arrival.", "semi-e134"),
                tile("SECS/GEM Message Bus", "api", "Equipment host communication for remote commands, trace reports and alarms.", "secs-gem"),
                tile("OSAT Test File Exchange", "zplug", "STDF parametric files from outsourced assembly and test partners.", "stdf"),
            ]),
            "ppl": ppl2([
                biz("CEO & Fab Strategy", "Genie One", "The CEO on capacity utilisation and margin; the COO on cycle time, yield ramp and the cost of a fab excursion by product and layer.",
                    [["Genie One", "Ask what yesterday's fab output cost without booking analyst time."], ["AI/BI", "Yield, cycle time and OEE on certified Metric Views."], ["Unity Catalog", "Certification so yield means one thing across the enterprise."]]),
                biz("Fab Operations", "Lakehouse//RT", "Fab managers on WIP position, tool availability and lot disposition through each critical layer, defending cycle time and wafer starts.",
                    [["Fab Control Tower", "Live WIP and bottleneck tools on Databricks Apps over Lakebase."], ["Lakehouse//RT", "Equipment and lot state at fab-line latency."]]),
                biz("Yield Engineering", "Model Serving", "Yield engineers on defect pareto, spatial signatures and the designed experiments that recover margin before a lot is dispositioned.",
                    [["Yield Workbench", "Bin maps and excursion history before disposition is signed."], ["Model Serving", "Defect classification and yield prediction on incoming lots."]]),
                biz("Supply Chain", "AI/BI", "Materials planners on substrate lead times, wafer allocation and single-source risk, trading inventory cost against line-down risk.",
                    [["AI/BI", "Inventory, consumption and supplier OTIF on certified Metric Views."], ["Genie One", "Ask which lots are at risk from a supplier delay."]]),
                biz("Quality & Reliability", "Lakeflow", "Quality teams on customer returns, failure-analysis correlation and qualification change controls tied back to the fab lot and test bin.",
                    [["FA Correlation Lab", "Returns tied to fab lot, test bin and assembly trace."], ["Lakeflow", "Test, MES and returns feeds conformed for quality analytics."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land SECS/GEM tool events, MES lot history, ATE parametric dumps and ERP feeds; own Bronze to Silver and the pager when a yield pipeline stalls.",
                    [["Lakeflow Connect", "Managed connectors for MES, ERP and equipment host sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on SECS/GEM and test feeds."], ["Lakewatch", "Freshness on the yield tables engineering reads each shift."]]),
                biz("Data Scientists", "MLflow", "Defect-classification, yield-prediction, chamber-matching and test-optimisation models, and whether they still hold as processes and nodes shift.",
                    [["Feature Store", "Wafer and tool features read identically in training and serving."], ["MLflow", "Every excursion experiment tracked for audit and reproduction."], ["Model Serving", "Defect and yield models scored on incoming lots."]]),
                biz("App Developers", "Apps", "Ship the Fab Control Tower, Yield Workbench and Chamber Match apps engineering runs the line from, hosted next to governed MES and test data.",
                    [["Apps", "Fab screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for hold state and disposition writes."], ["Agent Bricks", "Agents that draft dispositions against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses with Unity Catalog permissions end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and yield alerts in the channel the fab works in."),
                    tile("Notebooks & IDEs", "notebook", "Engineering notebooks against governed MES, test and equipment data."),
                ]},
                {"box": "Distribution & Partners", "ic": "partner", "tiles": [
                    tile("Foundry Partner Portal", "api", "Yield summaries and lot status shared to fabless customers over Delta Sharing."),
                    tile("OSAT & Assembly Partners", "partner", "Test results and ship authorisation read by assembly partners under governed sharing."),
                    tile("Equipment OEM Feeds", "globe", "Chamber matching and maintenance recommendations exchanged with tool vendors.", "secs-gem"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("MES Hold & Release", "db", "Automated hold and release written back into MES for dispatch lists.", "applied-e3"),
                    tile("Recipe & R2R Adjust", "erp", "Run-to-run adjustments pushed to equipment hosts within approved guard bands."),
                    tile("Maintenance Work Orders", "apps", "Predicted tool removals raised as maintenance work orders on technician devices."),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Export & Trade Compliance", "gavel", "Technology node and end-use reporting from governed tables."),
                    tile("Customer Quality Reports", "share", "CoA, reliability and PPAP submissions from contracted Gold products."),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Yield and traceability products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Fabless customers and OSAT partners reading live tables via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Fab Control Tower", "Live WIP state", "gauge", "Fab managers run the line from bottleneck tools, hold queues and lot disposition on Databricks Apps over Lakebase."),
             app("Yield Workbench", "Excursion analysis", "chart", "Yield engineers see bin maps, defect overlays and excursion history before lot disposition."),
             app("Chamber Match Console", "Tool health", "iot", "Chamber matching scores and drift alerts by tool and recipe before yield moves."),
             app("FA Correlation Lab", "Returns trace", "partner", "Customer returns tied to fab lot, test bin and assembly genealogy in one view.")],
            [uc("Yield Excursion Detection", "Fab quality", "chart", "Detecting yield loss by layer, tool and product before wafers complete the route."),
             uc("Chamber Matching", "Equipment", "iot", "Matching chambers across a fleet on process signatures without manual tuning."),
             uc("Cycle Time & WIP", "Operations", "stream", "Cycle time and WIP ageing by route and bottleneck for capacity plans."),
             uc("Defect Classification", "Metrology", "gauge", "Automated defect classification from inspection images feeding disposition rules."),
             uc("Run-to-Run Control", "Process", "erp", "Closed-loop recipe adjustments within guard bands against inline metrology."),
             uc("Predictive Maintenance", "Tool uptime", "iot", "Predicting tool failures from SECS/GEM traces before unplanned downtime."),
             uc("Supply Risk & Allocation", "Materials", "globe", "Multi-tier supplier risk when lead times stretch or a sub-tier fab goes offline."),
             uc("Test Optimization", "Cost per die", "market", "Test time and coverage trade-offs scored per product for good die cost."),
             uc("Design-Fab Feedback", "DTCO", "sheet", "Closing the loop from yield data back to design rules and IP revisions."),
             uc("Customer Quality CoA", "Ship release", "product", "Certificates of analysis and ship-hold logic joined to final test gates.")],
        ),
        "sources": {
            "applied-e3": {"t": "Applied Materials E3 MES", "u": "https://www.appliedmaterials.com/us/en/products/e3.html"},
            "camstar": {"t": "Camstar Semiconductor Suite", "u": "https://plm.sw.siemens.com/en-US/opcenter/"},
            "brooks-pfab": {"t": "Brooks Automation PFAB", "u": "https://www.brooks.com/"},
            "synopsys-fusion": {"t": "Synopsys Fusion Design Platform", "u": "https://www.synopsys.com/implementation-and-signoff.html"},
            "cadence-virtuoso": {"t": "Cadence Virtuoso", "u": "https://www.cadence.com/en_US/home/tools/custom-ic-analog-rf-design/virtuoso-studio.html"},
            "calibre": {"t": "Siemens Calibre", "u": "https://eda.sw.siemens.com/en-US/ic/calibre-design/"},
            "teradyne": {"t": "Teradyne UltraFLEX", "u": "https://www.teradyne.com/products/test-systems/ultraflex/"},
            "pdf-exensio": {"t": "PDF Solutions Exensio", "u": "https://www.pdf.com/exensio"},
            "kla-5d": {"t": "KLA 5D Analyzer", "u": "https://www.kla.com/"},
            "secs-gem": {"t": "SECS/GEM equipment interface", "u": "https://www.semi.org/en/standards"},
            "asml-yieldstar": {"t": "ASML YieldStar metrology", "u": "https://www.asml.com/en/products/metrology-and-inspection-systems"},
            "lam-analytics": {"t": "Lam Research equipment analytics", "u": "https://www.lamresearch.com/"},
            "sap-s4": {"t": "SAP S/4HANA", "u": "https://www.sap.com/products/erp/s4hana.html"},
            "resilinc": {"t": "Resilinc supply risk", "u": "https://resilinc.com/"},
            "semi-e134": {"t": "SEMI E134 data collection", "u": "https://www.semi.org/en/products-services/standards"},
            "stdf": {"t": "STDF test data format", "u": "https://www.semi.org/en/products-services/standards"},
        },
    },
}
