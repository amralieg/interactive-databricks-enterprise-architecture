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


INDUSTRIES_BATCH_ADVERTISING = {
    'advertising': {
        "label": "Advertising",
        "blurb": "Media buying, campaign delivery, audience targeting, brand safety, and cross-channel attribution across linear, digital, and retail media.",
        "medallion": medallion(
            "Raw ad server and partner logs",
            "Impression, click, conversion and spend events from DSPs, ad servers and clean rooms, landed exactly as received so a bid or a view can be replayed for audit.",
            "Conformed campaigns and audiences",
            "Campaigns, line items, creatives and audience segments resolved into single entities across platforms, with identity graphs stitched and frequency caps reconciled.",
            "ROAS, reach and attribution",
            "Contracted products the media and finance teams run on: ROAS and CPA by channel, incremental lift, reach and frequency, and brand safety incident rates.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Ad Platforms & DSP",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "Google Campaign Manager",
                            "erp",
                            "Campaign trafficking, creative rotation and delivery reporting across display and video inventory.",
                            "google-cm360",
                        ),
                        tile(
                            "The Trade Desk",
                            "market",
                            "Programmatic buying, audience segments and bid stream across open web and CTV.",
                            "trade-desk",
                        ),
                        tile(
                            "Meta Ads Manager",
                            "partner",
                            "Paid social campaigns, creative variants and conversion events from Meta properties.",
                            "meta-ads",
                        ),
                        tile(
                            "Amazon Ads",
                            "product",
                            "Sponsored products, brands and display across retail media networks.",
                            "amazon-ads",
                        ),
                    ],
                },
                {
                    "box": "SSP & Inventory",
                    "ic": "stream",
                    "tiles": [
                        tile(
                            "Google Ad Manager",
                            "stream",
                            "Publisher ad serving, yield management and direct-sold inventory for owned media.",
                            "google-ad-manager",
                        ),
                        tile(
                            "Magnite SSP",
                            "market",
                            "Supply-side auction data, deal IDs and publisher yield across CTV and open web.",
                            "magnite",
                        ),
                        tile(
                            "Index Exchange",
                            "api",
                            "Header bidding and private marketplace bid requests for premium inventory.",
                            "index-exchange",
                        ),
                    ],
                },
                {
                    "box": "CRM & Identity",
                    "ic": "custlake",
                    "tiles": [
                        tile(
                            "Salesforce Marketing Cloud",
                            "custlake",
                            "Email, journey orchestration and first-party audience lists for activation.",
                            "sf-marketing-cloud",
                        ),
                        tile(
                            "Adobe Experience Platform",
                            "custlake",
                            "Real-time customer profiles, segments and consent state for cross-channel targeting.",
                            "adobe-aep",
                        ),
                        tile(
                            "LiveRamp RampID",
                            "partner",
                            "Identity resolution and onboarding for privacy-safe audience matching.",
                            "liveramp",
                        ),
                    ],
                },
                {
                    "box": "Measurement & Safety",
                    "ic": "chart",
                    "tiles": [
                        tile(
                            "Nielsen ONE",
                            "chart",
                            "Cross-media reach and frequency measurement across linear and digital.",
                            "nielsen-one",
                        ),
                        tile(
                            "IAS Brand Safety",
                            "gavel",
                            "Viewability, invalid traffic and brand suitability scoring on every impression.",
                            "ias",
                        ),
                        tile(
                            "AppsFlyer MMP",
                            "observ",
                            "Mobile attribution, SKAdNetwork postbacks and fraud signals.",
                            "appsflyer",
                        ),
                        tile(
                            "Kantar Brand Lift",
                            "ztarget",
                            "Survey-based brand lift studies tied to exposed and control cohorts.",
                            "kantar",
                        ),
                    ],
                },
                {
                    "box": "Creative & DAM",
                    "ic": "product",
                    "tiles": [
                        tile(
                            "Bynder DAM",
                            "product",
                            "Creative assets, rights metadata and version history for trafficking.",
                            "bynder",
                        ),
                        tile(
                            "Celtra Creative",
                            "apps",
                            "Dynamic creative optimization variants and performance by element.",
                            "celtra",
                        ),
                    ],
                },
                fed_group(
                    "Finance & Billing Mart",
                    "Agency billing, rebates and client invoicing marts left in place and queried under Unity Catalog.",
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "IAB Tech Lab OpenRTB",
                        "api",
                        "Bid request and response logs from programmatic exchanges, parsed into structured auction events.",
                        "iab-openrtb",
                    ),
                    tile(
                        "LiveRamp Data Clean Room",
                        "partner",
                        "Privacy-safe overlap and attribution queries against retailer and publisher partners.",
                        "liveramp-cleanroom",
                    ),
                    tile(
                        "Comscore Campaign Ratings",
                        "chart",
                        "Digital campaign delivery and demographic composition for guaranteed buys.",
                        "comscore",
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz("CMO & CFO Office", "Genie One",
                        "The CMO on brand share, working-media ratio and ROAS by channel; the CFO on agency fee efficiency and cost per acquisition.",
                        [["Genie One", "Ask what last quarter's ROAS was by channel without booking analyst time."],
                         ["AI/BI", "Reach, frequency and ROAS on certified Metric Views."],
                         ["Unity Catalog", "One definition of spend and conversion across platforms."]]),
                    biz("Media Planning", "AI/BI",
                        "Channel mix, flighting and budget allocation across linear, digital and retail media, judged on reach, effective CPM and incremental lift.",
                        [["Media Mix Model", "Scenario planning on incremental lift by channel."],
                         ["AI/BI", "Reach curves and budget pacing on governed data."]]),
                    biz("Performance Marketing", "Model Serving",
                        "Bid management, audience targeting and creative testing across programmatic and paid social, held to CPA, ROAS and viewability targets.",
                        [["Bid Optimizer", "Real-time bid adjustments against CPA and ROAS targets."],
                         ["Model Serving", "Conversion propensity scored in the bid path."]]),
                    biz("Brand Safety", "Lakehouse//RT",
                        "Suitability monitoring, invalid-traffic filtering and blocklists, tracked on IVT rate, viewability and brand-safety incident rate.",
                        [["Brand Safety Console", "Incidents flagged before scale is reached."],
                         ["Lakehouse//RT", "Live suitability scores at auction latency."]]),
                    biz("Finance & Billing", "AI/BI",
                        "Agency reconciliation, makegoods and client billing, watching over-pacing, rebate accruals and margin on booked media.",
                        [["AI/BI", "Spend reconciliation and variance to plan."],
                         ["Genie One", "Ask which campaigns are over-pacing without a finance pull."]]),
                ],
                [
                    biz("Data Engineers", "Lakeflow",
                        "Land the DSP bid stream, ad-server impression logs, clean-room overlaps and CRM audiences; own Bronze to Silver and the pager when pacing tables stall.",
                        [["Lakeflow Connect", "Managed connectors for ad servers, DSPs and SaaS marketing sources."],
                         ["Lakeflow Designer", "Declarative pipelines with expectations on impression and conversion feeds."],
                         ["Lakewatch", "Freshness on the pacing tables planners refresh through the day."]]),
                    biz("Data Scientists", "MLflow",
                        "Bid-optimisation, conversion-propensity, lookalike and media-mix models, and whether they still hold once cookies deprecate and channels shift.",
                        [["Feature Store", "Audience and context features read identically in training and the bidder."],
                         ["MLflow", "Every bid and lift experiment tracked for audit and reproduction."],
                         ["Model Serving", "Bid and propensity models scored inside the auction path."]]),
                    biz("App Developers", "Apps",
                        "Ship the campaign command, audience-studio and brand-safety apps the media and finance teams work in, hosted next to governed delivery data.",
                        [["Apps", "Pacing and audience screens with no separate web tier to secure."],
                         ["Lakebase", "Serverless Postgres for pacing state and blocklist writes."],
                         ["Agent Bricks", "Agents that draft budget shifts against governed tools."]]),
                ],
            ),
            "cons": cons_rail(
                [
                    {
                        "box": "BI & Productivity",
                        "ic": "chart",
                        "from": "bi",
                        "tiles": [
                            tile(
                                "Tableau / Power BI",
                                "chart",
                                "Executive and client dashboards against serverless SQL with Unity Catalog permissions.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for campaign performance answers in the channel planners already work in.",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Analyst notebooks and IDEs against governed audience and delivery data.",
                            ),
                        ],
                    },
                    {
                        "box": "Activation & Partners",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "DSP Bid Stream API",
                                "api",
                                "Optimized audiences and bid modifiers pushed back to The Trade Desk and DV360.",
                                "trade-desk",
                            ),
                            tile(
                                "Retail Media Partners",
                                "partner",
                                "Audience segments shared to Amazon, Walmart and Instacart via clean room.",
                                "amazon-ads",
                            ),
                            tile(
                                "Publisher PMP Deals",
                                "globe",
                                "Private marketplace packages activated from unified audience definitions.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "Budget Pacing Alerts",
                                "gauge",
                                "Flight-level pacing adjustments written to trafficking systems before overspend.",
                            ),
                            tile(
                                "Creative Trafficking",
                                "product",
                                "Winning creative variants pushed to ad servers for rotation.",
                                "google-cm360",
                            ),
                            tile(
                                "Blocklist Updates",
                                "gavel",
                                "Publisher and placement blocks synced to DSPs after safety incidents.",
                                "ias",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "Ad Transparency Reports",
                                "gavel",
                                "Political and issue ad disclosures filed from governed delivery tables.",
                            ),
                            tile(
                                "Client Delivery Reports",
                                "share",
                                "Guaranteed and bonus delivery reconciled for agency client billing.",
                            ),
                        ],
                    },
                    {
                        "box": "Published Products",
                        "ic": "product",
                        "tiles": [
                            tile(
                                "Data Products",
                                "product",
                                "Audience and performance products published in Unity Catalog Domains.",
                            ),
                            tile(
                                "Sharing Recipients",
                                "share",
                                "Agency and brand partners reading live tables via Delta Sharing.",
                            ),
                        ],
                    },
                ]
            ),
        },
        "top": top_band(
            [
                app(
                    "Campaign Command Center",
                    "Cross-channel pacing",
                    "gauge",
                    "Live spend, delivery and ROAS across every active flight, flagging flights that will miss guarantee before the IO closes.",
                ),
                app(
                    "Audience Studio",
                    "Segment builder",
                    "custlake",
                    "First-party segments composed from CRM, web and retail signals, ready for activation.",
                ),
                app(
                    "Brand Safety Console",
                    "Suitability monitoring",
                    "gavel",
                    "Incidents surfaced by severity with one-click blocklist propagation to buying platforms.",
                ),
                app(
                    "Media Mix Workbench",
                    "Channel planning",
                    "chart",
                    "Incremental lift scenarios by channel before the annual plan is locked.",
                ),
            ],
            [
                uc("Cross-Channel Attribution", "Measurement", "chart", "Credit assigned across linear, digital and retail touchpoints using governed identity graphs."),
                uc("Programmatic Bid Optimization", "Performance", "market", "Bids adjusted in real time against CPA, ROAS and incrementality targets."),
                uc("Audience Propensity", "Targeting", "custlake", "Lookalike and suppression audiences scored from first-party and partner signals."),
                uc("Brand Lift Measurement", "Brand", "ztarget", "Exposed versus control cohorts tied to survey lift and delivery logs."),
                uc("Frequency Management", "Reach", "stream", "Cross-platform frequency caps enforced before waste accumulates."),
                uc("Retail Media Activation", "Commerce", "product", "Sponsored search and display tuned against on-shelf availability."),
                uc("Creative DCO", "Creative", "apps", "Dynamic elements swapped by audience segment and performance."),
                uc("Fraud & IVT Detection", "Quality", "gavel", "Invalid traffic removed before it bills or pollutes attribution."),
                uc("Agency Reconciliation", "Finance", "erp", "Delivery, makegoods and rebates reconciled to contracted IO terms."),
                uc("Privacy-Safe Clean Rooms", "Identity", "partner", "Overlap and attribution computed without raw PII leaving either party."),
            ],
        ),
        "sources": {
            "google-cm360": {"t": "Google Campaign Manager 360", "u": "https://marketingplatform.google.com/about/campaign-manager-360/"},
            "trade-desk": {"t": "The Trade Desk", "u": "https://www.thetradedesk.com/"},
            "meta-ads": {"t": "Meta Ads Manager", "u": "https://www.facebook.com/business/tools/ads-manager"},
            "amazon-ads": {"t": "Amazon Ads", "u": "https://advertising.amazon.com/"},
            "google-ad-manager": {"t": "Google Ad Manager", "u": "https://admanager.google.com/"},
            "magnite": {"t": "Magnite SSP", "u": "https://www.magnite.com/"},
            "index-exchange": {"t": "Index Exchange", "u": "https://www.indexexchange.com/"},
            "sf-marketing-cloud": {"t": "Salesforce Marketing Cloud", "u": "https://www.salesforce.com/products/marketing-cloud/"},
            "adobe-aep": {"t": "Adobe Experience Platform", "u": "https://business.adobe.com/products/experience-platform/adobe-experience-platform.html"},
            "liveramp": {"t": "LiveRamp", "u": "https://liveramp.com/"},
            "nielsen-one": {"t": "Nielsen ONE", "u": "https://www.nielsen.com/solutions/nielsen-one/"},
            "ias": {"t": "Integral Ad Science", "u": "https://integralads.com/"},
            "appsflyer": {"t": "AppsFlyer", "u": "https://www.appsflyer.com/"},
            "kantar": {"t": "Kantar", "u": "https://www.kantar.com/"},
            "bynder": {"t": "Bynder DAM", "u": "https://www.bynder.com/"},
            "celtra": {"t": "Celtra", "u": "https://www.celtra.com/"},
            "iab-openrtb": {"t": "IAB OpenRTB", "u": "https://iabtechlab.com/standards/openrtb/"},
            "liveramp-cleanroom": {"t": "LiveRamp Data Collaboration", "u": "https://liveramp.com/data-collaboration/"},
            "comscore": {"t": "Comscore", "u": "https://www.comscore.com/"},
        },
    },
}
