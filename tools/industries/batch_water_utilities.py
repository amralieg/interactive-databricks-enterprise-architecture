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
                    [["Genie One", "Ask what last month's NRW was without analyst delay."], ["AI/BI", "Pressure and quality KPIs on certified Metric Views."], ["Unity Catalog", "One consumption definition across AMI and billing."]],
                    sub=[
                        ["General Manager", "cost per thousand gallons and the capital plan the board and rate case rest on."],
                        ["Chief Operating Officer", "non-revenue water and the response time when a main breaks or a zone loses pressure."],
                        ["CFO & Rates", "the revenue requirement, collections and the capital budget behind the next rate filing."],
                    ],
                    ucs=["Capital Planning", "Leak Detection", "Drought Contingency"]),
                biz("Distribution Ops", "Lakehouse//RT", "Control room operators on pressure, storage and pump scheduling, holding pressure zones in compliance while trimming energy at the pumps.",
                    [["Network Control Center", "Live SCADA, AMI leak flags and crew dispatch on one screen."], ["Lakehouse//RT", "Telemetry at control-room latency."]],
                    sub=[
                        ["Control Room Operators", "pressure, storage and pump status held in compliance across every zone each shift."],
                        ["Pump & Energy Lead", "pumping energy cost against tariff windows and tank targets."],
                        ["Leak & NRW Team", "night-flow anomalies and where to send crews to cut non-revenue water."],
                    ],
                    ucs=["Pressure Management", "Pump Optimization", "Leak Detection", "Outage Response"]),
                biz("Customer Operations", "CustomerLake", "Call centre and field service on outages, high-bill disputes and leak investigations, giving agents restoration ETA and account context.",
                    [["Customer Impact Console", "Outage map, estimated restoration and high-bill triage."], ["CustomerLake", "Account context without copying into a separate CRM."]],
                    sub=[
                        ["Call Centre Agents", "outage restoration ETAs and high-bill disputes answered on the first call."],
                        ["Field Service Dispatch", "leak, meter and service-line work orders routed to the right crew."],
                        ["Billing Analysts", "unusual consumption explained from meter intervals before a bill is disputed."],
                    ],
                    ucs=["Outage Response", "High Bill Investigation"]),
                biz("Asset Management", "AI/BI", "Engineers on main-replacement priority, pump health and capex planning, ranking mains on break risk, age and soil against renewal budget.",
                    [["AI/BI", "Asset risk and remaining life on certified views."], ["Genie One", "Ask which mains exceed break rate thresholds."]],
                    sub=[
                        ["Reliability Engineers", "main break risk, pipe condition and pump health across the network."],
                        ["Capital Planning", "the renewal and growth program ranked on risk, consequence and ROI."],
                        ["GIS & Asset Data", "the pipe, valve and hydrant network kept accurate for every risk model."],
                    ],
                    ucs=["Main Break Prediction", "Capital Planning", "Pump Optimization"]),
                biz("Water Quality", "Lakeflow", "Quality teams on sample results, regulatory exceedances and public notification, tying lab and sensor data to limits before a deadline.",
                    [["Quality Compliance Hub", "Lab results against limits with notification workflows."], ["Lakeflow", "SCADA, lab and AMI feeds conformed for quality analytics."]],
                    sub=[
                        ["Compliance Officers", "sampling results against limits and the primacy-agency reporting deadlines."],
                        ["Source Water Team", "raw-water quality and the drought and contamination risks to supply."],
                        ["Public Notification", "boil-water and exceedance notices issued to customers on time."],
                    ],
                    ucs=["Water Quality Exceedance", "Drought Contingency"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land SCADA historian tags, AMI interval reads, work orders and lab results; own Bronze to Silver and the pager when an NRW table stalls.",
                    [["Lakeflow Connect", "Managed connectors for CIS, SCADA and AMI sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on meter and telemetry feeds."], ["Lakewatch", "Freshness on the NRW tables the control room reads each shift."]],
                    sub=[
                        ["Ingestion Engineers", "SCADA historian, AMI reads, work orders and lab results landed reliably."],
                        ["Pipeline Owners", "Bronze-to-Silver quality and the pager when an NRW table stalls before a shift."],
                        ["Streaming Engineers", "control-room latency on pressure and leak-flag telemetry."],
                    ],
                    ucs=["Leak Detection", "Demand Forecasting", "Water Quality Exceedance"]),
                biz("Data Scientists", "MLflow", "Leak-detection, demand-forecast, main-break and pump-optimisation models, and whether they still hold as weather and network state shift.",
                    [["Feature Store", "Meter and asset features read identically in training and serving."], ["MLflow", "Every leak and break-risk experiment tracked for audit."], ["Model Serving", "Leak and demand models scored in the operational path."]],
                    sub=[
                        ["Hydraulic Modellers", "leak, demand and pressure models that hold as weather and network state shift."],
                        ["Asset Risk Modellers", "main-break and pump remaining-life scoring against condition data."],
                        ["MLOps", "every leak and break-risk model tracked, evaluated and monitored for audit."],
                    ],
                    ucs=["Leak Detection", "Demand Forecasting", "Main Break Prediction", "Pump Optimization"]),
                biz("App Developers", "Apps", "Ship the Network Control Center, Customer Impact and Quality Compliance apps control-room and quality teams work in, next to governed SCADA data.",
                    [["Apps", "Control-room screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for work order and notification state writes."], ["Agent Bricks", "Agents that draft pump setpoints against governed tools."]],
                    sub=[
                        ["App Engineers", "the control-room, customer and quality screens built on governed data."],
                        ["Integration Engineers", "work order and notification writeback state on Lakebase."],
                        ["Agent Developers", "agents that draft pump setpoints and outage notices against governed tools."],
                    ],
                    ucs=["Outage Response", "High Bill Investigation", "Water Quality Exceedance"]),
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
            [uc("Leak Detection", "NRW", "iot", "Distribution leaks inferred from AMI night flow and pressure transients.",
                problem="Distribution leaks hide as background loss until a main bursts, and crews chase them across thousands of miles of buried pipe with little night-flow evidence to say where to dig first.",
                who="Distribution Ops",
                how="AMI night-flow and PI pressure transients land in Lakehouse//RT and score against leak models in Model Serving, so anomalies surface on the Network Control Center for crew dispatch.",
                comps=["Network Control Center", "Itron OpenWay", "AVEVA PI System", "Model Serving", "Lakehouse//RT", "Delta Lake"],
                stories=[
                    ["Turning smart digital water meter data into autonomous actions", "https://www.databricks.com/customers/water-link"],
                    ["Pipeline Flow Monitoring", "https://www.databricks.com/blog/pipeline-flow-monitoring"],
                ]),
             uc("Demand Forecasting", "Planning", "chart", "Consumption forecast by district, weather and season.",
                problem="Demand is planned off last year's averages, so pumping, storage and purchases are set blind to weather, growth and seasonal swings, and the utility over-pumps or runs storage too low.",
                who="Distribution Ops",
                how="AMI intervals, weather and calendar features are engineered in Feature Store and forecast per district through Model Serving, published to planners on certified AI/BI Metric Views.",
                comps=["AI/BI", "Weather Forecast API", "Itron OpenWay", "Model Serving", "Feature Store", "Delta Lake"],
                stories=[
                    ["Sabesp Transforms Water Utility Operations with Lakehouse", "https://www.databricks.com/customers/sabesp"],
                ]),
             uc("Pressure Management", "Operations", "stream", "Pressure zones optimised for compliance and energy cost.",
                problem="Pressure zones are tuned by hand to avoid low-pressure complaints, so the network runs over-pressured, wasting pump energy and driving the main breaks and leakage it was meant to prevent.",
                who="Distribution Ops",
                how="PI pressure and Schneider PRV telemetry land in Lakehouse//RT and feed optimisation models in Model Serving, so setpoints hold compliance at lowest energy from the Network Control Center.",
                comps=["Network Control Center", "AVEVA PI System", "Schneider EcoStruxure", "Model Serving", "Lakehouse//RT"]),
             uc("Pump Optimization", "Energy", "iot", "Pump scheduling minimising energy while meeting storage targets.",
                problem="Pumps run on fixed schedules blind to tariff windows and tank state, so the utility burns energy at peak price and cycles equipment harder than storage targets actually require.",
                who="Distribution Ops",
                how="Pump, tank and tariff data feed scheduling models tracked in MLflow and scored in Model Serving, so optimised setpoints reach SCADA from the Network Control Center within hydraulic limits.",
                comps=["Network Control Center", "AVEVA PI System", "Model Serving", "MLflow", "Lakehouse//RT"],
                stories=[
                    ["Vattenfall Builds Real-Time Energy Intelligence", "https://www.databricks.com/customers/vattenfall/genie"],
                    ["What is Predictive Maintenance?", "https://www.databricks.com/blog/what-is-predictive-maintenance"],
                ]),
             uc("Water Quality Exceedance", "Compliance", "gavel", "Lab and online sensor exceedances flagged before reporting deadlines.",
                problem="Lab results and online sensor readings sit in separate systems, so a chlorine or turbidity exceedance can be missed until a reporting deadline or notification clock has already started.",
                who="Water Quality",
                how="Hach WIMS lab results and WISKI sensor series are conformed through Lakeflow under Unity Catalog and checked against limits, flagging exceedances early in the Quality Compliance Hub.",
                comps=["Quality Compliance Hub", "Hach WIMS", "KISTERS WISKI", "Lakeflow", "Unity Catalog"],
                stories=[
                    ["Turning smart digital water meter data into autonomous actions", "https://www.databricks.com/customers/water-link"],
                ]),
             uc("Main Break Prediction", "Assets", "db", "Pipe material, age and soil corrosivity scored for break risk.",
                problem="Mains are replaced on age alone, so sound pipe is dug up while corrosive-soil segments fail without warning, flooding streets and cutting service before any renewal budget reaches them.",
                who="Asset Management",
                how="Pipe material, age, break history and soil corrosivity from GIS and Maximo feed break-risk models in Model Serving tracked in MLflow, ranking segments in the Main Replacement Planner.",
                comps=["Main Replacement Planner", "Esri ArcGIS Utility", "IBM Maximo", "Model Serving", "MLflow", "Feature Store"],
                stories=[
                    ["What is Predictive Maintenance?", "https://www.databricks.com/blog/what-is-predictive-maintenance"],
                    ["Pipeline Flow Monitoring", "https://www.databricks.com/blog/pipeline-flow-monitoring"],
                ]),
             uc("Outage Response", "Customer", "gauge", "Outage scope, crew dispatch and restoration ETA for public communication.",
                problem="When a main breaks the call centre learns the scope from complaints, so agents cannot give a restoration time and crews are dispatched without knowing who is affected or how many.",
                who="Customer Operations",
                how="Network state, work orders and account data conform under Unity Catalog and surface in the Customer Impact Console on Lakebase, giving agents outage scope and a restoration ETA.",
                comps=["Customer Impact Console", "Cityworks AMS", "CustomerLake", "Lakebase", "AI/BI"]),
             uc("High Bill Investigation", "Billing", "market", "Unusual consumption patterns explained from AMI intervals.",
                problem="A high-bill dispute lands with no way to see the meter's own intervals, so agents open a field visit for what is usually a private-side leak or a seasonal fill the data already explains.",
                who="Customer Operations",
                how="AMI interval reads from Itron join billing from Oracle C2M in the Customer Impact Console, so agents and Genie explain a spike from the consumption pattern before a truck rolls.",
                comps=["Customer Impact Console", "Itron OpenWay", "Oracle Utilities C2M", "Genie One", "AI/BI"],
                stories=[
                    ["Turning smart digital water meter data into autonomous actions", "https://www.databricks.com/customers/water-link"],
                    ["Sabesp Transforms Water Utility Operations with Lakehouse", "https://www.databricks.com/customers/sabesp"],
                ]),
             uc("Capital Planning", "Finance", "erp", "Asset replacement and growth capital prioritised on risk and ROI.",
                problem="Renewal and growth capital is argued in spreadsheets, so replacement dollars chase the last failure instead of the risk-and-consequence ranking that would defend the plan to the board.",
                who="Asset Management",
                how="Asset condition, break risk and hydraulic constraint data are conformed under Unity Catalog and ranked on ROI in the Main Replacement Planner, published to finance on certified AI/BI views.",
                comps=["Main Replacement Planner", "IBM Maximo", "Esri ArcGIS Utility", "AI/BI", "Unity Catalog"],
                stories=[
                    ["How Scottish Water Made Its Capital Investment Data Conversational", "https://www.databricks.com/blog/how-scottish-water-made-its-capital-investment-data-conversational-databricks-genie"],
                ]),
             uc("Drought Contingency", "Resilience", "globe", "Stage restrictions and supply alternatives modeled against source levels.",
                problem="Drought stages are called late off manual reservoir reads, so restrictions and alternative-supply moves lag the shortage and the utility loses the lead time to soften customer impact.",
                who="GM & Executive Office",
                how="NOAA hydrology and forecast feeds join source-level and demand data on Delta Lake and model supply scenarios in Model Serving, so restriction stages and interties are planned in AI/BI.",
                comps=["NOAA Hydrology API", "Weather Forecast API", "Model Serving", "AI/BI", "Delta Lake"])],
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
