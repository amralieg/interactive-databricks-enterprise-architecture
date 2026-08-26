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


INDUSTRIES_BATCH_STAFFING_HR = {
    'staffing_hr': {
        "label": "Staffing & HR",
        "blurb": "Staffing firms and HR service providers: candidate sourcing, placement lifecycle, vendor management systems, payroll and compliance, and workforce analytics across clients and geographies.",
        "medallion": medallion(
            "Raw HR and placement feeds",
            "ATS applications, VMS requisitions, timecards, payroll runs and compliance documents, landed exactly as received so a placement margin or a credential can always be replayed.",
            "Conformed worker, req, client",
            "Candidates, requisitions, placements and time entries resolved into single conformed entities across ATS, VMS and payroll, with assignment dates stitched to one engagement.",
            "Fill rate, margin, compliance",
            "Contracted products sales and finance run on: time-to-fill, gross margin by client, credential expiry risk, overtime and bill-pay spread by skill.",
        ),
        "rails": {
            "src": [
                {"box": "ATS & Recruiting", "ic": "erp", "tiles": [
                    tile("Bullhorn ATS/CRM", "erp", "Candidate records, submissions, interviews and placement history for staffing firms.", "bullhorn"),
                    tile("Workday Recruiting", "people", "Requisitions, offers and onboarding for corporate HR and RPO programs.", "workday-rec"),
                    tile("Greenhouse", "sheet", "Structured hiring pipelines, scorecards and DEI reporting for enterprise clients.", "greenhouse"),
                ]},
                {"box": "VMS & Contingent", "ic": "market", "tiles": [
                    tile("Beeline VMS", "market", "Client requisitions, rate cards, approvals and supplier scorecards.", "beeline"),
                    tile("SAP Fieldglass", "partner", "Contingent workforce procurement, statements of work and compliance tracking.", "fieldglass"),
                    tile("Magnit VMS", "api", "MSP-managed programs: spend, tenure limits and conversion tracking.", "magnit"),
                ]},
                {"box": "Payroll & Time", "ic": "chart", "tiles": [
                    tile("ADP Workforce Now", "erp", "Payroll, tax and benefits for placed workers across jurisdictions.", "adp"),
                    tile("UKG Pro WFM", "people", "Time and attendance, scheduling and accruals for hourly placements.", "ukg-pro"),
                    tile("Deel Global Payroll", "globe", "Contractor payments and compliance in international staffing programs.", "deel"),
                ]},
                {"box": "Credentialing", "ic": "gavel", "tiles": [
                    tile("Symplr Credentialing", "gavel", "Licence verification, expirations and privileging for healthcare staffing.", "symplr"),
                    tile("Checkr Background", "partner", "Criminal, employment and education checks with adverse action workflow.", "checkr"),
                    tile("Everify I-9", "gavel", "Employment eligibility verification and audit trail for US placements.", "everify"),
                ]},
                {"box": "Learning & Skills", "ic": "product", "tiles": [
                    tile("Cornerstone LMS", "product", "Client-mandated training completion and skills certifications.", "cornerstone"),
                    tile("LinkedIn Talent Insights", "chart", "Labour market supply, demand and skill adjacency by geography.", "linkedin-ti"),
                ]},
                fed_group("Client HRIS Marts", "Client employee and cost centre marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("Indeed Job Feed", "api", "Job postings and application funnel metrics ingested for sourcing analytics.", "indeed"),
                tile("Lightcast Labour Market", "chart", "Occupation demand, wage benchmarks and skills taxonomy updates.", "lightcast"),
                tile("State Licence Boards", "gavel", "Professional licence status files consumed for credential monitoring.", "symplr"),
            ]),
            "ppl": ppl2([
                biz("CEO & Growth Office", "Genie One", "The CEO on gross margin and client concentration; the COO on fill rate, redeployment and the compliance exposure sitting in open placements.",
                    [["Genie One", "Ask what last quarter's margin by client was without analyst delay."], ["AI/BI", "Fill rate and spread on certified Metric Views."], ["Unity Catalog", "One placement definition across ATS and payroll."]]),
                biz("Recruiting & Sales", "Model Serving", "Recruiters and account managers on req pipelines, submittal quality and rate negotiations, defending time-to-fill and interview velocity.",
                    [["Recruiter Workbench", "Open reqs, submittal quality and interview velocity."], ["Model Serving", "Candidate match scores in the submission path."]]),
                biz("Workforce Operations", "Lakehouse//RT", "Schedulers on shift coverage, overtime creep and credential gaps that would block a worker from starting the client assignment on time.",
                    [["Coverage Console", "Open shifts and credential expiry on one screen."], ["Lakehouse//RT", "Timecard and credential state at shift latency."]]),
                biz("Payroll & Finance", "AI/BI", "Payroll and billing teams on bill-pay spread, accrual accuracy and client invoicing, chasing margin leakage that hides in missed approvals.",
                    [["AI/BI", "Margin and leakage on certified views."], ["Genie One", "Ask which clients are below target spread this month."]]),
                biz("Compliance & Risk", "Lakeflow", "Compliance officers on credential expirations, tenure limits and audit response, keeping every placement defensible under client and law.",
                    [["Compliance Dashboard", "Credential and I-9 status by placement."], ["Lakeflow", "ATS, VMS and payroll feeds conformed for audit."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land ATS submittals, VMS requisitions, timecards and payroll runs; own Bronze to Silver and the pager when a fill-rate or margin table breaks.",
                    [["Lakeflow Connect", "Managed connectors for ATS, VMS and payroll sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on placement and timecard feeds."], ["Lakewatch", "Freshness on the margin tables finance reads each morning."]]),
                biz("Data Scientists", "MLflow", "Candidate-match, time-to-fill, attrition and rate-benchmark models, and whether they still hold as skills demand and client mix shift.",
                    [["Feature Store", "Candidate and req features read identically in training and serving."], ["MLflow", "Every match and attrition experiment tracked for audit."], ["Model Serving", "Match and attrition models scored in the submission path."]]),
                biz("App Developers", "Apps", "Ship the Recruiter Workbench, Coverage Console and Margin Analyzer apps recruiting and finance work in, next to governed placement data.",
                    [["Apps", "Recruiting screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for shift and credential state writes."], ["Agent Bricks", "Agents that draft submittals against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Client and recruiter dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for fill rate and margin questions in the sales channel."),
                    tile("Notebooks & IDEs", "notebook", "Workforce analytics notebooks against governed placement data."),
                ]},
                {"box": "Client & Supplier", "ic": "partner", "tiles": [
                    tile("VMS Requisition API", "api", "Submittals and rate confirmations exchanged with client VMS platforms.", "beeline"),
                    tile("Client Billing Portal", "share", "Invoice backup and timesheet detail shared over Delta Sharing."),
                    tile("Supplier Scorecards", "globe", "Fill rate and quality metrics returned to MSP programs.", "magnit"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("ATS Status Updates", "erp", "Interview and offer status written back to Bullhorn.", "bullhorn"),
                    tile("Shift Offers", "apps", "Open shift notifications pushed to worker mobile apps."),
                    tile("Credential Renewals", "gavel", "Renewal tasks dispatched before expiry blocks placement.", "symplr"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("EEO & OFCCP Reports", "gavel", "Hiring diversity metrics filed from governed ATS data.", "greenhouse"),
                    tile("Pay Equity Analysis", "share", "Compensation parity evidence for client audits."),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Workforce analytics products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Clients reading live fill and spend metrics via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Recruiter Workbench", "Req pipeline", "people", "Open requisitions, submittal quality and interview velocity for each recruiter pod."),
             app("Coverage Console", "Shift staffing", "gauge", "Open shifts, credential gaps and overtime risk before the client shift starts."),
             app("Margin Analyzer", "Bill-pay spread", "market", "Gross margin and leakage by client, skill and geography on governed payroll data."),
             app("Compliance Dashboard", "Credential status", "gavel", "Licence, background and I-9 status by placement with renewal workflows.")],
            [uc("Candidate Matching", "Recruiting", "people", "Skills and availability scored against open reqs before submittal."),
             uc("Time-to-Fill", "Operations", "chart", "Req ageing decomposed by client approval, sourcing and interview stages."),
             uc("Credential Monitoring", "Compliance", "gavel", "Expiring licences flagged before they block placement or shift."),
             uc("Overtime Control", "Workforce", "stream", "Overtime hours predicted and capped against client rules."),
             uc("Payroll Leakage", "Finance", "erp", "Bill-pay mismatches and missed timecard approvals surfaced before close."),
             uc("Client Profitability", "Finance", "market", "Gross margin by client account including rebates and chargebacks."),
             uc("Attrition Prediction", "Retention", "custlake", "Assignment completion and extension likelihood scored per worker."),
             uc("Rate Benchmarking", "Pricing", "chart", "Bill rates compared to market benchmarks by skill and metro."),
             uc("DEI Hiring Analytics", "Compliance", "gavel", "Pipeline diversity metrics for client and regulatory reporting."),
             uc("Skills Taxonomy", "Talent", "product", "Skills inferred from placements and training for future req matching.")],
        ),
        "sources": {
            "bullhorn": {"t": "Bullhorn ATS/CRM", "u": "https://www.bullhorn.com/"},
            "workday-rec": {"t": "Workday Recruiting", "u": "https://www.workday.com/en-us/products/talent-management/talent-acquisition.html"},
            "greenhouse": {"t": "Greenhouse", "u": "https://www.greenhouse.com/"},
            "beeline": {"t": "Beeline VMS", "u": "https://www.beeline.com/"},
            "fieldglass": {"t": "SAP Fieldglass", "u": "https://www.sap.com/products/spend-management/fieldglass-vms.html"},
            "magnit": {"t": "Magnit VMS", "u": "https://magnitglobal.com/"},
            "adp": {"t": "ADP Workforce Now", "u": "https://www.adp.com/what-we-offer/products/adp-workforce-now.aspx"},
            "ukg-pro": {"t": "UKG Pro", "u": "https://www.ukg.com/solutions/human-capital-management"},
            "deel": {"t": "Deel global payroll", "u": "https://www.deel.com/"},
            "symplr": {"t": "Symplr credentialing", "u": "https://www.symplr.com/"},
            "checkr": {"t": "Checkr", "u": "https://checkr.com/"},
            "everify": {"t": "E-Verify", "u": "https://www.e-verify.gov/"},
            "cornerstone": {"t": "Cornerstone LMS", "u": "https://www.cornerstoneondemand.com/"},
            "linkedin-ti": {"t": "LinkedIn Talent Insights", "u": "https://business.linkedin.com/talent-solutions/talent-insights"},
            "indeed": {"t": "Indeed", "u": "https://www.indeed.com/hire"},
            "lightcast": {"t": "Lightcast labour market data", "u": "https://lightcast.io/"},
        },
    },
}
