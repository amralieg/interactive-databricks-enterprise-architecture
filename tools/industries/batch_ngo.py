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
                        tile("Salesforce Nonprofit", "custlake", "Donor profiles, campaigns, pledges and recurring gifts from the CRM fundraisers work in.", "sf-nonprofit"),
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
                        tile("Humanitarian Logistics", "stream", "Warehouse stock, in-kind donations and dispatch to distribution points.", "logistics-cluster"),
                        tile("Workday HCM", "people", "Staff roster, payroll and duty-of-care records across country offices.", "workday"),
                        tile("Duty of Care Tracking", "gavel", "Travel approvals, incident reports and security check-ins for field staff."),
                    ]},
                fed_group("UN Agency Data Mart", "OCHA and cluster reference datasets left at partners and queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("Guidestar / Candid", "partner", "Charity registry and 990 filings consumed inbound for due diligence on partners.", "candid"),
                tile("OFAC Sanctions Lists", "gavel", "Watchlist updates parsed on arrival for donor and vendor screening.", "ofac"),
                tile("OpenWeather Field", "globe", "Forecast and hazard feeds for anticipatory action triggers in field programs.", "openweather"),
            ]),
            "ppl": ppl_rail2([
                biz("Executive Directors", "Genie One", "The CEO on funds raised and program reach; the CFO on restricted-fund compliance and audit readiness when a major institutional grant closes out.", [["Genie One", "Ask what unrestricted reserves are after last quarter's campaigns without waiting on finance."], ["AI/BI", "Fundraising, program cost and compliance on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"restricted\" means one thing across CRM and ERP."]]),
                biz("Development & Marketing", "CustomerLake", "Major gifts, digital campaigns and donor journeys when appeal season peaks, tracked on donor retention and cost per dollar raised.", [["Donor Journey Hub", "Lapsed and upgrade segments before year-end mail drops."], ["CustomerLake", "Household segments without copying CRM into a separate CDP."], ["AI/BI", "Retention and cost per dollar raised on governed definitions."]]),
                biz("Programs & M&E", "AI/BI", "Country directors on indicator progress, beneficiary reach and field data quality, and cost per outcome compared across programs and geographies.", [["Program Portfolio", "Outcome indicators by grant and geography on one surface."], ["Genie One", "Ask which sites missed their vaccination target last month."], ["Unity Catalog", "One beneficiary definition across mobile and grant systems."]]),
                biz("Grants & Compliance", "Unity Catalog", "Grant managers on eligibility, reporting deadlines and sub-grantee risk, watching spend against budget and the compliance exception rate.", [["Grant Compliance Desk", "Milestone and budget exceptions before funder reports lock."], ["Unity Catalog", "Lineage from field survey to funder disclosure."], ["AI/BI", "Spend against budget on certified Metric Views."]]),
                biz("Field Operations", "Apps", "Logistics and security on stock positions, convoy movements and duty of care, tracked on distribution reach and lead time during emergency surges.", [["Field Ops Console", "Stock and distribution status during emergency surges."], ["Apps", "Approval workflows hosted next to governed data."], ["Lakehouse//RT", "Dispatch updates at the latency a crisis moves at."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the CRM gift, grant ledger, mobile survey and logistics feeds; own the Bronze to Silver path and the pager when a field pipeline breaks.", [["Lakeflow Connect", "Managed connectors for CRM, ERP and mobile M&E sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on gift and survey feeds."], ["Lakewatch", "Freshness on the fundraising and indicator tables leadership reads."]]),
                biz("Data Scientists", "MLflow", "Donor propensity, churn, beneficiary-targeting and anticipatory-action models, and whether they still hold six months after deployment in the field.", [["Feature Store", "Giving and field features read identically in training and serving."], ["MLflow", "Every propensity and churn run tracked for audit and reproduction."], ["Model Serving", "Donor and targeting models scored in the campaign and field path."]]),
                biz("App Developers", "Apps", "Ship the donor journey, grant compliance and field-ops applications development and program teams work in, hosted next to governed data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for case and approval state and governed writes."], ["Agent Bricks", "Agents that draft a funder narrative against governed tools."]]),
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
                uc("Donor Propensity", "Fundraising", "custlake", "Major-gift and upgrade likelihood scored from engagement and giving history."),
                uc("Donor Churn", "Retention", "people", "Lapsed and downgraded donors surfaced before renewal campaigns launch."),
                uc("Grant Compliance", "Audit", "gavel", "Restricted-fund exceptions flagged before funder and board review."),
                uc("Program Outcomes", "M&E", "chart", "Indicator attainment linked to spend and geography for portfolio reviews."),
                uc("Beneficiary Targeting", "Equity", "globe", "Underserved communities identified from field and census overlays."),
                uc("Emergency Surge", "Humanitarian", "stream", "Logistics and staffing scaled from early signals before peaks hit."),
                uc("Sanctions Screening", "Risk", "gavel", "Donor and vendor matches resolved against watchlists on every gift."),
                uc("Cost per Outcome", "Efficiency", "sheet", "Program economics compared across interventions and geographies."),
                uc("Volunteer Mobilisation", "Community", "people", "Volunteer capacity matched to campaigns and field events by region."),
                uc("Impact Storytelling", "Communications", "notebook", "Outcome evidence assembled for appeals without manual spreadsheet chases."),
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
            "logistics-cluster": {"t": "Humanitarian Logistics Cluster", "u": "https://logcluster.org/"},
            "workday": {"t": "Workday HCM", "u": "https://www.workday.com/en-us/products/human-capital-management/overview.html"},
            "candid": {"t": "Candid", "u": "https://candid.org/"},
            "ofac": {"t": "US Treasury OFAC sanctions", "u": "https://ofac.treasury.gov/"},
            "openweather": {"t": "OpenWeather API", "u": "https://openweathermap.org/api"},
        },
    },
}
