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


INDUSTRIES_BATCH_TRANSPORT_SHIPPING = {
    'transport_shipping': {
        "label": "Transport & Logistics",
        "blurb": "Freight carriers and 3PLs: transportation management, warehouse execution, route optimisation, fleet telematics, and shipper visibility across road, rail and last mile.",
        "medallion": medallion(
            "Raw shipment and fleet feeds",
            "TMS orders, WMS moves, ELD logs, carrier EDI and shipper tender events, landed exactly as received so a detention charge or a missed appointment can always be replayed.",
            "Conformed shipment, leg, asset",
            "Shipments, legs, stops and assets resolved into single conformed entities across TMS, WMS and telematics, with multi-stop routes stitched to one delivery.",
            "OTIF, cost per mile",
            "Contracted products operations and finance run on: on-time-in-full by lane, cost per mile, warehouse pick rate, detention and fuel surcharge recovery.",
        ),
        "rails": {
            "src": [
                {"box": "TMS & Planning", "ic": "erp", "tiles": [
                    tile("Oracle OTM", "erp", "Transportation planning, tendering, execution and freight payment.", "oracle-otm"),
                    tile("Blue Yonder TMS", "sheet", "Load building, mode selection and carrier assignment.", "blue-yonder-tms"),
                    tile("MercuryGate TMS", "market", "Multi-modal rating, routing and carrier scorecards.", "mercurygate"),
                ]},
                {"box": "WMS & Fulfillment", "ic": "db", "tiles": [
                    tile("Manhattan Active WMS", "db", "Receiving, putaway, picking and shipping execution.", "manhattan-wms"),
                    tile("SAP EWM", "erp", "Warehouse management integrated to manufacturing and retail flows.", "sap-ewm"),
                    tile("Körber WMS", "stream", "High-bay and automated storage execution for 3PL campuses.", "korber-wms"),
                ]},
                {"box": "Fleet & Telematics", "ic": "iot", "tiles": [
                    tile("Samsara Fleet", "iot", "GPS, ELD, dashcam and engine diagnostics for owned and leased fleets.", "samsara"),
                    tile("Geotab Fleet", "stream", "Vehicle location, idle time and maintenance alerts.", "geotab"),
                    tile("Omnitracs ELD", "partner", "Hours of service, route compliance and driver workflow.", "omnitracs"),
                ]},
                {"box": "Carrier & Freight", "ic": "partner", "tiles": [
                    tile("project44 Visibility", "api", "Real-time shipment tracking across LTL, TL and parcel networks.", "project44"),
                    tile("FourKites", "globe", "Predictive ETA and exception management for shipper portals.", "fourkites"),
                    tile("EDI VAN (Cleo)", "stream", "204 tender, 214 status and 210 invoice messages with carriers.", "cleo-edi"),
                ]},
                {"box": "Finance & Claims", "ic": "chart", "tiles": [
                    tile("SAP TM Settlement", "market", "Freight accruals, audit and payment matched to proof of delivery.", "sap-tm-settle"),
                    tile("Transporeon", "partner", "Dock appointment, yard management and detention billing.", "transporeon"),
                ]},
                fed_group("Shipper TMS Marts", "Shipper order and ASN marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("EDI X12 214/210", "stream", "Standard shipment status and freight invoice messages parsed on arrival.", "cleo-edi"),
                tile("FMCSA SAFER Feed", "gavel", "Carrier safety and authority status for onboarding checks.", "fmcsa"),
                tile("Fuel Index APIs", "market", "Weekly fuel surcharge indices consumed for rating updates.", "transporeon"),
            ]),
            "ppl": ppl2([
                biz("CEO & Network Office", "Genie One", "The CEO on margin per load; the COO on OTIF and fleet utilisation, trading empty miles and detention against the contracted service.",
                    [["Genie One", "Ask what last week's lane margin was without analyst delay."], ["AI/BI", "OTIF and cost per mile on certified Metric Views."], ["Unity Catalog", "One shipment definition across TMS and WMS."]]),
                biz("Transportation Ops", "Lakehouse//RT", "Dispatchers on tender acceptance, in-transit exceptions and appointment compliance, moving loads before ETA risk becomes a detention charge.",
                    [["Control Tower", "Live shipments, ETA risk and detention exposure on one map."], ["Lakehouse//RT", "ELD and TMS state at dispatch latency."]]),
                biz("Warehouse Ops", "Apps", "DC managers on pick rate, labour balance and outbound cut-off, releasing waves so the dock clears before the carrier appointment closes.",
                    [["Warehouse Pulse", "Pick waves, dock doors and labour plan against cut-off."], ["Apps", "Floor apps hosted next to governed WMS data."]]),
                biz("Commercial & Pricing", "Model Serving", "Pricing analysts on lane rates, accessorials and shipper contracts, scoring spot versus contract margin before a load is tendered.",
                    [["Rate Engine Workbench", "Contract and spot rates before tender."], ["Model Serving", "Dynamic pricing models in the bid path."]]),
                biz("Finance & Claims", "AI/BI", "Freight audit and claims teams on detention, fuel surcharge recovery and accrual variance, matching each invoice to contract and POD.",
                    [["AI/BI", "Accrual variance and audit findings on certified views."], ["Genie One", "Ask which carriers exceed detention thresholds."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land TMS orders, WMS moves, ELD logs and carrier EDI; own Bronze to Silver and the pager when an OTIF or cost-per-mile table breaks.",
                    [["Lakeflow Connect", "Managed connectors for TMS, WMS and telematics sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on EDI and ELD feeds."], ["Lakewatch", "Freshness on the OTIF tables the control tower reads through the day."]]),
                biz("Data Scientists", "MLflow", "Predictive-ETA, route-optimisation, dynamic-pricing and carrier-scoring models, and whether they still hold as lanes and fuel indices shift.",
                    [["Feature Store", "Shipment and lane features read identically in training and serving."], ["MLflow", "Every ETA and pricing experiment tracked for audit."], ["Model Serving", "ETA and pricing models scored in the dispatch and bid path."]]),
                biz("App Developers", "Apps", "Ship the Control Tower, Warehouse Pulse and Rate Engine apps operations and pricing teams work in, next to governed TMS and WMS data.",
                    [["Apps", "Operations screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for appointment and wave state writes."], ["Agent Bricks", "Agents that draft tender responses against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Operations and finance dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for OTIF and detention questions in the control tower channel."),
                    tile("Notebooks & IDEs", "notebook", "Network optimisation notebooks against governed TMS data."),
                ]},
                {"box": "Shipper & Carrier", "ic": "partner", "tiles": [
                    tile("Shipper Visibility API", "api", "ETA and exception events shared to shipper TMS over Delta Sharing.", "project44"),
                    tile("Carrier Tender Portal", "market", "Loads tendered and accepted through governed APIs.", "mercurygate"),
                    tile("3PL Billing Portal", "share", "Invoice backup and POD images delivered to shippers."),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("TMS Appointment Update", "db", "Dock appointments written back to TMS and yard systems.", "oracle-otm"),
                    tile("Driver Mobile Tasks", "apps", "Stop sequence and document capture pushed to driver devices.", "samsara"),
                    tile("WMS Wave Release", "stream", "Pick waves released to the floor based on cut-off optimisation."),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("HOS Compliance Reports", "gavel", "ELD violation summaries for safety audits.", "omnitracs"),
                    tile("Carbon & Scope 3", "share", "Emissions per shipment reported to shipper sustainability programs."),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Visibility and lane performance products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Shippers reading live ETA via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Control Tower", "Shipment visibility", "globe", "Live shipments, ETA risk and detention exposure on a map with exception workflows."),
             app("Warehouse Pulse", "DC operations", "db", "Pick waves, labour and dock capacity against outbound cut-off."),
             app("Rate Engine Workbench", "Pricing", "market", "Contract, spot and accessorial rates before tender and audit."),
             app("Driver Mobile Hub", "Last mile", "apps", "Stop sequence, POD capture and exception codes on driver devices.")],
            [uc("Route Optimization", "Planning", "sheet", "Multi-stop routes optimised for miles, HOS and appointment windows."),
             uc("Predictive ETA", "Visibility", "globe", "ETA refined from telematics, traffic and historical lane performance."),
             uc("Detention Management", "Finance", "market", "Detention clock and claims raised before free time expires."),
             uc("Load Consolidation", "TMS", "erp", "LTL and partial loads combined to improve utilisation and margin."),
             uc("Warehouse Slotting", "WMS", "db", "Pick path and slot placement tuned to velocity and seasonality."),
             uc("Carrier Scorecards", "Procurement", "partner", "OTIF, cost and claims history scored per carrier and lane."),
             uc("Freight Audit", "Finance", "chart", "Invoices matched to contract, POD and accessorial rules before payment."),
             uc("Cold Chain Monitoring", "Compliance", "iot", "Temperature excursions flagged for food and pharma loads."),
             uc("Yard Management", "Operations", "stream", "Trailer location and dock door assignment to cut yard turns."),
             uc("Scope 3 Emissions", "Sustainability", "gavel", "Emissions per shipment calculated for shipper ESG reporting.")],
        ),
        "sources": {
            "oracle-otm": {"t": "Oracle Transportation Management", "u": "https://www.oracle.com/scm/logistics/transportation-management/"},
            "blue-yonder-tms": {"t": "Blue Yonder TMS", "u": "https://blueyonder.com/solutions/transportation-management"},
            "mercurygate": {"t": "MercuryGate TMS", "u": "https://mercurygate.com/"},
            "manhattan-wms": {"t": "Manhattan Active WMS", "u": "https://www.manh.com/solutions/warehouse-management"},
            "sap-ewm": {"t": "SAP Extended Warehouse Management", "u": "https://www.sap.com/products/scm/extended-warehouse-management.html"},
            "korber-wms": {"t": "Körber WMS", "u": "https://www.koerber-supplychain.com/"},
            "samsara": {"t": "Samsara", "u": "https://www.samsara.com/"},
            "geotab": {"t": "Geotab", "u": "https://www.geotab.com/"},
            "omnitracs": {"t": "Omnitracs", "u": "https://www.omnitracs.com/"},
            "project44": {"t": "project44", "u": "https://www.project44.com/"},
            "fourkites": {"t": "FourKites", "u": "https://www.fourkites.com/"},
            "cleo-edi": {"t": "Cleo integration", "u": "https://www.cleo.com/"},
            "sap-tm-settle": {"t": "SAP TM settlement", "u": "https://www.sap.com/products/scm/transportation-logistics.html"},
            "transporeon": {"t": "Transporeon", "u": "https://www.transporeon.com/"},
            "fmcsa": {"t": "FMCSA SAFER", "u": "https://www.fmcsa.dot.gov/"},
        },
    },
}
