import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import app, biz, cons_rail, fed_group, ing_rail, medallion, tile, top_band, uc


def ppl2(business_tiles, tech_tiles):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": tech_tiles[:3]},
    ]


INDUSTRIES_BATCH_CASINOS_GAMING = {
    "casinos_gaming": {
        "label": "Casinos & Resorts",
        "blurb": "Casino resorts and integrated gaming operators: slot and table floor operations, player loyalty and host development, hotel and F&B, sportsbook and iGaming, and AML and responsible-gaming compliance.",
        "medallion": medallion(
            "Raw gaming and property feeds",
            "Slot machine SAS and G2S meters, table-game ratings, PMS folios and F&B checks, sportsbook and iGaming bet feeds, loyalty transactions and cage entries, landed exactly as received so a jackpot, a rating or a marker can always be replayed as it stood.",
            "Conformed player, trip, property",
            "Patrons, trips and gaming sessions resolved into single conformed entities across the casino floor, hotel, F&B and online estates, with loyalty accounts, hotel guests and online wallets matched to one player and theoretical and actual win reconciled per session.",
            "Theo win, ADT, reinvestment",
            "Contracted products the property runs on: theoretical and actual win and hold by area, average daily theoretical and worth by player, reinvestment and comp ratios, RevPAR and occupancy, and Title 31 and responsible-gaming exposure.",
        ),
        "rails": {
            "src": [
                {
                    "box": "Casino Management",
                    "ic": "erp",
                    "tiles": [
                        tile(
                            "IGT Advantage",
                            "erp",
                            "The casino management system of record: slot and table player tracking, floor accounting, jackpots and bonusing, and the source of carded play and theoretical win.",
                            "igt-advantage",
                        ),
                        tile(
                            "Aristocrat Oasis 360",
                            "erp",
                            "The Bally-lineage casino management and player-tracking system, the incumbent floor system where IGT is not, feeding the same rating and win entities.",
                            "oasis",
                        ),
                        tile(
                            "Konami SYNKROS",
                            "product",
                            "Casino management and loyalty platform for slot and table tracking, promotions and bonusing across the floor.",
                            "synkros",
                        ),
                        tile(
                            "Everi CashClub",
                            "product",
                            "Cage, kiosk and cashless-wallet system: ticket redemption, funds access and the cashless play the floor increasingly runs on.",
                            "everi",
                        ),
                    ],
                },
                {
                    "box": "Hotel & F&B",
                    "ic": "custlake",
                    "tiles": [
                        tile(
                            "Agilysys Stay/LMS",
                            "erp",
                            "The property management system for casino resorts: reservations, folios, comps and group blocks, the system of record for the hotel side of the trip.",
                            "agilysys",
                        ),
                        tile(
                            "Oracle OPERA PMS",
                            "erp",
                            "Hospitality property management for rooms, rates and guest profiles, the incumbent PMS where OPERA is the resort standard.",
                            "opera",
                        ),
                        tile(
                            "Agilysys InfoGenesis",
                            "product",
                            "Point of sale for restaurants, bars and retail across the property, the source of F&B checks and non-gaming spend.",
                            "agilysys",
                        ),
                        tile(
                            "Oracle Simphony POS",
                            "product",
                            "Enterprise restaurant point of sale for outlets and banqueting, feeding the same F&B and non-gaming revenue entities.",
                            "simphony",
                        ),
                    ],
                },
                {
                    "box": "Sportsbook & iGaming",
                    "ic": "market",
                    "tiles": [
                        tile(
                            "Kambi Sportsbook",
                            "market",
                            "Sportsbook platform for odds, risk management and bet settlement across retail and online, the trading engine behind the book.",
                            "kambi",
                        ),
                        tile(
                            "OpenBet Platform",
                            "product",
                            "Sports-betting engine for bet capture, pricing and settlement at scale, the incumbent platform where OpenBet runs the book.",
                            "openbet",
                        ),
                        tile(
                            "IGT PlayDigital",
                            "product",
                            "Online casino and iGaming platform: game content, player wallet and remote game server for the digital estate.",
                            "igt-playdigital",
                        ),
                        tile(
                            "L&W OpenGaming",
                            "product",
                            "Light & Wonder's content aggregation and remote game server distributing casino games across online operators.",
                            "lnw-opengaming",
                        ),
                    ],
                },
                {
                    "box": "Loyalty & Marketing",
                    "ic": "partner",
                    "tiles": [
                        tile(
                            "Player Loyalty/CRM",
                            "custlake",
                            "Tier status, points, earn-and-burn and offer history, the profile every host action and reinvestment decision is scored against.",
                        ),
                        tile(
                            "SF Marketing Cloud",
                            "crm",
                            "Campaign orchestration, journeys and email across the player base, executing the offers and communications the property sends.",
                            "sfmc",
                        ),
                        tile(
                            "Host Management",
                            "people",
                            "Host books, contacts and trip planning for premium and VIP players, the source of relationship and reinvestment activity.",
                        ),
                        tile(
                            "Web & App Clickstream",
                            "observ",
                            "Search, browse and session events from the property's web and mobile app, joined to play for online engagement analysis.",
                        ),
                    ],
                },
                {
                    "box": "Cage, Credit & Comp.",
                    "ic": "gavel",
                    "tiles": [
                        tile(
                            "Cage & Credit",
                            "db",
                            "Cage transactions, markers, front-money and credit lines, the ledger Title 31 aggregation and AML monitoring run against.",
                        ),
                        tile(
                            "Title 31 / FinCEN",
                            "gavel",
                            "Currency-transaction and suspicious-activity reporting under the Bank Secrecy Act, the regulatory obligation the gaming day is measured against.",
                            "fincen",
                        ),
                        tile(
                            "Surveillance / SDS",
                            "iot",
                            "Surveillance and incident systems: game protection, exclusions and integrity events joined to play for investigation.",
                        ),
                    ],
                },
                fed_group(
                    "Casino Accounting",
                    "Revenue-audit, general-ledger and gaming-tax marts left where they are and queried in place under Unity Catalog, which avoids a second copy of the audited win.",
                ),
            ],
            "ing": ing_rail(
                [
                    tile(
                        "Slot Floor SAS/G2S",
                        "iot",
                        "Streaming meter, handle-pull and event messages from the slot floor over the SAS and G2S protocols, the ground truth for coin-in, win and machine state.",
                    ),
                    tile(
                        "Sportsbook Bet Stream",
                        "stream",
                        "Real-time bet, odds and settlement events from the sportsbook and iGaming platforms, the live feed liability and trading are managed against.",
                    ),
                    tile(
                        "TCS Table Radar",
                        "iot",
                        "RFID chip and table-monitoring events from the pit, giving table games the ratings and drop accuracy slots have had for years.",
                        "tcsjohnhuxley",
                    ),
                ]
            ),
            "ppl": ppl2(
                [
                    biz(
                        "Property Execs",
                        "Genie One",
                        "The CEO and property president on total gaming and non-gaming revenue and EBITDA; the CFO on cash, credit and the cost of reinvestment; the general manager on floor performance, hotel occupancy and the guest experience across the property.",
                        [
                            ["Genie One", "Ask what the floor won last night or what a segment is worth this month without booking analyst time."],
                            ["AI/BI", "Gaming win, ADT, RevPAR and reinvestment on one certified set of Metric Views."],
                            ["Unity Catalog", "Certification and the business glossary, so \"theo win\" and \"worth\" mean one thing across the property."],
                        ],
                        sub=[
                            ["CEO / President", "total gaming and non-gaming revenue, EBITDA and the property story."],
                            ["CFO & Finance", "cash, credit exposure and the cost of reinvestment."],
                            ["General Manager", "floor performance, occupancy and the guest experience."],
                        ],
                        ucs=["Hotel Yield & RevPAR", "Slot Floor Analytics", "Player 360"],
                    ),
                    biz(
                        "Casino Ops",
                        "Lakehouse//RT",
                        "Slot operations managers on floor mix, denomination and performance by bank; table games on hold, game protection and dealer productivity; the sportsbook and surveillance teams on live risk, limits and integrity across the floor and online.",
                        [
                            ["Floor Performance", "Slot and table performance by machine and pit at the latency the floor moves at."],
                            ["Lakehouse//RT", "Live meter, rating and bet state joined as the session unfolds."],
                            ["Model Serving", "Slot-placement, hold and risk models scored in the operational path."],
                        ],
                        sub=[
                            ["Slot Operations", "floor mix, denomination and performance by bank."],
                            ["Table Games", "hold, game protection and dealer productivity."],
                            ["Sportsbook & Surveillance", "live risk, limits and floor integrity."],
                        ],
                        ucs=["Slot Floor Analytics", "Sportsbook Trading", "Fraud & Bonus Abuse"],
                    ),
                    biz(
                        "Player Dev",
                        "Model Serving",
                        "Casino hosts managing their book of premium and VIP players; player-development analysts on trip planning, reinvestment and reactivation; the loyalty team on tier economics, earn-and-burn and the worth of every carded player.",
                        [
                            ["Host Cockpit", "Each host's book with worth, trip pace and next-best action on Lakebase."],
                            ["Model Serving", "Worth, churn and offer-response models scored per player."],
                            ["CustomerLake", "The player profile activated across gaming, hotel and online without a separate CDP."],
                        ],
                        sub=[
                            ["Casino Hosts", "the book of premium and VIP players and their trips."],
                            ["Player Development", "trip planning, reinvestment and reactivation."],
                            ["Loyalty & Rewards", "tier economics, earn-and-burn and carded worth."],
                        ],
                        ucs=["Host & Player Dev", "Player 360", "Reinvestment & Comps"],
                    ),
                    biz(
                        "Marketing",
                        "AI/BI",
                        "The CMO and database-marketing team on segmentation and campaign lift; the reinvestment and offer team on comp mail, free play and the cost of every offer; the digital and iGaming marketers on acquisition, cross-sell and online lifetime value.",
                        [
                            ["AI/BI", "Segment worth, offer cost and campaign lift on certified Metric Views."],
                            ["Reinvestment Studio", "Offer and free-play decisions costed against predicted response."],
                            ["Model Serving", "Response, cross-sell and churn propensity scored per player."],
                        ],
                        sub=[
                            ["Database Marketing", "segmentation, campaign design and measured lift."],
                            ["Reinvestment & Offers", "comp mail, free play and offer economics."],
                            ["Digital & iGaming", "acquisition, cross-sell and online lifetime value."],
                        ],
                        ucs=["Reinvestment & Comps", "Player 360", "iGaming Offers"],
                    ),
                    biz(
                        "Compliance",
                        "Unity Catalog",
                        "The compliance officer on Title 31 currency reporting and SAR filing; the AML team on structuring, source-of-funds and sanctions screening; the responsible-gaming team on markers of harm, self-exclusion and duty-of-care intervention.",
                        [
                            ["AML Watchtower", "CTR and SAR candidates and RG risk flags on one governed screen."],
                            ["Unity Catalog", "One governed, auditable definition of a reportable event across the estate."],
                            ["AI Functions", "Marker notes, KYC documents and alerts parsed and classified at scale."],
                        ],
                        sub=[
                            ["Compliance Officer", "Title 31 currency reporting and SAR filing."],
                            ["AML & KYC", "structuring, source-of-funds and sanctions screening."],
                            ["Responsible Gaming", "markers of harm, self-exclusion and intervention."],
                        ],
                        ucs=["AML & Title 31", "Responsible Gaming", "Fraud & Bonus Abuse"],
                    ),
                ],
                [
                    biz(
                        "Gaming Data Eng",
                        "Lakeflow",
                        "Land the slot SAS and G2S meters, table ratings, PMS and POS folios, sportsbook and iGaming feeds and loyalty transactions; own the Bronze to Silver path and the pager when the floor and reinvestment tables stall.",
                        [
                            ["Lakeflow Connect", "Managed connectors for the CMS, PMS, POS and loyalty cores."],
                            ["Lakeflow Designer", "Declarative pipelines with expectations on meter, rating and bet feeds."],
                            ["Lakewatch", "Freshness on the floor and marketing tables hosts and analysts read each morning."],
                        ],
                    ),
                    biz(
                        "Casino ML",
                        "MLflow",
                        "Worth, churn, offer-response, slot-placement and responsible-gaming risk models built from carded play, ratings and online behaviour; whether they still hold as the floor mix and player base shift.",
                        [
                            ["Feature Store", "Player, session and rating features read identically in training and serving."],
                            ["MLflow", "Every worth and risk model tracked for audit and reproduction."],
                            ["Model Serving", "Worth, response and risk models scored inside the operational path."],
                        ],
                    ),
                    biz(
                        "App Developers",
                        "Apps",
                        "Ship the host, floor, reinvestment and compliance applications the property works in, hosted next to governed data with writes back into the CMS, PMS and loyalty systems.",
                        [
                            ["Apps", "Host, floor and compliance screens with no separate web tier to run or secure."],
                            ["Lakebase", "Serverless Postgres for host actions, offer state and case notes with governed writes."],
                            ["Agent Bricks", "Agents that draft a host offer or a SAR narrative against governed tools."],
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
                                "Floor, marketing and finance dashboards against serverless SQL with Unity Catalog permissions enforced end to end.",
                            ),
                            tile(
                                "Microsoft Teams",
                                "chat",
                                "Genie in Teams for governed answers on win, worth and reinvestment in the channel the property already works in (Beta).",
                            ),
                            tile(
                                "Notebooks & IDEs",
                                "notebook",
                                "Analyst and data-science notebooks and IDEs against governed player, floor and online data.",
                            ),
                        ],
                    },
                    {
                        "box": "Distribution & Partners",
                        "ic": "partner",
                        "tiles": [
                            tile(
                                "Sportsbook Partners",
                                "api",
                                "Odds, risk and settlement exchanged with the sportsbook and iGaming platform providers over governed APIs.",
                                "kambi",
                            ),
                            tile(
                                "Affiliate Networks",
                                "partner",
                                "Acquisition, referral and revenue-share data reconciled with affiliate and media partners for the online business.",
                            ),
                            tile(
                                "Data Sharing",
                                "share",
                                "Exposure, performance and audience segments shared to partners and jurisdictions over Delta Sharing rather than file exchange.",
                            ),
                        ],
                    },
                    {
                        "box": "Operational Writeback",
                        "ic": "opdb",
                        "tiles": [
                            tile(
                                "CMS Offer Writeback",
                                "erp",
                                "Free play, comps and reinvestment decisions written back into the casino management system so the offer reaches the player's card.",
                                "igt-advantage",
                            ),
                            tile(
                                "PMS & Kiosk Offers",
                                "db",
                                "Room offers and rates written into the property management system and to the kiosk so the answer reaches check-in and the floor.",
                                "opera",
                            ),
                            tile(
                                "Player App Push",
                                "apps",
                                "Personalised offers, RG nudges and event invites pushed to the mobile app and reels the player actually carries.",
                            ),
                        ],
                    },
                    {
                        "box": "Regulatory & Reporting",
                        "ic": "gavel",
                        "tiles": [
                            tile(
                                "Gaming Board & MICS",
                                "gavel",
                                "Regulatory, MICS and revenue-audit submissions to the gaming control board produced from the same governed tables the property runs on.",
                            ),
                            tile(
                                "Title 31 Reporting",
                                "sheet",
                                "CTR, SAR and 8300 filings to FinCEN filed from contracted Gold products with a full audit trail.",
                                "fincen",
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
                                "Partners, auditors and jurisdictions reading live tables with no copy and no egress duplication.",
                            ),
                        ],
                    },
                ]
            ),
        },
        "top": top_band(
            [
                app(
                    "Host Cockpit",
                    "Player development",
                    "gauge",
                    "The screen a casino host runs their book from: each player's worth, trip pace, offer history and next-best action, with reinvestment room and RG flags in one view, on Databricks Apps over Lakebase.",
                ),
                app(
                    "Floor Performance",
                    "Slot & table ops",
                    "market",
                    "Live slot and table performance by machine, bank and pit against theoretical, so operations move underperforming units and rebalance the floor on evidence rather than instinct.",
                ),
                app(
                    "Reinvestment Studio",
                    "Offers & comps",
                    "chart",
                    "Where database marketing sizes comp mail, free play and offers against predicted response and worth, so reinvestment is spent on the players who return it.",
                ),
                app(
                    "AML Watchtower",
                    "Compliance & RG",
                    "gavel",
                    "CTR and SAR candidates, structuring alerts and responsible-gaming risk flags ranked with the play and cage evidence that supports them, so compliance works the strongest cases first.",
                ),
            ],
            [
                uc(
                    "Player 360",
                    "Single patron view",
                    "custlake",
                    "One governed view of the patron across slot and table play, hotel, F&B, loyalty and online, so worth, segment and next offer are based on the whole relationship, not one system's slice.",
                    problem="Player data sits in the casino management system, the PMS, the POS, the loyalty engine and the online wallet; stitched by hand, worth is understated, VIPs are missed and every team markets to a different version of the same patron.",
                    who="Marketing",
                    how="Slot, table, hotel, F&B and online feeds are matched to one patron through CustomerLake without a separate CDP; worth and segment are scored in Model Serving and surfaced in AI/BI and the Host Cockpit.",
                    comps=["Host Cockpit", "CustomerLake", "Model Serving", "IGT Advantage", "AI/BI"],
                    stories=[
                        ["SciPlay unifies player data to lift retention", "https://www.databricks.com/customers/sciplay"],
                        ["Bally's scales real-time gaming intelligence", "https://www.databricks.com/customers/ballys"],
                    ],
                ),
                uc(
                    "Slot Floor Analytics",
                    "Floor optimisation",
                    "market",
                    "Slot and table performance by machine, denomination and pit against theoretical win, so the floor mix, placement and par are set on evidence and underperforming units are moved before a quarter is lost.",
                    problem="Floor decisions ride on gut and stale reports; without meter-level performance against theoretical, poor performers hold prime space while winners sit in corners, and the mix drifts from what the players actually play.",
                    who="Casino Ops",
                    how="SAS and G2S meters and table ratings land through Lakeflow into the lakehouse; performance against theoretical is modelled in Model Serving and explored in AI/BI and the Floor Performance app.",
                    comps=["Floor Performance", "Slot Floor SAS/G2S", "AI/BI", "Aristocrat Oasis 360", "Model Serving"],
                    stories=[
                        ["The Rank Group improves player experience on Lakeflow", "https://www.databricks.com/customers/the-rank-group-plc/lakeflow-jobs"],
                    ],
                ),
                uc(
                    "Reinvestment & Comps",
                    "Offer economics",
                    "chart",
                    "Sizing comp mail, free play and offers against each player's predicted response and worth, so reinvestment lands on the players who return it instead of the same mass drop to everyone.",
                    problem="Reinvestment is the property's largest discretionary spend, yet offers go out on tier and gut; over-mailed to some and under to others, free play is given away where it changes nothing and withheld where it would have brought a trip.",
                    who="Marketing",
                    how="Carded play and response history are conformed in the lakehouse; response and worth models score each offer through Model Serving, and the Reinvestment Studio costs the drop before it is mailed.",
                    comps=["Reinvestment Studio", "CustomerLake", "Model Serving", "Konami SYNKROS", "AI/BI"],
                    stories=[
                        ["Tabcorp personalises offers and saves $1.75M", "https://www.databricks.com/customers/tabcorp"],
                    ],
                ),
                uc(
                    "Host & Player Dev",
                    "VIP hosting",
                    "people",
                    "Giving each host a live book of their players with worth, trip pace and next-best action, so premium and VIP relationships are worked proactively rather than reconstructed from yesterday's reports.",
                    problem="Hosts fly blind between systems: a VIP's slowing trip pace or a reactivation window is invisible until the play is already gone, and the host learns worth from a spreadsheet a day late.",
                    who="Player Dev",
                    how="Player worth, trip-pace and churn signals are scored in Model Serving and served into the Host Cockpit on Lakebase, with Genie One answering ad-hoc questions on a player's history.",
                    comps=["Host Cockpit", "CustomerLake", "Model Serving", "Genie One", "Lakebase"],
                ),
                uc(
                    "Responsible Gaming",
                    "Duty of care",
                    "zshield",
                    "Detecting markers of harm from play, deposit and session behaviour and delivering the right intervention at the right time, to protect players and meet a growing duty-of-care obligation.",
                    problem="Signals of harm are spread across gaming, deposit and session data and surface too late; without scoring behaviour continuously, at-risk players are identified after the damage and regulators after the fact.",
                    who="Compliance",
                    how="Play, deposit and session feeds stream into Lakehouse//RT; risk models score markers of harm in Model Serving and AI Functions classifies interactions, driving governed interventions from the AML Watchtower under Unity Catalog.",
                    comps=["AML Watchtower", "Model Serving", "Lakehouse//RT", "AI Functions", "Unity Catalog"],
                    stories=[
                        ["Responsible Gaming Solution Accelerator", "https://www.databricks.com/solutions/accelerators/responsible-gaming"],
                        ["Tabcorp advances safer gambling with real-time data", "https://www.databricks.com/customers/tabcorp"],
                    ],
                ),
                uc(
                    "AML & Title 31",
                    "Financial crime",
                    "gavel",
                    "Aggregating cage, marker and wallet activity to identify currency-transaction reports, structuring and suspicious activity, so Title 31 filing is complete, timely and defensible.",
                    problem="Title 31 aggregation spans the cage, slots, tables and online wallet across a gaming day; done by hand it misses structuring and multi-station patterns, and a late or missed SAR is a regulatory exposure.",
                    who="Compliance",
                    how="Cage, marker and wallet activity are conformed in the lakehouse; aggregation and structuring models score CTR and SAR candidates in Model Serving, and AI Functions drafts narratives from marker and KYC notes for the AML Watchtower.",
                    comps=["AML Watchtower", "Cage & Credit", "AI Functions", "Model Serving", "Unity Catalog"],
                ),
                uc(
                    "Sportsbook Trading",
                    "Risk & pricing",
                    "market",
                    "Pricing markets, managing liability and personalising the sportsbook in real time, so odds, limits and content respond to the book and the player as the bets come in.",
                    problem="Bets and market moves arrive faster than batch pipelines can answer; without real-time liability and player data, prices lag, sharp action goes unmanaged and content is the same for every customer.",
                    who="Casino Ops",
                    how="The bet and odds stream lands in Lakehouse//RT; pricing, liability and personalisation models score each request through Model Serving behind the sportsbook platform, with AI/BI on the trading position.",
                    comps=["Kambi Sportsbook", "Lakehouse//RT", "Model Serving", "Sportsbook Bet Stream", "AI/BI"],
                    stories=[
                        ["Sportsbet builds a real-time personalization engine", "https://www.databricks.com/customers/sportsbet"],
                        ["Kaizen Gaming ports sportsbook personalization in days", "https://www.databricks.com/customers/kaizen-gaming"],
                    ],
                ),
                uc(
                    "iGaming Offers",
                    "Online personalisation",
                    "custlake",
                    "Personalising game recommendations, bonuses and content across the online casino and app, scored per player against behaviour the online estate already holds.",
                    problem="Online players see the same lobby, the same bonus and the same games; the behavioural signal needed to personalise the experience exists behind the iGaming platform, unused, while acquisition cost keeps rising.",
                    who="Marketing",
                    how="Online session and wager behaviour is activated through CustomerLake; recommendation and bonus-response models score each player in Model Serving with AI Search over the game catalogue, served from Lakehouse//RT into the app.",
                    comps=["IGT PlayDigital", "CustomerLake", "Model Serving", "AI Search", "Lakehouse//RT"],
                    stories=[
                        ["Kaizen Gaming delivers real-time AI to players", "https://www.databricks.com/customers/kaizen-gaming"],
                        ["SciPlay launches games 75% faster with the lakehouse", "https://www.databricks.com/customers/sciplay"],
                    ],
                ),
                uc(
                    "Hotel Yield & RevPAR",
                    "Resort revenue",
                    "sheet",
                    "Setting room rates and comp-room allocation against gaming worth, so the room is priced on the whole relationship and RevPAR is optimised for the property, not just the hotel.",
                    problem="The hotel prices rooms in isolation from the casino, so a comp room is given to a low-worth guest while a high-worth player pays rack or books elsewhere, and RevPAR is optimised against the wrong objective.",
                    who="Property Execs",
                    how="PMS occupancy and rate data are conformed with gaming worth in the lakehouse; yield and comp-allocation are modelled in Model Serving and explored in AI/BI, with Genie One answering rate and occupancy questions.",
                    comps=["Oracle OPERA PMS", "AI/BI", "Model Serving", "Agilysys Stay/LMS", "Genie One"],
                ),
                uc(
                    "Fraud & Bonus Abuse",
                    "Integrity",
                    "gavel",
                    "Detecting collusion, chip-dumping, bonus abuse and payment fraud across the floor and online, so integrity threats are caught as they happen rather than found in the monthly reconciliation.",
                    problem="Fraud crosses the floor and the online estate: bonus abuse, chip-dumping and payment fraud hide in high-frequency play and deposit data that batch reconciliation only surfaces after the money is gone.",
                    who="Compliance",
                    how="Floor, wallet and payment feeds land in Lakehouse//RT; anomaly and collusion models built on Feature Store score activity in Model Serving and flag cases in the AML Watchtower.",
                    comps=["AML Watchtower", "Model Serving", "Lakehouse//RT", "IGT PlayDigital", "Feature Store"],
                    stories=[
                        ["Bally's supports fraud detection and compliance", "https://www.databricks.com/customers/ballys"],
                    ],
                ),
            ],
        ),
        "sources": {
            "igt-advantage": {"t": "IGT Advantage casino management", "u": "https://en.wikipedia.org/wiki/International_Game_Technology"},
            "oasis": {"t": "Bally / Aristocrat Oasis 360", "u": "https://en.wikipedia.org/wiki/Bally_Technologies"},
            "synkros": {"t": "Konami SYNKROS casino management", "u": "https://www.konamigaming.com/systems/synkros/"},
            "everi": {"t": "Everi cashless and cage", "u": "https://www.everi.com"},
            "agilysys": {"t": "Agilysys hospitality software", "u": "https://www.agilysys.com/"},
            "opera": {"t": "Oracle OPERA property management", "u": "https://www.oracle.com/hospitality/hotel-property-management/"},
            "simphony": {"t": "Oracle Simphony POS (MICROS)", "u": "https://en.wikipedia.org/wiki/MICROS_Systems"},
            "kambi": {"t": "Kambi sportsbook platform", "u": "https://www.kambi.com/"},
            "openbet": {"t": "OpenBet sports-betting engine", "u": "https://www.openbet.com/"},
            "igt-playdigital": {"t": "IGT PlayDigital iGaming", "u": "https://www.igt.com/products-and-services/igaming"},
            "lnw-opengaming": {"t": "Light & Wonder OpenGaming", "u": "https://www.opengaming.com/"},
            "sfmc": {"t": "Salesforce Marketing Cloud", "u": "https://www.salesforce.com/products/marketing-cloud/overview/"},
            "fincen": {"t": "FinCEN Title 31 / BSA reporting", "u": "https://www.fincen.gov/"},
            "tcsjohnhuxley": {"t": "TCS John Huxley table systems", "u": "https://www.tcsjohnhuxley.com/"},
        },
    }
}
