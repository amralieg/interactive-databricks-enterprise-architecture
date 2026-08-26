import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_DATA_CENTERS = {
    "data_centers": {
        "label": "Data Centers & Cloud",
        "blurb": "Colocation and hyperscale data-center operations: DCIM and critical facilities, power and cooling efficiency, capacity and interconnection, energy and sustainability, and tenant service.",
        "medallion": medallion(
            "Raw facility & sensor feeds",
            "DCIM asset records, BMS BACnet and Modbus points, PDU branch-circuit power reads, chiller and CRAH telemetry, SNMP and NetFlow, access-control and video events and ServiceNow tickets, landed exactly as received so any PUE figure or outage can be replayed as it stood.",
            "Conformed site, asset, tenant",
            "Sites, halls, racks, power chains, cooling loops and tenants resolved into single conformed entities across the DCIM, BMS and ITSM estates, with sensor points reconciled to one tag namespace and alarms and access events joined to the assets they touch.",
            "PUE, uptime, capacity",
            "Contracted products operations and commercial run on: PUE and WUE by site, power and cooling capacity headroom, uptime and SLA compliance, interconnection utilisation and revenue, and metered tenant power billing.",
        ),
        "rails": {
            "src": [
                {
                    "box": "DCIM & Assets",
                    "ic": "erp",
                    "tiles": [
                        tile(
                            "EcoStruxure IT",
                            "erp",
                            "Schneider Electric EcoStruxure IT DCIM: the system of record for assets, power chains, rack and space allocation and environmental monitoring across the estate.",
                            "schneider",
                        ),
                        tile(
                            "Nlyte DCIM",
                            "erp",
                            "Carrier Nlyte data-center infrastructure management: asset lifecycle, workflow and capacity records, the incumbent inventory of what is racked where and on which circuit.",
                            "nlyte",
                        ),
                        tile(
                            "Sunbird dcTrack",
                            "sheet",
                            "Sunbird dcTrack DCIM: rack elevations, power-port and network-port connectivity and capacity, the source for space, power and cooling headroom by cabinet.",
                            "sunbird",
                        ),
                        tile(
                            "Vertiv Environet",
                            "observ",
                            "Vertiv Environet monitoring: real-time power, cooling and environmental alarms and trends across critical infrastructure, the operator's view of live facility health.",
                            "vertiv-env",
                        ),
                    ],
                },
                {
                    "box": "Building & Power",
                    "ic": "iot",
                    "tiles": [
                        tile(
                            "JCI Metasys",
                            "iot",
                            "Johnson Controls Metasys building automation: the BMS that runs cooling plant, air handling and building systems and publishes the setpoints and status the floor operates on.",
                            "jci",
                        ),
                        tile(
                            "Siemens Desigo CC",
                            "iot",
                            "Siemens Desigo CC building management: a common BMS platform for HVAC, power and environmental supervision where Metasys is not the incumbent, feeding the same point data.",
                            "siemens",
                        ),
                        tile(
                            "Vertiv Liebert iCOM",
                            "iot",
                            "Vertiv Liebert thermal controls and CRAC/CRAH units: chilled-water and DX cooling status, fan speed and return-air temperature, the raw signal for cooling optimisation.",
                            "liebert",
                        ),
                        tile(
                            "Schneider PowerLogic",
                            "gauge",
                            "Schneider PowerLogic power monitoring: switchgear, UPS and branch-circuit metering across the power chain, the electrical ground truth behind PUE and billing.",
                            "powerlogic",
                        ),
                    ],
                },
                {
                    "box": "Environmental & IoT",
                    "ic": "stream",
                    "tiles": [
                        tile(
                            "BACnet & Modbus",
                            "stream",
                            "Temperature, humidity, differential-pressure and leak sensors published over the BACnet and Modbus protocols the building estate speaks, parsed on arrival as structured events.",
                            "bacnet",
                        ),
                        tile(
                            "Ignition SCADA",
                            "iot",
                            "Inductive Automation Ignition SCADA: supervisory control and historian for electrical and mechanical plant, the tag store many operators standardise facility telemetry on.",
                            "ignition",
                        ),
                        tile(
                            "PDU Branch Metering",
                            "gauge",
                            "Intelligent rack PDUs from Raritan and Server Technology reporting per-outlet and branch-circuit power, the meter behind tenant billing and stranded-capacity analysis.",
                            "raritan",
                        ),
                    ],
                },
                {
                    "box": "Interconnect & Net",
                    "ic": "network",
                    "tiles": [
                        tile(
                            "Equinix Fabric",
                            "network",
                            "Equinix Fabric software-defined interconnection: cross-connects, virtual connections and fabric ports, the record of who is connected to whom across the meet-me room.",
                            "equinix",
                        ),
                        tile(
                            "Digital Realty Fabric",
                            "network",
                            "Digital Realty PlatformDIGITAL ServiceFabric: interconnection and connectivity records where Digital Realty is the operator, feeding the same utilisation and revenue view.",
                            "digitalrealty",
                        ),
                        tile(
                            "SolarWinds NPM",
                            "observ",
                            "SolarWinds Network Performance Monitor: SNMP-polled device health, interface utilisation and up/down state across the facility network fabric.",
                            "solarwinds",
                        ),
                        tile(
                            "Kentik NPM",
                            "network",
                            "Kentik network observability: flow, BGP and traffic-engineering telemetry, the demand signal that justifies interconnection capacity and pricing.",
                            "kentik",
                        ),
                    ],
                },
                {
                    "box": "Service & Physical Sec",
                    "ic": "gavel",
                    "tiles": [
                        tile(
                            "ServiceNow ITSM",
                            "opdb",
                            "ServiceNow IT Service Management: incidents, changes and work orders raised against facility and IT assets, the process record from alarm to resolved ticket.",
                            "servicenow",
                        ),
                        tile(
                            "Genetec Security",
                            "zshield",
                            "Genetec Security Center: unified access control and video surveillance across the perimeter, halls and cages, the source of who entered where and when.",
                            "genetec",
                        ),
                        tile(
                            "Lenel OnGuard",
                            "key",
                            "LenelS2 OnGuard access control: badge, door and alarm events across the physical estate where OnGuard is the incumbent, feeding the same physical-security view.",
                            "lenel",
                        ),
                        tile(
                            "Tenant Billing",
                            "market",
                            "The colocation billing and contract system carrying committed power and space, metered usage rules and SLA terms, reconciled against the meters that actually recorded draw.",
                        ),
                    ],
                },
                fed_group(
                    "Utility & Energy Mkts",
                    "Utility interval-meter reads, wholesale energy-market prices and renewable-energy-certificate and PPA registries left in their existing warehouses and queried in place under Unity Catalog, so cost and carbon attribution join facility telemetry without a second copy.",
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "SNMP & Telemetry",
                        "stream",
                        "SNMP traps, syslog and NetFlow from power, cooling and network gear polled continuously and landed as governed events for real-time facility and network analysis.",
                        "snmp",
                    ),
                    tile(
                        "Kafka Sensor Bus",
                        "eventbus",
                        "High-frequency BMS, PDU and environmental events carried on existing Kafka topics, consumed continuously into the lakehouse for near-real-time cooling and power analytics.",
                        "kafka",
                    ),
                    tile(
                        "MQTT Gateway",
                        "iot",
                        "Edge sensor and controller telemetry published to an MQTT broker at the site, bridged into the lakehouse so hall-level readings arrive at the cadence they are sampled.",
                        "mqtt",
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Executive Team",
                        "Genie One",
                        "The CEO on capacity, uptime and the cost of powering AI-era demand; the CFO on capital deployment across sites and the return on every megawatt; the COO on availability, SLA exposure and the sustainability commitments made to investors and tenants.",
                        [
                            ["Genie One", "Ask what a site cost to run last month, or where capacity is stranded, without booking analyst time."],
                            ["AI/BI", "PUE, uptime, capacity headroom and energy cost on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the glossary, so \"PUE\" and \"availability\" mean one thing across every site."],
                        ],
                        sub=[
                            ["CEO", "capacity, uptime and the cost of powering AI-era demand."],
                            ["CFO", "capital deployment across sites and return on every megawatt."],
                            ["COO", "availability, SLA exposure and sustainability commitments."],
                        ],
                        ucs=["Capacity Planning", "PUE & Sustainability", "Energy Procurement", "Uptime & Availability"],
                    ),
                    biz(
                        "Facilities Ops",
                        "Lakehouse//RT",
                        "Critical facility engineers watching the power chain and cooling loops on a live floor, shift operators in the NOC acknowledging alarms against the clock, and mechanical and electrical teams keeping UPS, generators and chillers inside their operating envelope.",
                        [
                            ["Critical Ops Cockpit", "Power-chain, cooling and alarm state on one screen before an operator escalates."],
                            ["Lakehouse//RT", "BMS, PDU and chiller telemetry at the latency a thermal event moves at."],
                            ["Model Serving", "Cooling-setpoint and failure-risk models scored inline against live conditions."],
                        ],
                        sub=[
                            ["Critical facility eng", "the power chain and cooling loops on a live floor."],
                            ["NOC operators", "alarm acknowledgement and first-response triage."],
                            ["M&E engineers", "UPS, generator and chiller operating envelopes."],
                        ],
                        ucs=["Cooling Optimization", "Predictive Maintenance", "Incident & Change", "Uptime & Availability"],
                    ),
                    biz(
                        "Capacity & IX",
                        "AI/BI",
                        "Capacity planners tracking power, cooling and space headroom hall by hall before a sales commitment strands a cabinet, and interconnection product managers monetising cross-connects and fabric ports across the meet-me room.",
                        [
                            ["Capacity Planner", "Power, cooling and space headroom and stranded capacity by hall on governed data."],
                            ["AI/BI", "Utilisation, headroom and interconnection revenue on the definitions the board reads."],
                            ["Genie", "Plain-English questions on where the next cabinet or cross-connect can land."],
                        ],
                        sub=[
                            ["Capacity planners", "power, cooling and space headroom by hall."],
                            ["Interconnection PMs", "cross-connect and fabric-port monetisation."],
                        ],
                        ucs=["Capacity Planning", "Interconnect Revenue"],
                    ),
                    biz(
                        "Sustainability",
                        "Model Serving",
                        "Energy procurement teams hedging and buying power against volatile wholesale markets, and ESG and sustainability leads accounting for PUE, WUE and Scope 1-3 carbon across the estate for regulators, investors and tenants.",
                        [
                            ["PUE Optimizer", "Cooling and PUE recommendations reconciled against the carbon and cost they move."],
                            ["Model Serving", "Load, price and carbon-intensity forecasts scored behind procurement and reporting."],
                            ["AI/BI", "PUE, WUE and Scope 1-3 emissions on governed, audit-ready Gold tables."],
                        ],
                        sub=[
                            ["Energy procurement", "hedging and buying power against wholesale markets."],
                            ["ESG & sustainability", "PUE, WUE and Scope 1-3 carbon accounting."],
                        ],
                        ucs=["PUE & Sustainability", "Energy Procurement"],
                    ),
                    biz(
                        "Service & Sec",
                        "Agent Bricks",
                        "Incident and change managers running the ITSM process when an alarm becomes a ticket, physical-security teams watching access control and video across the perimeter, and tenant-success and billing teams reconciling metered power draw against colocation contracts.",
                        [
                            ["Tenant Portal", "Metered power, billing, SLA and interconnection self-service for every tenant."],
                            ["Agent Bricks", "Agents that triage an alarm, draft a change record or answer a tenant query against governed tools."],
                            ["Lakehouse//RT", "Access-control, video and ITSM events joined to the assets they touch, live."],
                        ],
                        sub=[
                            ["Incident & change mgrs", "the ITSM process from alarm to resolved ticket."],
                            ["Physical security", "access control and video across the perimeter."],
                            ["Tenant success & billing", "metered power reconciled against colo contracts."],
                        ],
                        ucs=["Incident & Change", "Physical Security", "Tenant Billing & SLA"],
                    ),
                ],
                [
                    biz(
                        "DC Data Engineers",
                        "Lakeflow",
                        "Land DCIM asset records, BMS BACnet and Modbus points, PDU branch-circuit power reads and SNMP and NetFlow telemetry; own the Bronze-to-Silver path and the pager when a facility feed stalls.",
                        [
                            ["Lakeflow Connect", "Managed connectors for DCIM, ITSM and BMS historian sources."],
                            ["Auto Loader", "Incremental ingestion of high-frequency sensor and meter files into conformed tables."],
                            ["Lakeflow", "Declarative pipelines with expectations on every power, cooling and network feed."],
                        ],
                    ),
                    biz(
                        "Optimization Eng",
                        "Model Serving",
                        "Build cooling-setpoint and PUE-optimisation models against BMS and chiller telemetry, and remaining-useful-life models on UPS, battery and CRAH condition data, and keep them honest six months after deployment.",
                        [
                            ["Feature Store", "Sensor features defined once and read identically in training and serving."],
                            ["MLflow", "Every optimisation and RUL run tracked for audit and reproduction."],
                            ["Model Serving", "Setpoint and failure-risk models scored in the operational control path."],
                        ],
                    ),
                    biz(
                        "Ops App Devs",
                        "Apps",
                        "Ship the NOC, capacity and tenant applications the operator works in, hosted next to governed facility data with governed writes back to ITSM and DCIM.",
                        [
                            ["Apps", "Operational screens with no separate web tier to run or secure."],
                            ["Lakebase", "Serverless Postgres for ticket, work-order and acknowledgement state."],
                            ["Agent Bricks", "Agents that draft a change record or a tenant answer against governed tools."],
                        ],
                    ),
                ],
            ),
            "cons": cons_rail(
                [
                    {
                        "box": "BI & Productivity",
                        "ic": "chart",
                        "from": "bi",
                        "tiles": [
                            tile(
                                "Power BI / Tableau",
                                "chart",
                                "Executive and operations dashboards against serverless SQL warehouses, with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for Unity Catalog-governed answers from the facility lakehouse, and incident and capacity updates in the channel operations already works in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Engineer and analyst notebooks, VS Code and JetBrains against governed facility data and Genie Code.",
                            ),
                        ],
                    },
                    {
                        "box": "NOC & Alerting",
                        "ic": "gauge",
                        "tiles": [
                            tile(
                                "PagerDuty / Opsgenie",
                                "gauge",
                                "Scored, correlated alarms routed to the on-call rotation so the one incident that matters pages a human, not the whole storm.",
                            ),
                            tile(
                                "NOC Dashboards",
                                "chart",
                                "Live power-chain, cooling and network state surfaced to the network operations centre with recommended actions attached.",
                            ),
                            tile(
                                "Alarm Correlation",
                                "stream",
                                "BMS, PDU and network alarms clustered into incidents in near real time so operators triage causes, not a flood of symptoms.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "ServiceNow Work Orders",
                                "opdb",
                                "Predicted failures and correlated incidents raised as work orders and change records in ServiceNow, in the system operations already runs.",
                                "servicenow",
                            ),
                            tile(
                                "DCIM Writeback",
                                "db",
                                "Reconciled capacity, connectivity and asset state written back into DCIM so the inventory operations plans against stays true.",
                            ),
                            tile(
                                "Setpoint Advisories",
                                "iot",
                                "Cooling-setpoint recommendations delivered as advisories to controls engineers, who apply them in the BMS rather than a model driving plant directly.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & ESG",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "ESG & Carbon Report",
                                "gavel",
                                "PUE, WUE and Scope 1-3 emissions reporting for CSRD and investor disclosure, produced from the same governed tables the floor runs on.",
                            ),
                            tile(
                                "SLA & Uptime Report",
                                "gavel",
                                "Contracted uptime and service-credit reporting to tenants produced from contracted Gold products rather than reassembled by hand under deadline.",
                            ),
                            tile(
                                "Audit Evidence",
                                "docs",
                                "Immutable query and access logs proving who saw what and when, covering facility and tenant audit requirements without extra instrumentation.",
                            ),
                        ],
                    },
                    {
                        "box": "Sharing & Products",
                        "ic": "product",
                        "tiles": [
                            tile(
                                "Data Products",
                                "product",
                                "Published, contracted facility and tenant products discoverable in Unity Catalog Domains and shared over Open Sharing.",
                            ),
                            tile(
                                "Tenant Data Sharing",
                                "share",
                                "Live power, uptime and interconnection data shared to each tenant over Delta Sharing with no copy and no egress duplication.",
                            ),
                            tile(
                                "Sharing Recipients",
                                "share",
                                "Partners, utilities and regulators reading live governed tables directly rather than by nightly file exchange.",
                            ),
                        ],
                    },
                ]
            ),
        },
        "top": top_band(
            [
                app(
                    "Critical Ops Cockpit",
                    "Live facility state",
                    "gauge",
                    "The screen the NOC and critical-facility engineers run a floor from: power-chain, cooling and alarm state, correlated into the one incident that matters, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Capacity Planner",
                    "Power & space headroom",
                    "sheet",
                    "Power, cooling and space headroom and stranded capacity by hall and cabinet, so a sales commitment lands where capacity actually exists rather than behind a full breaker.",
                ),
                app(
                    "PUE Optimizer",
                    "Cooling efficiency",
                    "chart",
                    "Cooling-setpoint and airflow recommendations scored against live heat load and reconciled to the PUE, cost and carbon they move, delivered as advisories to the controls team.",
                ),
                app(
                    "Tenant Portal",
                    "Billing & SLA",
                    "product",
                    "Metered power, billing, SLA and interconnection self-service for every tenant, served from governed data and shared live over Delta Sharing.",
                ),
            ],
            [
                uc(
                    "Cooling Optimization",
                    "Efficiency",
                    "iot",
                    "Optimising chiller, CRAH and airflow setpoints against live heat load to cut the cooling energy that is a third of a site's power, without leaving the thermal envelope.",
                    problem="Cooling runs on static, conservative setpoints tuned for the worst case, so a third of site power is spent holding halls colder than the live heat load actually needs.",
                    who="Facilities Ops",
                    how="BMS, chiller and PDU telemetry lands in Lakehouse//RT; setpoint models tracked in MLflow score against live load in Model Serving and are surfaced as advisories in the Critical Ops Cockpit.",
                    comps=["Critical Ops Cockpit", "Lakehouse//RT", "Model Serving", "JCI Metasys", "MLflow"],
                    stories=[
                        ["Schneider Electric industrialises energy AI on Databricks", "https://www.databricks.com/blog/ai-doesnt-scale-until-you-stop-calling-it-innovation"],
                        ["Databricks IoT platform for predictive maintenance and optimization", "https://www.databricks.com/resources/demos/tutorials/lakehouse-platform/iot-and-predictive-maintenance"],
                    ],
                ),
                uc(
                    "PUE & Sustainability",
                    "Carbon & PUE",
                    "chart",
                    "Measuring PUE, WUE and Scope 1-3 carbon across the estate from the same governed telemetry the floor runs on, so a disclosure is produced continuously rather than reassembled each quarter.",
                    problem="PUE, WUE and carbon are reassembled by hand each reporting cycle from meters, spreadsheets and vendor portals the auditors cannot see into, so disclosures lag the operation by a quarter.",
                    who="Sustainability",
                    how="Meter, BMS and utility feeds are conformed to Gold with lineage in Unity Catalog; PUE, WUE and Scope 1-3 emissions are published as governed Data Products and read in AI/BI.",
                    comps=["AI/BI", "Unity Catalog", "Utility & Energy Mkts", "Data Products", "PDU Branch Metering"],
                    stories=[
                        ["How Dow built a carbon footprint ledger on Databricks", "https://www.databricks.com/blog/how-dow-built-carbon-footprint-ledger-databricks-accelerate-sustainability-scale"],
                        ["Vattenfall quantifies carbon impact at second-level granularity", "https://www.databricks.com/customers/vattenfall/genie"],
                    ],
                ),
                uc(
                    "Predictive Maintenance",
                    "Critical plant",
                    "iot",
                    "Predicting UPS, battery, generator and CRAH failures from condition telemetry so a component is changed on a planned window instead of tripping a live floor.",
                    problem="Critical plant is maintained on a calendar rather than its condition, so a failing UPS string or battery is discovered when it trips a floor, not on a planned window.",
                    who="Facilities Ops",
                    how="PDU, BMS and Vertiv Environet condition data feed remaining-useful-life models tracked in MLflow and scored in Model Serving; predicted failures raise work orders from the Critical Ops Cockpit.",
                    comps=["Critical Ops Cockpit", "Vertiv Environet", "MLflow", "Model Serving", "Lakeflow"],
                    stories=[
                        ["Predictive maintenance on the Databricks Lakehouse", "https://www.databricks.com/blog/what-is-predictive-maintenance"],
                        ["Turning predictive-maintenance scores into a reliability app", "https://developers.databricks.com/perspectives/databricks-supports-predictive-maintenance-iot-analytics-for-energy-operations"],
                    ],
                ),
                uc(
                    "Capacity Planning",
                    "Headroom",
                    "sheet",
                    "Tracking power, cooling and space headroom cabinet by cabinet so a sales commitment lands where capacity exists instead of stranding a megawatt behind a full breaker.",
                    problem="Power, cooling and space are tracked in separate DCIM, BMS and spreadsheet views, so capacity is sold against stale headroom and megawatts strand behind full breakers and hot aisles.",
                    who="Capacity & IX",
                    how="DCIM, branch-circuit and cooling feeds are conformed in the lakehouse; headroom and stranded capacity by hall are modelled and explored in the Capacity Planner on AI/BI.",
                    comps=["Capacity Planner", "AI/BI", "Sunbird dcTrack", "Nlyte DCIM", "Schneider PowerLogic"],
                    stories=[
                        ["E.ON unifies energy asset data on the Databricks Platform", "https://www.databricks.com/customers/eon"],
                    ],
                ),
                uc(
                    "Interconnect Revenue",
                    "Meet-me room",
                    "network",
                    "Monetising cross-connects and fabric ports by joining interconnection records to network telemetry, so the meet-me room is priced and provisioned on real utilisation.",
                    problem="Interconnection revenue and port utilisation live in the fabric platform while the traffic that justifies them lives in network telemetry, so cross-connects are priced and provisioned blind to real use.",
                    who="Capacity & IX",
                    how="Equinix Fabric and Digital Realty records are joined to SolarWinds and Kentik telemetry in the lakehouse; utilisation and revenue are surfaced through AI/BI and the Tenant Portal.",
                    comps=["Equinix Fabric", "Digital Realty Fabric", "Kentik NPM", "AI/BI", "Tenant Portal"],
                ),
                uc(
                    "Incident & Change",
                    "ITSM",
                    "opdb",
                    "Correlating the alarm storm into the one incident that matters and scoring the risk of every change before it touches a live floor.",
                    problem="A single fault throws hundreds of BMS and network alarms into ServiceNow at once and change risk is judged on memory, so the real incident is buried and risky changes reach live floors.",
                    who="Service & Sec",
                    how="Alarms and tickets from ServiceNow ITSM and the BMS estate are correlated in Lakehouse//RT; an agent on Agent Bricks drafts the incident and flags change risk against history.",
                    comps=["ServiceNow ITSM", "Lakehouse//RT", "Agent Bricks", "SNMP & Telemetry", "AI Functions"],
                ),
                uc(
                    "Energy Procurement",
                    "Power buying",
                    "market",
                    "Buying and hedging power against volatile wholesale markets from a forecast of site load and carbon intensity, instead of a static block bought a year ahead.",
                    problem="Power is the largest operating cost and is bought against static blocks and gut feel, so the operator is exposed to spot volatility and misses the carbon-intensity windows that cut cost and emissions.",
                    who="Sustainability",
                    how="Site-load, market-price and carbon-intensity feeds are conformed to Gold; forecasts scored in Model Serving inform hedging and demand-response decisions read in AI/BI.",
                    comps=["Model Serving", "AI/BI", "Utility & Energy Mkts", "Delta Lake", "Lakeflow"],
                    stories=[
                        ["Helen forecasts energy demand and production with Databricks", "https://www.databricks.com/customers/helen"],
                        ["Vattenfall builds real-time energy-market intelligence", "https://www.databricks.com/customers/vattenfall/genie"],
                    ],
                ),
                uc(
                    "Physical Security",
                    "Access & video",
                    "zshield",
                    "Fusing access-control and video events with facility state to flag tailgating, anomalous access and perimeter risk before it becomes an incident.",
                    problem="Access control, video and facility systems each see one slice, so tailgating and anomalous after-hours access only surface on a manual review of footage after something has already gone wrong.",
                    who="Service & Sec",
                    how="Genetec and Lenel events are joined to facility state in the lakehouse; anomaly models in Model Serving flag risk to the Critical Ops Cockpit and physical-security teams.",
                    comps=["Genetec Security", "Lenel OnGuard", "Model Serving", "Lakehouse//RT", "Critical Ops Cockpit"],
                ),
                uc(
                    "Tenant Billing & SLA",
                    "Metering",
                    "product",
                    "Billing metered power draw and reporting SLA and uptime to every tenant from branch-circuit meters, so an invoice and a service credit come from the same governed record.",
                    problem="Metered power for billing and uptime for SLA credits are pulled from different systems by hand, so invoices are late, disputes are common, and a service credit is argued rather than evidenced.",
                    who="Service & Sec",
                    how="PDU branch-circuit reads and power-chain uptime are conformed to Gold; tenant billing, SLA and interconnection views are served through the Tenant Portal and shared over Delta Sharing.",
                    comps=["Tenant Portal", "PDU Branch Metering", "Tenant Billing", "Data Products", "Unity Catalog"],
                    stories=[
                        ["Databricks Data Intelligence Platform for Energy (AMI metering)", "https://www.databricks.com/company/newsroom/press-releases/databricks-launches-data-intelligence-platform-energy-bringing"],
                    ],
                ),
                uc(
                    "Uptime & Availability",
                    "Resilience",
                    "gauge",
                    "Forecasting availability risk across the power and cooling chain so the operator defends the uptime SLA before a redundancy is quietly lost, not after an outage.",
                    problem="Redundancy is assumed until an outage proves it was lost weeks earlier; availability risk hides across UPS, generator, cooling and network layers that no single system watches together.",
                    who="Facilities Ops",
                    how="Power, cooling and network telemetry are unified in Lakehouse//RT; availability-risk models in Model Serving forecast single points of failure and surface them in the Critical Ops Cockpit.",
                    comps=["Critical Ops Cockpit", "Lakehouse//RT", "Model Serving", "SolarWinds NPM", "Vertiv Environet"],
                    stories=[
                        ["Databricks for Energy: forecast load and predict outages", "https://www.databricks.com/company/newsroom/press-releases/databricks-launches-data-intelligence-platform-energy-bringing"],
                        ["E.ON improves grid asset management on Databricks", "https://www.databricks.com/customers/eon"],
                    ],
                ),
            ],
        ),
        "sources": {
            "schneider": {"t": "Schneider Electric EcoStruxure IT", "u": "https://www.se.com/us/en/product-range/64046-ecostruxure-it/"},
            "nlyte": {"t": "Carrier Nlyte DCIM", "u": "https://www.nlyte.com/"},
            "sunbird": {"t": "Sunbird dcTrack DCIM", "u": "https://www.sunbirddcim.com/"},
            "vertiv-env": {"t": "Vertiv Environet monitoring", "u": "https://www.vertiv.com/en-us/products-catalog/monitoring-control-and-management/"},
            "jci": {"t": "Johnson Controls Metasys", "u": "https://www.johnsoncontrols.com/building-automation-and-controls/building-management/building-automation-systems/metasys-building-automation-system"},
            "siemens": {"t": "Siemens Desigo CC", "u": "https://www.siemens.com/global/en/products/buildings/automation/desigo/building-management.html"},
            "liebert": {"t": "Vertiv Liebert thermal management", "u": "https://www.vertiv.com/en-us/products/brands/liebert/"},
            "powerlogic": {"t": "Schneider PowerLogic power monitoring", "u": "https://www.se.com/us/en/product-range/62306-powerlogic/"},
            "bacnet": {"t": "BACnet building protocol", "u": "https://www.bacnet.org/"},
            "ignition": {"t": "Inductive Automation Ignition SCADA", "u": "https://inductiveautomation.com/ignition/"},
            "raritan": {"t": "Raritan intelligent rack PDUs", "u": "https://www.raritan.com/products/power-distribution/rack-pdus"},
            "equinix": {"t": "Equinix Fabric interconnection", "u": "https://www.equinix.com/interconnection-services/equinix-fabric"},
            "digitalrealty": {"t": "Digital Realty PlatformDIGITAL ServiceFabric", "u": "https://www.digitalrealty.com/platform-digital/servicefabric"},
            "solarwinds": {"t": "SolarWinds Network Performance Monitor", "u": "https://www.solarwinds.com/network-performance-monitor"},
            "kentik": {"t": "Kentik network observability", "u": "https://www.kentik.com/"},
            "servicenow": {"t": "ServiceNow IT Service Management", "u": "https://www.servicenow.com/products/itsm.html"},
            "genetec": {"t": "Genetec Security Center", "u": "https://www.genetec.com/products/unified-security/security-center"},
            "lenel": {"t": "LenelS2 OnGuard access control", "u": "https://www.lenels2.com/"},
            "snmp": {"t": "SNMP network management protocol", "u": "https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol"},
            "kafka": {"t": "Apache Kafka", "u": "https://kafka.apache.org/"},
            "mqtt": {"t": "MQTT IoT messaging protocol", "u": "https://mqtt.org/"},
        },
    }
}
