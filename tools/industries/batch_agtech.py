import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_AGTECH = {
    "agtech": {
        "label": "AgTech",
        "blurb": "Agriculture technology vendors: precision-ag platforms, farm-management software, equipment telematics, satellite and sensor networks, crop-science R&D, and sustainability programs.",
        "medallion": medallion(
            "Raw field & fleet feeds",
            "Machine telemetry off the CAN bus, satellite and drone imagery tiles, weather-station and soil-probe readings, agronomy trial and lab results, and FMS field boundaries landed exactly as received, so a yield map or a spray pass can always be replayed as it stood.",
            "Conformed field, grower, machine",
            "Fields, growers, crops, seasons and machines resolved into single conformed entities across the FMS, telematics, imagery and agronomy estates, with field boundaries reconciled to a common geometry and trial plots stitched to their protocols.",
            "Yield, agronomy, sustainability",
            "Contracted products the agronomy, product and sustainability teams run on: yield and vegetation index by field and hybrid, variable-rate prescription performance, machine uptime and utilisation, and verified carbon and practice-change outcomes by supply shed.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Farm Mgmt Platforms",
                    "ic": "appbuilder",
                    "tiles": [
                        tile(
                            "Climate FieldView",
                            "appbuilder",
                            "Bayer's digital farming platform and the system of record for connected field data: planting, application and harvest layers synced off the FieldView Drive across tens of millions of acres.",
                            "fieldview",
                        ),
                        tile(
                            "JD Operations Center",
                            "apps",
                            "John Deere's farm-management hub: fields, jobs, guidance lines and agronomic layers, the offboard home for the data machines generate in the field.",
                            "jd-opscenter",
                        ),
                        tile(
                            "Trimble Ag Software",
                            "sheet",
                            "Precision-ag field records, mapping and prescription authoring used across mixed-fleet operations, feeding boundaries and as-applied data into the estate.",
                            "trimble-ag",
                        ),
                        tile(
                            "Granular by Corteva",
                            "product",
                            "Farm business and agronomy software from Corteva: field operations, financials and input planning tied to the seed and crop-protection catalogue.",
                            "granular",
                        ),
                    ],
                },
                {
                    "box": "Equipment Telematics",
                    "ic": "iot",
                    "tiles": [
                        tile(
                            "JDLink Telematics",
                            "iot",
                            "John Deere machine connectivity: position, engine, implement and as-applied telemetry streamed off the machine into the Operations Center and the data platform.",
                            "jdlink",
                        ),
                        tile(
                            "CNH AFS Connect",
                            "iot",
                            "Case IH and New Holland fleet telematics and remote display access: machine health, location and agronomic data across the CNH equipment estate.",
                            "cnh-afs",
                        ),
                        tile(
                            "AGCO Fuse",
                            "stream",
                            "AGCO's smart-farming connectivity across Fendt, Massey Ferguson and Valtra: mixed-fleet machine and agronomic data brought together for the operation.",
                            "agco-fuse",
                        ),
                        tile(
                            "ISOBUS Task Data",
                            "connect",
                            "The ISO 11783 in-cab standard for task controllers and implement data: as-applied logs and prescriptions exchanged between terminal and machine, parsed on arrival.",
                            "isobus",
                        ),
                    ],
                },
                {
                    "box": "Imagery & Remote Sensing",
                    "ic": "globe",
                    "tiles": [
                        tile(
                            "Planet Imagery",
                            "globe",
                            "Daily high-cadence satellite imagery over every field, the raster source behind vegetation-index time series and in-season crop monitoring.",
                            "planet",
                        ),
                        tile(
                            "Sentinel Hub",
                            "globe",
                            "Copernicus Sentinel-2 and Landsat archive access with on-the-fly processing, the free-tier backbone for NDVI and change-detection layers.",
                            "sentinelhub",
                        ),
                        tile(
                            "DJI Ag Drones",
                            "media",
                            "Low-altitude drone imagery and multispectral capture for scouting and trial plots, landed as high-resolution rasters alongside the satellite feeds.",
                            "dji-ag",
                        ),
                        tile(
                            "Descartes Labs",
                            "network",
                            "Analysis-ready geospatial data and remote-sensing models over large areas, used for regional crop and yield signals.",
                            "descartes",
                        ),
                    ],
                },
                {
                    "box": "Weather & Field Sensors",
                    "ic": "iot",
                    "tiles": [
                        tile(
                            "DTN Weather",
                            "stream",
                            "Hyper-local forecasts, historical weather and field-level conditions, the meteorology layer behind spray windows, disease risk and yield modelling.",
                            "dtn",
                        ),
                        tile(
                            "CropX Soil Probes",
                            "iot",
                            "In-ground soil moisture, temperature and salinity sensors feeding irrigation and nutrient decisions at the root zone.",
                            "cropx",
                        ),
                        tile(
                            "Semios IoT Network",
                            "network",
                            "In-canopy pest, disease and microclimate sensors for permanent crops, streamed as time series for scouting and spray timing.",
                            "semios",
                        ),
                        tile(
                            "Pessl METOS Stations",
                            "iot",
                            "Field weather stations and disease-model dataloggers from Pessl Instruments, the on-farm ground truth calibrating remote signals.",
                            "metos",
                        ),
                    ],
                },
                {
                    "box": "R&D, Agronomy & ERP",
                    "ic": "erp",
                    "tiles": [
                        tile(
                            "Cropwise Agronomy",
                            "sheet",
                            "Syngenta's digital agronomy suite: field scouting, agronomic recommendations and product performance tied to the crop-protection portfolio.",
                            "cropwise",
                        ),
                        tile(
                            "LabWare LIMS",
                            "docs",
                            "The laboratory information management system of record for seed, trait and crop-protection R&D: sample results, assays and study data.",
                            "labware",
                        ),
                        tile(
                            "SAP S/4HANA",
                            "erp",
                            "The commercial system of record for the ag vendor: orders, inventory, dealer settlements and the input supply chain behind the products in the field.",
                            "sap-s4",
                        ),
                        tile(
                            "DSSAT & APSIM Models",
                            "model",
                            "Crop-simulation frameworks turning weather, soil and genetics into growth-stage and yield estimates, run at scale against the conformed field data.",
                            "dssat",
                        ),
                    ],
                },
                fed_group(
                    "Commercial Data Mart",
                    "Legacy commercial, dealer and R&D data marts left where they are and queried in place under Unity Catalog, which avoids a second copy of numbers still under retention and contract.",
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "AgGateway ADAPT",
                        "connect",
                        "The industry data-interoperability framework and plugins that normalise as-applied, prescription and setup files across mixed equipment brands.",
                        "adapt",
                    ),
                    tile(
                        "Leaf Ag API",
                        "api",
                        "A unified API over FieldView, Operations Center, CNH and other providers, pulling machine and field data through one governed connector.",
                        "leaf",
                    ),
                    tile(
                        "Machine Event Streams",
                        "eventbus",
                        "Existing Kafka and MQTT topics carrying live machine, sensor and gateway events, landed generically as structured streaming tables.",
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Digital Product",
                        "Genie One",
                        "The leaders of the digital ag platform: the chief digital officer and precision-ag product managers who own FieldView, Operations Center and the grower and agronomist experience, and the platform GM who answers for adoption and connected acres.",
                        [
                            ["Genie One", "Ask how many acres synced last week or which prescription workflow is stalling without booking analyst time."],
                            ["AI/BI", "Connected acres, feature adoption and platform reliability on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the glossary, so \"active acre\" and \"as-applied\" mean one thing across the platform."],
                        ],
                        sub=[
                            ["Chief Digital Officer", "the digital farming strategy and the connected-acre growth target."],
                            ["Precision Ag Product", "FieldView and Operations Center feature adoption and grower retention."],
                            ["Platform GM", "reliability, partner integrations and the data-sharing ecosystem."],
                        ],
                        ucs=["FMS Platform", "VRA Prescriptions", "Imagery at Scale"],
                    ),
                    biz(
                        "Agronomy & R&D",
                        "AI/BI",
                        "The crop scientists and agronomists: seed and crop-protection R&D running multi-year trials, field research turning plots into product claims, and the agronomy advisory team standing behind the recommendations growers act on.",
                        [
                            ["AI/BI", "Trial results, product performance and agronomic signals on governed, certified data."],
                            ["Model Serving", "Yield, pest and disease models scored into the products agronomists use."],
                            ["Genie One", "Ask how a hybrid performed by geography or which trials are ready to read without an analyst pull."],
                        ],
                        sub=[
                            ["Crop Science R&D", "seed, trait and crop-protection discovery and development pipelines."],
                            ["Field Trials", "multi-location protocols and the statistics behind product claims."],
                            ["Agronomy Advisory", "the recommendations and prescriptions growers act on in season."],
                        ],
                        ucs=["Yield Prediction", "Crop R&D Analytics", "Pest & Disease"],
                    ),
                    biz(
                        "Equipment Eng",
                        "Lakehouse//RT",
                        "The OEM engineering side: telematics engineers landing machine telemetry at fleet scale, reliability engineers on component life and in-season uptime, and the autonomy and guidance teams building the systems that steer and spray the machine.",
                        [
                            ["Lakehouse//RT", "Live machine and implement state at the latency an in-season fleet moves at."],
                            ["Model Serving", "Remaining-life and anomaly models scored against streaming telemetry."],
                            ["Apache Spark", "Petabyte-scale geospatial and telemetry processing across the connected fleet."],
                        ],
                        sub=[
                            ["Telematics Engineering", "machine, implement and as-applied telemetry off the CAN bus."],
                            ["Machine Reliability", "component life, warranty and in-season uptime."],
                            ["Autonomy & Guidance", "steering, See & Spray and the perception data behind them."],
                        ],
                        ucs=["Fleet Telematics", "Predictive Uptime", "VRA Prescriptions"],
                    ),
                    biz(
                        "Sustainability",
                        "Model Serving",
                        "The teams behind the carbon and stewardship programs: carbon program operators enrolling acres, the MRV and verification team standing behind every credit, and regenerative-ag leads proving practice change across the supply shed.",
                        [
                            ["Model Serving", "Soil-carbon and emissions models scored against imagery and practice data."],
                            ["Unity Catalog", "Auditable lineage from field practice to reported credit under one governance model."],
                            ["AI/BI", "Enrolled acres, practice adoption and verified outcomes on certified views."],
                        ],
                        sub=[
                            ["Carbon Programs", "enrolment, baselining and grower payments across the supply shed."],
                            ["MRV & Verification", "measurement, reporting and verification behind every issued credit."],
                            ["Regenerative Ag", "cover crops, tillage and the practice-change evidence base."],
                        ],
                        ucs=["Carbon MRV", "Traceability", "Imagery at Scale"],
                    ),
                    biz(
                        "Commercial",
                        "AI/BI",
                        "The go-to-market side: the dealer and channel network selling and servicing equipment and inputs, grower-success teams on retention and expansion, and input supply and pricing balancing demand against the season.",
                        [
                            ["AI/BI", "Dealer performance, grower retention and input demand on certified Metric Views."],
                            ["Genie One", "Ask which dealers are trending down or where input demand is spiking without a finance pull."],
                            ["Model Serving", "Churn, demand and cross-sell models scored into the commercial workflow."],
                        ],
                        sub=[
                            ["Dealer Network", "channel performance, parts and service revenue."],
                            ["Grower Success", "onboarding, retention and expansion on the platform."],
                            ["Input Supply & Pricing", "seed and crop-protection demand against the season."],
                        ],
                        ucs=["Traceability", "Fleet Telematics", "FMS Platform"],
                    ),
                ],
                [
                    biz(
                        "Geospatial Eng",
                        "Lakeflow",
                        "Land the imagery, boundary and telemetry feeds from Planet, Sentinel, JDLink and ISOBUS; own the raster-to-tabular path with GDAL, rasterio and H3, and the pager when a tile or telemetry feed stalls.",
                        [
                            ["Lakeflow Connect", "Managed connectors for FMS, telematics and imagery providers."],
                            ["Apache Spark", "Mosaic and Spatial SQL H3 indexing turning rasters into governed tables."],
                            ["Lakewatch", "Freshness on the field and fleet tables agronomists read every morning."],
                        ],
                        ucs=["Imagery at Scale", "Yield Prediction", "Fleet Telematics"],
                    ),
                    biz(
                        "Ag Data Science",
                        "MLflow",
                        "Yield, pest, disease and remaining-life models built on remote-sensing computer vision, crop simulations and telemetry, and whether they still hold a season after deployment.",
                        [
                            ["Feature Store", "Field, weather and machine features read identically in training and serving."],
                            ["MLflow", "Every run tracked for audit and reproduction across seasons and geographies."],
                            ["Model Serving", "Yield, pest and uptime models scored in the product and operational path."],
                        ],
                        ucs=["Yield Prediction", "Pest & Disease", "Predictive Uptime"],
                    ),
                    biz(
                        "App & IoT Eng",
                        "Apps",
                        "Ship the grower, agronomist and dealer applications and the ingestion behind millions of connected machines, hosted next to governed data.",
                        [
                            ["Apps", "Grower and dealer screens with no separate web tier to run or secure."],
                            ["Lakebase", "Serverless Postgres for prescription, workflow and roster state with governed writes."],
                            ["Zerobus", "High-volume machine and sensor events ingested directly to the lakehouse."],
                        ],
                        ucs=["Fleet Telematics", "FMS Platform", "VRA Prescriptions"],
                    ),
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
                                "Product, agronomy and commercial dashboards against serverless SQL with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for Unity Catalog-governed answers in the channel product and agronomy teams already work in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Data-scientist notebooks, VS Code and JetBrains against governed field, imagery and telemetry data.",
                            ),
                        ],
                    },
                    {
                        "box": "Grower & Dealer Apps",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "FMS Grower Apps",
                                "apps",
                                "The grower and agronomist mobile and web apps served next to governed data on Databricks Apps over Lakebase.",
                                "fieldview",
                            ),
                            tile(
                                "Dealer Portals",
                                "globe",
                                "Equipment and input dealer portals reading machine health, parts demand and grower activity from certified products.",
                            ),
                            tile(
                                "Genie for Agronomists",
                                "genie",
                                "Plain-language answers on hybrid performance, disease risk and field history grounded in governed data.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "VRA Writeback",
                                "db",
                                "Variable-rate seeding and nutrient prescriptions written back into the FMS and machine terminal so the answer reaches the field.",
                                "fieldview",
                            ),
                            tile(
                                "Telematics Alerts",
                                "stream",
                                "Predicted faults and service needs pushed to dealer service and the machine's connected display before the failure lands.",
                                "jdlink",
                            ),
                            tile(
                                "Agronomy Recs",
                                "sheet",
                                "Scouting and product recommendations synced back into the agronomy apps advisors work in.",
                                "cropwise",
                            ),
                        ],
                    },
                    {
                        "box": "Sustainability & Reg",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "Carbon Registry",
                                "gavel",
                                "Practice-change and soil-carbon evidence filed to the registry from the same governed tables the program runs on.",
                                "verra",
                            ),
                            tile(
                                "EUDR Traceability",
                                "share",
                                "Deforestation-free due-diligence and geolocation evidence produced for the EU Deforestation Regulation from governed provenance data.",
                                "eudr",
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
                                "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing.",
                            ),
                            tile(
                                "Sharing Recipients",
                                "share",
                                "Growers, food and CPG partners and regulators reading live tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ]
            ),
        },
        "top": top_band(
            [
                app(
                    "Field Insights Hub",
                    "Agronomy view",
                    "gauge",
                    "The screen agronomists and product teams run a field from: yield, vegetation index, soil and weather layers stitched to the boundary, on Databricks Apps over Lakebase so a recommendation reaches the grower app.",
                ),
                app(
                    "Fleet Watchtower",
                    "Machine health",
                    "iot",
                    "Connected-fleet health and utilisation by machine and region, so engineering and dealers plan a service before an in-season breakdown costs a planting or harvest window.",
                ),
                app(
                    "Prescription Studio",
                    "Variable-rate ag",
                    "sheet",
                    "Where variable-rate seeding and nutrient prescriptions are built from conformed field data and pushed to the FMS and machine terminal in the ISOBUS format the implement reads.",
                ),
                app(
                    "Carbon MRV Console",
                    "Sustainability",
                    "gavel",
                    "Where the sustainability team baselines acres, scores practice change against imagery and models, and assembles the audit trail behind every carbon credit.",
                ),
            ],
            [
                uc(
                    "FMS Platform",
                    "Digital ag",
                    "appbuilder",
                    "Unifying connected field, machine and agronomy data into the farm-management platform at scale, so growers and advisors see one governed view of the operation.",
                    problem="Field, machine and agronomy data arrive from dozens of brands and formats, so the platform stitches them by hand and every new source is a bespoke integration project.",
                    who="Digital Product",
                    how="FMS, telematics and imagery feeds land through Lakeflow and are conformed on Delta Lake under Unity Catalog, giving the platform one governed field-and-grower model to build features on.",
                    comps=["Field Insights Hub", "Climate FieldView", "Lakeflow", "Unity Catalog", "Delta Lake"],
                    stories=[
                        ["Bayer transforms global data management with Databricks", "https://www.databricks.com/customers/bayer"],
                        ["Accelerating Corteva's data source onboarding with Lakeflow", "https://www.databricks.com/dataaisummit/session/accelerating-cortevas-data-source-onboarding-lakeflow"],
                    ],
                ),
                uc(
                    "Yield Prediction",
                    "Agronomy",
                    "chart",
                    "Predicting field and hybrid yield from imagery, weather, soil and management history, so agronomists and growers act on a forecast rather than last year's average.",
                    problem="Yield is estimated from spotty history and gut feel, so agronomic and commercial decisions are made without a defensible forecast per field and hybrid.",
                    who="Agronomy & R&D",
                    how="Imagery, weather and soil features are engineered in Feature Store and scored through Model Serving, with runs tracked in MLflow for audit across seasons and geographies.",
                    comps=["Field Insights Hub", "Model Serving", "MLflow", "Planet Imagery", "Feature Store"],
                    stories=[
                        ["Agerpoint partners with Databricks for agriculture data intelligence", "https://www.agerpoint.com/blog/agerpoint-partners-with-databricks-to-scale-enterprise-data-intelligence-for-agriculture-and-nature-systems"],
                    ],
                ),
                uc(
                    "Crop R&D Analytics",
                    "Product dev",
                    "notebook",
                    "Unifying lab, trial, imagery and field data so crop-science R&D reads results in minutes and shortens the multi-year path from discovery to a product claim.",
                    problem="R&D data is siloed across countries, labs and legacy systems, so scientists wait months for insights and the eight-to-twelve-year development cycle stretches further.",
                    who="Agronomy & R&D",
                    how="Lab, trial and imagery data are conformed into governed data products under Unity Catalog and explored in AI/BI and Genie, cutting access time from months to minutes.",
                    comps=["LabWare LIMS", "Unity Catalog", "AI/BI", "Delta Lake", "Genie One"],
                    stories=[
                        ["Syngenta accelerates crop protection research with Gaia", "https://www.databricks.com/customers/syngenta"],
                        ["FMC optimizes harvests with data and AI", "https://www.databricks.com/customers/fmc-corporation"],
                    ],
                ),
                uc(
                    "Fleet Telematics",
                    "Equipment",
                    "iot",
                    "Ingesting machine and implement telemetry at petabyte scale so the OEM turns raw CAN-bus feeds into engineering, service and agronomic insight.",
                    problem="Machine data doubles or triples each year, and legacy stores cannot ingest and geospatially analyse it fast enough to feed engineering, sales and service teams.",
                    who="Equipment Eng",
                    how="Telemetry streams into Lakehouse//RT and is processed with Apache Spark and H3 indexing on Delta Lake, giving every downstream team one scalable view of the connected fleet.",
                    comps=["Fleet Watchtower", "JDLink Telematics", "Lakehouse//RT", "Apache Spark", "Delta Lake"],
                    stories=[
                        ["How John Deere uses industrial AI for precision agriculture", "https://www.databricks.com/blog/2021/07/09/down-to-the-individual-grain-how-john-deere-uses-industrial-ai-to-increase-crop-yields-through-precision-agriculture.html"],
                        ["CNH analyzes geospatial data to improve crop outputs", "https://www.databricks.com/customers/cnh"],
                    ],
                ),
                uc(
                    "Predictive Uptime",
                    "Machine health",
                    "gauge",
                    "Predicting component failure on connected machines so a service is planned at the dealer instead of discovered mid-harvest.",
                    problem="A breakdown in a planting or harvest window costs the grower the season, yet failures are found after the machine stops rather than predicted from its own telemetry.",
                    who="Equipment Eng",
                    how="Streaming telemetry feeds remaining-life and anomaly models tracked in MLflow and scored in Model Serving, so predicted faults raise service alerts from the Fleet Watchtower.",
                    comps=["Fleet Watchtower", "Model Serving", "MLflow", "CNH AFS Connect", "Lakehouse//RT"],
                    stories=[
                        ["How John Deere uses industrial AI for precision agriculture", "https://www.databricks.com/blog/2021/07/09/down-to-the-individual-grain-how-john-deere-uses-industrial-ai-to-increase-crop-yields-through-precision-agriculture.html"],
                        ["What is predictive maintenance on the Databricks platform", "https://www.databricks.com/blog/what-is-predictive-maintenance"],
                    ],
                ),
                uc(
                    "VRA Prescriptions",
                    "Precision ag",
                    "sheet",
                    "Building variable-rate seeding and nutrient prescriptions from conformed field data and pushing them to the machine in the format the implement reads.",
                    problem="Prescriptions are authored in one tool and executed in another, so field data, agronomic models and the machine terminal rarely line up and rates default to flat.",
                    who="Digital Product",
                    how="Field, soil and yield layers are scored with AI Functions and Model Serving in Prescription Studio, then written back to FieldView and the ISOBUS task controller.",
                    comps=["Prescription Studio", "Model Serving", "Climate FieldView", "ISOBUS Task Data", "AI Functions"],
                    stories=[
                        ["How John Deere uses industrial AI for precision agriculture", "https://www.databricks.com/blog/2021/07/09/down-to-the-individual-grain-how-john-deere-uses-industrial-ai-to-increase-crop-yields-through-precision-agriculture.html"],
                    ],
                ),
                uc(
                    "Pest & Disease",
                    "Scouting",
                    "globe",
                    "Detecting pest and disease pressure from imagery, traps and weather so growers intervene on the acres at risk before an infestation spreads.",
                    problem="Infestations are found on foot after they establish, and the geospatial and weather signals that would flag them early sit in disconnected systems.",
                    who="Agronomy & R&D",
                    how="Vision models on trap and imagery data are enriched with weather and location features in Feature Store and scored in Model Serving to anticipate where pressure will emerge.",
                    comps=["Model Serving", "Planet Imagery", "DTN Weather", "Feature Store", "AI Functions"],
                    stories=[
                        ["FMC optimizes harvests with data and AI (Arc farm intelligence)", "https://www.databricks.com/customers/fmc-corporation"],
                    ],
                ),
                uc(
                    "Imagery at Scale",
                    "Remote sensing",
                    "globe",
                    "Turning daily satellite and drone rasters into governed, query-ready analytics with H3 indexing, without an expensive legacy GIS in the middle.",
                    problem="Raster imagery is slow and costly to process, so vegetation-index and change layers arrive too late and only a GIS specialist can touch them.",
                    who="Digital Product",
                    how="Rasters are H3-indexed into tabular Delta with Apache Spark and Spatial SQL, so imagery joins field and weather data and anyone can query it in AI/BI.",
                    comps=["Planet Imagery", "Sentinel Hub", "Apache Spark", "Delta Lake", "AI/BI"],
                    stories=[
                        ["CNH analyzes geospatial data to improve crop outputs", "https://www.databricks.com/customers/cnh"],
                        ["Built-in H3 for geospatial analytics", "https://www.databricks.com/blog/announcing-built-h3-expressions-geospatial-processing-and-analytics"],
                    ],
                ),
                uc(
                    "Carbon MRV",
                    "Sustainability",
                    "gavel",
                    "Measuring, reporting and verifying practice-change carbon at supply-shed scale so every credit stands up to an audit.",
                    problem="Carbon programs enrol acres faster than they can prove the outcome, and measurement stitched from spreadsheets and one-off models will not survive verification.",
                    who="Sustainability",
                    how="Imagery, practice and soil data feed carbon and emissions models scored in Model Serving, with Unity Catalog holding an auditable lineage from field practice to reported credit.",
                    comps=["Carbon MRV Console", "Model Serving", "Planet Imagery", "Unity Catalog", "AI/BI"],
                    stories=[
                        ["Agerpoint partners with Databricks for agriculture and nature systems", "https://www.agerpoint.com/blog/agerpoint-partners-with-databricks-to-scale-enterprise-data-intelligence-for-agriculture-and-nature-systems"],
                        ["Geospatial AI Accelerator by Lovelytics", "https://www.databricks.com/company/partners/consulting-and-si/partner-solutions/lovelytics-geospatial-accelerator"],
                    ],
                ),
                uc(
                    "Traceability",
                    "Supply chain",
                    "share",
                    "Following crop and input provenance from field to processor so deforestation-free and scope-3 claims are backed by governed evidence, not attestation.",
                    problem="Provenance evidence for regulations like EUDR and for scope-3 sourcing is scattered across ERP, field and partner systems, so due diligence is manual and hard to defend.",
                    who="Commercial",
                    how="Field, ERP and partner data are conformed under Unity Catalog and published as governed data products shared to partners and regulators over Open Sharing.",
                    comps=["SAP S/4HANA", "Unity Catalog", "Open Sharing", "Data Products", "Delta Lake"],
                ),
            ],
        ),
        "sources": {
            "fieldview": {"t": "Bayer Climate FieldView", "u": "https://climate.com/"},
            "jd-opscenter": {"t": "John Deere Operations Center", "u": "https://www.deere.com/en/technology-products/precision-ag-technology/data-management/operations-center/"},
            "trimble-ag": {"t": "Trimble Agriculture", "u": "https://agriculture.trimble.com/"},
            "granular": {"t": "Granular by Corteva", "u": "https://granular.ag/"},
            "jdlink": {"t": "John Deere JDLink telematics", "u": "https://www.deere.com/en/technology-products/precision-ag-technology/data-management/jdlink/"},
            "cnh-afs": {"t": "Case IH Advanced Farming Systems (AFS Connect)", "u": "https://www.caseih.com/en-us/unitedstates/products/advanced-farming-systems/afs-connect"},
            "agco-fuse": {"t": "AGCO Fuse smart farming", "u": "https://www.fuse-technologies.com/"},
            "isobus": {"t": "ISO 11783 (ISOBUS)", "u": "https://en.wikipedia.org/wiki/ISO_11783"},
            "planet": {"t": "Planet Labs", "u": "https://www.planet.com/"},
            "sentinelhub": {"t": "Sentinel Hub", "u": "https://www.sentinel-hub.com/"},
            "dji-ag": {"t": "DJI Agriculture", "u": "https://ag.dji.com/"},
            "descartes": {"t": "Descartes Labs", "u": "https://www.descarteslabs.com/"},
            "dtn": {"t": "DTN Agriculture", "u": "https://www.dtn.com/agriculture/"},
            "cropx": {"t": "CropX soil sensing", "u": "https://cropx.com/"},
            "semios": {"t": "Semios crop intelligence", "u": "https://semios.com/"},
            "metos": {"t": "Pessl Instruments METOS", "u": "https://metos.global/en/"},
            "cropwise": {"t": "Syngenta Cropwise", "u": "https://www.cropwise.com/"},
            "labware": {"t": "LabWare LIMS", "u": "https://www.labware.com/"},
            "sap-s4": {"t": "SAP S/4HANA", "u": "https://www.sap.com/products/erp/s4hana.html"},
            "dssat": {"t": "DSSAT crop simulation", "u": "https://dssat.net/"},
            "adapt": {"t": "AgGateway ADAPT framework", "u": "https://adaptframework.org/"},
            "leaf": {"t": "Leaf agriculture API", "u": "https://withleaf.io/"},
            "verra": {"t": "Verra carbon registry", "u": "https://verra.org/"},
            "eudr": {"t": "EU Deforestation Regulation", "u": "https://environment.ec.europa.eu/topics/forests/deforestation/regulation-deforestation-free-products_en"},
        },
    }
}
