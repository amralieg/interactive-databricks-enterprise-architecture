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
                        tile("Buildout Marketing", "market", "Listing collateral, floor plans and marketing performance by asset.", "buildout"),
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
                biz("Fund & Asset Leadership", "Genie One", "The CEO on portfolio NOI and occupancy; the CFO on capex per square foot and fund IRR when interest rates and cap rates shift the book.", [["Genie One", "Ask what same-store NOI was last quarter without waiting on asset management."], ["AI/BI", "NOI, occupancy and capex on one certified set of Metric Views."], ["Unity Catalog", "Certification so \"occupancy\" means one thing across ERP and CRM."]]),
                biz("Asset Management", "AI/BI", "Portfolio managers on rent rolls, renewals and capital plans by asset, tracking same-store NOI and tenant retention against the annual budget.", [["Portfolio Command", "Lease expirations and renewal risk on one surface."], ["AI/BI", "NOI and retention on governed definitions."], ["Genie One", "Ask which assets missed budgeted rent steps."]]),
                biz("Development", "Lakehouse//RT", "Development directors on draw schedules, milestones and contractor performance, watching cost-to-complete and development IRR against covenants.", [["Development Tracker", "Budget and schedule variance before lender reports."], ["Lakehouse//RT", "Site progress at the latency a delay compounds at."], ["Model Serving", "Cost-to-complete models scored on draw history."]]),
                biz("Leasing & Brokerage", "CustomerLake", "Brokerage teams on pipeline, tour conversion and time-to-lease, tracking leasing velocity and net effective rent by asset and market.", [["Leasing Pipeline", "Proposal status and comp rents before options expire."], ["CustomerLake", "Tenant prospects without copying CRM elsewhere."], ["Apps", "Tour and proposal workflows on governed data."]]),
                biz("Property Operations", "Apps", "Building engineers and FM on work orders, energy intensity and tenant satisfaction, watching SLA breaches and operating cost per square foot.", [["Operations Hub", "Open tickets and SLA breaches before renewals."], ["Apps", "Technician mobile workflows on governed BMS data."], ["Lakeflow", "Utility and work-order feeds conformed for asset analytics."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the ERP lease, CRM, construction and BMS meter feeds; own the Bronze to Silver path and the pager when a portfolio pipeline breaks.", [["Lakeflow Connect", "Managed connectors for property ERP, CRM and BMS sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on lease and meter feeds."], ["Lakewatch", "Freshness on the NOI and occupancy tables asset teams read."]]),
                biz("Data Scientists", "MLflow", "Rent-forecast, tenant-retention, energy-optimisation and cost-to-complete models, and whether they still hold six months after deployment across the portfolio.", [["Feature Store", "Lease and market features read identically in training and serving."], ["MLflow", "Every rent and retention run tracked for audit and reproduction."], ["Model Serving", "Rent and churn models scored in the underwriting path."]]),
                biz("App Developers", "Apps", "Ship the portfolio command, development tracker and operations applications asset and FM teams work in, hosted next to governed property data.", [["Apps", "Operational screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for work-order state and governed writes."], ["Agent Bricks", "Agents that draft a lease abstract against governed tools."]]),
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
                uc("Rent Forecasting", "Underwriting", "chart", "Market rent and renewal probability scored with comps and tenant history."),
                uc("Tenant Retention", "Occupancy", "custlake", "Churn risk surfaced from service tickets and lease economics before expiration."),
                uc("Capex Planning", "Investment", "sheet", "Replacement and repositioning projects ranked by NOI impact and risk."),
                uc("Energy Optimisation", "Operations", "iot", "HVAC and lighting schedules tuned to occupancy and tariff signals."),
                uc("Development ROI", "Projects", "product", "Cost-to-complete and IRR tracked against lender covenants in real time."),
                uc("Lease Abstraction", "Legal", "gavel", "Critical dates and options extracted from abstracts with audit lineage."),
                uc("CAM Reconciliation", "Finance", "erp", "Operating expense pools reconciled before tenant true-ups post."),
                uc("Portfolio Risk", "Climate", "globe", "Flood and hazard exposure aggregated for insurance and disclosure."),
                uc("Broker Performance", "Leasing", "partner", "Tour conversion and time-to-lease compared across brokerage teams."),
                uc("Investor Reporting", "Funds", "share", "NAV and waterfall metrics produced from the same tables finance closes on."),
            ],
        ),
        "sources": {
            "yardi": {"t": "Yardi Voyager", "u": "https://www.yardi.com/products/voyager/"},
            "mri": {"t": "MRI Software", "u": "https://www.mrisoftware.com/"},
            "sap-rem": {"t": "SAP Real Estate Management", "u": "https://www.sap.com/products/financial-management/real-estate-management.html"},
            "sf-real-estate": {"t": "Salesforce for real estate", "u": "https://www.salesforce.com/solutions/industries/real-estate/"},
            "vts": {"t": "VTS", "u": "https://www.vts.com/"},
            "buildout": {"t": "Buildout", "u": "https://www.buildout.com/"},
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
