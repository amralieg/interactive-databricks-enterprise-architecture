import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    app, biz, cons_rail, dashboard, data_out, fed_group, flow, genie, ing_rail,
    medallion, tile, top_band, uc,
)


def ppl2(business_tiles, tech_tiles):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_CYBERSECURITY = {
    "cybersecurity": {
        "label": "Cybersecurity",
        "blurb": "Enterprise security operations: threat detection and correlation, alert triage, threat hunting, insider risk, vulnerability management, incident response, and compliance across the SOC.",
        "medallion": medallion(
            "Raw security telemetry",
            "Endpoint, identity, network, cloud-audit and SIEM logs from CrowdStrike, Splunk, Okta and dozens of sources, landed exactly as received in open OCSF, Delta and Iceberg formats so any alert can be replayed against full-fidelity history rather than a truncated retention window.",
            "Conformed entities & OCSF",
            "Users, hosts, identities and assets resolved into single conformed entities across the endpoint, identity and network estates, normalised to the Open Cybersecurity Schema Framework and enriched with threat-intel indicators and MITRE ATT&CK technique tags.",
            "Detections, risk, MTTR",
            "Contracted products the SOC and GRC teams run on: high-fidelity detections mapped to MITRE ATT&CK, entity risk scores, mean-time-to-detect and respond, and compliance coverage measured by control framework.",
        ),
        "rails": {
            "src": [
                {
                    "box": "SIEM & Log Analytics",
                    "ic": "observ",
                    "tiles": [
                        tile(
                            "Splunk Enterprise",
                            "observ",
                            "The incumbent SIEM and search index for security events, alerts and dashboards, and the source of the SPL detections and correlation searches the SOC runs today.",
                            "splunk",
                            cat="SIEM / Log Analytics",
                            what="Incumbent SIEM and search index for security events, alerts and dashboards; runs the SPL detections and correlation searches the SOC uses today.",
                            users="SOC analysts, detection engineers and security leadership.",
                            data_out=data_out(
                                batch=flow(["semi-structured"], "TB/day indexed logs", "Continuous + scheduled searches"),
                                stream=flow(["semi-structured"], "100k-1M events/sec at peak", "Continuous")),
                        ),
                        tile(
                            "Elastic Security",
                            "observ",
                            "Elastic Common Schema logs, detection rules and endpoint telemetry, a common SIEM and search estate for high-volume log analytics.",
                            "elastic",
                            cat="SIEM / Log Analytics",
                            what="Elastic Common Schema logs, detection rules and endpoint telemetry for high-volume log analytics.",
                            users="SOC analysts and security engineering.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "50k-500k events/sec at peak", "Continuous")),
                        ),
                        tile(
                            "Microsoft Sentinel",
                            "zshield",
                            "Cloud-native SIEM and SOAR: analytics rules, incidents and workbooks over identity, endpoint and productivity signals across the Microsoft estate.",
                            "sentinel",
                            cat="Cloud SIEM / SOAR",
                            what="Cloud-native SIEM and SOAR: analytics rules, incidents and workbooks over identity, endpoint and productivity signals across the Microsoft estate.",
                            users="SOC analysts and Microsoft-estate security teams.",
                            data_out=data_out(
                                batch=flow(["semi-structured"], "100s of GB/day", "Daily"),
                                stream=flow(["semi-structured"], "10-100k events/sec at peak", "Continuous")),
                        ),
                        tile(
                            "Chronicle SecOps",
                            "observ",
                            "Petabyte-scale security telemetry, UDM-normalised events and curated detections, retained for long-horizon threat investigation.",
                            "chronicle",
                            cat="Cloud-Scale Security Analytics",
                            what="Petabyte-scale security telemetry, UDM-normalised events and curated detections retained for long-horizon investigation.",
                            users="SOC, threat hunters and detection engineers.",
                            data_out=data_out(
                                batch=flow(["semi-structured"], "PB-scale retained telemetry", "Continuous ingest"),
                                stream=flow(["semi-structured"], "100k-1M events/sec at peak", "Continuous")),
                        ),
                    ],
                },
                {
                    "box": "Endpoint & XDR",
                    "ic": "zshield",
                    "tiles": [
                        tile(
                            "CrowdStrike Falcon",
                            "zshield",
                            "Endpoint detection and response telemetry, process trees, detections and containment actions from the Falcon sensor across the fleet.",
                            "crowdstrike",
                            cat="Endpoint Detection & Response (EDR)",
                            what="Endpoint detection and response telemetry, process trees, detections and containment actions from the Falcon sensor across the fleet.",
                            users="SOC, incident responders and endpoint teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "10-100k events/sec at peak", "Continuous")),
                        ),
                        tile(
                            "SentinelOne EDR",
                            "zshield",
                            "Singularity endpoint and identity telemetry, behavioural detections and automated response for workstations, servers and cloud workloads.",
                            "sentinelone",
                            cat="Endpoint / XDR",
                            what="Singularity endpoint and identity telemetry, behavioural detections and automated response across workstations, servers and cloud workloads.",
                            users="SOC and endpoint security teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "10-100k events/sec at peak", "Continuous")),
                        ),
                        tile(
                            "Microsoft Defender XDR",
                            "zshield",
                            "Cross-domain endpoint, email, identity and app signals with alerts and advanced hunting tables spanning the Defender suite.",
                            "defender",
                            cat="Extended Detection & Response (XDR)",
                            what="Cross-domain endpoint, email, identity and app signals with alerts and advanced-hunting tables across the Defender suite.",
                            users="SOC analysts and Microsoft security teams.",
                            data_out=data_out(
                                batch=flow(["semi-structured"], "100s of GB/day hunting tables", "Daily"),
                                stream=flow(["semi-structured"], "10-100k events/sec at peak", "Continuous")),
                        ),
                    ],
                },
                {
                    "box": "Identity & Access",
                    "ic": "identity",
                    "tiles": [
                        tile(
                            "Okta Identity Cloud",
                            "identity",
                            "Workforce sign-in, MFA, factor and system-log events, the authoritative record of who authenticated where and how.",
                            "okta",
                            cat="Identity Provider (IdP)",
                            what="Workforce sign-in, MFA, factor and system-log events; the authoritative record of who authenticated where and how.",
                            users="Identity, SOC and insider-risk teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "100s-1000s of events/sec", "Continuous")),
                        ),
                        tile(
                            "Microsoft Entra ID",
                            "identity",
                            "Directory, conditional-access and sign-in logs with risk detections, the identity graph every UEBA and lateral-movement detection joins to.",
                            "entra",
                            cat="Identity & Access Management (IAM)",
                            what="Directory, conditional-access and sign-in logs with risk detections; the identity graph UEBA and lateral-movement detections join to.",
                            users="Identity, SOC and GRC teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "100s-1000s of events/sec", "Continuous")),
                        ),
                        tile(
                            "CyberArk PAM",
                            "key",
                            "Privileged session recordings, vault checkouts and secret access, the source of truth for privileged-account misuse detection.",
                            "cyberark",
                            cat="Privileged Access Management (PAM)",
                            what="Privileged session recordings, vault checkouts and secret access; the source of truth for privileged-account misuse detection.",
                            users="Identity, insider-risk and SOC teams.",
                            data_out=data_out(
                                batch=flow(["structured", "unstructured"], "GBs/day (logs + session recordings)", "Hourly"),
                                stream=flow(["semi-structured"], "tens of events/sec", "Continuous")),
                        ),
                    ],
                },
                {
                    "box": "Vuln & Threat Intel",
                    "ic": "gauge",
                    "tiles": [
                        tile(
                            "Tenable Nessus",
                            "gauge",
                            "Vulnerability scan results, plugin findings and asset exposure across the estate, the raw feed for exposure prioritisation.",
                            "tenable",
                            cat="Vulnerability Scanning",
                            what="Vulnerability scan results, plugin findings and asset exposure across the estate; the raw feed for exposure prioritisation.",
                            users="Vulnerability management and GRC teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-5 GB/scan cycle", "Daily / weekly scans")),
                        ),
                        tile(
                            "Qualys VMDR",
                            "gauge",
                            "Vulnerability management, detection and response findings with asset criticality and patch state for risk-based prioritisation.",
                            "qualys",
                            cat="Vulnerability Management (VM)",
                            what="Vulnerability management, detection and response findings with asset criticality and patch state for risk-based prioritisation.",
                            users="Vulnerability management and risk teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-5 GB/day", "Daily")),
                        ),
                        tile(
                            "Mandiant Threat Intel",
                            "globe",
                            "Adversary profiles, indicators and campaign intelligence used to prioritise detections against the threats actually targeting the sector.",
                            "mandiant",
                            cat="Threat Intelligence Provider",
                            what="Adversary profiles, indicators and campaign intelligence used to prioritise detections against the threats targeting the sector.",
                            users="Threat intel analysts and detection engineers.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "sub-GB/day", "Daily + on-demand")),
                        ),
                        tile(
                            "Recorded Future",
                            "globe",
                            "Real-time indicators, risk scores and dark-web intelligence enriched onto entities to raise or lower detection confidence.",
                            "recorded-future",
                            cat="Threat Intelligence Provider",
                            what="Real-time indicators, risk scores and dark-web intelligence enriched onto entities to raise or lower detection confidence.",
                            users="Threat intel analysts and SOC teams.",
                            data_out=data_out(
                                batch=flow(["structured", "semi-structured"], "sub-GB/day", "Daily"),
                                stream=flow(["semi-structured"], "100s of indicators/sec", "Continuous (API)")),
                        ),
                    ],
                },
                {
                    "box": "Network & Cloud Sec",
                    "ic": "network",
                    "tiles": [
                        tile(
                            "Palo Alto NGFW",
                            "network",
                            "Next-generation firewall traffic, threat-prevention and URL-filtering logs, the perimeter and east-west view of the network.",
                            "paloalto",
                            cat="Next-Gen Firewall (NGFW)",
                            what="Next-generation firewall traffic, threat-prevention and URL-filtering logs; the perimeter and east-west view of the network.",
                            users="Network security and SOC teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "10-100k events/sec at peak", "Continuous")),
                        ),
                        tile(
                            "Zscaler ZIA/ZPA",
                            "cloud",
                            "Secure web gateway and zero-trust access logs for every user-to-app session, the source for egress and exfiltration analysis.",
                            "zscaler",
                            cat="Secure Web Gateway / ZTNA",
                            what="Secure web gateway and zero-trust access logs for every user-to-app session; the source for egress and exfiltration analysis.",
                            users="Network security, SOC and insider-risk teams.",
                            data_out=data_out(
                                stream=flow(["semi-structured"], "10-100k events/sec at peak", "Continuous")),
                        ),
                        tile(
                            "Corelight NDR",
                            "network",
                            "Zeek-based network evidence and detections, the high-fidelity packet-derived record threat hunters pivot on during investigations.",
                            "corelight",
                            cat="Network Detection & Response (NDR)",
                            what="Zeek-based network evidence and detections; the high-fidelity packet-derived record hunters pivot on during investigations.",
                            users="Threat hunters, SOC and network security teams.",
                            data_out=data_out(
                                batch=flow(["semi-structured"], "TB/day network evidence", "Continuous"),
                                stream=flow(["semi-structured"], "10-100k events/sec at peak", "Continuous")),
                        ),
                        tile(
                            "Wiz CNAPP",
                            "cloud",
                            "Cloud security posture, misconfiguration and runtime findings across cloud accounts, containers and workloads.",
                            "wiz",
                            cat="Cloud Security (CNAPP)",
                            what="Cloud security posture, misconfiguration and runtime findings across cloud accounts, containers and workloads.",
                            users="Cloud security, GRC and SOC teams.",
                            data_out=data_out(
                                batch=flow(["structured"], "1-5 GB/day findings", "Daily"),
                                stream=flow(["semi-structured"], "tens of events/sec", "Continuous (runtime)")),
                        ),
                    ],
                },
                fed_group(
                    "Enterprise Audit Marts",
                    "Cloud-provider audit trails, HR joiner-mover-leaver records and asset inventories left in their existing warehouses and queried in place under Unity Catalog, so identity and asset context enriches detections without a second copy of sensitive data.",
                    cat="Enterprise Data Warehouse / Audit",
                    what="Cloud-provider audit trails, HR joiner-mover-leaver records and asset inventories kept in existing warehouses and queried in place through federation.",
                    users="GRC, insider-risk and SOC analysts.",
                    data_out=data_out(
                        batch=flow(["structured"], "TB-scale audit history", "Queried on demand (federated)")),
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "OCSF Event Streams",
                        "stream",
                        "Security telemetry normalised to the Open Cybersecurity Schema Framework on arrival and landed as governed tables, so detections are written once against a vendor-neutral schema.",
                        "ocsf",
                        cat="Normalized Security Schema (OCSF)",
                        what="Security telemetry normalised to the Open Cybersecurity Schema Framework on arrival and landed as governed tables.",
                        users="Security data engineers and detection engineers.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "100k-1M events/sec at peak", "Continuous")),
                    ),
                    tile(
                        "Kafka Security Topics",
                        "eventbus",
                        "High-volume endpoint, network and identity events carried on existing Kafka topics, consumed continuously into the lakehouse for near-real-time detection.",
                        "kafka",
                        cat="Event Streaming Platform",
                        what="High-volume endpoint, network and identity events carried on existing Kafka topics, consumed continuously for near-real-time detection.",
                        users="Security data engineers and streaming teams.",
                        data_out=data_out(
                            stream=flow(["semi-structured"], "50k-1M events/sec at peak", "Continuous")),
                    ),
                    tile(
                        "Cortex XSOAR",
                        "orch",
                        "SOAR case, playbook-run and enrichment records ingested back so response actions and analyst decisions are analysed alongside the alerts that triggered them.",
                        "xsoar",
                        cat="SOAR / Case Management",
                        what="SOAR case, playbook-run and enrichment records ingested back so response actions and analyst decisions are analysed alongside the alerts that triggered them.",
                        users="SOC, incident responders and detection engineers.",
                        data_out=data_out(
                            batch=flow(["structured", "semi-structured"], "sub-GB/day cases + playbook runs", "Hourly"),
                            stream=flow(["semi-structured"], "tens of events/sec", "Continuous")),
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Security Leadership",
                        "Genie One",
                        "The CISO on aggregate risk posture, board-level cyber exposure and the cost and coverage of the security programme; the deputy CISO and SecOps director on detection coverage against MITRE ATT&CK, mean-time-to-respond and the economics of log retention.",
                        [
                            ["Genie One", "Ask what the current risk posture and open critical incidents are without booking analyst time."],
                            ["AI/BI", "Detection coverage, MTTD and MTTR, and SIEM spend on one certified set of Metric Views."],
                            ["Unity Catalog", "Governance and the security glossary, so \"critical incident\" and \"coverage\" mean one thing across the programme."],
                        ],
                        sub=[
                            ["CISO", "aggregate risk posture, board reporting and cyber exposure."],
                            ["Deputy CISO", "detection coverage, control effectiveness and programme maturity."],
                            ["SecOps Director", "SOC throughput, mean-time-to-respond and retention economics."],
                        ],
                        ucs=["Threat Detection", "Security Lakehouse", "Compliance Reporting"],
                    ),
                    biz(
                        "SOC & Response",
                        "Lakehouse//RT",
                        "Tier-1 and tier-2 SOC analysts triaging alerts against a shrinking clock, incident responders containing active intrusions, and on-call leads running the bridge when a confirmed breach is in progress.",
                        [
                            ["SOC Triage Console", "The alert, its full entity context and the recommended action on one screen before an analyst escalates."],
                            ["Lakehouse//RT", "Endpoint, identity and network events at the latency an intrusion moves at."],
                            ["Model Serving", "Alert-scoring and deduplication models scored inline so the queue is ordered by real risk."],
                        ],
                        sub=[
                            ["Tier-1 analysts", "first-pass triage and false-positive suppression."],
                            ["Tier-2 analysts", "deeper correlation and escalation decisions."],
                            ["Incident responders", "containment, eradication and recovery on active intrusions."],
                        ],
                        ucs=["Threat Detection", "Alert Triage & Dedup", "Incident Forensics", "Phishing & BEC Defense"],
                    ),
                    biz(
                        "Threat Intelligence",
                        "AI/BI",
                        "Threat intel analysts curating adversary tradecraft and indicators, and threat hunters forming hypotheses and pivoting across months of telemetry to find what no rule fired on.",
                        [
                            ["Threat Hunt Workbench", "Hypothesis-driven hunts across the full-fidelity history rather than a two-week index."],
                            ["Genie", "Plain-English pivots across petabytes so a hunt is not gated on SPL fluency."],
                            ["AI/BI", "Campaign, indicator and coverage views on governed data."],
                        ],
                        sub=[
                            ["Threat intel analysts", "adversary profiling, indicator curation and prioritisation."],
                            ["Threat hunters", "hypothesis-driven hunting across long-horizon telemetry."],
                        ],
                        ucs=["Threat Hunting", "Threat Detection", "Vulnerability Triage"],
                    ),
                    biz(
                        "GRC & Compliance",
                        "Unity Catalog",
                        "Governance, risk and compliance teams evidencing controls to auditors, insider-risk analysts investigating anomalous user behaviour, and risk owners prioritising the vulnerabilities that actually matter to the business.",
                        [
                            ["Unity Catalog", "Lineage, access controls and control evidence produced from the same governed tables the SOC runs on."],
                            ["AI/BI", "Compliance coverage, insider-risk scores and exposure by control framework."],
                            ["Genie One", "Ask which controls lack evidence this quarter without a manual audit pull."],
                        ],
                        sub=[
                            ["Compliance analysts", "control evidence and framework coverage (SOC 2, PCI, NIST)."],
                            ["Insider-risk analysts", "anomalous user and privileged-access behaviour."],
                            ["Risk owners", "risk-based vulnerability and exposure prioritisation."],
                        ],
                        ucs=["Compliance Reporting", "Insider Risk & UEBA", "Vulnerability Triage"],
                    ),
                    biz(
                        "Detection Engineering",
                        "Model Serving",
                        "Detection engineers who write, test and ship detection content as code, and content developers who tune rules against false positives and keep coverage mapped to the ATT&CK matrix.",
                        [
                            ["Detection Studio", "Detections authored, backtested against history and shipped through CI/CD."],
                            ["Model Serving", "Behavioural and anomaly models scored alongside rule-based detections."],
                            ["Unity Catalog", "Versioned, governed detection content with lineage from rule to alert."],
                        ],
                        sub=[
                            ["Detection engineers", "detection-as-code authoring, testing and deployment."],
                            ["Content developers", "false-positive tuning and ATT&CK coverage mapping."],
                        ],
                        ucs=["Detection-as-Code", "Phishing & BEC Defense", "Alert Triage & Dedup"],
                    ),
                ],
                [
                    biz(
                        "Detection Engineers",
                        "Lakeflow",
                        "Write detections as code in Sigma, SQL and Python notebooks, backtest them against historical telemetry, and manage the rule library through Git and CI/CD instead of hand-editing SIEM consoles.",
                        [
                            ["Genie Code", "Draft and refine detections and translate hunt questions into SQL against governed tables."],
                            ["Lakeflow", "Streaming and batch detection pipelines with expectations on every security feed."],
                            ["Unity Catalog", "Versioned detection content with lineage from rule change to alert."],
                        ],
                    ),
                    biz(
                        "Sec Data Engineers",
                        "Lakeflow",
                        "Land Splunk, EDR, identity and network feeds, normalise them to OCSF with Auto Loader and Lakeflow, and own the Bronze-to-Silver path and the pager when a security pipeline stalls.",
                        [
                            ["Lakeflow Connect", "Managed connectors for SIEM, EDR, identity and SaaS security sources."],
                            ["Auto Loader", "Incremental ingestion of high-volume log files into OCSF-conformed tables."],
                            ["Lakeflow", "Declarative pipelines with expectations on endpoint, identity and network feeds."],
                        ],
                    ),
                    biz(
                        "Threat Hunters",
                        "AI/BI",
                        "Form hypotheses from ATT&CK tradecraft and Corelight and Zeek evidence, pivot across months of telemetry in notebooks, and turn confirmed findings into new detection content.",
                        [
                            ["Genie", "Natural-language pivots across full-fidelity history without SPL or KQL fluency."],
                            ["AI/BI", "Hunt findings, indicator overlaps and coverage gaps on governed data."],
                            ["Model Serving", "Anomaly and entity-risk models scored to surface hunt leads."],
                        ],
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
                                "Executive risk and SOC-performance dashboards against serverless SQL warehouses, with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for Unity Catalog-governed answers from the security lakehouse, and incident updates in the channel the SOC already works in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Analyst and hunter notebooks, VS Code and JetBrains against governed telemetry and Genie Code.",
                            ),
                        ],
                    },
                    {
                        "box": "Response & Orchestration",
                        "ic": "orch",
                        "tiles": [
                            tile(
                                "SOAR Playbooks",
                                "orch",
                                "Enriched, scored alerts pushed to Cortex XSOAR so containment and notification playbooks fire with full lakehouse context attached.",
                                "xsoar",
                            ),
                            tile(
                                "EDR Host Isolation",
                                "zshield",
                                "Confirmed-compromise decisions written back to CrowdStrike or SentinelOne to isolate a host in the tool the responder already operates.",
                                "crowdstrike",
                            ),
                            tile(
                                "ITSM Ticketing",
                                "opdb",
                                "Incidents and remediation tasks raised in ServiceNow Security Operations, tracked to closure against the same governed record.",
                                "servicenow",
                            ),
                        ],
                    },
                    {
                        "box": "Detection Delivery",
                        "ic": "cicd",
                        "tiles": [
                            tile(
                                "Detection CI/CD",
                                "cicd",
                                "Detection-as-code changes tested against historical telemetry and promoted through pipelines rather than edited live in a console.",
                            ),
                            tile(
                                "Sigma Rule Sync",
                                "code",
                                "Vendor-neutral Sigma rules translated and deployed to the lakehouse and downstream SIEMs from one governed source.",
                                "sigma",
                            ),
                            tile(
                                "Alert Dashboards",
                                "gauge",
                                "Scored, deduplicated alert queues surfaced to analysts with entity context and recommended actions.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Audit",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "Compliance Reporting",
                                "gavel",
                                "SOC 2, PCI DSS and NIST control coverage and evidence produced from the same governed tables the SOC runs on.",
                            ),
                            tile(
                                "Audit Evidence",
                                "docs",
                                "Immutable query and access logs proving who saw what and when, covering audit requirements without extra instrumentation.",
                            ),
                            tile(
                                "Regulatory Filings",
                                "gavel",
                                "Breach-notification and regulator reporting produced from contracted Gold products rather than reassembled by hand under deadline.",
                            ),
                        ],
                    },
                    {
                        "box": "Sharing & Products",
                        "ic": "product",
                        "tiles": [
                            tile(
                                "Data Products",
                                "product",
                                "Published, contracted security products discoverable in Unity Catalog Domains and shared over Open Sharing.",
                            ),
                            tile(
                                "Threat Intel Sharing",
                                "share",
                                "Curated indicators and detections shared with ISACs and partners over Delta Sharing rather than emailed spreadsheets.",
                            ),
                            tile(
                                "Sharing Recipients",
                                "share",
                                "Subsidiaries, MSSPs and regulators reading live governed tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ],
                genie_spaces=[
                    genie("SOC Operations", "Ask about open incidents, alert quality and response times in plain language.",
                          feeds=["Splunk Enterprise", "CrowdStrike Falcon", "Cortex XSOAR", "Detections, risk, MTTR"],
                          teams=["SOC & Response", "Security Leadership", "Detection Engineering"],
                          questions=[
                              "How many open critical incidents do we have right now?",
                              "What is mean-time-to-detect and respond this week?",
                              "Which alert types have the worst false-positive rate?",
                              "Which hosts have the most unresolved detections?",
                              "What is the alert backlog past SLA by tier?"]),
                    genie("Threat Hunting", "Pivot across full-fidelity telemetry and threat intel to find what no rule fired on.",
                          feeds=["Corelight NDR", "Chronicle SecOps", "Mandiant Threat Intel", "Conformed entities & OCSF"],
                          teams=["Threat Intelligence", "Threat Hunters", "SOC & Response"],
                          questions=[
                              "Which entities match indicators from the latest campaign?",
                              "Where do we see lateral movement across identities this month?",
                              "Which hosts beaconed to rare external destinations?",
                              "Which ATT&CK techniques have no detection coverage?",
                              "Which internal assets contacted known-bad infrastructure?"]),
                    genie("Identity & Insider Risk", "Explore identity anomalies, privileged access and entity risk across the estate.",
                          feeds=["Okta Identity Cloud", "Microsoft Entra ID", "CyberArk PAM", "Enterprise Audit Marts"],
                          teams=["GRC & Compliance", "SOC & Response", "Security Leadership"],
                          questions=[
                              "Which users show anomalous access versus their baseline?",
                              "Which privileged accounts checked out secrets off-hours?",
                              "Where did impossible-travel sign-ins occur this week?",
                              "Which leavers still have active entitlements?",
                              "Which identities have the highest entity-risk score?"]),
                    genie("Exposure & Compliance", "Answer vulnerability exposure and control-coverage questions across frameworks.",
                          feeds=["Tenable Nessus", "Qualys VMDR", "Wiz CNAPP", "Detections, risk, MTTR"],
                          teams=["GRC & Compliance", "Security Leadership", "Detection Engineering"],
                          questions=[
                              "Which exploitable vulnerabilities sit on business-critical assets?",
                              "What is our patch-SLA compliance by asset class?",
                              "Which controls lack evidence for the current audit cycle?",
                              "Which cloud misconfigurations are exposed to the internet?",
                              "How has overall exposure risk trended this quarter?"]),
                ],
                dashboards=[
                    dashboard("SOC Performance", "Detection coverage, alert volumes and MTTD/MTTR across the SOC.",
                              kpis=["MTTD", "MTTR", "Alert volume", "False-positive rate", "Backlog past SLA"],
                              teams=["SOC & Response", "Security Leadership", "Detection Engineering"]),
                    dashboard("Detection Coverage", "MITRE ATT&CK coverage and detection health across the estate.",
                              kpis=["ATT&CK coverage", "Detections shipped", "Rule false-positive rate", "Coverage gaps", "Backtest pass rate"],
                              teams=["Detection Engineering", "Threat Intelligence", "SOC & Response"]),
                    dashboard("Exposure & Vulnerability", "Risk-based vulnerability exposure and remediation SLA by asset.",
                              kpis=["Critical exposures", "Patch-SLA compliance", "Exploitable-on-critical", "Mean-time-to-remediate", "Cloud misconfigurations"],
                              teams=["GRC & Compliance", "Security Leadership", "Detection Engineering"]),
                    dashboard("Identity & Insider Risk", "Identity anomalies, privileged access and entity-risk scores.",
                              kpis=["Entity-risk score", "Anomalous sign-ins", "Privileged checkouts", "Dormant entitlements", "Impossible-travel events"],
                              teams=["GRC & Compliance", "SOC & Response", "Security Leadership"]),
                ],
            ),
        },
        "top": top_band(
            [
                app(
                    "SOC Triage Console",
                    "Alert triage",
                    "gauge",
                    "The screen a SOC analyst runs the queue from: each alert with its full entity context, deduplicated and scored, and a recommended action, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Threat Hunt Workbench",
                    "Hunting queries",
                    "observ",
                    "Where hunters form a hypothesis and pivot across months of full-fidelity telemetry in plain English, turning a confirmed finding into new detection content in the same session.",
                ),
                app(
                    "Detection Studio",
                    "Detection-as-code",
                    "code",
                    "Author, backtest and ship detections as versioned code, with coverage mapped to the MITRE ATT&CK matrix and every change promoted through CI/CD.",
                ),
                app(
                    "Exposure Manager",
                    "Vuln prioritization",
                    "zshield",
                    "Vulnerabilities ranked by exploitability, asset criticality and active-threat context so remediation effort goes to the exposures an adversary would actually use.",
                ),
            ],
            [
                uc(
                    "Threat Detection",
                    "Correlation",
                    "zshield",
                    "Correlating endpoint, identity, network and cloud signals into high-fidelity detections mapped to MITRE ATT&CK, across full-fidelity history rather than a truncated index.",
                    problem="Signals scattered across a dozen point tools and a two-week SIEM index mean multi-stage attacks are only correlated after the fact, once the retention window has already dropped the earliest evidence.",
                    who="SOC & Response",
                    how="Endpoint, identity and network telemetry land in Lakehouse//RT normalised to OCSF; detections mapped to ATT&CK are scored in Model Serving and surfaced to the SOC Triage Console.",
                    comps=["SOC Triage Console", "Lakehouse//RT", "Splunk Enterprise", "CrowdStrike Falcon", "Model Serving"],
                    stories=[
                        ["Barracuda: real-time threat detection, 75% lower cost", "https://www.databricks.com/customers/barracuda-networks/cybersecurity"],
                        ["Building the future of security with NAB and Lakewatch", "https://www.databricks.com/blog/building-future-security-nab-lakewatch"],
                    ],
                ),
                uc(
                    "Alert Triage & Dedup",
                    "Triage",
                    "gauge",
                    "Deduplicating and scoring the alert flood so analysts work a queue ordered by real risk instead of drowning in near-duplicate, low-context tickets.",
                    problem="Alert volume outruns analyst capacity: near-duplicate alerts from overlapping tools flood the queue, real incidents wait behind noise, and burnout drives inconsistent triage.",
                    who="SOC & Response",
                    how="Alerts are conformed and clustered in the lakehouse; a scoring and deduplication model in Model Serving orders the queue, and the result reaches analysts through the SOC Triage Console and Alert Dashboards.",
                    comps=["SOC Triage Console", "Model Serving", "Cortex XSOAR", "Lakehouse//RT", "Alert Dashboards"],
                    stories=[
                        ["Barracuda makes security logs conversational with Genie", "https://www.databricks.com/blog/barracuda-makes-security-logs-conversational-genie"],
                        ["Lakewatch: the open security lakehouse for the AI era", "https://www.databricks.com/product/lakewatch"],
                    ],
                ),
                uc(
                    "Threat Hunting",
                    "Proactive",
                    "observ",
                    "Hypothesis-driven hunting across months of full-fidelity telemetry to find the tradecraft no rule fired on, in plain English rather than gated on query-language fluency.",
                    problem="Hunting stops at the SIEM's retention wall and the analyst's SPL fluency; the long, quiet campaigns that matter most live in exactly the history that was aged out to save cost.",
                    who="Threat Intelligence",
                    how="Full-fidelity telemetry is retained in Delta Lake; hunters pivot in plain English through Genie on the Threat Hunt Workbench and turn confirmed findings into new detections.",
                    comps=["Threat Hunt Workbench", "Genie", "AI/BI", "Corelight NDR", "Delta Lake"],
                    stories=[
                        ["NAB hunts at scale on the open security lakehouse", "https://www.databricks.com/blog/building-future-security-nab-lakewatch"],
                        ["Lakewatch: AI-driven hunting on the lakehouse", "https://www.databricks.com/product/lakewatch"],
                    ],
                ),
                uc(
                    "Phishing & BEC Defense",
                    "Email threat",
                    "chat",
                    "Detecting phishing and business email compromise from behavioural signals across email, identity and message content rather than static rules and blocklists.",
                    problem="Socially engineered email and account-takeover BEC evade signature and rule-based filters, and the behavioural signal needed to catch them spans email, identity and history that legacy filters never see together.",
                    who="Detection Engineering",
                    how="Email, identity and content signals are joined in the lakehouse; behaviour models trained with Feature Store and tracked in MLflow score each message through Model Serving alongside Defender signals.",
                    comps=["Model Serving", "Microsoft Defender XDR", "Feature Store", "MLflow", "Detection Studio"],
                    stories=[
                        ["Abnormal Security scales behavioural email AI on Databricks", "https://www.databricks.com/customers/abnormal"],
                    ],
                ),
                uc(
                    "Insider Risk & UEBA",
                    "Behaviour",
                    "people",
                    "User and entity behaviour analytics that baseline normal activity and flag anomalous access, exfiltration and privilege misuse before it becomes a breach.",
                    problem="Insider threat and account misuse look like ordinary activity one event at a time; the anomaly only appears when identity, access and data-movement history are baselined together, which siloed tools cannot do.",
                    who="GRC & Compliance",
                    how="Identity, privileged-access and audit signals are conformed and joined with Enterprise Audit Marts; UEBA models in Model Serving score entity risk against learned baselines with governance in Unity Catalog.",
                    comps=["Model Serving", "Okta Identity Cloud", "CyberArk PAM", "Feature Store", "Enterprise Audit Marts"],
                    stories=[
                        ["Atlassian modernises threat detection on a security lakehouse", "https://www.databricks.com/customers/atlassian/security-lakehouse"],
                    ],
                ),
                uc(
                    "Vulnerability Triage",
                    "Exposure",
                    "gauge",
                    "Ranking vulnerabilities by exploitability, asset criticality and active-threat context so scarce remediation effort goes to the exposures an adversary would actually use.",
                    problem="Scanners return more critical findings than any team can patch, and raw CVSS scores ignore whether an asset is exposed, business-critical, or being actively exploited right now.",
                    who="GRC & Compliance",
                    how="Tenable and Qualys findings are joined to asset criticality and threat-intel exploitability in the lakehouse; a risk model in AI/BI and Model Serving ranks exposures in the Exposure Manager.",
                    comps=["Exposure Manager", "Tenable Nessus", "Qualys VMDR", "AI/BI", "Model Serving"],
                ),
                uc(
                    "Incident Forensics",
                    "Response",
                    "zshield",
                    "Reconstructing an intrusion end to end from full-fidelity history, and driving containment into the response tools without leaving the investigation.",
                    problem="When a breach is confirmed, responders need the full timeline across every tool, but the earliest evidence has usually aged out of the SIEM and stitching it back together by hand costs the hours that matter most.",
                    who="SOC & Response",
                    how="Full-fidelity endpoint and network evidence is queried from Delta Lake; the timeline is assembled in the SOC Triage Console with Genie, and containment is written back through EDR Host Isolation.",
                    comps=["SOC Triage Console", "Corelight NDR", "Delta Lake", "Genie", "EDR Host Isolation"],
                    stories=[
                        ["Atlassian: long-horizon investigations on the lakehouse", "https://www.databricks.com/customers/atlassian/security-lakehouse"],
                        ["Barracuda delivers alerts with full context in minutes", "https://www.databricks.com/customers/barracuda-networks/cybersecurity"],
                    ],
                ),
                uc(
                    "Detection-as-Code",
                    "Engineering",
                    "code",
                    "Treating detections as version-controlled, tested and CI/CD-deployed software, with coverage mapped to MITRE ATT&CK and every rule backtested against real history.",
                    problem="Detections hand-edited in SIEM consoles drift, go untested and leave silent coverage gaps; there is no peer review, no backtest against history and no map of what the estate can and cannot see.",
                    who="Detection Engineering",
                    how="Detections are authored in Detection Studio as Sigma, SQL and notebook code, backtested against Delta history, governed in Unity Catalog, and shipped through Detection CI/CD.",
                    comps=["Detection Studio", "Detection CI/CD", "Sigma Rule Sync", "Unity Catalog", "Genie Code"],
                    stories=[
                        ["Databricks announces Lakewatch: detection-as-code, agentic SIEM", "https://www.databricks.com/blog/databricks-announces-lakewatch-new-agentic-siem"],
                        ["Barracuda: detection rules managed and deployed automatically", "https://www.databricks.com/customers/barracuda-networks/cybersecurity"],
                    ],
                ),
                uc(
                    "Compliance Reporting",
                    "Governance",
                    "gavel",
                    "Producing control coverage and audit evidence for SOC 2, PCI DSS and NIST from the same governed tables the SOC runs on, rather than a separate reporting scramble.",
                    problem="Compliance evidence is reassembled by hand each cycle from tools the auditors cannot see into, and proving who accessed sensitive security data means bolt-on instrumentation the SIEM never captured.",
                    who="GRC & Compliance",
                    how="Control coverage and access evidence are produced from governed Gold tables with lineage and immutable audit logs in Unity Catalog, and surfaced through AI/BI and Compliance Reporting.",
                    comps=["Unity Catalog", "AI/BI", "Compliance Reporting", "Audit Evidence", "Regulatory Filings"],
                    stories=[
                        ["Barracuda: governed audit trail covers SOC 2 with Genie", "https://www.databricks.com/blog/barracuda-makes-security-logs-conversational-genie"],
                    ],
                ),
                uc(
                    "Security Lakehouse",
                    "SIEM cost & tiering",
                    "lakehouse",
                    "Retaining full-fidelity telemetry in open formats at cloud-commodity cost, tiering logs by source and value, and querying years of history instead of dropping data to fit a SIEM budget.",
                    problem="Per-gigabyte SIEM ingestion pricing forces teams to drop logs, shorten retention and ignore unstructured data, so detection and investigation run on incomplete evidence chosen by budget rather than risk.",
                    who="Security Leadership",
                    how="All telemetry lands in the Lakehouse in open OCSF, Delta and Iceberg formats with Auto Loader and Lakeflow, retained cheaply and governed in Unity Catalog, with compute paid only on query.",
                    comps=["Lakehouse", "Unity Catalog", "Delta Lake", "Lakeflow", "Auto Loader"],
                    stories=[
                        ["Atlassian: 80% reduction in ingestion overhead", "https://www.databricks.com/customers/atlassian/security-lakehouse"],
                        ["Lakewatch: retain 100% of telemetry, no SIEM tax", "https://www.databricks.com/blog/databricks-announces-lakewatch-new-agentic-siem"],
                    ],
                ),
            ],
        ),
        "sources": {
            "splunk": {"t": "Splunk Enterprise Security", "u": "https://www.splunk.com/en_us/products/enterprise-security.html"},
            "elastic": {"t": "Elastic Security (SIEM)", "u": "https://www.elastic.co/security"},
            "sentinel": {"t": "Microsoft Sentinel", "u": "https://www.microsoft.com/en-us/security/business/siem-and-xdr/microsoft-sentinel"},
            "chronicle": {"t": "Google Security Operations (Chronicle)", "u": "https://cloud.google.com/security/products/security-operations"},
            "crowdstrike": {"t": "CrowdStrike Falcon platform", "u": "https://www.crowdstrike.com/platform/"},
            "sentinelone": {"t": "SentinelOne Singularity platform", "u": "https://www.sentinelone.com/platform/"},
            "defender": {"t": "Microsoft Defender XDR", "u": "https://www.microsoft.com/en-us/security/business/siem-and-xdr/microsoft-defender-xdr"},
            "okta": {"t": "Okta Workforce Identity", "u": "https://www.okta.com/products/single-sign-on-workforce-identity/"},
            "entra": {"t": "Microsoft Entra ID", "u": "https://www.microsoft.com/en-us/security/business/microsoft-entra"},
            "cyberark": {"t": "CyberArk Privileged Access Manager", "u": "https://www.cyberark.com/products/privileged-access-manager/"},
            "tenable": {"t": "Tenable Nessus", "u": "https://www.tenable.com/products/nessus"},
            "qualys": {"t": "Qualys VMDR", "u": "https://www.qualys.com/apps/vulnerability-management-detection-response/"},
            "mandiant": {"t": "Mandiant Threat Intelligence", "u": "https://cloud.google.com/security/products/threat-intelligence"},
            "recorded-future": {"t": "Recorded Future Intelligence Cloud", "u": "https://www.recordedfuture.com/platform"},
            "paloalto": {"t": "Palo Alto Networks NGFW", "u": "https://www.paloaltonetworks.com/network-security/next-generation-firewall"},
            "zscaler": {"t": "Zscaler Internet Access", "u": "https://www.zscaler.com/products-and-solutions/zscaler-internet-access"},
            "corelight": {"t": "Corelight Open NDR", "u": "https://corelight.com/"},
            "wiz": {"t": "Wiz CNAPP", "u": "https://www.wiz.io/"},
            "ocsf": {"t": "Open Cybersecurity Schema Framework", "u": "https://ocsf.io/"},
            "kafka": {"t": "Apache Kafka", "u": "https://kafka.apache.org/"},
            "xsoar": {"t": "Palo Alto Cortex XSOAR", "u": "https://www.paloaltonetworks.com/cortex/cortex-xsoar"},
            "servicenow": {"t": "ServiceNow Security Operations", "u": "https://www.servicenow.com/products/security-operations.html"},
            "sigma": {"t": "Sigma detection rules (SigmaHQ)", "u": "https://sigmahq.io/"},
        },
    }
}
