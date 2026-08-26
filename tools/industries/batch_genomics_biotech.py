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


INDUSTRIES_BATCH_GENOMICS_BIOTECH = {
    'genomics_biotech': {
        "label": "Genomics & Biotech",
        "blurb": "Genomics and biotechnology: sequencing pipelines, variant interpretation, lab operations, clinical trial biomarkers and regulated research data.",
        "medallion": medallion(
            "Raw sequence and LIMS",
            "FASTQ and BAM files, LIMS sample metadata, instrument QC metrics and electronic lab notebook entries, landed exactly as received so a variant call or a sample chain can always be replayed.",
            "Conformed sample, variant",
            "Samples, subjects, assays and variant calls resolved into single conformed entities across LIMS, sequencers and analysis pipelines, with sample lineage reconciled from collection through report.",
            "Actionable clinical biomarkers",
            "Contracted products clinical and research teams run on: variant classification tiers, trial enrolment biomarker rates, lab turnaround time, and pipeline QC pass rates.",
        ),
        "rails": {
            "src": [
                {"box": "Sequencing & Omics", "ic": "stream", "tiles": [
                    tile("Illumina BaseSpace", "db", "Run metadata, cluster density and demultiplexed FASTQ from NovaSeq and NextSeq instruments.", "illumina-basespace"),
                    tile("Oxford Nanopore EPI2ME", "iot", "Long-read basecalls, methylation and structural variant calls from MinION and PromethION.", "nanopore-epi2me"),
                    tile("10x Genomics Cloud", "api", "Single-cell and spatial gene expression matrices from Chromium and Visium workflows.", "10x-cloud")
                ]},
                {"box": "Lab & Sample Mgmt", "ic": "erp", "tiles": [
                    tile("Benchling R&D Cloud", "notebook", "Sample registration, chain of custody and structured experiment records.", "benchling"),
                    tile("LabVantage LIMS", "db", "Clinical and research sample accessioning, aliquots and result release.", "labvantage"),
                    tile("LIMS", "sheet", "Specimen tracking, storage location and stability across biobank freezers.", "samplemanager")
                ]},
                {"box": "Clinical & Trials", "ic": "people", "tiles": [
                    tile("Medidata Rave EDC", "gavel", "Electronic case report forms, visit schedules and protocol deviations.", "medidata-rave"),
                    tile("Veeva Vault CTMS", "partner", "Site activation, enrolment milestones and monitoring visit findings.", "veeva-ctms"),
                    tile("Flatiron Oncology EHR", "custlake", "De-identified oncology clinical records for real-world evidence cohorts.", "flatiron")
                ]},
                {"box": "Knowledge & Reference", "ic": "globe", "tiles": [
                    tile("ClinVar & gnomAD", "share", "Public variant pathogenicity and population frequency references for annotation.", "clinvar"),
                    tile("COSMIC Cancer DB", "db", "Somatic mutation catalogue for oncology biomarker interpretation.", "cosmic"),
                    tile("Instrument QC Telemetry", "observ", "Sequencer health, reagent lot and calibration drift joined to run outcomes.")
                ]},
                fed_group(
                    "CRO Analysis Results",
                    "Contract research organisation variant reports left at partners and queried in place under Unity Catalog.",
                ),
            ],
            "ing": ing_rail([
                tile("GA4GH WES/WGS APIs", "api", "Beacon and phenopacket exchange endpoints consumed inbound for federated discovery.", "ga4gh"),
                tile("HL7 FHIR Genomics", "stream", "Diagnostic report and observation resources normalised on ingest for clinical integration.", "fhir-genomics"),
                tile("dbGaP Authorised Access", "gavel", "Controlled-access cohort files retrieved under DAC-approved scopes.")
            ]),
            "ppl": ppl2([
                biz("CSO & CFO", "Genie One", "The CSO on sequencing throughput and biomarker programme progress; the CFO on CRO spend, cost-per-sample and trial enrolment velocity.",
                    [["Genie One", "Ask how many samples cleared QC this week without waiting on bioinformatics."], ["AI/BI", "Throughput, QC and trial metrics on one certified set of Metric Views."], ["Unity Catalog", "Certification and the business glossary, so \"pathogenic\" means one thing across labs."]]),
                biz("Bioinformatics", "Model Serving", "Pipeline engineers and analysts on variant calling, annotation and the VUS queue, deciding what is safe to release to clinicians at sign-out.",
                    [["Variant Review Workbench", "VUS queues prioritised by evidence tier before sign-out."], ["Model Serving", "Classifier models scored in the interpretation path."], ["MLflow", "Pipeline runs tracked for CLIA and CAP audit."]]),
                biz("Clinical Operations", "AI/BI", "Trial managers on site enrolment against target, sample-collection SLAs and protocol deviations before a site is at risk of closing.",
                    [["Trial Enrolment Tracker", "Biomarker-positive screen failures surfaced before sites close."], ["AI/BI", "Enrolment and deviation metrics on certified Metric Views."], ["Unity Catalog", "One definition of subject status across EDC and LIMS."]]),
                biz("Lab Operations", "Lakeflow", "Lab directors on assay turnaround time, reagent-lot inventory and instrument utilisation before a client escalates a late result.",
                    [["Lab Ops Dashboard", "Queue depth and TAT by assay before clients escalate."], ["Lakeflow", "LIMS and instrument feeds conformed for operations analytics."], ["Lakewatch", "Freshness on the tables sign-out depends on."]]),
                biz("Regulatory & Quality", "AI/BI", "Quality and regulatory affairs on CAP and CLIA audits, QC failure rates and the validation documentation a submission stands or falls on.",
                    [["Quality Metrics", "QC failure rates and CAPA aging on governed definitions."], ["AI/BI", "Audit-ready dashboards regulators can trace."], ["Unity Catalog", "Lineage from raw FASTQ to signed report."]]),
            ], [
                biz("Data Engineers", "Lakeflow", "Land the sequencer, LIMS and trial EDC feeds; own the Bronze to Silver path and the pager when a run or sample feed breaks.",
                    [["Lakeflow Connect", "Managed connectors for BaseSpace, LIMS and EDC sources."], ["Lakeflow Designer", "Declarative pipelines with expectations on FASTQ and sample feeds."], ["Lakewatch", "Freshness on the tables sign-out and trial teams read every morning."]]),
                biz("Data Scientists", "MLflow", "Variant-classification, biomarker-discovery and turnaround-time models, and whether they still hold under CAP and CLIA validation.",
                    [["Feature Store", "Sample and variant features defined once for training and serving."], ["MLflow", "Every pipeline run tracked for CLIA and CAP audit."], ["Model Serving", "Classifier models scored in the interpretation path."]]),
                biz("App Developers", "Apps", "Ship the variant review, enrolment-tracking and lab-ops applications the labs work in, hosted next to governed data.",
                    [["Apps", "Review and lab screens with no separate web tier to run or secure."], ["Lakebase", "Serverless Postgres for sign-out and sample writes."], ["Agent Bricks", "Agents that draft a variant summary or enrolment check against governed tools."]]),
            ]),
            "cons": cons_rail([
                {"box": "BI & Productivity", "ic": "chart", "from": "bi", "tiles": [
                    tile("Tableau / Qlik / ThoughtSpot", "chart", "External BI against serverless SQL warehouses, with Unity Catalog permissions enforced end to end."),
                    tile("Microsoft Teams", "chat", "Genie in Teams for Unity Catalog-governed answers from the lakehouse, and lab alerts in the channel teams already work in (Beta)."),
                    tile("Notebooks & IDEs", "notebook", "Notebooks, VS Code and JetBrains against governed data and Genie Code.")
                ]},
                {"box": "Clinical Writeback", "ic": "opdb", "tiles": [
                    tile("Signed Report Release", "gavel", "Interpreted variants and diagnostic narratives written back into LIMS for clinician delivery.", "labvantage"),
                    tile("EDC Biomarker Flags", "db", "Enrolment eligibility results pushed to the trial EDC at screening.", "medidata-rave"),
                    tile("Lab Queue Mobile", "apps", "Sample prep tasks and exception handling pushed to bench technologists.")
                ]},
                {"box": "Research Partners", "ic": "partner", "tiles": [
                    tile("CRO Data Exchange", "share", "Variant and QC tables shared with contract labs over Delta Sharing under study agreements."),
                    tile("Academic Collaborations", "globe", "Federated cohort queries via GA4GH beacons without exporting patient-level files.", "ga4gh"),
                    tile("Pharma Alliance Feeds", "product", "Biomarker prevalence and response summaries exchanged under collaboration MSAs.")
                ]},
                {"box": "Regulatory & Reporting", "ic": "gavel", "tiles": [
                    tile("CLIA/CAP Compliance", "gavel", "QC, proficiency and corrective action records produced from governed lab tables."),
                    tile("FDA Submission Packages", "share", "Validation summaries and analysis reproducibility filed from contracted Gold products.")
                ]},
                {"box": "Published Products", "ic": "product", "tiles": [
                    tile("Data Products", "product", "Published, contracted products discoverable in Unity Catalog Domains and shared over Open Sharing."),
                    tile("Sharing Recipients", "share", "CROs, pharma partners and consortia reading live tables with no copy and no egress duplication.")
                ]},
            ]),
        },
        "top": top_band(
            [
                app("Variant Review Workbench", "Clinical sign-out", "gauge", "VUS and pathogenic calls ranked by evidence tier with literature and population frequency at the curator's fingertips."),
                app("Trial Enrolment Tracker", "Biomarker screening", "people", "Sites, screen failures and biomarker-positive enrolment against protocol targets in real time."),
                app("Lab Ops Dashboard", "Throughput & TAT", "stream", "Instrument queues, reagent lots and turnaround time by assay before clients escalate."),
                app("Pipeline QC Console", "Bioinformatics", "iot", "Run-level QC metrics and pipeline failures surfaced before downstream annotation consumes bad calls."),
            ],
            [
                uc("Variant Interpretation", "Diagnostics", "gauge", "Somatic and germline variants classified with reproducible evidence chains clinicians can defend."),
                uc("Biomarker Discovery", "Research", "sheet", "Multi-omic signals ranked for trial enrichment and companion diagnostic development."),
                uc("Trial Enrolment", "Clinical ops", "people", "Screening workflows that match patients to protocols from genomic and clinical criteria."),
                uc("Lab Turnaround Optimisation", "Operations", "stream", "Queue bottlenecks identified from accession through sign-out, not average TAT alone."),
                uc("Real-World Evidence", "Outcomes", "custlake", "Treatment response cohorts built from linked genomic and oncology EHR records under governance."),
                uc("Single-Cell Analytics", "Discovery", "notebook", "Cell-type resolution across tumour microenvironment for target identification."),
                uc("Pipeline Reproducibility", "Quality", "gavel", "Every analysis from FASTQ to report traced for CAP, CLIA and FDA inspection."),
                uc("Reference Data Harmonisation", "Annotation", "globe", "ClinVar, gnomAD and COSMIC updates propagated without breaking historical calls."),
                uc("Sample Chain of Custody", "Compliance", "product", "Aliquot location and handling events reconciled from collection through destruction."),
                uc("Pharmacogenomics", "Therapeutics", "market", "Drug-gene interactions surfaced at ordering for precision prescribing programmes."),
            ],
        ),
        "sources": {
            "illumina-basespace": {"t": "Illumina BaseSpace Sequence Hub", "u": "https://www.illumina.com/products/by-type/informatics-products/basespace-sequence-hub.html"},
            "nanopore-epi2me": {"t": "Oxford Nanopore EPI2ME", "u": "https://epi2me.nanoporetech.com/"},
            "10x-cloud": {"t": "10x Genomics Cloud Analysis", "u": "https://www.10xgenomics.com/products/cloud-analysis"},
            "benchling": {"t": "Benchling R&D Cloud", "u": "https://www.benchling.com/"},
            "labvantage": {"t": "LabVantage LIMS", "u": "https://www.labvantage.com/"},
            "samplemanager": {"t": "Thermo Fisher SampleManager LIMS", "u": "https://www.thermofisher.com/samplemanager"},
            "medidata-rave": {"t": "Medidata Rave EDC", "u": "https://www.medidata.com/en/clinical-trial-products/clinical-data-management/edc-systems/"},
            "veeva-ctms": {"t": "Veeva Vault CTMS", "u": "https://www.veeva.com/products/vault-ctms/"},
            "flatiron": {"t": "Flatiron Health oncology data", "u": "https://flatiron.com/"},
            "clinvar": {"t": "NCBI ClinVar", "u": "https://www.ncbi.nlm.nih.gov/clinvar/"},
            "cosmic": {"t": "COSMIC cancer database", "u": "https://cancer.sanger.ac.uk/cosmic"},
            "ga4gh": {"t": "Global Alliance for Genomics and Health", "u": "https://www.ga4gh.org/"},
            "fhir-genomics": {"t": "HL7 FHIR genomics implementation guide", "u": "https://hl7.org/fhir/uv/genomics-reporting/"}
        },
    },
}
