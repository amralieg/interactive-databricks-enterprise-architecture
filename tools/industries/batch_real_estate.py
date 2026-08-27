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


INDUSTRIES_BATCH_REAL_ESTATE = {
    'real_estate': {
        "label": "Real Estate",
        "blurb": "Property investment, development and operations: leasing, valuations, construction progress and tenant experience across commercial and residential portfolios.",
        "medallion": medallion(
            "Raw lease and ops",
            "Lease abstracts, rent rolls, construction draws, work orders and utility meter reads, landed exactly as received so a square foot or a rent step can always be replayed as it stood.",
            "Conformed asset, lease",
            "Properties, units, tenants and leases resolved into single conformed entities across ERP, CRM and operations systems, with CAM reconciliations stitched and occupancy reconciled to one unit record.",
            "NOI, occupancy, capex",
            "Contracted products asset and portfolio leaders run on: net operating income, occupancy and retention, capex per square foot and development IRR.",
        ),
        "rails": {
            "src": [
                {"box": "Property & ERP", "ic": "erp", "tiles": [
                        tile("Yardi Voyager", "erp", "Property accounting, AP/AR and CAM reconciliations for operating portfolios.", "yardi"),
                        tile("MRI Software", "db", "Commercial lease administration, billing and investor reporting.", "mri"),
                        tile("SAP Real Estate Mgmt", "erp", "Corporate real estate, cost allocations and IFRS lease accounting.", "sap-rem"),
                    ]},
                {"box": "Leasing & CRM", "ic": "custlake", "tiles": [
                        tile("Salesforce Real Estate", "custlake", "Broker pipelines, tour activity and lease negotiation stages.", "sf-real-estate"),
                        tile("VTS Lease Platform", "partner", "Availabilities, proposals and executed leases for commercial assets.", "vts"),
                        tile("ARGUS Enterprise", "chart", "Discounted cash flow valuation and hold-sell analysis for commercial assets.", "buildout"),
                    ]},
                {"box": "Construction & Dev", "ic": "sheet", "tiles": [
                        tile("Procore Project Mgmt", "sheet", "Budgets, schedules, RFIs and daily logs from development sites.", "procore"),
                        tile("Oracle Aconex", "notebook", "Document transmittals, submittals and design revisions.", "aconex"),
                        tile("CoStar Market Data", "chart", "Comparable rents, vacancy and transaction comps for underwriting.", "costar"),
                    ]},
                {"box": "Operations & IoT", "ic": "iot", "tiles": [
                        tile("Honeywell Forge BMS", "iot", "HVAC, access and energy telemetry from building management systems.", "honeywell-forge"),
                        tile("ServiceChannel FM", "stream", "Work orders, contractor SLAs and tenant service requests.", "servicechannel"),
                        tile("Measurabl ESG", "observ", "Utility bills, ENERGY STAR scores and carbon disclosures by asset.", "measurabl"),
                    ]},
                fed_group("Investor Reporting Mart", "Fund NAV and waterfall marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("Municipal Permit APIs", "api", "Zoning and permit filings consumed inbound for development risk monitoring.", "procore"),
                tile("Walk Score / Transit", "globe", "Amenity and transit scores attached to assets for underwriting models.", "walkscore"),
                tile("Flood & Hazard Layers", "globe", "Climate hazard overlays normalised for portfolio risk scoring."),
            ]),
            "ppl": ppl_rail2([
                biz("Fund & Asset Leadership", "Genie One", "The CEO on portfolio NOI and occupancy; the CFO on capex per square foot and fund IRR when interest rates and cap rates shift the book.", [["Genie One", "Ask what same-store NOI was last quarter without waiting on asset management."], ["AI/BI", "NOI, occupancy and capex on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"occupancy\" means one thing across ERP and CRM."]],
                    sub=[
                        ["CEO", "portfolio NOI, occupancy and the trade between growth and the cost of capital."],
                        ["CFO & Treasury", "capex per square foot, fund IRR and debt covenants as rates and cap rates move."],
                        ["Head of Investor Relations", "NAV, waterfalls and the reporting investors and lenders see each quarter."],
                    ],
                    ucs=["Investor Reporting", "Portfolio Risk", "Capex Planning", "Rent Forecasting"]),
                biz("Asset Management", "AI/BI", "Portfolio managers on rent rolls, renewals and capital plans by asset, tracking same-store NOI and tenant retention against the annual budget.", [["Portfolio Command", "Lease expirations and renewal risk on one surface."], ["AI/BI", "NOI and retention on governed definitions."], ["Genie One", "Ask which assets missed budgeted rent steps."]],
                    sub=[
                        ["Portfolio Manager", "same-store NOI, renewal risk and the capital plan against the annual budget."],
                        ["Lease Administration", "rent steps, recoveries and critical dates across the rent roll."],
                        ["Valuations", "cap rates, comps and the mark on each asset at reporting."],
                    ],
                    ucs=["Rent Forecasting", "Tenant Retention", "Capex Planning", "CAM Reconciliation"]),
                biz("Development", "Lakehouse//RT", "Development directors on draw schedules, milestones and contractor performance, watching cost-to-complete and development IRR against covenants.", [["Development Tracker", "Budget and schedule variance before lender reports."], ["Lakehouse//RT", "Site progress at the latency a delay compounds at."], ["Model Serving", "Cost-to-complete models scored on draw history."]],
                    sub=[
                        ["Development Director", "draw schedules, cost-to-complete and development IRR against covenants."],
                        ["Project Controls", "budget and schedule variance and contractor performance on site."],
                        ["Construction Finance", "lender draws, retention and the capital stack on each project."],
                    ],
                    ucs=["Development ROI", "Capex Planning"]),
                biz("Leasing & Brokerage", "CustomerLake", "Brokerage teams on pipeline, tour conversion and time-to-lease, tracking leasing velocity and net effective rent by asset and market.", [["Leasing Pipeline", "Proposal status and comp rents before options expire."], ["CustomerLake", "Tenant prospects without copying CRM elsewhere."], ["Apps", "Tour and proposal workflows on governed data."]],
                    sub=[
                        ["Leasing Director", "pipeline, net effective rent and time-to-lease by asset and market."],
                        ["Brokerage Team", "tour activity, proposals and conversion across the deal desk."],
                        ["Lease Counsel", "clauses, options and the abstract behind every executed lease."],
                    ],
                    ucs=["Broker Performance", "Lease Abstraction", "Tenant Retention"]),
                biz("Property Operations", "Apps", "Building engineers and FM on work orders, energy intensity and tenant satisfaction, watching SLA breaches and operating cost per square foot.", [["Operations Hub", "Open tickets and SLA breaches before renewals."], ["Apps", "Technician mobile workflows on governed BMS data."], ["Lakeflow", "Utility and work-order feeds conformed for asset analytics."]],
                    sub=[
                        ["Chief Engineer", "HVAC, energy intensity and equipment reliability across the building."],
                        ["Facilities Management", "work orders, contractor SLAs and tenant service requests."],
                        ["ESG & Sustainability", "ENERGY STAR, carbon disclosure and utility cost per square foot."],
                    ],
                    ucs=["Energy Optimisation", "CAM Reconciliation", "Tenant Retention"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the ERP lease, CRM, construction and BMS meter feeds; own the Bronze to Silver path and the pager when a portfolio pipeline breaks.", [["Lakeflow Connect", "Managed connectors for property ERP, CRM and BMS sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on lease and meter feeds."], ["Lakewatch", "Freshness on the NOI and occupancy tables asset teams read."]],
                    sub=[
                        ["Ingestion Engineering", "the ERP lease, CRM, construction and BMS feeds landing on time."],
                        ["Platform Reliability", "the pager and freshness on the NOI and occupancy tables."],
                        ["Governance Engineering", "Unity Catalog permissions and lineage across property systems."],
                    ],
                    ucs=["Development ROI", "CAM Reconciliation", "Portfolio Risk"]),
                biz("Data Scientists", "MLflow", "Rent-forecast, tenant-retention, energy-optimisation and cost-to-complete models, and whether they still hold six months after deployment across the portfolio.", [["Feature Store", "Lease and market features read identically in training and serving."], ["MLflow", "Every rent and retention run tracked for audit and reproduction."], ["Model Serving", "Rent and churn models scored in the underwriting path."]],
                    sub=[
                        ["Rent & Valuation Modelling", "market rent, renewal probability and asset valuation models."],
                        ["Retention & Risk", "tenant churn, credit and portfolio climate-risk scoring."],
                        ["Energy Optimisation", "occupancy and tariff-aware HVAC and lighting models."],
                    ],
                    ucs=["Rent Forecasting", "Tenant Retention", "Energy Optimisation"]),
                biz("App Developers", "Apps", "Ship the portfolio command, development tracker and operations applications asset and FM teams work in, hosted next to governed property data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for work-order state and governed writes."], ["Agent Bricks", "Agents that draft a lease abstract against governed tools."]],
                    sub=[
                        ["Application Engineering", "the portfolio, leasing and operations screens teams work in."],
                        ["Workflow & Writeback", "governed writes back to Yardi, BMS and FM systems."],
                        ["Agent Engineering", "agents that draft a lease abstract against governed tools."],
                    ],
                    ucs=["Lease Abstraction", "Broker Performance", "Investor Reporting"]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                        tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                        tile("Microsoft Teams", "chat", "Genie in Teams for governed answers and site updates in the channel asset teams work in (Beta)."),
                        tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code."),
                    ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                        tile("Yardi Lease Posting", "erp", "Executed lease terms and rent steps written back into property accounting.", "yardi"),
                        tile("BMS Setpoint Adjust", "iot", "Approved HVAC schedules pushed from energy optimisation runs.", "honeywell-forge"),
                        tile("FM Work Orders", "stream", "Predictive maintenance tasks raised in ServiceChannel before failures.", "servicechannel"),
                    ]},
                {"box": "Investors & Tenants", "ic": "partner", "tiles": [
                        tile("Investor Portal API", "share", "Fund performance and property KPIs shared over Delta Sharing not quarterly PDFs.", "mri"),
                        tile("Tenant Experience App", "apps", "Service requests and amenity bookings on Apps reading governed operations data."),
                        tile("Broker Co-broke Feed", "api", "Availability and comps served to brokerage partners from governed listings.", "vts"),
                    ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                        tile("GRESB / ESG Filing", "gavel", "Energy and emissions disclosures filed from governed utility and BMS data.", "measurabl"),
                        tile("IFRS 16 / ASC 842", "share", "Lease liability schedules from contracted Gold products.", "sap-rem"),
                    ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                        tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                        tile("Sharing Recipients", "share", "Investors, lenders and partners reading live tables with no copy."),
                    ]},
            ]),
        },
        "top": top_band(
            [
                app("Portfolio Command", "NOI live", "gauge", "Occupancy, NOI and capex by asset on Databricks Apps over Lakebase."),
                app("Development Tracker", "Draw schedule", "sheet", "Budget, milestone and contractor variance before lender reporting."),
                app("Leasing Pipeline", "Tour to lease", "custlake", "Proposals, comps and expiration risk before options lapse."),
                app("Operations Hub", "FM & energy", "iot", "Work orders, SLA breaches and energy anomalies before tenant renewals."),
            ],
            [
                uc("Rent Forecasting", "Underwriting", "chart", "Market rent and renewal probability scored with comps and tenant history.",
                    problem="Market rent and renewal outcomes are guessed from stale comps and last year's rent roll, so underwriting and budgeted rent steps rest on a number no one can defend per asset.",
                    who="Asset Management",
                    how="Comps, tenant history and market signals are engineered in Feature Store and scored through Model Serving, landing renewal probability and market rent on Portfolio Command.",
                    comps=["Portfolio Command", "CoStar Market Data", "Model Serving", "Feature Store", "MLflow"],
                    stories=[
                        ["Reonomy modernizes real estate with data and ML", "https://www.databricks.com/customers/reonomy"],
                    ]),
                uc("Tenant Retention", "Occupancy", "custlake", "Churn risk surfaced from service tickets and lease economics before expiration.",
                    problem="Tenants leave at renewal after a year of unresolved service tickets and off-market rent, but that churn signal is buried in FM logs and lease economics no one joins until the notice lands.",
                    who="Asset Management",
                    how="Service-ticket history and lease economics are joined and scored in Model Serving, surfacing churn risk on the Leasing Pipeline before renewal windows open.",
                    comps=["Leasing Pipeline", "ServiceChannel FM", "CustomerLake", "Model Serving", "AI/BI"],
                    stories=[
                        ["Cushman & Wakefield builds an enterprise AI core on Databricks", "https://www.databricks.com/blog/your-ai-ready-your-data-foundation-probably-isnt"],
                    ]),
                uc("Capex Planning", "Investment", "sheet", "Replacement and repositioning projects ranked by NOI impact and risk.",
                    problem="Capital plans are built in spreadsheets per asset, so replacement and repositioning projects compete for budget without a comparable view of NOI impact or risk across the portfolio.",
                    who="Fund & Asset Leadership",
                    how="Work-order, condition and NOI data are conformed on Delta Lake under Unity Catalog and ranked in AI/BI, so capex projects sort by NOI impact on Portfolio Command.",
                    comps=["Portfolio Command", "Yardi Voyager", "AI/BI", "Unity Catalog", "Delta Lake"]),
                uc("Energy Optimisation", "Operations", "iot", "HVAC and lighting schedules tuned to occupancy and tariff signals.",
                    problem="HVAC and lighting run to fixed schedules regardless of occupancy or tariff, so energy burns in empty floors and peak-price windows while operating cost per square foot and ESG targets slip.",
                    who="Property Operations",
                    how="BMS telemetry and tariff signals feed optimisation models scored in Model Serving, and approved setpoint schedules are written back to Honeywell Forge BMS from the Operations Hub.",
                    comps=["Operations Hub", "Honeywell Forge BMS", "Model Serving", "Lakehouse//RT", "Measurabl ESG"],
                    stories=[
                        ["Colas drives efficiency and cuts energy use with Databricks", "https://www.databricks.com/customers/colas"],
                        ["TK Elevator delivers service intelligence across connected buildings", "https://www.databricks.com/customers/tke-elevator"],
                    ]),
                uc("Development ROI", "Projects", "product", "Cost-to-complete and IRR tracked against lender covenants in real time.",
                    problem="Development budgets and schedules live in the project system while draws and covenants live in finance, so cost-to-complete and IRR are reconciled by hand and slippage surfaces only at the lender report.",
                    who="Development",
                    how="Procore budget, schedule and draw data land through Lakeflow and are tracked against covenants in AI/BI, so cost-to-complete and IRR update live on the Development Tracker.",
                    comps=["Development Tracker", "Procore Project Mgmt", "Lakeflow", "AI/BI", "Delta Lake"],
                    stories=[
                        ["Trackunit eliminates downtime for the construction industry", "https://www.databricks.com/customers/trackunit"],
                    ]),
                uc("Lease Abstraction", "Legal", "gavel", "Critical dates and options extracted from abstracts with audit lineage.",
                    problem="Critical dates, options and clauses sit in thousands of PDF leases in varied formats and languages, so abstraction is manual and slow and a missed option date is a real financial loss.",
                    who="Leasing & Brokerage",
                    how="Lease PDFs are extracted with AI Functions and Agent Bricks into governed records under Unity Catalog, with lineage back to the source clause and Genie for portfolio-level questions.",
                    comps=["Leasing Pipeline", "AI Functions", "Agent Bricks", "Unity Catalog", "Genie One"],
                    stories=[
                        ["JLL turns lease data into governed insights with Genie and AI/BI", "https://www.databricks.com/customers/jll/dealsumm"],
                    ]),
                uc("CAM Reconciliation", "Finance", "erp", "Operating expense pools reconciled before tenant true-ups post.",
                    problem="Operating-expense pools are reconciled against hundreds of lease recovery clauses by hand each year, so CAM true-ups post late and disputes erode the recoveries the budget assumed.",
                    who="Property Operations",
                    how="Expense ledgers and lease recovery terms are conformed on Delta Lake and reconciled in AI/BI, so CAM pools tie out before true-ups post from Yardi Voyager.",
                    comps=["Operations Hub", "Yardi Voyager", "MRI Software", "Delta Lake", "AI/BI"]),
                uc("Portfolio Risk", "Climate", "globe", "Flood and hazard exposure aggregated for insurance and disclosure.",
                    problem="Flood, wildfire and heat exposure is assessed asset by asset at insurance renewal, so the portfolio's aggregate climate risk and its effect on premiums and disclosure is never seen whole.",
                    who="Fund & Asset Leadership",
                    how="Hazard layers are joined to the asset register with H3 spatial indexing in Apache Spark and aggregated in AI/BI, so climate exposure rolls up by fund on Portfolio Command.",
                    comps=["Portfolio Command", "Flood & Hazard Layers", "Apache Spark", "AI/BI", "Delta Lake"],
                    stories=[
                        ["Geospatial analytics and AI with Databricks and CARTO for JLL", "https://www.databricks.com/blog/2021/12/09/announcing-cartos-spatial-extension-for-databricks-powering-geospatial-analysis-for-jll.html"],
                    ]),
                uc("Broker Performance", "Leasing", "partner", "Tour conversion and time-to-lease compared across brokerage teams.",
                    problem="Tour activity, proposals and executed leases sit in the CRM and the leasing platform separately, so time-to-lease and conversion are compared across brokerage teams from stale exports weeks late.",
                    who="Leasing & Brokerage",
                    how="Salesforce and VTS activity are conformed under Unity Catalog and surfaced in AI/BI, so tour conversion and time-to-lease compare across teams on the Leasing Pipeline.",
                    comps=["Leasing Pipeline", "VTS Lease Platform", "Salesforce Real Estate", "Unity Catalog", "AI/BI"]),
                uc("Investor Reporting", "Funds", "share", "NAV and waterfall metrics produced from the same tables finance closes on.",
                    problem="Fund NAV and waterfalls are rebuilt in spreadsheets each quarter from data finance already closed, so investor reporting lags weeks behind and every number is reconciled twice.",
                    who="Fund & Asset Leadership",
                    how="NAV and waterfall marts are queried in place from the Investor Reporting Mart under Unity Catalog and shared to investors over Open Sharing instead of quarterly PDFs.",
                    comps=["Investor Reporting Mart", "Unity Catalog", "Open Sharing", "Data Products", "AI/BI"],
                    stories=[
                        ["JLL modernizes its data stack and analytics with Databricks", "https://www.databricks.com/customers/jll/training-and-certification"],
                    ]),
            ],
        ),
        "sources": {
            "yardi": {"t": "Yardi Voyager", "u": "https://www.yardi.com/products/voyager/"},
            "mri": {"t": "MRI Software", "u": "https://www.mrisoftware.com/"},
            "sap-rem": {"t": "SAP Real Estate Management", "u": "https://www.sap.com/products/financial-management/real-estate-management.html"},
            "sf-real-estate": {"t": "Salesforce for real estate", "u": "https://www.salesforce.com/solutions/industries/real-estate/"},
            "vts": {"t": "VTS", "u": "https://www.vts.com/"},
            "buildout": {"t": "Altus ARGUS Enterprise", "u": "https://www.altusgroup.com/solutions/argus-enterprise/"},
            "procore": {"t": "Procore", "u": "https://www.procore.com/"},
            "aconex": {"t": "Oracle Aconex", "u": "https://www.oracle.com/industries/construction-engineering/aconex/"},
            "costar": {"t": "CoStar", "u": "https://www.costar.com/"},
            "honeywell-forge": {"t": "Honeywell Forge", "u": "https://www.honeywellforge.com/"},
            "servicechannel": {"t": "ServiceChannel", "u": "https://servicechannel.com/"},
            "measurabl": {"t": "Measurabl", "u": "https://www.measurabl.com/"},
            "walkscore": {"t": "Walk Score", "u": "https://www.walkscore.com/professional/"},
        },
    },
}
