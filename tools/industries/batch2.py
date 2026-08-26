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


INDUSTRIES_BATCH2 = {
    "education": {
        "label": "Education",
        "blurb": "Higher education and K-12: student lifecycle from inquiry through alumni, learning outcomes, financial aid, and campus operations.",
        "medallion": medallion(
            "Raw campus feeds",
            "SIS enrollments, LMS activity logs, admissions CRM events, aid awards and bursar transactions, landed exactly as received so a grade or an aid decision can always be replayed as it stood.",
            "Conformed student, course",
            "Students, courses, sections and terms resolved into single conformed entities across the SIS, LMS and CRM estates, with cross-system identifiers reconciled and transfer credit stitched to one academic record.",
            "Retention, enrollment, outcomes",
            "Contracted products academic and finance leaders run on: retention and persistence by cohort, enrollment yield and melt, learning outcome attainment, and aid packaging compliance.",
        ),
        "rails": {
            "src": [
                {"box": "Student Information", "ic": "erp", "tiles": [
                    tile("Ellucian Banner", "erp", "Student information system of record: enrollments, registrations, grades, degree progress and transcript history.", "ellucian-banner"),
                    tile("Workday Student", "erp", "Cloud SIS for academic records, advising holds, program completion and residency rules.", "workday-student"),
                    tile("Oracle PeopleSoft Campus", "db", "Campus solutions for admissions, records, financials and HR shared across the institution.", "peoplesoft-campus")
                ]},
                {"box": "Learning & Content", "ic": "notebook", "tiles": [
                    tile("Canvas LMS", "notebook", "Course shells, assignments, discussion activity and outcome mastery data from the primary learning environment.", "canvas-lms"),
                    tile("Blackboard Learn", "notebook", "LMS engagement, assessment attempts and content access for institutions on the Blackboard estate.", "blackboard"),
                    tile("Panopto Lecture Capture", "stream", "Recorded lecture views, watch time and search queries joined to course enrollment for engagement analysis.", "panopto")
                ]},
                {"box": "Admissions & CRM", "ic": "partner", "tiles": [
                    tile("Slate by Technolutions", "partner", "Inquiry, application, decision and yield events from the admissions CRM the recruitment team works in.", "slate"),
                    tile("Salesforce Education Cloud", "custlake", "Prospect journeys, recruiter activities and conversion funnels for institutions on Education Cloud.", "sf-edu-cloud"),
                    tile("National Student Clearinghouse", "share", "Enrollment verification, degree completion and transfer research files exchanged with peer institutions.", "nsc")
                ]},
                {"box": "Finance & Student Aid", "ic": "market", "tiles": [
                    tile("PowerFAIDS", "market", "Need analysis, packaging rules and ISIR-driven award letters the financial aid office certifies.", "powerfaids"),
                    tile("Nelnet Campus Commerce", "erp", "Tuition billing, payment plans and bursar receivables reconciled against enrollment status.", "nelnet"),
                    tile("Web & Portal Clickstream", "observ", "Prospect and student portal events from search through registration, joined to applications and enrollments.")
                ]},
                fed_group(
                    "Research Grants Ledger",
                    "Sponsored research accounting and effort certification marts left where they are and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("Ed-Fi Data Standard", "api", "Interoperable student and assessment APIs normalised on ingest for state reporting and district exchange.", "ed-fi"),
                tile("IMS Global LTI", "api", "Learning tool interoperability launches and grade passback events from third-party publishers.", "ims-lti"),
                tile("IPEDS / State Reporting", "gavel", "Federal and state compliance file layouts consumed inbound for validation before submission season.", "ipeds")
            ]),
            "ppl": ppl2([
                biz("President & Provost", "Genie One", "The president and provost on enrollment health, first-year retention and six-year completion, and the trade between access and net-tuition sustainability.",
                    [["Genie One", "Ask what fall enrollment looks like against target without waiting on institutional research."], ["AI/BI", "Retention, yield and net tuition on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"retention\" means one thing across campus."]]),
                biz("Registrar & Records", "AI/BI", "Official academic records, transfer articulation and degree-audit exceptions, and who is eligible to walk at commencement this term.",
                    [["AI/BI", "Registration velocity, credit accumulation and stop-out patterns on governed definitions."], ["Genie One", "Ask which programs are behind on degree progress this term."], ["Unity Catalog", "One definition of enrollment status across SIS and LMS."]]),
                biz("Student Success", "Model Serving", "Advising, tutoring and early-alert teams intervening on rising-risk students from LMS inactivity, grade slippage and aid gaps before one silently stops out.",
                    [["Retention Risk Hub", "Risk scores and recommended outreach before census."], ["Model Serving", "Persistence models scored against live LMS and SIS signals."], ["CustomerLake", "Student segments without copying profiles into a separate CDP."]]),
                biz("Admissions & Enrollment", "CustomerLake", "Recruitment yield by channel and territory, melt between deposit and day one, and section fill measured against instructional and housing capacity.",
                    [["Enrollment Forecast", "Cohort scenarios scored on instructional and housing capacity."], ["CustomerLake", "Prospect journeys joined to application and enrollment outcomes."], ["AI/BI", "Yield and melt dashboards the cabinet reads each cycle."]]),
                biz("Finance & Financial Aid", "AI/BI", "Net tuition revenue, the aid discount rate and packaging that stays inside federal Title IV rules while hitting the class the cabinet promised.",
                    [["Aid Packaging Workbench", "Award scenarios tested against policy before letters release."], ["AI/BI", "Discount rate and tuition revenue on certified Metric Views."], ["Unity Catalog", "One definition of aid and billing across bursar and aid systems."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the SIS, LMS and admissions CRM feeds; own the Bronze to Silver path and the pager when a nightly enrollment or grade load breaks.",
                    [["Lakeflow Connect", "Managed connectors for Banner, Canvas and Slate."], ["Lakeflow Designer", "Declarative pipelines with expectations on enrollment and grade feeds."], ["Lakewatch", "Freshness on the tables the registrar and advisors read every morning."]]),
                biz("Data Scientists", "MLflow", "Retention-risk, enrollment-yield and course-demand models, and whether they still hold a term after deployment.",
                    [["Feature Store", "Student features defined once and read identically in training and serving."], ["MLflow", "Every retention model run tracked for audit and reproduction."], ["Model Serving", "Persistence and yield models scored against live LMS and SIS signals."]]),
                biz("App Developers", "Apps", "Ship the advising, retention and aid-packaging applications the campus works in, hosted next to governed data.",
                    [["Apps", "Advising and retention screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for advising notes and aid-decision writes."], ["Agent Bricks", "Agents that draft outreach or an aid scenario against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and advising updates in the channel teams already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Student Systems", "ic": "opdb", "tiles": [
                    tile("Banner Registration Writeback", "db", "Section capacity and registration holds written back into the SIS so the answer reaches the student portal.", "ellucian-banner"),
                    tile("Canvas Grade Passback", "notebook", "Final grades and outcome mastery pushed to the LMS of record after faculty approval.", "canvas-lms"),
                    tile("Advising Mobile", "apps", "Early alerts, appointment notes and degree exceptions pushed to advisors in the field.")
                ]},
                {"box": "Learning Platforms", "ic": "partner", "tiles": [
                    tile("LTI Tool Provisioning", "api", "Publisher tools entitled from governed roster and outcome data rather than flat CSV exports.", "ims-lti"),
                    tile("Ed-Fi Partner Exchange", "share", "District and state partners reading roster and assessment tables over Delta Sharing.", "ed-fi"),
                    tile("Alumni & Advancement", "custlake", "Graduate outcomes and giving propensity shared to advancement without nightly flat files.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("IPEDS & Federal Reporting", "gavel", "IPEDS, Clery and financial responsibility metrics produced from the same governed tables the institution runs on.", "ipeds"),
                    tile("FERPA Audit Trail", "share", "Directory and disclosure logs filed from contracted Gold products for compliance review.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Consortia, researchers and state agencies reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Student 360", "Unified learner view", "custlake", "Every touchpoint from inquiry through alumni on one screen: academics, aid, engagement and risk, on Databricks Apps over Lakebase."),
                app("Retention Risk Hub", "Early intervention", "gauge", "Cohort risk ranked before census with recommended outreach and advising appointments queued for coordinators."),
                app("Course Demand Planner", "Section planning", "sheet", "Historical fill and waitlist patterns scored against instructional capacity before the schedule locks."),
                app("Aid Packaging Workbench", "Award decisions", "market", "Packaging scenarios tested against policy and budget before award letters release to students."),
            ],
            [
                uc("Early Alert & Retention", "Persistence", "gauge", "Identifying students likely to stop out from LMS inactivity, grades and aid gaps, and intervening before census."),
                uc("Enrollment Forecasting", "Capacity", "sheet", "Fall and spring headcount scenarios scored against housing, staffing and section capacity before the board commits."),
                uc("Learning Analytics", "Outcomes", "notebook", "Course and modality effectiveness measured on mastery and completion, not satisfaction surveys alone."),
                uc("Financial Aid Packaging", "Compliance", "market", "Need-based awards optimised within discount rate targets and federal packaging rules."),
                uc("Recruitment Yield", "Admissions", "partner", "Inquiry-to-enroll funnels by channel and territory, with melt between deposit and day one surfaced early."),
                uc("Curriculum Optimisation", "Programs", "sheet", "Which courses and pathways drive time-to-degree and which bottleneck completion."),
                uc("Accreditation Reporting", "Assurance", "gavel", "Learning outcomes and employment metrics produced from governed tables accreditors can trace."),
                uc("Space & Scheduling", "Operations", "stream", "Room utilisation and prime-time conflicts resolved before students register into overloaded sections."),
                uc("Alumni Engagement", "Advancement", "custlake", "Graduate outcomes and giving propensity scored from the same student record advancement already trusts."),
                uc("Research Compliance", "Grants", "product", "Effort certification and cost share reconciled against sponsored project ledgers without a second shadow mart."),
            ],
        ),
        "sources": {
            "ellucian-banner": {"t": "Ellucian Banner SIS", "u": "https://www.ellucian.com/solutions/ellucian-banner"},
            "workday-student": {"t": "Workday Student", "u": "https://www.workday.com/en-us/products/student.html"},
            "peoplesoft-campus": {"t": "Oracle PeopleSoft Campus Solutions", "u": "https://docs.oracle.com/en/applications/peoplesoft/campus-solutions/index.html"},
            "canvas-lms": {"t": "Instructure Canvas LMS", "u": "https://www.instructure.com/canvas"},
            "blackboard": {"t": "Anthology Blackboard Learn", "u": "https://www.anthology.com/products/teaching-and-learning/learning-effectiveness/blackboard"},
            "panopto": {"t": "Panopto video platform", "u": "https://www.panopto.com/"},
            "slate": {"t": "Technolutions Slate", "u": "https://technolutions.com/slate"},
            "sf-edu-cloud": {"t": "Salesforce Education Cloud", "u": "https://www.salesforce.com/education/"},
            "nsc": {"t": "National Student Clearinghouse", "u": "https://www.studentclearinghouse.org/"},
            "powerfaids": {"t": "PowerFAIDS", "u": "https://www.powerfaids.org/"},
            "nelnet": {"t": "Nelnet Campus Commerce", "u": "https://en.wikipedia.org/wiki/Nelnet"},
            "ed-fi": {"t": "Ed-Fi data standard", "u": "https://www.ed-fi.org/"},
            "ims-lti": {"t": "IMS Global Learning Tools Interoperability", "u": "https://www.imsglobal.org/activity/learning-tools-interoperability"},
            "ipeds": {"t": "IPEDS federal reporting", "u": "https://nces.ed.gov/ipeds/"}
        },
    },
    "energy_utilities": {
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
                    tile("OSIsoft PI Historian", "db", "Substation analogs, breaker operations and equipment alarms at SCADA sampling rates.", "osisoft-pi"),
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
                    [["Genie One", "Ask what yesterday's SAIDI was by district without waiting on operations analytics."], ["AI/BI", "Reliability, losses and collections on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"outage\" means one thing across the utility."]]),
                biz("Grid Operations", "Lakehouse//RT", "Control-centre operators and distribution planners on faults, switching orders and end-of-line voltage violations across blue-sky and storm days.",
                    [["OMS Control Tower", "Restoration options costed against crew capacity and critical customers."], ["Lakehouse//RT", "Live feeder state at the latency a storm moves at."], ["AI/BI", "SAIDI and momentary counts on governed definitions."]]),
                biz("Customer Operations", "AI/BI", "Contact centre and field service on high-bill complaints, move-in and move-out volume, payment arrangements and collections effectiveness.",
                    [["AI/BI", "Call volume, first-call resolution and collections on certified Metric Views."], ["Genie One", "Ask which premises drove yesterday's complaint spike."], ["CustomerLake", "Segments and outreach without copying CIS profiles elsewhere."]]),
                biz("Asset Management", "Lakeflow", "Engineering and vegetation management on inspection backlogs, transformer and conductor failure risk, and which assets to replace before the fault.",
                    [["Asset Health Cockpit", "Condition scores and work order backlog by feeder class."], ["Lakeflow", "AMI, inspection and work-order feeds conformed for asset analytics."], ["MLflow", "Failure-risk models tracked for audit and reproduction."]]),
                biz("Regulatory & Rates", "AI/BI", "Regulatory affairs on cost-of-service studies, class revenue requirements and rate design that survives a commission challenge.",
                    [["Rate Case Analytics", "Cost allocation and class revenue requirements on governed ledgers."], ["AI/BI", "Regulatory KPIs the commission and board read."], ["Unity Catalog", "One definition of revenue and plant investment across finance and operations."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the AMI, SCADA, CIS and GIS feeds; own the Bronze to Silver path and the pager when a meter or outage feed breaks.",
                    [["Lakeflow Connect", "Managed connectors for AMI head-ends, CIS and asset systems."], ["Lakeflow Designer", "Declarative pipelines with expectations on meter and outage feeds."], ["Lakewatch", "Freshness on the tables the control centre reads every morning."]]),
                biz("Data Scientists", "MLflow", "Load-forecasting, non-technical-loss and asset failure-risk models, and whether they still hold a season after deployment.",
                    [["Feature Store", "Premise and feeder features defined once for training and serving."], ["MLflow", "Every forecast and failure-risk run tracked for audit and reproduction."], ["Model Serving", "Load and loss models scored in the operational path."]]),
                biz("App Developers", "Apps", "Ship the OMS control tower, asset-health and collections applications operations works in, hosted next to governed data.",
                    [["Apps", "Storm and asset screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for restoration decisions and crew writes."], ["Agent Bricks", "Agents that draft a switching plan or work order against governed tools."]]),
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
                uc("Storm Restoration", "Reliability", "gauge", "Restoring feeders and customers after weather, optimising crew routing and switching against critical premises."),
                uc("Load Forecasting", "Operations", "chart", "Short- and long-term demand forecasts that account for weather, DER and electrification load growth."),
                uc("Non-Technical Loss", "Revenue", "market", "Theft and meter bypass detection from AMI anomalies, tamper flags and billing pattern divergence."),
                uc("Voltage Management", "Power quality", "iot", "Conservation voltage reduction and capacitor switching scored against end-of-line voltage violations."),
                uc("Vegetation Management", "Asset risk", "sheet", "Trim cycles prioritised by grow-in risk and historical fault correlation, not calendar rotation alone."),
                uc("DER Orchestration", "Grid edge", "stream", "Behind-the-meter solar and batteries coordinated for peak shaving without violating feeder limits."),
                uc("Customer Propensity", "Programs", "custlake", "Efficiency program uptake and payment-plan acceptance scored per premise from CIS and AMI history."),
                uc("Rate Design Analytics", "Regulatory", "gavel", "Class revenue requirements and cost causation studies that survive regulatory challenge."),
                uc("Water Loss Management", "Distribution", "stream", "District metering and acoustic leak correlation for water utilities reducing real and apparent losses."),
                uc("Capital Planning", "Investment", "product", "Replacement prioritisation across transformers, mains and meters against reliability and financial targets."),
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
    "food_beverage": {
        "label": "Food & Beverage",
        "blurb": "CPG food and beverage manufacturers: recipe and batch production, quality and traceability, demand planning, and cold-chain logistics.",
        "medallion": medallion(
            "Raw plant and ERP",
            "MES batch records, ERP production orders, quality lab results, warehouse movements and retailer POS feeds, landed exactly as received so a lot code or a fill weight can always be replayed.",
            "Conformed SKU, batch",
            "SKUs, batches, plants and distribution nodes resolved into single conformed entities across ERP, MES and WMS, with lot genealogy reconciled from raw material to finished case.",
            "Yield, OTIF, quality",
            "Contracted products operations and sales run on: line yield and scrap, OTIF to retail customers, quality hold rates, and trade promotion ROI.",
        ),
        "rails": {
            "src": [
                {"box": "Manufacturing & MES", "ic": "erp", "tiles": [
                    tile("Rockwell FactoryTalk", "iot", "Line speeds, filler weights, CIP cycles and downtime reason codes from the plant floor.", "rockwell-ft"),
                    tile("Siemens Opcenter MES", "sheet", "Batch recipes, material consumption and electronic batch records for regulated plants.", "siemens-opcenter"),
                    tile("SAP S/4HANA PP", "erp", "Production orders, BOM explosions, confirmations and co-product yields.", "sap-s4")
                ]},
                {"box": "Quality & Safety", "ic": "gavel", "tiles": [
                    tile("Veeva QualityDocs", "gavel", "Specifications, deviations, CAPA and release documentation for food safety programs.", "veeva-quality"),
                    tile("SafetyChain Plant Mgmt", "gauge", "HACCP checks, temperature logs and sanitation records from production shifts.", "safetychain"),
                    tile("LIMS Lab Results", "db", "Microbiology, allergen and nutritional assay results tied to lot and line.")
                ]},
                {"box": "Supply & Logistics", "ic": "stream", "tiles": [
                    tile("Blue Yonder TMS", "stream", "Inbound raw material and outbound finished goods movements with carrier ETA and temperature probes.", "blue-yonder"),
                    tile("Manhattan WMS", "product", "Warehouse inventory, pick/pack and shipment confirmation against customer orders.", "manhattan-wms"),
                    tile("Sensitech TempTale", "iot", "Cold-chain logger readings from plant dock through DC to customer delivery.", "sensitech")
                ]},
                {"box": "Commercial & Retail", "ic": "market", "tiles": [
                    tile("NielsenIQ POS", "market", "Syndicated and direct retail sell-through by SKU, banner and geography.", "nielseniq"),
                    tile("Circana/IRI Panel", "chart", "Household panel and causal analytics for category and brand performance.", "circana"),
                    tile("Trade Promotion Mgmt", "partner", "Promotional calendars, scan data and accrual settlements with retail partners.")
                ]},
                fed_group(
                    "Co-manufacturer Inventory",
                    "Third-party production inventory and batch status left at co-packers and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("GS1 EPCIS Events", "api", "Serial shipping container and lot traceability events normalised on ingest for recall readiness.", "gs1-epcis"),
                tile("FDA FSMA 204 Trace", "gavel", "Key data elements for high-risk foods consumed inbound for compliance validation.", "fsma-204"),
                tile("Weather & Commodity", "globe", "Crop condition and commodity price feeds for agricultural input planning.")
            ]),
            "ppl": ppl2([
                biz("CEO & COO", "Genie One", "The CEO on volume, gross margin and category share; the COO on plant OEE, OTIF service level and recall exposure across the network.",
                    [["Genie One", "Ask what yesterday's OTIF was by customer without waiting on supply analytics."], ["AI/BI", "Volume, margin and quality on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"yield\" means one thing across plants."]]),
                biz("Plant Operations", "Lakehouse//RT", "Plant managers and line leads on changeover time, downtime reason codes and batch release, chasing line yield and scrap before the shift ends.",
                    [["Batch Genealogy Console", "Lot trace from raw material to pallet in one view."], ["Lakehouse//RT", "Live filler and CIP state at line speed."], ["AI/BI", "OEE and scrap on governed definitions."]]),
                biz("Quality & Food Safety", "AI/BI", "Quality managers on hold rate, open deviations, CAPA aging and sanitation compliance across sites when a supplier alert lands.",
                    [["Quality Hold Dashboard", "Open deviations and release status by plant and SKU."], ["AI/BI", "Hold rate and CAPA aging on certified Metric Views."], ["Unity Catalog", "One definition of lot status across MES and LIMS."]]),
                biz("Supply Chain", "Model Serving", "Planners on forecast accuracy and bias, inventory days of supply and which customer orders are at risk before the S&OP cycle locks.",
                    [["Demand Planning Workbench", "Consensus forecast scenarios before S&OP locks."], ["Model Serving", "Demand and service models scored against live orders."], ["AI/BI", "OTIF and inventory turns the sales team reads."]]),
                biz("Sales & Marketing", "CustomerLake", "Category managers on promotion lift versus cannibalised base, distribution voids and the retailer scorecards that decide the next line review.",
                    [["Trade ROI Analytics", "Promotion spend versus incremental volume by banner."], ["CustomerLake", "Retailer segments without copying syndicated data elsewhere."], ["Genie One", "Ask which SKUs lost distribution last month."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the MES, ERP, quality and retailer POS feeds; own the Bronze to Silver path and the pager when a plant or trace feed breaks.",
                    [["Lakeflow Connect", "Managed connectors for S/4HANA, MES and WMS sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on batch and POS feeds."], ["Lakewatch", "Freshness on the tables plant and supply teams read every morning."]]),
                biz("Data Scientists", "MLflow", "Demand, shelf-life and line-yield models, and whether they still hold six months after deployment.",
                    [["Feature Store", "SKU and plant features defined once for training and serving."], ["MLflow", "Every demand and yield run tracked for audit and reproduction."], ["Model Serving", "Forecast and quality models scored against live orders."]]),
                biz("App Developers", "Apps", "Ship the genealogy, demand-planning and quality-hold applications operations works in, hosted next to governed data.",
                    [["Apps", "Plant and quality screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for batch-release and hold writes."], ["Agent Bricks", "Agents that draft a recall trace or hold decision against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and quality alerts in the channel plants already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Plant Writeback", "ic": "opdb", "tiles": [
                    tile("MES Batch Release", "erp", "Quality release decisions written back into MES so pallets ship from governed lot status.", "siemens-opcenter"),
                    tile("SAP Order Reschedule", "db", "Production order dates adjusted from forecast consensus before materials are staged.", "sap-s4"),
                    tile("Floor Mobile Apps", "apps", "Sanitation tasks, line checks and downtime codes pushed to tablets on the line.")
                ]},
                {"box": "Retail & Co-pack", "ic": "partner", "tiles": [
                    tile("Retailer VMI Portal", "share", "Inventory and forecast positions shared with key retailers over Delta Sharing instead of weekly spreadsheets."),
                    tile("Co-manufacturer Portal", "partner", "Production schedules and lot genealogy exchanged with co-pack partners under contract."),
                    tile("3PL Cold Chain", "stream", "Temperature excursions and delivery proof shared back to carriers and customers.", "sensitech")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("FSMA Traceability", "gavel", "Traceability lot records and recall simulations produced from governed genealogy tables.", "fsma-204"),
                    tile("Nutrition Label Compliance", "share", "Label claims and allergen controls filed from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Retailers, co-packers and auditors reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Batch Genealogy Console", "Lot traceability", "stream", "Forward and backward trace from ingredient lot to retail case in seconds during a quality hold or recall."),
                app("Demand Planning Workbench", "S&OP consensus", "sheet", "Statistical and commercial forecast scenarios reconciled before production and procurement lock."),
                app("Quality Hold Dashboard", "Release control", "gauge", "Open deviations, lab results and sanitation checks blocking shipment by plant and SKU."),
                app("Trade ROI Analytics", "Promotion lift", "market", "Scan data and accruals reconciled to incremental volume and margin by retailer event."),
            ],
            [
                uc("Recall Readiness", "Traceability", "gauge", "Lot genealogy and distribution lists produced in minutes, not days, when a supplier alert arrives."),
                uc("Demand Forecasting", "Planning", "sheet", "SKU-location forecasts that blend syndicated POS, promotions and plant capacity constraints."),
                uc("Line Yield Optimisation", "Manufacturing", "iot", "Scrap and giveaway reduced by correlating filler drift, changeover time and operator crew."),
                uc("Cold Chain Integrity", "Logistics", "stream", "Temperature excursions predicted and rerouted before product quality is compromised."),
                uc("Trade Promotion ROI", "Commercial", "market", "Which promotions paid for themselves in incremental volume versus cannibalised base."),
                uc("Allergen Control", "Food safety", "gavel", "Cross-contact risk flagged from scheduling, cleaning records and shared equipment genealogy."),
                uc("Shelf-Life Optimisation", "Quality", "product", "FEFO allocation scored against remaining shelf life and customer distance."),
                uc("Co-pack Visibility", "Network", "partner", "Third-party production status and inventory reconciled without manual spreadsheet chases."),
                uc("OEE & Downtime", "Operations", "chart", "Top loss categories by line and shift with root cause tied to MES reason codes."),
                uc("Sustainable Sourcing", "ESG", "globe", "Ingredient provenance and carbon intensity traced from farm through finished goods."),
            ],
        ),
        "sources": {
            "rockwell-ft": {"t": "Rockwell FactoryTalk", "u": "https://www.rockwellautomation.com/en-us/products/software/factorytalk.html"},
            "siemens-opcenter": {"t": "Siemens Opcenter MES", "u": "https://plm.sw.siemens.com/en-US/opcenter/execution/"},
            "sap-s4": {"t": "SAP S/4HANA", "u": "https://www.sap.com/products/erp/s4hana.html"},
            "veeva-quality": {"t": "Veeva QualityDocs", "u": "https://www.veeva.com/products/qualitydocs/"},
            "safetychain": {"t": "SafetyChain plant management", "u": "https://safetychain.com/"},
            "blue-yonder": {"t": "Blue Yonder transportation management", "u": "https://blueyonder.com/solutions/transportation-management"},
            "manhattan-wms": {"t": "Manhattan Active Warehouse Management", "u": "https://www.manh.com/solutions/warehouse-management"},
            "sensitech": {"t": "Sensitech TempTale", "u": "https://www.sensitech.com/en/solutions/"},
            "nielseniq": {"t": "NielsenIQ retail measurement", "u": "https://nielseniq.com/global/en/solutions/"},
            "circana": {"t": "Circana market measurement", "u": "https://www.circana.com/"},
            "gs1-epcis": {"t": "GS1 EPCIS standard", "u": "https://www.gs1.org/standards/epcis"},
            "fsma-204": {"t": "FDA FSMA Rule 204", "u": "https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-requirements-additional-traceability-records-certain-foods"}
        },
    },
    "gaming": {
        "label": "Gaming",
        "blurb": "Interactive entertainment and iGaming: player lifecycle, in-game economy, live ops, fraud and responsible gaming compliance.",
        "medallion": medallion(
            "Raw event streams",
            "Client telemetry, payment authorisations, KYC decisions, game server events and marketing sends, landed exactly as received so a session or a wager can always be replayed.",
            "Conformed player, session",
            "Players, devices, sessions and titles resolved into single conformed entities across platform, payments and CRM, with cross-device identity stitched to one profile.",
            "ARPDAU, LTV, churn",
            "Contracted products product and finance run on: ARPDAU and payer conversion, cohort LTV, churn and reactivation, and fraud loss rate.",
        ),
        "rails": {
            "src": [
                {"box": "Game Platform & Live", "ic": "stream", "tiles": [
                    tile("Unity Gaming Services", "api", "Player authentication, economy transactions and live ops configuration events.", "unity-gaming"),
                    tile("PlayFab Backend", "db", "Title data, inventory, matchmaking and leaderboard state for cross-platform games.", "playfab"),
                    tile("Custom Game Servers", "iot", "Authoritative match and session logs from dedicated and listen servers at tick resolution.")
                ]},
                {"box": "Payments & Wallet", "ic": "market", "tiles": [
                    tile("Adyen Payments", "market", "Card, wallet and local payment method authorisations, chargebacks and settlements.", "adyen"),
                    tile("Paysafe Skrill", "partner", "Digital wallet deposits and withdrawals for regulated iGaming markets.", "paysafe"),
                    tile("Pragmatic Play RGS", "product", "Remote game server rounds, bet outcomes and jackpot contributions for casino content.", "pragmatic")
                ]},
                {"box": "Player CRM & Support", "ic": "custlake", "tiles": [
                    tile("Salesforce Gaming CRM", "custlake", "Player segments, campaign responses and VIP host notes.", "sf-gaming"),
                    tile("Zendesk Player Support", "chat", "Tickets, chat transcripts and refund disputes tied to player accounts.", "zendesk"),
                    tile("Braze Lifecycle", "partner", "Push, email and in-app message sends with delivery and conversion events.", "braze")
                ]},
                {"box": "Fraud & Compliance", "ic": "gavel", "tiles": [
                    tile("SEON Fraud Prevention", "gauge", "Device fingerprinting, velocity rules and chargeback signals at registration and deposit.", "seon"),
                    tile("Onfido Identity", "people", "Document verification and biometric checks for KYC and age gating.", "onfido"),
                    tile("GeoComply Location", "globe", "Geolocation compliance pings proving the player is in an permitted jurisdiction.", "geocomply")
                ]},
                fed_group(
                    "Publisher Revenue Share",
                    "Third-party title royalty ledgers left at partners and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("AppsFlyer Attribution", "api", "Install and in-app event attribution consumed inbound for UA spend optimisation.", "appsflyer"),
                tile("Steam & Console APIs", "partner", "Platform achievement, entitlement and sales reports normalised on ingest."),
                tile("Regulator GGR Feeds", "gavel", "Jurisdictional gross gaming revenue file layouts validated before submission windows.")
            ]),
            "ppl": ppl2([
                biz("CEO & CFO", "Genie One", "The CEO on MAU, payer conversion and studio ROI; the CFO on gross gaming revenue, hold percentage and chargeback loss rate.",
                    [["Genie One", "Ask what yesterday's ARPDAU was by title without waiting on analytics."], ["AI/BI", "Revenue, retention and fraud on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"active player\" means one thing across titles."]]),
                biz("Live Ops & Product", "Model Serving", "Live-ops managers on event-calendar performance, economy sink-and-source balance and how each content release moves retention and spend.",
                    [["Live Ops Console", "Event performance and economy sinks before the next patch ships."], ["Model Serving", "Churn and LTV models scored per cohort."], ["AI/BI", "Funnel and engagement on governed definitions."]]),
                biz("Player Experience", "CustomerLake", "Community and VIP host teams on player sentiment, complaint drivers and the high-value accounts worth saving before they churn.",
                    [["Player 360", "Support history, spend and play patterns in one view."], ["CustomerLake", "Segments and activations without copying profiles into a separate CDP."], ["Genie One", "Ask which VIP accounts opened tickets after the last update."]]),
                biz("Risk & Compliance", "AI/BI", "Fraud analysts and compliance officers on AML and SAR alerts, self-exclusion enforcement and jurisdictional filings before payouts release.",
                    [["Fraud Command Centre", "Velocity and device clusters flagged before payouts release."], ["AI/BI", "Chargeback and SAR metrics on certified Metric Views."], ["Unity Catalog", "One definition of GGR across platform and RGS."]]),
                biz("Marketing & UA", "AI/BI", "User acquisition on CPI, ROAS and creative performance by channel and geography, reallocating spend before daily budgets exhaust.",
                    [["UA Optimiser", "Spend reallocation scenarios before daily budgets exhaust."], ["AI/BI", "ROAS and cohort payback the growth team reads."], ["Model Serving", "LTV models informing bid caps."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the game platform, payments and CRM event streams; own the Bronze to Silver path and the pager when telemetry breaks.",
                    [["Lakeflow Connect", "Managed connectors for platform, payment and CRM sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on telemetry and payment feeds."], ["Lakewatch", "Freshness on the tables live ops and risk teams read every morning."]]),
                biz("Data Scientists", "MLflow", "Churn, LTV, fraud and matchmaking models, and whether they still hold a season after each content patch.",
                    [["Feature Store", "Player features defined once and read identically in training and serving."], ["MLflow", "Every churn and fraud run tracked for audit and reproduction."], ["Model Serving", "LTV and fraud models scored in the live player path."]]),
                biz("App Developers", "Apps", "Ship the live ops, player 360 and fraud command applications the studio works in, hosted next to governed data.",
                    [["Apps", "Live ops and risk screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for economy config and case writes."], ["Agent Bricks", "Agents that draft a live ops tweak or fraud case against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and live ops alerts in the channel teams already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Platform Writeback", "ic": "opdb", "tiles": [
                    tile("Economy Config Push", "api", "Live ops price and drop-rate changes written back into title configuration after simulation.", "playfab"),
                    tile("Fraud Block Lists", "gauge", "Device and payment instrument blocks pushed to the authorisation path in near real time.", "seon"),
                    tile("CRM Campaign Triggers", "custlake", "Win-back and VIP offers triggered from governed segments without nightly exports.", "braze")
                ]},
                {"box": "Studio & Platform", "ic": "partner", "tiles": [
                    tile("Publisher Analytics Share", "share", "Title performance and royalty positions shared with external studios over Delta Sharing."),
                    tile("RGS Content Partners", "product", "Round-level GGR and jackpot feeds exchanged with remote game server providers.", "pragmatic"),
                    tile("Affiliate Networks", "partner", "Acquisition partner reporting reconciled against attributed deposits and NGR.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("GGR Regulatory Filings", "gavel", "Jurisdictional gross gaming revenue and responsible gaming reports produced from governed tables."),
                    tile("AML & SAR Reporting", "share", "Suspicious activity metrics filed from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Studios, affiliates and regulators reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Live Ops Console", "Event management", "gauge", "Economy balance, event calendars and cohort impact before and after each content release."),
                app("Player 360", "Support & VIP", "custlake", "Play, spend, support and risk history on one screen for hosts and community managers."),
                app("Fraud Command Centre", "Risk operations", "stream", "Velocity clusters, bonus abuse and chargeback patterns flagged before withdrawals approve."),
                app("UA Optimiser", "Acquisition spend", "market", "Channel and creative performance scored against predicted LTV before daily budgets lock."),
            ],
            [
                uc("Player Churn Prediction", "Retention", "gauge", "Identifying players likely to lapse from session decay and economy frustration before they uninstall."),
                uc("LTV & Monetisation", "Revenue", "market", "Cohort lifetime value and payer conversion scored per acquisition channel and title."),
                uc("Live Ops Balancing", "Economy", "sheet", "Sink and source tuning tested against simulated economy health before patches ship."),
                uc("Fraud & Bonus Abuse", "Risk", "stream", "Multi-accounting, collusion and promo abuse detected from device, payment and play graphs."),
                uc("Responsible Gaming", "Compliance", "gavel", "Self-exclusion, deposit limits and harm markers enforced from governed player state."),
                uc("Matchmaking Quality", "Engagement", "people", "Queue times and match fairness optimised without opening exploit vectors."),
                uc("Content Personalisation", "Live ops", "custlake", "Offers and events targeted per player segment from in-game behaviour, not batch exports."),
                uc("Chargeback Prevention", "Payments", "market", "High-risk instruments and behaviours blocked before authorisation settles."),
                uc("Regulatory GGR", "Reporting", "gavel", "Jurisdiction-accurate gross gaming revenue reconciled across platform and RGS content."),
                uc("Studio Royalty", "Partners", "product", "Third-party title revenue share calculated from governed round and jackpot data."),
            ],
        ),
        "sources": {
            "unity-gaming": {"t": "Unity Gaming Services", "u": "https://unity.com/solutions/gaming-services"},
            "playfab": {"t": "Microsoft PlayFab", "u": "https://playfab.com/"},
            "adyen": {"t": "Adyen payments platform", "u": "https://www.adyen.com/"},
            "paysafe": {"t": "Paysafe digital wallets", "u": "https://www.paysafe.com/"},
            "pragmatic": {"t": "Pragmatic Play", "u": "https://www.pragmaticplay.com/"},
            "sf-gaming": {"t": "Salesforce for gaming", "u": "https://www.salesforce.com/solutions/industries/"},
            "zendesk": {"t": "Zendesk customer service", "u": "https://www.zendesk.com/"},
            "braze": {"t": "Braze customer engagement", "u": "https://www.braze.com/"},
            "seon": {"t": "SEON fraud prevention", "u": "https://seon.io/"},
            "onfido": {"t": "Onfido identity verification", "u": "https://onfido.com/"},
            "geocomply": {"t": "GeoComply geolocation compliance", "u": "https://www.geocomply.com/"},
            "appsflyer": {"t": "AppsFlyer mobile attribution", "u": "https://www.appsflyer.com/"}
        },
    },
    "genomics_biotech": {
        "label": "Genomics & Biotech",
        "blurb": "Genomics and biotechnology: sequencing pipelines, variant interpretation, lab operations, clinical trial biomarkers and regulated research data.",
        "medallion": medallion(
            "Raw sequence and LIMS",
            "FASTQ and BAM files, LIMS sample metadata, instrument QC metrics and electronic lab notebook entries, landed exactly as received so a variant call or a sample chain can always be replayed.",
            "Conformed sample, variant",
            "Samples, subjects, assays and variant calls resolved into single conformed entities across LIMS, sequencers and analysis pipelines, with sample lineage reconciled from collection through report.",
            "Actionable clinical biomarkers",
            "Contracted products clinical and research teams run on: variant classification tiers, trial enrolment biomarker rates, lab turnaround time, and pipeline QC pass rates.",
        ),
        "rails": {
            "src": [
                {"box": "Sequencing & Omics", "ic": "stream", "tiles": [
                    tile("Illumina BaseSpace", "db", "Run metadata, cluster density and demultiplexed FASTQ from NovaSeq and NextSeq instruments.", "illumina-basespace"),
                    tile("Oxford Nanopore EPI2ME", "iot", "Long-read basecalls, methylation and structural variant calls from MinION and PromethION.", "nanopore-epi2me"),
                    tile("10x Genomics Cloud", "api", "Single-cell and spatial gene expression matrices from Chromium and Visium workflows.", "10x-cloud")
                ]},
                {"box": "Lab & Sample Mgmt", "ic": "erp", "tiles": [
                    tile("Benchling R&D Cloud", "notebook", "Sample registration, chain of custody and structured experiment records.", "benchling"),
                    tile("LabVantage LIMS", "db", "Clinical and research sample accessioning, aliquots and result release.", "labvantage"),
                    tile("LIMS", "sheet", "Specimen tracking, storage location and stability across biobank freezers.", "samplemanager")
                ]},
                {"box": "Clinical & Trials", "ic": "people", "tiles": [
                    tile("Medidata Rave EDC", "gavel", "Electronic case report forms, visit schedules and protocol deviations.", "medidata-rave"),
                    tile("Veeva Vault CTMS", "partner", "Site activation, enrolment milestones and monitoring visit findings.", "veeva-ctms"),
                    tile("Flatiron Oncology EHR", "custlake", "De-identified oncology clinical records for real-world evidence cohorts.", "flatiron")
                ]},
                {"box": "Knowledge & Reference", "ic": "globe", "tiles": [
                    tile("ClinVar & gnomAD", "share", "Public variant pathogenicity and population frequency references for annotation.", "clinvar"),
                    tile("COSMIC Cancer DB", "db", "Somatic mutation catalogue for oncology biomarker interpretation.", "cosmic"),
                    tile("Instrument QC Telemetry", "observ", "Sequencer health, reagent lot and calibration drift joined to run outcomes.")
                ]},
                fed_group(
                    "CRO Analysis Results",
                    "Contract research organisation variant reports left at partners and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("GA4GH WES/WGS APIs", "api", "Beacon and phenopacket exchange endpoints consumed inbound for federated discovery.", "ga4gh"),
                tile("HL7 FHIR Genomics", "stream", "Diagnostic report and observation resources normalised on ingest for clinical integration.", "fhir-genomics"),
                tile("dbGaP Authorised Access", "gavel", "Controlled-access cohort files retrieved under DAC-approved scopes.")
            ]),
            "ppl": ppl2([
                biz("CSO & CFO", "Genie One", "The CSO on sequencing throughput and biomarker programme progress; the CFO on CRO spend, cost-per-sample and trial enrolment velocity.",
                    [["Genie One", "Ask how many samples cleared QC this week without waiting on bioinformatics."], ["AI/BI", "Throughput, QC and trial metrics on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"pathogenic\" means one thing across labs."]]),
                biz("Bioinformatics", "Model Serving", "Pipeline engineers and analysts on variant calling, annotation and the VUS queue, deciding what is safe to release to clinicians at sign-out.",
                    [["Variant Review Workbench", "VUS queues prioritised by evidence tier before sign-out."], ["Model Serving", "Classifier models scored in the interpretation path."], ["MLflow", "Pipeline runs tracked for CLIA and CAP audit."]]),
                biz("Clinical Operations", "AI/BI", "Trial managers on site enrolment against target, sample-collection SLAs and protocol deviations before a site is at risk of closing.",
                    [["Trial Enrolment Tracker", "Biomarker-positive screen failures surfaced before sites close."], ["AI/BI", "Enrolment and deviation metrics on certified Metric Views."], ["Unity Catalog", "One definition of subject status across EDC and LIMS."]]),
                biz("Lab Operations", "Lakeflow", "Lab directors on assay turnaround time, reagent-lot inventory and instrument utilisation before a client escalates a late result.",
                    [["Lab Ops Dashboard", "Queue depth and TAT by assay before clients escalate."], ["Lakeflow", "LIMS and instrument feeds conformed for operations analytics."], ["Lakewatch", "Freshness on the tables sign-out depends on."]]),
                biz("Regulatory & Quality", "AI/BI", "Quality and regulatory affairs on CAP and CLIA audits, QC failure rates and the validation documentation a submission stands or falls on.",
                    [["Quality Metrics", "QC failure rates and CAPA aging on governed definitions."], ["AI/BI", "Audit-ready dashboards regulators can trace."], ["Unity Catalog", "Lineage from raw FASTQ to signed report."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the sequencer, LIMS and trial EDC feeds; own the Bronze to Silver path and the pager when a run or sample feed breaks.",
                    [["Lakeflow Connect", "Managed connectors for BaseSpace, LIMS and EDC sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on FASTQ and sample feeds."], ["Lakewatch", "Freshness on the tables sign-out and trial teams read every morning."]]),
                biz("Data Scientists", "MLflow", "Variant-classification, biomarker-discovery and turnaround-time models, and whether they still hold under CAP and CLIA validation.",
                    [["Feature Store", "Sample and variant features defined once for training and serving."], ["MLflow", "Every pipeline run tracked for CLIA and CAP audit."], ["Model Serving", "Classifier models scored in the interpretation path."]]),
                biz("App Developers", "Apps", "Ship the variant review, enrolment-tracking and lab-ops applications the labs work in, hosted next to governed data.",
                    [["Apps", "Review and lab screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for sign-out and sample writes."], ["Agent Bricks", "Agents that draft a variant summary or enrolment check against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and lab alerts in the channel teams already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Clinical Writeback", "ic": "opdb", "tiles": [
                    tile("Signed Report Release", "gavel", "Interpreted variants and diagnostic narratives written back into LIMS for clinician delivery.", "labvantage"),
                    tile("EDC Biomarker Flags", "db", "Enrolment eligibility results pushed to the trial EDC at screening.", "medidata-rave"),
                    tile("Lab Queue Mobile", "apps", "Sample prep tasks and exception handling pushed to bench technologists.")
                ]},
                {"box": "Research Partners", "ic": "partner", "tiles": [
                    tile("CRO Data Exchange", "share", "Variant and QC tables shared with contract labs over Delta Sharing under study agreements."),
                    tile("Academic Collaborations", "globe", "Federated cohort queries via GA4GH beacons without exporting patient-level files.", "ga4gh"),
                    tile("Pharma Alliance Feeds", "product", "Biomarker prevalence and response summaries exchanged under collaboration MSAs.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("CLIA/CAP Compliance", "gavel", "QC, proficiency and corrective action records produced from governed lab tables."),
                    tile("FDA Submission Packages", "share", "Validation summaries and analysis reproducibility filed from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "CROs, pharma partners and consortia reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Variant Review Workbench", "Clinical sign-out", "gauge", "VUS and pathogenic calls ranked by evidence tier with literature and population frequency at the curator's fingertips."),
                app("Trial Enrolment Tracker", "Biomarker screening", "people", "Sites, screen failures and biomarker-positive enrolment against protocol targets in real time."),
                app("Lab Ops Dashboard", "Throughput & TAT", "stream", "Instrument queues, reagent lots and turnaround time by assay before clients escalate."),
                app("Pipeline QC Console", "Bioinformatics", "iot", "Run-level QC metrics and pipeline failures surfaced before downstream annotation consumes bad calls."),
            ],
            [
                uc("Variant Interpretation", "Diagnostics", "gauge", "Somatic and germline variants classified with reproducible evidence chains clinicians can defend."),
                uc("Biomarker Discovery", "Research", "sheet", "Multi-omic signals ranked for trial enrichment and companion diagnostic development."),
                uc("Trial Enrolment", "Clinical ops", "people", "Screening workflows that match patients to protocols from genomic and clinical criteria."),
                uc("Lab Turnaround Optimisation", "Operations", "stream", "Queue bottlenecks identified from accession through sign-out, not average TAT alone."),
                uc("Real-World Evidence", "Outcomes", "custlake", "Treatment response cohorts built from linked genomic and oncology EHR records under governance."),
                uc("Single-Cell Analytics", "Discovery", "notebook", "Cell-type resolution across tumour microenvironment for target identification."),
                uc("Pipeline Reproducibility", "Quality", "gavel", "Every analysis from FASTQ to report traced for CAP, CLIA and FDA inspection."),
                uc("Reference Data Harmonisation", "Annotation", "globe", "ClinVar, gnomAD and COSMIC updates propagated without breaking historical calls."),
                uc("Sample Chain of Custody", "Compliance", "product", "Aliquot location and handling events reconciled from collection through destruction."),
                uc("Pharmacogenomics", "Therapeutics", "market", "Drug-gene interactions surfaced at ordering for precision prescribing programmes."),
            ],
        ),
        "sources": {
            "illumina-basespace": {"t": "Illumina BaseSpace Sequence Hub", "u": "https://www.illumina.com/products/by-type/informatics-products/basespace-sequence-hub.html"},
            "nanopore-epi2me": {"t": "Oxford Nanopore EPI2ME", "u": "https://epi2me.nanoporetech.com/"},
            "10x-cloud": {"t": "10x Genomics Cloud Analysis", "u": "https://www.10xgenomics.com/products/cloud-analysis"},
            "benchling": {"t": "Benchling R&D Cloud", "u": "https://www.benchling.com/"},
            "labvantage": {"t": "LabVantage LIMS", "u": "https://www.labvantage.com/"},
            "samplemanager": {"t": "Thermo Fisher SampleManager LIMS", "u": "https://www.thermofisher.com/samplemanager"},
            "medidata-rave": {"t": "Medidata Rave EDC", "u": "https://www.medidata.com/en/clinical-trial-products/clinical-data-management/edc-systems/"},
            "veeva-ctms": {"t": "Veeva Vault CTMS", "u": "https://www.veeva.com/products/vault-ctms/"},
            "flatiron": {"t": "Flatiron Health oncology data", "u": "https://flatiron.com/"},
            "clinvar": {"t": "NCBI ClinVar", "u": "https://www.ncbi.nlm.nih.gov/clinvar/"},
            "cosmic": {"t": "COSMIC cancer database", "u": "https://cancer.sanger.ac.uk/cosmic"},
            "ga4gh": {"t": "Global Alliance for Genomics and Health", "u": "https://www.ga4gh.org/"},
            "fhir-genomics": {"t": "HL7 FHIR genomics implementation guide", "u": "https://hl7.org/fhir/uv/genomics-reporting/"}
        },
    },
    "grocery": {
        "label": "Grocery",
        "blurb": "Grocery retail and wholesale: store operations, replenishment, fresh perimeter, loyalty and supplier collaboration.",
        "medallion": medallion(
            "Raw POS and supply",
            "POS transactions, inventory snapshots, DC shipments, planogram compliance scans and loyalty swipes, landed exactly as received so a basket or a shrink event can always be replayed.",
            "Conformed SKU, store",
            "SKUs, stores, vendors and customers resolved into single conformed entities across POS, merchandising and supply systems, with promotion flags reconciled to the item sold.",
            "Shrink, fill rate, basket",
            "Contracted products merchandising and operations run on: shrink and waste by department, on-shelf availability, basket size and loyalty penetration.",
        ),
        "rails": {
            "src": [
                {"box": "Store & POS", "ic": "market", "tiles": [
                    tile("NCR Voyix POS", "market", "Lane transactions, tenders, voids and item-level scans from store registers.", "ncr-voyix"),
                    tile("Toshiba ACE POS", "erp", "Front-end and self-checkout events with department and weight-scale integration.", "toshiba-ace"),
                    tile("Trax Shelf Analytics", "iot", "On-shelf availability and planogram compliance from in-aisle image recognition.", "trax")
                ]},
                {"box": "Merchandising & Promo", "ic": "sheet", "tiles": [
                    tile("Relex Space Planning", "sheet", "Planograms, facings and space-to-sales assignments by store cluster.", "relex"),
                    tile("SymphonyAI IRIS", "chart", "Promotion planning, lift forecasts and vendor funding accruals.", "symphony-iris"),
                    tile("Dunnhumby Customer Data", "custlake", "Loyalty baskets, segments and propensity scores from the science partner.", "dunnhumby")
                ]},
                {"box": "Supply & Fresh", "ic": "stream", "tiles": [
                    tile("Blue Yonder Replenishment", "stream", "Store and DC orders, forecasts and service-level exceptions.", "blue-yonder-repl"),
                    tile("Sensitech Fresh Chain", "iot", "Temperature monitoring for dairy, meat and produce from DC to store backroom.", "sensitech"),
                    tile("Invafresh Fresh Platform", "product", "Markdown, production planning and waste tracking for bakery, deli and produce.", "invafresh")
                ]},
                {"box": "E-com & Fulfillment", "ic": "partner", "tiles": [
                    tile("Instacart Marketplace", "partner", "Third-party pick, substitution and delivery events attributed to store inventory.", "instacart"),
                    tile("Ocado Smart Platform", "api", "CFC pick accuracy, route density and on-time delivery for automated fulfillment.", "ocado"),
                    tile("Web & App Clickstream", "observ", "Digital basket builds, search and coupon clips joined to in-store loyalty ID.")
                ]},
                fed_group(
                    "Franchisee POS",
                    "Licensed store sales and inventory left at franchise operators and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("GS1 GDSN Product Data", "api", "Synchronised item attributes and packaging hierarchies consumed inbound for master data.", "gs1-gdsn"),
                tile("NielsenIQ Store Read", "market", "Syndicated store-level performance for competitive benchmarking.", "nielseniq"),
                tile("Weather & Local Events", "globe", "Forecast and event calendars for demand shaping on perishable categories.")
            ]),
            "ppl": ppl2([
                biz("CEO & COO", "Genie One", "The CEO on comparable-store sales and market share; the COO on shrink, labor productivity and on-shelf availability through the peak trading weeks.",
                    [["Genie One", "Ask what comp sales were yesterday by banner without waiting on retail analytics."], ["AI/BI", "Sales, shrink and availability on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"comp\" means one thing across banners."]]),
                biz("Merchandising", "Model Serving", "Category managers on assortment localisation, price and the promotion lift that decides which vendor deals fund the next circular.",
                    [["Promo Planning Workbench", "Lift scenarios before vendor deals lock."], ["Model Serving", "Demand models scored per SKU-store."], ["AI/BI", "Category performance on governed definitions."]]),
                biz("Store Operations", "Lakehouse//RT", "District managers on labor schedules, on-shelf gaps and fresh-department waste, timing markdowns before the perishable code date closes.",
                    [["Fresh Markdown Console", "Perishable markdown timing by sell-through curve."], ["Lakehouse//RT", "Live out-of-stock signals at store-hour granularity."], ["AI/BI", "Shrink and labor productivity the field reads."]]),
                biz("Supply Chain", "AI/BI", "Replenishment planners on forecast bias, store and DC fill rate and days of supply against warehouse capacity constraints.",
                    [["Replenishment Optimiser", "Order proposals tested against service targets."], ["AI/BI", "Fill rate and days of supply on certified Metric Views."], ["Unity Catalog", "One definition of inventory across POS and WMS."]]),
                biz("Loyalty & Marketing", "CustomerLake", "Personalised offers, fuel rewards and digital-coupon redemption scored per household to lift basket size and loyalty penetration.",
                    [["Loyalty Offer Engine", "Offers scored per household from basket history."], ["CustomerLake", "Segments without copying Dunnhumby exports elsewhere."], ["Genie One", "Ask which segments responded to last week's digital coupon."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the POS, merchandising and replenishment feeds; own the Bronze to Silver path and the pager when a store feed breaks.",
                    [["Lakeflow Connect", "Managed connectors for POS, merchandising and supply sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on POS and inventory feeds."], ["Lakewatch", "Freshness on the tables merchandising and the field read every morning."]]),
                biz("Data Scientists", "MLflow", "Demand, fresh-waste and loyalty-offer models, and whether they still hold a season after deployment.",
                    [["Feature Store", "SKU-store features defined once for training and serving."], ["MLflow", "Every demand and offer run tracked for audit and reproduction."], ["Model Serving", "Forecast and personalisation models scored per SKU-store."]]),
                biz("App Developers", "Apps", "Ship the replenishment, fresh-markdown and loyalty applications stores work in, hosted next to governed data.",
                    [["Apps", "Store and markdown screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for order and markdown writes."], ["Agent Bricks", "Agents that draft an order proposal or markdown against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and store alerts in the channel operations already works in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Store Writeback", "ic": "opdb", "tiles": [
                    tile("Replenishment Orders", "stream", "System-generated store orders written back into replenishment after planner review.", "blue-yonder-repl"),
                    tile("Fresh Markdown Prices", "market", "Dynamic markdowns pushed to POS labels for approaching sell-by inventory.", "invafresh"),
                    tile("Associate Task Mobile", "apps", "Gap scans, facing tasks and temperature checks pushed to handheld devices.")
                ]},
                {"box": "Supplier & Partners", "ic": "partner", "tiles": [
                    tile("Vendor VMI Portal", "share", "Inventory and forecast positions shared with key CPG suppliers over Delta Sharing."),
                    tile("Marketplace Pick Partners", "partner", "Substitution and fill-rate metrics exchanged with delivery marketplaces.", "instacart"),
                    tile("Franchise Reporting", "globe", "Licensed store KPIs aggregated without nightly flat-file collection.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Weights & Measures", "gavel", "Scale calibration and packaged goods compliance records from governed store audits."),
                    tile("Vendor Funding Audit", "share", "Promotion accruals and scan-based trade reconciliations filed from Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "CPG vendors, franchisees and analysts reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Replenishment Optimiser", "Store orders", "stream", "SKU-store order proposals scored against service level, capacity and spoilage risk before the cut-off."),
                app("Fresh Markdown Console", "Perishable waste", "gauge", "Markdown timing and depth optimised from sell-through curves and hours-to-code by department."),
                app("Promo Planning Workbench", "Vendor deals", "market", "Lift forecasts and funding accruals reconciled before circular and digital ads lock."),
                app("Loyalty Offer Engine", "Personalisation", "custlake", "Household offers scored from basket history and channel preference on governed segments."),
            ],
            [
                uc("Demand Forecasting", "Replenishment", "sheet", "SKU-store forecasts that blend loyalty baskets, weather and local events for perishables and center store."),
                uc("Fresh Waste Reduction", "Shrink", "gauge", "Markdown and production planning that cuts spoilage without sacrificing on-shelf availability."),
                uc("On-Shelf Availability", "Operations", "iot", "Gaps detected from POS voids, inventory and shelf vision before customers leave empty-handed."),
                uc("Promotion Optimisation", "Merchandising", "market", "Which deals drove incremental units versus subsidised baseline sales."),
                uc("Assortment Localisation", "Space", "sheet", "Cluster-specific assortments scored on velocity, margin and local demographic fit."),
                uc("Labor Scheduling", "Store ops", "people", "Shift plans aligned to forecast traffic and fresh production workloads."),
                uc("E-commerce Substitution", "Digital", "partner", "Pick accuracy and substitution rules tuned from historical customer acceptance."),
                uc("Loyalty Personalisation", "CRM", "custlake", "Offers and fuel rewards targeted per household without batch list exports."),
                uc("Vendor Collaboration", "CPG", "share", "Joint business planning on shared forecast and inventory positions."),
                uc("Shrink Attribution", "Loss prevention", "chart", "Theft, spoilage and scanning errors separated by department and store pattern."),
            ],
        ),
        "sources": {
            "ncr-voyix": {"t": "NCR Voyix retail platform", "u": "https://www.ncr.com/retail"},
            "toshiba-ace": {"t": "Toshiba Global Commerce ACE", "u": "https://www.toshibacommerce.com/"},
            "trax": {"t": "Trax retail shelf analytics", "u": "https://www.traxretail.com/"},
            "relex": {"t": "Relex space planning", "u": "https://www.relexsolutions.com/solutions/"},
            "symphony-iris": {"t": "SymphonyAI IRIS promotion planning", "u": "https://www.symphonyai.com/retail/"},
            "dunnhumby": {"t": "Dunnhumby customer data science", "u": "https://www.dunnhumby.com/"},
            "blue-yonder-repl": {"t": "Blue Yonder demand planning", "u": "https://blueyonder.com/solutions"},
            "invafresh": {"t": "Invafresh fresh food retail", "u": "https://invafresh.com/"},
            "sensitech": {"t": "Sensitech cold-chain monitoring", "u": "https://www.sensitech.com/en/solutions/"},
            "nielseniq": {"t": "NielsenIQ retail measurement", "u": "https://nielseniq.com/global/en/solutions/"},
            "instacart": {"t": "Instacart marketplace", "u": "https://www.instacart.com/company/business"},
            "ocado": {"t": "Ocado Smart Platform", "u": "https://ocadointelligentautomation.com/"},
            "gs1-gdsn": {"t": "GS1 Global Data Synchronisation Network", "u": "https://www.gs1.org/services/gdsn"}
        },
    },
    "health_insurance": {
        "label": "Health Insurance",
        "blurb": "Health payers: member enrollment, claims adjudication, provider network, care management and regulatory reporting.",
        "medallion": medallion(
            "Raw claims and enrollment",
            "EDI 837/835 transactions, enrollment files, provider directories, prior auth decisions and pharmacy claims, landed exactly as received so a paid claim or a member month can always be replayed.",
            "Conformed member, claim",
            "Members, providers, claims and authorizations resolved into single conformed entities across core admin and clinical systems, with ICD and CPT codes reconciled to one service line.",
            "MLR, risk, quality",
            "Contracted products actuarial and quality teams run on: medical loss ratio, risk-adjusted revenue, HEDIS measure rates, and fraud waste and abuse savings.",
        ),
        "rails": {
            "src": [
                {"box": "Core Admin & Claims", "ic": "erp", "tiles": [
                    tile("Facets Core Admin", "erp", "Membership, benefits, premium billing and claims adjudication for commercial and government lines.", "facets"),
                    tile("HealthEdge Source", "db", "Enrollment, pricing and payment integrity for Medicare Advantage and Exchange plans.", "healthedge"),
                    tile("Cotiviti Payment Integrity", "market", "Pre- and post-pay edits, DRG validation and recovery findings on paid claims.", "cotiviti")
                ]},
                {"box": "Clinical & UM", "ic": "people", "tiles": [
                    tile("Epic Payer Platform", "custlake", "Prior authorization, care management notes and member clinical summaries from provider connectivity.", "epic-payer"),
                    tile("NaviNet Prior Auth", "api", "Authorization requests, determinations and appeal status exchanged with provider portals.", "navinet"),
                    tile("Change Healthcare Clinical", "stream", "Lab, imaging and ADT feeds supplementing claims with clinical context.", "change-healthcare")
                ]},
                {"box": "Pharmacy & Network", "ic": "product", "tiles": [
                    tile("CVS Caremark PBM", "market", "Pharmacy claims, formulary access edits, specialty dispensing and rebate accruals from the pharmacy benefit manager.", ["caremark", "mmit", "accredo"]),
                    tile("Symplr Provider Data", "people", "Credentialing, roster and directory accuracy for network adequacy.", "symplr"),
                    tile("CMS Encounter Data", "gavel", "Risk adjustment diagnoses and encounter records submitted for Medicare Advantage.", "cms-encounter")
                ]},
                fed_group(
                    "TPA Sub-claims",
                    "Third-party administrator claim detail left at TPAs and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("X12 EDI Clearinghouse", "stream", "837 institutional and professional claims normalised on ingest through the multi-payer network with companion guide validation.", ["x12-edi", "avality"]),
                tile("NCQA HEDIS Measures", "gavel", "Measure specification updates consumed inbound before HEDIS season.", "ncqa-hedis"),
                tile("CMS Risk Model Files", "chart", "HCC coefficients and model software updates for risk adjustment scoring.")
            ]),
            "ppl": ppl2([
                biz("CEO & CFO", "Genie One", "The CEO on membership growth and medical loss ratio; the CFO on risk-adjusted revenue, medical trend and reserve adequacy by line of business.",
                    [["Genie One", "Ask what medical trend was last month by line of business without waiting on actuarial."], ["AI/BI", "MLR, membership and quality on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"paid claim\" means one thing across admin systems."]]),
                biz("Actuarial & Finance", "AI/BI", "Pricing, reserving and risk-score reconciliation for Medicare and commercial blocks, chasing HCC completeness before the submission window closes.",
                    [["Risk Adjustment Workbench", "HCC gaps and encounter completeness before submission."], ["AI/BI", "MLR and trend on certified Metric Views the board reads."], ["Unity Catalog", "One definition of premium and claims across lines."]]),
                biz("Care Management", "Model Serving", "Nurses and care coordinators on rising-risk members, open gaps in care and readmission prevention before an avoidable ED visit or admission.",
                    [["Care Manager Console", "Rising-risk members ranked before ED utilisation spikes."], ["Model Serving", "Risk models scored at enrollment and monthly refresh."], ["CustomerLake", "Member segments without copying clinical exports elsewhere."]]),
                biz("Provider Relations", "AI/BI", "Contracting on network adequacy, value-based arrangement performance and out-of-network leakage when a provider dispute lands.",
                    [["Provider Scorecard", "Quality and cost metrics by TIN and contract."], ["AI/BI", "Network leakage and adequacy on governed definitions."], ["Genie One", "Ask which specialties drive out-of-network spend."]]),
                biz("Fraud & Integrity", "Lakehouse//RT", "SIU investigators on aberrant provider billing patterns, duplicate claims and pharmacy fraud, flagged pre-pay before dollars go out the door.",
                    [["FWA Command Centre", "Anomaly clusters flagged before payment releases."], ["Lakehouse//RT", "Pre-pay edits scored at adjudication latency."], ["AI/BI", "Recovery and avoidance on certified Metric Views."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the EDI claims, enrollment and clinical feeds; own the Bronze to Silver path and the pager when an 837 load breaks.",
                    [["Lakeflow Connect", "Managed connectors for core admin, clinical and pharmacy sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on claims and enrollment feeds."], ["Lakewatch", "Freshness on the tables actuarial and care teams read every morning."]]),
                biz("Data Scientists", "MLflow", "Risk-adjustment, rising-risk and fraud-waste-and-abuse models, and whether they still hold across a plan year.",
                    [["Feature Store", "Member features defined once for training and serving."], ["MLflow", "Every risk model run tracked for audit and reproduction."], ["Model Serving", "Risk and FWA models scored at enrollment and adjudication."]]),
                biz("App Developers", "Apps", "Ship the care manager, risk-adjustment and FWA applications the plan works in, hosted next to governed data.",
                    [["Apps", "Care and integrity screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for care-plan and claims-edit writes."], ["Agent Bricks", "Agents that draft an outreach or edit override against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and care team updates in the channel coordinators already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Admin Writeback", "ic": "opdb", "tiles": [
                    tile("Claims Edit Overrides", "db", "Medical director and SIU decisions written back into adjudication before payment.", "facets"),
                    tile("Care Plan Tasks", "apps", "Outreach and intervention tasks pushed to care manager workflows.", "epic-payer"),
                    tile("Provider Roster Updates", "people", "Directory corrections written back after credentialing review.", "symplr")
                ]},
                {"box": "Provider & Members", "ic": "partner", "tiles": [
                    tile("Provider Portal Data", "share", "Quality scorecards and remittance detail shared with provider groups over Delta Sharing."),
                    tile("Member App Personalisation", "custlake", "Benefit and care gap nudges triggered from governed member segments."),
                    tile("Broker & Employer Reporting", "partner", "Group renewal and experience metrics exchanged with distribution partners.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("CMS Star & HEDIS", "gavel", "HEDIS, Stars and MLR reports produced from the same governed tables operations runs on.", "ncqa-hedis"),
                    tile("State Filing Packages", "share", "Rate and form filings assembled from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Employers, providers and regulators reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Care Manager Console", "Population health", "people", "Rising-risk members, gaps in care and authorised interventions on one screen for nurse care managers."),
                app("Risk Adjustment Workbench", "Medicare revenue", "chart", "HCC capture gaps and encounter completeness scored before CMS submission windows close."),
                app("FWA Command Centre", "Payment integrity", "gauge", "Provider and pharmacy anomaly clusters flagged before claims pay or after for recovery."),
                app("Provider Scorecard", "Network value", "market", "Quality, cost and patient experience by TIN for value-based contract negotiations."),
            ],
            [
                uc("Risk Adjustment", "Medicare", "chart", "HCC capture and encounter data completeness maximised before annual risk model runs."),
                uc("Medical Loss Ratio", "Finance", "market", "MLR tracked by line and market with trend drivers actuaries can explain to regulators."),
                uc("HEDIS Quality", "Stars", "gavel", "Measure gaps closed through outreach before submission season, not after chart chase."),
                uc("Fraud Waste & Abuse", "Integrity", "gauge", "Billing patterns and pharmacy anomalies detected pre-pay and recovered post-pay."),
                uc("Care Management", "Clinical", "people", "High-cost members identified and engaged before preventable admissions."),
                uc("Network Adequacy", "Provider", "globe", "Directory accuracy and time-and-distance standards monitored for regulatory compliance."),
                uc("Prior Auth Optimisation", "Utilisation", "api", "Authorization turnaround and denial overturn rates improved without loosening medical necessity."),
                uc("Pharmacy Trend", "PBM", "product", "Specialty spend, formulary adherence and rebate performance reconciled to medical trend."),
                uc("Member Retention", "Growth", "custlake", "Disenrollment risk scored from service complaints, claims gaps and digital engagement."),
                uc("Value-Based Contracts", "Provider", "partner", "Shared savings and quality bonuses calculated from governed claims and clinical data."),
            ],
        ),
        "sources": {
            "facets": {"t": "Oracle Health Facets", "u": "https://www.oracle.com/health/"},
            "healthedge": {"t": "HealthEdge Source", "u": "https://healthedge.com/solutions/source"},
            "cotiviti": {"t": "Cotiviti payment integrity", "u": "https://www.cotiviti.com/solutions/payment-accuracy"},
            "epic-payer": {"t": "Epic Payer Platform", "u": "https://www.epic.com/software/payer-platform"},
            "navinet": {"t": "NaviNet prior authorization", "u": "https://www.navinet.net/"},
            "change-healthcare": {"t": "Change Healthcare clinical connectivity", "u": "https://www.changehealthcare.com/"},
            "caremark": {"t": "CVS Caremark pharmacy benefits", "u": "https://www.caremark.com/"},
            "accredo": {"t": "Accredo specialty pharmacy", "u": "https://www.accredo.com/"},
            "mmit": {"t": "MMIT formulary access", "u": "https://www.mmitnetwork.com/"},
            "symplr": {"t": "Symplr provider management", "u": "https://www.symplr.com/"},
            "avality": {"t": "Avality multi-payer network", "u": "https://www.availity.com/"},
            "cms-encounter": {"t": "CMS encounter data submission", "u": "https://www.cms.gov/medicare/payment/medicare-advantage-rates-statistics/risk-adjustment"},
            "x12-edi": {"t": "X12 EDI standards", "u": "https://x12.org/"},
            "ncqa-hedis": {"t": "NCQA HEDIS measures", "u": "https://www.ncqa.org/hedis/"}
        },
    },
    "healthcare": {
        "label": "Healthcare",
        "blurb": "Health systems and hospitals: EHR clinical data, revenue cycle, capacity management, population health and quality reporting.",
        "medallion": medallion(
            "Raw clinical feeds",
            "HL7 ADT and ORU messages, FHIR resources, charge master transactions, imaging DICOM metadata and device telemetry, landed exactly as received so a diagnosis or a charge can always be replayed.",
            "Conformed patient, encounter",
            "Patients, encounters, orders and charges resolved into single conformed entities across EHR, billing and ancillary systems, with MRNs reconciled and transfers stitched to one episode.",
            "LOS, margin, outcomes",
            "Contracted products clinical and finance leaders run on: length of stay, contribution margin by service line, readmission rates, and quality measure attainment.",
        ),
        "rails": {
            "src": [
                {"box": "EHR & Clinical", "ic": "erp", "tiles": [
                    tile("Epic Caboodle", "db", "Orders, results, notes and billing extracts from the hospital EHR of record.", "epic"),
                    tile("Oracle Health Millennium", "erp", "Inpatient and ambulatory clinical, scheduling and documentation for Cerner estates.", "oracle-millennium"),
                    tile("Meditech Expanse", "sheet", "Acute and post-acute clinical records for community hospital networks.", "meditech")
                ]},
                {"box": "Revenue Cycle", "ic": "market", "tiles": [
                    tile("R1 RCM Platform", "market", "Charge capture, claims scrubbing, denials and patient collections workflow.", "r1-rcm"),
                    tile("Waystar Claims", "api", "Eligibility, prior auth status and remittance advice across payers.", "waystar"),
                    tile("3M CodeAssist", "gavel", "CDI queries, DRG grouping and coding compliance suggestions.", "3m-codeassist")
                ]},
                {"box": "Imaging & Devices", "ic": "iot", "tiles": [
                    tile("Philips IntelliSpace", "stream", "Radiology worklists, study metadata and dose metrics from imaging PACS.", "philips-pacs"),
                    tile("Capsule Medical Device", "iot", "Bedside monitor vitals, ventilator settings and infusion pump alarms.", "capsule"),
                    tile("Masimo Patient SafetyNet", "gauge", "Continuous pulse oximetry and early warning scores from wearable sensors.", "masimo")
                ]},
                {"box": "Operations & Staffing", "ic": "people", "tiles": [
                    tile("TeleTracking Capacity", "gauge", "Bed requests, patient placement and transfer centre milestones.", "teletracking"),
                    tile("Kronos Workforce", "people", "Nurse schedules, acuity staffing and overtime by unit.", "kronos"),
                    tile("Press Ganey Experience", "partner", "HCAHPS and point-of-care patient satisfaction surveys.", "press-ganey")
                ]},
                fed_group(
                    "Affiliate EHR Feeds",
                    "Joint venture and affiliated clinic clinical summaries left at partner systems and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("HL7 FHIR Bulk Data", "api", "Patient, encounter and observation exports normalised on ingest for analytics.", "fhir-bulk"),
                tile("CMS Quality Reporting", "gavel", "Hospital compare and value-based programme specifications consumed inbound.", "cms-quality"),
                tile("Syndromic Surveillance", "stream", "Public health case feeds exchanged under state reporting agreements.")
            ]),
            "ppl": ppl2([
                biz("CEO, CNO & CMO", "Genie One", "The CEO on volume, contribution margin and quality scores; the CNO on staffing and patient safety; the CMO on outcomes and 30-day readmissions.",
                    [["Genie One", "Ask what yesterday's census and contribution margin were without waiting on finance."], ["AI/BI", "Volume, margin and quality on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"contribution margin\" means one thing across the health system."]]),
                biz("Clinical Operations", "Lakehouse//RT", "Bed management, ED throughput and OR scheduling on a typical inpatient day, moving boarding patients before diversion becomes necessary.",
                    [["Capacity Command Centre", "ED boarding and bed placement options costed in real time."], ["Lakehouse//RT", "Live census and acuity at hospital operational latency."], ["AI/BI", "LOS and throughput on governed definitions."]]),
                biz("Revenue Cycle", "AI/BI", "Denials, underpayments and CDI queries that decide whether documented care is actually paid, flagged before the claim leaves the building.",
                    [["Denial Prevention Workbench", "At-risk accounts flagged before claim submission."], ["AI/BI", "Net revenue and denial rate on certified Metric Views."], ["Unity Catalog", "One definition of charges and payments across EHR and RCM."]]),
                biz("Population Health", "Model Serving", "Care managers and physicians on attributed panels, open gaps in care and rising-risk patients before preventable utilisation spikes.",
                    [["Population Health Registry", "Attributed patients ranked by preventable utilisation risk."], ["Model Serving", "Readmission models scored at discharge."], ["CustomerLake", "Panel segments without copying payer files elsewhere."]]),
                biz("Quality & Safety", "AI/BI", "Infection prevention, sepsis-bundle compliance and hospital-acquired-condition reduction, catching the deterioration before the public measure does.",
                    [["Quality Dashboard", "Core measures and HAC rates before public reporting."], ["AI/BI", "Mortality and complication indices on governed definitions."], ["Genie One", "Ask which units drove last month's CLABSI count."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the EHR, revenue-cycle and device feeds; own the Bronze to Silver path and the pager when an HL7 or charge feed breaks.",
                    [["Lakeflow Connect", "Managed connectors for EHR, RCM and ancillary sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on ADT and charge feeds."], ["Lakewatch", "Freshness on the tables the command centre and finance read every morning."]]),
                biz("Data Scientists", "MLflow", "Readmission, sepsis and denial-risk models, and whether they still hold six months after deployment.",
                    [["Feature Store", "Patient and encounter features defined once for training and serving."], ["MLflow", "Every clinical model run tracked for audit and reproduction."], ["Model Serving", "Readmission and sepsis models scored at discharge and bedside."]]),
                biz("App Developers", "Apps", "Ship the capacity, denial-prevention and population-health applications the health system works in, hosted next to governed data.",
                    [["Apps", "Capacity and revenue screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for bed-placement and query writes."], ["Agent Bricks", "Agents that draft a CDI query or discharge plan against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and capacity alerts in the channel operations already works in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Clinical Writeback", "ic": "opdb", "tiles": [
                    tile("EHR Chart Queries", "db", "CDI and quality queries written back into the EHR inbox for physician response.", "epic"),
                    tile("Bed Placement Orders", "gauge", "Accepted bed assignments pushed to transport and nursing workflows.", "teletracking"),
                    tile("Care Gap Outreach", "apps", "Preventive care tasks pushed to ambulatory care teams from panel registries.")
                ]},
                {"box": "Payer & Community", "ic": "partner", "tiles": [
                    tile("Payer Risk Contracts", "share", "Quality and utilisation metrics shared with payers under value-based arrangements."),
                    tile("HIE Clinical Exchange", "api", "Summaries and referrals exchanged with regional health information exchanges.", "fhir-bulk"),
                    tile("Employer Reporting", "partner", "Occupational health and direct-contract outcomes reported to self-insured employers.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("CMS Quality Programs", "gavel", "HAC, readmission and MIPS measures produced from governed clinical tables.", "cms-quality"),
                    tile("State Reporting", "share", "Mandatory infection and utilization filings assembled from Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Researchers, payers and affiliates reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Capacity Command Centre", "Patient flow", "gauge", "ED boarding, bed placement and surgical holds costed in real time before diversion becomes necessary."),
                app("Denial Prevention Workbench", "Revenue integrity", "market", "Accounts at risk of denial flagged from documentation, coding and payer rules before claims submit."),
                app("Population Health Registry", "Attributed panels", "people", "Rising-risk patients and gaps in care ranked for outreach before utilisation spikes."),
                app("Sepsis Surveillance", "Patient safety", "iot", "Early warning from vitals, labs and nursing assessments before bundle compliance windows close."),
            ],
            [
                uc("Hospital Throughput", "Operations", "gauge", "ED boarding, discharge planning and OR turnover optimised as one patient-flow problem."),
                uc("Readmission Reduction", "Quality", "people", "Discharge risk scored and interventions triggered before the 30-day window opens."),
                uc("Denial Management", "Revenue", "market", "Root causes of denials traced to documentation, coding and authorization gaps."),
                uc("Sepsis Early Warning", "Safety", "iot", "Deterioration detected from streaming vitals and labs before codes are called."),
                uc("OR Utilisation", "Surgical", "sheet", "Block time, turnover and case mix analysed to recover lost surgical minutes."),
                uc("Nurse Staffing", "Workforce", "people", "Acuity-adjusted schedules that match census forecasts without chronic overtime."),
                uc("Clinical Documentation", "CDI", "gavel", "Queries raised where clinical truth and billed severity diverge before final coding."),
                uc("Imaging Utilisation", "Ancillary", "stream", "Appropriate use and turnaround analysed by modality and site."),
                uc("Patient Experience", "HCAHPS", "partner", "Satisfaction drivers linked to operational and clinical variables teams can act on."),
                uc("Research Cohorts", "Evidence", "notebook", "De-identified cohorts built from governed EHR data under IRB protocols."),
            ],
        ),
        "sources": {
            "epic": {"t": "Epic Systems EHR", "u": "https://www.epic.com/"},
            "oracle-millennium": {"t": "Oracle Health Millennium", "u": "https://www.oracle.com/industries/healthcare/"},
            "meditech": {"t": "Meditech Expanse", "u": "https://ehr.meditech.com/"},
            "r1-rcm": {"t": "R1 RCM revenue cycle", "u": "https://www.r1rcm.com/"},
            "waystar": {"t": "Waystar healthcare payments", "u": "https://www.waystar.com/"},
            "3m-codeassist": {"t": "3M CodeAssist CDI", "u": "https://www.3m.com/3M/en_US/health-information-systems-us/"},
            "philips-pacs": {"t": "Philips IntelliSpace PACS", "u": "https://www.philips.com/healthcare"},
            "capsule": {"t": "Capsule medical device integration", "u": "https://www.capsuletech.com/"},
            "masimo": {"t": "Masimo Patient SafetyNet", "u": "https://www.masimo.com/"},
            "teletracking": {"t": "TeleTracking capacity management", "u": "https://www.teletracking.com/"},
            "kronos": {"t": "UKG workforce management", "u": "https://www.ukg.com/workforce-management"},
            "press-ganey": {"t": "Press Ganey patient experience", "u": "https://www.pressganey.com/"},
            "fhir-bulk": {"t": "HL7 FHIR Bulk Data Access", "u": "https://hl7.org/fhir/uv/bulkdata/"},
            "cms-quality": {"t": "CMS hospital quality reporting", "u": "https://www.cms.gov/medicare/quality/initiatives/hospital-quality-initiative"}
        },
    },
    "legal": {
        "label": "Legal",
        "blurb": "Law firms and corporate legal departments: matter management, e-discovery, contract lifecycle, time and billing, and regulatory compliance.",
        "medallion": medallion(
            "Raw matter and document feeds",
            "DMS documents, billing entries, court docket events, contract repository versions and e-discovery load files, landed exactly as received so a privilege call or a time entry can always be replayed.",
            "Conformed matter, client",
            "Clients, matters, documents and timekeepers resolved into single conformed entities across DMS, billing and CLM systems, with matter IDs reconciled and related-party conflicts stitched to one engagement.",
            "Realization, risk, compliance",
            "Contracted products practice and finance leaders run on: realization rate and leverage, matter profitability, e-discovery review throughput, and outside counsel spend against budget.",
        ),
        "rails": {
            "src": [
                {"box": "Document & DMS", "ic": "db", "tiles": [
                    tile("iManage Work", "db", "Matter workspaces, document versions, metadata and ethical wall enforcement.", "imanage"),
                    tile("NetDocuments", "sheet", "Cloud DMS profiles, collaboration and client matter security.", "netdocuments"),
                    tile("Microsoft Purview", "gavel", "Records classification, retention labels and legal hold across M365 estates.", "purview")
                ]},
                {"box": "Practice & Billing", "ic": "erp", "tiles": [
                    tile("Elite 3E", "erp", "Time entries, disbursements, WIP and matter accounting for large firms.", "elite-3e"),
                    tile("Aderant Expert", "market", "Billing, collections and financial reporting across practice groups.", "aderant"),
                    tile("Clio Manage", "apps", "Matter intake, calendaring and trust accounting for mid-market firms.", "clio")
                ]},
                {"box": "E-Discovery", "ic": "gavel", "tiles": [
                    tile("RelativityOne", "gavel", "Processing, review, analytics and production for litigation and investigations.", "relativity"),
                    tile("Everlaw", "partner", "Collaborative review, storybuilder and deposition preparation workflows.", "everlaw"),
                    tile("PACER Court Records", "api", "Federal docket filings, orders and party events from public court systems.", "pacer")
                ]},
                {"box": "Contracts", "ic": "sheet", "tiles": [
                    tile("Ironclad CLM", "product", "Contract intake, negotiation workflow and obligation tracking.", "ironclad"),
                    tile("Thomson Reuters Westlaw", "globe", "Case law, statutes and citator research with usage telemetry.", "westlaw"),
                    tile("LexisNexis Guidance", "notebook", "Practice notes, checklists and standard clauses referenced at drafting.", "lexis")
                ]},
                fed_group(
                    "Client ERP Contract Mart",
                    "Corporate customer contract and vendor obligation marts left in place and queried under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("EDRM XML Load Files", "api", "Standardised processing and review metadata consumed inbound for cross-tool portability.", "edrm"),
                tile("LEDES Billing", "market", "Outside counsel invoice formats validated before accrual and payment.", "ledes"),
                tile("Sanctions & PEP Lists", "gavel", "Watchlist updates consumed inbound for client intake screening.", "worldcheck")
            ]),
            "ppl": ppl2([
                biz("Managing Partner & GC", "Genie One", "The managing partner on realization rate and leverage; the general counsel on outside-counsel spend against budget and matter profitability by practice group.",
                    [["Genie One", "Ask firm-wide realization this quarter without waiting on finance."], ["AI/BI", "Realization, leverage and WIP on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"realization\" means one thing across practices."]]),
                biz("Practice Management", "AI/BI", "Practice leaders on matter staffing and leverage, budget burn by phase and whether contracts hold to the firm playbook before write-offs pile up.",
                    [["Matter Profitability Console", "Budget versus actual by matter phase and timekeeper."], ["Contract Intelligence Hub", "Non-standard clauses flagged at intake against the playbook."], ["AI/BI", "Matter margin and leverage on certified Metric Views."]]),
                biz("Litigation Support", "Lakehouse//RT", "E-discovery managers on custodian completeness, processing queues and reviewer throughput against the court deadline that will not move.",
                    [["Review Command Centre", "Reviewer throughput and custodian completeness before court deadlines."], ["Lakehouse//RT", "Live review progress at case latency."], ["AI/BI", "Review cost and pace per matter on governed definitions."]]),
                biz("Compliance", "AI/BI", "Conflicts, KYC and ethics on new-business intake and ongoing matter monitoring, clearing party hits before an engagement letter releases.",
                    [["Conflicts Clearance", "Party and relationship hits before engagement letters release."], ["AI/BI", "Sanctions and PEP screening on certified views."], ["Unity Catalog", "One definition of party and matter across DMS and billing."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the DMS, billing, docket and CLM feeds; own the Bronze to Silver path and the pager when a review or billing load breaks.",
                    [["Lakeflow Connect", "Managed connectors for iManage, Elite 3E and Relativity sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on billing and review feeds."], ["Lakewatch", "Freshness on the tables practice and finance leaders read every morning."]]),
                biz("Data Scientists", "MLflow", "Privilege-prediction, realization and clause-risk models, and whether they still hold six months after deployment.",
                    [["Feature Store", "Matter and document features defined once for training and serving."], ["MLflow", "Every review model run tracked for audit and reproduction."], ["Model Serving", "Privilege and clause models scored in the review path."]]),
                biz("App Developers", "Apps", "Ship the matter-profitability, review and conflicts applications the firm works in, hosted next to governed data.",
                    [["Apps", "Matter and review screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for review assignments and pre-bill writes."], ["Agent Bricks", "Agents that draft a clause review or conflicts check against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Practice and finance dashboards on serverless SQL with Unity Catalog permissions."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and matter alerts in the channel teams already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Analytics notebooks against governed billing and review data.")
                ]},
                {"box": "Matter Writeback", "ic": "opdb", "tiles": [
                    tile("DMS Metadata Updates", "db", "Privilege and issue codes written back into document profiles after review.", "imanage"),
                    tile("Billing Pre-bill Release", "market", "Approved time and disbursement entries released from WIP to client invoices.", "elite-3e"),
                    tile("Review Assignments", "apps", "Reviewer queues and issue tags pushed to Relativity workspaces.", "relativity")
                ]},
                {"box": "Clients & Counsel", "ic": "partner", "tiles": [
                    tile("Outside Counsel Guidelines", "share", "Budget and staffing compliance shared with panel firms over Delta Sharing."),
                    tile("Corporate Legal Portal", "partner", "Matter status and spend dashboards exchanged with in-house clients."),
                    tile("Court E-filing", "api", "Production sets and certificates of service filed through e-filing gateways.", "pacer")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("LEDES & Accrual Reporting", "gavel", "Outside counsel invoice accruals reconciled to matter budgets from governed billing tables.", "ledes"),
                    tile("Ethics & Audit Trail", "share", "Conflicts clearance and privilege logs filed from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Corporate clients and co-counsel reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Matter Profitability Console", "Practice economics", "market", "Budget, WIP and realization by matter phase and timekeeper before write-offs accumulate."),
                app("Review Command Centre", "E-discovery ops", "gauge", "Custodian completeness, reviewer throughput and production deadlines on one litigation ops screen."),
                app("Contract Intelligence Hub", "CLM analytics", "product", "Non-standard clauses, renewal risk and obligation calendars scored against the firm playbook."),
                app("Conflicts Clearance", "New business", "gavel", "Party and relationship hits surfaced before engagement letters and ethical walls are set."),
            ],
            [
                uc("Matter Profitability", "Finance", "market", "Realization, leverage and matter margin tracked before year-end write-offs."),
                uc("E-Discovery Review", "Litigation", "gauge", "Processing, prioritisation and reviewer throughput optimised against court deadlines."),
                uc("Privilege Prediction", "Risk", "gavel", "Attorney-client and work-product calls assisted with reproducible model evidence."),
                uc("Contract Playbook Compliance", "Commercial", "product", "Clause deviations flagged at intake before negotiation cycles expand."),
                uc("Conflicts Screening", "Ethics", "people", "New business intake screened against parties, matters and watchlists in one governed graph."),
                uc("Outside Counsel Spend", "Corporate", "chart", "Panel firm invoices reconciled to matter budgets and LEDES guidelines."),
                uc("Legal Research Analytics", "Knowledge", "notebook", "Precedent and research usage tied to matter outcomes and staffing decisions."),
                uc("Docket Monitoring", "Litigation", "api", "Court filings and orders tracked across matters without manual PACER pulls."),
                uc("Records Retention", "Compliance", "db", "Legal holds and disposition executed from governed retention policies."),
                uc("Time Entry Compliance", "Billing", "erp", "Narrative and UTBMS code quality scored before invoices reach clients."),
            ],
        ),
        "sources": {
            "imanage": {"t": "iManage Work", "u": "https://imanage.com/product/imanage-work/"},
            "netdocuments": {"t": "NetDocuments", "u": "https://www.netdocuments.com/"},
            "purview": {"t": "Microsoft Purview", "u": "https://learn.microsoft.com/en-us/purview/"},
            "elite-3e": {"t": "Elite 3E", "u": "https://www.elite.com/products/3e/"},
            "aderant": {"t": "Aderant Expert", "u": "https://www.aderant.com/products/expert/"},
            "clio": {"t": "Clio Manage", "u": "https://www.clio.com/"},
            "relativity": {"t": "RelativityOne", "u": "https://www.relativity.com/"},
            "everlaw": {"t": "Everlaw", "u": "https://www.everlaw.com/"},
            "pacer": {"t": "PACER court records", "u": "https://pacer.uscourts.gov/"},
            "ironclad": {"t": "Ironclad CLM", "u": "https://ironcladapp.com/"},
            "westlaw": {"t": "Thomson Reuters Westlaw", "u": "https://legal.thomsonreuters.com/en/westlaw"},
            "lexis": {"t": "LexisNexis Practical Guidance", "u": "https://www.lexisnexis.com/"},
            "edrm": {"t": "EDRM resources", "u": "https://edrm.net/"},
            "ledes": {"t": "LEDES billing formats", "u": "https://ledes.org/"},
            "worldcheck": {"t": "LSEG World-Check", "u": "https://www.lseg.com/en/risk-intelligence/screening-solutions/world-check-kyc-screening"}
        },
    },
    "life_insurance": {
        "label": "Life Insurance",
        "blurb": "Life and annuity carriers: policy administration, underwriting, claims, actuarial reserving, reinsurance and distribution across individual and group blocks.",
        "medallion": medallion(
            "Raw policy and claims feeds",
            "Policy administration transactions, underwriting evidence, claims files, agent commissions and reinsurance bordereaux, landed exactly as received so a premium or a reserve can always be replayed.",
            "Conformed policy, party",
            "Policies, insureds, agents and claims resolved into single conformed entities across admin, underwriting and finance systems, with rider and beneficiary relationships stitched to one contract.",
            "Persistency, mortality, margin",
            "Contracted products actuarial and distribution leaders run on: persistency and lapse rates, mortality and morbidity experience, new business strain, and embedded value by product.",
        ),
        "rails": {
            "src": [
                {"box": "Policy Administration", "ic": "erp", "tiles": [
                    tile("FINEOS Life", "erp", "Individual and group life policy issuance, servicing, billing and claims on one admin platform.", "fineos"),
                    tile("Majesco LifePlus", "db", "Policy, billing and claims for life, annuity and supplemental benefits.", "majesco"),
                    tile("Oracle Insurance Policy", "sheet", "Product configuration, policy transactions and financial integration for carriers.", "oracle-insurance")
                ]},
                {"box": "New Business & UW", "ic": "people", "tiles": [
                    tile("Munich Re ALLFINANZ", "partner", "Automated underwriting rules, evidence ordering and risk classification.", "munich-allfinanz"),
                    tile("ExamOne Lab Results", "stream", "Paramedical exams, labs and APS retrieval tied to application case IDs.", "examone"),
                    tile("MIB Underwriting Exchange", "gavel", "Industry application history and code hits at point of underwriting.", "mib")
                ]},
                {"box": "Claims & Customer", "ic": "market", "tiles": [
                    tile("Sedgwick Life Claims", "market", "Death, disability and waiver claims intake, adjudication and payment.", "sedgwick"),
                    tile("Salesforce Financial Services", "custlake", "Agent and policyholder relationships, service cases and cross-sell opportunities.", "sf-finserv"),
                    tile("Call Centre Telephony", "chat", "IVR, call recordings and disposition codes joined to policy and claim events.")
                ]},
                {"box": "Actuarial & Finance", "ic": "chart", "tiles": [
                    tile("Moody's Analytics AXIS", "chart", "Actuarial models, reserves, capital and asset-liability management projections.", "axis"),
                    tile("SAP S/4HANA Insurance", "erp", "General ledger, statutory reporting and investment accounting integration.", "sap-insurance"),
                    tile("Reinsurance Bordereaux", "partner", "Ceded premium, claims and experience reports exchanged with reinsurance partners.")
                ]},
                fed_group(
                    "MGU Admin Feeds",
                    "Managing general underwriter policy detail left at partners and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("ACORD Life Standards", "api", "Application, policy and claims XML messages normalised on ingest for straight-through processing.", "acord"),
                tile("NAIC Statutory Filings", "gavel", "Annual statement schedules and risk-based capital specifications consumed inbound.", "naic"),
                tile("Mortality Table Updates", "chart", "Industry mortality and lapse assumptions published by regulators and reinsurers.")
            ]),
            "ppl": ppl2([
                biz("CEO & CFO", "Genie One", "The CEO on new-business volume and embedded value; the CFO on statutory reserves, risk-based capital and the expense ratio by product line.",
                    [["Genie One", "Ask what last month's issued premium was by product without waiting on actuarial."], ["AI/BI", "Persistency, mortality and margin on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"in-force\" means one thing across admin and finance."]]),
                biz("Actuarial & Reserving", "AI/BI", "Appointed actuaries on reserve adequacy, mortality and lapse experience studies and the model governance a statutory opinion depends on.",
                    [["Reserve Analytics Workbench", "Experience versus pricing assumptions before opinion sign-off."], ["AI/BI", "Reserve roll-forward and variance on certified Metric Views."], ["Unity Catalog", "One definition of claim and policy counts across systems."]]),
                biz("Underwriting", "Model Serving", "Chief underwriters on straight-through-processing rates, evidence-ordering bottlenecks and mortality leakage before an offer expires.",
                    [["Underwriting Decision Hub", "Risk class and evidence status before offers expire."], ["Model Serving", "Mortality and lapse models scored at application."], ["MLflow", "Every underwriting model run tracked for audit."]]),
                biz("Claims", "Lakehouse//RT", "Claims operations on death verification, contestable-period review and beneficiary payout, ranking open claims by SLA and fraud signal before disbursement.",
                    [["Claims Adjudication Console", "Open claims ranked by SLA and fraud signals."], ["Lakehouse//RT", "Claim status at operational latency."], ["AI/BI", "Severity and cycle time on governed definitions."]]),
                biz("Distribution", "CustomerLake", "Agency leaders on producer productivity, block persistency and suitability compliance when a lapse or replacement spike shows up.",
                    [["Agent Performance Hub", "Production, persistency and complaints by channel."], ["CustomerLake", "Household segments without copying CRM exports elsewhere."], ["Genie One", "Ask which agents drove last month's lapse spike."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the policy-admin, underwriting and reinsurance feeds; own the Bronze to Silver path and the pager when a bordereau load breaks.",
                    [["Lakeflow Connect", "Managed connectors for FINEOS, underwriting and finance sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on policy and claims feeds."], ["Lakewatch", "Freshness on the tables actuarial and distribution read every morning."]]),
                biz("Data Scientists", "MLflow", "Mortality, lapse and claims-fraud models, and whether they still hold across an experience study.",
                    [["Feature Store", "Policy and party features defined once for training and serving."], ["MLflow", "Every underwriting model run tracked for audit and reproduction."], ["Model Serving", "Mortality and lapse models scored at application and renewal."]]),
                biz("App Developers", "Apps", "Ship the underwriting, claims and agent-performance applications the carrier works in, hosted next to governed data.",
                    [["Apps", "Underwriting and claims screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for servicing and claims writes."], ["Agent Bricks", "Agents that draft an underwriting or claims decision against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Actuarial and distribution dashboards on serverless SQL with Unity Catalog permissions."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and claims alerts in the channel teams already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Actuarial notebooks against governed policy and experience data.")
                ]},
                {"box": "Admin Writeback", "ic": "opdb", "tiles": [
                    tile("Policy Servicing Updates", "db", "Beneficiary and address changes written back into admin after verification.", "fineos"),
                    tile("Underwriting Decisions", "people", "Approved risk classes and requirements released to issuance workflows.", "munich-allfinanz"),
                    tile("Claims Payments", "market", "Adjudicated claim amounts released to disbursement after fraud review.", "sedgwick")
                ]},
                {"box": "Dist. & Reinsurance", "ic": "partner", "tiles": [
                    tile("Agent Portal Reporting", "share", "Production and persistency scorecards shared with agencies over Delta Sharing."),
                    tile("Reinsurer Bordereaux", "partner", "Ceded experience and claims detail exchanged under treaty agreements."),
                    tile("Broker Illustration Systems", "api", "Approved product illustrations and rates pushed to broker platforms.", "acord")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("NAIC Statutory Statements", "gavel", "Annual statement schedules produced from the same governed tables finance runs on.", "naic"),
                    tile("Experience Study Filing", "share", "Mortality and lapse studies filed from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "Reinsurers, distributors and regulators reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Underwriting Decision Hub", "New business", "people", "Application evidence, risk class and straight-through eligibility on one screen before offers expire."),
                app("Claims Adjudication Console", "Benefit payout", "gauge", "Death and disability claims ranked by SLA, contestability and fraud signals before disbursement."),
                app("Reserve Analytics Workbench", "Actuarial", "chart", "Experience versus pricing assumptions reconciled before reserve opinion and statutory filing."),
                app("Agent Performance Hub", "Distribution", "custlake", "Production, persistency and complaint rates by agent and channel for compensation and compliance."),
            ],
            [
                uc("Mortality Underwriting", "Risk selection", "people", "Applicant risk classified with evidence completeness tracked before bind."),
                uc("Lapse & Persistency", "Retention", "gauge", "Policies at risk of lapse identified from payment, service and engagement signals."),
                uc("Claims Fraud Detection", "Integrity", "stream", "Suspicious death and disability claims flagged before payout."),
                uc("Reserve Adequacy", "Actuarial", "chart", "Reserve roll-forward and experience variance explained before opinion sign-off."),
                uc("New Business Strain", "Finance", "market", "Acquisition costs and strain capital modelled by product and distribution channel."),
                uc("Agent Suitability", "Compliance", "gavel", "Sales practices and replacement activity monitored against suitability rules."),
                uc("Reinsurance Recovery", "Treaty", "partner", "Ceded claims and experience reconciled to bordereaux without manual disputes."),
                uc("Cross-sell Propensity", "Growth", "custlake", "Annuity and supplemental offers scored from in-force household relationships."),
                uc("Straight-Through Processing", "Operations", "api", "Clean applications issued without manual touch when evidence and rules align."),
                uc("Embedded Value", "Strategy", "product", "In-force value and new business contribution tracked for portfolio decisions."),
            ],
        ),
        "sources": {
            "fineos": {"t": "FINEOS Life", "u": "https://www.fineos.com/"},
            "majesco": {"t": "Majesco LifePlus", "u": "https://www.majesco.com/solutions/life-insurance/"},
            "oracle-insurance": {"t": "Oracle Insurance Policy Administration", "u": "https://www.oracle.com/industries/financial-services/insurance/"},
            "munich-allfinanz": {"t": "Munich Re ALLFINANZ", "u": "https://www.munichre.com/automation-solutions/en.html"},
            "examone": {"t": "ExamOne paramedical services", "u": "https://www.examone.com/"},
            "mib": {"t": "MIB underwriting exchange", "u": "https://www.mib.com/"},
            "sedgwick": {"t": "Sedgwick claims management", "u": "https://www.sedgwick.com/"},
            "sf-finserv": {"t": "Salesforce Financial Services Cloud", "u": "https://www.salesforce.com/financial-services/"},
            "axis": {"t": "Moody's Analytics AXIS", "u": "https://www.moodysanalytics.com/product-list/axis"},
            "sap-insurance": {"t": "SAP for Insurance", "u": "https://www.sap.com/industries/insurance.html"},
            "acord": {"t": "ACORD standards", "u": "https://www.acord.org/"},
            "naic": {"t": "NAIC statutory reporting", "u": "https://www.naic.org/"},
        },
    },
}
