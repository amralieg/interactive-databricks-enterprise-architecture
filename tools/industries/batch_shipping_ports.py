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


INDUSTRIES_BATCH_SHIPPING_PORTS = {
    'shipping_ports': {
        "label": "Shipping & Ports",
        "blurb": "Port and terminal operations: vessel scheduling, berth and crane allocation, cargo handling, customs clearance, and landside logistics across container and bulk terminals.",
        "medallion": medallion(
            "Raw port and vessel feeds",
            "TOS moves, AIS position reports, berth plans, customs declarations and gate transactions, landed exactly as received so a dwell time or a crane move can always be replayed.",
            "Conformed vessel, visit, unit",
            "Vessels, port calls, containers and bills of lading resolved into single conformed entities across TOS, PCS and carrier systems, with voyage legs stitched to one visit.",
            "Throughput, dwell, crane rate",
            "Contracted products terminal and port authority teams run on: crane moves per hour, truck turnaround, vessel berth productivity, container dwell and demurrage exposure.",
        ),
        "rails": {
            "src": [
                {"box": "Terminal Operating", "ic": "erp", "tiles": [
                    tile("Navis N4 TOS", "erp", "Terminal operating system: vessel plans, yard slots, crane dispatch and gate transactions.", "navis-n4"),
                    tile("CyberLogitec OPUS", "db", "Container yard inventory, equipment control and rail loading for multi-modal terminals.", "cyberlogitec"),
                    tile("SAP TM for Ports", "sheet", "Landside transport orders, appointment scheduling and carrier billing.", "sap-tm"),
                ]},
                {"box": "Vessel & Traffic", "ic": "stream", "tiles": [
                    tile("Port Community System", "api", "Berth requests, pilot orders and customs pre-arrival messages exchanged with carriers.", "pcs"),
                    tile("AIS Vessel Tracking", "globe", "Position, ETA and anchorage queue for every vessel approaching the port.", "ais"),
                    tile("MarineTraffic API", "partner", "Historical track, port calls and congestion signals for schedule planning.", "marinetraffic"),
                ]},
                {"box": "Cargo & Customs", "ic": "gavel", "tiles": [
                    tile("Descartes Customs", "gavel", "Import and export declarations, duty calculation and hold status from customs brokers.", "descartes-customs"),
                    tile("CargoWise One", "market", "Freight forwarding, house bills and milestone events for containerised cargo.", "cargowise"),
                    tile("INTTRA eBL", "product", "Electronic bills of lading and booking confirmations from ocean carriers.", "inttra"),
                ]},
                {"box": "Equipment & Yard", "ic": "iot", "tiles": [
                    tile("Kalmar Insight", "iot", "RTG and STS crane telemetry, spreader cycles and fuel burn by shift.", "kalmar-tv"),
                    tile("Identec RFID Gates", "stream", "Automated gate OCR, RFID and chassis identification at in-gate and out-gate.", "identec"),
                    tile("SICK Yard Automation", "partner", "Automated straddle carrier and AGV position for high-throughput yards.", "sick-yard"),
                ]},
                {"box": "Finance & Tariffs", "ic": "market", "tiles": [
                    tile("Jade Master Terminal", "erp", "Storage, handling and demurrage invoices reconciled against actual moves.", "oracle-port"),
                    tile("Tideworks Mainsail", "chart", "Published tariffs, rebates and contract rates applied to each service event.", "hph-tariff"),
                ]},
                fed_group("Carrier Schedule Marts", "Vessel schedules and capacity marts left with carriers and queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("UN/EDIFACT COPRAR / CODECO", "stream", "COPRAR and CODECO vessel and gate moves and IFTMIN and IFTSTA transport messages from shipping lines, parsed on arrival.", "edifact"),
                tile("Port Authority AIS Feed", "api", "Real-time berth occupancy and pilot boarding events from the port authority.", "pcs"),
                tile("Customs Single Window", "gavel", "Government clearance status and inspection results consumed inbound.", "descartes-customs"),
            ]),
            "ppl": ppl2([
                biz("Port Director Office", "Genie One", "The port director on throughput and revenue per call; the COO on berth productivity, truck queues and the terminal's demurrage exposure.",
                    [["Genie One", "Ask what yesterday's vessel productivity cost without analyst delay."], ["AI/BI", "Crane rate and dwell on certified Metric Views."], ["Unity Catalog", "One definition of dwell across terminal and finance."]],
                    sub=[
                        ["Port Director", "throughput, revenue per call and the port's standing against neighbouring gateways."],
                        ["Chief Operating Officer", "berth productivity, truck queues and the terminal's demurrage exposure each shift."],
                        ["Harbour Master", "vessel safety, berth allocation and traffic through the approach channel."],
                    ],
                    ucs=["Berth Productivity", "Tariff & Storage Revenue", "Vessel ETA Reliability", "Environmental Reporting"]),
                biz("Terminal Operations", "Lakehouse//RT", "Berth planners and shift managers on crane allocation, yard density and vessel cut-off, defending crane moves per hour on the stow plan.",
                    [["Berth Planner", "Live berth and crane plan against AIS ETA and yard capacity."], ["Lakehouse//RT", "Gate and crane state at terminal-line latency."]],
                    sub=[
                        ["Berth Planner", "the berth and crane plan against AIS ETA, stow and yard capacity."],
                        ["Shift Manager", "crane moves per hour and gang deployment across the working shift."],
                        ["Yard Controller", "slot density, rehandles and equipment balance across the stacks."],
                    ],
                    ucs=["Berth Productivity", "Crane Sequencing", "Vessel ETA Reliability", "Container Dwell"]),
                biz("Commercial & Tariffs", "AI/BI", "Tariff managers on contract compliance, rebate accuracy and storage revenue leakage where free-dwell days slip past the billed clock.",
                    [["AI/BI", "Handling revenue and demurrage on certified views."], ["Genie One", "Ask which customers exceed free dwell this week."]],
                    sub=[
                        ["Tariff Manager", "contract rates, rebate accuracy and storage revenue leakage on free-dwell days."],
                        ["Key Account Manager", "line and shipper agreements and volume commitments per service."],
                        ["Revenue Assurance", "billed moves reconciled to the actual crane and gate events."],
                    ],
                    ucs=["Tariff & Storage Revenue", "Container Dwell", "Berth Productivity"]),
                biz("Landside Logistics", "Model Serving", "Truck appointment and rail planners on gate queues and intermodal handoff, matching slots to yard density before demurrage accrues.",
                    [["Gate Optimizer", "Appointment slots scored against yard density and cut-off."], ["Model Serving", "Dwell prediction models before demurrage accrues."]],
                    sub=[
                        ["Gate Manager", "truck appointment slots, gate queues and turnaround time at the terminal."],
                        ["Intermodal Planner", "rail consist, train windows and the yard-to-ramp handoff."],
                        ["Drayage Coordinator", "carrier slot compliance and container availability at pickup."],
                    ],
                    ucs=["Gate Turnaround", "Container Dwell", "Intermodal Rail Load"]),
                biz("Customs & Security", "Lakeflow", "Compliance teams on customs holds, inspection outcomes and dangerous-goods declarations validated against stow position and segregation.",
                    [["Customs Hold Console", "Declaration status and inspection outcomes in one governed view."], ["Lakeflow", "PCS and customs feeds conformed for compliance analytics."]],
                    sub=[
                        ["Customs Compliance", "declaration status, holds and inspection outcomes before cargo lands."],
                        ["DG Officer", "dangerous-goods segregation, stow position and hazmat documentation."],
                        ["Port Security", "ISPS access control, seals and screening across the terminal perimeter."],
                    ],
                    ucs=["Customs Clearance", "Dangerous Goods", "Container Dwell"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land TOS moves, AIS position reports, PCS messages and customs feeds; own Bronze to Silver and the pager when a dwell or crane table breaks.",
                    [["Lakeflow Connect", "Managed connectors for TOS, PCS and carrier sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on AIS and gate feeds."], ["Lakewatch", "Freshness on the dwell tables the berth desk reads each shift."]],
                    sub=[
                        ["Ingestion Engineer", "TOS moves, AIS position reports, PCS and customs feeds landed on arrival."],
                        ["Pipeline Engineer", "Bronze-to-Silver conformance and expectations on the dwell and crane tables."],
                        ["Platform SRE", "the pager when a dwell or crane table the berth desk reads breaks."],
                    ],
                    ucs=["Berth Productivity", "Container Dwell", "Vessel ETA Reliability", "Customs Clearance"]),
                biz("Data Scientists", "MLflow", "Dwell-prediction, vessel-ETA, crane-sequencing and gate-turnaround models, and whether they still hold as schedules and yard density shift.",
                    [["Feature Store", "Vessel and yard features read identically in training and serving."], ["MLflow", "Every ETA and dwell experiment tracked for audit."], ["Model Serving", "Dwell and ETA models scored on approaching calls."]],
                    sub=[
                        ["ETA & Dwell Modeler", "vessel-ETA and container-dwell models as schedules and yard density shift."],
                        ["Optimisation Scientist", "crane-sequencing and berth-allocation under twin-lift and rehandle limits."],
                        ["MLOps Engineer", "feature parity and drift on the ETA and dwell models in production."],
                    ],
                    ucs=["Container Dwell", "Vessel ETA Reliability", "Crane Sequencing", "Gate Turnaround"]),
                biz("App Developers", "Apps", "Ship the Berth Planner, Gate Optimizer and Yard Density apps terminal teams work in, hosted next to governed TOS and AIS data.",
                    [["Apps", "Terminal screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for appointment and dispatch writes."], ["Agent Bricks", "Agents that draft crane sequences against governed tools."]],
                    sub=[
                        ["Full-Stack Engineer", "the Berth Planner, Gate Optimizer and Yard Density screens teams work in."],
                        ["Backend Engineer", "appointment and dispatch writes on serverless Postgres next to governed data."],
                        ["Agent Developer", "agents that draft crane sequences against governed terminal tools."],
                    ],
                    ucs=["Berth Productivity", "Gate Turnaround", "Container Dwell"]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Terminal KPI dashboards on serverless SQL with Unity Catalog permissions."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for berth and dwell questions in the operations channel."),
                    tile("Notebooks & IDEs", "notebook", "Operations notebooks against governed TOS and AIS data."),
                ]},
                {"box": "Carrier & Landside", "ic": "partner", "tiles": [
                    tile("Vessel Schedule API", "api", "Berth windows and crane availability shared to shipping lines over Delta Sharing."),
                    tile("Trucker Appointment Portal", "apps", "Gate slots and container availability pushed to drayage carriers."),
                    tile("Rail Ramp Partners", "globe", "Outbound train consist and loading status shared to intermodal operators."),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("TOS Crane Dispatch", "db", "Optimised crane sequences written back to the TOS dispatch list.", "navis-n4"),
                    tile("Gate Appointment Release", "stream", "Appointment capacity adjustments pushed to the truck portal."),
                    tile("Yard Rehandle Orders", "apps", "Rehandle tasks dispatched to yard equipment operators."),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Port Authority KPIs", "gavel", "Throughput and environmental metrics filed to the port authority.", "pcs"),
                    tile("Customs Audit Trail", "share", "Declaration and inspection evidence from contracted Gold products."),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Terminal performance products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Carriers and shippers reading live dwell and berth data via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Berth Planner", "Vessel scheduling", "gauge", "Berth and crane plans scored against AIS ETA, yard density and labour availability."),
             app("Gate Optimizer", "Truck appointments", "stream", "Appointment slots and gate lanes matched to yard capacity and vessel cut-off."),
             app("Yard Density Map", "Slot utilisation", "iot", "Live yard occupancy and rehandle risk before the vessel gang lands."),
             app("Customs Hold Console", "Clearance status", "gavel", "Declaration holds, inspections and release milestones in one operations view.")],
            [uc("Berth Productivity", "Vessel ops", "gauge", "Crane moves per hour and berth idle time attributed to plan versus execution.",
                problem="Crane rate and berth idle time live in TOS and crane logs separately, so a shift that loses productivity to plan versus execution is only reconstructed next day, after the vessel sailed.",
                who="Terminal Operations",
                how="Navis N4 TOS moves and Kalmar Insight equipment telemetry land through Lakeflow and conform on Delta Lake, so berth productivity is attributed to plan versus execution and read in the Berth Planner.",
                comps=["Berth Planner", "Navis N4 TOS", "Kalmar Insight", "Lakeflow", "Delta Lake", "AI/BI"],
                stories=[
                    ["PTP gains real-time operational insights with Databricks Lakehouse", "https://www.tigeranalytics.com/perspectives/case-study/delivering-real-time-operational-insights-for-ptp-with-databricks-lakehouse/"],
                    ["From raw shipping data to real-time predictions on Databricks", "https://community.databricks.com/t5/technical-blog/from-raw-shipping-data-to-real-time-predictions-in-one-platform/ba-p/153713"],
                ]),
             uc("Container Dwell", "Yard ops", "db", "Dwell days and demurrage exposure predicted before free time expires.",
                problem="Free-dwell clocks tick across thousands of boxes at once, so by the time a spreadsheet flags the units about to breach, demurrage has accrued and the yard is congested with stale containers.",
                who="Landside Logistics",
                how="Gate, TOS and customs events feed dwell features scored in Model Serving, and predicted breaches surface in the Yard Density Map so operators clear boxes before free time expires.",
                comps=["Yard Density Map", "Model Serving", "Identec RFID Gates", "Descartes Customs", "Feature Store", "Delta Lake"],
                stories=[
                    ["Kotahi improves container movement visibility with Azure Databricks", "https://www.databricks.com/customers/kotahi"],
                ]),
             uc("Gate Turnaround", "Landside", "stream", "Truck visit duration decomposed by queue, OCR and yard handoff.",
                problem="Truck visit time blends queueing, OCR read failures and yard handoff delays, but the causes sit buried in gate and TOS logs, so drivers wait and appointment capacity is set by rule of thumb.",
                who="Landside Logistics",
                how="Identec gate OCR and TOS handoff events land through Lakeflow and are decomposed on Delta Lake, so the Gate Optimizer matches appointment slots to real turnaround by queue, OCR and yard stage.",
                comps=["Gate Optimizer", "Identec RFID Gates", "Navis N4 TOS", "Lakeflow", "Delta Lake", "AI/BI"]),
             uc("Crane Sequencing", "Equipment", "iot", "Crane work lists optimised for twin-lift and minimum rehandle.",
                problem="Crane work lists are built by hand against the stow plan, so twin-lift chances are missed and avoidable rehandles pile up, dragging moves per hour down when the berth window is tightest.",
                who="Terminal Operations",
                how="Stow, yard-slot and crane telemetry are conformed on Delta Lake and optimised with Model Serving, and the sequence is written back to the Navis N4 TOS dispatch list for the gang to work.",
                comps=["Berth Planner", "Navis N4 TOS", "Kalmar Insight", "Model Serving", "Delta Lake", "Apache Spark"]),
             uc("Vessel ETA Reliability", "Planning", "globe", "AIS-derived ETA accuracy scored against declared schedules.",
                problem="Carrier-declared ETAs drift by hours against what AIS actually shows, so berths and gangs are planned to a schedule already wrong, and the terminal absorbs the idle time or the scramble.",
                who="Terminal Operations",
                how="AIS Vessel Tracking and MarineTraffic history feed ETA models tracked in MLflow and scored in Model Serving, so the Berth Planner ranks declared schedules against a live AIS-derived arrival.",
                comps=["Berth Planner", "AIS Vessel Tracking", "MarineTraffic API", "Model Serving", "MLflow", "Lakehouse//RT"],
                stories=[
                    ["From raw shipping data to real-time predictions on Databricks", "https://community.databricks.com/t5/technical-blog/from-raw-shipping-data-to-real-time-predictions-in-one-platform/ba-p/153713"],
                ]),
             uc("Customs Clearance", "Compliance", "gavel", "Pre-arrival screening and hold resolution before cargo lands.",
                problem="Declarations, holds and inspections arrive from brokers and the single window on their own clocks, so a box can reach the quay still held and the desk learns only when discharge stalls.",
                who="Customs & Security",
                how="Descartes and Customs Single Window feeds conform through Lakeflow into the Customs Hold Console, so pre-arrival screening and hold resolution happen on one governed view before cargo lands.",
                comps=["Customs Hold Console", "Descartes Customs", "Customs Single Window", "Lakeflow", "Unity Catalog", "AI/BI"],
                stories=[
                    ["Hapag-Lloyd uses Databricks to enhance audit and compliance efficiency", "https://www.databricks.com/customers/hapag-lloyd"],
                ]),
             uc("Intermodal Rail Load", "Rail", "partner", "Train loading plans matched to vessel discharge and yard slots.",
                problem="Rail load plans are built before the vessel finishes discharge, so when the box mix or yard position shifts the train works from stale lists, wagons go out light and ramp slots are wasted.",
                who="Landside Logistics",
                how="TOS discharge events and SAP TM rail orders conform on Delta Lake, so load plans in the Gate Optimizer are matched to actual discharge and yard slots and shared to the ramp over Open Sharing.",
                comps=["Gate Optimizer", "SAP TM for Ports", "Navis N4 TOS", "Delta Lake", "Open Sharing", "AI/BI"]),
             uc("Tariff & Storage Revenue", "Commercial", "market", "Handling and storage charges reconciled to actual moves.",
                problem="Handling and storage charges bill from the TOS, but rebates, contract rates and free-dwell exceptions live in other systems, so revenue leaks wherever billed and actual moves diverge.",
                who="Commercial & Tariffs",
                how="Jade Master Terminal and Tideworks Mainsail data conform on Delta Lake and reconcile to actual crane and gate events, so handling and storage revenue is verified on certified AI/BI views.",
                comps=["Jade Master Terminal", "Tideworks Mainsail", "Navis N4 TOS", "Delta Lake", "AI/BI", "Unity Catalog"],
                stories=[
                    ["Hafnia modernizes maritime operations with Lakebase", "https://www.databricks.com/customers/hafnia/lakebase"],
                ]),
             uc("Dangerous Goods", "Safety", "gavel", "DG declarations validated against stow position and segregation rules.",
                problem="DG declarations are checked against stow position and segregation rules by hand, so a mis-declared or wrongly stowed hazardous box can reach the yard, caught only at inspection.",
                who="Customs & Security",
                how="INTTRA eBL and PCS declarations conform through Lakeflow and are validated against stow position on Delta Lake, so segregation breaches surface in the Customs Hold Console before the box is worked.",
                comps=["Customs Hold Console", "INTTRA eBL", "Port Community System", "Lakeflow", "Delta Lake", "Unity Catalog"]),
             uc("Environmental Reporting", "ESG", "chart", "Emissions and noise metrics reported to port authority programs.",
                problem="Emissions, energy and noise metrics for port-authority programs are stitched by hand from crane fuel, vessel AIS and equipment telemetry each cycle, so numbers arrive late and untraced.",
                who="Port Director Office",
                how="AIS, crane fuel and equipment telemetry conform on Delta Lake with Unity Catalog lineage, so emissions metrics are computed once and reported to port-authority programs from certified AI/BI products.",
                comps=["AIS Vessel Tracking", "Kalmar Insight", "Unity Catalog", "Delta Lake", "AI/BI", "Data Products"],
                stories=[
                    ["Leveraging ESG data to operationalize sustainability with Databricks", "https://www.databricks.com/blog/2020/11/11/leveraging-esg-data-to-operationalize-sustainability.html"],
                ])],
        ),
        "sources": {
            "navis-n4": {"t": "Navis N4 terminal operating system", "u": "https://www.navis.com/products/navis-n4"},
            "cyberlogitec": {"t": "CyberLogitec OPUS Terminal", "u": "https://www.cyberlogitec.com/"},
            "sap-tm": {"t": "SAP Transportation Management", "u": "https://www.sap.com/products/scm/transportation-logistics.html"},
            "pcs": {"t": "Port community systems", "u": "https://www.ipcsa.international/"},
            "ais": {"t": "Automatic Identification System", "u": "https://www.imo.org/en/OurWork/Safety/Pages/AIS.aspx"},
            "marinetraffic": {"t": "MarineTraffic", "u": "https://www.marinetraffic.com/"},
            "descartes-customs": {"t": "Descartes customs compliance", "u": "https://www.descartes.com/"},
            "cargowise": {"t": "CargoWise One", "u": "https://www.cargowise.com/"},
            "inttra": {"t": "INTTRA eBL platform", "u": "https://www.inttra.com/"},
            "kalmar-tv": {"t": "Kalmar Insight", "u": "https://www.kalmarglobal.com/parts-services/kalmar-insight/"},
            "identec": {"t": "Identec Solutions", "u": "https://www.identecsolutions.com/"},
            "sick-yard": {"t": "SICK logistics automation", "u": "https://www.sick.com/"},
            "oracle-port": {"t": "Jade Master Terminal TOS", "u": "https://www.jadelogistics-asia.com/products/master-terminal"},
            "hph-tariff": {"t": "Tideworks Mainsail TOS", "u": "https://tideworks.com/mainsail/"},
            "edifact": {"t": "UN/EDIFACT messaging", "u": "https://unece.org/trade/uncefact/introducing-unedifact"},
        },
    },
}
