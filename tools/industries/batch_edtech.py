import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_EDTECH = {
    "edtech": {
        "label": "EdTech",
        "blurb": "EdTech software vendors: online learning platforms, LMS and courseware, assessment and proctoring, adaptive learning, learner engagement, and subscription billing and outcomes analytics.",
        "medallion": medallion(
            "Raw learning and billing events",
            "Clickstream and lesson events from the learning platform, LMS activity and grade-passback callbacks over LTI, rostering files from Clever and OneRoster, Stripe and Chargebee billing records and proctoring and assessment logs, landed exactly as received so an engagement spike or a disputed grade can always be replayed as it stood.",
            "Conformed learner, course, tenant",
            "Learners, courses, content items and tenants resolved into single conformed entities across the LMS, telemetry, billing and assessment estates, with anonymous device ids stitched to known learners and multi-tenant institution data isolated to one governed hierarchy.",
            "Outcomes, engagement, retention, NRR",
            "Contracted products the product, learning-science and revenue teams run on: engagement and activation funnels, mastery and learning-outcome attainment, at-risk and retention scores by cohort, subscription NRR and churn, and metering accuracy for usage-based billing.",
        ),
        "rails": {
            "src": [
                {
                    "box": "CRM & Subscriptions",
                    "ic": "crm",
                    "tiles": [
                        tile(
                            "Salesforce Sales Cloud",
                            "crm",
                            "The system of record for institution and district accounts, opportunities and the pipeline, and the source of the customer hierarchy every revenue metric rolls up to.",
                            "salesforce",
                        ),
                        tile(
                            "HubSpot CRM",
                            "custlake",
                            "Contacts, deals and marketing engagement for the self-serve and teacher-led motion, joined to product signups.",
                            "hubspot",
                        ),
                        tile(
                            "Chargebee Billing",
                            "market",
                            "Subscription lifecycle, dunning and revenue operations for the self-serve and B2C billing motion, the source of MRR and churn.",
                            "chargebee",
                        ),
                        tile(
                            "Stripe Billing",
                            "market",
                            "Subscriptions, invoices, seat and usage records and payment events, reconciled against enrolment and consumption.",
                            "stripe",
                        ),
                    ],
                },
                {
                    "box": "LMS & Rostering",
                    "ic": "notebook",
                    "tiles": [
                        tile(
                            "Instructure Canvas",
                            "notebook",
                            "Course shells, assignment activity and gradebook events from the LMS the product launches into over LTI, the source of in-course engagement.",
                            "instructure",
                        ),
                        tile(
                            "Moodle LMS",
                            "notebook",
                            "Open-source LMS activity, submission and completion logs for the institutions and markets running on the Moodle estate.",
                            "moodle",
                        ),
                        tile(
                            "Clever Rostering",
                            "people",
                            "Single sign-on and roster sync for K-12: students, sections and teachers provisioned from the district into the product.",
                            "clever",
                        ),
                        tile(
                            "OneRoster & LTI",
                            "api",
                            "The 1EdTech interoperability standards carrying rostering, launch and grade passback between the product and the customer's LMS and SIS.",
                            "oneroster",
                        ),
                    ],
                },
                {
                    "box": "Learning Telemetry",
                    "ic": "stream",
                    "tiles": [
                        tile(
                            "Segment CDP",
                            "custlake",
                            "The customer data platform routing product, web and lesson events into one schema of identified and anonymous learner activity.",
                            "segment",
                        ),
                        tile(
                            "Amplitude Analytics",
                            "chart",
                            "Product analytics events, funnels and feature adoption, the source of activation and engagement measurement.",
                            "amplitude",
                        ),
                        tile(
                            "Snowplow Behavioral",
                            "stream",
                            "First-party behavioural event pipeline with a governed schema, the raw clickstream behind engagement and drop-off models.",
                            "snowplow",
                        ),
                        tile(
                            "xAPI Record Store",
                            "db",
                            "The Experience API learning record store capturing granular lesson, attempt and mastery statements across content and tools.",
                            "xapi",
                        ),
                    ],
                },
                {
                    "box": "Assessment & Proctoring",
                    "ic": "gavel",
                    "tiles": [
                        tile(
                            "Proctorio",
                            "watch",
                            "Remote proctoring session events, gaze and behaviour signals and integrity flags captured during online exams.",
                            "proctorio",
                        ),
                        tile(
                            "ExamSoft Assessment",
                            "gavel",
                            "Secure exam delivery, item-level response data and category analytics for high-stakes computer-based testing.",
                            "examsoft",
                        ),
                        tile(
                            "Respondus LockDown",
                            "key",
                            "Lockdown browser and monitoring events restricting and recording the exam environment for online assessment.",
                            "respondus",
                        ),
                        tile(
                            "QTI Question Banks",
                            "sheet",
                            "Question and Test Interoperability item banks and rubrics, the interchange format for assessment content and scoring keys.",
                            "qti",
                        ),
                    ],
                },
                {
                    "box": "Content & Support",
                    "ic": "docs",
                    "tiles": [
                        tile(
                            "SCORM Cloud",
                            "docs",
                            "SCORM and xAPI content packaging, launch and completion tracking for the courseware the platform delivers.",
                            "scorm",
                        ),
                        tile(
                            "Contentful CMS",
                            "docs",
                            "Headless content management for lessons, media and metadata, the source of the courseware catalogue.",
                            "contentful",
                        ),
                        tile(
                            "Zendesk Support",
                            "chat",
                            "Learner and educator support tickets, CSAT and macros, a leading churn signal and the corpus behind support deflection.",
                            "zendesk",
                        ),
                        tile(
                            "Intercom",
                            "dial",
                            "In-product messaging, conversations and resolution data across the onboarding and support journey.",
                            "intercom",
                        ),
                    ],
                },
                fed_group(
                    "Warehouse Marts",
                    "Existing cloud data warehouse finance and analytics marts left where they are and queried in place under Unity Catalog, which avoids a second copy of the reported numbers.",
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "Kafka Event Streams",
                        "eventbus",
                        "Learning-event topics on Kafka or managed streaming carrying lesson-start, submission and grade events, parsed on arrival and landed as structured events.",
                        "kafka",
                    ),
                    tile(
                        "LTI & Webhooks",
                        "api",
                        "LTI launch, deep-linking and grade-passback callbacks plus Stripe and Zendesk webhooks delivering near-real-time enrolment, billing and ticket events. Managed ELT connectors and existing streaming topics land here too, drawn generically on the reference board.",
                    ),
                    tile(
                        "Clickstream Firehose",
                        "stream",
                        "High-volume web and mobile app clickstream from the learning experience, joined to enrolments for engagement and drop-off analysis.",
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Exec & Product",
                        "Genie One",
                        "The CEO on growth, net revenue retention and the efficacy story that wins renewals; the Chief Product Officer on activation, engagement and the roadmap that moves learning outcomes; the Chief Learning Officer on whether the product actually teaches.",
                        [
                            ["Genie One", "Ask what this month's retention was by cohort, or which features move outcomes, without booking analyst time."],
                            ["AI/BI", "Growth, engagement and learning-outcome metrics on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the glossary, so \"active learner\" and \"mastery\" mean one thing across the company."],
                        ],
                        sub=[
                            ["CEO", "growth, net revenue retention and the efficacy story behind renewals."],
                            ["Chief Product Officer", "activation, engagement and the roadmap that moves outcomes."],
                            ["Chief Learning Officer", "whether the product actually teaches, measured on outcomes."],
                        ],
                        ucs=["Learner Engagement", "At-Risk & Retention", "Subscription Churn", "Adaptive Learning"],
                    ),
                    biz(
                        "Learning Science",
                        "Model Serving",
                        "Learning scientists and psychometricians validating that content teaches, curriculum designers sequencing adaptive paths, and efficacy researchers proving outcome gains against a control cohort.",
                        [
                            ["Adaptive Path Engine", "The next best lesson sequenced per learner from live mastery estimates."],
                            ["Model Serving", "Knowledge-tracing and item-response models scored inside the learning path."],
                            ["MLflow", "Every efficacy and knowledge-tracing run tracked for audit and reproduction."],
                        ],
                        sub=[
                            ["Learning scientists", "knowledge tracing, item response and mastery modelling."],
                            ["Curriculum designers", "adaptive sequencing and content-to-standard alignment."],
                            ["Efficacy researchers", "outcome gains proven against a control cohort."],
                        ],
                        ucs=["Adaptive Learning", "Content Efficacy", "Automated Scoring", "GenAI Tutor"],
                    ),
                    biz(
                        "Growth & Engage",
                        "Lakehouse//RT",
                        "Growth teams on signup-to-activation and free-to-paid conversion, lifecycle marketing on onboarding and reactivation nudges, and engagement analysts on the clickstream signals that predict who quietly disengages.",
                        [
                            ["Learner 360", "Engagement, streaks and risk on one profile per learner."],
                            ["AI/BI", "Activation and engagement funnels on governed event data with one metric definition."],
                            ["Lakehouse//RT", "Live learner state at the latency an onboarding flow moves at."],
                        ],
                        sub=[
                            ["Growth", "signup-to-activation and free-to-paid conversion loops."],
                            ["Lifecycle marketing", "onboarding, reactivation and in-app nudges."],
                            ["Engagement analysts", "the clickstream signals behind quiet disengagement."],
                        ],
                        ucs=["Learner Engagement", "GenAI Tutor", "Support Deflection"],
                    ),
                    biz(
                        "Finance & RevOps",
                        "AI/BI",
                        "The CFO on gross margin, cash and the efficiency of growth; RevOps on seat and usage-based revenue, metering accuracy and billed-to-consumed; the renewals desk on the accounts quietly heading for non-renewal.",
                        [
                            ["AI/BI", "MRR, the ARR bridge and net revenue retention on certified Metric Views."],
                            ["Model Serving", "Churn and expansion propensity scored inside the renewals path."],
                            ["Genie One", "Ask which accounts are under-billed this month without a finance pull."],
                        ],
                        sub=[
                            ["CFO", "gross margin, cash and the efficiency of growth."],
                            ["RevOps & billing", "seat and usage revenue, metering accuracy and billed-to-consumed."],
                            ["Renewals desk", "the accounts quietly heading for non-renewal."],
                        ],
                        ucs=["Subscription Churn", "Usage-Based Billing", "At-Risk & Retention"],
                    ),
                    biz(
                        "Trust & Safety",
                        "Unity Catalog",
                        "Assessment-integrity teams on exam anomalies and proctoring signals, the trust and safety desk on student-safety alerts in K-12 environments, and the privacy office on FERPA, COPPA and GDPR obligations across minors' data.",
                        [
                            ["Integrity Monitor", "Exam-session anomalies and proctoring flags ranked for human review."],
                            ["Unity Catalog", "Row and column governance so minors' data is reachable only by who may see it."],
                            ["Model Serving", "Anomaly and safety-signal models scored on assessment and clickstream events."],
                        ],
                        sub=[
                            ["Assessment integrity", "exam anomalies and proctoring-signal review."],
                            ["Trust & safety", "student-safety alerts in K-12 environments."],
                            ["Privacy office", "FERPA, COPPA and GDPR across minors' data."],
                        ],
                        ucs=["Exam Integrity", "Automated Scoring", "At-Risk & Retention"],
                    ),
                ],
                [
                    biz(
                        "Data Engineers",
                        "Lakeflow",
                        "Land the LMS, rostering, clickstream, billing and assessment feeds with Fivetran, Airbyte and Kafka; run dbt and Airflow on the Bronze to Silver path; own the pager when the engagement and billing tables stall.",
                        [
                            ["Lakeflow Connect", "Managed connectors for Salesforce, Stripe and the SaaS learning sources."],
                            ["Lakeflow Designer", "Declarative pipelines with expectations on clickstream and grade feeds."],
                            ["Lakewatch", "Freshness on the engagement and outcome tables the business reads every morning."],
                        ],
                        sub=[
                            ["Ingestion engineers", "LMS, rostering and billing feeds into Bronze."],
                            ["Streaming engineers", "clickstream and xAPI events into Lakehouse//RT."],
                            ["Platform & governance", "Unity Catalog permissions and the pipeline SLAs."],
                        ],
                        ucs=["Learner Engagement", "Adaptive Learning", "Usage-Based Billing"],
                    ),
                    biz(
                        "ML Scientists",
                        "MLflow",
                        "Knowledge-tracing, item-response, churn and content-recommendation models built in Python with PyTorch and scikit-learn, and whether they still hold once the curriculum and the cohort change.",
                        [
                            ["Feature Store", "Learner and content features read identically in training and serving."],
                            ["MLflow", "Every knowledge-tracing and churn run tracked for audit and reproduction."],
                            ["Model Serving", "Mastery, recommendation and churn models scored in the learning and CRM path."],
                        ],
                        sub=[
                            ["Learning modelers", "knowledge tracing, item response and mastery estimation."],
                            ["Applied GenAI", "tutoring and grading agents on governed content."],
                            ["MLOps", "tracking and serving models in the learning path."],
                        ],
                        ucs=["Adaptive Learning", "Automated Scoring", "GenAI Tutor"],
                    ),
                    biz(
                        "App Developers",
                        "Apps",
                        "Ship the learner, tutor, adaptive and integrity applications the product runs in, hosted next to governed data with LTI launch into the customer's LMS.",
                        [
                            ["Apps", "Learner and educator screens with no separate web tier to run or secure."],
                            ["Lakebase", "Serverless Postgres for learner state, streaks and governed writes."],
                            ["Agent Bricks", "Tutor and grading agents that act against governed tools."],
                        ],
                        sub=[
                            ["Learning app developers", "learner, educator and tutor screens."],
                            ["Backend & Lakebase", "learner state and progress with governed writes."],
                            ["Agent developers", "tutoring and grading agents over MCP."],
                        ],
                        ucs=["GenAI Tutor", "Exam Integrity"],
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
                                "Executive and board dashboards against serverless SQL warehouses, with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for Unity Catalog-governed answers from the lakehouse, in the channel product and learning teams already work in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Analyst notebooks, VS Code and JetBrains against governed learning and revenue data with Genie Code.",
                            ),
                        ],
                    },
                    {
                        "box": "Learner Activation",
                        "ic": "zfunnel",
                        "tiles": [
                            tile(
                                "Reverse ETL to CDP",
                                "reverse",
                                "Engagement scores and lifecycle segments synced back to Segment and the CRM for in-app and email activation.",
                                "segment",
                            ),
                            tile(
                                "In-App Nudges",
                                "dial",
                                "Onboarding and re-engagement nudges served into the learning app from governed engagement and risk scores.",
                            ),
                            tile(
                                "Email & Push",
                                "market",
                                "Lifecycle and reactivation campaigns triggered from governed cohorts in Braze and the marketing stack.",
                                "braze",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "LTI Grade Passback",
                                "reverse",
                                "Grades and mastery written back into the customer's LMS gradebook over LTI so the score reaches the course the learner works in.",
                                "oneroster",
                            ),
                            tile(
                                "CRM Health Writeback",
                                "crm",
                                "Account health and churn risk written back to Salesforce so success teams act in the system they live in.",
                                "salesforce",
                            ),
                            tile(
                                "Adaptive Content Push",
                                "product",
                                "Next-best content decisions pushed into the learning platform so the path adapts in the flow.",
                            ),
                        ],
                    },
                    {
                        "box": "Partners & Sharing",
                        "ic": "share",
                        "tiles": [
                            tile(
                                "Institution Products",
                                "product",
                                "Engagement and outcome products published in Unity Catalog Domains and shared with customer institutions over Open Sharing.",
                            ),
                            tile(
                                "Publisher Sharing",
                                "share",
                                "Content usage and efficacy shared live with courseware publishers over Delta Sharing rather than quarterly file exchange.",
                            ),
                            tile(
                                "Embedded Analytics",
                                "aibi",
                                "Educator- and admin-facing dashboards embedded in the product against governed tables with per-tenant row isolation.",
                            ),
                        ],
                    },
                    {
                        "box": "Privacy & Compliance",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "FERPA & COPPA Evidence",
                                "gavel",
                                "Access and consent evidence for FERPA and COPPA produced from the same governed tables the product runs on.",
                            ),
                            tile(
                                "Privacy & DSAR",
                                "zshield",
                                "GDPR and CCPA subject access and deletion for learners and guardians fulfilled from one governed learner record.",
                            ),
                        ],
                    },
                ]
            ),
        },
        "top": top_band(
            [
                app(
                    "Learner 360",
                    "Engagement & risk",
                    "custlake",
                    "One profile per learner across every product and LMS: streaks, mastery, engagement and disengagement risk composed from clickstream, assessment and billing signals, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Adaptive Path Engine",
                    "Personalized learning",
                    "ztarget",
                    "The next best lesson sequenced per learner from live mastery estimates, so each learner sees content pitched at the edge of what they can already do rather than a fixed syllabus.",
                ),
                app(
                    "Outcomes Studio",
                    "Efficacy analytics",
                    "chart",
                    "Where learning scientists and product prove which content, sequence and intervention actually move outcomes, on the same certified metrics the executive team reads.",
                ),
                app(
                    "Integrity Monitor",
                    "Exam integrity",
                    "watch",
                    "Exam-session anomalies and proctoring signals ranked for human review, so integrity cases surface from the data instead of a spot check after grades post.",
                ),
            ],
            [
                uc(
                    "Learner Engagement",
                    "Engagement",
                    "stream",
                    "Engagement, streaks and quiet disengagement measured on one governed event stream, so product, growth and learning-science read the same activity instead of three tools' versions of it.",
                    problem="Learning events sit in a CDP and two analytics tools that each define \"active\" differently, so no two teams agree on engagement or spot the learner drifting toward churn until they are gone.",
                    who="Growth & Engage",
                    how="Segment and Snowplow clickstream land through Lakeflow and are conformed to certified Metric Views; engagement and risk are composed per learner in Learner 360 on Lakehouse//RT.",
                    comps=["Segment CDP", "Snowplow Behavioral", "Lakehouse//RT", "Learner 360", "AI/BI"],
                    stories=[
                        ["HOMER lifts engagement and cuts churn with Databricks", "https://www.databricks.com/customers/homer"],
                        ["GoGuardian improves learning outcomes with Databricks", "https://www.databricks.com/customers/goguardian"],
                    ],
                ),
                uc(
                    "Adaptive Learning",
                    "Personalization",
                    "ztarget",
                    "The next best lesson chosen per learner from live mastery estimates, so each learner works at the edge of what they can already do rather than a fixed syllabus.",
                    problem="A one-size syllabus bores the learner who is ahead and loses the one who is behind, and the mastery signal needed to adapt is scattered across LMS activity and assessment attempts.",
                    who="Learning Science",
                    how="xAPI and assessment events feed knowledge-tracing models tracked in MLflow and scored in Model Serving; the Adaptive Path Engine sequences the next item from live mastery.",
                    comps=["xAPI Record Store", "Model Serving", "Feature Store", "Adaptive Path Engine", "MLflow"],
                    stories=[
                        ["McGraw Hill drives adaptive learning on Databricks Delta", "https://www.databricks.com/blog/leveraging-delta-across-teams-mcgraw-hill"],
                        ["Democratizing big data and ML at McGraw-Hill", "https://www.databricks.com/blog/2017/10/18/using-databricks-democratize-big-data-machine-learning-mcgraw-hill-education.html"],
                    ],
                ),
                uc(
                    "Content Efficacy",
                    "Efficacy",
                    "chart",
                    "Proving which content, sequence and intervention actually move learning outcomes, measured against a control rather than asserted from a content calendar.",
                    problem="Content is shipped on intuition and refreshed on a calendar, while the evidence of what actually teaches sits unjoined across engagement, assessment and outcome data.",
                    who="Learning Science",
                    how="Engagement and outcome events are conformed to certified Metric Views; efficacy is measured in AI/BI from the Outcomes Studio on one definition of mastery under Unity Catalog.",
                    comps=["Amplitude Analytics", "AI/BI", "Outcomes Studio", "Unity Catalog", "xAPI Record Store"],
                    stories=[
                        ["Democratizing big data and ML at McGraw-Hill", "https://www.databricks.com/blog/2017/10/18/using-databricks-democratize-big-data-machine-learning-mcgraw-hill-education.html"],
                        ["Data analytics and AI in education", "https://www.databricks.com/solutions/industries/education"],
                    ],
                ),
                uc(
                    "At-Risk & Retention",
                    "Retention",
                    "people",
                    "Predicting the learner who will disengage or fail from LMS activity, assessment and support signals, so the intervention happens before the term is lost, not in the post-mortem.",
                    problem="At-risk learners are identified after they fail or churn, when the leading signals of struggle were visible weeks earlier across activity, grades and support tickets.",
                    who="Exec & Product",
                    how="Activity, assessment and support features feed risk models tracked in MLflow and scored in Model Serving; risk and its drivers surface per learner in Learner 360 for the owning team.",
                    comps=["Instructure Canvas", "Model Serving", "Feature Store", "Learner 360", "MLflow"],
                    stories=[
                        ["GoGuardian improves learning outcomes with Databricks", "https://www.databricks.com/customers/goguardian"],
                        ["Data analytics and AI in education", "https://www.databricks.com/solutions/industries/education"],
                    ],
                ),
                uc(
                    "Automated Scoring",
                    "Assessment",
                    "gauge",
                    "Open-response and behavioural assessments scored by governed models with human oversight, turning a multi-day human backlog into near-instant, consistent feedback.",
                    problem="Open-response and simulation scoring is a slow, expensive human bottleneck, and inconsistent scoring undermines both the learner's feedback and the assessment's validity.",
                    who="Trust & Safety",
                    how="Item banks and rubrics are governed in Unity Catalog; scoring runs through AI Functions and fine-tuned models in Model Serving with an Agent Bricks review loop, tracked in MLflow.",
                    comps=["QTI Question Banks", "AI Functions", "Model Serving", "Agent Bricks", "MLflow"],
                    stories=[
                        ["DDI automates behavioral simulation scoring with GenAI", "https://www.databricks.com/customers/ddi"],
                    ],
                ),
                uc(
                    "Exam Integrity",
                    "Integrity",
                    "gavel",
                    "Exam-session anomalies and proctoring signals ranked for human review, so integrity cases surface from the data rather than a spot check after grades post.",
                    problem="Proctoring generates far more signal than reviewers can watch, so real cheating hides in the volume while honest learners are flagged by blunt rules.",
                    who="Trust & Safety",
                    how="Proctoring, keystroke and response-timing events stream into Lakehouse//RT; anomaly models in Model Serving rank sessions for review in the Integrity Monitor, tracked in MLflow.",
                    comps=["Proctorio", "Model Serving", "Lakehouse//RT", "Integrity Monitor", "MLflow"],
                ),
                uc(
                    "GenAI Tutor",
                    "Tutoring",
                    "chat",
                    "A governed AI tutor that explains, hints and quizzes from the product's own content and the learner's mastery state, at a scale one-to-one human tutoring never reaches.",
                    problem="One-to-one tutoring is the strongest lever on outcomes and the least scalable, and an ungoverned chatbot risks hallucinating answers or leaking a minor's data.",
                    who="Learning Science",
                    how="Product content is governed in Unity Catalog and retrieved by an Agent Bricks tutor using AI Functions and Model Serving, grounded in the learner's mastery from the Adaptive Path Engine.",
                    comps=["Agent Bricks", "AI Functions", "Model Serving", "Adaptive Path Engine", "Unity Catalog"],
                    stories=[
                        ["AI applications: tools, use cases and platforms", "https://www.databricks.com/blog/ai-applications"],
                        ["Data analytics and AI in education", "https://www.databricks.com/solutions/industries/education"],
                    ],
                ),
                uc(
                    "Subscription Churn",
                    "Retention",
                    "market",
                    "Predicting subscription churn and expansion from engagement, outcome and billing signals so the save happens before the renewal date, not at it.",
                    problem="Churn shows up in the renewal number when it is too late to act, while the leading signals sit unjoined across product engagement, learning outcomes and billing.",
                    who="Finance & RevOps",
                    how="Engagement, outcome and billing features feed churn and expansion models tracked in MLflow and scored in Model Serving; risk is activated through CustomerLake and read in AI/BI.",
                    comps=["Chargebee Billing", "Model Serving", "Feature Store", "CustomerLake", "AI/BI"],
                    stories=[
                        ["HOMER lowers churn and lifts conversion with Databricks", "https://www.databricks.com/customers/homer"],
                    ],
                ),
                uc(
                    "Usage-Based Billing",
                    "Monetization",
                    "gauge",
                    "Seat and usage consumption rated and reconciled to invoices before the close, so the vendor bills exactly what institutions and learners actually used.",
                    problem="Seat- and usage-based pricing leaks revenue when metering, rating and the invoice disagree, and the reconciliation of consumed to billed only surfaces after the period closes.",
                    who="Finance & RevOps",
                    how="Raw seat and usage events are conformed in the lakehouse, rated against the plan and reconciled to Stripe and Chargebee invoices, with margin and revenue-at-risk read in AI/BI.",
                    comps=["Stripe Billing", "Chargebee Billing", "AI/BI", "Lakeflow", "Unity Catalog"],
                ),
                uc(
                    "Support Deflection",
                    "Support",
                    "chat",
                    "A governed assistant that resolves common learner and educator questions from the product docs and ticket history, deflecting volume before it reaches an agent.",
                    problem="Support volume scales with the learner base, and the answers already exist in docs and past tickets, but agents re-solve the same questions by hand every day.",
                    who="Growth & Engage",
                    how="Zendesk and Intercom history and product docs are governed in Unity Catalog and served to an Agent Bricks assistant with AI Functions and Model Serving, deflecting and summarising tickets.",
                    comps=["Zendesk Support", "Intercom", "Agent Bricks", "AI Functions", "Model Serving"],
                ),
            ],
        ),
        "sources": {
            "salesforce": {"t": "Salesforce Sales Cloud", "u": "https://www.salesforce.com/sales/"},
            "hubspot": {"t": "HubSpot CRM", "u": "https://www.hubspot.com/products/crm"},
            "chargebee": {"t": "Chargebee", "u": "https://www.chargebee.com/"},
            "stripe": {"t": "Stripe Billing", "u": "https://stripe.com/billing"},
            "instructure": {"t": "Instructure Canvas LMS", "u": "https://www.instructure.com/canvas"},
            "moodle": {"t": "Moodle LMS", "u": "https://moodle.org/"},
            "clever": {"t": "Clever rostering and SSO", "u": "https://www.clever.com/"},
            "oneroster": {"t": "1EdTech OneRoster & LTI", "u": "https://www.1edtech.org/standards/oneroster"},
            "segment": {"t": "Twilio Segment CDP", "u": "https://segment.com/"},
            "amplitude": {"t": "Amplitude product analytics", "u": "https://amplitude.com/"},
            "snowplow": {"t": "Snowplow behavioral data", "u": "https://snowplow.io/"},
            "xapi": {"t": "Experience API (xAPI)", "u": "https://xapi.com/"},
            "proctorio": {"t": "Proctorio remote proctoring", "u": "https://proctorio.com/"},
            "examsoft": {"t": "ExamSoft assessment", "u": "https://examsoft.com/"},
            "respondus": {"t": "Respondus LockDown Browser", "u": "https://web.respondus.com/"},
            "qti": {"t": "1EdTech QTI standard", "u": "https://www.1edtech.org/standards/qti"},
            "scorm": {"t": "SCORM Cloud (Rustici)", "u": "https://scorm.com/"},
            "contentful": {"t": "Contentful headless CMS", "u": "https://www.contentful.com/"},
            "zendesk": {"t": "Zendesk", "u": "https://www.zendesk.com/"},
            "intercom": {"t": "Intercom", "u": "https://www.intercom.com/"},
            "kafka": {"t": "Apache Kafka", "u": "https://kafka.apache.org/"},
            "braze": {"t": "Braze customer engagement", "u": "https://www.braze.com/"},
        },
    }
}
