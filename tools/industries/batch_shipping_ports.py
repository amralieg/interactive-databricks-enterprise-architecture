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
                    tile("Kalmar Terminal Vision", "iot", "RTG and STS crane telemetry, spreader cycles and fuel burn by shift.", "kalmar-tv"),
                    tile("Identec RFID Gates", "stream", "Automated gate OCR, RFID and chassis identification at in-gate and out-gate.", "identec"),
                    tile("SICK Yard Automation", "partner", "Automated straddle carrier and AGV position for high-throughput yards.", "sick-yard"),
                ]},
                {"box": "Finance & Tariffs", "ic": "market", "tiles": [
                    tile("Oracle Port Billing", "erp", "Storage, handling and demurrage invoices reconciled against actual moves.", "oracle-port"),
                    tile("HPH Tariff Engine", "chart", "Published tariffs, rebates and contract rates applied to each service event.", "hph-tariff"),
                ]},
                fed_group("Carrier Schedule Marts", "Vessel schedules and capacity marts left with carriers and queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("UN/EDIFACT IFTS", "stream", "Standard vessel visit and cargo messages from shipping lines parsed on arrival.", "edifact"),
                tile("Port Authority AIS Feed", "api", "Real-time berth occupancy and pilot boarding events from the port authority.", "pcs"),
                tile("Customs Single Window", "gavel", "Government clearance status and inspection results consumed inbound.", "descartes-customs"),
            ]),
            "ppl": ppl2([
                biz("Port Director Office", "Genie One", "The port director on throughput and revenue per call; the COO on berth productivity, truck queues and the terminal's demurrage exposure.",
                    [["Genie One", "Ask what yesterday's vessel productivity cost without analyst delay."], ["AI/BI", "Crane rate and dwell on certified Metric Views."], ["Unity Catalog", "One definition of dwell across terminal and finance."]]),
                biz("Terminal Operations", "Lakehouse//RT", "Berth planners and shift managers on crane allocation, yard density and vessel cut-off, defending crane moves per hour on the stow plan.",
                    [["Berth Planner", "Live berth and crane plan against AIS ETA and yard capacity."], ["Lakehouse//RT", "Gate and crane state at terminal-line latency."]]),
                biz("Commercial & Tariffs", "AI/BI", "Tariff managers on contract compliance, rebate accuracy and storage revenue leakage where free-dwell days slip past the billed clock.",
                    [["AI/BI", "Handling revenue and demurrage on certified views."], ["Genie One", "Ask which customers exceed free dwell this week."]]),
                biz("Landside Logistics", "Model Serving", "Truck appointment and rail planners on gate queues and intermodal handoff, matching slots to yard density before demurrage accrues.",
                    [["Gate Optimizer", "Appointment slots scored against yard density and cut-off."], ["Model Serving", "Dwell prediction models before demurrage accrues."]]),
                biz("Customs & Security", "Lakeflow", "Compliance teams on customs holds, inspection outcomes and dangerous-goods declarations validated against stow position and segregation.",
                    [["Customs Hold Console", "Declaration status and inspection outcomes in one governed view."], ["Lakeflow", "PCS and customs feeds conformed for compliance analytics."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land TOS moves, AIS position reports, PCS messages and customs feeds; own Bronze to Silver and the pager when a dwell or crane table breaks.",
                    [["Lakeflow Connect", "Managed connectors for TOS, PCS and carrier sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on AIS and gate feeds."], ["Lakewatch", "Freshness on the dwell tables the berth desk reads each shift."]]),
                biz("Data Scientists", "MLflow", "Dwell-prediction, vessel-ETA, crane-sequencing and gate-turnaround models, and whether they still hold as schedules and yard density shift.",
                    [["Feature Store", "Vessel and yard features read identically in training and serving."], ["MLflow", "Every ETA and dwell experiment tracked for audit."], ["Model Serving", "Dwell and ETA models scored on approaching calls."]]),
                biz("App Developers", "Apps", "Ship the Berth Planner, Gate Optimizer and Yard Density apps terminal teams work in, hosted next to governed TOS and AIS data.",
                    [["Apps", "Terminal screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for appointment and dispatch writes."], ["Agent Bricks", "Agents that draft crane sequences against governed tools."]]),
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
            [uc("Berth Productivity", "Vessel ops", "gauge", "Crane moves per hour and berth idle time attributed to plan versus execution."),
             uc("Container Dwell", "Yard ops", "db", "Dwell days and demurrage exposure predicted before free time expires."),
             uc("Gate Turnaround", "Landside", "stream", "Truck visit duration decomposed by queue, OCR and yard handoff."),
             uc("Crane Sequencing", "Equipment", "iot", "Crane work lists optimised for twin-lift and minimum rehandle."),
             uc("Vessel ETA Reliability", "Planning", "globe", "AIS-derived ETA accuracy scored against declared schedules."),
             uc("Customs Clearance", "Compliance", "gavel", "Pre-arrival screening and hold resolution before cargo lands."),
             uc("Intermodal Rail Load", "Rail", "partner", "Train loading plans matched to vessel discharge and yard slots."),
             uc("Tariff & Storage Revenue", "Commercial", "market", "Handling and storage charges reconciled to actual moves."),
             uc("Dangerous Goods", "Safety", "gavel", "DG declarations validated against stow position and segregation rules."),
             uc("Environmental Reporting", "ESG", "chart", "Emissions and noise metrics reported to port authority programs.")],
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
            "kalmar-tv": {"t": "Kalmar Terminal Vision", "u": "https://www.kalmarglobal.com/"},
            "identec": {"t": "Identec Solutions", "u": "https://www.identecsolutions.com/"},
            "sick-yard": {"t": "SICK logistics automation", "u": "https://www.sick.com/"},
            "oracle-port": {"t": "Oracle utilities and port billing", "u": "https://www.oracle.com/industries/utilities/"},
            "hph-tariff": {"t": "Hutchison Ports tariff management", "u": "https://www.hutchisonports.com/"},
            "edifact": {"t": "UN/EDIFACT messaging", "u": "https://unece.org/trade/uncefact/introducing-unedifact"},
        },
    },
}
