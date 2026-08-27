import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl_rail2(business_tiles, tech_tiles):
    """People rail with per-industry Technical roles instead of shared TECH_PPL."""
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles},
    ]


INDUSTRIES_BATCH_NGO = {
    'ngo': {
        "label": "NGO & Non-Profit",
        "blurb": "Donor stewardship, grant compliance, program delivery and field operations for humanitarian, development and advocacy organisations operating across borders.",
        "medallion": medallion(
            "Raw donor and field",
            "CRM gifts, grant ledger entries, mobile survey responses, logistics waybills and banking settlements, landed exactly as received so a donation or a beneficiary visit can always be replayed as it stood.",
            "Conformed donor, grant",
            "Donors, households, grants, projects and beneficiaries resolved into single conformed entities across CRM, ERP and field systems, with restricted-fund balances reconciled and program outcomes stitched to one intervention record.",
            "Reach, cost, compliance",
            "Contracted products leadership and boards run on: funds raised and donor retention, cost per outcome by program, grant spend against budget and compliance exception rates.",
        ),
        "rails": {
            "src": [
                {"box": "CRM & Fundraising", "ic": "custlake", "tiles": [
                        tile("Salesforce Nonprofit Cloud", "custlake", "Donor profiles, campaigns, pledges and recurring gifts from the CRM fundraisers work in.", "sf-nonprofit"),
                        tile("Blackbaud Raiser's Edge", "people", "Major-gift pipelines, events and acknowledgment history for development teams.", "blackbaud-re"),
                        tile("Classy Donation Pages", "partner", "Peer-to-peer and crowdfunding transactions with UTM and appeal codes.", "classy"),
                    ]},
                {"box": "Grants & Finance", "ic": "erp", "tiles": [
                        tile("Blackbaud Financial Edge", "erp", "Restricted and unrestricted funds, allocations and grant drawdowns.", "blackbaud-fe"),
                        tile("Fluxx Grantmaker", "sheet", "Sub-grant applications, awards and milestone reporting to institutional donors.", "fluxx"),
                        tile("SAP Public Sector", "erp", "Project accounting, procurement and audit-ready financial close for large NGOs.", "sap-public"),
                    ]},
                {"box": "Program & Field M&E", "ic": "globe", "tiles": [
                        tile("CommCare Mobile", "api", "Field surveys, case management and visit logs from community health and protection programs.", "commcare"),
                        tile("KoBoToolbox", "notebook", "Rapid assessments and baseline surveys deployed in low-connectivity settings.", "kobo"),
                        tile("DevResults M&E", "chart", "Indicator frameworks, results chains and portfolio dashboards for program teams.", "devresults"),
                    ]},
                {"box": "Logistics & HR", "ic": "stream", "tiles": [
                        tile("RITA (Logistics Cluster)", "stream", "WFP and Logistics Cluster relief-item tracking: warehouse stock and dispatch to distribution points.", "logistics-cluster"),
                        tile("Workday HCM", "people", "Staff roster, payroll and duty-of-care records across country offices.", "workday"),
                        tile("International SOS", "gavel", "Travel risk approvals, incident reports and security check-ins for field staff."),
                    ]},
                fed_group("UN Agency Data Mart", "OCHA and cluster reference datasets left at partners and queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("Guidestar / Candid", "partner", "Charity registry and 990 filings consumed inbound for due diligence on partners.", "candid"),
                tile("OFAC Sanctions Lists", "gavel", "Watchlist updates parsed on arrival for donor and vendor screening.", "ofac"),
                tile("IATI d-portal / HXL (HDX)", "globe", "Aid-flow (IATI) and 3W activity data on HDX parsed on arrival for coordination and targeting.", "openweather"),
            ]),
            "ppl": ppl_rail2([
                biz("Executive Directors", "Genie One", "The CEO on funds raised and program reach; the CFO on restricted-fund compliance and audit readiness when a major institutional grant closes out.", [["Genie One", "Ask what unrestricted reserves are after last quarter's campaigns without waiting on finance."], ["AI/BI", "Fundraising, program cost and compliance on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"restricted\" means one thing across CRM and ERP."]], sub=[["CEO & Board", "funds raised, program reach and whether the mission is moving for the money spent."], ["CFO & Finance", "restricted-fund compliance, reserves and a clean audit when a major grant closes out."], ["Country Directors", "portfolio delivery and cost per outcome across programs and geographies."]], ucs=["Cost per Outcome", "Program Outcomes", "Grant Compliance", "Donor Churn"]),
                biz("Development & Marketing", "CustomerLake", "Major gifts, digital campaigns and donor journeys when appeal season peaks, tracked on donor retention and cost per dollar raised.", [["Donor Journey Hub", "Lapsed and upgrade segments before year-end mail drops."], ["CustomerLake", "Household segments without copying CRM into a separate CDP."], ["AI/BI", "Retention and cost per dollar raised on governed definitions."]], sub=[["Major Gifts", "the major-gift pipeline and which prospects are ready for the ask this quarter."], ["Digital Fundraising", "appeal performance, cost per dollar raised and donor acquisition channels."], ["Donor Care", "stewardship, retention and the lapsed and upgrade journeys before year-end."]], ucs=["Donor Propensity", "Donor Churn", "Impact Storytelling", "Volunteer Mobilisation"]),
                biz("Programs & M&E", "AI/BI", "Country directors on indicator progress, beneficiary reach and field data quality, and cost per outcome compared across programs and geographies.", [["Program Portfolio", "Outcome indicators by grant and geography on one surface."], ["Genie One", "Ask which sites missed their vaccination target last month."], ["Unity Catalog", "One beneficiary definition across mobile and grant systems."]], sub=[["Country Directors", "indicator progress and beneficiary reach across the country portfolio."], ["M&E Advisors", "results chains, indicator definitions and the evidence behind outcome claims."], ["Field Data Quality", "survey completeness and one beneficiary definition across mobile and grant systems."]], ucs=["Program Outcomes", "Beneficiary Targeting", "Cost per Outcome"]),
                biz("Grants & Compliance", "Unity Catalog", "Grant managers on eligibility, reporting deadlines and sub-grantee risk, watching spend against budget and the compliance exception rate.", [["Grant Compliance Desk", "Milestone and budget exceptions before funder reports lock."], ["Unity Catalog", "Lineage from field survey to funder disclosure."], ["AI/BI", "Spend against budget on certified Metric Views."]], sub=[["Grant Managers", "eligibility, reporting deadlines and spend against budget on every award."], ["Compliance & Audit", "restricted-fund rules, audit readiness and the exception rate funders see."], ["Sub-grantee Risk", "due diligence, sanctions screening and sub-grantee monitoring."]], ucs=["Grant Compliance", "Sanctions Screening", "Cost per Outcome"]),
                biz("Field Operations", "Apps", "Logistics and security on stock positions, convoy movements and duty of care, tracked on distribution reach and lead time during emergency surges.", [["Field Ops Console", "Stock and distribution status during emergency surges."], ["Apps", "Approval workflows hosted next to governed data."], ["Lakehouse//RT", "Dispatch updates at the latency a crisis moves at."]], sub=[["Logistics & Supply", "stock positions, in-kind donations and dispatch to distribution points."], ["Security & Duty of Care", "travel approvals, incident reports and staff check-ins in the field."], ["Volunteer Coordination", "volunteer capacity and rostering for campaigns and emergency surges."]], ucs=["Emergency Surge", "Volunteer Mobilisation", "Beneficiary Targeting"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the CRM gift, grant ledger, mobile survey and logistics feeds; own the Bronze to Silver path and the pager when a field pipeline breaks.", [["Lakeflow Connect", "Managed connectors for CRM, ERP and mobile M&E sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on gift and survey feeds."], ["Lakewatch", "Freshness on the fundraising and indicator tables leadership reads."]], sub=[["Ingestion", "managed connectors for CRM, grant ledger, mobile M&E and logistics feeds."], ["Pipeline Reliability", "Bronze-to-Silver expectations and the pager when a field feed breaks."], ["Governance", "lineage and freshness on the fundraising and indicator tables leadership reads."]], ucs=["Grant Compliance", "Program Outcomes", "Emergency Surge"]),
                biz("Data Scientists", "MLflow", "Donor propensity, churn, beneficiary-targeting and anticipatory-action models, and whether they still hold six months after deployment in the field.", [["Feature Store", "Giving and field features read identically in training and serving."], ["MLflow", "Every propensity and churn run tracked for audit and reproduction."], ["Model Serving", "Donor and targeting models scored in the campaign and field path."]], sub=[["Donor Modeling", "propensity and churn models on giving and engagement history."], ["Targeting & Anticipatory", "beneficiary-targeting and anticipatory-action models for the field."], ["Model Ops", "whether a model still holds six months after deployment in the field."]], ucs=["Donor Propensity", "Donor Churn", "Beneficiary Targeting", "Emergency Surge"]),
                biz("App Developers", "Apps", "Ship the donor journey, grant compliance and field-ops applications development and program teams work in, hosted next to governed data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for case and approval state and governed writes."], ["Agent Bricks", "Agents that draft a funder narrative against governed tools."]], sub=[["Donor & Marketing Apps", "the donor journey and stewardship screens fundraisers work in."], ["Field & Grant Apps", "grant compliance and field-ops apps hosted next to governed data."], ["Agents", "agents that draft a funder narrative against governed tools."]], ucs=["Impact Storytelling", "Volunteer Mobilisation", "Grant Compliance"]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                        tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                        tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and surge updates in the channel field teams already work in (Beta)."),
                        tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code."),
                    ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                        tile("Donor Writeback", "custlake", "Gift thank-you and pledge reminders written back into CRM from governed segments.", "sf-nonprofit"),
                        tile("Grant Milestone Posts", "erp", "Approved narrative and financial actuals posted to grantmaker portals.", "fluxx"),
                        tile("Field Case Updates", "api", "Supervisor approvals pushed to mobile case management after data review.", "commcare"),
                    ]},
                {"box": "Partners & Donors", "ic": "partner", "tiles": [
                        tile("Institutional Funder Portal", "share", "Portfolio indicators and financial summaries shared over Delta Sharing instead of emailed PDFs.", "fluxx"),
                        tile("Corporate Partner API", "api", "Campaign impact metrics served to corporate sponsors from governed outcomes.", "classy"),
                        tile("Consortium Data Exchange", "globe", "Cluster partners reading live program tables during joint responses.", "logistics-cluster"),
                    ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                        tile("990 / Charity Filings", "gavel", "Annual charity returns produced from the same governed tables finance closes on.", "candid"),
                        tile("Funder Narrative Reports", "share", "Indicator and financial annexes filed from contracted Gold products.", "devresults"),
                    ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                        tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                        tile("Sharing Recipients", "share", "Funders, partners and auditors reading live tables with no copy and no egress duplication."),
                    ]},
            ]),
        },
        "top": top_band(
            [
                app("Donor Journey Hub", "Stewardship", "custlake", "Upgrade, lapse and major-gift pipelines on Databricks Apps over Lakebase before appeal windows close."),
                app("Program Portfolio", "M&E live", "chart", "Indicator progress and beneficiary reach by grant and country on one surface."),
                app("Grant Compliance Desk", "Funder reporting", "gavel", "Budget variance and milestone risk before quarterly submissions lock."),
                app("Field Ops Console", "Surge logistics", "stream", "Stock, convoy and distribution status during emergency deployments."),
            ],
            [
                uc("Donor Propensity", "Fundraising", "custlake", "Major-gift and upgrade likelihood scored from engagement and giving history.",
                    problem="Major-gift and upgrade potential is buried in years of gifts, events and email history, so gift officers chase warm names by instinct and the best prospects go unworked before the ask.",
                    who="Development & Marketing",
                    how="Engagement and giving history are engineered in Feature Store and scored through Model Serving, surfacing ranked prospects into the Donor Journey Hub before the ask.",
                    comps=["Donor Journey Hub", "Model Serving", "Feature Store", "Salesforce Nonprofit Cloud", "MLflow"],
                    stories=[
                        ["MissionWired drives strong donor campaigns through predictive data", "https://www.databricks.com/customers/missionwired"],
                    ]),
                uc("Donor Churn", "Retention", "people", "Lapsed and downgraded donors surfaced before renewal campaigns launch.",
                    problem="Lapsed and downgraded donors are noticed only after the renewal fails, when reactivation costs far more than the retention touch that would have kept the relationship alive.",
                    who="Development & Marketing",
                    how="Giving cadence and engagement signals feed churn models scored in Model Serving, pushing at-risk and win-back segments into the Donor Journey Hub before renewal campaigns launch.",
                    comps=["Donor Journey Hub", "Model Serving", "MLflow", "CustomerLake", "Feature Store"],
                    stories=[
                        ["MissionWired drives strong donor campaigns through predictive data", "https://www.databricks.com/customers/missionwired"],
                        ["Australian Red Cross Lifeblood: 2023 Databricks Data Team Awards", "https://www.databricks.com/blog/announcing-winners-2023-databricks-data-team-awards"],
                    ]),
                uc("Grant Compliance", "Audit", "gavel", "Restricted-fund exceptions flagged before funder and board review.",
                    problem="Restricted-fund rules, milestones and budgets live in separate finance, grants and field systems, so exceptions surface in the funder audit rather than before the report is filed.",
                    who="Grants & Compliance",
                    how="Grant ledger, budget and milestone data are conformed under Unity Catalog and checked in the Grant Compliance Desk, flagging restricted-fund exceptions before funder and board review.",
                    comps=["Grant Compliance Desk", "Unity Catalog", "Blackbaud Financial Edge", "Fluxx Grantmaker", "AI/BI"]),
                uc("Program Outcomes", "M&E", "chart", "Indicator attainment linked to spend and geography for portfolio reviews.",
                    problem="Indicator results sit in mobile survey tools while spend sits in finance, so no one can show whether a program actually moved its outcomes for the money it consumed.",
                    who="Programs & M&E",
                    how="Survey and grant data are conformed on Delta Lake and served through the Program Portfolio and AI/BI, linking indicator attainment to spend and geography for portfolio reviews.",
                    comps=["Program Portfolio", "AI/BI", "Unity Catalog", "DevResults M&E", "Delta Lake"],
                    stories=[
                        ["Turning insight into impact with Databricks and Global Orphan Project", "https://www.databricks.com/blog/turning-insight-impact-databricks-and-global-orphan-go-project"],
                        ["How World Bank Group uses Databricks to eradicate poverty through shared knowledge", "https://www.databricks.com/blog/how-world-bank-group-uses-databricks-eradicate-poverty-through-shared-knowledge"],
                    ]),
                uc("Beneficiary Targeting", "Equity", "globe", "Underserved communities identified from field and census overlays.",
                    problem="Aid is allocated on last year's caseload and gut feel, so underserved households are missed while served areas get revisited and equity claims cannot be evidenced.",
                    who="Programs & M&E",
                    how="Field survey and census overlays are scored in Model Serving against a conformed beneficiary model, surfacing underserved communities into program planning.",
                    comps=["Model Serving", "CommCare Mobile", "Unity Catalog", "AI/BI", "Feature Store"],
                    stories=[
                        ["Virtue Foundation scales global health with data and AI", "https://www.databricks.com/customers/virtue-foundation"],
                    ]),
                uc("Emergency Surge", "Humanitarian", "stream", "Logistics and staffing scaled from early signals before peaks hit.",
                    problem="When a crisis breaks, stock, staff and cash are mobilised from spreadsheets and phone calls, so the response lags the need and pre-positioning decisions are made blind.",
                    who="Field Operations",
                    how="Hazard, logistics and roster feeds land in Lakehouse//RT and drive anticipatory-action triggers in the Field Ops Console, scaling supply and staffing before peaks hit.",
                    comps=["Field Ops Console", "Lakehouse//RT", "IATI d-portal / HXL (HDX)", "RITA (Logistics Cluster)", "Model Serving"],
                    stories=[
                        ["Zipline delivers critical medical supplies with data and AI", "https://www.databricks.com/customers/zipline"],
                    ]),
                uc("Sanctions Screening", "Risk", "gavel", "Donor and vendor matches resolved against watchlists on every gift.",
                    problem="Every gift and vendor must clear watchlists, yet manual name matching against sanctions lists is slow and error-prone, leaving the organisation exposed on the matches it misses.",
                    who="Grants & Compliance",
                    how="Donor and vendor records are matched against parsed OFAC lists with AI Functions under Unity Catalog, resolving hits on every gift with a lineage trail for audit.",
                    comps=["OFAC Sanctions Lists", "AI Functions", "Unity Catalog", "Salesforce Nonprofit Cloud", "Model Serving"]),
                uc("Cost per Outcome", "Efficiency", "sheet", "Program economics compared across interventions and geographies.",
                    problem="Comparing what an outcome costs across programs and countries means reconciling incompatible budgets and indicators by hand, so leadership debates anecdotes instead of unit economics.",
                    who="Executive Directors",
                    how="Conformed spend and outcome products are exposed as certified Metric Views in AI/BI and the Program Portfolio, comparing cost per outcome across interventions and geographies.",
                    comps=["Program Portfolio", "AI/BI", "Unity Catalog", "Blackbaud Financial Edge", "Data Products"]),
                uc("Volunteer Mobilisation", "Community", "people", "Volunteer capacity matched to campaigns and field events by region.",
                    problem="Volunteer availability, skills and history are scattered across events and offices, so campaigns and field surges are staffed late and willing volunteers are never asked.",
                    who="Field Operations",
                    how="Volunteer and campaign data are conformed under Unity Catalog and matched in an Apps console on Lakebase, aligning volunteer capacity to campaigns and field events by region.",
                    comps=["Apps", "Lakebase", "Unity Catalog", "Workday HCM", "AI/BI"],
                    stories=[
                        ["Crisis Text Line supports people in crisis with data and AI", "https://www.databricks.com/customers/crisis-text-line"],
                    ]),
                uc("Impact Storytelling", "Communications", "notebook", "Outcome evidence assembled for appeals without manual spreadsheet chases.",
                    problem="Appeals and funder narratives are assembled by chasing outcome numbers across spreadsheets and inboxes, so the story lands late and rarely reflects the latest governed evidence.",
                    who="Development & Marketing",
                    how="Agent Bricks drafts appeal and funder narratives with AI Functions against governed Gold outcome products, so evidence-backed stories assemble without manual spreadsheet chases.",
                    comps=["Agent Bricks", "AI Functions", "Genie One", "Data Products", "AI/BI"],
                    stories=[
                        ["Turning insight into impact with Databricks and Global Orphan Project", "https://www.databricks.com/blog/turning-insight-impact-databricks-and-global-orphan-go-project"],
                    ]),
            ],
        ),
        "sources": {
            "sf-nonprofit": {"t": "Salesforce Nonprofit Cloud", "u": "https://www.salesforce.com/nonprofit/"},
            "blackbaud-re": {"t": "Blackbaud Raiser's Edge NXT", "u": "https://www.blackbaud.com/products/raisers-edge-nxt"},
            "classy": {"t": "Classy fundraising", "u": "https://www.classy.org/"},
            "blackbaud-fe": {"t": "Blackbaud Financial Edge NXT", "u": "https://www.blackbaud.com/financial-management/financial-edge-nxt"},
            "fluxx": {"t": "Fluxx Grantmaker", "u": "https://www.fluxx.io/grantmaker"},
            "sap-public": {"t": "SAP for public sector", "u": "https://www.sap.com/industries/public-sector.html"},
            "commcare": {"t": "CommCare", "u": "https://www.commcare.org/"},
            "kobo": {"t": "KoBoToolbox", "u": "https://www.kobotoolbox.org/"},
            "devresults": {"t": "DevResults", "u": "https://www.devresults.com/"},
            "logistics-cluster": {"t": "Logistics Cluster (RITA)", "u": "https://rita.logcluster.org/"},
            "workday": {"t": "Workday HCM", "u": "https://www.workday.com/en-us/products/human-capital-management/overview.html"},
            "candid": {"t": "Candid", "u": "https://candid.org/"},
            "ofac": {"t": "US Treasury OFAC sanctions", "u": "https://ofac.treasury.gov/"},
            "openweather": {"t": "IATI Standard / HDX (HXL)", "u": "https://iatistandard.org"},
        },
    },
}
