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
                    [["Genie One", "Ask firm-wide realization this quarter without waiting on finance."], ["AI/BI", "Realization, leverage and WIP on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"realization\" means one thing across practices."]],
                    sub=[
                        ["Managing Partner", "firm-wide realization, leverage and the trade between growth and profit per equity partner."],
                        ["General Counsel", "outside-counsel spend against budget and matter profitability by practice group."],
                        ["Firm CFO", "WIP, collections and the gap between billed and collected across the firm."],
                    ],
                    ucs=["Matter Profitability", "Outside Counsel Spend", "Time Entry Compliance"]),
                biz("Practice Management", "AI/BI", "Practice leaders on matter staffing and leverage, budget burn by phase and whether contracts hold to the firm playbook before write-offs pile up.",
                    [["Matter Profitability Console", "Budget versus actual by matter phase and timekeeper."], ["Contract Intelligence Hub", "Non-standard clauses flagged at intake against the playbook."], ["AI/BI", "Matter margin and leverage on certified Metric Views."]],
                    sub=[
                        ["Practice Group Leader", "staffing, leverage and budget burn by matter phase before write-offs pile up."],
                        ["Matter Pricing", "alternative fee arrangements and whether a matter holds to its budget."],
                        ["Knowledge Management", "the firm playbook and standard clauses reused across the practice."],
                    ],
                    ucs=["Matter Profitability", "Contract Playbook Compliance", "Legal Research Analytics", "Time Entry Compliance"]),
                biz("Litigation Support", "Lakehouse//RT", "E-discovery managers on custodian completeness, processing queues and reviewer throughput against the court deadline that will not move.",
                    [["Review Command Centre", "Reviewer throughput and custodian completeness before court deadlines."], ["Lakehouse//RT", "Live review progress at case latency."], ["AI/BI", "Review cost and pace per matter on governed definitions."]],
                    sub=[
                        ["E-Discovery Manager", "custodian completeness, processing queues and throughput against the deadline."],
                        ["Review Team Lead", "reviewer quality, privilege calls and the pace and cost per matter."],
                        ["Litigation Paralegal", "docket deadlines, production sets and certificates of service."],
                    ],
                    ucs=["E-Discovery Review", "Privilege Prediction", "Docket Monitoring"]),
                biz("Compliance", "AI/BI", "Conflicts, KYC and ethics on new-business intake and ongoing matter monitoring, clearing party hits before an engagement letter releases.",
                    [["Conflicts Clearance", "Party and relationship hits before engagement letters release."], ["AI/BI", "Sanctions and PEP screening on certified views."], ["Unity Catalog", "One definition of party and matter across DMS and billing."]],
                    sub=[
                        ["Conflicts Counsel", "party and relationship hits cleared before an engagement letter releases."],
                        ["Ethics & Risk", "ethical walls, privilege logs and the firm's professional-responsibility record."],
                        ["KYC & Intake", "client screening against sanctions and PEP watchlists at new business."],
                    ],
                    ucs=["Conflicts Screening", "Records Retention", "Privilege Prediction"]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the DMS, billing, docket and CLM feeds; own the Bronze to Silver path and the pager when a review or billing load breaks.",
                    [["Lakeflow Connect", "Managed connectors for iManage, Elite 3E and Relativity sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on billing and review feeds."], ["Lakewatch", "Freshness on the tables practice and finance leaders read every morning."]],
                    sub=[
                        ["Ingestion Engineering", "the iManage, Elite 3E, Relativity and docket connectors and the Bronze-to-Silver path."],
                        ["Pipeline Reliability", "the pager when a review or billing load breaks before the morning read."],
                        ["Data Quality", "expectations on billing and review feeds so matter numbers reconcile."],
                    ],
                    ucs=["E-Discovery Review", "Matter Profitability", "Docket Monitoring"]),
                biz("Data Scientists", "MLflow", "Privilege-prediction, realization and clause-risk models, and whether they still hold six months after deployment.",
                    [["Feature Store", "Matter and document features defined once for training and serving."], ["MLflow", "Every review model run tracked for audit and reproduction."], ["Model Serving", "Privilege and clause models scored in the review path."]],
                    sub=[
                        ["ML Engineering", "privilege, realization and clause-risk models from features to serving."],
                        ["Model Governance", "whether a model still holds six months on, tracked in MLflow for audit."],
                        ["NLP & Documents", "clause extraction and time-narrative scoring over legal text."],
                    ],
                    ucs=["Privilege Prediction", "Contract Playbook Compliance", "Matter Profitability"]),
                biz("App Developers", "Apps", "Ship the matter-profitability, review and conflicts applications the firm works in, hosted next to governed data.",
                    [["Apps", "Matter and review screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for review assignments and pre-bill writes."], ["Agent Bricks", "Agents that draft a clause review or conflicts check against governed tools."]],
                    sub=[
                        ["Application Engineering", "the matter-profitability, review and conflicts screens the firm works in."],
                        ["Platform & Lakebase", "serverless Postgres for review assignments and pre-bill writes."],
                        ["Agent Engineering", "agents that draft a clause review or conflicts check against governed tools."],
                    ],
                    ucs=["Matter Profitability", "E-Discovery Review", "Conflicts Screening"]),
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
                uc("Matter Profitability", "Finance", "market", "Realization, leverage and matter margin tracked before year-end write-offs.",
                    problem="Realization and matter margin surface only at year-end, when write-offs are already booked, because WIP, billing and staffing live in separate systems no partner can reconcile in time.",
                    who="Managing Partner & GC",
                    how="Billing, WIP and timekeeper feeds land through Lakeflow and conform on Delta Lake, so the Matter Profitability Console shows budget-versus-actual by phase on certified Metric Views in AI/BI.",
                    comps=["Matter Profitability Console", "Elite 3E", "Lakeflow", "Delta Lake", "AI/BI"]),
                uc("E-Discovery Review", "Litigation", "gauge", "Processing, prioritisation and reviewer throughput optimised against court deadlines.",
                    problem="Review runs against a court deadline that will not move, yet custodian completeness, processing queues and reviewer throughput sit in the e-discovery tool with no governed view of cost.",
                    who="Litigation Support",
                    how="Relativity load files and review metadata land through Lakeflow into Lakehouse//RT, so the Review Command Centre tracks reviewer throughput live against the court deadline.",
                    comps=["Review Command Centre", "RelativityOne", "Lakeflow", "Lakehouse//RT", "AI/BI"],
                    stories=[["How Clifford Chance improves legal document review with data science", "https://www.databricks.com/blog/2020/03/31/data-science-with-azure-databricks-at-clifford-chance.html"]]),
                uc("Privilege Prediction", "Risk", "gavel", "Attorney-client and work-product calls assisted with reproducible model evidence.",
                    problem="Privilege review is manual and inconsistent across reviewers, so attorney-client and work-product calls vary by matter and a missed call risks waiver or an over-broad, costly withholding.",
                    who="Litigation Support",
                    how="Document and matter features are engineered in Feature Store and scored through Model Serving in the review path, with every run tracked in MLflow for defensible, reproducible evidence.",
                    comps=["Review Command Centre", "Model Serving", "MLflow", "Feature Store", "RelativityOne"],
                    stories=[["How Clifford Chance improves legal document review with data science", "https://www.databricks.com/blog/2020/03/31/data-science-with-azure-databricks-at-clifford-chance.html"]]),
                uc("Contract Playbook Compliance", "Commercial", "product", "Clause deviations flagged at intake before negotiation cycles expand.",
                    problem="Non-standard clauses are caught late in negotiation, if at all, because contract terms sit in the CLM while the firm playbook lives in checklists no one opens at intake.",
                    who="Practice Management",
                    how="Ironclad contract text is parsed with AI Functions and scored against the playbook in the Contract Intelligence Hub, flagging clause deviations at intake before negotiation cycles expand.",
                    comps=["Contract Intelligence Hub", "Ironclad CLM", "AI Functions", "Unity Catalog", "AI/BI"],
                    stories=[["Cracking complex contracts with GenAI on Databricks", "https://www.databricks.com/blog/cracking-complex-contracts-genai-azure-databricks"], ["EY-Parthenon turns unstructured M&A data into strategy", "https://www.databricks.com/customers/ey-parthenon"]]),
                uc("Conflicts Screening", "Ethics", "people", "New business intake screened against parties, matters and watchlists in one governed graph.",
                    problem="New business intake is screened against parties, matters and watchlists held in DMS, billing and CLM silos, so a conflict hit can slip through before an engagement letter releases.",
                    who="Compliance",
                    how="Party and matter data conform under Unity Catalog into one governed graph, and the Conflicts Clearance app surfaces relationship and watchlist hits before an engagement letter releases.",
                    comps=["Conflicts Clearance", "Sanctions & PEP Lists", "Unity Catalog", "Delta Lake", "AI/BI"]),
                uc("Outside Counsel Spend", "Corporate", "chart", "Panel firm invoices reconciled to matter budgets and LEDES guidelines.",
                    problem="In-house teams accrue panel-firm invoices against budgets they cannot see line by line, because LEDES files and matter budgets never meet in one place until the bill is already paid.",
                    who="Managing Partner & GC",
                    how="LEDES invoices are validated on ingest and reconciled to matter budgets on Delta Lake, so outside-counsel spend against guidelines shows in the Matter Profitability Console and AI/BI.",
                    comps=["Matter Profitability Console", "LEDES Billing", "Delta Lake", "Unity Catalog", "AI/BI"]),
                uc("Legal Research Analytics", "Knowledge", "notebook", "Precedent and research usage tied to matter outcomes and staffing decisions.",
                    problem="Research spend on Westlaw and Lexis is untethered from matter outcomes and staffing, so no one knows which precedent work actually moved a matter or justified the hours it cost.",
                    who="Practice Management",
                    how="Research usage telemetry conforms with matter and billing data under Unity Catalog and is explored in AI/BI and Genie, tying precedent work to outcomes and staffing decisions.",
                    comps=["Thomson Reuters Westlaw", "LexisNexis Guidance", "Unity Catalog", "AI/BI", "Genie One"],
                    stories=[["JLL turns lease data into governed, queryable knowledge", "https://www.databricks.com/customers/jll/dealsumm"]]),
                uc("Docket Monitoring", "Litigation", "api", "Court filings and orders tracked across matters without manual PACER pulls.",
                    problem="Court filings and orders are tracked by manual PACER pulls per matter, so a deadline-setting order can land unseen for days across a large litigation portfolio.",
                    who="Litigation Support",
                    how="PACER docket events land through Lakeflow onto Delta Lake and stream into Lakehouse//RT, so new filings raise alerts across matters in the Review Command Centre without manual pulls.",
                    comps=["Review Command Centre", "PACER Court Records", "Lakeflow", "Lakehouse//RT", "Delta Lake"]),
                uc("Records Retention", "Compliance", "db", "Legal holds and disposition executed from governed retention policies.",
                    problem="Legal holds and disposition depend on retention rules scattered across the DMS and records tools, so holds are missed and documents kept long past policy, raising cost and discovery risk.",
                    who="Compliance",
                    how="Retention labels from Microsoft Purview conform under Unity Catalog, so holds and disposition execute from one governed policy with auditable lineage from rule to document.",
                    comps=["Microsoft Purview", "Unity Catalog", "Delta Lake", "iManage Work", "AI/BI"],
                    stories=[["Building document intelligence pipelines with Lakeflow", "https://www.databricks.com/blog/building-databricks-document-intelligence-and-lakeflow"]]),
                uc("Time Entry Compliance", "Billing", "erp", "Narrative and UTBMS code quality scored before invoices reach clients.",
                    problem="Time narratives and UTBMS codes are corrected only after a client rejects the bill, so realization leaks to write-downs and pre-bill review eats partner hours late in the cycle.",
                    who="Practice Management",
                    how="Time entries are scored for narrative and UTBMS code quality with AI Functions on Delta Lake, flagging weak entries in the Matter Profitability Console before invoices reach clients.",
                    comps=["Matter Profitability Console", "Elite 3E", "AI Functions", "Delta Lake", "AI/BI"]),
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
