import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_PUBLIC_SAFETY = {
    "public_safety": {
        "label": "Public Safety",
        "blurb": "Police, fire, EMS and emergency management: computer-aided dispatch and 911 call handling, records and digital evidence, crime analysis, and coordinated multi-agency response.",
        "medallion": medallion(
            "Raw responder system feeds",
            "CAD incidents and unit statuses, 911 and NG911 call records, records-management reports, body-worn and in-car video metadata, ALPR reads and ePCR patient-care records landed exactly as received, so any incident or call can be replayed as it stood for court and audit.",
            "Conformed incident, unit, person",
            "Incidents, units, people, vehicles and locations resolved into single conformed entities across the dispatch, records, evidence and fire/EMS estates, with master names and addresses reconciled and CJIS-controlled records governed under one access model.",
            "Response time, clearance, safety",
            "Contracted products command and oversight run on: response time by call type and beat, case clearance rates, calls-for-service demand by hour and location, use-of-force and early-intervention indicators, and NIBRS, NFIRS and NEMSIS reporting.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Dispatch & 911",
                    "ic": "stream",
                    "tiles": [
                        tile(
                            "Tyler Enterprise CAD",
                            "stream",
                            "Enterprise Public Safety computer-aided dispatch: the system of record for calls for service, unit assignment and incident timestamps.",
                            "tyler-cad",
                        ),
                        tile(
                            "Hexagon CAD",
                            "stream",
                            "HxGN OnCall Dispatch: incident intake, resource recommendation and unit status used by large agencies and consolidated dispatch centres.",
                            "hexagon-cad",
                        ),
                        tile(
                            "Carbyne NG911",
                            "dial",
                            "Cloud-native NG911 call handling with caller location and live video, the front door for emergency calls into the CAD estate.",
                            "carbyne",
                        ),
                        tile(
                            "CentralSquare CAD",
                            "stream",
                            "Public-safety CAD and 911 used across many city and county agencies, feeding the same incident and unit entities.",
                            "centralsquare",
                        ),
                    ],
                },
                {
                    "box": "Records & Jail",
                    "ic": "erp",
                    "tiles": [
                        tile(
                            "Mark43 RMS",
                            "db",
                            "Cloud records management: incident and arrest reports, case files and NIBRS-ready records, the system of record for what happened after the call.",
                            "mark43",
                        ),
                        tile(
                            "Tyler Odyssey Court",
                            "gavel",
                            "Enterprise Justice court case management: charges, dispositions and warrants shared with law enforcement and corrections.",
                            "odyssey",
                        ),
                        tile(
                            "Guardian RFID JMS",
                            "gavel",
                            "Jail management: booking, classification, housing and inmate movement tracked as the custody record of the facility.",
                            "guardian-rfid",
                        ),
                    ],
                },
                {
                    "box": "Digital Evidence",
                    "ic": "media",
                    "tiles": [
                        tile(
                            "Axon Evidence",
                            "media",
                            "Digital evidence management: body-worn and in-car video, photos and files with chain of custody, the evidence estate of record.",
                            "axon",
                        ),
                        tile(
                            "Axon Body 4",
                            "media",
                            "Body-worn cameras streaming live and uploading recordings, the source of the video every review and disclosure request draws on.",
                            "axon-body",
                        ),
                        tile(
                            "Genetec Clearance",
                            "share",
                            "Digital evidence sharing and redaction across agencies and prosecutors, the disclosure path for video and case files.",
                            "genetec",
                        ),
                        tile(
                            "Flock Safety ALPR",
                            "network",
                            "Automatic licence-plate recognition cameras generating plate reads matched against wanted and missing-person lists.",
                            "flock",
                        ),
                    ],
                },
                {
                    "box": "Fire & EMS",
                    "ic": "iot",
                    "tiles": [
                        tile(
                            "ImageTrend ePCR",
                            "docs",
                            "Electronic patient-care records and fire incident reporting: the NEMSIS and NFIRS-ready record of every EMS and fire response.",
                            "imagetrend",
                        ),
                        tile(
                            "ESO EHR",
                            "docs",
                            "EMS electronic health records and fire records, feeding patient outcomes, response intervals and quality review.",
                            "eso",
                        ),
                        tile(
                            "First Due Fire",
                            "gauge",
                            "Fire prevention, inspections and pre-incident planning: the building, hydrant and inspection record behind risk-based deployment.",
                            "firstdue",
                        ),
                    ],
                },
                {
                    "box": "GIS & Telemetry",
                    "ic": "globe",
                    "tiles": [
                        tile(
                            "Esri ArcGIS",
                            "globe",
                            "The GIS of record: beats, parcels, hydrants and service geographies and the spatial layers behind hotspots, coverage and response.",
                            "arcgis-esri",
                        ),
                        tile(
                            "AVL Telemetry",
                            "iot",
                            "Automatic vehicle location and unit telemetry from patrol cars, fire apparatus and ambulances, the ground truth for travel time.",
                        ),
                        tile(
                            "FirstNet Broadband",
                            "network",
                            "The first-responder broadband network carrying location, status and field data from responders back to the operations picture.",
                            "firstnet",
                        ),
                    ],
                },
                fed_group(
                    "CJIS Repository",
                    "State criminal-justice and NCIC/III record stores left where they are and queried in place under Unity Catalog, so CJIS-controlled records are never needlessly copied.",
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "RapidSOS API",
                        "api",
                        "Device and app emergency data, precise caller location and medical profiles, streamed into the 911 and CAD picture.",
                        "rapidsos",
                    ),
                    tile(
                        "ShotSpotter Alerts",
                        "stream",
                        "Acoustic gunshot detection alerts with location and time, ingested as events for real-time response and analysis.",
                        "shotspotter",
                    ),
                    tile(
                        "Weather & Traffic",
                        "globe",
                        "National Weather Service and traffic feeds joined for demand forecasting, routing and disaster response.",
                        "nws",
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Command Staff",
                        "Genie One",
                        "The police chief on crime trends and clearance; the fire chief and EMS medical director on response times and unit availability; the emergency manager on a live common picture when a storm or mass-casualty event stretches every agency at once.",
                        [
                            ["Genie One", "Ask what response times or calls for service looked like last night across the city without booking an analyst."],
                            ["AI/BI", "Response times, clearance and calls-for-service demand on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the glossary, so \"response time\" and \"cleared\" mean one thing across every agency."],
                        ],
                        sub=[
                            ["Police Chief", "crime trends, clearance rates and the deployment that moves them."],
                            ["Fire Chief", "response times, unit availability and station coverage."],
                            ["Emergency Manager", "a live common operating picture across agencies in a disaster."],
                        ],
                        ucs=["Response Times", "Real-Time Crime", "Disaster Response"],
                    ),
                    biz(
                        "Patrol Ops",
                        "Lakehouse//RT",
                        "Watch commanders and dispatch supervisors running the shift: which units are available, where calls are stacking, and how long the queue is before the next car clears, on the day it is happening rather than in a monthly report.",
                        [
                            ["Lakehouse//RT", "Live CAD, unit and call-queue state at the latency a shift moves at."],
                            ["AI/BI", "Beat-level response times and calls-for-service load on governed data."],
                            ["Model Serving", "Demand and staffing models that flag where the next car will be needed."],
                        ],
                        sub=[
                            ["Watch Commander", "unit availability and the call queue across the shift."],
                            ["Dispatch Supervisor", "911 and CAD load, hold times and unit assignment."],
                            ["Field Supervisor", "officer status, backup and scene safety."],
                        ],
                        ucs=["Response Times", "Real-Time Crime", "Officer Safety"],
                    ),
                    biz(
                        "Investigations",
                        "AI Functions",
                        "Detectives and crime analysts working cases: linking incidents into patterns, searching hours of body-worn and in-car video and digital evidence, and turning ALPR reads and BOLOs into leads instead of a backlog.",
                        [
                            ["AI Functions", "Transcription, summarisation and search over evidence run in SQL on governed data."],
                            ["AI Search", "Semantic search across case notes, reports and evidence transcripts."],
                            ["Model Serving", "Pattern and hotspot models scored into the analyst workflow."],
                        ],
                        sub=[
                            ["Detectives", "case linkage, evidence review and leads."],
                            ["Crime Analysts", "hotspots, patterns and bulletins for deployment."],
                            ["Digital Evidence", "chain of custody, redaction and disclosure."],
                        ],
                        ucs=["Crime Analytics", "Evidence Search", "ALPR & BOLO"],
                    ),
                    biz(
                        "Fire & EMS",
                        "Model Serving",
                        "Fire operations and EMS medical directors on demand and risk: where the next call will fall, which properties carry the highest fire risk, and whether ambulances are staged where the calls actually are.",
                        [
                            ["Model Serving", "Demand and fire-risk models scored into deployment and inspection planning."],
                            ["AI/BI", "Calls-for-service demand, turnout time and unit-hour utilisation on certified views."],
                            ["Feature Store", "Property, weather and history features read identically in training and serving."],
                        ],
                        sub=[
                            ["Fire Operations", "turnout time, station coverage and move-up."],
                            ["EMS Medical Director", "ambulance demand, response intervals and patient outcomes."],
                            ["Fire Prevention", "risk-based inspection targeting across the building stock."],
                        ],
                        ucs=["EMS Demand", "Fire Risk", "Disaster Response"],
                    ),
                    biz(
                        "Prof Standards",
                        "AI/BI",
                        "The accountability and community-trust side of the house: internal affairs and early-intervention review, records and CJIS compliance, and the transparency numbers the agency publishes to the public it serves.",
                        [
                            ["AI/BI", "Use-of-force, complaint and early-intervention indicators on governed data."],
                            ["Unity Catalog", "CJIS-aligned access, lineage and audit across every record."],
                            ["Genie One", "Ask which indicators are trending or which records an audit needs without a manual pull."],
                        ],
                        sub=[
                            ["Internal Affairs", "complaints, use-of-force review and early intervention."],
                            ["Records & CJIS", "record retention, disclosure and CJIS-compliant access."],
                            ["Community Relations", "the transparency numbers published to the public."],
                        ],
                        ucs=["Use of Force", "Evidence Search", "Crime Analytics"],
                    ),
                ],
                [
                    biz(
                        "Data Engineers",
                        "Lakeflow",
                        "Land the CAD, 911, RMS, digital-evidence and fire/EMS feeds from Tyler, Hexagon, Carbyne, Mark43, Axon and ImageTrend; own the Bronze to Silver path and the pager when a response-time table stalls.",
                        [
                            ["Lakeflow Connect", "Managed connectors for CAD, RMS and SaaS public-safety systems."],
                            ["Lakeflow Designer", "Declarative pipelines with expectations on incident and call feeds."],
                            ["Lakewatch", "Freshness on the tables the watch and command staff read every shift."],
                        ],
                    ),
                    biz(
                        "GIS Analysts",
                        "Model Serving",
                        "Beats, parcels, hydrants and service geographies from Esri ArcGIS joined to incident and call data, and the spatial models behind hotspots, station coverage and disaster response.",
                        [
                            ["Model Serving", "Spatial hotspot, demand and risk models scored in the operational path."],
                            ["Feature Store", "Geography and location features read identically in training and serving."],
                            ["AI Functions", "Geocoding and address matching run in SQL against governed data."],
                        ],
                    ),
                    biz(
                        "App Developers",
                        "Apps",
                        "Ship the RTCC, response-time and evidence applications the agencies work in, hosted next to governed data with governed writes back to CAD and records.",
                        [
                            ["Apps", "Command-centre and field screens with no separate web tier to secure."],
                            ["Lakebase", "Serverless Postgres for case, BOLO and workflow state."],
                            ["Agent Bricks", "Agents that draft a bulletin or evidence summary against governed tools."],
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
                                "Tableau / Power BI",
                                "chart",
                                "Command and oversight dashboards against serverless SQL with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for Unity Catalog-governed answers in the channel command staff already work in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Analyst notebooks, VS Code and JetBrains against governed incident, call and evidence data.",
                            ),
                        ],
                    },
                    {
                        "box": "Public & Partners",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "Community Portal",
                                "globe",
                                "Public crime maps and transparency numbers served to residents from governed Gold products.",
                            ),
                            tile(
                                "Regional Sharing",
                                "share",
                                "Mutual-aid and neighbouring agencies reading live incident and BOLO tables over Delta Sharing instead of file exchange.",
                            ),
                            tile(
                                "Genie for Field",
                                "genie",
                                "Plain-language answers about incidents, records and BOLOs grounded in governed data for officers in the field.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "CAD Writeback",
                                "stream",
                                "Recommended unit and ETA decisions written back into CAD so the answer reaches the dispatcher in the moment.",
                                "tyler-cad",
                            ),
                            tile(
                                "RMS Case Update",
                                "db",
                                "Linked incidents, patterns and clearances written back into the records system investigators work in.",
                                "mark43",
                            ),
                            tile(
                                "BOLO & Alerts",
                                "dial",
                                "Plate hits, wanted matches and officer-safety alerts pushed to mobile data terminals and field devices.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "NIBRS Submission",
                                "gavel",
                                "National Incident-Based Reporting System crime submissions produced from the same governed tables the agency runs on.",
                                "nibrs",
                            ),
                            tile(
                                "NFIRS / NERIS",
                                "share",
                                "National fire incident reporting to USFA, produced from conformed fire and EMS Gold products.",
                                "nfirs",
                            ),
                            tile(
                                "NEMSIS EMS",
                                "docs",
                                "National EMS Information System patient-care reporting filed from governed ePCR data.",
                                "nemsis",
                            ),
                        ],
                    },
                    {
                        "box": "Published Products",
                        "ic": "product",
                        "tiles": [
                            tile(
                                "Data Products",
                                "product",
                                "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing.",
                            ),
                            tile(
                                "Sharing Recipients",
                                "share",
                                "Other agencies, prosecutors and researchers reading live tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ]
            ),
        },
        "top": top_band(
            [
                app(
                    "RTCC Cockpit",
                    "Real-time crime center",
                    "gauge",
                    "The screen a real-time crime centre runs on: live 911 and CAD calls, nearby cameras, ALPR reads and gunshot alerts fused on a map so operators guide responding officers with current ground truth, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Response Time Board",
                    "Dispatch to on-scene",
                    "stream",
                    "Live response-time state by call type and beat against target, flagging the calls holding in queue so supervisors move units before the standard is missed.",
                ),
                app(
                    "Evidence Finder",
                    "Search & redaction",
                    "media",
                    "Where investigators search transcribed body-worn and in-car video, case notes and reports by what was said and seen, with redaction and disclosure tracked for court.",
                ),
                app(
                    "EMS Demand Planner",
                    "Ambulance deployment",
                    "iot",
                    "Predicted calls for service by hour and location so ambulances are staged where the next call will fall instead of chasing it across town.",
                ),
            ],
            [
                uc(
                    "Response Times",
                    "Dispatch performance",
                    "stream",
                    "Response time attacked end to end: call-taking, dispatch and travel measured by call type and beat so the delay is moved before the standard is missed, not explained after.",
                    problem="Response time is reported monthly and in aggregate, so a beat that is slipping is discovered weeks late and the call-taking, dispatch and travel components are never separated to see where the time actually goes.",
                    who="Patrol Ops",
                    how="CAD and 911 call events stream into Lakehouse//RT and are conformed to certified Metric Views; the Response Time Board flags calls holding in queue so supervisors move units before the standard is missed.",
                    comps=["Response Time Board", "Lakehouse//RT", "Tyler Enterprise CAD", "AI/BI", "Esri ArcGIS"],
                    stories=[
                        ["Databricks for state & local public safety", "https://www.databricks.com/solutions/industries/state-local-government"],
                        ["Public sector: real-time emergency response", "https://www.databricks.com/solutions/industries/public-sector"],
                    ],
                ),
                uc(
                    "Real-Time Crime",
                    "Live common picture",
                    "gauge",
                    "A real-time crime centre that fuses 911 and CAD calls, cameras, ALPR reads and gunshot alerts into one live picture so operators guide officers on current ground truth.",
                    problem="When a call comes in, operators piece the picture together from separate systems, cameras, ALPR, 911 and CAD that do not talk, so officers arrive with less context than the data already holds.",
                    who="Patrol Ops",
                    how="Call, camera, ALPR and gunshot feeds land in Lakehouse//RT and are fused on a map in the RTCC Cockpit; proximity and risk models in Model Serving surface the feeds that matter for each call.",
                    comps=["RTCC Cockpit", "Lakehouse//RT", "ShotSpotter Alerts", "Flock Safety ALPR", "Model Serving"],
                    stories=[
                        ["Telefónica Tech: predictive policing on Databricks Genie", "https://www.databricks.com/blog/transforming-industries-conversational-ai-partner-solutions-built-databricks-genie"],
                        ["Databricks for state & local public safety", "https://www.databricks.com/solutions/industries/state-local-government"],
                    ],
                ),
                uc(
                    "Crime Analytics",
                    "Hotspots & patterns",
                    "chart",
                    "Linking incidents into patterns and hotspots across records and calls for service so deployment is driven by where and when crime actually concentrates, with plain-language questions instead of a monthly report.",
                    problem="Crime patterns hide across records, calls for service and partner data that rarely sit together, so hotspots and series are spotted late and deployment lags the trend.",
                    who="Investigations",
                    how="RMS and calls-for-service data are conformed under Unity Catalog; hotspot and pattern models score in Model Serving and analysts ask questions in Genie against certified data.",
                    comps=["Mark43 RMS", "AI/BI", "Model Serving", "Esri ArcGIS", "Genie One"],
                    stories=[
                        ["Telefónica Tech: predictive policing on Databricks Genie", "https://www.databricks.com/blog/transforming-industries-conversational-ai-partner-solutions-built-databricks-genie"],
                        ["ArcGIS GeoAnalytics Engine on Databricks", "https://www.databricks.com/blog/2022/12/07/arcgis-geoanalytics-engine-databricks.html"],
                    ],
                ),
                uc(
                    "Evidence Search",
                    "Video & case search",
                    "media",
                    "Making hours of body-worn and in-car video, case notes and reports searchable by what was said and seen, with redaction and disclosure tracked so evidence reaches court on time.",
                    problem="Digital evidence piles up faster than anyone can review it, and finding the moment that matters means scrubbing hours of video by hand while disclosure deadlines run.",
                    who="Investigations",
                    how="Evidence metadata and transcripts are governed in Unity Catalog; AI Functions transcribe and summarise while AI Search finds the moment across the case, surfaced in the Evidence Finder.",
                    comps=["Evidence Finder", "Axon Evidence", "AI Functions", "AI Search", "Unity Catalog"],
                    stories=[
                        ["Databricks for state & local public safety", "https://www.databricks.com/solutions/industries/state-local-government"],
                    ],
                ),
                uc(
                    "ALPR & BOLO",
                    "Plate reads & alerts",
                    "network",
                    "Turning ALPR reads and BOLOs into timely leads, matching plate reads against wanted and missing-person lists and pushing alerts to the field before the vehicle is gone.",
                    problem="ALPR generates millions of reads that mostly sit unqueried, so a hit against a wanted or missing-person list arrives too late to act on, or never surfaces at all.",
                    who="Investigations",
                    how="Plate reads land in Lakehouse//RT and match against governed watch-lists in Model Serving; hits push to the field through BOLO & Alerts with evidence linked in Genetec Clearance.",
                    comps=["Flock Safety ALPR", "Model Serving", "Lakehouse//RT", "BOLO & Alerts", "Genetec Clearance"],
                    stories=[
                        ["Databricks for state & local public safety", "https://www.databricks.com/solutions/industries/state-local-government"],
                    ],
                ),
                uc(
                    "Officer Safety",
                    "Responder telemetry",
                    "iot",
                    "Bringing first-responder location, status and telemetry together over broadband so a supervisor sees a responder in trouble and moves backup before a check-in is missed.",
                    problem="Officer status lives on the radio and in the supervisor's head, so a responder in trouble is noticed when a check-in is missed rather than when the signals first turn.",
                    who="Patrol Ops",
                    how="FirstNet location and telemetry feeds stream into Lakehouse//RT; models flag distress and isolation in Model Serving so supervisors move backup before a check-in is missed.",
                    comps=["FirstNet Broadband", "AVL Telemetry", "Lakehouse//RT", "Model Serving", "Lakeflow"],
                    stories=[
                        ["Public sector: safer communities with real-time AI", "https://www.databricks.com/solutions/industries/public-sector"],
                    ],
                ),
                uc(
                    "EMS Demand",
                    "Ambulance deployment",
                    "iot",
                    "Forecasting calls for service by hour and location so ambulances and crews are staged where the next call will fall instead of chasing it across the service area.",
                    problem="Ambulances are posted on static plans, so crews are in the wrong place when demand shifts and response intervals stretch on exactly the calls that matter most.",
                    who="Fire & EMS",
                    how="ePCR and historical call data are conformed with weather and event features; demand models score in Model Serving and the EMS Demand Planner recommends staging by hour and post.",
                    comps=["EMS Demand Planner", "ImageTrend ePCR", "Model Serving", "AI/BI", "Esri ArcGIS"],
                    stories=[
                        ["ArcGIS GeoAnalytics Engine on Databricks", "https://www.databricks.com/blog/2022/12/07/arcgis-geoanalytics-engine-databricks.html"],
                        ["Public sector: real-time emergency response", "https://www.databricks.com/solutions/industries/public-sector"],
                    ],
                ),
                uc(
                    "Fire Risk",
                    "Risk-based inspection",
                    "gauge",
                    "Scoring the building stock on fire risk from inspection, incident and property history so prevention targets the properties most likely to burn, not just the ones due on the calendar.",
                    problem="Inspections run on fixed cycles and complaints, so high-risk properties that have quietly slipped the queue keep slipping until an incident finds them first.",
                    who="Fire & EMS",
                    how="Inspection, incident and property records are unified under Unity Catalog; a risk model tracked in MLflow scores each property in Model Serving so First Due inspections target the highest risk.",
                    comps=["First Due Fire", "Model Serving", "AI/BI", "Esri ArcGIS", "MLflow"],
                    stories=[
                        ["ArcGIS GeoAnalytics Engine on Databricks", "https://www.databricks.com/blog/2022/12/07/arcgis-geoanalytics-engine-databricks.html"],
                        ["Databricks for state & local public safety", "https://www.databricks.com/solutions/industries/state-local-government"],
                    ],
                ),
                uc(
                    "Disaster Response",
                    "Multi-agency COP",
                    "globe",
                    "A live common operating picture across police, fire, EMS and emergency management in a storm or mass-casualty event, built from the same governed feeds every agency already sends.",
                    problem="In a disaster the operating picture is stitched together by hand from agency feeds that arrive too late and never agree, exactly when coordination matters most.",
                    who="Command Staff",
                    how="Incident, unit, GIS and weather feeds stream into Lakehouse//RT and are mapped against Esri layers; Genie answers situation questions in plain language so agencies act on one picture.",
                    comps=["Lakehouse//RT", "Esri ArcGIS", "Weather & Traffic", "AI/BI", "Lakeflow"],
                    stories=[
                        ["Slalom LakeSpeak: real-time emergency reports on Databricks", "https://www.databricks.com/blog/transforming-industries-conversational-ai-partner-solutions-built-databricks-genie"],
                        ["State of Washington builds data-driven government", "https://www.databricks.com/customers/state-of-washington"],
                    ],
                ),
                uc(
                    "Use of Force",
                    "Accountability",
                    "gavel",
                    "Bringing use-of-force, complaint and early-intervention indicators together so supervisors and internal affairs see a pattern forming while there is still time to intervene.",
                    problem="Use-of-force and complaint signals sit in separate systems, so an officer trending toward trouble is recognised after an incident rather than in the early-intervention window.",
                    who="Prof Standards",
                    how="Use-of-force, complaint and body-worn evidence are conformed under Unity Catalog; early-intervention indicators surface in AI/BI so supervisors act within the window, with the numbers published for transparency.",
                    comps=["Axon Evidence", "AI/BI", "Unity Catalog", "Genie One", "Mark43 RMS"],
                    stories=[
                        ["Fatal force: analyzing police shootings on Databricks", "https://www.databricks.com/blog/2020/11/16/fatal-force-exploring-police-shootings-with-sql-analytics.html"],
                        ["Databricks for state & local public safety", "https://www.databricks.com/solutions/industries/state-local-government"],
                    ],
                ),
            ],
        ),
        "sources": {
            "tyler-cad": {"t": "Tyler Enterprise Public Safety (CAD)", "u": "https://www.tylertech.com/products/enterprise-public-safety"},
            "hexagon-cad": {"t": "Hexagon HxGN OnCall Dispatch", "u": "https://hexagon.com/products/hxgn-oncall-dispatch"},
            "carbyne": {"t": "Carbyne NG911 call handling", "u": "https://carbyne.com/"},
            "centralsquare": {"t": "CentralSquare Public Safety", "u": "https://www.centralsquare.com/"},
            "mark43": {"t": "Mark43 Records Management", "u": "https://mark43.com/"},
            "odyssey": {"t": "Tyler Enterprise Justice (Odyssey)", "u": "https://www.tylertech.com/products/enterprise-justice"},
            "guardian-rfid": {"t": "GUARDIAN RFID jail management", "u": "https://guardianrfid.com/"},
            "axon": {"t": "Axon Evidence (Evidence.com)", "u": "https://www.axon.com/products/axon-evidence"},
            "axon-body": {"t": "Axon Body 4 body-worn camera", "u": "https://www.axon.com/products/axon-body-4"},
            "genetec": {"t": "Genetec Clearance evidence sharing", "u": "https://www.genetec.com/products/operations/clearance"},
            "flock": {"t": "Flock Safety ALPR", "u": "https://www.flocksafety.com/"},
            "imagetrend": {"t": "ImageTrend ePCR & fire reporting", "u": "https://www.imagetrend.com/"},
            "eso": {"t": "ESO EMS & fire records", "u": "https://www.eso.com/"},
            "firstdue": {"t": "First Due fire prevention & inspections", "u": "https://www.firstdue.com/"},
            "arcgis-esri": {"t": "Esri ArcGIS", "u": "https://www.esri.com/en-us/arcgis/about-arcgis/overview"},
            "firstnet": {"t": "FirstNet responder broadband", "u": "https://www.firstnet.com/"},
            "rapidsos": {"t": "RapidSOS emergency data", "u": "https://rapidsos.com/"},
            "shotspotter": {"t": "SoundThinking ShotSpotter", "u": "https://www.soundthinking.com/"},
            "nws": {"t": "NOAA National Weather Service", "u": "https://www.weather.gov/"},
            "nibrs": {"t": "FBI NIBRS crime reporting", "u": "https://www.fbi.gov/how-we-can-help-you/more-fbi-services-and-information/ucr/nibrs"},
            "nfirs": {"t": "USFA NFIRS fire reporting", "u": "https://www.usfa.fema.gov/nfirs/"},
            "nemsis": {"t": "NEMSIS national EMS data", "u": "https://nemsis.org/"},
        },
    }
}
