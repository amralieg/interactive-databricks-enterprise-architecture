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


INDUSTRIES_BATCH_TELECOMMUNICATION = {
    'telecommunication': {
        "label": "Telecommunications",
        "blurb": "Mobile and fixed operators: network inventory and performance, customer billing and care, field service, fraud and revenue assurance, and 5G service orchestration.",
        "medallion": medallion(
            "Raw network and BSS feeds",
            "CDR and usage records, probe and SNMP metrics, CRM interactions, work orders and billing cycles, landed exactly as received so a dropped call or a disputed charge can always be replayed.",
            "Conformed subscriber, session",
            "Subscribers, devices, cells and service instances resolved into single conformed entities across BSS, OSS and CRM, with session records stitched to one journey.",
            "Churn, ARPU, network KPI",
            "Contracted products commercial and network teams run on: churn and ARPU by segment, dropped-call rate, mean time to repair, fraud loss and NPS drivers.",
        ),
        "rails": {
            "src": [
                {"box": "BSS & Billing", "ic": "erp", "tiles": [
                    tile("Amdocs CES", "erp", "Customer, product and billing: subscriptions, invoices, payments and dunning.", "amdocs-ces"),
                    tile("Netcracker BSS", "market", "Order management, product catalog and revenue management for converged offers.", "netcracker"),
                    tile("CSG Singleview", "chart", "Mediation, rating and billing for high-volume prepaid and postpaid.", "csg"),
                ]},
                {"box": "OSS & Inventory", "ic": "db", "tiles": [
                    tile("Ericsson ENM", "stream", "Radio access network configuration, alarms and performance counters.", "ericsson-enm"),
                    tile("Nokia NetAct", "iot", "Multi-vendor OSS fault, configuration and performance for transport and RAN.", "nokia-netact"),
                    tile("Cisco Crosswork", "api", "IP/MPLS transport inventory, topology and service paths.", "cisco-crosswork"),
                ]},
                {"box": "Customer & Care", "ic": "custlake", "tiles": [
                    tile("Salesforce Service Cloud", "partner", "Cases, omni-channel interactions and knowledge articles.", "sf-service"),
                    tile("Genesys Cloud CX", "chat", "Contact centre queues, IVR paths and agent handle times.", "genesys"),
                    tile("Medallia Experience", "observ", "NPS, CES and verbatim feedback tied to subscriber journeys.", "medallia"),
                ]},
                {"box": "Field Service", "ic": "people", "tiles": [
                    tile("ServiceMax FSM", "apps", "Technician dispatch, truck rolls, parts and SLA compliance.", "servicemax"),
                    tile("ClickSoftware WFM", "sheet", "Field workforce scheduling and capacity for fibre and tower work.", "clicksoftware"),
                    tile("Geotab Fleet", "iot", "Van location, job duration and fuel for field operations.", "geotab"),
                ]},
                {"box": "Fraud & Assurance", "ic": "gavel", "tiles": [
                    tile("Subex Revenue Assurance", "gavel", "Leakage detection across rating, interconnect and roaming.", "subex"),
                    tile("Mobileum Fraud", "partner", "SIM swap, IRSF and subscription fraud scored in near real time.", "mobileum"),
                    tile("WeDo RAID", "chart", "Revenue, asset and usage integrity dashboards for finance.", "wedo"),
                ]},
                fed_group("MVNO Partner Marts", "Wholesale usage and settlement marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("GSMA TAP Roaming", "stream", "TAP files and roaming usage from partner operators parsed on arrival.", "gsma-tap"),
                tile("TM Forum Open APIs", "api", "TMF Open API event streams for order and trouble-ticket lifecycle.", "tmforum"),
                tile("RAN PM File Exchange", "zplug", "Vendor performance management files from multi-vendor RAN estates.", "ericsson-enm"),
            ]),
            "ppl": ppl2([
                biz("CEO & CTO Office", "Genie One", "The CEO on ARPU and churn; the CTO on network availability and capex efficiency, trading coverage build against the subscribers it retains.",
                    [["Genie One", "Ask what last month's churn cost without analyst delay."], ["AI/BI", "ARPU and NPS on certified Metric Views."], ["Unity Catalog", "One subscriber definition across BSS and CRM."]]),
                biz("Network Operations", "Lakehouse//RT", "NOC engineers on alarms, cell performance and outage restoration, grouping faults to root cause and customer impact before a truck rolls.",
                    [["NOC War Room", "Live alarms, customer impact and truck rolls on one screen."], ["Lakehouse//RT", "Probe and alarm state at network latency."]]),
                biz("Commercial & Marketing", "CustomerLake", "Product owners on offer uptake, upsell and retention campaigns, scoring next-best-offer per subscriber before the contract renewal window.",
                    [["Offer Management", "Propensity-scored upsell before renewal."], ["CustomerLake", "Segments without copying profiles into a separate CDP."]]),
                biz("Customer Care", "Apps", "Care leaders on first-contact resolution, handle time and complaint drivers, putting subscriber and network context beside every ticket.",
                    [["Care Agent Desktop", "Subscriber context and next-best-action beside the ticket."], ["Apps", "Care tools hosted next to governed BSS data."]]),
                biz("Revenue Assurance", "AI/BI", "Finance and fraud teams on leakage, disputes and roaming settlement, catching SIM-swap and IRSF loss before it clears interconnect.",
                    [["AI/BI", "Leakage and fraud loss on certified views."], ["Genie One", "Ask which roaming partners exceed dispute thresholds."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land CDR and usage records, probe and SNMP metrics, CRM interactions and billing cycles; own Bronze to Silver and the pager when a churn table stalls.",
                    [["Lakeflow Connect", "Managed connectors for BSS, OSS and CRM sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on CDR and probe feeds."], ["Lakewatch", "Freshness on the churn tables commercial reads each morning."]]),
                biz("Data Scientists", "MLflow", "Churn, fault-correlation, fraud-scoring and capacity-forecast models, and whether they still hold as network load and offer mix shift.",
                    [["Feature Store", "Subscriber and network features read identically in training and serving."], ["MLflow", "Every churn and fraud experiment tracked for audit."], ["Model Serving", "Churn and fraud models scored in the operational path."]]),
                biz("App Developers", "Apps", "Ship the NOC War Room, Care Agent Desktop and Churn Prevention apps network and care teams work in, next to governed BSS and probe data.",
                    [["Apps", "Care and NOC screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for ticket and offer state writes."], ["Agent Bricks", "Agents that draft next-best-action against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Network and commercial dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for outage impact and churn questions in the NOC channel."),
                    tile("Notebooks & IDEs", "notebook", "Network analytics notebooks against governed probe and CDR data."),
                ]},
                {"box": "Partner & Wholesale", "ic": "partner", "tiles": [
                    tile("Roaming Settlement API", "api", "Usage and dispute status shared to partner operators over Delta Sharing.", "gsma-tap"),
                    tile("MVNO Usage Portal", "share", "Wholesale usage and rating detail delivered to MVNO partners."),
                    tile("Tower Co SLA Feed", "globe", "Site availability and maintenance windows shared to tower companies."),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("BSS Order Provisioning", "erp", "Service orders and product changes written back to order management.", "amdocs-ces"),
                    tile("Field Work Orders", "apps", "Truck rolls and parts reservations dispatched to technician apps.", "servicemax"),
                    tile("Policy & Charging Rules", "stream", "Throttling and offer rules pushed to policy control functions."),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("Regulatory Quality Reports", "gavel", "Call completion and coverage metrics filed to the regulator."),
                    tile("Lawful Intercept Audit", "share", "Compliance evidence from governed access logs."),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Network and subscriber products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Partners reading live usage via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("NOC War Room", "Outage management", "gauge", "Live alarms, subscriber impact and restoration progress on Databricks Apps over Lakebase."),
             app("Care Agent Desktop", "Subscriber context", "custlake", "Billing, network and case history beside the ticket for first-contact resolution."),
             app("Churn Prevention Hub", "Retention offers", "market", "Propensity-scored offers and save scripts before contract expiry."),
             app("Field Dispatch Console", "Truck rolls", "people", "Technician capacity, parts and SLA risk for fibre and RAN maintenance.")],
            [uc("Churn Prediction", "Retention", "custlake", "Churn risk scored by usage, care and network quality signals."),
             uc("Network Fault Correlation", "NOC", "stream", "Alarms grouped to root cause and customer impact before truck roll."),
             uc("Capacity Forecasting", "Planning", "chart", "Cell and transport capacity forecast against traffic growth."),
             uc("Fraud Detection", "Revenue", "gavel", "SIM swap, IRSF and subscription fraud flagged before settlement."),
             uc("QoS & Dropped Calls", "Quality", "iot", "Radio and core KPIs tied to subscriber complaints and NPS."),
             uc("Offer Personalization", "Marketing", "market", "Next-best-offer scored per subscriber at renewal and in-app."),
             uc("Roaming Disputes", "Wholesale", "partner", "TAP discrepancies reconciled before partner settlement."),
             uc("Field SLA Management", "Operations", "apps", "Truck roll SLA risk predicted from parts and technician availability."),
             uc("5G Slice Orchestration", "5G", "api", "Slice SLA monitored against enterprise customer contracts."),
             uc("Energy at Cell Sites", "Sustainability", "chart", "Site power consumption optimised against traffic load.")],
        ),
        "sources": {
            "amdocs-ces": {"t": "Amdocs CES", "u": "https://www.amdocs.com/solutions/digital-business/"},
            "netcracker": {"t": "Netcracker BSS", "u": "https://www.netcracker.com/"},
            "csg": {"t": "CSG Singleview", "u": "https://www.csgi.com/products/singleview/"},
            "ericsson-enm": {"t": "Ericsson ENM", "u": "https://www.ericsson.com/en/ran/ran-automation-and-management"},
            "nokia-netact": {"t": "Nokia NetAct", "u": "https://www.nokia.com/networks/solutions/netact/"},
            "cisco-crosswork": {"t": "Cisco Crosswork", "u": "https://www.cisco.com/c/en/us/products/cloud-systems-management/crosswork-network-automation/index.html"},
            "sf-service": {"t": "Salesforce Service Cloud", "u": "https://www.salesforce.com/service/"},
            "genesys": {"t": "Genesys Cloud CX", "u": "https://www.genesys.com/"},
            "medallia": {"t": "Medallia", "u": "https://www.medallia.com/"},
            "servicemax": {"t": "ServiceMax", "u": "https://www.servicemax.com/"},
            "clicksoftware": {"t": "ClickSoftware", "u": "https://www.clicksoftware.com/"},
            "geotab": {"t": "Geotab", "u": "https://www.geotab.com/"},
            "subex": {"t": "Subex revenue assurance", "u": "https://www.subex.com/"},
            "mobileum": {"t": "Mobileum fraud management", "u": "https://www.mobileum.com/"},
            "wedo": {"t": "WeDo RAID", "u": "https://www.wedotechnologies.com/"},
            "gsma-tap": {"t": "GSMA TAP roaming", "u": "https://www.gsma.com/"},
            "tmforum": {"t": "TM Forum Open APIs", "u": "https://www.tmforum.org/"},
        },
    },
}
