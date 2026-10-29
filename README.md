# DFX Intelligence: MCP server

[![DFX Intelligence MCP server: quality and maintenance score on Glama](https://glama.ai/mcp/servers/Capital-W-Holdings/us-property-parcel-real-estate-debt/badges/score.svg)](https://glama.ai/mcp/servers/Capital-W-Holdings/us-property-parcel-real-estate-debt)

**Private credit research for agents.** Ask which lenders finance a company, which BDCs hold a borrower's loans and when they mature, which sponsors a lender backs, and which institutions allocate to private credit. Every answer is built only from cited claims read from primary documents (BDC schedules of investments filed with the SEC, Form ADV and IAPD, public pension commitment reports), with the source and the observation date on every row.

**DFX Intelligence.** Evidence-backed private capital intelligence platform for AI agents, 136 MCP tools across private credit, BDC portfolios and lenders; private equity firms, funds and deals; venture capital; family offices; RIAs and advisor moves; independent sponsors; allocators and LP commitments; real estate funds; US real estate debt and property records. Facts carry their source and observation date, and every answer states OK, NO_MATCH, NOT_COVERED or UNKNOWN rather than guessing. 131 of 136 tools are free to call with no key; 5 save an account's own research watches and need an account key. Without a DFX plan, list answers name the first rows and count the rest, and contact values are never returned. For agents: [https://dfxintel.com/agents](https://dfxintel.com/agents).

## Connect

**Endpoint (start here, anonymous):** `https://exchange-production-9123.up.railway.app/mcp/core?c=gh-repo`
**Member sign-in (OAuth 2.1):** `https://exchange-production-9123.up.railway.app/mcp/core/member`
**Full profile:** `https://exchange-production-9123.up.railway.app/mcp?c=gh-repo`
**Transport:** Streamable HTTP
**Auth:** none for anonymous reads; OAuth 2.1 sign-in on dfxintel.com or a `dfx_live_` account key for members
**Registry:** `io.github.Capital-W-Holdings/us-property-parcel-real-estate-debt`

The core profile leads with `research`: one question, answered in one call, with the reads it composes.
The full profile lists `research` first too, then every read tool. Members sign in at the member URL (it is never tagged,
because the OAuth resource must match exactly), or send `Authorization: Bearer dfx_live_...` on either anonymous URL.

131 of 136 tools are free with no key, no sign-up and no OAuth. The other 5 (`watch_cancel`, `watch_changes`, `watch_create`, `watch_list` and `watch_reevaluate`) save an account's own research watches and need an account key. A list answer to an anonymous caller names its first 5 rows and counts the rest, and says what it withheld. Contact values are never returned.

```bash
claude mcp add --transport http dfx 'https://exchange-production-9123.up.railway.app/mcp/core?c=gh-repo'
```

Example call on the core profile:

```json
{"name": "research", "arguments": {"question": "Which BDCs hold the loans of Hyland Software and when do they mature?"}}
```

> Every number on this page is measured against production, not typed. Last measured
> **2026-10-29**. Call `dfx_coverage` for the same grid at the moment you read it.

---

## Beyond private credit: US real estate debt and property records

The other graphs (family offices, independent sponsors, venture capital) follow in [Beyond real estate](#beyond-real-estate-family-offices-independent-sponsors-venture-capital).

The real estate domain answers dated questions about two things: **United States commercial and
federal-programme real estate debt**, where loan maturities are published across
52 state codes, compliance expiries across 56 and subsidy expiries across
54, and **property records**, where 2,479,346 New York, Ohio, Washington, Massachusetts and Illinois parcels carry
ownership and assessed value and 95,616 recorded sale instruments cover the District of Columbia, Massachusetts, New York and Wisconsin.
Call it when an agent needs to know who owns a specific building, what it last sold
for, or which loans and subsidies come due in a given state and time window, with the
source and the observation date attached to every claim.

**Coverage is deliberately uneven and it is stated up front rather than discovered by
trial.**

United States, unevenly. NATIONAL: federal programme debt and maturities, LIHTC, HUD
subsidy, distress and commercial tenancy. MASSACHUSETTS ONLY: parcels and ownership.
RECORDED SALES: Massachusetts statewide, plus New York City deeds at or above $10m.
BOSTON ONLY: permits and certificates of occupancy. coverage_by_event_type below is the
measured grid, per event family, per state.

The measured per-type, per-state numbers are in
[Event coverage, measured](#event-coverage-measured) below, and `dfx_coverage` returns
the same grid at call time so an agent never has to guess from an empty result.

A tool that answers "no" clearly is worth more to an agent than one that answers an
empty list, so this server refuses unknown arguments with the served vocabulary
attached.

---

## Read the schemas before you call anything

A plain `GET` on the full profile returns the full tool list, the coverage numbers and a
worked example. No handshake, no session, no `initialize`.

```bash
curl -s 'https://exchange-production-9123.up.railway.app/mcp?c=gh-repo'
```

Then call a real estate tool over JSON-RPC (the real estate tools are on the full profile):

```bash
curl -s 'https://exchange-production-9123.up.railway.app/mcp?c=gh-repo' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":
       {"name":"resolve_address","arguments":
        {"address":"100 Binney St","city":"Cambridge","state":"MA"}}}'
```

That address returns a parcel carrying a recorded sale, with the registry book and
page it was recorded under.

### If you are a harvester rather than a caller

The endpoint serves the discovery conventions from its own origin, so an index does
not have to guess and does not have to be told:

| path | what it is |
|---|---|
| [`/llms.txt`](https://exchange-production-9123.up.railway.app/llms.txt) | the entry point, for something holding only this host name |
| [`/.well-known/ard.json`](https://exchange-production-9123.up.railway.app/.well-known/ard.json) | Agentic Resource Discovery catalog |
| [`/.well-known/mcp/server-cards.json`](https://exchange-production-9123.up.railway.app/.well-known/mcp/server-cards.json) | MCP server card |
| [`/.well-known/agent-card.json`](https://exchange-production-9123.up.railway.app/.well-known/agent-card.json) | A2A style agent card |
| [`/agents.txt`](https://exchange-production-9123.up.railway.app/agents.txt) | the agents.txt convention |
| [`/openapi.json`](https://exchange-production-9123.up.railway.app/openapi.json) | the same capabilities over plain HTTP |
| [`/robots.txt`](https://exchange-production-9123.up.railway.app/robots.txt) | crawlers and agents are welcome, and it says so |

`agents.txt` names no payment protocol because nothing on this server is priced.

---

## The 136 tools

| Tool | Takes | Returns | Price |
|---|---|---|---|
| `research` | as_of?, continue?, depth?, detail?, entity?, question?, ... | One private markets question in one call: BDC and private credit lenders, borrowers, loans, maturities and non-accrual, sponsors, advisers, teams, pension commi... | free |
| `resolve_address` | address, city?, state? | canonical DFX ids with the match basis and any ambiguity | free |
| `resolve_organization` | name | entity ids for owners, managers, lenders, servicers | free |
| `get_occupancy` | a property or company id, or a company name with an address | who is observed to occupy a building, or where a company operates, with the evidence tier | free |
| `get_property_record` | a DFX id | state, dated events, relationships, debt with maturity dates, recorded sales, provenance | free |
| `search_property_events` | event_type?, state?, within_days? | dated events with provenance | free |
| `search_bank_cre_exposure` | state?, name?, CRE-to-equity range?, above_guidance?, min_assets_usd?, min_noncurrent_pct?, sort? | FDIC-insured banks by CRE concentration with the guidance screen and UBPR percentile ranks | free |
| `search_subsidised_housing` | state?, city?, program?, min_waiting_months?, occupancy range?, min_units? | HUD-subsidised projects with units available, occupancy, months on the waiting list, rent, income and HUD spend, one annual capture | free |
| `search_parcels` | filters | parcels by attribute rather than by an address you already knew | free |
| `what_can_dfx_answer` | an objective, in natural language | whether DFX can help, which tool to call, the arguments, and a free sample | free |
| `changes_since` | an opaque cursor | what DFX has **learned** since your cursor | free |
| `debt_maturity_schedule` | state, within_days?, limit? | the loan tape: principal, lender, instrument, maturity, secured property | free |
| `dfx_coverage` | nothing | measured coverage, served sources, object types, known gaps | free |
| `search_family_offices` | allocates_to_managers?, asset_class?, city?, class?, co_invested_with?, counterparty_kind?, ... | Family offices as compact cards: class (single, multi, embedded...) with confidence, whether they invest directly, sectors and asset classes on record, check si... | free |
| `rank_family_offices` | allocates_to_managers?, asset_classes?, backs_independent_sponsors?, capital_max_usd?, capital_min_usd?, check_max_usd?, ... | THE tool for any family office question with criteria (sector, check size, capital, sponsors, co-investors, recent events, geography, reachable people) | free |
| `get_family_office` | dfx_id | The full card for one family office: profile, AUM / RAUM / 13F value kept apart with their as-of dates, behaviour, the people who run it with roles, its observe... | free |
| `search_family_office_investments` | asset_class?, include_candidates?, investment_kind?, limit?, office_dfx_id?, sector?, ... | Dated investments family offices have been observed making: target, sector, asset class, structure, control or minority, lead or participant, amounts where disc... | free |
| `search_independent_sponsors` | city?, include_unverified?, kind?, limit?, min_confidence?, query?, ... | Verified independent sponsor firms (deal-by-deal acquirers of lower middle market companies) as compact cards: verification status, classification, mandate summ... | free |
| `get_independent_sponsor` | dfx_id | The full card for any entity on the sponsor graph: a sponsor (with its verification status, the companies resembling its observed deals as counted facts and rea... | free |
| `search_sponsor_capital_providers` | limit?, making_new_investments?, min_fund_size_usd?, provider_type?, query?, sbic_licensed?, ... | SBICs, mezzanine and private equity funds, and family offices observed providing capital to independent sponsors: provider type, strategy, fund style, fund size... | free |
| `search_private_companies` | city?, limit?, max_participants?, min_opportunity?, min_participants?, naics_prefix?, ... | US private companies whose filings (Form 5500 plan history, final filings, ownership changes) record a change: vertical, plan participants as a size proxy, EBIT... | free |
| `search_sponsor_deals` | limit?, query?, since?, sponsor_dfx_id?, state?, target_dfx_id?, ... | Announced acquisitions, recapitalisations and exits by independent sponsors: sponsor, target, dates, enterprise value range where disclosed, structure, parties ... | free |
| `search_pending_ownership_changes` | changed_since?, limit?, query?, state?, tag?, view? | OFFICIAL state records that a skilled nursing facility's ownership, control or operator is changing, before the change takes effect (Kentucky, New York, Rhode I... | free |
| `search_vc_firms` | active_only?, city?, emerging_manager?, limit?, min_investments?, query?, ... | Venture firms as compact cards: stated sectors, stages, geography and check size beside OBSERVED behaviour (investments in the last 6 and 12 months, lead count,... | free |
| `get_vc_firm` | dfx_id | The full card for any entity on the venture graph: a firm (with recent investments, co-investors and funds), a person (with attributed investments and board sea... | free |
| `search_vc_investments` | alongside_investor_dfx_id?, company_dfx_id?, investor_dfx_id?, investor_type?, lead_only?, limit?, ... | Investor-by-investor participations in rounds: investor, company, fund, the partner attributed (with attribution level), role (lead or participant), new or foll... | free |
| `search_vc_funds` | fundraising_state?, lifecycle_state?, limit?, max_vintage?, min_form_d_sold_usd?, min_vintage?, ... | Funds with every amount under its own name (target, first close, final close, announced size, Form D offering and sold, ADV gross asset value), vintage and basi... | free |
| `search_pe_firms` | class?, class_state?, cursor?, limit?, min_transactions_36m?, query?, ... | Private equity firms (management companies and advisers) as compact cards: the classifier's class with its state, confidence and basis; size band with the evide... | free |
| `get_pe_firm` | dfx_id | The full card for a private equity firm: identity (website, HQ, ADV filing dates), classification with basis and the size band's definition and evidence, classi... | free |
| `search_pe_funds` | adv_fund_type?, cursor?, lifecycle_state?, limit?, max_vintage?, min_adv_gav_usd?, ... | Funds on the private equity graph with every amount under its own name and beside its basis: target, first close, final close, announced size, Form D offering a... | free |
| `get_pe_fund` | dfx_id | One fund: manager, vintage and basis, every amount kept apart with its basis (adv_gross_asset_value is reported gross assets, not fund size or dry powder), the ... | free |
| `search_pe_transactions` | add_on_only?, control_status?, cursor?, firm_dfx_id?, limit?, platform_dfx_id?, ... | Acquisitions, add-ons, recapitalisations, carve-outs, secondary sales and exits on the private equity graph: type, status, announced and closed dates, target wi... | free |
| `search_pe_platforms` | limit?, min_add_ons_24m?, owner_dfx_id?, query?, sector?, sort?, ... | Companies that act as a platform (a sponsor's platform investment, or a company that has made add-ons): industry, add-on counts (total and last 24 months) and l... | free |
| `find_pe_buyers_for_company` | dfx_id, limit? | Computed buyer_for_company matches from the private equity matcher for one company (a dfx:pe:, dfx:isi: or dfx:vc: company id): each firm with the matcher's rea... | free |
| `find_pe_companies_for_buyer` | dfx_id, limit? | Computed company_for_buyer matches for one private equity firm (dfx:pe: id): each company (on the private equity, sponsor or venture graph, with its dfx id) wit... | free |
| `find_pe_addons_for_platform` | dfx_id, limit? | Computed addon_for_platform matches for one platform (a dfx:pe: company id from search_pe_platforms): each candidate company with the matcher's reasons, blocker... | free |
| `search_ria` | city?, cursor?, entity_type?, firm_class?, firm_crd?, fund_type?, ... | Registered investment advisers (Form ADV: RAUM, clients by type, employees, advisors on IAPD, private funds, class such as INDEPENDENT_WEALTH or WIREHOUSE), reg... | free |
| `get_ria_firm` | dfx_id | The full card for one registered investment adviser plus its people flows (joins, departures, net, rates over 90 days, 12 and 36 months), growth between annual ... | free |
| `get_ria_advisor` | dfx_id | One IAPD-registered advisor: name, current firm with class and tenure, employment history as dated registration spans in order (firm, begin, end, current), ever... | free |
| `resolve_ria_advisor` | crd?, firm?, firm_crd?, limit?, name, state? | Resolve an advisor by name AND a firm (name or CRD), or by individual CRD, to one person card | free |
| `search_ria_funds` | cursor?, firm_dfx_id?, form_d_file_number?, fund_type?, group_by?, include_custodians?, ... | Private funds from Form ADV Schedule D 7.B.(1): fund name, SEC fund id (805-...), type, gross asset value with its as-of date (reported gross assets, NOT fund s... | free |
| `search_ria_advisor_moves` | advisor_dfx_id?, cursor?, from_dfx_id?, include_bulk?, include_departures?, limit?, ... | Advisors who left one firm and registered at another: the person, from and to firms with class, the registration end and begin dates, the gap, and the move type... | free |
| `search_ria_teams` | cursor?, from_dfx_id?, include_members?, kind?, limit?, min_members?, ... | Teams: clusters of advisors who left the same firm for the same firm from the same branch state within a 14-day chain, with member count, dates, spread, the fro... | free |
| `search_ria_ma` | acquirer?, acquirer_crd?, cursor?, firm_dfx_id?, kind?, limit?, ... | RIA M&A from three factual sources, each labelled: successions the acquirer swore on Form ADV Item 4 (succession); firms whose advisors re-registered whole at o... | free |
| `search_ria_changes` | cursor?, dfx_id?, event_type?, limit?, signal_family?, since, ... | The RIA event tape by OBSERVATION time: advisor firm changes and departures, team lift-outs and absorptions, successions, RAUM and headcount changes, control pe... | free |
| `get_ria_trends` | firm_class?, limit?, min_advisors?, min_raum_usd?, sort?, state?, ... | Three derived views from the RIA lane's aggregates: state_stats (SEC-registered firms, wealth firms, RAUM, private funds, advisors, joins, departures and new fi... | free |
| `get_ria_capital_links` | dfx_id, limit? | For one RIA firm (or one private fund): every link to the private equity, venture, family office and sponsor graphs written on a shared identifier, with the bas... | free |
| `get_ria_practice` | dfx_id | What a practice looks like from what it filed: reported Form ADV fields (RAUM, discretionary, accounts, employees, advisors, clients and RAUM by type, private f... | free |
| `search_ria_practices` | archetype?, bank_owned?, cursor?, custody?, financial_planning?, firm_class?, ... | SEC-registered advisers screened on the practice layer: by archetype (HNW_WEALTH_MANAGER, UHNW_PRIVATE_WEALTH, MASS_AFFLUENT_RIA, INSTITUTIONAL_ASSET_MANAGER, R... | free |
| `search_ria_anomalies` | anomaly_type?, cursor?, family?, firm_class?, firm_crd?, limit?, ... | Reported values and filing-to-filing changes that stand out against a peer group (segment by RAUM band, 30 or more advisers), each with the metric, current and ... | free |
| `search_ria_offices` | cursor?, firm_class?, firm_crd?, limit?, min_advisors?, sort?, ... | Offices (a firm and an IAPD branch city) ranked by departures, joins, net flow, departure rate, team lift-outs out or in, breakaways in formation (advisors at t... | free |
| `search_ria_move_indicators` | advisor_dfx_id?, cursor?, firm?, firm_dfx_id?, kind?, limit?, ... | The observed pre-move indicators DFX holds, per advisor: a prior co-move teammate or the team's senior member left the firm (with who and where to), a fifth or ... | free |
| `search_ria_outside_business` | category?, category_group?, current_only?, cursor?, firm_crd?, investment_related?, ... | Outside-business entries from the advisor's own Form U4 disclosure, reviewed extraction: the company, what it does and on what basis, the advisor's role (owner,... | free |
| `get_ria_outside_business` | company_id?, dfx_id? | With an advisor (dfx:ria: id or individual CRD): every reviewed outside-business entry, the measured dimensions (entrepreneurial, breadth, community, network, r... | free |
| `search_private_credit` | bdc_advisers_only?, class?, cursor?, entity_type?, held_only?, industry?, ... | The capital structure graph behind private markets, built from every BDC's schedule of investments each quarter since 2022 | free |
| `get_credit_provider` | detail?, dfx_id | A credit manager: its classes with basis, the BDCs it advises (from each BDC's own 10-K) with their latest schedules, its credit funds on Form ADV, its sponsor ... | free |
| `get_bdc_portfolio` | as_of?, cursor?, dfx_id, group_by?, include_equity?, limit?, ... | Every position a BDC tagged at one quarter end (the latest unless as_of is given), each in the filer's own figures: borrower, instrument, kind, lien, principal,... | free |
| `get_borrower_capital_structure` | dfx_id | The borrower group (its spellings and grade), every facility (kind, lien, principal held across lenders as a lower bound, mark, pricing, PIK, maturity with basi... | free |
| `get_credit_facility` | dfx_id | A facility (one borrower group in one instrument class): size as the sum of BDC pieces with its basis, pricing modal and ranged across pieces, maturity with bas... | free |
| `search_credit_maturities` | cursor?, from?, lien?, limit?, min_principal_usd?, months?, ... | Debt facilities still on a BDC schedule whose tagged or written maturity falls inside the window (default the next 24 months from today), ordered by date: borro... | free |
| `search_sponsor_lender` | cursor?, lender_dfx_id?, limit?, min_borrowers?, sort?, sponsor_dfx_id? | Sponsor x lender pairs counted once per borrower held (the lender is the adviser behind the BDCs, or the BDC where the adviser is not read): borrowers, faciliti... | free |
| `find_lenders_for_financing` | band_max_usd?, band_min_usd?, industry, lien?, limit?, since?, ... | Lenders ranked on the comparable facilities they CURRENTLY HOLD on BDC schedules: same lien, a borrower industry containing the term (as the filer wrote it: hea... | free |
| `search_private_credit_changes` | by?, cursor?, dfx_id?, event_type?, include_reraised?, include_reshuffles?, ... | Dated changes by effective date (the quarter end where the change is visible) or by first-seen (by=observed, which leaves out a re-raise, an old claim written a... | free |
| `search_allocators` | allocator_class?, consultant_class?, cursor?, entity_type?, include_components?, limit?, ... | The capital-owner graph: public pensions (every Census unit), corporate and Taft-Hartley DB plans (Form 5500), endowments and foundations (IRS), state pools and... | free |
| `get_allocator` | dfx_id | For an allocator: the card with reported assets and basis, funded status, the latest allocation policy rows (target, range, actual as printed with the subject's... | free |
| `search_allocator_commitments` | allocator_dfx_id?, bucket?, consultant_dfx_id?, cursor?, first_time_only?, fund_dfx_id?, ... | One row per line of a plan's own disclosure: allocator, fund as printed, manager and fund resolved to the pe / vc graphs where the resolver matched, bucket, the... | free |
| `search_re_fund_managers` | crd?, cursor?, first_vehicle_year_from?, include_former?, invested_state?, latest_vintage_from?, ... | Advisers that swear a Real Estate Fund vehicle on Form ADV Schedule D 7.B.(1): one manager is one CRD, with its registration and latest filing, regulatory asset... | free |
| `get_re_fund_manager` | dfx_id | The manager card, its ten largest vehicles and the whole family by vintage, validated property bindings with the rule and confidence behind each and the propert... | free |
| `search_re_fund_vehicles` | cursor?, exclude_feeders?, first_reported_from?, first_reported_year?, include_dropped?, lifecycle_state?, ... | Vehicles sworn as Real Estate Funds by their SEC fund id (805-...): the fund and its family and sequence, master, feeder or fund of funds, gross asset value lat... | free |
| `get_re_fund_vehicle` | dfx_id | The vehicle card with its reporting history year by year as filed (gross asset value, owners, minimum investment, the fund type and name as filed that year), it... | free |
| `get_re_fund_trends` | limit?, min_gav_usd?, view? | Derived series over the sworn tape, each with its population, derivation and caveat printed beside it: vehicles first reported by year (with the managers filing... | free |
| `search_re_fund_loans` | cursor?, group_by?, instrument_kind?, lender?, limit?, manager_dfx_id?, ... | Loans bound to a real estate fund manager through a validated property binding: lender of record (labelled when it is the CMBS trust holding the note rather tha... | free |
| `search_re_fund_lenders` | cursor?, lender?, limit?, manager_dfx_id?, min_loans?, property_type?, ... | Manager by lender pairs from the loans at the manager's validated holdings: the lender group, loans, principal, properties, property types and states, first and... | free |
| `search_re_fund_lps` | allocator?, allocator_dfx_id?, allocator_state?, commitment_type?, cursor?, group_by?, ... | The public LP tape resolved to real estate fund managers and vehicles: the plan (allocator id), the manager and vehicle with the basis of each resolution, the f... | free |
| `get_capital_paths` | dfx_id, include_former?, kind?, limit? | Published capital flow paths through one institution: which allocators back this manager and through which fund, which lenders finance this sponsor's borrowers ... | free |
| `get_commitments` | dfx_id, include_holdings?, limit? | The commitment tapes, in one call, for any id they reference: the allocator tape (a public plan's own disclosure, with the plan, the fund as printed, the manage... | free |
| `get_borrower_facilities` | as_of?, detail?, dfx_id, group_by?, held_only?, limit? | Every facility a borrower group has on the BDC tape (kind, lien, principal held across lenders as a lower bound, mark on cost, pricing, PIK, maturity with its b... | free |
| `get_sponsor_lenders` | dfx_id, limit?, min_borrowers?, sort? | Sponsor by lender pairs counted once per borrower held: borrowers, facilities, principal held, first and latest quarter, new borrowers in the last four quarters... | free |
| `search_capital_changes` | dfx_id?, event_type?, graph, include_seeded?, limit?, since | The change tape for the three capital graphs by FIRST SIGHT: the day DFX first saw each row, which is the only order a poller can trust | free |
| `search_entities` | active_only?, asset_class?, city?, cursor?, domain?, entity_type?, ... | One search across family offices, independent sponsors and their capital providers, private companies, venture firms, private equity firms and funds, and real e... | free |
| `resolve_name` | domain?, entity_type?, limit?, name, prefer_domain? | Resolve a firm, fund, person or company name to canonical dfx ids from the Data Factory's index of every published name and alias (former names, dbas, legal nam... | free |
| `get_entity` | detail?, dfx_id, event_limit?, evidence_limit?, include?, relationship_limit? | For any DFX id: the full card, published relationships with sources and dates, recent events, evidence rows (the observation each fact traces to), cross-graph s... | free |
| `search_people` | cross_graph_only?, current_only?, domain?, investment_responsibility?, limit?, organization?, ... | Investment professionals, principals and family office staff as names with titles, roles, seniority, investment responsibility, organisation and tenure, from pu... | free |
| `search_relationships` | current_only?, detail?, dfx_id, limit?, rel_type? | Every published relationship touching one entity (EMPLOYS, PRINCIPAL_OF, INVESTED_IN, CO_INVESTED_WITH, MANAGES, OWNS, BOARD_MEMBER_OF, VEHICLE_OF, ...), each w... | free |
| `relationship_path` | from_dfx_id, max_hops?, to_dfx_id | An evidence-backed path between two DFX ids across every graph: each hop is a published relationship with its source, or a SAME_AS identity link by shared CRD/C... | free |
| `search_events` | cursor?, dfx_id?, domain?, event_type?, exclude_routine?, limit?, ... | Dated events across family offices, sponsors, venture, private equity and real estate: investments announced, vehicles formed, Form D and ADV filings, people jo... | free |
| `verify` | as_of?, claim?, object?, object_dfx_id?, predicate?, subject?, ... | SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED or UNKNOWN for a claim, with the observations | free |
| `find_capital_for_opportunity` | asset_class?, check_size_usd?, control?, deal_size_usd?, dfx_id?, investor_types?, ... | Investors for a company (dfx_id) or a described opportunity (sector, state, deal size, stage, control): verified independent sponsors with observed acquisitions... | free |
| `find_opportunities_for_capital` | dfx_id, limit? | For a family office, sponsor, capital provider or venture firm: the opportunities DFX knows that fit its DEMONSTRATED behaviour: computed matches where the grap... | free |
| `explain_match` | dfx_id_a, dfx_id_b | For an investor and an opportunity (either order): MATCH REASONS, BLOCKERS, SUPPORTING OBSERVATIONS, COMPARABLE HISTORY (the investor's dated investments in the... | free |
| `why_now` | dfx_id, within_days? | Evidence-backed reasons an entity matters now: recent filings, vehicles formed, deployments, people moves, fundraising, transition signals, loan maturities, eac... | free |
| `who_should_care` | dfx_id?, event_id?, limit? | Given an entity or an event id: who is likely to care and why | free |
| `search_documents` | dfx_id?, limit?, query | Full-text search over DFX's document index: verbatim passages from the documents the graph already points at (SEC filings and BDC schedules of investments, publ... | free |
| `find_real_estate_lenders` | band_max_usd?, band_min_usd?, city?, limit?, property_type, since?, ... | Lenders ranked on the commercial real estate loans they ORIGINATED, from CMBS loan-level filings (SEC ABS-EE): same property type, loans in the states and city ... | free |
| `search_cmbs_loans` | cursor?, distress?, dscr_max?, limit?, loan_keys?, maturity_from?, ... | Loans on the ACTIVE CMBS tape (SEC ABS-EE, each loan's latest monthly reading, read within 100 days of the newest period) with the servicer's own fields: paymen... | free |
| `search_signals` | affected_dfx_id?, cursor?, domain?, family?, include_audience?, limit?, ... | The governed signal layer the site ranks by (actionable now, public or sellable only): each card names its family, the subject with its dfx id, what changed, wh... | free |
| `search_opportunities` | condition_kind?, cursor?, family?, include_held?, intelligence_class?, limit?, ... | Opportunity summaries: the condition (credit deterioration, refinancing window, lender group change, capital raised, advisor movement, servicing distress ...), ... | free |
| `who_to_contact` | dfx_id?, limit?, opportunity_id?, organization?, prefer_domain?, purpose? | For one organization (dfx_id, or its name in `organization`, resolved through the identity layer so every graph the institution is on is read) or one opportunit... | free |
| `search_forward_opportunities` | contact?, cursor?, entity_dfx_id?, evidence?, limit?, max_economic?, ... | Forward opportunities across DFX: an entity, the event a measured pattern points to (a borrower reaching non-accrual, a pension plan re-upping with a manager, a... | free |
| `get_forward_signal_ledger` | cursor?, limit?, signal_key?, status?, vertical? | The ledger behind every forward claim: for each pattern, its definition, population, test period, base rate, rate among entities showing it, lift with its inter... | free |
| `search_cmbs_resolutions` | cursor?, limit?, min_loss_usd?, property_type?, resolution?, since?, ... | Every conduit CMBS loan whose servicer reported a foreclosure, REO or deed in lieu workout (SEC ABS-EE), with how it ended: resolved or still pending, the SEC l... | free |
| `get_company_coverage` | naics, state? | The Census Bureau's count of firms (Statistics of US Businesses 2022, all firms and firms with 20 or more employees) in one NAICS code (2 to 6 digits) and one s... | free |
| `search_13f_sector_holders` | family_capital_only?, limit?, period?, sector?, sic?, state? | Family offices (and, with family_capital_only false, every 13F filer on the family office graph) that hold public positions in a sector per their latest Form 13... | free |
| `search_bdc_language_change` | changed_only?, filed_from?, limit?, section?, term | For a term (software, tariffs, AI, healthcare, energy, consumer, office, crypto or any word), every active BDC whose latest 10-K or 10-Q names it, compared sent... | free |
| `rank_sponsor_capital` | deal_company?, deal_sponsor?, ebitda_max_usd?, ebitda_min_usd?, group?, limit?, ... | The capital parties named on announced independent sponsor transactions, aggregated | free |
| `get_sponsor_portfolio` | dfx_id?, limit?, name?, status? | Every portfolio holding DFX has for one private equity or independent sponsor firm (current and exited): company, state, listed sector, fund, platform or add-on... | free |
| `rank_service_providers` | active_since?, cursor?, family?, limit?, min_deals?, query?, ... | Service providers on announced independent sponsor transactions, ranked over the whole graph: law firms (family legal), investment banks and M&A advisers (inves... | free |
| `get_service_provider` | dfx_id?, name? | A law firm, bank, accounting or diligence firm as the independent sponsor graph sees it: deal counts and role mix, the sponsors it has served most (with deal co... | free |
| `search_service_provider_sponsors` | cursor?, family?, limit?, min_deals?, provider?, sponsor? | Provider and sponsor pairs from announced independent sponsor transactions | free |
| `search_borrower_sponsors` | borrower?, current_only?, cursor?, group?, limit?, non_accrual_since?, ... | The borrower to sponsor chain: a BDC borrower, linked through a graded identity bridge to its company record, then to the private equity firms that invested (fu... | free |
| `search_credit_stress` | bdc_dfx_id?, event_types?, group?, limit?, period?, since?, ... | Credit stress on the BDC tape, counted over every event: NON_ACCRUAL_PLACED and RETURNED_TO_ACCRUAL (from each BDC's schedule of investments footnotes), PIK_ADD... | free |
| `who_should_provider_call` | limit?, provider?, role_family?, state?, trigger? | The independent sponsor call list (rule isi-pcall-1, XV1 2026-10-02): one row per role family, trigger and sponsor over census-verified sponsor deals | free |
| `search_isi_opportunities` | limit?, opportunity_type?, persona?, since?, state?, status? | ISI opportunities in the shared opportunity contract (rule isi-opp-1): deal_provider_gap (counsel, bank or accountant not on record for a recent sponsor deal), ... | free |
| `find_vc_investors` | active_only?, amount_usd?, city?, geography?, limit?, sector?, ... | Venture firms for a company raising a round, with HARD constraints (geography, sector, stage, amount_usd, active_only) kept apart from RANKING signals (observed... | free |
| `search_vc_coinvestors` | dfx_id?, firm?, limit?, since? | The firms that invest most often beside a named venture firm, from the rounds both were named on: shared portfolio companies, shared rounds, the last and first ... | free |
| `search_vc_new_funds` | all_vehicles?, city?, emerging_only?, lifecycle_state?, limit?, max_fund_number?, ... | Venture vehicles launched since a date (first Form D sale or first Form ADV appearance), or with an open Form D offering (raising_now), one row per manager: fun... | free |
| `search_vc_emerging_managers` | city?, launched_since?, limit?, new_adviser_since?, sector?, state? | Venture managers with an emerging-manager score of 0.5 or more (few funds, recent first vintage, small reported assets), with the score, sector evidence, fund c... | free |
| `search_vc_lp_commitments` | emerging_only?, group_by?, limit?, lp?, max_fund_number?, organization_dfx_id?, ... | Disclosed LP commitments to venture funds from the LPs' own public reports (public pensions, endowments): LP, fund, manager, amount, date, fund number | free |
| `search_vc_financings` | city?, debt_only?, entity_type?, first_sale_since?, first_sale_until?, include_out_of_scope?, ... | Companies on the venture graph that raised since a date, each financing labelled an ANNOUNCED ROUND (press: round type, stage, amount where disclosed) or an SEC... | free |
| `search_vc_next_funds` | limit?, max_sequence?, min_sequence?, sector?, since?, within_days? | Fund N+1: a known venture manager's next numbered fund (Fund III after Fund II), dated by its first Form D, with the previous fund, the years between them and t... | free |
| `search_vc_service_opportunities` | limit?, min_amount_usd?, new_only?, provider_type?, since?, trigger_family?, ... | Filed or announced triggers on the venture graph mapped to the service providers they create work for (admin, audit, law, placement, banking, lending, insurance... | free |
| `search_vc_exits` | dated_only?, investor_dfx_id?, kinds?, limit?, since?, within_days? | Acquisitions, IPOs and listings of venture-backed companies, with the investor that reported it and the date's basis: occurred (a dated source) or observed (see... | free |
| `search_vc_repeat_founders` | city?, geography?, include_out_of_scope?, limit?, prior_venture_backed_only?, sector?, ... | People named as an executive officer on the Form D filings of two or more operating companies, listed by the NEW company with its first Form D date, the person,... | free |
| `search_vc_raise_candidates` | city?, geography?, limit?, max_months_since_financing?, min_months_since_financing?, sector?, ... | Venture-backed companies that are CANDIDATES BY RULE to raise again: last dated financing 12 to 36 months ago and none since, no exit on record, still listed on... | free |
| `search_vc_provider_calls` | city?, geography?, limit?, min_size_usd?, role?, since?, ... | The call list for a fund administrator, auditor, custodian or placement agent: venture funds with no provider of that role on record (new fund Form D), next num... | free |
| `search_vc_opportunities` | city?, family?, geography?, limit?, persona?, provider_gap?, ... | The venture opportunity object: dated signals (fund formation, fund lifecycle, company capital, people movement, relationship change) each with why now, what ha... | free |
| `get_re_debt_exposure` | distress?, group?, limit?, min_balance?, name?, property_type?, ... | CMBS debt grouped by who carries it (latest reading per loan on the SEC ABS-EE tape): group=sponsor (the prospectus annex's sponsor or carve-out guarantor, by n... | free |
| `search_re_lps_by_manager` | limit?, manager?, min_funds? | Allocator x manager pairs from published LP commitments: distinct funds, total committed, first and latest commitment, re-up, the latest funds with their source | free |
| `get_re_org_chain` | limit?, name | By the firm's name family: its real estate fund managers, vehicles by lifecycle, published holdings with basis and confidence, fund loans and lender groups, CMB... | free |
| `get_re_property_chain` | limit?, owner_ids?, property?, property_dfx_id? | A building's recorded NYC mortgages, satisfactions and assignments (parties as filed), the sponsor resolved behind an owner of record when owner_ids are given, ... | free |
| `get_research_records` | kind?, limit?, query?, record_id? | DFX's own published research records and investigations: each finding with its permanent id, version, as-of date, denominator, method link, sources and citation... | free |
| `watch_create` | baseline?, conditions?, include_failing?, include_historical?, include_unmeasured?, maturity_within_months?, ... | Save a private credit investigation for this account: a research question and/or borrowers, a sponsor's borrowers or a lender's book, and the changes to watch (... | account key |
| `watch_list` | nothing | This account's watches with status, latest checkpoint, reads used and cost | account key |
| `watch_changes` | checkpoint?, include_historical?, watch_id | Material changes since a checkpoint: each with its filing, filing date, a check against the lender's own rows, NEW_EVENT or NEWLY_OBSERVED_HISTORICAL, a materia... | account key |
| `watch_reevaluate` | checkpoint?, watch_id | Re-tests the conclusions recorded at a checkpoint (maturity, mark, lenders, performing) against what changed since, and diffs a saved investigation's claims aga... | account key |
| `watch_cancel` | watch_id | Cancels a watch: no further deliveries, the quota slot is freed, earlier deliveries stay readable | account key |

**Start with `what_can_dfx_answer`** if you do not know what to ask for. It says no
clearly when the answer is no, and it records the ask, so questions DFX cannot answer
shape what gets built next.

---

## Beyond real estate: family offices, independent sponsors, venture capital

The same connection answers across three more DFX graphs, with one id scheme (`dfx:fo:`, `dfx:isi:`, `dfx:vc:`, and the real estate ids above), one response contract, and cross-graph identity by shared CRD, CIK or EIN only. A same-name entity on another graph is returned as a candidate, never merged.

**Family offices.** 2,577 offices on the graph (668 candidates, 162 confirmed multi-family, 342 probable single-family, 139 outsourced), 4,238 foundations, 748 offices with 13F positions, 424 with observed direct investments. A candidate is a name, never a class; AUM, RAUM and 13F value are three numbers and are never substituted for one another.

**Independent sponsors.** 4,210 sponsors, 10,827 capital providers, 97,310 private companies with Department of Labor plan-filing history of which 17,081 carry a transition signal, 317,710 computed company-to-sponsor matches with reasons and blockers, 2,476 announced transactions. A plan-filing signal is one year lagged.

**Venture capital.** 78,377 funds with every fund amount kept apart (55,560 with Form D sold), 363,267 people, 156,522 companies and 163,786 rounds. A round is never a check.

**Across all of them:** `search_entities`, `get_entity` (everything on one id: card, relationships, events, evidence, cross-graph links), `search_people`, `search_relationships`, `relationship_path` (how X connects to Y, every hop an evidenced edge), `search_events`, `verify` (SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED or UNKNOWN, with the observations), and the economic tools `find_capital_for_opportunity`, `find_opportunities_for_capital`, `explain_match` (reasons and blockers, never a bare score), `why_now` and `who_should_care`.

Contact points are withheld over MCP on every graph. Call `what_can_dfx_answer` with `domain` set to any of `family_office`, `independent_sponsor`, `venture_capital` or `real_estate` for that domain's entity types, event families, rights, freshness and limitations.

---
## What is actually in here (real estate)

Two populations that barely overlap, and conflating them is the most common way to
misread this server.

| Object | What it is | Resolvable |
|---|---|---|
| `parcel` | Massachusetts. The municipal assessor and registry layer, carrying assessed value, land use and recorded sales. | 2,479,346 |
| `property` | National. Federal programme multifamily: HUD, LIHTC and FHA. | 108,359 |
| `organization` | Owners, managers, lenders and servicers. | not counted separately |

An address may return one, the other, or both.

### Recorded sales

the District of Columbia, Massachusetts, New York and Wisconsin: 95,616 instruments over 118,821 property links.

| Tape | Geography | Grain | Buyer | Seller | Repeat sales |
|---|---|---|---|---|---|
| `municipal recorder extract` | New York City, five boroughs | recorded instrument, grouped into economic transactions | yes | yes | yes |
| `statewide assessor roster` | Massachusetts, statewide | assessor roster: one sale date and price per parcel | yes | **no** | **no** |

- **`municipal recorder extract`**: deeds at or above $10,000,000 consideration. This is
  a deliberate cut by VALUE and not by date: a date cut would orphan the earlier leg of a
  repeat-sale pair. A smaller New York sale is outside the tranche, not absent from the
  city.

- **`municipal recorder extract`**: Fourteen same-day deeds between the same parties are
  ONE transaction with fourteen instrument ids preserved, and a 318-property deed is one
  transaction linked to 318 properties. Consideration is stated once per instrument and is
  never split across its properties. No natural person is named in an event headline, on
  either side.

- **`statewide assessor roster`**: An assessor roster carries the LAST sale, so
  repeat-sale pairs and hold periods are not derivable from it at any volume. A deed
  repeats its full consideration on every parcel it covers, so allocated_consideration is
  carried separately from consideration and allocation_basis says when a split is ours.

### Event coverage, measured

183,102 publishable events across 27 types, written by 30 sources on a published allowlist of 29.

| Event type | States | Published |
|---|---|---|
| `PROPERTY_SOLD` | 4 | 49,471 |
| `TAX_LIEN_LISTED` | 1 | 29,368 |
| `PERMIT_ISSUED` | 3 | 23,230 |
| `DEED_RECORDED` | 1 | 15,170 |
| `OWNERSHIP_CHANGED` | 1 | 15,061 |
| `COMPLIANCE_PERIOD_ENDING` | 56 | 11,956 |
| `VACANT_FORECLOSURE_REGISTERED` | 0 | 4,870 |
| `SUBSIDY_CONTRACT_EXPIRING` | 54 | 4,721 |
| `LEASE_EXPIRING` | 56 | 4,206 |
| `FORECLOSURE_FILED` | 1 | 4,054 |
| `CERTIFICATE_OF_OCCUPANCY` | 3 | 3,868 |
| `PORTFOLIO_EXPANDED` | 53 | 3,528 |
| `LOAN_MATURITY_SCHEDULED` | 52 | 3,298 |
| `PORTFOLIO_CONTRACTED` | 54 | 3,181 |
| `DISTRESS_FLAG_RAISED` | 26 | 3,083 |
| `DEMOLITION_FILED` | 3 | 2,467 |
| `USE_CONVERSION_PERMITTED` | 1 | 929 |
| `ZONING_EVENT` | 1 | 317 |
| `LOAN_MATURED` | 25 | 142 |
| `FORECLOSURE_EVENT` | 21 | 123 |
| `LOAN_MODIFIED` | 5 | 17 |
| `LOAN_STATUS_CHANGED` | 0 | 16 |
| `PERMIT_STATUS_CHANGED` | 0 | 13 |
| `LOAN_ASSIGNED` | 0 | 7 |
| `BANKRUPTCY_EVENT` | 4 | 4 |
| `DISTRESS_STATUS_CHANGED` | 1 | 1 |
| `SPECIAL_SERVICING_ENTERED` | 1 | 1 |

`ZONING_EVENT` are the District of Columbia only. `DISTRESS_STATUS_CHANGED` are Illinois
only. `USE_CONVERSION_PERMITTED` are Massachusetts only. `DEED_RECORDED`,
`OWNERSHIP_CHANGED`, `TAX_LIEN_LISTED` are New York only. `FORECLOSURE_FILED` are
Pennsylvania only. `SPECIAL_SERVICING_ENTERED` are Texas only.
`COMPLIANCE_PERIOD_ENDING`, `LEASE_EXPIRING`, `LOAN_MATURITY_SCHEDULED`,
`PORTFOLIO_CONTRACTED`, `PORTFOLIO_EXPANDED`, `SUBSIDY_CONTRACT_EXPIRING` are national.
Multi-state, with the number of states each reaches: `DISTRESS_FLAG_RAISED` (26),
`LOAN_MATURED` (25), `FORECLOSURE_EVENT` (21), `LOAN_MODIFIED` (5), `BANKRUPTCY_EVENT`
(4), `PROPERTY_SOLD` (4), `CERTIFICATE_OF_OCCUPANCY` (3), `DEMOLITION_FILED` (3),
`PERMIT_ISSUED` (3). `LOAN_ASSIGNED`, `LOAN_STATUS_CHANGED`, `PERMIT_STATUS_CHANGED`,
`VACANT_FORECLOSURE_REGISTERED` carries rows that resolve to no state at all, so a state
filter cannot reach it.

---

## The loan tape: `debt_maturity_schedule`

Free with no key. For one US state and one forward window, up
to 200 loans per call, one row per loan, ordered by maturity date:

- `maturity_date` and `maturity_basis`
- `original_principal_usd`, `current_principal_usd`, `interest_rate_pct`, `origination_date`, `term_months`
- `instrument_type`
- the lender's canonical name and DFX id where resolved
- the secured property: DFX id, street address, city, state, postal code, unit count, property type
- the `source_key` for that row

**Why the dates can be trusted.** 23,870 loans carry a maturity date and **23,870 of
23,870 carry `maturity_basis = 'confirmed'`.** Not one is estimated, inferred from a
term length, or carried forward from a stale reading. Every date was filed with the SEC
by a loan servicer or recorded by HUD, and then resolved to a specific building.

`search_property_events` returns the **event**: a date, a headline, an address. The loan
tape returns the **loan**: the principal, the lender, the instrument, deduplicated to one
row per loan, up to 200 rows instead of 50, with the population stated so you can tell a
complete answer from a truncated one. The two populations are different sizes on purpose
and both numbers are true: an event has to be promoted to a single place, a loan only has
to be filed, so the 23,870 loans on the tape are reached here while
3,298 maturity events are reachable through the event search.

**How the loans spread.** Of the 23,870 loans, 1,990 mature inside
the default 548-day window, and they are not evenly spread. Measured 2026-10-29:

| State | Loans maturing in the next 548 days |
|---|---|
| CA | 355 |
| NY | 211 |
| TX | 125 |
| FL | 102 |
| OH | 68 |
| NJ | 62 |
| GA | 60 |
| MI | 59 |
| PA | 56 |
| IL | 52 |
| VA | 44 |
| NV | 42 |
| IN | 40 |
| WA | 38 |
| AZ | 36 |
| NC | 35 |
| CO | 31 |
| LA | 24 |
| MD | 23 |
| MO | 23 |
| SC | 23 |
| AL | 22 |

26 further states hold between 1 and 18 loans in that window; Montana and Wyoming hold
1. Widen `within_days` to reach further out; each call returns up to 200 loans.

255 of those 1,990 carry no single state: a loan secured by several
buildings has no property anchor, so a state filter cannot reach it. Those are reached
through `get_property_record`.

**What it does not cover, stated plainly.** These are the gaps the server itself
reports through `dfx_coverage`, reprinted here so you do not have to call it to find
them:

- Loan maturity coverage is federal programme lending only (FHA insured and agency
  backed). The Registries of Deeds are closed to automation, so conventionally financed
  property carries no debt record here. A property absent from a maturity search is NOT a
  property without debt.

- LIHTC compliance periods are statutory and every one falls on 31 December, so a count
  bucketed by day shows a December cliff that is an artefact of the statute rather than a
  market event.

- Permit and demolition coverage is the City of Boston only.

- No outcome has ever been observed for any prediction in this graph. Nothing served
  here carries a calibrated probability; every score is a ranked signal.

- One street address can carry several records. Measured across 6,114 such clusters:
  2,764 agree on unit count and are plausibly one asset registered by more than one
  programme, while 3,350 report DIFFERENT unit counts and are probably genuinely different
  buildings at one address, such as a scattered-site development. DFX has merged none of
  them and resolve() says which case you are looking at rather than choosing.

- Property and parcel are separate populations that barely overlap: 661 clean one-to-one
  pairs out of roughly 100,000 each. An address may resolve to one, the other, or both,
  and they are returned as distinct typed objects rather than merged.

- PROPERTY RECORDS ARE NOT ONE ROW PER BUILDING. 101,991 published property records
  cover 94,859 distinct normalised addresses, so a total computed across them overstates
  by roughly 8%. 245 Park Avenue is one tower and thirteen records, because thirteen
  securitisation trusts each report it. Every row is individually true, which is why the
  distortion is invisible per row. Each record carries address_group_size so you can see
  it: 1 is unique, and above 1 you should deduplicate by address before summing anything.
  DFX has not merged them because thousands of these clusters carry different unit counts
  and are genuinely different buildings at one address rather than one building recorded
  twice.

- The sale tape is two sources with different grain, and the difference decides which
  questions it can answer. MASSACHUSETTS is an assessor roster: statewide, one sale per
  parcel, buyer named and SELLER NEVER NAMED, so repeat-sale pairs and hold periods are
  not derivable from it at any volume and no further ingestion of it will change that. NEW
  YORK is a recorder extract: five boroughs, both parties named, every instrument dated,
  so repeat sales and hold periods ARE derivable, but only for deeds at or above
  $10,000,000. Neither one is a national sale tape and DFX does not have one.

---

## Connect it

Any MCP client that speaks Streamable HTTP. No credentials for anonymous reads. The core
profile is first; add the full profile too when you want the real estate tools by name.

```json
{
  "mcpServers": {
    "dfx": {
      "type": "http",
      "url": "https://exchange-production-9123.up.railway.app/mcp/core?c=gh-repo"
    },
    "dfx-full": {
      "type": "http",
      "url": "https://exchange-production-9123.up.railway.app/mcp?c=gh-repo"
    }
  }
}
```

### In your editor

Cursor, one click:

[![Add DFX to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=dfx&config=eyJ1cmwiOiJodHRwczovL2V4Y2hhbmdlLXByb2R1Y3Rpb24tOTEyMy51cC5yYWlsd2F5LmFwcC9tY3AvY29yZT9jPWlkZS1jdXJzb3IifQ%3D%3D)

```text
cursor://anysphere.cursor-deeplink/mcp/install?name=dfx&config=eyJ1cmwiOiJodHRwczovL2V4Y2hhbmdlLXByb2R1Y3Rpb24tOTEyMy51cC5yYWlsd2F5LmFwcC9tY3AvY29yZT9jPWlkZS1jdXJzb3IifQ==
```

VS Code (GitHub Copilot agent mode), from a terminal, or paste the `vscode:` link into a
browser's address bar:

```bash
code --add-mcp '{"name":"dfx","type":"http","url":"https://exchange-production-9123.up.railway.app/mcp/core?c=ide-vscode"}'
```

```text
vscode:mcp/install?%7B%22name%22%3A%22dfx%22%2C%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fexchange-production-9123.up.railway.app%2Fmcp%2Fcore%3Fc%3Dide-vscode%22%7D
```

Claude Code:

```bash
claude mcp add --transport http dfx 'https://exchange-production-9123.up.railway.app/mcp/core?c=ide-claude-code'
claude mcp add --transport http dfx-full 'https://exchange-production-9123.up.railway.app/mcp?c=gh-repo'
```

A member whose client cannot send a header (a Claude custom connector, ChatGPT developer
mode) adds `https://exchange-production-9123.up.railway.app/mcp/core/member` instead and signs in with OAuth 2.1.

Both the current protocol revision and the older `initialize` handshake are served,
because most deployed clients still send the latter.

### From code: the dfx-intel SDKs

Python and TypeScript clients for `research`, `verify` and `resolve_name` on the core
profile, with no runtime dependencies. Anonymous by default; a member key is read from
`DFX_API_KEY`.

```bash
pip install dfx-intel
npm install dfx-intel
```

Runnable examples, each next to the real output of its last run against production, are in
[`examples/sdk/`](examples/sdk/): anonymous research, printing the citation behind every
claim, error handling and retries, pagination, member access with a key from the
environment, and a short integration tutorial. Choosing between anonymous access, OAuth
sign-in and an account key, what each client supports, and troubleshooting:
[`docs/CONNECT.md`](docs/CONNECT.md).

Starting from an agent framework instead? [`examples/frameworks/`](examples/frameworks/)
has one runnable example each for the Claude Agent SDK, the OpenAI Agents SDK, LangGraph
and the Vercel AI SDK, plus copy-paste MCP configs for Cursor, VS Code, Windsurf and
Claude Desktop, each with the recorded output of a run against production.

Attaching DFX as an MCP server from Python? [`examples/mcp/`](examples/mcp/) has
runnable scripts for langchain-mcp-adapters, the OpenAI Agents SDK
(`MCPServerStreamableHttp`) and LlamaIndex (`llama-index-tools-mcp`), each asking one
real question and printing the cited answer, with the output of its last run beside it.
[`examples/quickstart.ipynb`](examples/quickstart.ipynb) does the same in a notebook:
raw JSON-RPC over httpx, then the OpenAI Agents SDK.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Capital-W-Holdings/us-property-parcel-real-estate-debt/blob/main/examples/quickstart.ipynb)

### If your client only speaks stdio

Some clients launch a subprocess and speak JSON-RPC over its pipes; they have no way to
reach a URL at all. `bridge/dfx_mcp_stdio.py` is the whole adapter for those: one file,
standard library only, no key, no state. It forwards each message to the endpoint above
and writes the answer back.

```json
{
  "mcpServers": {
    "dfx-real-estate": {
      "command": "python3",
      "args": ["/path/to/us-property-parcel-real-estate-debt/bridge/dfx_mcp_stdio.py"]
    }
  }
}
```

Use an absolute path. An MCP client launches the command from its own working directory,
not yours, so a relative one will not find the file.

Use the URL directly if your client can. The bridge adds a process and a hop and buys
nothing when Streamable HTTP is available. It reads the tool list from the live server
on every `tools/list`, so an installed copy does not go stale when DFX publishes a new
event family; there is nothing in it that knows what a family is.

---

## Questions this server is good at

- Which commercial mortgages in this state mature in the next 548 days, who lent, and against which building?
- What has DFX learned since I last asked? (`changes_since`, cursor-based, ordered by when DFX came to know a fact rather than when the fact occurred.)
- Which LIHTC compliance periods and HUD subsidy contracts are expiring, and where?
- What did this parcel last sell for, to whom, and under which book and page?
- Who owns, manages or lends against this building?

### Three recipes, as an agent calls them

Each is one tool call, the arguments verbatim, and what came back when this page was
generated. Paste the call; the numbers are the wire's, not this page's.

**Where is the queue?** Subsidised projects in Ohio with a waiting list of 24 months or more, deepest first.

```json
{"tool": "search_subsidised_housing", "arguments": {"state": "OH", "min_waiting_months": 24, "limit": 10}}
```

Returns `matched: 69` and ten rows, the longest at 85 months, each with units available, occupancy, rent, household income and what HUD pays per unit, and `waiting_list_coverage` saying how many projects in the state report a list at all. One annual capture (29,455 projects nationally), stated on every row. A NULL waiting list is an absent disclosure, never an empty queue.

**Which banks are past the CRE guidance line?** FDIC-insured banks in Ohio whose total CRE exceeds 300% of equity, most concentrated first.

```json
{"tool": "search_bank_cre_exposure", "arguments": {"state": "OH", "above_guidance": true, "limit": 10}}
```

Returns `matched: 8` with each bank's CRE book against equity and assets, noncurrent and charge-off ratios and its UBPR peer and national percentile ranks. 626 of 4,313 banks nationally are over that line on this measure. The guidance tests total risk based capital and these ratios are on equity, so the row says "screen", not "finding".

**What matures, and against which building?** Securitised and FHA-insured loans on Texas property maturing inside a year, soonest first.

```json
{"tool": "search_property_events", "arguments": {"event_type": "LOAN_MATURITY_SCHEDULED", "state": "TX", "within_days": 365, "limit": 50}}
```

Returns 77 events (page with `next_cursor`), each with the building's `dfx_id`. Then, for any row, `get_property_record` with that id returns the loan itself free: current principal, interest rate, original principal, maturity and basis. `debt_maturity_schedule` is the same population as one deduplicated statewide list with the lender name and a completeness figure.

### One page per question, with the measured coverage on it

- [Which commercial real-estate loans mature in a given state and window?](https://dfxintel.com/ai/real-estate-mcp/cre-loan-maturities): 3,298 LOAN_MATURITY_SCHEDULED, 52 states and territories.
- [Which LIHTC properties are reaching the end of a compliance period?](https://dfxintel.com/ai/real-estate-mcp/lihtc-year-15-data): 11,956 COMPLIANCE_PERIOD_ENDING, 56 states and territories.
- [Which HUD-subsidised properties have contracts approaching expiry?](https://dfxintel.com/ai/real-estate-mcp/hud-subsidy-expiry-data): 4,721 SUBSIDY_CONTRACT_EXPIRING, 54 states and territories.
- [Where is commercial real estate in distress, foreclosure or workout?](https://dfxintel.com/ai/real-estate-mcp/distressed-cre-data): 3,083 DISTRESS_FLAG_RAISED, 123 FORECLOSURE_EVENT, 17 LOAN_MODIFIED, 26 states.
- [What did this property sell for, and who owns it?](https://dfxintel.com/ai/real-estate-mcp/property-sales-and-ownership-data): 49,471 PROPERTY_SOLD, 4 states.
- [Which commercial leases are approaching expiry, and who occupies a building?](https://dfxintel.com/ai/real-estate-mcp/commercial-lease-expiry-data): 4,206 LEASE_EXPIRING, 56 states and territories.

## Questions it is not good at, and will say so

- Anything about a person. Person lookup is deliberately not offered.
- Assessor and parcel data outside Massachusetts.
- Debt on conventionally financed property.
- Anything outside the United States.

---

## Design notes an agent developer may care about

- **`changes_since` is ordered by when DFX learned a fact, not when the fact occurred.** A deed signed in March is recorded in August. Polling a date filter would show you the same rows forever.
- **An unrecognised `event_type` is refused with the served vocabulary attached**, never answered with an empty list, because an empty list reads as an absent market.
- **A name is a blocking key, never an identity.** `resolve_organization` returns all candidates rather than guessing one.
- **Every returned fact carries its provenance**: the source, the evidence class, and for sales the registry book and page.
- **Coverage is a tool, not a footnote.** Call `dfx_coverage` before concluding that an empty result means an absent market.

### What is behind the rows

29 registered feeds pass the rights filter and serve this endpoint, in 5 families:

- **County and municipal records** (20): The property layer: assessment, recorded instruments, permits, code enforcement and tax status.
- **Federal program and statistical data** (4): Federal programme registers and statistical series: who is funded, insured, assisted or measured.
- **Public records** (3): Public records that do not sit in one of the families above.
- **Federal regulator filings** (1): What firms, funds and plans are required to tell a federal regulator, on the regulator's own schedule.
- **Securitised debt reporting** (1): Loan-level and servicer reporting on debt that has been securitised, month by month.

Every returned row names its own source, the date it was effective and the date DFX read it. Which individual feeds sit inside a family is not published.


## Terms

The example code in `examples/` is MIT licensed. The data served by the endpoint is
not: it is derived from public federal and municipal sources under DFX's own
processing, and is served for use, not for redistribution as a dataset. Ask if you
want something broader; the answer is often yes.

Operated by DFX Intelligence. Developer reference: <https://dfxintel.com/ai/real-estate-mcp>
