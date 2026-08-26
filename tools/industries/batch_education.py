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


INDUSTRIES_BATCH_EDUCATION = {
    'education': {
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
}
