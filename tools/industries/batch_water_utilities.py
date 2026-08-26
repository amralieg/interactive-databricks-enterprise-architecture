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


INDUSTRIES_BATCH_WATER_UTILITIES = {
    'water_utilities': {
        "label": "Water Utilities",
        "blurb": "Municipal and investor-owned water utilities: SCADA and AMI metering, network asset management, customer billing, field work orders, and regulatory quality reporting.",
        "medallion": medallion(
            "Raw network and meter feeds",
            "SCADA historian tags, AMI interval reads, work orders, billing cycles and lab sample results, landed exactly as received so a leak alert or a quality exceedance can always be replayed.",
            "Conformed meter, asset, account",
            "Meters, assets, service accounts and pressure zones resolved into single conformed entities across CIS, SCADA and GIS, with consumption intervals stitched to one account.",
            "NRW, pressure, compliance",
            "Contracted products operations and regulators run on: non-revenue water, pressure compliance, boil-water event response, and cost per thousand gallons by district.",
        ),
        "rails": {
            "src": [
                {"box": "CIS & Billing", "ic": "erp", "tiles": [
                    tile("Oracle Utilities C2M", "erp", "Customer information, billing, payments and credit collections.", "oracle-c2m"),
                    tile("SAP IS-U", "market", "Utility billing and device management for multi-commodity utilities.", "sap-isu"),
                    tile("VertexOne CIS", "chart", "Cloud CIS for water and wastewater with customer self-service.", "vertexone"),
                ]},
                {"box": "SCADA & Operations", "ic": "stream", "tiles": [
                    tile("AVEVA PI System", "stream", "Historian for pumps, tanks, pressure and flow across the distribution network.", "aveva-pi"),
                    tile("Ignition SCADA", "iot", "Plant and remote site SCADA for treatment and pumping stations.", "ignition"),
                    tile("Schneider EcoStruxure", "partner", "Edge control and telemetry for lift stations and PRVs.", "schneider-eco"),
                ]},
                {"box": "AMI & Metering", "ic": "iot", "tiles": [
                    tile("Itron OpenWay", "iot", "Advanced metering infrastructure: interval reads, tamper and leak flags.", "itron"),
                    tile("Sensus FlexNet", "api", "AMI head-end for residential and commercial meter populations.", "sensus"),
                    tile("Badger Beacon", "db", "Encoder registers and mobile collection for legacy meter routes.", "badger"),
                ]},
                {"box": "GIS & Assets", "ic": "db", "tiles": [
                    tile("Esri ArcGIS Utility", "globe", "Pipe network, valves, hydrants and service connections geospatially modeled.", "esri-utility"),
                    tile("IBM Maximo", "erp", "Asset registry, work orders and preventive maintenance for treatment plants.", "maximo"),
                    tile("Cityworks AMS", "sheet", "Work management for mains breaks, service line replacements and inspections.", "cityworks"),
                ]},
                {"box": "Lab & Quality", "ic": "gavel", "tiles": [
                    tile("Hach WIMS", "gavel", "Water quality lab results, chain of custody and regulatory limits.", "hach-wims"),
                    tile("KISTERS WISKI", "chart", "Hydrological and water quality time series for source water monitoring.", "kisters"),
                ]},
                fed_group("Regional Agency Marts", "Wholesale and intertie flow marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("EPA SDWIS Feed", "gavel", "Safe Drinking Water Information System reference for compliance benchmarking.", "epa-sdwis"),
                tile("NOAA Hydrology API", "stream", "River flow and drought indices for source water planning.", "noaa"),
                tile("Weather Forecast API", "observ", "Demand and infiltration forecasting inputs from meteorological services.", "noaa"),
            ]),
            "ppl": ppl2([
                biz("GM & Executive Office", "Genie One", "The general manager on cost per gallon and the capital plan; the COO on non-revenue water and the response time on a distribution outage.",
                    [["Genie One", "Ask what last month's NRW was without analyst delay."], ["AI/BI", "Pressure and quality KPIs on certified Metric Views."], ["Unity Catalog", "One consumption definition across AMI and billing."]]),
                biz("Distribution Ops", "Lakehouse//RT", "Control room operators on pressure, storage and pump scheduling, holding pressure zones in compliance while trimming energy at the pumps.",
                    [["Network Control Center", "Live SCADA, AMI leak flags and crew dispatch on one screen."], ["Lakehouse//RT", "Telemetry at control-room latency."]]),
                biz("Customer Operations", "CustomerLake", "Call centre and field service on outages, high-bill disputes and leak investigations, giving agents restoration ETA and account context.",
                    [["Customer Impact Console", "Outage map, estimated restoration and high-bill triage."], ["CustomerLake", "Account context without copying into a separate CRM."]]),
                biz("Asset Management", "AI/BI", "Engineers on main-replacement priority, pump health and capex planning, ranking mains on break risk, age and soil against renewal budget.",
                    [["AI/BI", "Asset risk and remaining life on certified views."], ["Genie One", "Ask which mains exceed break rate thresholds."]]),
                biz("Water Quality", "Lakeflow", "Quality teams on sample results, regulatory exceedances and public notification, tying lab and sensor data to limits before a deadline.",
                    [["Quality Compliance Hub", "Lab results against limits with notification workflows."], ["Lakeflow", "SCADA, lab and AMI feeds conformed for quality analytics."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land SCADA historian tags, AMI interval reads, work orders and lab results; own Bronze to Silver and the pager when an NRW table stalls.",
                    [["Lakeflow Connect", "Managed connectors for CIS, SCADA and AMI sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on meter and telemetry feeds."], ["Lakewatch", "Freshness on the NRW tables the control room reads each shift."]]),
                biz("Data Scientists", "MLflow", "Leak-detection, demand-forecast, main-break and pump-optimisation models, and whether they still hold as weather and network state shift.",
                    [["Feature Store", "Meter and asset features read identically in training and serving."], ["MLflow", "Every leak and break-risk experiment tracked for audit."], ["Model Serving", "Leak and demand models scored in the operational path."]]),
                biz("App Developers", "Apps", "Ship the Network Control Center, Customer Impact and Quality Compliance apps control-room and quality teams work in, next to governed SCADA data.",
                    [["Apps", "Control-room screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for work order and notification state writes."], ["Agent Bricks", "Agents that draft pump setpoints against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Operations and regulatory dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for pressure and outage questions in the control room channel."),
                    tile("Notebooks & IDEs", "notebook", "Hydraulic and demand notebooks against governed SCADA and AMI data."),
                ]},
                {"box": "Customer & Agency", "ic": "partner", "tiles": [
                    tile("Outage Notification API", "api", "Estimated restoration and boil-water alerts pushed to customer channels.", "oracle-c2m"),
                    tile("Regional Intertie Portal", "share", "Wholesale flow and quality shared to regional agencies over Delta Sharing."),
                    tile("Contractor Work Portal", "globe", "Main replacement and inspection work packages shared to contractors.", "cityworks"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Pump Setpoint Adjust", "stream", "Optimised pump schedules written back to SCADA setpoints within limits.", "aveva-pi"),
                    tile("Field Work Orders", "apps", "Leak repair and meter exchange orders dispatched to crews.", "cityworks"),
                    tile("AMI Valves & Alerts", "iot", "Remote valve commands and customer leak notifications from AMI flags.", "itron"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("SDWIS Compliance", "gavel", "Sampling and exceedance reports filed to the primacy agency.", "epa-sdwis"),
                    tile("Consumer Confidence", "share", "Annual water quality reports published from contracted Gold products.", "hach-wims"),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Network and quality products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Regional agencies reading live flow via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Network Control Center", "SCADA ops", "gauge", "Live pressure, storage, pump status and AMI leak flags on Databricks Apps over Lakebase."),
             app("Customer Impact Console", "Outages & billing", "custlake", "Outage map, restoration ETA and high-bill triage for call centre agents."),
             app("Quality Compliance Hub", "Lab results", "gavel", "Sample results against regulatory limits with public notification workflows."),
             app("Main Replacement Planner", "Asset capex", "db", "Main break history and risk scores prioritising replacement capital.")],
            [uc("Leak Detection", "NRW", "iot", "Distribution leaks inferred from AMI night flow and pressure transients."),
             uc("Demand Forecasting", "Planning", "chart", "Consumption forecast by district, weather and season."),
             uc("Pressure Management", "Operations", "stream", "Pressure zones optimised for compliance and energy cost."),
             uc("Pump Optimization", "Energy", "iot", "Pump scheduling minimising energy while meeting storage targets."),
             uc("Water Quality Exceedance", "Compliance", "gavel", "Lab and online sensor exceedances flagged before reporting deadlines."),
             uc("Main Break Prediction", "Assets", "db", "Pipe material, age and soil corrosivity scored for break risk."),
             uc("Outage Response", "Customer", "gauge", "Outage scope, crew dispatch and restoration ETA for public communication."),
             uc("High Bill Investigation", "Billing", "market", "Unusual consumption patterns explained from AMI intervals."),
             uc("Capital Planning", "Finance", "erp", "Asset replacement and growth capital prioritised on risk and ROI."),
             uc("Drought Contingency", "Resilience", "globe", "Stage restrictions and supply alternatives modeled against source levels.")],
        ),
        "sources": {
            "oracle-c2m": {"t": "Oracle Utilities C2M", "u": "https://www.oracle.com/industries/utilities/"},
            "sap-isu": {"t": "SAP for Utilities", "u": "https://www.sap.com/industries/utilities.html"},
            "vertexone": {"t": "VertexOne", "u": "https://vertexone.net/"},
            "aveva-pi": {"t": "AVEVA PI System", "u": "https://www.aveva.com/en/products/pi-system/"},
            "ignition": {"t": "Ignition SCADA", "u": "https://inductiveautomation.com/"},
            "schneider-eco": {"t": "Schneider EcoStruxure", "u": "https://www.se.com/ww/en/work/solutions/system/s1/ecostruxure/"},
            "itron": {"t": "Itron OpenWay", "u": "https://www.itron.com/"},
            "sensus": {"t": "Sensus FlexNet", "u": "https://sensus.com/"},
            "badger": {"t": "Badger Meter Beacon", "u": "https://www.badgermeter.com/"},
            "esri-utility": {"t": "Esri ArcGIS Utility Network", "u": "https://www.esri.com/en-us/industries/water"},
            "maximo": {"t": "IBM Maximo", "u": "https://www.ibm.com/products/maximo"},
            "cityworks": {"t": "Cityworks AMS", "u": "https://www.cityworks.com/"},
            "hach-wims": {"t": "Hach WIMS", "u": "https://www.hach.com/"},
            "kisters": {"t": "KISTERS WISKI", "u": "https://www.kisters.net/"},
            "epa-sdwis": {"t": "EPA SDWIS", "u": "https://www.epa.gov/ground-water-and-drinking-water"},
            "noaa": {"t": "NOAA National Weather Service", "u": "https://www.weather.gov/"},
        },
    },
}
