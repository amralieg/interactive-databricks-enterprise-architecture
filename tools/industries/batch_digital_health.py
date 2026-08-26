import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_DIGITAL_HEALTH = {
    "digital_health": {
        "label": "Digital Health",
        "blurb": "Telehealth and virtual-care platforms: video and asynchronous visits, remote patient monitoring and wearables, care management, FHIR-based EHR integration, member engagement and outcomes.",
        "medallion": medallion(
            "Raw visit, device, claim feeds",
            "Video and async visit records from the telehealth platform, device telemetry from wearables and RPM kits, FHIR resources pulled from EHRs, engagement events and eligibility and paid-claims files, landed exactly as received so a reading or a visit can always be replayed as it stood.",
            "Conformed member, encounter, device",
            "Members, encounters, care plans and device streams resolved into single conformed entities across the telehealth, monitoring and engagement estates, with FHIR Patient and Observation identities matched and eligibility reconciled to one member record.",
            "Engagement, outcomes, cost of care",
            "Contracted products clinical and commercial teams run on: visit access and no-show rates, RPM adherence and alert precision, care-gap closure and quality measures, engagement and retention, and clinical and financial outcomes by cohort.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Virtual Care Platform",
                    "ic": "erp",
                    "tiles": [
                        tile(
                            "Amwell Platform",
                            "erp",
                            "The virtual-care platform of record: scheduled and on-demand video visits, provider queues and visit notes, and the source of the telehealth encounter.",
                            "amwell",
                        ),
                        tile(
                            "Teladoc Health",
                            "erp",
                            "Whole-person virtual care across urgent, chronic and mental health, carrying visits, programmes and clinician assignments into the estate.",
                            "teladoc",
                        ),
                        tile(
                            "Zoom for Healthcare",
                            "globe",
                            "HIPAA-configured video sessions embedded in the care journey, the media and connection quality feed behind each visit.",
                            "zoom-health",
                        ),
                        tile(
                            "Doxy.me Telehealth",
                            "globe",
                            "Browser-based telemedicine for lightweight virtual visits, feeding session and waiting-room events where Doxy.me is the incumbent.",
                            "doxyme",
                        ),
                    ],
                },
                {
                    "box": "Clinical & EHR (FHIR)",
                    "ic": "partner",
                    "tiles": [
                        tile(
                            "Epic FHIR APIs",
                            "erp",
                            "Patient, Encounter, Observation and Medication resources pulled from the EHR over FHIR R4, the clinical spine every care plan is joined to.",
                            "epic-fhir",
                        ),
                        tile(
                            "athenahealth API",
                            "erp",
                            "Ambulatory EHR and practice data over athenahealth's APIs, feeding problems, medications and results where athena is the record.",
                            "athenahealth",
                        ),
                        tile(
                            "Redox Interop",
                            "partner",
                            "Interoperability layer normalising HL7 v2 and FHIR across dozens of EHRs into one integration the platform reads.",
                            "redox",
                        ),
                        tile(
                            "Health Gorilla",
                            "partner",
                            "National FHIR network for clinical records, labs and patient query, the source of longitudinal history beyond the platform's own visits.",
                            "health-gorilla",
                        ),
                    ],
                },
                {
                    "box": "RPM & Wearables",
                    "ic": "iot",
                    "tiles": [
                        tile(
                            "Validic Device Hub",
                            "iot",
                            "Device-data aggregation across hundreds of wearables and RPM kits, normalising readings into one Observation stream.",
                            "validic",
                        ),
                        tile(
                            "Apple HealthKit",
                            "iot",
                            "Steps, heart rate, sleep and workout data shared from the member's phone, the consumer-side signal behind adherence and coaching.",
                            "healthkit",
                        ),
                        tile(
                            "Dexcom CGM",
                            "iot",
                            "Continuous glucose readings streamed from the sensor, the ground truth for diabetes and cardiometabolic programmes.",
                            "dexcom",
                        ),
                        tile(
                            "Fitbit & Google Fit",
                            "iot",
                            "Activity, resting heart rate and sleep from consumer wearables, joined to programmes for behavioural and outcome signals.",
                            "fitbit",
                        ),
                    ],
                },
                {
                    "box": "Member Engagement",
                    "ic": "custlake",
                    "tiles": [
                        tile(
                            "SF Health Cloud",
                            "crm",
                            "Salesforce Health Cloud: member and care-team relationships, service cases and next-best-action, the system of record for engagement and outreach.",
                            "sf-health",
                        ),
                        tile(
                            "Twilio Comms",
                            "chat",
                            "SMS, voice and WhatsApp reminders and nudges, the delivery channel and event source for every outreach the platform sends.",
                            "twilio",
                        ),
                        tile(
                            "Braze Journeys",
                            "custlake",
                            "Lifecycle campaigns and in-app messaging, carrying journey membership, sends and responses into the estate.",
                            "braze",
                        ),
                    ],
                },
                {
                    "box": "Claims & Eligibility",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "Change Healthcare",
                            "market",
                            "Clearinghouse for eligibility, claims and remittance, the gateway between the platform and payer adjudication.",
                            "change",
                        ),
                        tile(
                            "Availity Gateway",
                            "partner",
                            "Real-time eligibility, benefits and prior-authorisation checks against payers, feeding coverage state into the visit path.",
                            "availity",
                        ),
                        tile(
                            "Stripe Payments",
                            "product",
                            "Copay, subscription and self-pay transactions, the source of billing and collection events for the member.",
                            "stripe",
                        ),
                    ],
                },
                fed_group(
                    "Enrollment & Claims",
                    "Employer and payer eligibility, enrollment and adjudicated-claims marts left where they are and queried in place under Unity Catalog, which avoids a second copy of the paid claims.",
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "Twilio Event Streams",
                        "stream",
                        "Delivery, open and reply events from SMS and voice outreach streamed in for engagement and adherence analysis.",
                        "twilio",
                    ),
                    tile(
                        "HL7 & FHIR Messages",
                        "stream",
                        "HL7 v2 ADT and FHIR subscription events parsed on arrival and landed as structured clinical events for near-real-time care.",
                        "hl7-fhir",
                    ),
                    tile(
                        "Kafka Device Events",
                        "eventbus",
                        "High-frequency device telemetry from RPM kits and wearables on existing Kafka or event-hub topics, landed as it streams.",
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Clinical Ops",
                        "Genie One",
                        "The Chief Medical Officer on clinical quality and safety; care-delivery leadership on visit access, clinician utilisation and outcomes; the quality team on measures, escalations and clinical governance.",
                        [
                            ["Genie One", "Ask what this week's no-show rate or alert precision is without booking analyst time."],
                            ["AI/BI", "Visit access, RPM adherence and quality measures on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the clinical glossary, so \"active member\" and \"adherent\" mean one thing across the platform."],
                        ],
                        sub=[
                            ["Chief Medical Officer", "clinical quality, safety and the outcomes story."],
                            ["Care Delivery", "visit access, clinician utilisation and wait times."],
                            ["Quality & Safety", "measures, escalations and clinical governance."],
                        ],
                        ucs=["Virtual Visit Ops", "Risk Stratification", "Care Coordination"],
                    ),
                    biz(
                        "Member Growth",
                        "AI/BI",
                        "The Chief Growth Officer on acquisition, activation and retention; member-engagement leads on outreach performance and adherence; lifecycle marketing on journeys, channels and reactivation.",
                        [
                            ["AI/BI", "Activation, engagement and retention on certified Metric Views."],
                            ["Genie One", "Ask which cohort is disengaging this month without a report pull."],
                            ["Model Serving", "Engagement and adherence propensity scored per member."],
                        ],
                        sub=[
                            ["Chief Growth Officer", "acquisition, activation and retention."],
                            ["Member Engagement", "outreach performance, adherence and satisfaction."],
                            ["Lifecycle Marketing", "journeys, channels and reactivation."],
                        ],
                        ucs=["Member Engagement", "Digital Therapeutics", "Virtual Visit Ops"],
                    ),
                    biz(
                        "Care Management",
                        "Lakehouse//RT",
                        "Care managers running panels of chronic and rising-risk members; RPM nurses triaging device alerts through the day; health coaches driving adherence and behaviour change against the care plan.",
                        [
                            ["Care Command Center", "Device alerts and risk scores on a panel before the day starts."],
                            ["Lakehouse//RT", "Live device, visit and engagement state at the latency a care team acts at."],
                            ["Model Serving", "Deterioration and adherence models scored inside the care path."],
                        ],
                        sub=[
                            ["Care Managers", "chronic and rising-risk panels and escalations."],
                            ["RPM Nurses", "device-alert triage and remote intervention."],
                            ["Health Coaches", "adherence, behaviour change and coaching."],
                        ],
                        ucs=["RPM & Alerting", "Care Gap Closure", "Risk Stratification", "Care Coordination"],
                    ),
                    biz(
                        "Payer Partners",
                        "AI/BI",
                        "The VP of payer partnerships on contract performance and value-based targets; contracting on eligibility, claims and shared-savings settlement; the actuarial and VBC team on cost, utilisation and outcomes attribution.",
                        [
                            ["AI/BI", "Contract performance, cost and utilisation on certified views."],
                            ["Genie One", "Ask what a cohort's cost of care and gap closure look like this quarter."],
                            ["Unity Catalog", "One definition of member, cost and outcome across clinical and finance."],
                        ],
                        sub=[
                            ["VP Partnerships", "contract performance and value-based targets."],
                            ["Contracting", "eligibility, claims and shared-savings settlement."],
                            ["Actuarial & VBC", "cost, utilisation and outcomes attribution."],
                        ],
                        ucs=["Eligibility & Claims", "Outcomes Analytics", "Care Gap Closure"],
                    ),
                    biz(
                        "Product & Data",
                        "Model Serving",
                        "The Chief Product Officer on the digital experience and feature bets; the digital-therapeutics team on programme efficacy and FDA-cleared claims; data science on the models behind coaching, triage and outcomes.",
                        [
                            ["Model Serving", "Coaching, triage and outcome models scored in the member path."],
                            ["MLflow", "Every model versioned for audit, evidence and reproduction."],
                            ["Feature Store", "Member, device and clinical features read identically in training and serving."],
                        ],
                        sub=[
                            ["Chief Product Officer", "the digital experience and feature bets."],
                            ["Digital Therapeutics", "programme efficacy and cleared claims."],
                            ["Data Science", "models behind coaching, triage and outcomes."],
                        ],
                        ucs=["FHIR Interoperability", "Digital Therapeutics", "Outcomes Analytics"],
                    ),
                ],
                [
                    biz(
                        "Health Data Eng",
                        "Lakeflow",
                        "Land telehealth, EHR (FHIR), device and eligibility feeds; build the FHIR-conformed clinical model; own Bronze to Silver and the pager when the care and engagement tables stall.",
                        [
                            ["Lakeflow Connect", "Managed connectors for the telehealth, CRM and claims sources."],
                            ["Lakeflow Designer", "Declarative pipelines with expectations on visit, device and eligibility feeds."],
                            ["Lakewatch", "Freshness on the tables care teams read every morning."],
                        ],
                        ucs=["FHIR Interoperability", "RPM & Alerting", "Eligibility & Claims"],
                    ),
                    biz(
                        "Clinical ML",
                        "MLflow",
                        "Deterioration, readmission-risk, adherence and engagement models built from FHIR, device streams and claims; whether they still hold six months on as cohorts and devices shift.",
                        [
                            ["Feature Store", "Clinical, device and engagement features read identically in training and serving."],
                            ["MLflow", "Every risk and adherence model tracked for audit and reproduction."],
                            ["Model Serving", "Risk and adherence models scored inside the care path."],
                        ],
                        ucs=["Risk Stratification", "Digital Therapeutics", "Care Gap Closure"],
                    ),
                    biz(
                        "App & FHIR Devs",
                        "Apps",
                        "Ship the member app, provider portal and care screens, and the SMART-on-FHIR APIs partners integrate against, hosted next to governed data.",
                        [
                            ["Apps", "Member and care screens with no separate web tier to run or secure."],
                            ["Lakebase", "Serverless Postgres for care-plan state and governed writes."],
                            ["Agent Bricks", "Agents that draft outreach or a care-plan update against governed tools."],
                        ],
                        ucs=["Virtual Visit Ops", "Care Coordination"],
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
                                "Clinical, engagement and outcomes dashboards against serverless SQL with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for governed answers on access, adherence and outcomes in the channel the business already works in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Clinical data-science notebooks and IDEs against governed member, device and claims data.",
                            ),
                        ],
                    },
                    {
                        "box": "Member & Provider Apps",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "Member Mobile App",
                                "apps",
                                "Real-time member profile, adherence and connected-device data served to the app over Lakebase for a live experience.",
                            ),
                            tile(
                                "Provider Portal",
                                "apps",
                                "Panel, alert and outcome views served to clinicians and care teams over governed APIs.",
                            ),
                            tile(
                                "FHIR & SMART APIs",
                                "api",
                                "SMART-on-FHIR endpoints served to partner EHRs and apps against contracted Gold products.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "EHR FHIR Writeback",
                                "erp",
                                "Risk flags, care-gap tasks and observations written back into the EHR over FHIR so the answer reaches the clinician's workflow.",
                                "epic-fhir",
                            ),
                            tile(
                                "Health Cloud Sync",
                                "crm",
                                "Risk, engagement and next-best-action signals written into Salesforce Health Cloud for care-team and outreach action.",
                                "sf-health",
                            ),
                            tile(
                                "Care Plan Writeback",
                                "opdb",
                                "Coaching and care-plan updates written to the care-management workflow on Lakebase in the tool the care team works in.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "HIPAA & HITRUST",
                                "gavel",
                                "PHI access, audit and de-identification governed in Unity Catalog, with HIPAA and HITRUST evidence produced from the same tables.",
                            ),
                            tile(
                                "HEDIS & Star Ratings",
                                "sheet",
                                "Quality measures, HEDIS and Star Ratings submissions produced from contracted Gold products, not a separate extract.",
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
                                "Payers, health-system partners and researchers reading live tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ]
            ),
        },
        "top": top_band(
            [
                app(
                    "Care Command Center",
                    "RPM & care triage",
                    "gauge",
                    "The screen the care team runs the day from: device alerts, deterioration and adherence scores across the panel with next-best-action, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Member 360 Hub",
                    "Engagement",
                    "custlake",
                    "One governed view of the member across visits, devices, claims and engagement, with the outreach and journey history that makes personalisation possible.",
                ),
                app(
                    "Visit Operations",
                    "Telehealth ops",
                    "stream",
                    "Live virtual-care state: clinician availability against demand, queue depth and no-show risk, so visits are staffed and steered before the wait becomes a cancellation.",
                ),
                app(
                    "Outcomes Explorer",
                    "Value-based",
                    "chart",
                    "Clinical and financial outcomes by cohort and programme, so product, clinical and payer teams see what actually moves adherence, gaps and cost of care.",
                ),
            ],
            [
                uc(
                    "Virtual Visit Ops",
                    "Telehealth",
                    "stream",
                    "Matching clinician supply to demand across scheduled and on-demand visits, cutting wait times and no-shows so access holds as volume grows.",
                    problem="Demand for virtual visits is spiky and clinician supply is fixed; without live matching, members wait, clinicians idle, and no-shows waste the slot that a waiting member needed.",
                    who="Clinical Ops",
                    how="Visit, queue and engagement feeds land in Lakehouse//RT; demand and no-show models score through Model Serving and the Visit Operations app steers staffing and reminders before the wait becomes a cancellation.",
                    comps=["Visit Operations", "Amwell Platform", "Lakehouse//RT", "Model Serving", "AI/BI"],
                    stories=[
                        ["Accolade delivers seamless virtual care experiences on Databricks", "https://www.databricks.com/customers/accolade"],
                        ["Bupa unifies telehealth and health data on Databricks", "https://www.databricks.com/customers/bupaaustralia"],
                    ],
                ),
                uc(
                    "RPM & Alerting",
                    "Monitoring",
                    "iot",
                    "Turning high-frequency device telemetry into high-precision clinical alerts, so nurses act on deterioration early without drowning in noise.",
                    problem="RPM kits and wearables push millions of readings in dozens of formats; triaged by hand the signal is lost to alert fatigue, and the deterioration that mattered is seen too late.",
                    who="Care Management",
                    how="Device streams land through Auto Loader and Kafka into Lakehouse//RT; deterioration models score through Model Serving and the Care Command Center on Lakebase drives nurse triage and intervention.",
                    comps=["Care Command Center", "Validic Device Hub", "Kafka Device Events", "Lakehouse//RT", "Model Serving"],
                    stories=[
                        ["Austin Health monitors patients at home with Databricks", "https://www.databricks.com/customers/austin-health"],
                    ],
                ),
                uc(
                    "Member Engagement",
                    "Engagement",
                    "custlake",
                    "Personalised outreach and adherence nudges scored per member against the profile the engagement estate already holds, so activation and retention rise.",
                    problem="Outreach is blasted the same to everyone while the signal to personalise it already sits behind the CRM and messaging estate, unused, so members disengage and programmes churn.",
                    who="Member Growth",
                    how="Engagement, visit and device data are unified through CustomerLake without a separate CDP; propensity and next-best-action are scored in Model Serving and activated through Braze and the Member 360 Hub.",
                    comps=["Member 360 Hub", "CustomerLake", "Braze Journeys", "Model Serving", "AI/BI"],
                    stories=[
                        ["Flo Health scales personalised experiences on Databricks", "https://www.databricks.com/customers/flo-health"],
                    ],
                ),
                uc(
                    "Care Gap Closure",
                    "Quality",
                    "gauge",
                    "Finding open care gaps and quality-measure misses across the panel and driving the outreach and tasks that close them before the measurement window shuts.",
                    problem="Care gaps and HEDIS misses hide across claims, clinical and engagement systems; found late, quality scores slip and avoidable cost lands that a timely nudge would have prevented.",
                    who="Care Management",
                    how="Claims, clinical and engagement data are conformed to certified Gold; gaps are computed on Unity Catalog definitions, scored for outreach priority in Model Serving and pushed to care teams via Health Cloud Sync.",
                    comps=["Enrollment & Claims", "AI/BI", "Model Serving", "Unity Catalog", "Health Cloud Sync"],
                    stories=[
                        ["Healthcare and life sciences on the Databricks Platform", "https://www.databricks.com/solutions/industries/healthcare-and-life-sciences"],
                    ],
                ),
                uc(
                    "Risk Stratification",
                    "Population",
                    "chart",
                    "Ranking members by rising risk from clinical, device and claims signals, so care management works the members most likely to deteriorate first.",
                    problem="Panels are worked by tenure or squeaky wheel, not risk; the member quietly deteriorating is missed while care time is spent where it changes the least.",
                    who="Clinical Ops",
                    how="FHIR clinical history, device features and claims are conformed in the lakehouse; risk models tracked in MLflow score through Model Serving and surface the rising-risk panel in the Care Command Center.",
                    comps=["Care Command Center", "Epic FHIR APIs", "Feature Store", "MLflow", "Model Serving"],
                    stories=[
                        ["Accolade improves member stratification with Databricks", "https://www.databricks.com/customers/accolade"],
                    ],
                ),
                uc(
                    "FHIR Interoperability",
                    "Interop",
                    "api",
                    "Turning HL7 v2, C-CDA and FHIR from many EHRs into one conformed clinical model, so every downstream care and analytics use case reads one patient record.",
                    problem="Clinical data arrives from dozens of EHRs as HL7, C-CDA and nested FHIR JSON; without a conformed model, every team rebuilds the same patient and every join drifts.",
                    who="Product & Data",
                    how="HL7 and FHIR events land through subscriptions into Delta Lake; SQL-on-FHIR transformations build conformed resources served operationally on Lakebase and governed end to end in Unity Catalog.",
                    comps=["HL7 & FHIR Messages", "Redox Interop", "Health Gorilla", "Delta Lake", "Lakebase", "Unity Catalog"],
                    stories=[
                        ["Building a FHIR-native health data platform on Databricks Lakebase", "https://www.databricks.com/blog/building-fhir-native-health-data-platform-databricks-lakebase"],
                    ],
                ),
                uc(
                    "Eligibility & Claims",
                    "Revenue",
                    "market",
                    "Real-time eligibility and benefit checks in the visit path and clean claims out, so members are covered before care and revenue is not lost to rejects.",
                    problem="Eligibility is checked late or not at all and claims reject on avoidable errors; members hit surprise bills and the platform chases denials it could have prevented at the point of care.",
                    who="Payer Partners",
                    how="Change Healthcare and Availity eligibility and claims traffic are conformed in the lakehouse; coverage is verified in the visit path and denial-risk is scored before submission, on pipelines built in Lakeflow.",
                    comps=["Change Healthcare", "Availity Gateway", "Enrollment & Claims", "Lakeflow", "AI/BI"],
                ),
                uc(
                    "Digital Therapeutics",
                    "DTx",
                    "apps",
                    "Powering evidence-based digital coaching for chronic conditions and proving programme efficacy for cleared claims and payer contracts.",
                    problem="Digital therapeutics live or die on efficacy evidence, but coaching signals, device readings and outcomes sit apart, so personalisation is coarse and the evidence base is slow to build.",
                    who="Product & Data",
                    how="Device, engagement and clinical data are aggregated into a member view; coaching and efficacy models tracked in MLflow score through Model Serving and Feature Store into the programme in the Member 360 Hub.",
                    comps=["Member 360 Hub", "Apple HealthKit", "Dexcom CGM", "Model Serving", "MLflow", "Feature Store"],
                    stories=[
                        ["Welldoc enhances cardiometabolic digital coaching on Databricks", "https://www.databricks.com/blog/welldocr-and-databricks-enhancing-cardiometabolic-care-improved-data-tailored-interventions"],
                    ],
                ),
                uc(
                    "Outcomes Analytics",
                    "Value-based",
                    "sheet",
                    "Measuring clinical and financial outcomes by cohort and programme, so product, clinical and payer teams see what actually moves adherence, gaps and cost of care.",
                    problem="Outcomes are reported quarterly from stale extracts that cannot separate what worked from what did not, so value-based contracts are argued on anecdote and product bets are unproven.",
                    who="Payer Partners",
                    how="Clinical, engagement and claims outcomes are conformed to certified Gold; cohort and programme results are explored in AI/BI on Unity Catalog definitions and published as Data Products in the Outcomes Explorer.",
                    comps=["Outcomes Explorer", "AI/BI", "Unity Catalog", "Data Products", "Genie One"],
                    stories=[
                        ["Welldoc surfaces population outcomes for health plans on Databricks", "https://www.databricks.com/blog/welldocr-and-databricks-enhancing-cardiometabolic-care-improved-data-tailored-interventions"],
                        ["Healthcare and life sciences on the Databricks Platform", "https://www.databricks.com/solutions/industries/healthcare-and-life-sciences"],
                    ],
                ),
                uc(
                    "Care Coordination",
                    "Coordination",
                    "people",
                    "Coordinating hand-offs across virtual visits, RPM, coaching and the EHR so the member has one care plan, not a set of disconnected touchpoints.",
                    problem="A member's care is split across telehealth, monitoring, coaching and their provider's EHR; without a shared plan the touchpoints contradict each other and work falls between the teams.",
                    who="Clinical Ops",
                    how="A unified member and care-plan view is served on Lakebase; agents draft hand-offs and updates against governed tools with Agent Bricks and AI Functions and write back to the EHR and Health Cloud.",
                    comps=["Care Command Center", "Agent Bricks", "AI Functions", "Lakebase", "Model Serving"],
                    stories=[
                        ["Bupa builds a unified digital health view on Databricks", "https://www.databricks.com/customers/bupaaustralia"],
                    ],
                ),
            ],
        ),
        "sources": {
            "amwell": {"t": "Amwell virtual care platform", "u": "https://business.amwell.com/"},
            "teladoc": {"t": "Teladoc Health", "u": "https://www.teladochealth.com/"},
            "zoom-health": {"t": "Zoom for Healthcare", "u": "https://www.zoom.com/en/industry/healthcare/"},
            "doxyme": {"t": "Doxy.me telemedicine", "u": "https://doxy.me/"},
            "epic-fhir": {"t": "Epic on FHIR", "u": "https://fhir.epic.com/"},
            "athenahealth": {"t": "athenahealth", "u": "https://www.athenahealth.com/"},
            "redox": {"t": "Redox interoperability", "u": "https://www.redoxengine.com/"},
            "health-gorilla": {"t": "Health Gorilla health data network", "u": "https://www.healthgorilla.com/"},
            "validic": {"t": "Validic device data platform", "u": "https://validic.com/"},
            "healthkit": {"t": "Apple HealthKit", "u": "https://developer.apple.com/health-fitness/"},
            "dexcom": {"t": "Dexcom continuous glucose monitoring", "u": "https://www.dexcom.com/"},
            "fitbit": {"t": "Fitbit", "u": "https://www.fitbit.com/global/us/home"},
            "sf-health": {"t": "Salesforce Health Cloud", "u": "https://www.salesforce.com/products/health-cloud/overview/"},
            "twilio": {"t": "Twilio communications", "u": "https://www.twilio.com/"},
            "braze": {"t": "Braze engagement platform", "u": "https://www.braze.com/"},
            "change": {"t": "Change Healthcare", "u": "https://www.changehealthcare.com/"},
            "availity": {"t": "Availity", "u": "https://www.availity.com/"},
            "stripe": {"t": "Stripe payments", "u": "https://stripe.com/"},
            "hl7-fhir": {"t": "HL7 FHIR", "u": "https://www.hl7.org/fhir/"},
        },
    }
}
