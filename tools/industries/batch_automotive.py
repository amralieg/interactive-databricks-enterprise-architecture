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


INDUSTRIES_BATCH_AUTOMOTIVE = {
    'automotive': {
        "label": "Automotive",
        "blurb": "Vehicle design, manufacturing, dealer networks, connected services, and aftersales across OEMs, tier suppliers, and mobility fleets.",
        "medallion": medallion(
            "Raw plant and vehicle feeds",
            "MES, telematics, dealer DMS and warranty claims landed exactly as received so a VIN lifecycle can be replayed.",
            "Conformed vehicles and parts",
            "VINs, BOMs, dealers and service events resolved into single entities across engineering, plant and retail systems.",
            "Quality, throughput, loyalty",
            "Contracted products operations and sales run on: plant OEE, defect PPM, days supply and service retention.",
        ),
        "rails": {
            "src": [
                {"box": "Engineering & PLM", "ic": "product", "tiles": [
                    tile("Siemens Teamcenter", "product", "EBOM, change orders and variant configuration through SOP.", "teamcenter"),
                    tile("Dassault 3DEXPERIENCE", "product", "CAD, simulation and manufacturing process definitions.", "3dexperience"),
                    tile("PTC Windchill", "product", "Part masters, effectivity and supplier packages.", "windchill"),
                ]},
                {"box": "Manufacturing MES", "ic": "iot", "tiles": [
                    tile("Siemens Opcenter", "iot", "Line sequencing, torque traces, andon events by station.", "opcenter"),
                    tile("Rockwell FactoryTalk", "iot", "PLC tags, quality checks and downtime reason codes.", "factorytalk"),
                    tile("Bosch Nexeed", "stream", "Tier-1 JIT sequencing and logistics for assembly plants.", "nexeed"),
                ]},
                {"box": "Dealer & Retail", "ic": "market", "tiles": [
                    tile("CDK Global DMS", "erp", "Dealer inventory, deals, F&I and service ROs.", "cdk"),
                    tile("Reynolds ERA", "erp", "Retail, parts and service transactions across dealer groups.", "reynolds"),
                    tile("VinSolutions CRM", "custlake", "Leads, appointments and sold-not-reported tracking.", "vinsolutions"),
                ]},
                {"box": "Connected Vehicle", "ic": "stream", "tiles": [
                    tile("OEM Telematics Gateway", "iot", "CAN signals, GPS and remote diagnostics from connected fleets.", "telematics"),
                    tile("HERE HD Maps", "globe", "Lane-level map tiles for ADAS and navigation features.", "here-maps"),
                    tile("Aptiv Smart Vehicle", "zplug", "Sensor fusion and software-defined feature telemetry.", "aptiv"),
                ]},
                {"box": "Aftersales & Parts", "ic": "zplug", "tiles": [
                    tile("SAP Aftermarket", "erp", "Parts catalog, supersession and dealer ordering.", "sap-aftermarket"),
                    tile("Mitchell Repair", "product", "Labor guides, TSBs and repair procedures.", "mitchell"),
                ]},
                fed_group("Finance & Warranty Mart", "Warranty accrual and revenue recognition marts queried in place under Unity Catalog."),
            ],
            "ing": ing_rail([
                tile("JD Power IQS/SSI", "chart", "Initial quality and sales satisfaction benchmarks by segment.", "jdpower"),
                tile("Polk Registration", "market", "Vehicle registration and conquest data by geography.", "polk"),
                tile("UNECE WP.29 R155", "gavel", "Cybersecurity and software update compliance telemetry.", "unece-r155"),
            ]),
            "ppl": ppl2([
                biz("CEO & Mfg COO", "Genie One",
                    "The CEO on market share and program ROI; the COO on plant OEE, first-time-through quality and defect PPM against the launch curve by line.",
                    [["Genie One", "Ask what last month's plant OEE was by line."], ["AI/BI", "Quality and throughput on certified Metric Views."], ["Unity Catalog", "One VIN definition across plant and dealer."]]),
                biz("Manufacturing", "Lakehouse//RT",
                    "Line balancing, andon response and launch curve tracking, run on OEE, cycle time and bottleneck-station losses against takt.",
                    [["Plant Cockpit", "Live OEE and bottleneck stations on the floor."], ["Lakehouse//RT", "Torque and vision checks at line latency."]]),
                biz("Quality Engineering", "AI/BI",
                    "Defect pareto, supplier PPM and containment across plants, tracked on warranty cost per vehicle, scrap rate and time-to-containment.",
                    [["Quality Command", "Emerging defect trends before field campaigns."], ["AI/BI", "PPM and scrap on governed inspection data."]]),
                biz("Sales & Marketing", "Model Serving",
                    "Incentive planning, conquest targeting and digital lead scoring, judged on incentive spend per unit, conquest rate and margin.",
                    [["Incentive Optimizer", "Program spend against margin guardrails."], ["Model Serving", "Lead scores in the CRM routing path."]]),
                biz("Aftersales", "Apps",
                    "Service retention, parts availability and warranty recovery, measured on retention rate, parts fill rate and chargeback recovery.",
                    [["Service Advisor App", "Next-best service offers on governed vehicle history."], ["Apps", "Dealer tools hosted next to governed data."]]),
            ], [
                biz("Data Engineers", "Lakeflow",
                    "Land MES torque traces, telematics CAN signals, dealer DMS and warranty claims; own Bronze to Silver and the pager when the OEE tables stall.",
                    [["Lakeflow Connect", "Managed connectors for MES, ERP and dealer DMS sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on line and telematics feeds."], ["Lakewatch", "Freshness on the OEE and quality tables the plant reads each shift."]]),
                biz("Data Scientists", "MLflow",
                    "Predictive-quality, remaining-useful-life, lead-scoring and incentive models, and whether they still hold across a model-year changeover.",
                    [["Feature Store", "VIN and station features read identically in training and serving."], ["MLflow", "Every quality and RUL model tracked for audit and reproduction."], ["Model Serving", "Quality and lead models scored in the line and CRM path."]]),
                biz("App Developers", "Apps",
                    "Ship the plant cockpit, quality command, incentive optimizer and service advisor apps operations and dealers work in, next to governed VIN data.",
                    [["Apps", "Plant and dealer screens with no separate web tier to secure."], ["Lakebase", "Serverless Postgres for line and service-advisor state."], ["Agent Bricks", "Agents that draft containment and work orders against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Power BI", "chart", "Plant and regional sales dashboards on serverless SQL."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for quality and inventory in plant channels."),
                    tile("Notebooks & IDEs", "notebook", "Engineering notebooks against governed BOM and telemetry."),
                ]},
                {"box": "Dealer & Partners", "ic": "partner", "tiles": [
                    tile("Dealer Inventory Feed", "api", "Days supply and allocation pushed to DMS nightly.", "cdk"),
                    tile("OTA Update Channel", "iot", "Software campaigns delivered to connected VINs.", "telematics"),
                    tile("Supplier Portal", "zplug", "ASN and quality alerts shared with tier-1 suppliers.", "nexeed"),
                ]},
                {"box": "Operational Writeback", "ic": "opdb", "tiles": [
                    tile("Line Sequencing", "stream", "Re-sequenced build orders sent to MES after disruption."),
                    tile("Recall Campaign List", "gavel", "Affected VINs pushed to dealer service systems."),
                    tile("Parts Allocation", "product", "Scarce parts prioritized to high-value ROs.", "sap-aftermarket"),
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("NHTSA Reporting", "gavel", "Safety defects and recall filings from governed case data."),
                    tile("EU CO2 Fleet Targets", "share", "Fleet emissions reported to regulators.", "unece-r155"),
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Vehicle and quality products in Unity Catalog Domains."),
                    tile("Sharing Recipients", "share", "Suppliers and finance partners via Delta Sharing."),
                ]},
            ]),
        },
        "top": top_band(
            [app("Plant Cockpit", "Line OEE", "gauge", "Live throughput, andon state and bottleneck stations across assembly lines."),
             app("Quality Command", "Defect intelligence", "gavel", "Emerging defect clusters flagged before field campaigns are required."),
             app("Incentive Optimizer", "Program planning", "market", "Regional incentive spend modeled against margin and conquest targets."),
             app("Service Advisor App", "Aftersales", "custlake", "Next-best service and retention offers on governed vehicle history.")],
            [uc("Predictive Quality", "Manufacturing", "iot", "Torque and vision anomalies predicted before vehicles leave the station."),
             uc("Launch Curve Tracking", "Program", "sheet", "Build and quality ramp against SOP targets by week."),
             uc("Connected Diagnostics", "Telematics", "stream", "Remote fault prediction triggering proactive service offers."),
             uc("Warranty Recovery", "Aftersales", "erp", "Supplier chargebacks matched to field failure modes."),
             uc("Dealer Inventory Opt", "Retail", "market", "Allocation and days supply tuned by market demand."),
             uc("OTA Campaign Mgmt", "Software", "api", "Feature rollouts and recalls delivered over the air."),
             uc("Supplier PPM", "Quality", "zplug", "Incoming quality scored and ranked across the supply base."),
             uc("Conquest Marketing", "Sales", "custlake", "Competitive owners targeted with governed registration data."),
             uc("Parts Forecasting", "Aftersales", "product", "Dealer and DC parts stock against failure curves."),
             uc("EV Battery Health", "Mobility", "iot", "State of health scored for resale and fleet redeployment.")],
        ),
        "sources": {
            "teamcenter": {"t": "Siemens Teamcenter", "u": "https://plm.sw.siemens.com/en-US/teamcenter/"},
            "3dexperience": {"t": "Dassault 3DEXPERIENCE", "u": "https://www.3ds.com/3dexperience"},
            "windchill": {"t": "PTC Windchill", "u": "https://www.ptc.com/en/products/windchill"},
            "opcenter": {"t": "Siemens Opcenter", "u": "https://plm.sw.siemens.com/en-US/opcenter/"},
            "factorytalk": {"t": "Rockwell FactoryTalk", "u": "https://www.rockwellautomation.com/en-us/products/software/factorytalk.html"},
            "nexeed": {"t": "Bosch Nexeed", "u": "https://www.bosch-connected-industry.com/"},
            "cdk": {"t": "CDK Global", "u": "https://www.cdkglobal.com/"},
            "reynolds": {"t": "Reynolds and Reynolds", "u": "https://www.reyrey.com/"},
            "vinsolutions": {"t": "VinSolutions", "u": "https://www.vinsolutions.com/"},
            "telematics": {"t": "Connected vehicle telematics", "u": "https://www.sae.org/standards/content/j3016_202104/"},
            "here-maps": {"t": "HERE Technologies", "u": "https://www.here.com/platform"},
            "aptiv": {"t": "Aptiv", "u": "https://www.aptiv.com/"},
            "sap-aftermarket": {"t": "SAP Automotive", "u": "https://www.sap.com/industries/automotive.html"},
            "mitchell": {"t": "Mitchell International", "u": "https://www.mitchell.com/"},
            "jdpower": {"t": "J.D. Power", "u": "https://www.jdpower.com/business/automotive"},
            "polk": {"t": "S&P Global Mobility Polk", "u": "https://www.spglobal.com/mobility/"},
            "unece-r155": {"t": "UNECE WP.29 R155", "u": "https://unece.org/transport/documents/2021/03/standards/un-regulation-no-155-cyber-security-and-cyber-security"},
        },
    },
}
