# Phoenix EX — Complete Feature Catalog

**Product:** an AI employee-experience (EX) HR platform. Employees talk to it by voice (IVA, phone) and text (chatbot). It answers, takes requests, and analyses every conversation into tags, categories and insights for HR.

**Audience:** TPM, CTO, tech leads. Use this as the master list: add rows, change priorities, link Fit-Gap IDs.

**Date:** 2026-10-17 · **Code basis:** repo at `cb570a50b` (see `product/README.md` and the dossiers) · **Competitor basis:** dossier §25 (sources G1–G31, R1–R*) + new research listed in [Sources](#sources).

## How to read this

| Column | Meaning |
|---|---|
| **Need** | The problem the feature solves, in one line |
| **Solution options** | Ways to build it; the **bold** one is my recommendation |
| **What others do** | How world leaders solve it (source in brackets) |
| **Phoenix today** | ✅ have · 🟡 partial · ❌ missing — from code, not from claims |
| **Pri** | **P0** = needed for pilot trust / UAT · **P1** = needed to sell and renew · **P2** = differentiator or later |
| **Eff** | Effort for the current team (~10 people): **S** ≤ 1 week · **M** 2–4 weeks · **L** > 1 month |

Effort and priority are my judgment (INFERENCE). Re-check them against the Fit-Gap tracker before committing dates.

---

## Contents

1. [Product shape: users and the four jobs](#1-product-shape-users-and-the-four-jobs)
2. [Channels and access](#2-channels-and-access)
3. [Identity, consent and anonymity](#3-identity-consent-and-anonymity)
4. [Voice experience (IVA)](#4-voice-experience-iva)
5. [Conversation brain (understand and answer)](#5-conversation-brain-understand-and-answer)
6. [Knowledge management](#6-knowledge-management)
7. [Actions and transactions](#7-actions-and-transactions)
8. [Requests, cases and ticketing](#8-requests-cases-and-ticketing)
9. [Conversation analytics: tags, categories, enrichment](#9-conversation-analytics-tags-categories-enrichment)
10. [Insights, dashboards and reporting](#10-insights-dashboards-and-reporting)
11. [Closing the loop: action on insights](#11-closing-the-loop-action-on-insights)
12. [Proactive listening (outbound and programs)](#12-proactive-listening-outbound-and-programs)
13. [Privacy, security and compliance](#13-privacy-security-and-compliance)
14. [Org data and integrations](#14-org-data-and-integrations)
15. [Admin and configuration studio](#15-admin-and-configuration-studio)
16. [AI quality, evaluation and AI ops](#16-ai-quality-evaluation-and-ai-ops)
17. [Platform, operations and cost](#17-platform-operations-and-cost)
18. [Commercial and customer success](#18-commercial-and-customer-success)
    - [18b. Recruiting: from interview scheduling to the candidate's status](#18b-recruiting-from-interview-scheduling-to-the-candidates-status)
19. [Key judgments](#19-key-judgments)
20. [Suggested release cut](#20-suggested-release-cut)
21. [Red lines: what not to build](#21-red-lines-what-not-to-build)
22. [Sources](#sources)

---

## 1. Product shape: users and the four jobs

Every feature below serves one of four jobs. If a proposed feature serves none of them, question it.

| Job | Who | Example |
|---|---|---|
| **J1 — Get help** | Employee | "How many leave days do I have?" "The office restaurant food was cold again." |
| **J2 — Get it done** | Employee → owner team | "I want a salary review." "Fix the AC on floor 3." |
| **J3 — Be heard** | Employee → organisation | Anonymous complaint about workload, feedback on a new policy |
| **J4 — Understand and act** | HR, EX analyst, managers | "What are the top 5 issues in the Tehran region this month, and is anything new?" |

**Roles to design for** (each needs its own view and permissions):

| Role | Needs |
|---|---|
| Employee | Fast answers, simple request tracking, trust that what they say is safe |
| Case owner / service team (HR, facilities, IT, restaurant vendor) | A queue, context, SLA, a way to reply |
| Line manager | Requests from their team (career, approvals), team-level insights (k-threshold) |
| Unit head (معاونت / اداره کل / اداره) | Insights for their scope and sub-units only |
| EX analyst / HR | Org-wide insights, taxonomy, reports, action plans |
| Knowledge owner | Edit their part of the KB, see unanswered questions in their area |
| Sensitive-case reviewer | A restricted queue; every open is logged |
| System admin | Config, users, roles; emergency identity resolution under control |
| Privacy / security officer | Audit log, retention, access reviews |
| Tech admin | Infra, monitoring, no access to content |

---

## 2. Channels and access

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| CH-01 | Inbound phone line (voice IVA) | Deskless and field staff have a phone, not a laptop | **SIP trunk → LiveKit → voice agent** (current); hosted CPaaS | UKG Bryte Voice works through Siri/Google, not phone calls; Paradox offers phone/voice for candidates [G24, G27] | ✅ `chatbot-iva-agent` | P0 | — |
| CH-02 | Web chat widget | Office staff prefer text | **Embeddable widget + SSO**; intranet page | Every HR agent (Leena, Moveworks, Workday Assistant) | ✅ `adcs` chat | P0 | — |
| CH-03 | Voice in browser / app | Voice without a phone line, e.g. at a kiosk | **WebRTC (websocall)** | Leena advertises voice in 100+ languages [G28] | ✅ `golang/websocall` | P1 | — |
| CH-04 | Messenger channels (Bale, Eitaa, Rubika, Telegram) | Where Iranian employees already are | **One channel adapter per messenger over the same chat API**; send-only first | Moveworks / Workday live inside Slack and Teams; in Iran the equivalents are local messengers | 🟡 Rubika send tool exists, disabled | P1 | M |
| CH-05 | SMS in/out | Confirmations, tracking codes, people with basic phones | **Outbound SMS for confirmations now**; inbound "reply with code" later | Paradox runs on SMS [G27] | 🟡 `send_sms` (outbound only, no rate limit) | P0 | S |
| CH-06 | Microsoft Teams / Slack | Customers outside Iran or tech companies | Bot-framework adapter | Workday for Teams/Slack; Moveworks | ❌ | P2 | M |
| CH-07 | Email intake | Formal requests, attachments | Inbound mailbox → request (§8) | Workday Help and Oracle accept cases by email [W-WD2, W-OR1] | ❌ | P2 | M |
| CH-08 | Kiosk / shared device mode | Factories and stores with no personal device | Kiosk login with personnel code + OTP; auto-logout | Common in frontline HCM (UKG) | ❌ | P2 | M |
| CH-09 | Cross-channel continuity | Start by phone, continue in chat, track via SMS | **One `conversation_id` + one `request_id` across channels; tracking code works everywhere** | ServiceNow Employee Center: one portal for every channel [W-SN1] | ❌ (sessions are per channel) | P1 | M |
| CH-10 | Business hours and fallback | What happens at 2 am or on holidays | Hours calendar with the Jalali holiday list; after-hours message, callback request | Standard in every contact-centre platform | 🟡 greeting is configurable, no calendar | P1 | S |
| CH-11 | Accessibility | Hearing or vision impaired staff, low literacy | Voice ↔ text both ways, slow-TTS option, DTMF menu fallback | WCAG for the web; voice for low literacy | 🟡 | P2 | S |
| CH-12 | Capacity and admission control | Do not drop calls at peak (e.g. payday) | **Concurrency cap + queue message + callback**; autoscale workers | Contact-centre call admission control (CAC) | 🟡 one job per call; no queue | P1 | M |
| CH-13 | **Voice message (async voice note)** — the employee chooses: live call, text chat, or just leave a voice message | Deskless staff prefer speaking to typing but don't want a live conversation (noise, no time, shyness, after hours); a one-way message feels safer for sensitive topics | **One voice-message pipeline for three entry points:** (a) mic button in web/app chat, (b) "leave a message" phone line, voicemail-style, works on basic phones, also the IVA after-hours fallback, (c) voice notes in messengers (Bale, Eitaa, Rubika). Flow: upload → ASR → same tagging pipeline as calls → reply by text/SMS/TTS. Anonymous mode: keep the transcript only and delete the audio after ASR, or distort the voice | SpeakUp: voice message with optional voice distortion, anonymous code to check replies [W-SU1]; FaceUp: anonymised voice notes [W-FU1]; Whistlelink: oral reports with voice distortion [W-WL1]; AWS: WhatsApp voice notes + Transcribe for field workers [W-AWS4]; Medallia: voice/video feedback at scale [W-MD1]. Iranian HR products: not seen | 🟡 `adcs` ASR endpoint transcribes an uploaded voice clip to text (WAV only, ≤ 10 MB, audio not stored, no auth: `adcs/chat/views/audio.py`); no voicemail line, no messenger intake, no OGG/Opus/WebM/AMR support | P1 | S (chat mic) / M (phone line, messengers) |

**CH-13 design notes.** Cap length (e.g. 3 minutes) and say so before recording. Convert phone and messenger formats (OGG/Opus from Bale and Telegram, WebM from browsers, AMR/M4A from phones) to WAV before ASR. If ASR confidence is low, reply "I didn't catch that, please resend or type it" instead of guessing. One message may hold several issues: tag at segment level (AN-07). Who may listen to the audio is data tier 4 (SC-02), and every playback is logged (SC-03). In anonymous mode the voice itself identifies the speaker, so the default is transcript-only. A voice message can create a tag-queue item or a request exactly like a call (§8).

---

## 3. Identity, consent and anonymity

This is the heart of trust. Listening products (J3) need anonymity; requests (J2) need identity. **Both live in the same product, so the mode must be explicit in every conversation.**

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| ID-01 | Three conversation modes: **Anonymous / Confidential / Identified** | One channel serves feedback and requests | **Mode is chosen at start or switched with consent; stored on every record**; analytics uses only de-identified data | AllVoices and Deel: anonymous reporting with two-way follow-up [W-AV1, W-DL1]; Qualtrics/Glint: confidential surveys with k-threshold | ❌ | P0 | M |
| ID-02 | Caller identification | Know who is calling, for requests | **Phone → ChannelKey → Person (hashed)**; personnel code + OTP for sensitive actions | Moveworks/Workday use the SSO identity; phone channels use ANI + PIN/OTP | 🟡 phone number used directly | P0 | M |
| ID-03 | Step-up verification (OTP) | Before showing a payslip or creating an identified request | **SMS OTP or a personnel-code question**; voice-biometrics later | Banks and telcos: ANI + OTP; Leena: SSO | ❌ | P1 | S |
| ID-04 | Explicit consent prompts | Legal and trust: "to follow up we must know who you are" | **Scripted consent turn + consent record (who, when, what for)** | AllVoices: anonymous until the reporter chooses to reveal [W-AV1] | ❌ | P0 | S |
| ID-05 | Admission control / allow-list | Pilot limited to some staff | **Enforce at SBC/routing + app check** | — | 🟡 whitelist gates memory only, not admission (finding 9) | P0 | S |
| ID-06 | Long-term memory with consent | Personalisation vs tracking | **Off in Anonymous mode; opt-in in Identified mode; visible and deletable** | — | 🟡 memory per phone, always on (finding 11) | P0 | S |
| ID-07 | Anonymous two-way follow-up | HR needs to ask more without revealing identity | **Anonymous case ID + PIN; employee calls back or checks via chat** | AllVoices, Deel, NAVEX [W-AV1, W-DL1, G15] | ❌ | P1 | M |
| ID-08 | Identity-resolution break-glass | Emergency (safety threat) needs the caller's identity | **Time-limited grant + reason + second approver + audit** | Glint/Peakon: no identity, ever; NAVEX: only through legal process | ❌ (and `expires_at` is not enforced) | P0 | M |

---

## 4. Voice experience (IVA)

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| VX-01 | Persian STT on 8 kHz phone audio | Understanding is the first failure point | **Current STT + measured WER per accent and noise level**; fine-tune on own calls | Local vendors (Part, Asr Gooyesh, Amerandish) [dossier §25.4] | ✅ STT, but no WER measurement | P0 | M (to measure) |
| VX-02 | Dialect and accent coverage | Staff in all provinces; Turkish- and Kurdish-accented Persian | **Eval set per region**; route low-confidence turns to a clarifying question | — | 🟡 `transcript_confidence` is stored, not used | P1 | M |
| VX-03 | Domain vocabulary boost | HR terms, unit names, personnel codes | **Custom vocabulary / hot-words from the org tree and KB** | Contact-centre ASR "phrase hints" (Google, AWS) | ❌ | P1 | S |
| VX-04 | Natural TTS voice | Trust and comprehension | Current TTS; customer-branded voice | PolyAI is known for natural voices [W-PA1] | ✅ | P1 | — |
| VX-05 | Low latency (time to first audio) | Silence over 1.5 s feels broken | **Sentence-streamed TTS (done), tuned endpointing, thinking sounds, fast LLM for first sentence** | Voice-agent platforms all optimise for this | ✅ streaming; endpointing tunable | P0 | S |
| VX-06 | Turn detection and barge-in | Do not cut people off; let them interrupt | **LLM/semantic end-of-turn model (recent commit)** + VAD | PolyAI "interruption friendly" [W-PA1] | ✅ MCI model / LLM turn detection, 0.4 s barge-in | P0 | — |
| VX-07 | Silence and noise handling | Factory noise, user goes quiet | User-away prompts; noise suppression | Standard | ✅ user-away (off by default) | P1 | S |
| VX-08 | Read-back and confirmation | Voice has no screen: numbers and names get misheard | **Confirm critical slots (dates, amounts, codes) before acting** | Moveworks "slots" pattern for structured data [R4] | ❌ (no rule for it) | P0 | S |
| VX-09 | DTMF fallback | When STT fails twice, e.g. entering a personnel code | **Keypad input for codes and menu choices** | Classic IVR | ❌ | P2 | S |
| VX-10 | Warm handover to a human | Some needs require a person | **SIP transfer + a summary passed to the agent screen** | Contact-centre standard; Cognigy/NICE hand over with context | 🟡 transfer works (SIP MESSAGE to 6040); no context passed | P1 | M |
| VX-11 | Callback instead of waiting | No human free, or after hours | Schedule a callback, created as a request | Contact-centre virtual hold | 🟡 the dialing mechanism exists (dobby); no scheduling or request link | P2 | M |
| VX-12 | Call recording with notice | Quality and audit, but privacy | **Announced recording; separate tracks; retention policy** | — | ✅ egress to MinIO; retention exists | P0 | — |
| VX-13 | Graceful end of call | Clear closing, no false promises | **Closing script by mode (CON-09: no follow-up promise in MVP)** | — | ✅ exit tool | P0 | — |

---

## 5. Conversation brain (understand and answer)

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| BR-01 | Intent triage into the 4 jobs (help / do / be heard / sensitive) | Decide the path in the first 1–2 turns | **LLM classifier with a fixed intent schema + rules that override it for sensitive intents** | Moveworks/Leena: intent → answer, ticket or workflow | 🟡 classify + intent branches exist; no HR schema | P0 | M |
| BR-02 | Grounded answers from the KB (RAG) | Correct, policy-based answers | **Retrieval filtered by the employee's unit and role; answer with the source cited; say "I don't know" below a threshold** | Leena: answer only from allowed knowledge per group; ServiceNow per-KB read rights [dossier MARKET_ALIGNMENT §5c] | 🟡 RAG top-10 at ≥ 0.5; no scope filter; no citation | P0 | M |
| BR-03 | Clarifying questions | Vague requests | Clarify branch | — | ✅ clarifying branch (no feature flag) | P0 | — |
| BR-04 | Slot filling for requests | Collect the fields a request needs | **Category schema → required slots → the LLM asks for missing ones → confirm** | Moveworks slots and in-chat catalog forms [R4, W-MW1] | ❌ | P0 | M |
| BR-05 | Guardrails | Off-topic, abuse, prompt injection, legal advice | **Guardrail branch (exists) + HR policy topics list + output filter** | Every vendor; Kore.ai sells "governance" [W-KO1] | ✅ guardrail branch with examples | P0 | — |
| BR-06 | Never promise outcomes | "Your raise is approved" would be a disaster | **Output rule + eval tests: no commitments on pay, promotion or decisions** | Common rule in HR bots | ❌ (not tested) | P0 | S |
| BR-07 | Sensitive-topic detection | Harassment, self-harm, safety, fraud must not get a chatbot answer | **Detector (keywords + LLM) → fixed safe script → restricted case (CS-09)** | Peakon: fixed sensitive categories; NAVEX/SpeakUp AI intake [dossier §25] | ❌ | P0 | M |
| BR-08 | Personalisation by employee context | Answers differ by unit, grade, contract type, location | **Pass Person attributes (from HR sync) into retrieval and prompt** | Workday/SAP/HiBob answer with HR data [G20, G25, G30] | ❌ (no org data) | P1 | M |
| BR-09 | Multi-intent handling | "I need a payslip and the restaurant is bad" | Handle one by one; create two records | Moveworks handles multiple asks | 🟡 | P1 | S |
| BR-10 | Escalation to a human | Bot can't help, or the user asks for a person | **Explicit "talk to a person" intent + confidence threshold → handover or request** | Universal | 🟡 redirect intent exists | P0 | S |
| BR-11 | Tone and persona | Respectful, short, plain Persian | Prompt + style evals; formal/informal setting | — | ✅ prompts editable | P1 | S |
| BR-12 | Model routing and fallback | Cost, latency, outage | **Seven LLM roles already configurable; add fallback model on error** | — | 🟡 roles configurable; no fallback | P1 | S |

---

## 6. Knowledge management

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| KB-A | KB CRUD, import/export | Basic content management | — | — | ✅ `adcs-knowledgebase` | P0 | — |
| KB-B | Document ingestion (PDF/Word policies) | HR has regulations, not Q&A pairs | **Chunk + embed documents; generate Q&A drafts for review** | Deel builds agents from policy documents [G22] | 🟡 summarise exists; no doc pipeline | P1 | M |
| KB-C | Multi-owner knowledge spaces | HR, welfare, IT, facilities each own their part | **Knowledge space with owner, editors, readers by scope** | ServiceNow: owner per KB, deny beats allow [MARKET_ALIGNMENT §5c] | ❌ | P1 | M |
| KB-D | Scope by audience | Rules differ by region, unit, contract type | **Audience tags on each entry, filtered at retrieval** | Leena: knowledge per employee group | ❌ | P1 | M |
| KB-E | Effective dates and versioning | Policy changes on 1 Farvardin | **valid_from / valid_to + version history + rollback** | Standard KM | 🟡 `start_time` / `end_time` / `is_active` on every QA; a Celery job (every 300 s by default) adds entries to Qdrant when they start and removes them when they end (`adcs_kb/knowledgebase/models/qa.py`, `handlers/qdrant/sync.py`, `config.py:40`). No version history or rollback | P1 | S |
| KB-F | Review and approval before publish | No wrong policy goes live | Draft → review → publish workflow | ServiceNow KM workflow | ❌ | P1 | S |
| KB-G | **Knowledge-gap detection** | Know what employees ask that we can't answer | **Log unanswered and low-confidence turns → cluster → ranked "write this" list per owner** | Moveworks Knowledge Studio: "Knowledge Gap" and "Knowledge Update" recommendations, drafts articles [W-MW3] | ❌ (unanswered questions not logged) | **P0** | S–M |
| KB-H | Stale-content detection | Old answers stay wrong | Flag entries past review date, or entries that keep generating requests | Moveworks "Knowledge Update" [W-MW3] | ❌ | P2 | S |
| KB-I | Answer test bench | Check answers before publishing | Run a question set against the draft KB; diff the answers | — | ❌ | P1 | S |
| KB-J | **Time-bound notices** ("why is the parking closed today?", "why is the restaurant shut?") | Temporary situations change daily; callers ask the same thing all day, and tomorrow the reason may differ | **Notice = a short KB entry with start, end (required), scope (building / site / unit) and owner.** It overrides the standing answer while active, is spoken with its time ("as of 10:30 today…"), is mentioned in the greeting to callers in that scope, and expires automatically. A quick form (panel or SMS) lets the facility owner post it without a KB admin. A spike of calls on one topic suggests "publish a notice?" to the owner (IN-05). Callers can ask "tell me when it is fixed" → SMS/callback on resolve | ServiceNow Employee Center announcements: start/end schedule + audience targeting [W-SN3]; Moveworks API: event-triggered proactive messages to employees [W-MW4]; IVR platforms: scheduled pre-menu announcements with start and end dates [W-VX1]. Iranian HR products: not seen | 🟡 timed KB entries already work (KB-E). Missing: scope by building/unit, priority over the standing answer, time in the spoken answer, greeting mention, quick owner form, spike→notice suggestion, "notify me when fixed" | P1 | S–M |
| KB-K | **Real-time awareness layer** — the bot knows what is happening right now | Answers must reflect today's events and live data, not last month's KB | **Four layers:** (1) static knowledge in the KB; (2) today's events as time-bound notices (KB-J), posted by owners or pushed by systems through an event webhook; (3) live data fetched at answer time via tools/MCP, never copied (HR balances, canteen menu, request status); (4) crowd signal: a burst of calls on one topic raises a real-time alert and suggests a notice. Rule: copy what changes slowly, ask live for what changes fast, announce what matters to many. Every answer carries the time of its fact; if the source is down or stale, say "I don't have current information" rather than guess. Pick which live sources to connect from the unanswered-question log (KB-G) | Moveworks, Workday, SAP, HiBob read live system data at answer time (HiBob via MCP) [§25.5b, G25]; ServiceNow timed announcements [W-SN3]; Moveworks event-triggered messages [W-MW4] | 🟡 layer 1 ✅; layer 2 timed KB ✅ but KB changes reach the bot only every 300 s (Celery beat, `adcs_kb/settings.py:191-194`), no instant sync on save, no event intake; layer 3 tool + MCP mechanism ✅ (`dobby` live `gold_price`), no company-system connectors; layer 4 trends and alerts are periodic, not real-time | P1 (layers 1–2) / P2 (3–4) | S (instant sync, freshness) · S–M (event webhook) · M per live source |

---

## 7. Actions and transactions

Answering is becoming a commodity; **doing** is where HR agents compete now (dossier §25.5b pattern 2).

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| AC-01 | Tool framework | Let the agent do things | **ReAct + tool registry (exists) + MCP client** | Oracle Agent Studio, Leena AOP, HiBob MCP [G31, G28, G25] | ✅ tool registry, MCP client | P0 | — |
| AC-02 | Read-only HR lookups | Leave balance, payslip, insurance status | **Read-only HRIS connector first; OTP before personal data** | Workday, SAP, UKG, ADP all do this [§25.5b] | ❌ | P1 | M |
| AC-03 | Payslip explanation | "Why is my salary lower?" is a top HR question | **Read the payslip lines + explain the differences vs last month** | SAP Payroll Agent, UKG Agentic Pay, ADP [G30, G24, G23] | ❌ | P1 | M |
| AC-04 | Write transactions with confirmation | Submit leave, update an address | **Write only after OTP + read-back + explicit "yes"; idempotent; audit** | Rippling AI, ADP Assist [G19, G23] | ❌ | P2 | L |
| AC-05 | Reminders and notifications | "Remind me of the insurance deadline" | — | — | ✅ `set_reminder`, `read_reminders` | P2 | — |
| AC-06 | Letters and certificates | Employment certificate, salary letter | Template + HR data → PDF → SMS link | Common HR self-service | ❌ | P2 | M |
| AC-07 | Action safety layer | One bad tool call can hurt | **Allow-list per mode and role, rate limits, dry-run, audit of every tool call** | Leena audit trail [dossier §25.5b pattern 7] | ❌ (SMS has no rate limit) | P0 | S |

---

## 8. Requests, cases and ticketing

Full reasoning is in the previous discussion. Short version: **the LLM calls one internal tool (`create_request`); platform code routes, applies SLAs and syncs; the employee always tracks the request through Phoenix.**

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| CS-01 | Request record (the "ledger") | Track every J2 need in one place | **`Request` + `RequestEvent` timeline: type, category, requester, org-unit path at creation, owner team, assignee, status, priority, SLA due, confidentiality, channel, source conversation, external_ref** | Workday Help, Oracle HR Help Desk, SAP ECSC, Leena helpdesk all keep their own case record [W-WD1, W-OR1, W-SAP1, W-LE2] | ❌ (`tickets` app is analytics on imported tickets, with no assignee or SLA) | P1* | M |
| CS-02 | Agent tools: `create_request`, `get_request_status`, `add_request_comment`, `cancel_request` | Voice/chat create and track | **Add to `aiva/tools/registry.py` (same pattern as `set_reminder`)** | Moveworks files, comments on and checks tickets in chat [W-MW2] | ❌ | P1* | S |
| CS-03 | Request catalog (categories + schemas) | Each category needs different fields and owners | **Admin-defined category: required slots, owner rule, SLA, confidentiality, allowed modes** | ServiceNow HR services / catalog items; Workday case types [W-SN2, W-WD2] | ❌ | P1* | M |
| CS-04 | Routing rules | Right team, right unit | **Category × org scope → service team; fallback queue; load-based assignment** | Workday routing rules per category; Darwinbox load-based assignment [W-WD2, W-DB1] | ❌ | P1* | M |
| CS-05 | Built-in desk (inbox) | Customers with no ticketing system | **Lightweight queue: assign, reply, internal note, status, SLA timer, merge duplicates** | Workday Help case workspace; Oracle; SAP ECSC [W-WD1, W-OR1, W-SAP1] | ❌ | P1* | M |
| CS-06 | No-login owner link | Restaurant vendor, building manager with no account | **Signed magic link by SMS/email: view, reply, mark done** | — (INFERENCE: a gap in the big suites) | ❌ | P1 | S |
| CS-07 | External ticketing connectors | Customer already has Jira SM / ServiceNow / Zendesk / local TT | **Connector interface (create, comment, status webhook); Phoenix keeps a mirror; one system owns status** | Leena: ServiceNow, Freshservice, Jira SM, Zendesk…; Moveworks: ServiceNow [W-LE1, W-MW2] | ❌ (MCI's TT system exists, `tt_code`) | P2 | M per connector |
| CS-08 | Email-to-ticket fallback | Any helpdesk that accepts email | Send a formatted email with the request ID; parse replies | Workday accepts cases by email [W-WD2] | ❌ | P2 | S |
| CS-09 | Confidential cases | Harassment, medical, ethics | **Restricted queue; never synced externally; access logged; anonymous follow-up (ID-07)** | Workday: confidential cases only to permitted teams; Oracle cases for harassment [W-WD2, W-OR2] | ❌ | P1 | M |
| CS-10 | Career requests (raise, promotion, level-up) | Not a helpdesk ticket: it is a manager decision | **Route as a "career conversation request" to the line manager + HRBP; no promise of outcome; status = scheduled / discussed / closed** | Workday: compensation changes run as a business process started by the manager, not a help case (INFERENCE from the product model) | ❌ | P2 | S |
| CS-11 | SLA policies with business hours | Promise and measure response times | **SLA per category, Iranian work week + Jalali holidays; pause on "waiting for employee"** | Workday SLA per service team, based on case creation time [W-WD2] | ❌ | P1 | S |
| CS-12 | Status notifications to the employee | "Where is my request?" calls waste capacity | **SMS on every status change + status by voice via the tracking code** | Moveworks "ticket needs user input" notifications [W-MW2] | 🟡 SMS tool exists | P1 | S |
| CS-13 | Duplicate and mass-issue grouping | 200 people report the same broken AC | **Link similar requests to one parent "problem"; notify all on resolve** | Oracle: a case links to several service requests [W-OR1] | ❌ | P2 | M |
| CS-14 | Request satisfaction (CSAT) | Measure the service quality | One-question SMS/voice survey on close | Standard ITSM | ❌ | P2 | S |

\* **P1 with a contract change:** CON-09 in the MVP agreement forbids promising individual follow-up. Requests are out of the pilot unless EX agrees to change it.

### Scope fence: how much ticketing to build

**Position:** "We are not a ticketing system. We record the request, deliver it to the owner, and let the employee track it. If you have a ticketing or office-automation system, we connect to it." That is about 5% of a ticketing system: record, deliver, track.

**Why "connect or nothing" is not enough:**
1. The IVA makes the promise to the employee. A lost request kills trust in *our* channel, and participation is what we sell.
2. Most Iranian organisations have office automation (Chargoon Didgah, Rahkaran, Hamkaran), not an HR ticketing tool (INFERENCE, verify with the market). "Connect only" would leave most local customers with no tracking.
3. Sensitive cases must never go to an external queue, so a small internal queue is needed anyway.
4. The closest foreign analogue, Leena AI (an assistant layer, not an HRIS), ships a light built-in helpdesk plus connectors [W-LE1, W-LE2]. Moveworks connects only to ServiceNow [W-MW2], but it sells to enterprises that all run ServiceNow and is now part of ServiceNow [G11].

| Build (≈ 3–5 weeks, INFERENCE) | Never build |
|---|---|
| Request record (CS-01), LLM tools (CS-02), delivery by connector / email / no-login SMS link (CS-06/07/08), employee tracking by SMS and IVA (CS-12), confidential queue (CS-09) | Full agent workspace (macros, advanced merge, multi-queue, tiered escalation), multi-level escalation matrix and multi-step approval workflows, asset management / ITSM / agent knowledge base, full agent-performance reporting |

**Decision rule:** when a customer asks for anything in the "never" column, the answer is "we connect to your ticketing or office-automation system for that". Connect-or-nothing applies to advanced features, not to tracking itself.

**Why this is on-strategy:** the core product is "hear employees and turn it into action". Request outcomes are insight data (e.g. 200 canteen-quality requests, 150 closed, 50 open for months). We leave the strategy only if we start managing agents' work.

**Tag-based follow-up queue (pilot step 1).** A "needs action" tag on a call (with category and unit), a filtered queue in the COA dashboard, a three-state status (new / in review / closed), a restricted queue for sensitive tags, and a measured tag recall. This is what Qualtrics closed-loop tickets and Amazon Contact Lens rules + tasks do [W-QT3, W-AWS2], and it does not conflict with CON-09. Limits: the employee does not see a tracking code, a missed tag means a missed call (so measure recall and allow manual tagging), and anonymous mode allows only collective actions. In release R2 the `create_request` tool is added and the tag queue stays as the safety net for calls where the IVA did not create a request.

**Plan:** pilot = no tickets (CON-09); tag outcomes as "needs action" with category and unit, which becomes evidence for the next sale. R2 = the 5% fence above; first connectors: email, webhook, Didgah cartable, then MCI's TT system (`tt_code`).

---

### Outbound calls: we call the employee

**Statement (QUOTE, Ali Salimi):** calling the user from our side is possible and has been assessed for feasibility. *The verbatim text and date are not yet recorded in this document; add them here: `<exact quote, date, source>`.*

**Code evidence:** `golang/dobby/internal/tools/call_reminder.go:98-140` (dobby v0.1.0, commit `9d0b9ef07`, 2026-09-27). The `call_reminder` MCP tool stores a reminder, then dials the user's own number through LiveKit SIP (`CreateSIPParticipant` on the configured trunk, `WaitUntilAnswered`), in a room named `outbound_<number>_<random>`; the voice agent reads the reminder from its id.

**Not yet proven:**
1. Read from code only; nothing was run, and the outbound trunk, SBC and number permissions at MCI are outside this repo (TELECOM).
2. Today it only reads a reminder; it is not a conversation.
3. The Python agent's handling of `outbound_` rooms is claimed in a Go comment, but I found no `outbound_` string in `chatbot-iva-agent/src`. Test before promising (INFERENCE).
4. Contact rules are missing: consent (the "may call" flag on Person), quiet hours, frequency caps, opt-out (PL-04).

**What it unlocks:** follow-up calls for tag-queue items (with consent), callback instead of waiting (VX-11), lifecycle pulse calls (PL-01/02), "you said, we did" calls (LP-04). First low-risk step: callbacks for people who agreed on the call, not cold calls.

---

## 9. Conversation analytics: tags, categories, enrichment

Turn every conversation into structured, trustworthy data.

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| AN-01 | Transcripts, both sides, with timestamps | Base data | — | — | ✅ utterances + confidence in the Kafka summary | P0 | — |
| AN-02 | PII redaction before storage | Names, phone numbers and national IDs in text | **Redact in the pipeline before ClickHouse; keep raw only in the restricted store** | Contact Lens and Google redact PII as a standard feature | ❌ (transcripts stored raw, finding 2) | P0 | M |
| AN-03 | Conversation summary | Analysts can't read every call | **LLM summary with a fixed template; minimum-duration guard (VIA-07)** | Contact Lens gen-AI summaries seconds after a contact [W-AWS1] | ✅ summary (coa-ai, frozen) | P0 | S (guard) |
| AN-04 | **Managed HR taxonomy** (category → subcategory → topic) | Consistent categories over time | **Fixed top-down taxonomy owned by EX, versioned; customer-editable** | Qualtrics Text iQ: top-down + bottom-up + automatic, iterative [W-QT1] | 🟡 category/subcategory exist (call-centre oriented) | P0 | M |
| AN-05 | **Automatic topic discovery** | Find what you didn't know to look for | **Cluster embeddings of new conversations → LLM names clusters → "suggested topics" for EX to accept into the taxonomy** | Google CCAI topic model builds a taxonomy with Gemini [W-GO1]; Contact Lens theme detection [W-AWS2]; Qualtrics recommended topics [W-QT1] | ❌ | P1 | M |
| AN-06 | Multi-label tagging per conversation | One call has several issues | **Up to N topics per conversation, each with evidence (quote span) and confidence** | Qualtrics: multiple topics per comment [W-QT1] | 🟡 topics list | P0 | S |
| AN-07 | Tag at the segment level, not only the call | The restaurant complaint is 20 seconds of a 5-minute call | **Tag each issue segment; aggregate per call** | Text iQ tags at sentence level | ❌ | P1 | M |
| AN-08 | Sentiment (aggregate only) | Tone per topic and unit | **Per-topic sentiment, shown only aggregated over the k-threshold** | Perceptyx built its own feedback sentiment model [R7]; Contact Lens −5..+5 [W-AWS3] | ✅ sentiment | P0 | — |
| AN-09 | Emotion detection | — | **Do not use on employees (red line, EU AI Act Art. 5)** | — | ⚠️ `emotions` tag exists: switch off for EX | P0 | S |
| AN-10 | Entity extraction | Which office, restaurant, manager, policy, date | **NER plus mapping to the org tree and facilities list** | Standard text analytics | ❌ | P1 | M |
| AN-11 | Urgency and risk flags | Safety, legal, self-harm, fraud | **Rule + LLM classifier → alert + restricted queue (CS-09)** | Contact Lens rules → alert or task [W-AWS2]; Peakon sensitive categories | ❌ | P0 | M |
| AN-12 | Actionability / "suggestion" tag | Separate complaints from concrete suggestions | Classifier: complaint / suggestion / question / praise | — | 🟡 `suggestions` exists | P1 | S |
| AN-13 | Rule-based categories | Business needs exact rules ("mentions overtime AND negative") | **Rules on keywords + tags + metadata → category, alert or request** | Contact Lens rules [W-AWS2] | ❌ | P1 | M |
| AN-14 | Human review and relabel | Analysts must correct the AI | **Edit tag → stored as gold label → used for eval and few-shot** | Google Quality AI calibration with expected answers [W-GO2] | ❌ | P0 | M |
| AN-15 | Taxonomy migration | Topics get renamed and merged | **Taxonomy versions + mapping table; re-tag history in the background** | — | 🟡 `sync_canonical_mappings` | P1 | M |
| AN-16 | Bot quality scoring | Did the IVA answer correctly and politely? | **Auto-score every conversation on a scorecard (answered, accurate, escalated correctly)** | Google Quality AI scores 100% of conversations [W-GO2] | ❌ | P1 | M |
| AN-17 | Containment and outcome tagging | Was the employee's need met? | Outcome = answered / request created / handed over / abandoned | Moveworks deflection metrics [R5] | ❌ | P0 | S |
| AN-18 | Re-run analytics engine | `coa-ai` frozen since 2025-07 | **Move enrichment to an LLM pipeline the team owns, versioned prompts, eval-gated** | — | ❌ (risk) | P0 | M |

---

## 10. Insights, dashboards and reporting

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| IN-01 | Overview dashboard | Volume, top topics, sentiment, outcomes | — | All listening vendors | ✅ coa-api dashboards (global, not scoped) | P0 | — |
| IN-02 | Org-scope filtering | A unit head sees only their scope | **One `apply_scope(qs, user)` used everywhere, including exports and AQA** | Qualtrics/Medallia hierarchy-based access [MARKET_ALIGNMENT §6] | ❌ | P0 | M |
| IN-03 | k-anonymity threshold | Small groups reveal identity | **Suppress or roll up groups under k (e.g. 5 for numbers, 10 for text)** | Glint, Peakon, Culture Amp all set minimums [MARKET_ALIGNMENT §5b] | ❌ (PRV-05) | P0 | S |
| IN-04 | Trends and anomalies | "Is this rising?" | — | — | ✅ trends with baseline and score | P0 | — |
| IN-05 | Emerging-topic alerts | New problems early | **Spike on a discovered cluster → alert to the owner** | Contact Lens theme detection; CCAI discovery engine [W-AWS2, W-GO1] | 🟡 trend alerts; fixed severity | P1 | S |
| IN-06 | Drill-down to evidence | Trust the numbers | **Click a topic → de-identified quotes and summaries (k-gated)** | Qualtrics Comment Summaries widget [W-QT2] | 🟡 | P0 | S |
| IN-07 | AI comment summaries per topic and unit | Executives read 5 lines, not 500 calls | **LLM summary over the filtered set, with quote references** | Peakon AI summaries, Glint Copilot [G5, G7] | ❌ | P1 | S |
| IN-08 | Natural-language questions on data | "Which province complained most about overtime?" | **AQA, with DB-level row security and the k-threshold** | Glint Copilot, Perceptyx agents [G7, G3] | ✅ AQA (no scope, finding 13) | P1 | M (security) |
| IN-09 | Scheduled reports | Monthly management pack | PDF/Excel by email, scoped per recipient | Standard | ❌ | P1 | S |
| IN-10 | Benchmark across units | Compare regions fairly | Normalise per headcount; k-gated | Culture Amp benchmarks | ❌ | P2 | S |
| IN-11 | Service desk analytics | Request volume, SLA breach, backlog by team | From the CS-01 timeline | ServiceNow / Workday SLA reports | ❌ | P1 | S |
| IN-12 | ROI and KPI dashboard | The buyer renews on numbers | **Containment rate, hours saved, requests per topic, time to resolve, adoption** | Leena and Deel report "hours saved" [dossier §25] | ❌ | P1 | S |
| IN-13 | Export with governance | Analysts want Excel | Scoped export, no identity columns, logged | — | 🟡 export exists, not scoped | P0 | S |

---

## 11. Closing the loop: action on insights

Listening without action destroys participation. Every listening leader sells this, and Phoenix has none of it.

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| LP-01 | Topic ownership | Every top issue has an owner | Assign a taxonomy topic to a team (same model as CS-04) | Medallia and Qualtrics route insights to owners | ❌ | P1 | S |
| LP-02 | Action plans | Track what was done about a topic | **Action item: topic, owner, due date, status, linked evidence** | Qualtrics, Culture Amp, Glint action planning | ❌ | P1 | M |
| LP-03 | Manager nudges | Managers don't open dashboards | Weekly digest + one suggested action per manager (k-gated) | Culture Amp AI Coach, Perceptyx agents [G8, G3] | ❌ | P2 | M |
| LP-04 | "You said, we did" broadcast | Show employees that speaking up works | **IVA mentions resolved topics in greetings or at the end of calls; SMS/intranet post** | Common EX best practice | ❌ (greeting management APIs just landed) | P1 | S |
| LP-05 | Annotations on trends | Explain spikes (e.g. "new canteen contractor") | — | — | ✅ `TrendAnnotation` | P1 | — |
| LP-06 | Impact measurement | Did the action fix the topic? | Before/after trend per action plan | — | ❌ | P2 | S |

---

## 12. Proactive listening (outbound and programs)

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| PL-01 | Outbound pulse calls | Hear from people who never call | **Short adaptive voice survey (3–5 questions + one open follow-up)** | Qualtrics conversational feedback [G1]; Listen Labs / Outset AI interviews [G18] | 🟡 outbound dialing exists in `golang/dobby` (`call_reminder`, LiveKit `CreateSIPParticipant`); no survey flow, no contact rules; not tested on the real MCI trunk | P2 | M |
| PL-02 | Lifecycle moments | Onboarding day 30, exit interview, after a transfer | **Triggered by HR-sync events → outbound call or SMS link** | ServiceNow lifecycle events; Exid/Lyzr exit-interview agents [W-SN2, G18] | ❌ | P2 | M |
| PL-03 | Campaigns | Feedback on a new policy for 2 weeks | Campaign = topic + audience + channel + date range | — | 🟡 `campaign_rank` tool (disabled, unrelated) | P2 | M |
| PL-04 | Contact-permission and quiet hours | Don't call people at night or against their wishes | Opt-out list, time windows, frequency cap | Telemarketing compliance practice | ❌ | P2 | S |

---

## 13. Privacy, security and compliance

Dossier finding: **the engine is built; trust is not.** Most P0s are here.

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| SC-01 | Authentication on every API | Chat APIs are open at app level | **JWT check in each service, not only at the gateway** | — | ❌ (finding 12) | P0 | S |
| SC-02 | Role × data-tier matrix | Who sees numbers, summaries, text, audio, identity | **ScopeGrant + data tier (MARKET_ALIGNMENT §6b)** | Glint/Peakon role tiers | 🟡 RBAC exists | P0 | M |
| SC-03 | Audit log | Who saw what, when | **Append-only log of reads of text, audio, identity, exports and config changes** | Leena audit trail; HiBob Trust Center [G25] | ❌ (finding 3) | P0 | M |
| SC-04 | Audio ownership check (IDOR fix) | Any `view_calls` user can fetch any audio | Ownership/scope check on file access | — | ❌ (finding 1) | P0 | S |
| SC-05 | Secrets out of logs | Bearer tokens are logged | Header allow-list in the middleware | — | ❌ (finding 3) | P0 | S |
| SC-06 | Role expiry enforced | Temporary grants must end | Filter `expires_at` in the JWT builder | — | ❌ | P0 | S |
| SC-07 | Retention and deletion | Keep only as long as needed | Per-data-type retention; delete on request | — | ✅ archive job; 🟡 no per-type policy | P1 | S |
| SC-08 | Data residency / on-prem | Iranian government buyers; sanctions | **Private deployment with local LLMs (current model)** | Foreign SaaS can't serve this market [dossier §25.2] | ✅ | P0 | — |
| SC-09 | Employee data rights | See and delete my memory and requests | Self-service "what you know about me" via OTP | GDPR practice | ❌ | P2 | M |
| SC-10 | AI transparency notice | Employees should know it's an AI and how data is used | Spoken disclosure at call start + a written policy page | EU AI Act transparency duty | 🟡 | P0 | S |
| SC-11 | Trust pack for buyers | The buyer asks for proof | Security and privacy page, architecture, test results | HiBob AI Trust Center [G25] | ❌ | P1 | S |
| SC-12 | Pen-test and certification | Government buyers | External pen-test; certification as required | — | ❌ | P1 | L |

---

## 14. Org data and integrations

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| IG-01 | Org tree model (OrgLevel, OrgUnit with path, Person, ChannelKey, ScopeGrant) | Scope, routing and personalisation all depend on it | **Model from MARKET_ALIGNMENT §6a; org path stored on every record at creation time** | Medallia and Qualtrics store hierarchy at response time [W4, W12] | ❌ | **P0** | M |
| IG-02 | HR data sync | Manual Excel goes stale | **One canonical format; Excel, SFTP and SAP are just ways to deliver it** | Culture Amp: connectors, daily SFTP or manual upload [W14] | ❌ (SEG-07) | P0 (Excel) / P1 (SAP) | S / M |
| IG-03 | SSO (LDAP/AD, OIDC) | Staff log in to chat and the panel | OIDC/LDAP in adcs-auth | Standard | ❌ | P1 | M |
| IG-04 | Ticketing connectors | See CS-07 | — | — | ❌ | P2 | M each |
| IG-05 | Outbound webhooks / event stream | Customer automation | **Events: request.created, request.status_changed, alert.raised, topic.emerging** | Contact Lens → EventBridge [W-AWS2] | 🟡 trend webhook | P1 | S |
| IG-06 | Public API | Customers build on Phoenix | Versioned REST API with API keys and scopes | — | 🟡 internal APIs | P2 | M |
| IG-07 | Phoenix as an MCP server | Expose de-identified insights to local HR assistants (Rahkaran, Didgah) | MCP server over insight APIs, k-gated | HiBob MCP; Darwinbox [G25, G14] | ❌ (MCP client only) | P2 | M |
| IG-08 | Local messenger and SMS gateways | Delivery channels | Adapter per gateway | — | ✅ Resan SMS | P1 | S |

---

## 15. Admin and configuration studio

A product, not a project, means the customer can change things without a release.

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| AD-01 | Greeting and closing messages | Per channel, campaign and mode | — | — | ✅ greeting management APIs (recent commit) | P0 | — |
| AD-02 | Prompt and persona settings with versions | Safe changes | Versioned prompts, eval before publish, rollback | — | 🟡 editable in AQA; not versioned | P1 | S |
| AD-03 | Category / taxonomy editor | EX owns the taxonomy | UI for AN-04 / CS-03 | Qualtrics topic editor | ❌ | P1 | M |
| AD-04 | Routing, SLA and calendar editor | Ops owns routing | UI for CS-04 / CS-11 / CH-10 | Workday admin rules | ❌ | P1 | M |
| AD-05 | Alert rules editor | Thresholds per customer | UI for AN-13 / IN-05 | Contact Lens rules UI | ❌ (AN-09, CON-06) | P1 | S |
| AD-06 | Scenario studio (no-code flows) | New line, e.g. "welfare services", in a day | **Policy docs + a few rules + a tool selection → new assistant** | Oracle Agent Studio, Leena AOP Studio, Deel [G31, G28, G22] | ❌ | P2 | L |
| AD-07 | Feature flags per customer | Turn branches on and off safely | Config flags (classify/clarify have none today) | — | 🟡 | P1 | S |
| AD-08 | Sandbox / test call | Try changes before going live | Test number or web voice pointed at a staging config | — | 🟡 websocall | P1 | S |

---

## 16. AI quality, evaluation and AI ops

Without numbers there are no acceptance criteria (dossier finding 5).

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| QA-01 | Golden eval sets | Regression safety | **Per area: STT (WER), intent, answer faithfulness, tagging accuracy, sensitive recall** | Google Quality AI calibration sets [W-GO2] | 🟡 only AQA has an eval endpoint | P0 | M |
| QA-02 | Eval in CI | Don't ship regressions | Run evals on prompt, model and KB changes; block below threshold | — | ❌ | P1 | M |
| QA-03 | Simulated callers | Test voice end-to-end at scale | LLM-driven caller personas + TTS → the real pipeline | Voice-agent platforms offer simulation testing | ❌ | P1 | M |
| QA-04 | Hallucination and grounding check | Policy answers must come from the KB | Faithfulness check on answers; log ungrounded answers | — | ❌ | P1 | M |
| QA-05 | Feedback capture | Learn from users | "Was this helpful?" by voice/SMS; analyst thumbs-down with reason | Universal | ❌ | P1 | S |
| QA-06 | Human review sampling | Spot-check AI decisions | Sample N% of conversations and all sensitive ones for review | Quality AI sampling rules [W-GO2] | ❌ | P1 | S |
| QA-07 | Model and prompt registry | Know which version produced which tag | Store model, prompt version and taxonomy version on every output | — | ❌ | P1 | S |
| QA-08 | Drift monitoring | Topic mix or STT quality changes | Weekly metrics on confidence, unknown rate, WER sample | — | 🟡 Prometheus metrics | P2 | S |

---

## 17. Platform, operations and cost

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| OP-01 | Repeatable customer deployment | Second customer in a week | **Helm/Ansible profile per customer; config, not forks** | — | 🟡 Helm/Ansible; per-customer bot forks exist | P1 | M |
| OP-02 | Multi-tenancy | SaaS economics later | Tenant ID in data + config; keep private deploy for government | — | ❌ (no tenant concept) | P2 | L |
| OP-03 | HA and failover | Calls die with their node | Multiple workers and zones; drain on deploy | — | 🟡 drain timeout | P1 | M |
| OP-04 | Observability per layer | Find the failing layer fast | Network → SIP → app → AI dashboards, request tracing | — | 🟡 Prometheus + APM | P1 | S |
| OP-05 | Cost per conversation | Unit economics and pricing | **Token and audio usage per call (already in the summary) → cost dashboard** | — | 🟡 data exists | P1 | S |
| OP-06 | Internet-outage resilience | Iranian outages | All models local; no foreign dependency | Chargoon writes about this risk [B9] | ✅ mostly | P0 | — |
| OP-07 | Load test with real SIP | Payday peaks | SIP load generator (e.g. SIPp) through the SBC | — | ❌ (WebSocket only) | P0 | S |
| OP-08 | Kafka resilience and DLQ | No lost data | — | — | ✅ grogu DLQ; 🟡 coa ticket produce errors only logged | P1 | S |

---

## 18. Commercial and customer success

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| CM-01 | Onboarding kit | Go live fast | Org data template, starter taxonomy, starter KB, scripts | Leena publishes deployment playbooks (CHRISTUS case) [R3] | ❌ | P1 | S |
| CM-02 | Starter HR content packs | Value on day one | Persian HR policy Q&A templates (labour law, insurance, leave) | Qualtrics premade EX topics [W-QT1] | ❌ | P1 | M |
| CM-03 | Usage metering | Price by employee, conversation or minute | From OP-05 | — | 🟡 | P2 | S |
| CM-04 | Support process and SLA | Buyer guide question 9 | Ticket process, response times, on-call | — | ❌ | P1 | S |
| CM-05 | Adoption campaigns | Employees must know the line exists | Posters, SMS, intranet; measure reach per unit | — | ❌ | P1 | S |

---

## 18b. Recruiting: from interview scheduling to the candidate's status

A different buyer (talent acquisition), a different user (a **candidate**, not an employee) and a higher risk (AI in hiring is **high-risk** under EU AI Act Annex III; NYC Local Law 144 requires a yearly independent bias audit and candidate notice) [W-LAW1, W-LAW2]. Dossier §25.2 lists it as Iranian white space: no Persian voice interviewing seen.

**Scope fence (same idea as ticketing):** we are the **voice and messaging layer** of the candidate journey, not an ATS. We schedule, remind, reschedule, run a short structured phone pre-screen, collect interviewer feedback, and tell the candidate their status. The ATS (Jobvision, Jobinja, the customer's HR system or a simple Phoenix candidate list) stays the record. **The AI never decides**: it suggests, a person decides and records the reason.

| # | Feature | Need | Solution options | What others do | Phoenix today | Pri | Eff |
|---|---|---|---|---|---|---|---|
| RC-01 | Candidate record and pipeline stages | Know where each candidate is | **Thin record: candidate, job, stage (applied → pre-screen → interview → feedback → decision → notified), owner, history; mirror of the ATS when one exists** | Paradox syncs with Workday, SuccessFactors and other ATSs [W-PX1]; Jobinja shows the candidate each review stage [W-JI1] | ❌ | P2 | M |
| RC-02 | Interview self-scheduling | Back-and-forth phone calls waste recruiter time | **Interviewer availability slots → candidate picks by SMS link, chat or voice → invites to all; Jalali calendar and Iranian holidays** | Paradox: calendar sync, candidate picks a slot in chat, invites to all, panels and multi-location [W-PX1] | ❌ | P2 | M |
| RC-03 | Reminders and no-show reduction | No-shows waste interview slots | **SMS + outbound call 24 h and 1 h before; "reply 1 to confirm"** | Paradox reminders 24 h and 1 h before [W-PX1] | 🟡 SMS, `set_reminder`, outbound `call_reminder` exist (dobby) | P2 | S |
| RC-04 | Reschedule and cancel by voice or SMS | People's plans change | Candidate or interviewer says "I can't make it" → offer new slots | Paradox reschedules for either side [W-PX1] | ❌ | P2 | S |
| RC-05 | Structured phone pre-screen | High-volume roles (call centre, stores, field) need a fast first filter | **Short fixed question set (availability, location, shift, expected pay, must-have licence); same questions for everyone; transcript + summary to the recruiter; knock-out only on objective facts the candidate states** | Paradox, UKG Rapid Hire, HeyMilo, Ribbon, Alex [dossier §25.3] | 🟡 IVA, outbound call, transcript, summary exist; no screening flow | P2 | M |
| RC-06 | AI structured first-round interview | Interview hundreds in parallel | Competency questions with rubric; AI scores **with evidence quotes**, a human reviews every report | Eightfold AI Interviewer, Alex, HeyMilo [dossier §25.3] | ❌ | P2 (bet) | L |
| RC-07 | Interviewer feedback collection | Feedback is late or missing, decisions stall | Scorecard link by SMS right after the interview; reminders until filled; the AI drafts a summary from the scorecard and the interview notes | Paradox lists "ratings & feedback" [W-PX2] | ❌ | P2 | S |
| RC-08 | Human decision with recorded reason | Fairness, appeal, audit | **Decision only by a person; reason required; AI suggestions shown separately and logged** | Common model: AI screens, humans decide [W-LAW3] | ❌ | P2 | S |
| RC-09 | Candidate status updates and "what's my status?" | Silence is the top candidate complaint | **SMS on each stage change; candidate calls the IVA and hears their status with a code** | Jobinja notifies the candidate at each stage [W-JI1]; Jobvision: the employer calls the candidate to arrange the interview [W-JV1] | 🟡 SMS + IVA exist | P2 | S |
| RC-10 | Candidate notice and consent | Legal and trust: the candidate must know an AI is talking and recording | Spoken notice at call start; consent record; human alternative on request | NYC LL144: notice 10 business days before use [W-LAW2] | ❌ | P2 | S |
| RC-11 | Fairness monitoring | STT errors differ by accent, so scores can be unfair by region | **Selection rate by group (four-fifths rule), WER by accent on screening calls, rubric review** | Bias audits with impact ratios [W-LAW3] | ❌ | P2 | M |
| RC-12 | Candidate data retention | Rejected candidates' recordings must not live forever | Short retention for audio, transcript kept per policy; delete on request | GDPR / AI Act logging duties [W-LAW1] | 🟡 retention job exists for calls | P2 | S |

**Judgment:** keep it P2 until the EX pilot is proven: it is a new buyer and a new sales motion. The cheap, low-risk part (RC-02/03/04/07/09: scheduling, reminders, rescheduling, feedback chasing, status updates) reuses what is already built (outbound calls, SMS, reminders, IVA) and makes no hiring judgment. RC-05 is the natural next step. RC-06 (AI interviewer) is a bet that needs fairness work (RC-11) first, because Persian STT quality varies by accent.

---

## 19. Key judgments

1. **Answering is a commodity; channel, language and trust are the moat.** All 13 HCM vendors now have an HR service agent (dossier §25.5b). None has Persian voice on the phone with on-prem models. Compete on CH-01, VX-*, SC-08 and the privacy block, not on "our bot answers better".
2. **Trust is the P0, not features.** SC-01 to SC-06, ID-01, IN-02/03 and AN-02 are small jobs, mostly S and M. Without them the buyer test fails, however good the AI is.
3. **The org tree (IG-01) is the hidden dependency.** Scope, k-threshold, routing, personalisation and segment analytics all depend on it. Build it before any of those.
4. **Taxonomy = top-down + discovered + human-corrected.** Every leader (Qualtrics, Google, AWS) combines a managed taxonomy with automatic discovery. Fixed categories alone miss new problems; discovery alone gives unstable dashboards. Do AN-04 + AN-06 + AN-14 now and AN-05 next.
5. **Knowledge-gap logging (KB-G) is the cheapest high-value feature.** It is a few days of work. It improves the bot every week and gives EX a concrete report ("employees asked 340 times about X and we had no answer").
6. **Requests need a contract decision first.** Technically it is one tool plus a ledger (S–M). Politically, CON-09 says no follow-up in the MVP and the listening channel promises anonymity. Agree the modes (ID-01) with EX before building CS-*.
7. **Raise and promotion are not tickets.** Route them as manager conversations (CS-10). A queue for "I want a raise" creates an expectation HR can't meet and blames the product.
8. **Close the loop or participation dies.** LP-02 and LP-04 are what make employees call a second time. They are cheap; schedule them right after the pilot proves volume.
9. **Re-own the analytics engine (AN-18).** The tags HR will judge the product on come from `coa-ai`, untouched for 14 months and built for customer call centres. Moving enrichment to an eval-gated LLM pipeline is a P0 risk item, not a refactor.

---

## 20. Suggested release cut

Deadlines follow the README rule: **T + n working days from a named input**, never a calendar date.

| Release | Goal | Features |
|---|---|---|
| **R0 — Trust (pilot gate)** | Pass the buyer's privacy test | SC-01/03/04/05/06/10, ID-01/04/05/06/08, IN-02/03/13, AN-02/09, BR-06/07, AC-07, OP-07, IG-01, IG-02 (Excel) |
| **R1 — Pilot proof** | Show measurable value | KB-G, AN-04/06/14/17/18, BR-01/02/04/10, VX-08, IN-06/07/12, QA-01/05 |
| **R2 — Second sale** | Requests + action | CS-01..06, CS-09/11/12, LP-01/02/04, IN-05/09/11, AN-05/10/11/13, CH-04, CH-13, KB-J, KB-K step 1, ID-03/07 |
| **R3 — Productise** | Second customer in a week | AD-*, OP-01/03/05, QA-02/03, CM-01/02, IG-03/05, KB-B/C/D/E/F |
| **R4 — Bets** | Differentiate further | AC-02/03/04, PL-*, CS-07/10/13, IG-07, AD-06, OP-02, RC-01..05/07..12 (recruiting voice layer), RC-06 later |

---

## 21. Red lines: what not to build

From dossier §25.8, plus the new areas:

- **No individual emotion detection on employees** (EU AI Act Art. 5): emotions only aggregated, or off.
- **No individual attrition-risk score.** Group level only, k-gated.
- **No passive listening** of email, chat or work calls; voluntary channels only.
- **No automatic HR decisions** (pay, promotion, discipline). The AI suggests and routes; people decide.
- **No full ITSM or BPM engine.** Keep the desk lightweight and integrate for the rest.
- **No full whistleblowing product.** A private queue only (CS-09).
- **No memory in anonymous mode**, ever.

---

## Sources

**Already in the repo:** dossier §25.9 (G1–G31, R1–R*, B1–B12, W-series in MARKET_ALIGNMENT) — `product/source/product_dossier_fa.html`, `product/source/market_alignment_fa.html`.

**New for this catalog:**

| Code | Topic | Link |
|---|---|---|
| W-WD1 | Workday Help case management | https://doc.workday.com/admin-guide/en-us/human-capital-management/hcm-innovation-services/workday-help/case-management/hot1559060224551.html |
| W-WD2 | Workday Help: routing, confidential, SLA, email/Teams/Slack intake | https://doc.workday.com/admin-guide/en-us/human-capital-management/hcm-innovation-services/workday-help/case-management/syz1562672658215.html |
| W-OR1 | Oracle HR Help Desk | https://www.oracle.com/human-capital-management/hr-help-desk/ |
| W-OR2 | Oracle HR case management | https://blogs.oracle.com/fusioninsider/newhr-case-management-for-hcm-help-desk-available-now |
| W-SAP1 | SAP Employee Central Service Center | https://sap.com/africa/products/hcm/employee-central-service-center.html |
| W-SAP2 | SAP ESM vs ECSC/HRSD | https://www.pentos.com/insights/events-and-webinars/recorded-webinars/HR-Service-Delivery |
| W-SN1 | ServiceNow + Workday, Employee Center | https://blog.vsoftconsulting.com/blog/elevate-hr-with-a-servicenow-and-workday-integration |
| W-SN2 | ServiceNow HRSD lifecycle events | https://docs.servicenow.com/bundle/orlando-hr-service-delivery/page/product/human-resources/concept/hr-lifecycle-event-configuration.html |
| W-MW1 | Moveworks for HR | https://help.moveworks.com/docs/moveworks-for-hr |
| W-MW2 | Moveworks ServiceNow ticketing | https://help.moveworks.com/docs/servicenow-ticketing-integration-overview |
| W-MW3 | Moveworks Knowledge Studio recommendations | https://help.moveworks.com/service-management/knowledge-studio/ai-powered-recommendations |
| W-LE1 | Leena AI integrations | https://leena.ai/integrations |
| W-LE2 | Leena AI helpdesk | https://docs.leena.ai/docs/helpdesk-overview |
| W-DB1 | Darwinbox helpdesk listing | https://platform.softwareone.com/product/employee-helpdesk/PCP-5387-7166 |
| W-AV1 | AllVoices anonymous two-way messaging | https://support.allvoices.co/hc/en-us/articles/8497429800091-How-can-an-employer-properly-investigate-a-report-if-it-is-anonymous |
| W-DL1 | Deel anonymous reporting | https://www.deel.com/solutions/anonymous-reporting/ |
| W-AWS1 | Contact Lens gen-AI summaries | https://aws.amazon.com/about-aws/whats-new/2024/07/amazon-connect-contact-lens-ai-powered-summaries/ |
| W-AWS2 | Contact Lens rules and theme detection | https://docs.aws.amazon.com/connect/latest/adminguide/build-rules-for-contact-lens.html · https://aws.amazon.com/about-aws/whats-new/2023/05/amazon-connect-contact-lens-theme-detection/ |
| W-AWS3 | Contact Lens sentiment | https://aws.amazon.com/blogs/contact-center/announcing-contact-lens-for-amazon-connect-preview/ |
| W-GO1 | Google CX Insights topic model | https://docs.cloud.google.com/contact-center/insights/docs/release-notes |
| W-GO2 | Google Quality AI | https://docs.cloud.google.com/contact-center/insights/docs/qai-setup-guide |
| W-QT1 | Qualtrics Text iQ | https://www.qualtrics.com/support/survey-platform/data-and-analysis-module/text-iq/text-iq-functionality/ |
| W-QT2 | Qualtrics EX Comment Summaries | https://qualtrics.com/support/employee-experience/creating-ee-project/dashboards-tab/widgets-ee/analysis-widgets-ee/comment-summaries-widget-ex |
| W-KO1 | Cognigy / Kore.ai / Parloa comparison | https://fin.ai/learn/cognigy-vs-kore-ai-vs-parloa |
| W-PA1 | Cognigy vs PolyAI | https://aiagentrank.io/compare/cognigy-vs-polyai |
| W-QT3 | Qualtrics closed loop / ticket tasks | https://www.qualtrics.com/support/vocalize/common-use-cases-voc/closing-the-loop/ · https://dxtraining.iowa.gov/digital-services/qualtrics/understanding-qualtrics-cx/closed-loop-ticket-system |
| W-SU1 | SpeakUp voice message with distortion (RIPE NCC policy) | https://www.RIPE.net/documents/3151/Whistleblower_Policy_2024.pdf |
| W-FU1 | FaceUp anonymised voice notes | https://faceup.com/en/compare/speakup-alternative |
| W-WL1 | Whistlelink oral reporting with voice distortion | https://www.whistlelink.com/product-news/january-2024/ |
| W-AWS4 | AWS WhatsApp voice notes + Transcribe | https://cpaasintel.rsunga.people.aws.dev/articles/94ac33693b9d |
| W-MD1 | Medallia voice/video feedback (third-party comparison) | https://www.enterpret.com/comparisons/qualtrics-vs-medallia |
| W-SN3 | ServiceNow Employee Center announcement (schedule + audience) | https://www.servicenow.com/docs/r/SogDT~k7ktsbe1ZYegnaLg/dtd_XHDQWqpVhDwveChZkQ |
| W-MW4 | Moveworks proactive messaging API | https://moveworks.com/us/en/company/news/press-releases/moveworks-announces-api-proactively-prevent-issues |
| W-VX1 | Scheduled IVR announcements (Voxo) | https://docs.voxo.co/pharmacy/announcements |
| W-PX1 | Paradox conversational scheduling | https://paradox.ai/products/scheduling |
| W-PX2 | Paradox feature list (ratings & feedback) | https://www.paradox.ai/franchise/kfc |
| W-JI1 | Jobinja employer panel: stages, interview details | https://jobinja.ir/how-to |
| W-JV1 | Jobvision FAQ: employer arranges interviews | https://jobvision.ir/faq |
| W-LAW1 | EU AI Act and hiring (high-risk, timing contested) | https://resources.rework.com/libraries/ai-for-hr/ai-hiring-laws |
| W-LAW2 | NYC Local Law 144 (bias audit, notice) | https://www.pivotpointsecurity.com/what-is-nycs-ai-bias-law-and-how-does-it-impact-firms-using-hr-automation/ |
| W-LAW3 | AI interview bias audits 2026 (four-fifths rule, human review) | https://humanly.io/blog/ai-interview-bias-audit-2026 |
| W-TD1 | HR tier-0 resolution figures (vendor, unverified) | https://www.infosys.com/newsroom/documents/robust-hr-service-delivery-solution.pdf · https://www.applaudhr.com/blog/artificial-intelligence/hr-meets-ai-enhancing-service-delivery-with-artificial-intelligence |

Third-party and vendor-marketing sources (W-KO1, W-PA1, W-DB1, W-TD1) are weaker. Verify them before quoting to a buyer.
