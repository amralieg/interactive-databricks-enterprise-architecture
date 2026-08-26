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


INDUSTRIES_BATCH_LEGAL = {
    'legal': {
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
}
