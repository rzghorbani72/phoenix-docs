"""English content for the Phoenix EX pipeline map. Layout lives in build_pipelines.py.

Step body conventions: str = paragraphs, list = bullets, {"table": rows}, {"ol": items},
{"note": text, "kind": "warn|bad"}, {"code": text}; a tuple holds several bodies.
Status: live | off (configured but disabled) | notdeployed | external (outside the cluster or
outside our repos) | unknown. Every code claim carries a path:line reference.
"""

from content_en_brain import BRAIN_STEPS

OPS = "chatbot-ops/prod/chatbot-ex/values.yaml"
AG = "python/chatbot-iva-agent@3524df3f"

UI = {
    "brand": "Phoenix EX pipelines",
    "nav_map": "Pipeline map", "nav_models": "Models", "nav_risks": "Risks & gaps", "other_lang": "فارسی",
    "status": {"live": "Live", "off": "Configured, off", "notdeployed": "Not deployed",
               "external": "External / outside repo", "unknown": "Unverified"},
    "legend_hint": "Click any step for its deep dive. Dashed boxes in the .drawio copy are off or not deployed.",
    "sys_title": "System at a glance", "steps_word": "steps",
    "prev": "←", "next": "→", "back": "Back to the map",
    "used_in": "Used in these steps", "col_sev": "Severity", "col_issue": "Issue", "col_why": "Why it matters",
    "col_where": "Steps", "sev": {"high": "High", "med": "Medium", "low": "Low"},
}

META = {
    "title": "Phoenix EX (Employee Voice): every pipeline, step by step",
    "title_plain": "Phoenix EX pipelines",
    "lede": "How an employee's phone call becomes a live AI conversation, how the agent decides each answer, where its knowledge comes from, and how every call becomes analytics. Each box opens a deep dive: the model, its size, why it is used, inputs and outputs, settings and the exact logic.",
    "source": "Read from code and prod config on 2026-11-02: `chatbot-ops` prod @ `dd851385e` (includes the 2026-11-02 move of the EX main agent and guardrail to a dedicated Gemma-4 31B); `phoenix` main @ `7b7c602eb`. Code refs follow what prod actually runs: aiva v0.31.1 (= commit `206e55746`; main is already at 0.33.3), voice agent `3524df3f` from the unmerged branch `feat-soniox-lang` (main v0.40.0 has no Soniox), coa-api v5.22.0 (= main). Paths are relative to each repo.",
    "footer": "Status labels: Live = in prod config and wired. Configured, off = present but disabled by a flag. Not deployed = code exists, no prod component. External = outside the cluster or outside both repos. Text marked (inferred) is reasoning, not code. Model sizes are public model facts, not read from code.",
}

LANES = [
    {"id": "call", "prefix": "V", "color": "teal", "short": "1 · Phone call", "tagline": "LiveKit voice agent",
     "title": "1 · Phone call: voice in and out", "title_plain": "1. Phone call: voice in and out",
     "desc": "From the employee dialing in to the last audio frame: VAD, speech-to-text, turn detection, text-to-speech, recording and the call summary. Component: `chatbot-ex-iva-agent` (6 replicas).",
     "handoff": "Each committed user turn goes to lane 2 (V7). After hang-up the recording and summary feed lane 5.",
     "steps": ["v-ingress", "v-session", "v-vad", "v-stt", "v-turn", "v-endpoint", "v-aiva", "v-tts",
               "v-bargein", "v-silence", "v-end", "v-record", "v-summary"]},
    {"id": "brain", "prefix": "B", "color": "violet", "short": "2 · The brain (aiva)", "tagline": "one turn = a chain of LLM agents",
     "title": "2 · The brain: one turn inside aiva", "title_plain": "2. The brain: one turn inside aiva",
     "desc": "What `aiva` (`iva-chatbot` v0.31.1, 4 replicas) does with one employee utterance: guardrail, classification, retrieval, the ReAct answer agent and tools. Prompts are pulled from the Phoenix prompt registry (`ex_iva_*`, tag `production`).",
     "handoff": "Retrieval details are in lane 3. The streamed answer returns to lane 1 (V8 text-to-speech).",
     "steps": []},  # filled from content_en_brain
    {"id": "kb", "prefix": "K", "color": "orange", "short": "3 · Knowledge base", "tagline": "curated Q&A → vectors → filter",
     "title": "3 · Knowledge base: authoring, indexing, retrieval", "title_plain": "3. Knowledge base: authoring, indexing, retrieval",
     "desc": "The approved HR answers the agent may use. Authoring and indexing run in `iva_kb` / `iva_kb_worker` (`aiva-knowledgebase:df70f4be`). Retrieval runs inside aiva on every turn.",
     "steps": ["k-author", "k-summarize", "k-sync", "k-embed", "k-collections", "k-search", "k-filter", "k-carry"]},
    {"id": "analytics", "prefix": "A", "color": "pink", "short": "5 · Post-call analytics", "tagline": "COA / CCA for EX",
     "title": "5 · Post-call analytics (COA / CCA)", "title_plain": "5. Post-call analytics (COA / CCA)",
     "desc": "After hang-up, every EX call is re-transcribed, analysed by the CCA engine and shown in the EX panel. EX has its own COA stack inside the `chatbot-ex` release.",
     "steps": ["a-ingest", "a-merge", "a-asr", "a-publish", "a-cca", "a-store", "a-sync", "a-api", "a-panel", "a-aqa"]},
    {"id": "memory", "prefix": "M", "color": "cyan", "short": "4 · Memory & data", "tagline": "history, memory, where data lives",
     "title": "4 · Memory and stored data", "title_plain": "4. Memory and stored data",
     "desc": "What the agent remembers inside a call and across calls, and where employee data is stored (important for HR privacy).",
     "steps": ["m-history", "m-longterm", "m-writer", "m-stores"]},
    {"id": "ops", "prefix": "P", "color": "blue", "short": "6 · Models & platform", "tagline": "serving, gateway, tracing",
     "title": "6 · Models, serving and observability", "title_plain": "6. Models, serving and observability",
     "desc": "Where the models run, how traffic reaches them, and where a TPM can see tokens, latency, prompts and traces.",
     "steps": ["p-serving", "p-gateway", "p-phoenix", "p-metrics"]},
]

SYSTEM_EDGES = [
    {"from": "call", "to": "brain", "label": "each turn", "dy": -12},
    {"from": "brain", "to": "call", "label": "answer → TTS", "dy": 14},
    {"from": "brain", "to": "kb", "label": "retrieve"},
    {"from": "call", "to": "analytics", "label": "Kafka summary + .ogg"},
    {"from": "brain", "to": "memory", "label": "history · memory"},
    {"from": "kb", "to": "ops", "label": "all LLM / embedding calls"},
]

KEY_POINTS = [
    {"note": "**In one sentence:** Soniox (cloud) transcribes the employee → a Gemma-4 26B-A4B model decides the turn is over → aiva runs guardrail, retrieval (Hakim embeddings + Gemma-4 E2B filter) and a Gemma-4 31B ReAct agent (guardrail and agent share one dedicated 31B instance) → neurobox TTS speaks the answer → after hang-up, grogu re-transcribes the call and the external CCA engine tags it for the EX panel."},
    {"note": "**Things to know before you read:** prod runs code that is not on local `main`. Two steps send employee data outside the cluster (Soniox speech-to-text, OpenAI greeting). The LLM call-tagging engine (CCA) and the EX panel source are not in our repos. See [Risks & gaps](risks.html).", "kind": "warn"},
]

STEPS = {
    # ------------------------------------------------------------------ lane 1: call
    "v-ingress": {
        "title": "Call ingress and dispatch", "title_plain": "Call ingress + dispatch", "status": "external",
        "chip": "SIP → LiveKit 10.154.0.4 → agent worker", "chip_plain": "SIP → LiveKit",
        "summary": "The employee's call reaches a dedicated LiveKit server over SIP. LiveKit opens a room and hands it to one of the pre-warmed Python agent processes.",
        "facts": [("Component", "LiveKit server + SIP (VM `10.154.0.4`, not in any repo) → `chatbot-ex-iva-agent`"),
                  ("Model", "none"), ("Capacity", "6 pods × 10 warm processes ≈ 60 concurrent calls (inferred)"),
                  ("Config", "`LIVEKIT_URL=ws://10.154.0.4:7880`, `AGENT_NUM_IDLE_PROCESSES=10`")],
        "sections": [
            ("What happens", {"ol": [
                "The telecom edge / SBC (outside our repos) delivers SIP to the LiveKit SIP service on `10.154.0.4`. Only EX uses this LiveKit server.",
                "LiveKit creates a room with a SIP participant whose identity looks like `sip_+98912…`.",
                "The worker has no `agent_name`, so LiveKit auto-dispatches every new room to it (inferred from LiveKit semantics) (`src/main.py:363-371`).",
                "The job joins audio-only, waits for the participant, and extracts the phone number with regex `sip_\\+?([a-zA-Z0-9]+)`, normalised to `98…` (`main.py:79, 320-333`).",
                "SIP headers `x-originalcallid` and `x-subscityid` are read. If the call id is missing EX falls back to the session id (`AGENT_ORIGINAL_CALL_ID_FALLBACK=session_id`, `" + OPS + ":3026`).",
            ]}),
            ("Why it is built this way", "Pre-warmed processes (Silero VAD loaded, session object built) remove model-load time from the first second of the call. Drain timeout 1800 s and pod grace 1920 s let live calls finish during a rollout (`" + OPS + ":2968`)."),
            ("Risks", [
                "LiveKit server, SIP trunk and dispatch rules are not in git: nobody can review them from code.",
                "LiveKit API key/secret and the Redis password are plaintext in `" + OPS + ":3075-3078, 3182-3191`.",
            ]),
            ("Sources", [f"`{AG}/src/main.py:79-109, 320-371`", f"`{OPS}:2967-3173` (agent component)"]),
        ]},
    "v-session": {
        "title": "Session start and greeting", "title_plain": "Session + greeting", "status": "live",
        "chip": "aiva /chat/session · greeting by OpenAI gpt-6-luna", "chip_plain": "greeting: gpt-6-luna (external)",
        "summary": "Before the employee hears anything, the agent asks aiva to create a session for this phone number. aiva writes a greeting, which is spoken through TTS.",
        "facts": [("Endpoint", "`POST chatbot-ex-iva-chatbot:8000/api/v1/chat/session {phone}`"),
                  ("Greeting model", "OpenAI `gpt-6-luna` via egress relay (external SaaS)"),
                  ("Timeouts", "8 s read × up to 4 attempts, blocking"), ("Interruptible", "yes")],
        "sections": [
            ("Logic", {"ol": [
                "In the agent constructor `instructions=session_id` triggers a **synchronous** HTTP call to aiva `/chat/session` (`agents/agentlib.py:63-93`).",
                "aiva gets or creates the `ChatbotUser` by phone, opens a `Session`, and its GreetingAgent writes a greeting from the user's long-term memory (`aiva/chat/views/session.py:43-81`). See [B2 Greeting agent](b-greeting.html).",
                "The agent starts the LiveKit session, waits `AGENT_SIP_RTP_STABILIZATION_DELAY=0.4 s` for the audio path to settle, then `session.say(greeting, allow_interruptions=True)` (`entrypoint.py:68-90`).",
                "The thinking sound (`OFFICE_AMBIENCE`, volume 0.5) is armed; ambient background is off (`" + OPS + ":3028-3037`).",
            ]}),
            ("If it fails", {"note": "If `/chat/session` fails the session id becomes `unknown` and the agent speaks `AGENT_GREETING_MESSAGE`, whose code default is the **MCI greeting** (“سلام، من دستیار هوشمند همراه اول هستم…”). EX does not override it (`config.py:410-413`). An EX caller would hear the MCI assistant.", "kind": "bad"}),
            ("Why OpenAI for the greeting", "The greeting is the only text-generation step in EX that leaves the cluster. The Gemma 26B URL is commented out (`" + OPS + ":2511-2523`). The commit does not say why (likely greeting quality or latency, inferred)."),
            ("Sources", [f"`{AG}/src/agents/agentlib.py:63-93`", f"`{AG}/src/entrypoint.py:68-94`", f"`{OPS}:2510-2523, 3022-3037, 3128-3129`"]),
        ]},
    "v-vad": {
        "title": "Voice activity detection (Silero)", "title_plain": "VAD (Silero)", "status": "live",
        "chip": "Silero VAD · ~0.001B params · CPU", "chip_plain": "Silero VAD ~1M params",
        "summary": "A tiny neural model decides, every few milliseconds, whether the employee is speaking. It drives end-of-speech, barge-in and the silence timer.",
        "facts": [("Model", "Silero VAD (`livekit-plugins-silero==1.2.8`)"), ("Size", "≈1M params ≈ 0.001 B, ~2 MB ONNX, CPU"),
                  ("Threshold", "0.3 (default 0.5)"), ("Min speech / silence", "0.2 s / 0.5 s")],
        "sections": [
            ("Settings in EX", {"table": [["Setting", "EX", "Code default", "Ref"],
                ["`AGENT_VAD_ACTIVATION_THRESHOLD`", "**0.3**", "0.5", "`" + OPS + ":3107`"],
                ["`AGENT_VAD_MIN_SPEECH_DURATION`", "**0.2 s**", "0.5", "`" + OPS + ":3111`"],
                ["`AGENT_VAD_MIN_SILENCE_DURATION`", "**0.5 s**", "1.0", "`" + OPS + ":3099`"],
                ["`AGENT_VAD_PREFIX_PADDING_DURATION`", "**0.5 s**", "2", "`" + OPS + ":3109`"]]}),
            ("Why this model and these numbers", "Silero is the standard VAD for LiveKit: tiny, CPU-only, and fast enough to run per audio frame inside each call process. EX is tuned to be **sensitive**: a low threshold and 0.2 s minimum catch short Persian replies like «بله». The cost is more false triggers from line noise, and more barge-ins on noise (inferred). The installed noise-cancellation plugin is not used (`requirements.txt:67`)."),
            ("Inputs / outputs", "Input: caller PCM frames. Output: speech-start / speech-end events consumed by STT segmentation, the turn detector, barge-in and the user-away timer."),
            ("Sources", [f"`{AG}/src/main.py:88-98, 157-195`", f"`{AG}/src/config.py:63-67`"]),
        ]},
    "v-stt": {
        "title": "Speech-to-text (Soniox, cloud)", "title_plain": "STT (Soniox cloud)", "status": "external",
        "chip": "Soniox real-time · Persian strict · external SaaS", "chip_plain": "Soniox STT (external)",
        "summary": "The employee's audio streams to Soniox, a cloud speech-recognition service, which returns Persian text as the person speaks.",
        "facts": [("Model", "Soniox real-time; model id not pinned (plugin default). Sister deployment aiva-neda pins `stt-rt-v5`"),
                  ("Size", "proprietary, not published"), ("Language", "`fa`, strict"),
                  ("Path", "via egress proxy `envoy-relay-chatbot`"), ("Retries", "3 × 10 s timeout")],
        "sections": [
            ("Logic", [
                "`AGENT_STT_CLIENT=soniox` selects `LoggedSonioxSTT`; the key is secret `aiva/soniox_api_key`; traffic goes through `AGENT_STT_PROXY` (`" + OPS + ":3117-3125`, `chatbotlib.py:284-296`).",
                "Soniox is a streaming recogniser, so frames go straight to it without a VAD stream adapter (`agentlib.py:299-311`). Interim and final transcripts arrive while the person is still talking.",
                "Language hints `[\"fa\"]`, strict (`config.py:378-387`).",
                "After 3 failed retries an STT error is counted; after `AGENT_MAX_UNRECOVERABLE_ERRORS=3` the session closes (inferred from LiveKit semantics).",
            ]),
            ("Why Soniox", "Higher Persian streaming accuracy and lower latency than the in-house ASR are the likely reasons (inferred; no decision record in code). The in-house k2 ASR is still used after the call for analytics (see [A3](a-asr.html))."),
            ("Watch out", ({"note": "**Branch drift:** Soniox support exists only in the deployed image `3524df3f` from branch `feat-soniox-lang`, which is **not merged into main**. Rebuilding the agent from main would silently send STT to an empty OpenAI URL (main: `src/agents/agentlib.py:354`).", "kind": "bad"},
                           {"note": "**Privacy:** employee voice leaves the cluster to a SaaS vendor, and every Soniox response is logged at INFO (`utils/soniox_stt.py:22-36`), so transcripts land in `/app/access.log`.", "kind": "warn"})),
            ("Sources", [f"`{AG}/src/utils/soniox_stt.py`", f"`{AG}/src/agents/chatbotlib.py:284-296`", f"`{OPS}:3117-3125`"]),
        ]},
    "v-turn": {
        "title": "End-of-turn detection (LLM)", "title_plain": "End-of-turn LLM", "status": "live",
        "chip": "Gemma-4 26B-A4B · 26B total / ~4B active", "chip_plain": "Gemma-4 26B-A4B",
        "summary": "When the employee pauses, a language model reads the last few turns and estimates the probability that they have finished speaking, so the agent neither interrupts nor waits too long.",
        "facts": [("Model", "`google/gemma-4-26B-A4B-it` at `gemma4-26b-llm-lb`"), ("Size", "26B total, ~4B active per token (MoE)"),
                  ("Input", "last 6 messages + latest user text"), ("Output", "one float 0.0–1.0"),
                  ("Timeout", "8 s read, 3 retries; on error returns 1.0 = finished")],
        "sections": [
            ("Logic", {"ol": [
                "VAD reports 0.5 s of silence.",
                "LiveKit calls `OpenAICompatibleModel` (`AGENT_TURN_MODEL=openai`, `" + OPS + ":3067-3072`).",
                "System prompt: “end-of-turn detector… respond with a single float 0.0-1.0” (`config.py:114-123`). User message: `Chat history:` + `latest user input:` built from the last `AGENT_MAX_HISTORY_TURNS=6` messages (`openai_turn_detector.py:84-86, 172-205`).",
                "The reply is parsed as `float(content)`. Below `AGENT_UNLIKELY_THRESHOLD=0.5` the turn is treated as unfinished and the agent waits longer (see [V6](v-endpoint.html)).",
                "**Fail-safe:** any HTTP error, timeout or unparsable reply returns 1.0, meaning “turn finished” (`openai_turn_detector.py:88-92`).",
            ]}),
            ("Why a 26B MoE for a yes/no question", "Persian end-of-turn needs language understanding (a trailing «که…» means more is coming). The A4B MoE gives near-large-model understanding at roughly 4B-model decode cost, and the reply is one token, so it is cheap (inferred). An older dedicated Persian turn model (`mci_turn_detector.py`) exists but is unused in EX."),
            ("Risks", ["It shares the `gemma4-26b-llm-lb` pool with 10 other services; under load the 8 s timeout and retries can stall a turn, and the fail-safe then cuts in.",
                       "The `timeout` argument LiveKit passes is ignored (`openai_turn_detector.py:82`)."]),
            ("Sources", [f"`{AG}/src/utils/openai_turn_detector.py`", f"`{OPS}:3067-3072, 3020-3021`", "`chatbot-ops/prod/gemma4-26b/values.yaml:87-108`"]),
        ]},
    "v-endpoint": {
        "title": "Endpointing delay", "title_plain": "Endpointing", "status": "live",
        "chip": "dynamic 0.1–0.5 s (default was 0.5–3 s)", "chip_plain": "dynamic 0.1–0.5 s",
        "summary": "After the turn model answers, LiveKit waits a short, adaptive delay before committing the employee's turn and calling the brain.",
        "facts": [("Mode", "`dynamic`, alpha 0.99"), ("Min / max delay", "0.1 s / 0.5 s"), ("Code defaults", "fixed, 0.5 / 3.0 s")],
        "sections": [
            ("Logic", "`EndpointingOptions(mode=dynamic, min_delay=0.1, max_delay=0.5, alpha=0.99)` (`main.py:159-166`, `" + OPS + ":3091-3106`). If the turn model says “finished” the wait is near `min_delay`; otherwise near `max_delay`. Dynamic mode adapts inside the range from observed pause statistics (inferred from LiveKit semantics)."),
            ("Latency budget (voice layer only)", {"table": [["Segment", "Value"],
                ["VAD end-of-speech", "0.5 s silence"], ["End-of-turn LLM", "typically sub-second (inferred); up to 8 s × retries"],
                ["Endpointing", "0.1–0.5 s"], ["aiva first token + first sentence", "brain lane"],
                ["TTS first audio", "one full sentence synthesised"], ["Voice-layer total", "≈ 0.7–1.5 s before aiva and TTS (inferred)"]]}),
            ("Why so tight", "EX is about 5× tighter than the defaults to feel conversational. The risk is cutting off employees who pause mid-sentence, which matters for emotional feedback calls (inferred)."),
        ]},
    "v-aiva": {
        "title": "Send the turn to the brain", "title_plain": "Call aiva", "status": "live",
        "chip": "POST /chat/completions (streamed)", "chip_plain": "→ aiva /chat/completions",
        "summary": "The committed text is sent to aiva as an OpenAI-style streamed chat request. The voice agent does not choose the model; aiva does.",
        "facts": [("Endpoint", "`chatbot-ex-iva-chatbot:8000/api/v1/chat/completions`"), ("Extra", "`extra_body.session_id`"),
                  ("Timeout", "10 s, 3 retries"), ("Model sent", "none (aiva decides)")],
        "sections": [
            ("Logic", [
                "`livekit_openai.LLM(client=AsyncClient(base_url=AGENT_LLM_BASE_URL))` with `extra_body={session_id}` (`agentlib.py:326-344`, `" + OPS + ":3126-3127`).",
                "aiva also recovers the session from the system message, which is the session id (`aiva/chat/views/completion.py:72-81`).",
                "While waiting, the thinking sound plays. `VOICE_BRIDGE_ENABLED=false`, so no filler sentence is generated (`" + OPS + ":2533`).",
                "Silence reminders reuse the same endpoint with `extra_body.signal=\"instruct\"` (`agentlib.py:506-531`).",
                "aiva returns HTTP 204 when the last history item is a tool output with nothing to say (`completion.py:103-108`).",
                "`AGENT_RECORD_LLM_REQUEST_TIMES=True` stores each request time for the Kafka summary (`" + OPS + ":3018`).",
            ]),
            ("Continue", "What happens inside aiva: [lane 2, the brain](../index.html#lane-brain)."),
        ]},
    "v-tts": {
        "title": "Text-to-speech (neurobox ex_prod)", "title_plain": "TTS (neurobox ex_prod)", "status": "unknown",
        "chip": "neurobox-gateway-green · model ex_prod · speed 1.1", "chip_plain": "TTS ex_prod (Triton)",
        "summary": "The streamed answer is split into sentences, and each sentence is synthesised to audio by the in-house neurobox TTS gateway.",
        "facts": [("Endpoint", "`neurobox-gateway-green.neurobox-prod:8080/v1/audio/speech`"), ("Model name", "`ex_prod`; backing voice unknown"),
                  ("Size", "unknown; if VITS ≈ 0.03–0.04 B (inferred)"), ("Speed", "1.1"), ("Timeouts", "connect 10 s, read 30 s, 3 retries; 204 not retried")],
        "sections": [
            ("Logic", {"ol": [
                "Markdown and emoji are stripped (`chatbotlib.py:377-378`).",
                "A `SentenceTokenizer` splits the stream **only on `\". \"`** (`config.py:173-176`). Persian `؟`, `!` and `،` are not separators, so a long question is synthesised as one chunk.",
                "Each chunk → `POST /v1/audio/speech` (`tts.py:54-117`). neurobox returns 204 for text with nothing speakable, which is not retried.",
                "neurobox is an OpenAI-style façade over Triton gRPC; its cache keys are text + speed + format, TTL 24 h (`golang/neurobox-gateway/internal/api/tts.go:187-190`).",
            ]}),
            ("Unknown", {"note": "In main's neurobox-gateway the Triton model is fixed by gateway config and the request `model` is used only for metrics (`internal/services/tts.go:24, 61-84`). Which voice `ex_prod` maps to on the `green` gateway cannot be verified from our repos.", "kind": "warn"}),
            ("Sources", [f"`{AG}/src/utils/tts.py`", f"`{OPS}:3130-3135`"]),
        ]},
    "v-bargein": {
        "title": "Barge-in (interruptions)", "title_plain": "Barge-in", "status": "live",
        "chip": "VAD-based · 0.4 s of caller speech", "chip_plain": "barge-in 0.4 s",
        "summary": "If the employee starts talking while the agent speaks, playback stops so the employee can be heard.",
        "facts": [("Mode", "VAD"), ("Min duration", "0.4 s"), ("Greeting interruptible", "yes"), ("Exit message interruptible", "no")],
        "sections": [
            ("Logic", "`InterruptionOptions(enabled=True, mode=\"vad\", min_duration=0.4, min_words=0)` (`main.py:167-172`, `" + OPS + ":3113`). Interrupted assistant messages are marked `interrupted=true` in history and in the Kafka summary (`entrypoint.py:319`)."),
            ("Risk", "With VAD threshold 0.3, background noise of 0.4 s or more can cut the agent off (inferred)."),
        ]},
    "v-silence": {
        "title": "Silence and noise handling", "title_plain": "Silence handling", "status": "live",
        "chip": "user-away reminders on · non-speech off", "chip_plain": "user-away on",
        "summary": "If both sides are silent for 10 s the agent asks whether the employee is still there; after three tries it says goodbye and hangs up.",
        "facts": [("User-away", "enabled, 10 s, 3 reminders"), ("Non-speech prompts", "disabled"), ("Worst case", "≈45–50 s of silence before hang-up (inferred)")],
        "sections": [
            ("Logic", {"ol": [
                "After `AGENT_USER_AWAY_TIMEOUT=10 s` of mutual silence LiveKit marks the user away (`agent_session.py:36-52`).",
                "The agent sends an instruction signal to aiva («من هستم اگه کاری داشتی») and speaks the reply (`agentlib.py:456-499`).",
                "Repeated up to 3 times; then the exit line («متاسفانه پاسخی دریافت نشد و تماس قطع می‌شود، خداحافظ») is played and the room is deleted.",
                "Any user speech cancels the loop.",
            ]}),
            ("Gap", "The reminder texts are generic code defaults, not reviewed for HR tone (`config.py:439-446`)."),
        ]},
    "v-end": {
        "title": "Call end and human transfer", "title_plain": "Call end / transfer", "status": "live",
        "chip": "exit tool · hang-up · transfer broken", "chip_plain": "exit / transfer",
        "summary": "A call ends when aiva calls the `exit` tool, the silence loop gives up, or the employee hangs up. Transfer to a human is wired in code but not configured for EX.",
        "facts": [("Ways to end", "`exit` tool, user-away exit, hang-up, redirect"), ("Transfer target", "SIP MESSAGE to `6040` via sip-messager"),
                  ("Transfer in EX", "always fails: `AGENT_SIP_REDIRECT_URL` unset")],
        "sections": [
            ("Logic", ["`exit`: wait for playout, then `delete_room()` (`chatbotlib.py:405-411`).",
                       "`redirect_to_human_agent`: builds a SIP MESSAGE from Via / Call-ID / X-channelId and POSTs it to `http://{AGENT_SIP_REDIRECT_URL}/api/v1/send-sip-message` (`agentlib.py:201-286`).",
                       "After any ending, the shutdown callback `_log_summary` publishes the summary ([V13](v-summary.html))."]),
            ("Broken in EX", {"note": "EX has no `AGENT_SIP_REDIRECT_URL`, so the URL becomes `http:///api/v1/send-sip-message`. Any transfer says «متاسفانه امکان انتقال به کارشناس انسانی وجود ندارد», records `redirect_status=failed`, and **drops the call** either way. Decide whether human hand-off is in scope for the pilot.", "kind": "bad"}),
        ]},
    "v-record": {
        "title": "Call recording", "title_plain": "Recording", "status": "live",
        "chip": "LiveKit egress → MinIO .ogg (shared MCI bucket)", "chip_plain": "egress → MinIO .ogg",
        "summary": "Two separate audio tracks, the employee's and the agent's, are recorded to object storage for later analysis.",
        "facts": [("Recorder", "`livekit/egress:v1.8.4`, 3 replicas"), ("Path", "`s3://chatbot-mci-iva/chatbot-ex-iva-prod/<track_id>.ogg`"),
                  ("Room recording", "off (track recordings only)")],
        "sections": [
            ("Logic", ["Egress starts after the greeting is queued; it looks up track ids 10 × 1 s, then starts one TrackEgress per track (`entrypoint.py:92-94, 160-180`, `egress_recorder.py:112-190`).",
                       "The bucket is the default `chatbot-mci-iva`, **shared with MCI IVA**, separated only by the prefix `chatbot-ex-iva-prod` (`config.py:163-167`).",
                       "The start of the greeting may be missing from the agent track (inferred)."]),
            ("Questions for HR", "Retention and access policy for employee recordings in a shared bucket are not defined in code."),
        ]},
    "v-summary": {
        "title": "Call summary to Kafka", "title_plain": "Summary → Kafka", "status": "live",
        "chip": "topic chatbot-mci-ex-iva → analytics", "chip_plain": "Kafka chatbot-mci-ex-iva",
        "summary": "When the call ends, the agent publishes a summary of the session to Kafka. Post-call analytics (lane 5) consumes it.",
        "facts": [("Topic", "`chatbot-mci-ex-iva`"), ("Messages per call", "session + one per message + aggregated"),
                  ("Consumer", "`grogu-ex-iva` only (no memory writer in EX)")],
        "sections": [
            ("Payload", "Phone, session id, call ids, city code, timings and duration, exit / redirect flags, track paths and statuses, token counts, STT audio seconds, TTS characters, `llm_request_times_seconds` (`schema.py:42-178`, `entrypoint.py:220-290`)."),
            ("Quirks", ["`llm_model` is hard-coded `\"unknown\"`; `stt_url` and `turn_url` are empty for EX (`entrypoint.py:265-272`).",
                        "Errors are logged and counted, never re-queued (`kafka.py:139-156`)."]),
            ("Continue", "[A1 grogu ingest](a-ingest.html)."),
        ]},

    # ------------------------------------------------------------------ lane 3: knowledge
    "k-author": {
        "title": "Authoring the knowledge base", "title_plain": "KB authoring", "status": "live",
        "chip": "admins add Q&A via API or CSV/JSON import", "chip_plain": "Q&A CRUD / import",
        "summary": "The KB is a hand-curated list of questions and approved answers, not uploaded documents. There is no PDF parsing or chunking.",
        "facts": [("API", "`/api/v1/kb/*` → `chatbot-ex-iva-kb:8000`"), ("Database", "Postgres `chatbot_ex_iva_kb`"),
                  ("Unit", "one answer + many paraphrase questions"), ("Answer types", "knowledge · incident · instruction")],
        "sections": [
            ("Data model", {"table": [["Table", "Holds", "Ref"],
                ["`question_answer`", "active flag, start/end time window, tags, created_by / updated_by", "`adcs_kb/knowledgebase/models/qa.py:20-60`"],
                ["`questions`", "paraphrase text (≤3000 chars), `as_suggestion`", "`models/question.py:18-29`"],
                ["`answers`", "`text`, `iva_text` (voice version), `type`", "`models/answer.py:18-34`"],
                ["`guardrails`", "example questions + allow/deny + reason", "`models/guardrail.py:18-24`"]]}),
            ("How content gets in", ["CRUD endpoints `/kb/qa`, `/kb/answer`, `/kb/question`, `/kb/tag`, `/kb/guardrail` with JWT permissions `adcs_kb.*_qa` (`knowledgebase/permissions.py:4-16`).",
                                     "Bulk `/kb/import`: CSV columns `questions` (`|`-separated), `answer_text`, `answer_iva_text`, `answer_type`, window, tags. Bad rows are skipped and reported; good rows commit in one transaction (`views/import_qa.py:36-155`)."]),
            ("Why Q&A and not documents", "Exact, approved wording is what the EX PRD asks for (answer only from approved content). The cost: coverage depends on admins writing enough paraphrases, because only the questions are embedded ([K4](k-embed.html))."),
        ]},
    "k-summarize": {
        "title": "Speakable-summary helper", "title_plain": "Summarize helper", "status": "live",
        "chip": "Gemma-4 31B · admin tool, human in the loop", "chip_plain": "Gemma-4 31B",
        "summary": "An optional admin tool: paste a long answer and get back a short version that sounds natural when spoken. Nothing is saved automatically.",
        "facts": [("Endpoint", "`/kb/summarize` (SSE)"), ("Model", "`google/gemma-4-31B-it` (31B dense)"),
                  ("Skip rule", "text ≤256 chars returned unchanged"), ("Code default model", "Qwen3.5-35B-A3B (overridden)")],
        "sections": [
            ("Why the 31B", "Quality of Persian rewriting matters more than speed for an offline admin tool, so the largest in-house model is used (inferred)."),
            ("Sources", ["`adcs_kb/knowledgebase/handlers/summarize/`", "`" + OPS + ":979-981`"]),
        ]},
    "k-sync": {
        "title": "Sync to the vector store (every 60 s)", "title_plain": "Sync every 60 s", "status": "live",
        "chip": "Celery beat · incremental by timestamp + hash", "chip_plain": "Celery sync 60 s",
        "summary": "A background job checks for new or edited Q&A every minute and indexes it. There is no publish button: an edit is live within about a minute.",
        "facts": [("Job", "`aiva_sync_qdrant_task`, interval 60 s (default 300)"), ("Worker", "`iva_kb_worker`, concurrency 1"),
                  ("Broker", "Redis `chatbot-ex-redis` db 1"), ("Re-index", "`scripts/run_kb_sync.sh`")],
        "sections": [
            ("Logic", {"ol": [
                "Select answers that are stale (`qdrant_last_sync < updated_at`, never synced, or flagged) **and** eligible (active and inside the time window) (`models/answer.py:52-60`).",
                "Gather each answer's valid questions; an answer with 0 questions is soft-deleted and its vector removed (`handlers/qdrant/sync.py:100-120`).",
                "Skip re-embedding when the SHA-256 of the payload is unchanged.",
                "Embed ([K4](k-embed.html)) and upsert ([K5](k-collections.html)); mark rows synced.",
                "Guardrails and suggestions are synced the same way into their own collections.",
            ]}),
            ("Failure", "A Qdrant or embedding error is logged and the rows stay unsynced, so the next tick retries. Old vectors stay live meanwhile. Changing the embedding model needs a manual full re-embed, because the hash does not include the model id (inferred)."),
        ]},
    "k-embed": {
        "title": "Embedding the questions", "title_plain": "Embed questions", "status": "live",
        "chip": "hakim-unsup · ~0.12B · 768-d", "chip_plain": "hakim-unsup embeddings",
        "summary": "Each paraphrase question is turned into a 768-number vector by an in-house Persian embedding model. The answer text itself is not embedded.",
        "facts": [("Model", "`hakim-unsup` (MCI in-house Hakim, unsupervised variant)"), ("Size", "≈0.12 B, BERT-base class (public Hakim paper; unverified)"),
                  ("Serving", "vLLM pooling, `hakim-unsupervised-vllm-proxy:1080/v1`, max-model-len 512"), ("Vector", "768-d, cosine, multivector per answer")],
        "sections": [
            ("Logic", "`get_multiple_embeddings(questions_only=True)` embeds each question separately and stacks the vectors into an N×768 multivector for the answer (`aiva_kb/handlers/embedding.py:26-65`; commit `4582c44b4` “ensure only questions are used”)."),
            ("Why questions only", "An employee's spoken question is closest to other questions, not to a long answer. Embedding only paraphrases makes matching question-to-question, which is more precise (inferred)."),
            ("Why Hakim", "A small Persian-specific encoder is cheap enough for CPU or a small GPU slice and is tuned for Persian, unlike generic multilingual models (inferred)."),
            ("Check", "Collections are created at 768 dims by default (`QDRANT_VECTOR_SIZE` not set). If hakim-unsup ever returned another size, upserts would fail every tick and only be logged."),
        ]},
    "k-collections": {
        "title": "Vector collections (Qdrant)", "title_plain": "Qdrant collections", "status": "live",
        "chip": "6 collections · shared Qdrant cluster", "chip_plain": "Qdrant collections",
        "summary": "Indexed knowledge is stored in Qdrant collections on a cluster shared with other products.",
        "facts": [("Cluster", "`qdrant-lb.chatbot-prod` (shared)"), ("Type", "multivector MAX_SIM, cosine")],
        "sections": [
            ("Collections", {"table": [["Collection", "Content", "Read by the voice agent?"],
                ["`chatbot-ex-aiva-contexts`", "questions → `answer.text`", "**yes** ([K6](k-search.html))"],
                ["`chatbot-ex-aiva-iva-contexts`", "questions → `answer.iva_text` (voice version)", "**no**: synced but never read"],
                ["`chatbot-ex-aiva-instructions`", "created, but **nothing writes to it**", "searched, always empty (inferred)"],
                ["`chatbot-ex-aiva-guardrails`", "guardrail example questions + allow/deny", "yes (guardrail)"],
                ["`chatbot-ex-aiva-suggestions`", "suggestion questions + markdown answer (Gemma-4 31B rewrite)", "no (text UI)"],
                ["`aiva-classification`", "**not EX-namespaced**: `CLASSIFYING_COLLECTION_NAME` unset", "yes (classifier)"]]}),
            ("Product question", "The voice-optimised `iva_text` is written but never used; the agent reads the text-chat answer. Is that intended for a voice product?"),
        ]},
    "k-search": {
        "title": "Search at answer time", "title_plain": "Query + search", "status": "live",
        "chip": "embed current utterance · top-10 · threshold 0.25", "chip_plain": "top-10 @ 0.25",
        "summary": "On every turn, only the employee's latest utterance is embedded and compared with the stored questions. Up to 10 matches above a low similarity bar are kept.",
        "facts": [("Query", "current utterance only; no rewriting, no history"), ("Top-k", "10"),
                  ("Threshold", "cosine 0.25 (code default 0.5)"), ("Filters", "none (no tag / department filter)")],
        "sections": [
            ("Logic", {"ol": [
                "`UserInputEvent` → `EmbeddingEvent` with `recent_item_only=True` (`agentlib@0.45.0:agentlib/events/embedding.py:18`).",
                "`AIVARetrieveEvent` fans out in parallel to contexts, instructions, guardrails, tools and classification retrievers (`aiva/chat/handlers/orchestrator.py:197-205`).",
                "Contexts: `LLMFilteredAdcsQdrantRetriever` on `chatbot-ex-aiva-contexts`, top-10, threshold 0.25. For each hit only the best-matching question text is kept (`aiva/retrieve/qdrant.py:47-82`).",
            ]}),
            ("Why a low threshold", "A permissive 0.25 favours recall: better to over-fetch and let the LLM filter ([K7](k-filter.html)) remove noise. The trade-off is that precision rests on the smallest model in the stack (inferred)."),
            ("Weak spot", "Follow-ups like «اون یکی چی؟» carry little meaning alone. Without query rewriting, grounding for follow-ups depends on carry-over ([K8](k-carry.html))."),
        ]},
    "k-filter": {
        "title": "Relevance filter (LLM)", "title_plain": "Contexts filter LLM", "status": "live",
        "chip": "Gemma-4 E2B · ~2B effective · fails open", "chip_plain": "Gemma-4 E2B filter",
        "summary": "A small, fast language model reads the conversation and the retrieved Q&A and picks which items are actually relevant. Only those reach the answer agent.",
        "facts": [("Model", "`google/gemma-4-E2B-it` at `gemma-4-e2b-llm-lb`"), ("Size", "~2B effective (~5B with embeddings)"),
                  ("Prompt", "`ex_iva_contexts_filter_llm_template` (Phoenix, tag production)"), ("History", "last 16 messages"),
                  ("Max output", "4096 tokens; temperature = server default"), ("Output", "`{\"indexes\":[…]}`")],
        "sections": [
            ("Logic", {"ol": [
                "Input JSON: `{current_user_input, history[≤15], retrieved_candidates[]}` (the last 16 items, with the current input moved out). Candidates are this turn's hits **plus last turn's selected contexts** (`aiva/retrieve/qdrant.py:216-246`).",
                "The model returns the indexes to keep.",
                "Kept current hits + kept previous contexts go to the answer agent.",
                "An empty search with no previous contexts skips the call.",
            ]}),
            ("Why E2B", "Picking relevant items from a short list is an easy classification task, and it runs on every turn of a live call. The smallest Gemma keeps latency and GPU cost low (inferred)."),
            ("Fail-open", {"note": "On an exception, non-JSON reply, duplicate or out-of-range index, all Qdrant candidates pass **unfiltered** and previous contexts are dropped (`qdrant.py:208-269`). Combined with threshold 0.25, “answer only from the KB” is enforced by the prompt alone; there is no code-level “no context → refuse” gate.", "kind": "warn"}),
            ("Instructions filter", "A second filter (`ex_iva_instructions_filter_llm_template`) is configured but disabled (`INSTRUCTIONS_FILTER_LLM_ENABLED` unset); its code default model is `openai/gpt-oss-120b`."),
        ]},
    "k-carry": {
        "title": "Hand-off and carry-over", "title_plain": "Inject + carry-over", "status": "live",
        "chip": "contexts → ReAct user prompt · saved for next turn", "chip_plain": "carry-over",
        "summary": "The selected Q&A is written into the answer agent's prompt, and saved on the session so the next turn can reuse it for follow-up questions.",
        "facts": [("Prompt slot", "`{contexts}` in `ex_iva_react_agent_llm_user_template`"), ("Format", "`Question:…\\nAnswer:…` or `Instructions:…`"),
                  ("Saved to", "`session.params.latest_contexts`")],
        "sections": [
            ("Logic", ["`RetrievedContextsEvent` → orchestrator waits for contexts, instructions and tools → `ReActChatEvent` (`orchestrator.py:207-309`).",
                       "Contexts are rendered in `aiva/agents/react/prompt.py:85-104` and recorded on the trace span `retrieval.contexts`.",
                       "After streaming, the filtered contexts are saved in a background task (`session_params_persistence.py:38-100`) and offered again to next turn's filter."]),
            ("Continue", "[The answer agent](b-react.html)."),
        ]},

    # ------------------------------------------------------------------ lane 4: memory
    "m-history": {
        "title": "In-call history", "title_plain": "In-call history", "status": "live",
        "chip": "full transcript resent each turn · cap 50", "chip_plain": "history ≤50",
        "summary": "Within one call, every request carries the whole conversation so far. aiva keeps the last 50 items for the agent and the last 16 for the relevance filter.",
        "facts": [("Limit", "`CHAT_HISTORY_LIMIT=50`"), ("Filter history", "16"), ("Also kept", "tool results replayed (`tool_call_results`)")],
        "sections": [("Sources", ["`aiva/chat/config.py:64`", "`aiva/chat/views/completion.py:83-89`"])]},
    "m-longterm": {
        "title": "Long-term memory (read side)", "title_plain": "Memory read", "status": "live",
        "chip": "chatbot_users.memory ≤1024 chars · likely empty", "chip_plain": "memory read",
        "summary": "Each employee (keyed by phone number) has a memory field that is injected into the greeting, classifier, clarifier and answer prompts. In EX nothing writes it, so prompts receive the literal text `{}`.",
        "facts": [("Field", "`chatbot_users.memory` (JSON, default `{}`)"), ("Read by", "greeting, classifying, clarifying, ReAct"), ("Written by", "nothing in EX")],
        "sections": [("Product question", {"note": "Should an anonymous-feedback product build per-employee memory at all? Today the read path is live and the write path is absent, so behaviour could change silently if the writer is deployed.", "kind": "warn"})]},
    "m-writer": {
        "title": "Memory writer (summariser)", "title_plain": "Memory writer", "status": "notdeployed",
        "chip": "Kafka consumer · not deployed in EX", "chip_plain": "not deployed",
        "summary": "Code exists that reads finished calls from Kafka and summarises them into the employee's memory. EX does not deploy it.",
        "facts": [("Command", "`aiva_consume_kafka`"), ("Prompt", "`aiva_summarize_agent_llm_template`"), ("Would use", "adcs `AGENT_LLM_*` → Gemma-4 31B at `172.23.0.17:8318` (inferred)")],
        "sections": [
            ("What it would do", "Consume `aggregated` call events, merge previous memory with the new transcript, and overwrite `ChatbotUser.memory` with “user goals, constraints, decisions, key facts… always include the name” (`aiva/memory/management/commands/aiva_consume_kafka.py`, `aiva/prompts/memory.py`). No TTL or purge exists."),
            ("Open item", "EX `iva-chatbot` sets no `KAFKA_BOOTSTRAP_SERVERS`, yet `MemorySettings` requires it at import (`aiva/memory/config.py:15`). Confirm with `kubectl exec env`; either the image ships a `.env` or the reading is wrong."),
        ]},
    "m-stores": {
        "title": "Where employee data is stored", "title_plain": "Data stores", "status": "live",
        "chip": "Postgres · Phoenix traces · logs · MinIO", "chip_plain": "data stores",
        "summary": "A privacy map of every place employee speech, identity or derived data ends up.",
        "sections": [
            ("Map", {"table": [["Store", "What", "Employee data?"],
                ["Postgres `chatbot_ex_iva_v2`", "`chatbot_users` (phone, memory), `sessions`, `messages` (every utterance and reply), votes", "**yes**, no retention job"],
                ["Phoenix traces `chatbot-ex-iva`", "phone, memory, input text, retrieved contexts; 100% sampled; 30-day retention", "**yes**"],
                ["App logs (fluentd)", "phone + memory every turn; Soniox transcripts at INFO; embedding query at DEBUG", "**yes**"],
                ["MinIO `chatbot-mci-iva`", "call recordings (shared MCI bucket)", "**yes**"],
                ["MinIO `coa-analysis-prod/ex/prod/voices`", "merged stereo WAV for analytics", "**yes**"],
                ["Postgres `coa_ex` + ClickHouse `ex_call_analytics_dist`", "call tags, summaries, sentiment", "**yes**"],
                ["Soniox (SaaS), OpenAI (greeting)", "live audio; memory / name for the greeting", "**leaves the cluster**"],
                ["Qdrant, KB Postgres", "approved Q&A only", "no"]]}),
            ("Needs sign-off", "Retention, purge and access policy for all **yes** rows; whether phone numbers should be pseudonymised in logs and traces."),
        ]},

    # ------------------------------------------------------------------ lane 5: analytics
    "a-ingest": {
        "title": "Ingest the finished call (grogu)", "title_plain": "grogu ingest", "status": "live",
        "chip": "grogu-ex-iva v0.33.1 · SOURCE_PLATFORM=iva", "chip_plain": "grogu ingest",
        "summary": "A Go service reads each call summary from Kafka, records the call as queued, and starts processing it.",
        "facts": [("Consumes", "`chatbot-mci-ex-iva`, group `anzu-coa-ex-iva-consumer`"), ("Pool", "10 workers"),
                  ("Delivery", "at-least-once: offset committed after the DB rows exist")],
        "sections": [
            ("Logic", {"ol": ["Parse; skip if `call_ai_tags` is already in_progress or succeed (`golang/grogu/internal/call/service.go:342-356`).",
                              "Write `calls.status=queued` and the first `call_ai_tags` row, then commit the Kafka offset (`worker.go:72-98`).",
                              "Set `in_progress` and process."]}),
            ("Note", "The summary already contains the live transcript, but grogu ignores it and re-transcribes the audio ([A3](a-asr.html)). That doubles ASR cost, and the analysed text can differ from what the bot heard."),
            ("Failure", "Any error → dead-letter table → retry worker every 5 min (EX), up to 10 retries (`deadletter/worker.go:43`, `internal/config/config.go:102`, `" + OPS + ":3391-3398`)."),
        ]},
    "a-merge": {
        "title": "Merge the two channels", "title_plain": "Channel merge", "status": "live",
        "chip": "ffmpeg · employee=ch1 (left), bot=ch2 (right)", "chip_plain": "ffmpeg merge",
        "summary": "The employee track and the agent track are combined into one stereo file, so later steps know who said what.",
        "facts": [("Tool", "ffmpeg"), ("Layout", "left = employee = `ch1`; right = bot = `ch2`"), ("Output", "`coa-analysis-prod/ex/prod/voices`")],
        "sections": [("Logic", "Download both `.ogg` tracks from `chatbot-mci-iva`, take the left channel of each, build stereo, upload the WAV (`internal/voice/merge.go:195-208`, `call/service.go:515-574, 894-975`). A `failed` track path drops the call.")]},
    "a-asr": {
        "title": "Offline speech recognition + emotion", "title_plain": "Offline ASR", "status": "external",
        "chip": "k2 ASR coa_iva_prod_long + emotion + gender", "chip_plain": "ASR coa_iva_prod_long",
        "summary": "The stereo file is transcribed again by the in-house ASR, with an emotion and gender label per segment.",
        "facts": [("Endpoint", "`asr-k2-tmp-gw-proxy.neurobox-prod/v1/audio/transcriptions`"), ("Model route", "`coa_iva_prod_long`"),
                  ("Extras", "emotion, gender"), ("Model / size", "not in our repos (k2/Zipformer family, inferred)"), ("Timeout", "30000 s; 3 retries; circuit breaker 12")],
        "sections": [
            ("Output", "`segments[]{start, end, text, channel, emotion, gender}` + overall emotion/gender (`internal/asr/service.go:22-37`)."),
            ("Validation", "No `ch1` segment means the employee was silent or the merge failed: the call is marked `invalid` and skipped (`service.go:1015-1029`). Overlap per channel is computed with a 1.0 s threshold."),
            ("Why re-transcribe", "Offline, full-file ASR with emotion and gender gives richer, consistent input for analytics than the live stream (inferred)."),
            ("Unknown", "grogu sends `include=emotion|gender`, but voice-segmenter expects `enable_emotion`; which service really backs `coa_iva_prod_long` is unverified."),
        ]},
    "a-publish": {
        "title": "Publish for analysis", "title_plain": "Publish", "status": "live",
        "chip": "Kafka anzu-coa-call-ex", "chip_plain": "Kafka anzu-coa-call-ex",
        "summary": "grogu publishes the segments, call info and overlap flags to the EX call topic for the analysis engine.",
        "facts": [("Topic", "`anzu-coa-call-ex`"), ("Payload", "`CallResultMessage{segments, metadata, call_info, overlap}`"), ("Account overview", "off for EX")],
        "sections": [("Call info", "`call_to=mcinext`, `platform=iva`, `service_no=phone`, `access_code=9990`, city code, start/end in Tehran time (`service.go:1051-1106`).")]},
    "a-cca": {
        "title": "AI analysis engine (CCA)", "title_plain": "CCA LLM analysis", "status": "external",
        "chip": "not in our repos · likely Gemma-4 COA pools", "chip_plain": "CCA (external)",
        "summary": "An LLM engine reads each call and produces sentiment, satisfaction, category, summary, suggestions and topics. Its code, prompts and model settings are not in the phoenix or chatbot-ops repos.",
        "facts": [("Code", "outside our repos (separate `coa-ops`, inferred)"), ("Likely models", "`gemma4-26b-coa` (26B MoE, 2 replicas) and/or `gemma4-31b-coa` (31B) — no client found"),
                  ("Prompts", "unknown"), ("Writes", "ClickHouse `zaal.ex_call_analytics_dist`")],
        "sections": [
            ("What it produces", "Inferred from the columns coa-api reads (`coa/apps/main/services/sync.py:354-417`): `user_sentiment` / `agent_sentiment`, bad words per side, agent greeting / farewell / referral, `user_satisfaction` + reason, `category_subcategory_dict`, `call_reason`, `call_summary`, `suggestions`, `info_category`, `topics`, `conversation_reform`."),
            ("HR gap", {"note": "There is no employee-feedback taxonomy and no sensitive/emergency classifier or alerting in code. The tags are call-centre tags, and “agent” etiquette tags now grade the bot. The EX chatbot prompt itself says post-call sensitive alerts are a backend job “not established as implemented” (`" + OPS + ":555-567`).", "kind": "bad"}),
            ("A reference prompt", "coa-api still carries a legacy evaluation prompt (`coa/config.py:407-583`) used by no code. It shows the field shape CCA follows: repair transcript → greeting → farewell → sentiment ANGRY/NORMAL with evidence → swearing → request summary + domain (SIM, package, signal, MyMCI)."),
            ("Ask", "Get the CCA repo: prompts, model, temperature, max tokens, batching, retries, and whether an HR category tree exists."),
        ]},
    "a-store": {
        "title": "Analytics storage", "title_plain": "Storage", "status": "live",
        "chip": "ClickHouse · Postgres coa_ex · MinIO · Redis", "chip_plain": "ClickHouse + Postgres",
        "summary": "Results land in ClickHouse; the panel reads a Postgres copy.",
        "sections": [("Stores", {"table": [["Store", "What"],
            ["ClickHouse `172.16.1.15:31390` `zaal.ex_call_analytics_dist`", "CCA output (Tehran time)"],
            ["Postgres `coa_ex` (shared `coa-prod-new` cluster)", "`calls`, `call_ai_tags`, human tags and logs"],
            ["MinIO `coa-analysis-prod/ex/prod/voices`", "merged audio"], ["Redis `coa-ex-redis`", "dashboard caches"]]})]},
    "a-sync": {
        "title": "Sync daemons", "title_plain": "Sync daemons", "status": "live",
        "chip": "6 loops copy ClickHouse → Postgres / Redis", "chip_plain": "6 sync loops",
        "summary": "Background loops copy analysis results into Postgres, apply category fixes, mark failures, load trends and pre-warm dashboards.",
        "sections": [
            ("Loops", {"table": [["Daemon", "Does", "Cadence"],
                ["`coa-ex-syncer`", "new ClickHouse rows → `calls` + `call_ai_tags`; emotion flags from segments", "batch 3000, every 5–60 s"],
                ["`coa-ex-ch-update-syncer`", "category edits by `updated_at`", "same"],
                ["`coa-ex-syncer-failed`", "HTTP-503 rows → status failed", "60–600 s"],
                ["`coa-ex-syncer-canonical`", "canonical category rules", "02:00–06:00 Tehran"],
                ["`coa-ex-trends-syncer`", "trend snapshot from MinIO; n8n alert webhook", "scheduled"],
                ["`coa-ex-dashboard-cache`", "pre-warm Redis dashboards", "every 30 min"]]}),
            ("EX falls back to MCI data", {"note": "The trends loop reads bucket `cca-mci` (default, not overridden), and failed calls read the default `unprocessed_calls_dist`. The EX panel may be showing **MCI call-centre trends** (inferred). Other CCA failures leave EX calls stuck `in_progress`.", "kind": "warn"}),
        ]},
    "a-api": {
        "title": "COA API", "title_plain": "coa-ex-api", "status": "live",
        "chip": "Django REST v5.22.0", "chip_plain": "coa-ex-api",
        "summary": "The REST API behind the EX panel: call lists, call detail, thematic analysis, dashboards, IVA metrics, trends and announcements.",
        "facts": [("Image", "`coa-api:v5.22.0` (= phoenix main after the 2026-11-02 pull; 5.22 adds DB-managed tag translations)"), ("LLM use", "only diacritisation for announcements (Gemma-4 31B via mcinext gateway)")],
        "sections": [("Endpoints", ["`/api/v1/analyse/calls/recordings`, `/analyse/voice/call/<id>`, `Thematic-analysis/*`, `special-analysis/*`, `dashboard/*`",
                                    "`/api/v1/iva/dashboard/{metrics, satisfaction-timeseries, time-buckets}`",
                                    "`/api/v1/iva/announcement/*` (TTS `coa-ex-prod` + diacritisation)", "`/api/v1/trends/*`, `/tickets/*`, `/management/*`"]),
                     ("Labels", "EX emotion tags: NORMAL عادی, COMPLAINING شاکی, ANGRY عصبانی, HAPPY خوشحال, SAD ناراحت, EXCITED هیجان‌زده, SWEAR الفاظ رکیک (`" + OPS + ":2686-2687`). Sentiment labels are inconsistent across code (`NORMAL`/`ANGRY`/`COMPLAINANT`/`COMPLAINING`).")]},
    "a-panel": {
        "title": "EX panel", "title_plain": "ex-agent-ui", "status": "external",
        "chip": "agent-ui v2.20.6 · source not in phoenix", "chip_plain": "EX panel",
        "summary": "The web panel HR users see: calls, playback, dashboards, thematic analysis, trends, KB and NL2SQL. Its source code is in another repo.",
        "facts": [("Image", "`agent-ui:v2.20.6`"), ("Host", "`ex-agent-new.pr.mci.dev` via `ex-agent-gateway`"), ("Date range", "7 days max per view")],
        "sections": [("Routes behind the panel", ["auth → `chatbot-ex-auth`", "calls, dashboards, IVA metrics, trends → `coa-ex-api`", "`/api/v1/kb` → KB", "`/aqa/` → NL2SQL", "`/api/v1/canonicals` → `ex-cca-mapper` (external)", "`/api/v1/voice-call` → websocall"])]},
    "a-aqa": {
        "title": "Ask-your-data (NL2SQL)", "title_plain": "AQA NL2SQL", "status": "live",
        "chip": "aqa-api · gpt-6-luna · queries MCI tables", "chip_plain": "AQA NL2SQL",
        "summary": "A natural-language question box that turns questions into SQL. In EX it points at the shared service, which queries MCI tables, not the EX table.",
        "facts": [("Model", "`gpt-6-luna` (external, via egress); temperature 0"), ("Agents", "intent → planner → SQL generation → analyser"),
                  ("Tables", "`call_category_client_view_dist` — not `ex_call_analytics_dist`")],
        "sections": [("Risk", {"note": "EX users asking questions would get MCI data (inferred), and if EX data were ever exposed to AQA it would go to an external model.", "kind": "warn"})]},

    # ------------------------------------------------------------------ lane 6: platform
    "p-serving": {
        "title": "Model serving (vLLM pools)", "title_plain": "vLLM pools", "status": "live",
        "chip": "Envoy LB → k8s pod + bare-metal GPUs", "chip_plain": "vLLM pools",
        "summary": "Each model is served by vLLM behind an Envoy load balancer that mixes one Kubernetes pod with several bare-metal GPU servers. One exception since 2026-11-02: the EX main agent and guardrail call a single bare-metal 31B instance directly, with no load balancer.",
        "sections": [
            ("Pools EX uses", {"table": [["Pool", "Model", "Context", "Notes"],
                ["`172.23.0.17:8318` (no LB)", "Gemma-4 31B", "unknown", "dedicated bare-metal vLLM for EX main agent + guardrail since 2026-11-02; launch flags (context, spec-decode) not in git; not scraped by the exporter"],
                ["`gemma-4-31b-llm-lb`", "Gemma-4 31B", "15K", "speculative decoding (MTP, 4 tokens); shared by 16 services; EX uses it only for KB summarise / markdown and text chat now"],
                ["`gemma4-26b-llm-lb`", "Gemma-4 26B-A4B", "23K", "spec-decode off (vLLM 0.25.1 bug); shared by 11 services; EX: intent, router, clarifying, end-of-turn"],
                ["`gemma-4-e2b-llm-lb`", "Gemma-4 E2B", "unknown", "bare-metal only; flags not in git; 13 services"],
                ["`hakim-unsupervised-vllm-proxy`", "hakim-unsup", "512", "vLLM pooling (CPU + GPU)"]]}),
            ("Gaps", ["No values file requests GPUs or sets tensor-parallel, dtype or max-num-seqs; bare-metal launch flags are not in git.",
                      "The dedicated 31B endpoint is a raw IP in the EX values (`" + OPS + ":1318-1327`), not behind any Envoy pool: no health check, no failover. The host `172.23.0.17` also backs other pools on other ports (31B pool `:8319`, zarebin, COA, Qwen, embeddings), so “dedicated” means its own vLLM process, not necessarily its own GPUs (inferred).",
                      "Context windows (15K / 23K) are far below the models' native windows; long prompts + history can hit vLLM 400 errors."]),
            ("Sources", ["`chatbot-ops/prod/gemma4-31b/values.yaml:86-107`", "`chatbot-ops/prod/gemma4-26b/values.yaml:87-108`", "`chatbot-ops/prod/gemma4-e2b-llm-lb/values.yaml:231-237`"]),
        ]},
    "p-gateway": {
        "title": "LLM gateway (AxonHub)", "title_plain": "AxonHub gateway", "status": "unknown",
        "chip": "routing table in Postgres, not git", "chip_plain": "AxonHub",
        "summary": "A gateway many services use to reach models by alias. EX uses it only for one disabled step, but its routing is invisible from the repos.",
        "facts": [("Image", "`looplj/axonhub:v1.0.0-beta11`, port 8090"), ("EX use", "idle message (disabled)")],
        "sections": [("Why it matters", "Aliases like `main-guardrail` or `gemma-4-26B-it-no-reasoning` resolve only inside its database, so for 19 services the real model cannot be read from git.")]},
    "p-phoenix": {
        "title": "Phoenix: tracing and prompt registry", "title_plain": "Arize Phoenix", "status": "live",
        "chip": "chatbot-phoenix.pr.mci.dev · prompts + traces", "chip_plain": "Phoenix",
        "summary": "Arize Phoenix stores every EX prompt version (the 38 prompts in the UI) and a trace of every IVA turn. It is the best place to see exactly what a model received and returned.",
        "facts": [("Projects", "`chatbot-ex`, `chatbot-ex-iva`"), ("Sampling", "100% for IVA"), ("Retention", "30 days"),
                  ("Prompt tag", "`production` (greeting suggestion `v0_2_0`)")],
        "sections": [
            ("How prompts load", "`USE_PHOENIX_PROMPTS=true`: aiva pulls each `*_TEMPLATE_PROMPT_NAME` by tag from `phoenix-svc:6006`. If loading fails, it falls back to the template in the env var of the same role (`aiva/prompts/loader/loader.py`, `" + OPS + ":1407-1461`). **Prompt versions are managed in Phoenix, not git**, so a prompt change is a production change without a code review."),
            ("How to use it as a TPM", ["Prompts → open an `ex_iva_*` prompt → Versions shows who changed what.",
                                        "Tracing → project `chatbot-ex-iva` → filter by session to replay one call turn by turn, including retrieved contexts.",
                                        "Token counts per span depend on instrumentation; no explicit `LLM_TOKEN_COUNT_*` attribute was found (inferred)."]),
        ]},
    "p-metrics": {
        "title": "Metrics: tokens, latency, load", "title_plain": "Prometheus / APM", "status": "live",
        "chip": "vLLM /metrics · Envoy · Elastic APM", "chip_plain": "metrics",
        "summary": "Per-model token counts and latency come from vLLM and Envoy metrics; per-request latency inside EX comes from Elastic APM.",
        "sections": [
            ("Useful series", ["tokens: `vllm:prompt_tokens_total`, `vllm:generation_tokens_total`",
                               "latency: `vllm:time_to_first_token_seconds`, `vllm:e2e_request_latency_seconds`",
                               "load: `vllm:num_requests_waiting`, KV-cache usage", "LB: `envoy_cluster_upstream_rq_time` per pool"]),
            ("Caveats", {"note": "Exporter targets do not match LB upstreams: some live 31B ports are not scraped (including the dedicated EX endpoint `172.23.0.17:8318`, so the EX main agent and guardrail have no vLLM metrics) and the zarebin pool is labelled 31B, so per-model totals are incomplete. vLLM metrics cannot split EX from other products sharing a pool; use Phoenix traces for that.", "kind": "warn"}),
        ]},
}
STEPS.update(BRAIN_STEPS)

MODELS = {
    "title": "Every model in EX: size, role and why",
    "lede": "Sizes are public model facts (billions of parameters), not read from code. MoE models list total and active parameters: active parameters drive speed and cost per token.",
    "cards": [
        {"name": "Gemma-4 26B-A4B-it", "size": "26B total · ~4B active (MoE) · context 23K here", "status": "live",
         "facts": ["**Role:** the main voice answer agent, intent, classifying, clarifying, end-of-turn detection, voice bridge (off).",
                   "**Why:** near-large-model understanding at ~4B-model speed, which is what a live phone turn needs (inferred).",
                   "**Serving:** `gemma4-26b-llm-lb`, vLLM 0.25.1, spec-decode off."],
         "steps": ["v-turn", "b-intent", "b-clarify", "b-classify", "b-react", "b-voicebridge"]},
        {"name": "Gemma-4 31B-it", "size": "31B dense · context 15K here", "status": "live",
         "facts": ["**Role:** guardrail, KB speakable summary, suggestion markdown, text chatbot agent, diacritisation.",
                   "**Why:** best in-house Persian quality where safety or wording matters more than latency (inferred).",
                   "**Serving:** `gemma-4-31b-llm-lb`, vLLM 0.25.1, MTP speculative decoding."],
         "steps": ["b-guardrail", "b-guard-reply", "k-summarize"]},
        {"name": "Gemma-4 E2B-it", "size": "~2B effective (~5B with embeddings)", "status": "live",
         "facts": ["**Role:** relevance filter over retrieved Q&A on every turn.", "**Why:** easy pick-from-list task, every turn, lowest latency (inferred).",
                   "**Serving:** bare-metal only, flags not in git."], "steps": ["k-filter"]},
        {"name": "hakim-unsup", "size": "≈0.12B encoder · 768-d (unverified)", "status": "live",
         "facts": ["**Role:** embeds KB questions and each employee utterance.", "**Why:** in-house Persian encoder, cheap enough for CPU (inferred).",
                   "**Serving:** vLLM pooling, max length 512."], "steps": ["k-embed", "k-search"]},
        {"name": "Silero VAD", "size": "≈1M params (0.001B) · CPU", "status": "live",
         "facts": ["**Role:** speech / silence detection inside each call process.", "**Why:** standard, tiny, per-frame fast."], "steps": ["v-vad"]},
        {"name": "Soniox real-time STT", "size": "proprietary · size not published", "status": "external",
         "facts": ["**Role:** live Persian transcription.", "**Why:** streaming accuracy and latency (inferred).", "**Note:** employee audio leaves the cluster."], "steps": ["v-stt"]},
        {"name": "OpenAI gpt-6-luna", "size": "proprietary", "status": "external",
         "facts": ["**Role:** greeting agent; also the shared AQA NL2SQL agent.", "**Note:** the only EX text generation outside the cluster."], "steps": ["b-greeting", "v-session", "a-aqa"]},
        {"name": "neurobox TTS `ex_prod`", "size": "unknown (VITS-class ≈0.03–0.04B if VITS, inferred)", "status": "unknown",
         "facts": ["**Role:** speaks every answer.", "**Serving:** Triton behind `neurobox-gateway-green` (neurobox-prod, not in our repos)."], "steps": ["v-tts"]},
        {"name": "k2 ASR `coa_iva_prod_long` + emotion + gender", "size": "unknown", "status": "external",
         "facts": ["**Role:** offline re-transcription for analytics.", "**Serving:** `asr-k2-tmp-gw-proxy` (neurobox-prod)."], "steps": ["a-asr"]},
        {"name": "CCA engine models", "size": "likely Gemma-4 26B-A4B and/or 31B COA pools (inferred)", "status": "external",
         "facts": ["**Role:** call tagging, sentiment, summary, categories.", "**Note:** no client of the COA pools in our repos."], "steps": ["a-cca"]},
    ],
    "sections": [
        ("How to read “B”", ["**B = billions of parameters.** It sets memory and quality. For MoE models (“A4B”, “A3B”) only the active part runs per token, so a 26B-A4B model decodes about as fast as a 4B dense model but needs the memory of a 26B one.",
                             "**Context length** (15K, 23K tokens here) is the most the model can read at once: system prompt + KB contexts + history + answer. It is set per deployment (`--max-model-len`), not by the model.",
                             "**Token budgets per step** (max output tokens, temperature) are listed on each step page when the code sets them."]),
    ],
}

RISKS = {
    "title": "Risks and gaps a TPM should track",
    "lede": "Collected from the code reading. Severity is my judgement for the HR pilot, not an agreed rating.",
    "items": [
        {"sev": "high", "title": "Prod voice agent runs an unmerged branch", "why": "STT (Soniox) exists only on `feat-soniox-lang`; a rebuild from main breaks transcription.", "steps": ["v-stt"]},
        {"sev": "high", "title": "Employee data leaves the cluster", "why": "Live audio → Soniox; greeting context → OpenAI; logs hold transcripts and phone numbers; traces sampled at 100%.", "steps": ["v-stt", "v-session", "m-stores"]},
        {"sev": "high", "title": "No HR sensitive / emergency handling after the call", "why": "No taxonomy, classifier or alerting in code; the bot prompt assumes a backend that does not exist.", "steps": ["a-cca"]},
        {"sev": "high", "title": "Analysis engine (CCA) is a black box", "why": "Prompts, models and settings are not in our repos, so EX analytics cannot be audited.", "steps": ["a-cca"]},
        {"sev": "high", "title": "Main agent and guardrail on one unmonitored endpoint", "why": "Since 2026-11-02 both call one bare-metal vLLM at `172.23.0.17:8318`: no load balancer, health check or failover, and not in the exporter, so no metrics. If it fails, every EX turn fails.", "steps": ["b-react", "b-guardrail", "p-serving", "p-metrics"]},
        {"sev": "high", "title": "Fallback prompts are broken", "why": "If Phoenix is unreachable at pod start, env fallbacks load; the ReAct one would make every main turn fail (KeyError) and the guardrail one ignores policies.", "steps": ["b-prompts"]},
        {"sev": "med", "title": "Grounding is prompt-only", "why": "Threshold 0.25 + fail-open filter on a ~2B model; no code gate for “no approved answer”.", "steps": ["k-search", "k-filter"]},
        {"sev": "med", "title": "Human transfer always fails and drops the call", "why": "`AGENT_SIP_REDIRECT_URL` unset.", "steps": ["v-end"]},
        {"sev": "med", "title": "MCI greeting fallback", "why": "If session creation fails the caller hears the MCI assistant greeting.", "steps": ["v-session"]},
        {"sev": "med", "title": "EX panel may show MCI data", "why": "Trends bucket, failed-calls table and NL2SQL tables default to MCI.", "steps": ["a-sync", "a-aqa"]},
        {"sev": "med", "title": "Prompts change outside code review", "why": "All `ex_iva_*` prompts are versioned in Phoenix, tag `production`.", "steps": ["p-phoenix"]},
        {"sev": "med", "title": "Guardrail on every turn, fails open, no timeout", "why": "A 31B check sits on the critical path and now queues on the same instance as the main answer; empty output = allowed; aiva sets no timeouts.", "steps": ["b-guardrail"]},
        {"sev": "med", "title": "Code / prod drift", "why": "aiva main 0.33.3 vs prod 0.31.1 (next deploy changes history handling); KB image tag `df70f4be` matches no commit.", "steps": ["b-setup", "k-author"]},
        {"sev": "low", "title": "Leftovers from MCI aiva", "why": "`send_sms` enabled without a token; shared `aiva-classification` examples; ignored prompt `ex_iva_guardrail_llm_base_template`.", "steps": ["b-tools", "b-classify", "b-guard-reply"]},
        {"sev": "low", "title": "Voice answer text unused", "why": "`iva_text` is indexed but the agent reads the text-chat answer.", "steps": ["k-collections"]},
        {"sev": "low", "title": "Persian sentence splitting", "why": "TTS splits only on `. `, so questions ending in `؟` are synthesised as one long chunk.", "steps": ["v-tts"]},
        {"sev": "low", "title": "Incomplete model metrics", "why": "Exporter targets do not match LB upstreams.", "steps": ["p-metrics"]},
        {"sev": "low", "title": "Plaintext credentials in values", "why": "LiveKit key/secret and Redis password.", "steps": ["v-ingress"]},
    ],
}

DATA = {"lang": "en", "dir": "ltr", "ui": UI, "meta": META, "lanes": LANES, "system_edges": SYSTEM_EDGES,
        "key_points": KEY_POINTS, "steps": STEPS, "models": MODELS, "risks": RISKS}
DATA["lanes"][1]["steps"] = [k for k in BRAIN_STEPS]
