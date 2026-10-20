# product/ — Phoenix product-management and technical documentation

Product-facing documentation derived **directly from the code** in this monorepo, for the
Technical PM role. Every claim here is backed by a `file:line` you can open.

- Code reviewed: **2026-09-28**; updated through commit `cb570a50b` (**2026-10-06**) — see §26 of both dossiers
- Scope: the 10 Python projects with commits since 2026-06-28 (~98k LOC)
- Agreement reviewed: `HR - meet UAT agreement - Fit-Gap MVP` (87 rows, 8 blocks) — the
  Employee Experience (EX) voice-of-employee pilot between MCINEXT and MCI's EX department

## What's in this folder

Documents are split by audience: **`product-management/`** for business, scope, customers and
competitors; **`technical/`** for architecture, code and operations. Both dossiers keep the
original chapter numbers (§1–10 and §25 are product, §11–24 are technical), so cross-references
like "§12" or "PRV-03" stay valid across the two. Every claim carries a source line — `CODE`
(path:line), `GIT` (commit), `DOC` (repo markdown), `BOARD` (whiteboard), `FIT-GAP` (agreement
row), `TELECOM` (industry-standard telecom fact), `WEB` (public source, listed in §25.9) or
`INFERENCE` (reasoning, verify before committing); all paths relative to the repo root.

Every document is published as a **dark-themed standalone HTML page** and (except the tracker) a PDF.

### `product-management/`

| File | Audience | What it is |
|---|---|---|
| `PRODUCT_DOSSIER_FA.pdf` | TPM, stakeholders | §1–10: exhaustive feature catalog, Fit-Gap verdict, critical findings, risks, unit economics, deadline strategy, Now/Next/Later scope, meeting Q&A. §25: HR product ideas, global and Iranian competitors, 13 HCM/HRIS vendors, feature-extraction matrix, approaches from competitor blogs, SAP deep dive, Chargoon, buyer-readiness test against Chargoon's selection guide, red lines, web sources. §27: Persian summary of `FEATURE_CATALOG.md` (17 domains, the ticketing decision "one internal `create_request` tool, platform routes inside or outside", 9 judgments, release cut R0–R4) |
| `FIT_GAP_TRACKER.xlsx` + `FIT_GAP_TRACKER_FA.html` | You (to fill in) | The 87 agreement rows plus code-verified status, evidence, confidence, dependency owner, proposed conditional deadline and action. RTL, filterable, with a live summary sheet |
| `ROADMAP_FA.pdf` | TPM, CTO, tech leads | How to think (8 decision principles), what to build (table stakes / differentiators / beyond-current), wave roadmap with exit criteria, team operating model, technical direction, metrics tree, risks, first 20 days |
| `INSPIRATION_PLAYBOOK_FA.html/.pdf` | TPM, tech leads, developers | Plain-Persian playbook: the Iranian competitors (Sokhan, Amerandish, Sitak, Asr Gooyesh, Part, Poshtyar, Chargoon, Porsline) and foreign sources of inspiration most similar to Phoenix, why each resembles us, how their key features work, what we already have, how to build it and how feasible it is. Ends with a versioned feature list: **v1 = MCI UAT agreement rows (with Fit-Gap IDs)**, v2/v3 = later |
| `MARKET_ALIGNMENT_FA.html/.pdf` | TPM, CTO, tech leads | Translates the MCI Fit-Gap needs into market patterns: 9 product building blocks (org tree + scope, data tiers, k-threshold, HR sync, knowledge spaces, insight engine, sensitive routing, program/channel, eval); all 87 rows tagged Generic / Config / MCI-only next to their code verdict; how Qualtrics, Viva Glint, Peakon, Medallia, Culture Amp, NICE, ServiceNow and Leena model access; the معاونت/اداره scope model with enforcement points and corner cases; COA/AIVA/Chatbot/auth shape; sequencing on the roadmap waves |
| `ANSWER_PACK_FA.pdf` | EX department and MCI evaluation committee | Buyer-facing draft answering Chargoon's HR software selection guide (7 Mehr 1405): problem as process, scope tiers, 8 testable criteria, role × data matrix, demo scenario with exceptions, the 10 demo questions, required inputs from EX, proposed acceptance criteria, cost-proposal structure. Yellow dashed fields need EX data or a joint decision before sending |
| `FEATURE_CATALOG.md` | TPM, CTO, tech leads | English master feature list for the whole EX product (voice + chat, answers, requests/ticketing, conversation tagging, insights, privacy, integrations, admin, AI quality, ops): 180 features in 18 domains (including recruiting), each with the need, solution options, what world leaders do (sourced), Phoenix status from code, priority and effort. Ends with key judgments, a release cut R0–R4 and red lines. Edit directly; not part of `build.sh` |
| `AI_LEARNING_GUIDE_FA.html/.pdf` | TPM, anyone on the team | Plain-Persian guide to staying current in AI: core concepts (tokens, SFT/RLHF, RAG, MoE, quantization), reading a Hugging Face model card field by field, an abbreviation glossary, what each benchmark measures and its pitfalls, a voice chapter (WER/CER for Persian, RTFx, MOS, turn-detection latency), curated leaderboards, papers, newsletters and courses, a weekly routine, a 10-minute model check and exercises |
| `IVA_EX_PROMPT_REQUIREMENTS_FA.html/.pdf` | Prompt-engineering team, IVA tech team, EX | Plain-Persian PRD for the new EX voice agent ("دستیار هوشمند صدای کارکنان"), derived from EX's Instruction v1.0: ~70 numbered, testable requirements (intro, tone, listening-first, follow-up, metadata confidentiality, voice types, KB answering and the three "can't answer" cases, summary, sensitive voice, angry callers, guardrails, closing) plus voice-channel and prompt-security additions, proposed tool contract, the prompt-engineering process, a prompt skeleton, 25 eval scenarios, release gate, open decisions, risks and a traceability matrix |

### `technical/`

| File | Audience | What it is |
|---|---|---|
| `TECHNICAL_DOSSIER_FA.pdf` | Engineers, tech leads, TPM when reviewing | Voice AI basics (VAD, Turn, STT/ASR, TTS, Egress); call path (service number → backbone → SBC → SIP/RTP → LiveKit → agent); §11 repo map; tech-stack philosophy (why each language, datastore and service, untapped capabilities, audio channel/codec trade-offs, CTO decision sheet); §12–24: architecture, agentlib, AIVA orchestration, IVA voice agent, CCA pipeline, AQA, auth, data model and messaging, config reference, CI/deploy, developer cookbook, tech debt, endpoint catalog; abbreviations and glossary |
| `IVA_COA_PIPELINES.html` | Engineers | IVA and COA pipeline walkthrough (overview, IVA, COA, gaps) |

### Shared

| File | Audience | What it is |
|---|---|---|
| `README.md` | Engineers, future you | This file — the "how" behind the system and how to regenerate everything |
| `source/` | Maintainers | HTML and TSV sources plus `build.sh`; everything above except `IVA_COA_PIPELINES.html` is reproducible from here |

### Using the tracker

Sheets: **راهنما** (guide & legend) · **ردیف‌ها** (the 87 rows) · **خلاصه** (live counts) ·
**یافته‌های بحرانی** (critical findings) · **معماری** (services & infra).

- Blue cells are yours to fill: `اولویت EX` (EX's priority) and `ددلاین نهایی` (final deadline).
- Status colours: green = confirmed in code · amber = partial · red = claim refuted by code ·
  grey = no code exists · blue = empty in the agreement.
- The summary sheet uses `COUNTIF`, so editing a status in **ردیف‌ها** updates the counts. Formula
  values compute when Excel/LibreOffice opens the file (it was written without a calc engine).
- **Deadline rule:** never a calendar date — write `T + n working days from receipt of <input>`.
  TEC-14's own acceptance criterion forbids committing a timeline without named dependencies.

## Voice AI concepts (and where they live here)

| Concept | What it is | In Phoenix |
|---|---|---|
| **VAD** — Voice Activity Detection | Detects whether someone is actually speaking vs. silence/noise. Used to start/stop processing, trigger STT, and decide when the user has finished talking. | Silero VAD loaded per worker (`chatbot-iva-agent/src/main.py:89`), tuned by `AGENT_VAD_*` (`src/config.py:62-67`). Standalone gRPC VAD in `rust/vad`; per-channel VAD on stereo recordings in `golang/voice-segmenter`. |
| **Turn** / turn-taking | One party's speaking segment. Turn-taking decides when to stop listening and start responding — critical for natural voice UX. | Endpointing delay 0.5–3 s (`src/config.py:69-73`); turn detector `deactive`/`mci`/`openai` (`:82-110`); barge-in after 0.4 s of user speech (`:68`), recorded as `interrupted` (`src/schema.py:22`); user-away prompts (`:401-427`). In AIVA each user turn is one `UserInputEvent` (`python/aiva/docs/RequestFlow.md:16`). |
| **STT** — Speech-to-Text (a.k.a. **ASR**) | Transcribes speech to text for the LLM or business logic. | Real-time: OpenAI-compatible client, 3 retries, 10 s timeout, per-utterance `transcript_confidence` (`src/config.py:29-31,364`; `src/schema.py:26`). Offline on recorded calls: `golang/grogu/internal/asr/service.go:85` behind a circuit breaker. Chat API: `POST /api/v1/chat/asr` in adcs. Models served on Triton via `golang/neurobox-gateway`. |
| **TTS** — Text-to-Speech | Converts the LLM's text response into audio for the user. | Sentence-by-sentence streaming to cut time-to-first-audio (`src/config.py:164`); 3 retries, `204` non-retryable (`:36-43`); `POST /api/v1/chat/tts` in adcs; announcement voices in coa-api (`coa/apps/iva/services.py:254`); TTS cache in neurobox-gateway (commit `57f969bc6`). |
| **Egress** | The outbound media path: synthesized audio sent to the caller/WebRTC client, or — in LiveKit specifically — recording/streaming a room's output elsewhere. | Agent audio is published into the LiveKit room and reaches the caller over SIP. LiveKit Egress records `participant` + `agent` tracks (on) and `room` (off) to MinIO bucket `chatbot-mci-iva` (`src/config.py:124-138,158`; `src/utils/egress_recorder.py:47`); recording paths travel in the Kafka session summary (`src/schema.py:115-131`). |

Typical flow of one voice turn:

```
caller audio -> VAD (is someone speaking?) -> turn detection (finished?) -> STT (text)
             -> LLM / aiva (answer, streamed) -> TTS (sentence by sentence)
             -> egress (audio track -> LiveKit room -> SIP -> caller)
                 └─ egress recording (participant + agent tracks -> MinIO)
VAD keeps listening during playback: user speech > 0.4 s => barge-in, TTS stops.
```

Perceived latency (time-to-first-audio) ≈ endpointing delay + STT + first LLM sentence + first
TTS chunk. The first term is directly tunable via `AGENT_MIN_ENDPOINTING_DELAY` (`src/config.py:70`).

Paths in this table are relative to `python/chatbot-iva-agent/` unless they start with `python/`,
`golang/` or `coa/` (`= python/coa-api/coa/`).

## The system, in one page

```
caller ──SIP──▶ SBC/SIP proxy* ──▶ LiveKit room ──▶ chatbot-iva-agent (VAD · turn · STT · TTS · egress)
                                                    │  text                    │ session summary
                                                    ▼                          ▼
                                        aiva  /api/v1/chat/completions     Kafka: chatbot-mci-iva
                                  (guardrail ∥ intent ∥ classify ∥ clarify    │
                                   ∥ voice-bridge ∥ retrieval → ReAct+tools)  ├─▶ aiva memory consumer
                                        │ Qdrant (contexts, guardrail, …)     │   (topic chatbot-mci-iva-intent)
                                        │ adcs-knowledgebase (KB CRUD)        ▼
                     TelC calls ──Kafka──▶ grogu (Go: MinIO audio · ASR via neurobox-gateway · MyMCI · DLQ) ──▶ Postgres
                                                                         │ Kafka
                                                                         ▼
                                                                         coa-ai  (frozen since 2025-07-13)
                                                                              │ results
                                                                              ▼
                                                                         ClickHouse ──sync daemons──▶ Postgres
                                                                                                        │
                                               aqa (NL→SQL, eval) ◀──── analysts ────▶ coa-api dashboards/trends
                                               adcs-auth issues JWTs verified statelessly by every service
```

\* The telephony edge (operator core, backbone, SBC, SIP proxy — often assumed to be Kamailio) is
**not in this repo**; see the next section.

### How each stage works

**1. Telephony → voice agent** — `python/chatbot-iva-agent`. A LiveKit worker joins each call's
room. Call identity comes from SIP headers (`call_id`, `x-originalcallid`, `city_code`, caller
number); `AGENT_ORIGINAL_CALL_ID_FALLBACK` covers a missing header. Everything is tuned by env
(`src/config.py`): VAD speech/silence thresholds, barge-in (`AGENT_MIN_INTERRUPTION_DURATION`),
turn detection (off / MCI model / LLM probability), greeting text, user-away and non-speech
prompts, background and "thinking" audio. STT/LLM/TTS each retry 3× with 10 s timeouts. TTS
streams sentence by sentence to cut perceived latency. `exit_tool` hangs up;
`redirect_to_human_agent` sends a SIP message (default destination `6040`).

**2. After the call** — LiveKit Egress records caller and agent tracks separately to MinIO
(`chatbot-mci-iva`). A `SessionSummarySchema` (`src/schema.py`) is published to Kafka with the
phone number, ids, timings, exit/redirect flags, **every utterance with `transcript_confidence`**,
recording paths, and **token/audio usage** — enough to compute exact cost per call.

**3. Conversation brain** — `python/aiva`, documented in `docs/RequestFlow.md`. One
`UserInputEvent` starts concurrent branches; `IVAChatOrchestrator` picks exactly one winner by
fixed precedence — guardrail denial › exit/redirect intent › clarifying › main (ReAct) — and
cancels the rest. Losing output never reaches the client or the history. Classifier failure falls
back to `main`. One embedding fans out to five Qdrant retrievals. Seven LLM roles are independently
configurable (`aiva/chat/config.py`); defaults are `google/gemma-4-31B-it` and
`openai/gpt-oss-120b`. VoiceBridge is **off by default**; classification/clarifying have **no
feature flag yet** (explicit TODO).

**4. Knowledge** — `adcs-knowledgebase` exposes QA CRUD, guardrail examples, tagging, summarise,
import/export. Retrieval: top-10 from `aiva-contexts` at similarity ≥ 0.5, optional LLM filter.
All KB writes are human API calls — there is no auto-update path. Unanswered questions are **not**
logged.

**5. Tools** — `aiva/tools/`. Enabled by default: `send_sms` (Resan gateway), reminders, gold
price, joke. Present but disabled: websearch, rubika, campaign_rank. The LLM decides when to send
SMS; there is no rate limit.

**6. Ingestion** — `golang/grogu` consumes TelC call records, IVA sessions and tickets from Kafka, downloads audio from MinIO, merges stereo channels, calls ASR (through `neurobox-gateway`, which fronts Triton over gRPC) behind a circuit breaker, enriches with MyMCI account data, upserts `calls`/`call_records`/`call_ai_tags` in the **same Postgres schema coa-api owns**, and dead-letters failures.

**7. Call analytics** — `python/coa-api` (Django/DRF) does **not** run the analysis; it reads
results from ClickHouse and syncs them to Postgres (`call_ai_tags`: sentiment, bad words,
greeting/farewell, satisfaction, category/subcategory, topics, summary, suggestions, emotions,
overlap, `raw_input` ASR text). Long-running management commands, one container each:
`clickhouse_sync`, `clickhouse_update_sync`, `failed_calls_sync`, `sync_canonical_mappings`
(Tehran-hour window), `trend_sync`, `archive_old_calls`. Celery runs with `concurrency=1`.

**8. Trends** — `coa/apps/trends`. Per subject × period × province: baseline, `trend_signal`,
`trend_score`, `is_trend`. Rebuilt every run (`_purge_stale`); `TrendAnnotation` is deliberately
denormalised so human notes survive the rebuild. Alerts go out via webhook with a fixed
`severity: "high"`.

**9. Retention** — `archive_old_calls`: weekly windows older than `ARCHIVE_CALLS_MONTHS` →
copy to temp tables → `pg_dump` → upload to MinIO → **only then** delete from five tables →
`VACUUM`. Aborts before deleting if dump or upload fails; supports `--dry-run`.

**10. NL analytics** — `python/aqa` (FastAPI). Multi-agent NL→SQL with SSE, runtime-editable
prompts/SQL examples/schema (`/api/v1/configs/*`), feedback, and the repo's only eval endpoint
(`POST /api/v1/eval/run`).

**11. Auth** — `adcs-auth` issues JWTs; services verify statelessly. `UserRole` has an `expires_at` field (`adcs-auth/adcs_auth/role/models.py:51`), but nothing reads it: the JWT builder (`adcs_auth/jwtoken/serializers.py:14-24`) still includes permissions from expired roles. A time-limited "resolve identity" grant for PRV-01/02 needs that filter added first. Permission-based RBAC
(`coa/apps/users/permissions.py`); users without `view_all_calls` are row-scoped to their own
`agent_id` in call search (`coa/apps/main/services/call.py:849`).

## Telephony: from dialing a number to the IVA agent (start of the pipeline)

Dossier chapter: **«مسیر تماس: از شماره‌گیری تا IVA Agent»** (right after the Voice AI basics).
Telecom facts there carry the `TELECOM` label: industry-standard VoIP behaviour, not read from this
repo and not MCI's real topology. Confirm them with the Network/VoIP teams before committing.

```
Caller ─▶ operator core ("Zone": number routing, signaling) ─▶ backbone (IP/MPLS, fiber)
       ─▶ DC edge (router → firewall/ACL → switch/VLAN) ─▶ SBC (SIP trunk ends here) ─▶ SIP proxy
═══════════════════════ Phoenix starts here ═══════════════════════
       ─▶ LiveKit SIP → room (participant "sip_+98…") ─▶ chatbot-iva-agent ─▶ aiva
```

**SIP ≠ audio.** SIP (INVITE → 100 → 180 → 200 OK+SDP → ACK … BYE) sets the call up and tears it down.
The voice itself is RTP over UDP, with IP/port/codec negotiated in SDP (typically G.711 A-law,
8 kHz, 20 ms; ≈87 kbps per direction per call, so 500 calls ≈ 44 Mbps each way). A wrong firewall
or NAT setting usually shows up as "connected but no audio", not "call failed".

### Abbreviations used in this section

| Abbr. | Full form | Meaning here |
|---|---|---|
| SIP | Session Initiation Protocol | call signaling (setup / teardown) |
| RTP | Real-time Transport Protocol | the actual voice, over UDP |
| SDP | Session Description Protocol | IP / port / codec negotiation inside SIP |
| SBC | Session Border Controller | security/control gateway for SIP at the network edge |
| PBX | Private Branch Exchange | enterprise phone switch |
| STT / TTS | Speech-to-Text / Text-to-Speech | audio ↔ text |
| LLM | Large Language Model | the model that writes the answer |
| RAG | Retrieval-Augmented Generation | fetch knowledge at answer time and add it to the prompt |
| VAD | Voice Activity Detection | is someone speaking? |
| ACL | Access Control List | allow/deny list for traffic |
| VLAN | Virtual Local Area Network | logical network separation |
| QoS / DSCP / EF | Quality of Service / Differentiated Services Code Point / Expedited Forwarding | traffic priority marking (voice = DSCP 46, EF) |
| NAT | Network Address Translation | classic cause of one-way or no audio |
| CAC | Call Admission Control | cap on accepted concurrent calls |
| DTMF | Dual-Tone Multi-Frequency | keypad tones |
| MOS | Mean Opinion Score | voice quality, 1–5 |
| WER | Word Error Rate | STT accuracy |
| DC / PoP | Data Center / Point of Presence | site types in the design |
| LLD | Low-Level Design | detailed network design |
| HA | High Availability | more than one node/site so one failure does not stop service |
| BGP / MPLS | Border Gateway Protocol / Multiprotocol Label Switching | inter-network routing / backbone transport |
| UDP / TCP / TLS | User Datagram Protocol / Transmission Control Protocol / Transport Layer Security | transports (RTP uses UDP; SIP uses UDP/TCP, TLS on 5061) |
| ACK | Acknowledgement | confirms the 200 OK in SIP |
| ASR | Answer-Seizure Ratio (telecom) | share of answered calls — **not** Automatic Speech Recognition here |
| APM / KPI / SLA | Application Performance Monitoring / Key Performance Indicator / Service Level Agreement | ops and contract terms |
| TPM / EX | Technical Product Manager / Employee Experience | roles / the pilot programme |
| KB / API | Knowledge Base / Application Programming Interface | |
| PCMA / PCMU | Pulse Code Modulation A-law / μ-law | the two G.711 variants |
| G.711, E.164 | ITU-T codec standard / ITU-T numbering plan | 8 kHz 64 kbps phone codec / `+98…` number format |
| RFC | Request for Comments | internet standard document (SIP = RFC 3261) |
| MCI | Mobile Telecommunication Company of Iran | Hamrah-e Avval |

### Project and platform abbreviations (whole dossier)

| Abbr. | Full form | Source |
|---|---|---|
| AIVA | Agentic Intelligent Virtual Assistant | `python/aiva/pyproject.toml` |
| IVA | Intelligent Virtual Assistant | inferred from AIVA; not defined on its own in the repo |
| AQA | Agentic Query Analyzer (a.k.a. Spotter) | `python/aqa/README.md` |
| ADCS | Agentlib Django Customer Support | `python/adcs/README.md` title |
| CCA | Call Center Analyze | dossier cover |
| COA, TelC, MyMCI, MCINEXT | internal names | full forms are **not defined** in the repo; not guessed |
| UAT / MVP | User Acceptance Testing / Minimum Viable Product | |
| SAP | Systems, Applications and Products (ERP) | employee-data source in SEG-07 |
| MCP | Model Context Protocol | |
| DLQ / SSE | Dead Letter Queue / Server-Sent Events | |
| JWT / DRF / CRUD | JSON Web Token / Django REST Framework / Create-Read-Update-Delete | |
| PSTN / WebRTC | Public Switched Telephone Network / Web Real-Time Communication | |
| ASR (outside the telephony chapter) | Automatic Speech Recognition | same as STT |

The dossier has the complete list in the appendix chapter «فهرست اختصارات کل سند».

### The 24 steps to production

| # | Step | Done when | In Phoenix |
|---|---|---|---|
| 1 | Business requirement (inbound/outbound, hours, recording, human transfer) | signed doc incl. capacity & transfer target | recording = egress; transfer target `6040` |
| 2 | Capacity & call flow | peak concurrency + flow diagram | 1 LiveKit job per call |
| 3 | Service number (سرشماره) allocation | number in numbering plan | external — **a number alone is not a working service** |
| 4 | Routing in operator network | test call's INVITE visible at SBC | external |
| 5 | Connectivity design (DC, PoP, redundancy, bandwidth) | LLD approved | external |
| 6 | Backbone connectivity (connectivity + routing + IP + security) | path provisioned | external |
| 7 | Fiber installation (fiber is only the medium) | link up, optical levels OK | external |
| 8 | Router / switch / VLAN / IP / routing | two-way ping + traceroute, no asymmetric routing | external |
| 9 | Firewall / ACL / QoS (SIP 5060/5061, RTP UDP range, DSCP EF) | two-way SIP **and** RTP port tests | external |
| 10 | SBC (security, NAT, topology hiding, CAC, normalization) | answers operator `OPTIONS` | external |
| 11 | SIP trunk (peer IPs, transport, E.164, max channels) | `OPTIONS 200` both ways | external |
| 12 | SIP configuration: LiveKit dispatch rule, **custom headers preserved** | `sip.h.*` visible in participant attributes | hard dependency; see headers below |
| 13 | RTP / codec / media | two-way audio, loss < 1 %, jitter < 30 ms | `AGENT_SIP_RTP_STABILIZATION_DELAY` |
| 14 | Connect to IVA (room + dispatch) | "starting voice assistant for participant sip_…" | `src/main.py:108-109` |
| 15-18 | STT → agent/LLM/RAG → backend APIs → TTS | golden scenarios pass | agent + `aiva` |
| 19 | End-to-end test | per-layer checklist green | — |
| 20 | Load test at peak concurrency | success ≥ 99 %, latency under cap | only `golang/websocall/tests/loadtest.js` (WebSocket, **no SIP**) |
| 21 | HA / failover | node killed under load, service continues | `AGENT_DRAIN_TIMEOUT=1800s`; in-flight calls die with their node |
| 22 | Monitoring (network → SIP → app → AI) | dashboards + alerts per layer | Prometheus `:9400` + APM; network/SIP/RTP metrics are external |
| 23 | Pilot | pilot KPIs met | phone whitelist does **not** gate admission (finding 9); restrict at routing/SBC |
| 24 | Production | go-live sign-off | — |

### What happens when a call reaches Phoenix

Paths are relative to `python/chatbot-iva-agent/`.

0. **Prewarm**: each worker process loads Silero VAD and an `IVAAgentSession` once
   (`src/main.py:88`); `AGENT_NUM_IDLE_PROCESSES=1` warm spare.
1. **Dispatch**: LiveKit hands the room's job to a worker, which connects with `AUDIO_ONLY` (`src/main.py:108`).
2. `wait_for_participant()`: the SIP caller joins as `sip_+98…` (`src/main.py:109`).
3. **Phone number**: regex `sip_\+?([a-zA-Z0-9]+)`, then normalization. 10 digits → `98`+n; 11 digits
   starting `0` → `98`+rest (`src/main.py:79,320-335`). An empty result becomes `"agentlib"`.
4. **Agent type** from `AGENT_LLM_STRUCTURE` (`agentlib` | `chatbotlib`) (`src/main.py:145`).
5. **SIP headers** are read from `participant.attributes` (table below).
6. **Session**: POST `{"phone": …}` to `AGENT_LLM_SESSION_BASE_URL` (`src/agents/agentlib.py:64-93`).
   aiva's `POST /api/v1/chat/session` get-or-creates the user by phone, creates a session, and has
   `GreetingAgent` write a greeting from that number's **long-term memory**
   (`python/aiva/aiva/chat/views/session.py:55,72`). On failure: `session_id="unknown"` plus
   `agent_llm_session_failed_requests_total`.
7. `session.start()` (`src/entrypoint.py:68`). VAD, turn detection, STT and TTS are now live.
8. Sleep `AGENT_SIP_RTP_STABILIZATION_DELAY` (default `0.0`; `src/entrypoint.py:77`). CHANGELOG:
   "in some cases it took a while to sip call become active". This is the first knob to turn if the
   start of the greeting is clipped.
9. **Greeting** via `session.say`, interruptible by default (`src/entrypoint.py:86`).
10. Background/thinking audio, a shutdown callback (Kafka summary → `chatbot-mci-iva`), and egress
    recordings (`src/entrypoint.py:92-94`). The turn loop starts.

| SIP attribute | Kind | Used for | If missing |
|---|---|---|---|
| `sip.h.x-originalcallid` | operator custom | `call_id` / `original_call_id` in Kafka summary | `"unknown"` or session id (`AGENT_ORIGINAL_CALL_ID_FALLBACK`) |
| `sip.h.x-subscityid` | operator custom | `city_code` | `"unknown"` |
| `sip.h.call-id`, `sip.h.via`, `sip.h.X-channelId` | standard / switch custom | human transfer | transfer skipped, caller hears the failure message |

> SBCs often strip unknown `X-*` headers. Calls still work, but summaries fall back to
> `call_id="unknown"` and transfers fail silently. **Make "all five headers arrive" an acceptance
> criterion of the SIP trunk.**

### How a call ends

- **Caller hangs up** → BYE → participant leaves → shutdown callback → Kafka summary.
- **`exit` tool** → wait for playout → `delete_room()` (`src/agents/chatbotlib.py:377-380`).
- **`redirect_to_human_agent`** (`src/agents/agentlib.py:202-286`): the agent parses IP:port from `Via`,
  then POSTs to `sip-messager` `/api/v1/send-sip-message`. That service sends a SIP **MESSAGE** (not
  REFER) to `sip:msg@<ip>:<port>` with `X-Resolution: Done`, `X-Destination: 6040`, body `ping`, and
  expects `202` within 15 s (`golang/sip-messager/internal/api/api.go:165-241`, `config/config.go:23,125`).
  The operator switch performs the actual transfer, so this is a two-sided dependency.
  `delete_room()` always runs. Metric: `agent_sip_redirect_requests_total`.
- **User away** (off by default): after 10 s of silence the agent prompts; once past 3 prompts it says
  goodbye and deletes the room (`src/config.py:401-427`, `src/agents/agentlib.py:460-471`).

### Symptom → suspect layer

| Symptom | Check first |
|---|---|
| no ring / fast busy | does the INVITE reach the SBC? → numbering/routing |
| `403` at SBC | source IP in SBC/firewall allow-list |
| connected, total silence | RTP port range in firewall; IP in SDP reachable (NAT) |
| one-way audio | NAT / asymmetric routing / one-direction firewall rule |
| drops ~32 s after answer | ACK not arriving (Record-Route / NAT) |
| drops at a fixed duration | SBC session timer / max call duration |
| greeting start clipped | raise `AGENT_SIP_RTP_STABILIZATION_DELAY` (e.g. 0.5 s) |
| robotic / choppy audio | jitter/loss/QoS, or worker CPU |
| connected, agent silent | free worker for dispatch? session API ok? TTS reachable? |
| `call_id="unknown"` in summaries | `X-originalCallID` stripped at SBC/proxy |
| "امکان انتقال … وجود ندارد" | `Via`/`X-channelId` present? sip-messager got `202`? switch implements MESSAGE? |

### For the TPM: "which layer are we on?"

"The number is allocated but IVA isn't usable" does not mean the work is almost finished. Track it as:

```
Number ✅ → Routing ⏳ → Fiber ⏳ → IP ⏳ → SBC ⏳ → SIP trunk ⏳ → Headers verified ⏳
→ IVA integration ⏳ → E2E ⏳ → Load ⏳ → HA ⏳ → Monitoring ⏳ → Pilot ⏳ → Production
```

Steps 3–13 are external dependencies with named owners. Write IVA deadlines as
`T + n working days from step 12 green (headers verified)`, never as a calendar date.

### RAG vs fine-tuning

RAG supplies knowledge at inference time from a knowledge base. Fine-tuning changes model weights
to learn a behaviour or task. Changing knowledge such as prices and packages → RAG, which is what
aiva does (Qdrant `aiva-contexts`, top-10, similarity ≥ 0.5). Tone, format or a specific task → a
fine-tuning candidate. The most plausible one here is STT on 8 kHz Persian telephone audio. The repo
has **no fine-tuning code**.

## Findings that change the agreement

| # | Finding | Evidence | Row(s) |
|---|---|---|---|
| 1 | **IDOR on raw audio** — gated by `view_calls` only, no ownership check on `name` | `coa/apps/files/views.py:19` | PRV-03 claimed "exists" |
| 2 | **Transcripts are stored** and published to Kafka | `models.py:397` `raw_input`; `services/call.py:771`; `chatbot-iva-agent/src/schema.py` | AI-02, PRV-08 claimed "out of scope" |
| 3 | **No audit log** anywhere; request middleware logs all headers incl. bearer tokens | grep → 0 hits; `coa/middlewares.py:26` | PRV-06 claimed "exists" |
| 4 | Analysis engine `coa-ai` untouched for 14 months | `git log -1 -- python/coa-ai` → 2025-07-13 | block 3 quality rows |
| 5 | No quality eval for AIVA/CCA (only aqa has one) | — | 11 quality claims |
| 6 | Board-3 "delete topic + its calls" pruner is **not** implemented | all delete paths audited | — (good news) |
| 7 | Retention is stronger than claimed | `archive_old_calls.py` | PRV-07, PRV-08 |
| 8 | SMS is already built | `aiva/tools/sms.py` | KB-06 claimed "needs dev" |
| 9 | Phone whitelist gates memory collection, not call admission; bypassed by default | `aiva/memory/config.py:20-21` | VIA-02, VIA-03 |
| 10 | aqa is production-grade and demoable | `python/aqa` | AN-12 |
| 11 | AIVA keeps **long-term memory per phone number** across calls; phone + memory also go into tracing spans | `aiva/memory/…/aiva_consume_kafka.py`; `aiva/chat/views/session.py` | CON-05, CON-02, PRV-01 |
| 12 | **All chat APIs are unauthenticated** at app level (`permission_classes = ()`); protection is delegated to the gateway | `aiva/chat/views/*.py`, `adcs/chat/views/*.py` | security |
| 13 | **AQA is a second path to identity** — free-form SQL over ClickHouse; read-only only via the DB user | `aqa/agents/tools/sql_executor.py` | PRV-02 |

Before UAT, fix: #1, the header logging in #3, and add a minimum-duration guard before
summarisation (VIA-07 — prevents fabricated summaries from dropped calls).

## Verify it yourself

```bash
# 1. IDOR: as a user with view_calls but NOT view_all_calls, request another agent's file
curl -H "Authorization: Bearer $TOKEN" "$COA/api/v1/files?name=<other-call-id>.wav"   # 200 today

# 2. transcript persistence
psql -c "select call_id, left(raw_input,80) from call_ai_tags where raw_input is not null limit 3;"

# 3. no audit trail
grep -rniE "audit|LogEntry|viewed_by|actor_id" python/{coa-api,adcs,aiva,adcs-auth,aqa}

# 4. frozen engine
git log -1 --format='%ad %s' --date=short -- python/coa-ai

# 7. retention, safely
python manage.py archive_old_calls --dry-run
```

## Regenerating

No third-party Python packages are required (the xlsx is written as raw OOXML).

```bash
cd product/source
./build.sh   # xlsx + tracker page, theme, then HTML + PDF of every document
```

- `fitgap_part{1,2,3}.tsv` — the agreement, verbatim, tab-separated
  (`block, id, requirement, description, acceptance, claimed_status, notes`)
- `verdicts.tsv` — code verdict per ID
  (`id, verified_status, evidence, confidence, owner, proposed_deadline, action`).
  Edit this when the code changes, then rebuild. The build fails if any ID is missing.
- `product_dossier_fa.html` → `product-management/PRODUCT_DOSSIER_FA.pdf` (§1–10, §25)
- `technical_dossier_fa.html` → `technical/TECHNICAL_DOSSIER_FA.pdf` (§11–24)
- `roadmap_fa.html`, `answer_pack_fa.html` → `product-management/`
- `inspiration_playbook_fa.html` → `product-management/INSPIRATION_PLAYBOOK_FA.{html,pdf}`
- `fit_gap_tracker_fa.html` is generated by `build_xlsx.py` from the same sheets as the xlsx.
- Design: `theme/phoenix_fa.css` + `theme/phoenix_fa.js` (dark by default, light via the
  toolbar, chapter sidebar on wide screens, BLAME toggle). `apply_theme.py` inlines them into
  every HTML source between marker comments, so edit the theme, never the inlined copy.
- The two dossiers share the same sources guide and glossary; edit both if you change those.

## Limits of this review

- `python/coa-ai` was out of scope (stale); AI-04–AI-07 are marked **نامشخص** (unverified) for
  that reason, and AI-12/AI-13 as "not found in active code" — they may exist there.
- Go/Rust services were read for role and main flow only (`grogu` handlers, `neurobox-gateway`,
  `websocall`, `dobby`). Kamailio/SBC/LiveKit-SIP configuration is **not in this repo**: the
  agent-side SIP handling (headers, redirect via `sip-messager`, RTP stabilization) is traced from
  code, while everything upstream of the LiveKit room is labelled `TELECOM` (industry pattern) in the dossier.
- Nothing was executed against a running environment; verdicts are from static reading.
