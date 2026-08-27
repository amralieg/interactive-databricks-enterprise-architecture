import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    """Business tiles plus an explicit, industry-specific Technical group of 3."""
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_ENERGY_UTILITIES = {
    'energy_utilities': {
        "label": "Energy & Utilities",
        "blurb": "Electric, gas and water utilities: AMI and SCADA, customer billing, grid operations, asset management and regulatory compliance.",
        "medallion": medallion(
            "Raw meter and SCADA",
            "AMI interval reads, SCADA analogs and events, CIS billing extracts, OMS outage tickets and GIS asset records, landed exactly as received so a meter read or a protection trip can always be replayed.",
            "Conformed meter, premise",
            "Meters, premises, feeders and assets resolved into single conformed entities across AMI, CIS and GIS, with service point identifiers reconciled and outage events stitched to affected customers.",
            "SAIDI, losses, collections",
            "Contracted products operations and regulators run on: SAIDI and SAIFI by circuit, technical and non-technical loss, collections effectiveness, and demand forecast accuracy.",
        ),
        "rails": {
            "src": [
                {"box": "Metering & AMI", "ic": "iot", "tiles": [
                    tile("Itron OpenWay", "iot", "Advanced metering infrastructure interval reads, voltage events and remote connect/disconnect commands.", "itron"),
                    tile("Landis+Gyr Gridstream", "iot", "Head-end collection, meter events and power-quality alarms from the AMI estate.", "landis-gyr"),
                    tile("Sensus FlexNet", "stream", "RF mesh AMI reads and endpoint alarms for water and electric deployments on FlexNet.", "sensus")
                ]},
                {"box": "SCADA & Grid Ops", "ic": "stream", "tiles": [
                    tile("AVEVA PI Historian", "db", "Substation analogs, breaker operations and equipment alarms at SCADA sampling rates.", "osisoft-pi"),
                    tile("GE Vernova ADMS", "gauge", "Distribution management: fault location, switching orders and restoration state for the control centre.", "ge-adms"),
                    tile("ABB Ellipse EAM", "erp", "Enterprise asset management: work orders, inspections and equipment condition for grid plant.", "abb-ellipse")
                ]},
                {"box": "Customer & Billing", "ic": "erp", "tiles": [
                    tile("SAP IS-U", "erp", "Utility customer master, rate schedules, billing determinants and payment history.", "sap-isu"),
                    tile("Oracle Utilities CCB", "db", "Customer care and billing for meter-to-cash, rate cases and collections workflows.", "oracle-ccb"),
                    tile("Kubra Payment Portal", "partner", "Customer self-service payments, paperless billing enrolment and outage notifications.", "kubra")
                ]},
                {"box": "GIS & Outage Mgmt", "ic": "globe", "tiles": [
                    tile("Esri ArcGIS Utility", "globe", "Network model, service territory and asset locations the field and planning teams navigate by.", "esri-utility"),
                    tile("Milsoft OMS", "gauge", "Outage management: trouble tickets, crew dispatch and ETR communicated to customers.", "milsoft-oms"),
                    tile("Weather & DER Telemetry", "iot", "Forecast feeds and behind-the-meter solar and battery inverter telemetry for net load planning.")
                ]},
                fed_group(
                    "Regulatory Cost Accounting",
                    "FERC and state jurisdictional cost ledgers left where they are and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("Green Button Connect", "api", "Customer-authorised interval usage from retailers and neighbouring utilities via Green Button standards.", "green-button"),
                tile("IEEE 2030.5 SEP2", "stream", "Smart Energy Profile demand-response events and thermostat enrollments parsed on arrival.", "ieee-2030"),
                tile("Weather Data Services", "globe", "Forecast and actual temperature feeds consumed inbound for load forecasting models.")
            ]),
            "ppl": ppl2([
                biz("CEO & COO", "Genie One", "The CEO on SAIDI reliability, rate-case outcomes and the capital plan; the COO on storm-response cost and how fast the last customer was restored.",
                    [["Genie One", "Ask what yesterday's SAIDI was by district without waiting on operations analytics."], ["AI/BI", "Reliability, losses and collections on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"outage\" means one thing across the utility."]],
                    sub=[
                        ["CEO", "SAIDI reliability, rate-case outcomes and the capital plan the board signs off."],
                        ["Chief Operating Officer", "storm-response cost and how fast the last customer was restored."],
                        ["CFO & Treasury", "the revenue requirement, capital spend and the return the commission allows."],
                    ],
                    ucs=["Storm Restoration", "Capital Planning", "Rate Design Analytics", "Load Forecasting"]),
                biz("Grid Operations", "Lakehouse//RT", "Control-centre operators and distribution planners on faults, switching orders and end-of-line voltage violations across blue-sky and storm days.",
                    [["OMS Control Tower", "Restoration options costed against crew capacity and critical customers."], ["Lakehouse//RT", "Live feeder state at the latency a storm moves at."], ["AI/BI", "SAIDI and momentary counts on governed definitions."]],
                    sub=[
                        ["Control-Centre Operators", "live feeder state, switching orders and end-of-line voltage on blue-sky and storm days."],
                        ["Distribution Planners", "hosting capacity, DER interconnection and where the next constraint lands."],
                        ["Storm Coordinators", "crew staging, mutual aid and estimated restoration times."],
                    ],
                    ucs=["Storm Restoration", "Voltage Management", "DER Orchestration", "Load Forecasting"]),
                biz("Customer Operations", "AI/BI", "Contact centre and field service on high-bill complaints, move-in and move-out volume, payment arrangements and collections effectiveness.",
                    [["AI/BI", "Call volume, first-call resolution and collections on certified Metric Views."], ["Genie One", "Ask which premises drove yesterday's complaint spike."], ["CustomerLake", "Segments and outreach without copying CIS profiles elsewhere."]],
                    sub=[
                        ["Contact Centre", "high-bill complaints, move-in and move-out volume and first-call resolution."],
                        ["Credit & Collections", "payment arrangements, delinquency and recoverable revenue."],
                        ["Revenue Protection", "meter tamper, theft cases and unbilled usage on the estate."],
                    ],
                    ucs=["Non-Technical Loss", "Customer Propensity"]),
                biz("Asset Management", "Lakeflow", "Engineering and vegetation management on inspection backlogs, transformer and conductor failure risk, and which assets to replace before the fault.",
                    [["Asset Health Cockpit", "Condition scores and work order backlog by feeder class."], ["Lakeflow", "AMI, inspection and work-order feeds conformed for asset analytics."], ["MLflow", "Failure-risk models tracked for audit and reproduction."]],
                    sub=[
                        ["Reliability Engineering", "transformer and conductor failure risk and the fault before it happens."],
                        ["Vegetation Management", "grow-in risk, trim-cycle prioritisation and ignition exposure."],
                        ["Capital Programs", "replacement prioritisation against reliability and financial targets."],
                    ],
                    ucs=["Vegetation Management", "Capital Planning", "Voltage Management"]),
                biz("Regulatory & Rates", "AI/BI", "Regulatory affairs on cost-of-service studies, class revenue requirements and rate design that survives a commission challenge.",
                    [["Rate Case Analytics", "Cost allocation and class revenue requirements on governed ledgers."], ["AI/BI", "Regulatory KPIs the commission and board read."], ["Unity Catalog", "One definition of revenue and plant investment across finance and operations."]],
                    sub=[
                        ["Rate Design", "class revenue requirements and cost causation that survives challenge."],
                        ["Regulatory Affairs", "commission filings, data requests and the reliability record."],
                        ["Cost of Service", "jurisdictional cost allocation across finance and operations."],
                    ],
                    ucs=["Rate Design Analytics", "Capital Planning"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the AMI, SCADA, CIS and GIS feeds; own the Bronze to Silver path and the pager when a meter or outage feed breaks.",
                    [["Lakeflow Connect", "Managed connectors for AMI head-ends, CIS and asset systems."], ["Lakeflow Designer", "Declarative pipelines with expectations on meter and outage feeds."], ["Lakewatch", "Freshness on the tables the control centre reads every morning."]],
                    sub=[
                        ["AMI & SCADA Pipelines", "meter head-end and substation feeds and the pager when a read stops landing."],
                        ["CIS & GIS Integration", "customer, premise and network-model reconciliation across systems."],
                        ["Streaming Platform", "storm-day event volume and the freshness the control centre reads by."],
                    ],
                    ucs=["Storm Restoration", "Load Forecasting", "Water Loss Management"]),
                biz("Data Scientists", "MLflow", "Load-forecasting, non-technical-loss and asset failure-risk models, and whether they still hold a season after deployment.",
                    [["Feature Store", "Premise and feeder features defined once for training and serving."], ["MLflow", "Every forecast and failure-risk run tracked for audit and reproduction."], ["Model Serving", "Load and loss models scored in the operational path."]],
                    sub=[
                        ["Forecasting", "short- and long-term demand under weather, DER and electrification."],
                        ["Loss & Fraud", "non-technical-loss and tamper models from AMI anomalies."],
                        ["Asset Risk", "failure-risk and remaining-life models on grid plant."],
                    ],
                    ucs=["Load Forecasting", "Non-Technical Loss", "Capital Planning", "Vegetation Management"]),
                biz("App Developers", "Apps", "Ship the OMS control tower, asset-health and collections applications operations works in, hosted next to governed data.",
                    [["Apps", "Storm and asset screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for restoration decisions and crew writes."], ["Agent Bricks", "Agents that draft a switching plan or work order against governed tools."]],
                    sub=[
                        ["Storm & Ops Apps", "the OMS control tower and switching screens operations runs a storm from."],
                        ["Asset & Collections Apps", "condition, work-order and revenue-recovery workbenches."],
                        ["Agents & Writeback", "switching-plan and work-order drafting against governed tools."],
                    ],
                    ucs=["Storm Restoration", "Capital Planning", "Non-Technical Loss"]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and storm updates in the channel operations already works in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("ADMS Switching Orders", "gauge", "Optimised switching steps written back into distribution management for operator approval.", "ge-adms"),
                    tile("OMS Crew Dispatch", "apps", "Crew assignments and ETR updates pushed to mobile devices in the field.", "milsoft-oms"),
                    tile("CIS Billing Adjustments", "erp", "High-bill remediation and payment-plan decisions written back into customer care and billing.", "oracle-ccb")
                ]},
                {"box": "Grid & Market Partners", "ic": "partner", "tiles": [
                    tile("ISO Market Data", "market", "LMP, dispatch and settlement files shared with the independent system operator under schedule."),
                    tile("Municipal Light & Power", "share", "Joint-use poles and mutual aid crews reading live outage tables over Delta Sharing."),
                    tile("DER Aggregators", "api", "Demand-response enrollments and dispatch signals exchanged through standard APIs.", "ieee-2030")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Reliability Reporting", "gavel", "SAIDI, SAIFI and major event day filings produced from the same governed tables operations runs on."),
                    tile("Rate Case Submissions", "share", "Cost-of-service and class revenue studies filed from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Municipalities, regulators and research partners reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("OMS Control Tower", "Storm restoration", "gauge", "The screen the control centre runs a major event from: crew dispatch, switching and ETR by feeder, on Databricks Apps over Lakebase."),
                app("Load Forecast Console", "Demand planning", "chart", "Weather-adjusted load scenarios scored against purchased power and DER availability before the trading desk commits."),
                app("Asset Health Cockpit", "Grid reliability", "iot", "Transformer and conductor condition ranked by failure risk so vegetation and replacement crews are sent before the fault."),
                app("Collections Workbench", "Revenue protection", "market", "High-bill and delinquency cases prioritised by recoverable revenue and vulnerable-customer flags."),
            ],
            [
                uc("Storm Restoration", "Reliability", "gauge", "Restoring feeders and customers after weather, optimising crew routing and switching against critical premises.",
                    problem="When a storm hits, outages, crews and switching orders live in separate systems, so the control centre restores feeders blind to which fix strands another circuit or a critical customer.",
                    who="Grid Operations",
                    how="AMI, SCADA and OMS feeds land in Lakehouse//RT; restoration and crew-routing options are scored in Model Serving and run from the OMS Control Tower on Lakebase, writing switching back to ADMS.",
                    comps=["OMS Control Tower", "Lakehouse//RT", "Model Serving", "GE Vernova ADMS", "Lakebase"],
                    stories=[
                        ["Alabama Power leverages Databricks for outage and storm modeling", "https://www.databricks.com/blog/alabama-power-leverages-databricks-outage-and-storm-modeling"],
                        ["Revolutionizing utility outage response with Databricks", "https://www.databricks.com/blog/revolutionizing-utility-outage-response"],
                    ]),
                uc("Load Forecasting", "Operations", "chart", "Short- and long-term demand forecasts that account for weather, DER and electrification load growth.",
                    problem="Demand is shifting under electrification, rooftop solar and heat waves, but forecasts built on last year's load and a spreadsheet miss the peaks that set purchased-power cost.",
                    who="Grid Operations",
                    how="Meter, weather and DER features are engineered in Feature Store and scored through Model Serving, tracked in MLflow, so the Load Forecast Console shows weather-adjusted load before the desk commits.",
                    comps=["Load Forecast Console", "Feature Store", "Model Serving", "MLflow", "Weather Data Services"],
                    stories=[
                        ["Unlocking the future of energy with smart meter innovation (Southern Company)", "https://www.databricks.com/blog/unlocking-future-energy-smart-meter-innovation"],
                    ]),
                uc("Non-Technical Loss", "Revenue", "market", "Theft and meter bypass detection from AMI anomalies, tamper flags and billing pattern divergence.",
                    problem="Theft and meter bypass hide inside millions of interval reads, and manual audits chase false alarms while genuine revenue leakage goes unbilled for months across the service territory.",
                    who="Customer Operations",
                    how="AMI anomalies, tamper flags and billing divergence are scored in Model Serving with AI Functions and ranked in the Collections Workbench, so investigators get dispatch-ready cases not raw meter dumps.",
                    comps=["Collections Workbench", "AI Functions", "Model Serving", "Itron OpenWay", "AI/BI"],
                    stories=[
                        ["Anomaly detection to prevent energy loss", "https://www.databricks.com/blog/anomaly-detection-prevent-energy-loss.html"],
                        ["Detect energy theft faster with Genie", "https://www.databricks.com/resources/demos/videos/detect-energy-theft-faster-genie"],
                    ]),
                uc("Voltage Management", "Power quality", "iot", "Conservation voltage reduction and capacitor switching scored against end-of-line voltage violations.",
                    problem="End-of-line voltage and capacitor state sit in SCADA historians, so conservation voltage reduction is run conservatively and the energy savings on the table are never actually captured.",
                    who="Grid Operations",
                    how="PI historian analogs stream into Lakehouse//RT and CVR set-points are scored in Model Serving, written back as capacitor and regulator steps through ADMS switching orders for operator approval.",
                    comps=["AVEVA PI Historian", "Model Serving", "Lakehouse//RT", "ADMS Switching Orders", "AI/BI"],
                    stories=[
                        ["Unlocking the future of energy with smart meter innovation (Southern Company)", "https://www.databricks.com/blog/unlocking-future-energy-smart-meter-innovation"],
                    ]),
                uc("Vegetation Management", "Asset risk", "sheet", "Trim cycles prioritised by grow-in risk and historical fault correlation, not calendar rotation alone.",
                    problem="Trim cycles run on a calendar, not on risk, so crews clear low-risk spans while a grow-in on a fault-prone feeder waits its rotation and becomes the next outage or ignition event.",
                    who="Asset Management",
                    how="Imagery, LiDAR and outage history are H3-indexed with Apache Spark and scored for grow-in risk in Model Serving, ranking spans in the Asset Health Cockpit against the ArcGIS network model.",
                    comps=["Asset Health Cockpit", "Apache Spark", "Model Serving", "Esri ArcGIS Utility", "AI/BI"],
                    stories=[
                        ["Nousot and Xcel Energy: geospatial AI for wildfire mitigation", "https://www.databricks.com/blog/nousot-and-xcel-energy-harnessing-ai-and-geospatial-intelligence-natural-disaster-mitigation"],
                    ]),
                uc("DER Orchestration", "Grid edge", "stream", "Behind-the-meter solar and batteries coordinated for peak shaving without violating feeder limits.",
                    problem="Behind-the-meter solar and batteries swing feeder load minute to minute, but dispatch signals and inverter telemetry live apart, so peak-shaving risks breaching thermal and voltage limits.",
                    who="Grid Operations",
                    how="Inverter and demand-response telemetry land in Lakehouse//RT over IEEE 2030.5, and dispatch set-points are scored in Model Serving and issued to DER aggregators, with feeder limits held in Lakebase.",
                    comps=["Lakehouse//RT", "Model Serving", "IEEE 2030.5 SEP2", "DER Aggregators", "Lakebase"],
                    stories=[
                        ["Octopus Energy builds the world's largest virtual power plant (2026 Customer Awards)", "https://www.databricks.com/blog/announcing-winners-2026-databricks-customer-awards"],
                    ]),
                uc("Customer Propensity", "Programs", "custlake", "Efficiency program uptake and payment-plan acceptance scored per premise from CIS and AMI history.",
                    problem="Efficiency programs and payment plans are marketed to everyone the same way, so uptake is low and the premises most likely to enrol or to default are never identified in advance.",
                    who="Customer Operations",
                    how="CIS and AMI history feed propensity features in Feature Store scored through Model Serving on CustomerLake, so outreach and payment-plan offers target the right premise without copying profiles.",
                    comps=["CustomerLake", "Model Serving", "Feature Store", "Oracle Utilities CCB", "AI/BI"]),
                uc("Rate Design Analytics", "Regulatory", "gavel", "Class revenue requirements and cost causation studies that survive regulatory challenge.",
                    problem="Cost-of-service and class revenue studies are rebuilt each rate case from ledgers spread across finance and operations, and a number that cannot be traced is one a commission can strike.",
                    who="Regulatory & Rates",
                    how="Jurisdictional cost ledgers are queried in place under Unity Catalog and modelled in AI/BI, so class revenue requirements and cost causation are filed as governed Rate Case Submissions that stand up.",
                    comps=["Regulatory Cost Accounting", "Unity Catalog", "AI/BI", "Rate Case Submissions", "Genie One"],
                    stories=[
                        ["Hawaiian Electric: AI agents transforming electric grid operations", "https://www.databricks.com/blog/manual-autonomous-how-ai-agents-are-transforming-electric-grid-operations"],
                    ]),
                uc("Water Loss Management", "Distribution", "stream", "District metering and acoustic leak correlation for water utilities reducing real and apparent losses.",
                    problem="Real and apparent water losses hide between district meters, and acoustic and flow signals arrive too sparsely and too late to localise a leak before it runs for weeks underground.",
                    who="Grid Operations",
                    how="District metering and acoustic sensor reads stream into Lakehouse//RT and are correlated in Model Serving against the ArcGIS network, flagging leak zones for crews before the loss compounds.",
                    comps=["Sensus FlexNet", "Lakehouse//RT", "Model Serving", "Esri ArcGIS Utility", "AI/BI"]),
                uc("Capital Planning", "Investment", "product", "Replacement prioritisation across transformers, mains and meters against reliability and financial targets.",
                    problem="Replacement budgets are split across transformers, mains and meters by age and gut feel, so capital chases the squeakiest asset rather than the one whose failure costs reliability the most.",
                    who="Asset Management",
                    how="Condition, failure-risk and criticality scores from Model Serving and MLflow are ranked in the Asset Health Cockpit against EAM work history, so capital follows reliability and financial impact.",
                    comps=["Asset Health Cockpit", "MLflow", "Model Serving", "ABB Ellipse EAM", "AI/BI"],
                    stories=[
                        ["AusNet Services predicts asset risk with Databricks", "https://www.databricks.com/customers/ausnet-services"],
                    ]),
            ],
        ),
        "sources": {
            "itron": {"t": "Itron OpenWay AMI", "u": "https://www.itron.com/na/solutions/what-we-enable/ami"},
            "landis-gyr": {"t": "Landis+Gyr Gridstream", "u": "https://www.landisgyr.com/"},
            "sensus": {"t": "Sensus FlexNet AMI", "u": "https://sensus.com/solutions/advanced-metering-infrastructure/"},
            "osisoft-pi": {"t": "AVEVA PI System", "u": "https://www.aveva.com/en/products/pi-system/"},
            "ge-adms": {"t": "GE Vernova grid software", "u": "https://www.gevernova.com/software"},
            "abb-ellipse": {"t": "Hitachi Energy Ellipse EAM", "u": "https://www.hitachienergy.com/"},
            "sap-isu": {"t": "SAP for Utilities", "u": "https://www.sap.com/industries/utilities.html"},
            "oracle-ccb": {"t": "Oracle Utilities Customer Care and Billing", "u": "https://www.oracle.com/industries/utilities/"},
            "kubra": {"t": "Kubra customer engagement", "u": "https://www.kubra.com/"},
            "esri-utility": {"t": "Esri ArcGIS Utility Network", "u": "https://www.esri.com/en-us/industries/utilities"},
            "milsoft-oms": {"t": "Milsoft Outage Management", "u": "https://www.milsoft.com/utility-solutions/"},
            "green-button": {"t": "Green Button data standard", "u": "https://www.greenbuttondata.org/"},
            "ieee-2030": {"t": "IEEE 2030.5 Smart Energy Profile", "u": "https://standards.ieee.org/standard/2030_5-2018.html"}
        },
    },
}
