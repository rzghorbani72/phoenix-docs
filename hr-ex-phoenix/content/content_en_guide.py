"""English learning guide for the Phoenix EX pipeline site. Rendered as guide.html next to index.html.

Body conventions (same as content_en.py): str = paragraphs split by blank lines, list = bullets,
{"table": [header, rows...]}, {"ol": items}, {"note": text, "kind": "warn|bad|"}, {"code": text};
a tuple holds several bodies. Inline markup: `code`, **bold**, [label](url), "(inferred)".
State reflects prod on 2026-11-02, including the move of the EX main ReAct agent and the guardrail
to Gemma-4 31B on the dedicated bare-metal endpoint 172.23.0.17:8318.
"""

AI_GUIDE = "docs/technical/AI_LEARNING_GUIDE_FA.html"
PRD = "docs/product-management/IVA_EX_PROMPT_REQUIREMENTS_FA.html"

GUIDE = {
    "title": "Learning guide: become fluent in Phoenix EX",
    "lede": "A study path for a Technical Product Manager who has to own the Employee Voice (صدای کارکنان) voice agent and speak confidently with every team behind it. Every concept is explained from zero and then tied to the exact step, model and setting where it shows up in EX. Read it next to the [pipeline map](index.html); it does not repeat the general AI course in the [AI learning guide (Persian)](" + AI_GUIDE + ").",
    "sections": [
        # ------------------------------------------------------------------ 1
        ("How to use this site", (
            "The site is built in layers. The [map](index.html) shows six lanes of boxes; each box opens a step page with the model, its size, inputs, outputs, settings, failure behaviour and code references. The [Models](models.html) page lists every model once, and [Risks & gaps](risks.html) collects what a TPM should track. This guide is the glue: it teaches the vocabulary, gives you a reading order, and turns the pages into exercises and questions.",
            {"ol": [
                "**The map first** ([index.html](index.html)). Read the one-sentence summary and the “things to know” warning. Do not open any step yet; just learn the six lanes and the arrows between them.",
                "**[Lane 1, the phone call](index.html#lane-call).** This is what the employee experiences. Read V1 → V13 in order; it teaches VAD, speech-to-text, turn-taking and text-to-speech in the order they happen.",
                "**[Lane 2, the brain](index.html#lane-brain).** One turn inside aiva. Read B1 (prompt loading) before anything else, then follow the orchestration: intent, clarifying, retrieval, guardrail, classifier, branch selection, ReAct.",
                "**[Lane 3, the knowledge base](index.html#lane-kb).** Where approved HR answers come from and how they reach the prompt. This lane decides whether the agent is grounded.",
                "**[Lane 5, post-call analytics](index.html#lane-analytics).** What HR sees in the panel after the call, and which parts are a black box.",
                "**[Models](models.html).** Now the sizes and roles make sense. Read it with section “How to reason about model choice” below.",
                "**[Risks & gaps](risks.html).** Read it last, when every risk points at a step you already know.",
                "**[The framework lane](index.html#lane-framework)** and the remaining lanes ([memory](index.html#lane-memory), [ops](index.html#lane-ops)) as reference: return to them when a question touches data stores, serving or observability.",
            ]},
            {"note": "**Status labels matter.** Live, Configured-off, Not-deployed, External and Unverified are different claims. When you repeat something from this site to a stakeholder, keep its label: “the code supports human transfer” is not the same as “EX transfers calls”. Text marked (inferred) is reasoning, not code.", "kind": "warn"},
            "Two other documents are your companions. The [EX PRD (Persian)](" + PRD + ") says what the agent **should** do (rule ids like SEN, GRD, KB, CLO, VOX); this site says what it **does**. The [AI learning guide (Persian)](" + AI_GUIDE + ") covers general AI background, benchmarks and Hugging Face reading; this guide only goes as deep as you need for EX.",
        )),

        # ------------------------------------------------------------------ 2
        ("A 10-day plan to proficiency", (
            "About 2–3 focused hours a day. Each day ends with a small artefact you keep (a note, a diagram, a list of questions), because writing is what turns reading into ownership. By day 10 you should be able to explain any EX turn end to end, name the model behind every decision, and run the pilot go/no-go conversation.",
            {"table": [
                ["Day", "Goal", "Read", "Do / produce"],
                ["1", "Mental model of the whole system", "[Map](index.html), this guide's “System on one page”, PRD sections on goal and non-goals", "Draw the six lanes from memory on one page. Mark the two places where employee data leaves the cluster."],
                ["2", "The phone call", "[Lane 1](index.html#lane-call): [V1](steps/v-ingress.html) → [V13](steps/v-summary.html); concepts “Voice” below", "Write the latency budget of one turn from end-of-speech to first audio. Call the EX line once (if allowed) and time the gap with a stopwatch."],
                ["3", "Tokens, context, model sizes", "Concepts “Language models” and “Serving” below; [Models](models.html)", "For each LLM call in EX, write: model, total/active params, context window, streaming or not."],
                ["4", "The brain, part 1", "[B1 prompts](steps/b-prompts.html), [B2 greeting](steps/b-greeting.html), [B3 setup](steps/b-setup.html), [B4 intent](steps/b-intent.html), [B5 clarify](steps/b-clarify.html)", "In Phoenix, open every `ex_iva_*` prompt and list its last version date and author (exercise 1)."],
                ["5", "The brain, part 2", "[B6 retrieve](steps/b-retrieve.html), [B7 guardrail](steps/b-guardrail.html), [B8 classify](steps/b-classify.html), [B9 branch](steps/b-branch.html), [B10 ReAct](steps/b-react.html)", "Open one trace in Phoenix and label every span with its step id (exercise 2). Compare the ReAct span's model name with the 2026-11-02 change."],
                ["6", "Grounding and the KB", "[Lane 3](index.html#lane-kb): [K1](steps/k-author.html) → [K8](steps/k-carry.html); concepts “Retrieval” below; PRD section KB", "Write the three “I cannot answer” cases from the PRD and, for each, which step in EX would produce it today."],
                ["7", "Memory, data and privacy", "[Lane 4](index.html#lane-memory), [M4 data stores](steps/m-stores.html), PRD sections MDT and SEN", "Build a data inventory: store, data, retention, who can read it, leaves cluster? Mark every unknown as a question."],
                ["8", "Post-call analytics", "[Lane 5](index.html#lane-analytics): [A1](steps/a-ingest.html) → [A10](steps/a-aqa.html)", "Trace one call id from Kafka to the panel. List which fields in the panel come from CCA, which you cannot audit."],
                ["9", "Platform and observability", "[Lane 6](index.html#lane-ops), [P1 serving](steps/p-serving.html), [P4 metrics](steps/p-metrics.html)", "Run the PromQL queries in exercise 4. Write the 5 numbers you will watch daily during the pilot."],
                ["10", "Synthesis", "[Risks & gaps](risks.html), the decision checklist below", "Write a one-page pilot readiness note: top risks, owners, decisions needed, and the questions you still have per team."],
            ]},
            {"note": "If you only have three days: day 1 + day 5 + day 10, with the worked example below as your reading for day 2.", "kind": ""},
        )),

        # ------------------------------------------------------------------ 3
        ("The system on one page", (
            "An employee calls a number. The call reaches a LiveKit server over SIP and is handed to a Python voice agent. The agent listens with Silero VAD, streams the audio to Soniox (a cloud speech-to-text service), asks a Gemma-4 26B-A4B model whether the employee has finished speaking, and then sends the text to **aiva**, the brain. aiva runs several small model calls in parallel (exit intent, a speculative short reply, retrieval with an E2B relevance filter, a route classifier and a 31B guardrail), then lets the **Gemma-4 31B ReAct agent** write the answer from approved HR knowledge. The streamed answer is spoken by the in-house neurobox TTS. After hang-up, the recording and a summary flow through Kafka to grogu, which re-transcribes the call, and to the external CCA engine, which tags it for the EX panel.",
            {"table": [
                ["Decision in a turn", "Step", "Model (prod, 2026-11-02)", "Where it runs"],
                ["Is the employee speaking?", "[V3](steps/v-vad.html)", "[Silero VAD](models/silero-vad.html) ≈1M params", "CPU, inside each call process"],
                ["What did they say?", "[V4](steps/v-stt.html)", "[Soniox real-time](models/soniox-stt.html)", "**External SaaS** via egress proxy"],
                ["Have they finished?", "[V5](steps/v-turn.html)", "[Gemma-4 26B-A4B](models/gemma-4-26b-a4b.html)", "shared `gemma4-26b-llm-lb`"],
                ["Do they want to hang up?", "[B4](steps/b-intent.html)", "Gemma-4 26B-A4B", "shared pool"],
                ["Short social reply ready, just in case", "[B5](steps/b-clarify.html)", "Gemma-4 26B-A4B", "shared pool"],
                ["Which approved Q&A is relevant?", "[K4](steps/k-embed.html), [K7](steps/k-filter.html)", "[hakim-unsup](models/hakim-unsup.html) + [Gemma-4 E2B](models/gemma-4-e2b.html)", "shared pools"],
                ["Is this request allowed?", "[B7](steps/b-guardrail.html)", "[Gemma-4 31B](models/gemma-4-31b.html)", "**dedicated** bare-metal `172.23.0.17:8318`"],
                ["Full answer or short reply?", "[B8](steps/b-classify.html)", "Gemma-4 26B-A4B", "shared pool"],
                ["Write the answer", "[B10](steps/b-react.html)", "**Gemma-4 31B**", "**dedicated** `172.23.0.17:8318`"],
                ["Say it", "[V8](steps/v-tts.html)", "[neurobox TTS ex_prod](models/neurobox-tts.html)", "neurobox-prod (in-house)"],
                ["First greeting (once per call)", "[B2](steps/b-greeting.html)", "[OpenAI gpt-6-luna](models/openai-frontier.html)", "**External SaaS**"],
                ["After the call: transcript, emotion", "[A3](steps/a-asr.html)", "[k2 ASR](models/neurobox-asr.html)", "neurobox-prod"],
                ["After the call: tags, sentiment, summary", "[A5](steps/a-cca.html)", "unknown (CCA is outside our repos)", "external to our repos"],
            ]},
            {"note": "**What changed on 2026-11-02.** Until today the ReAct agent ran on Gemma-4 26B-A4B (shared pool) and the guardrail on Gemma-4 31B (shared `gemma-4-31b-llm-lb`, 17 services). Both now call one dedicated Gemma-4 31B vLLM instance at `172.23.0.17:8318`. Intent, clarifying, classifier and end-of-turn stay on 26B-A4B. The trade-offs are in “How to reason about model choice”.", "kind": "warn"},
        )),

        # ------------------------------------------------------------------ 4
        ("Concepts 1: how a language model works (just enough)", (
            "You do not need the maths. You need the handful of quantities that decide **quality, speed, cost and failure modes** of every LLM call in EX. For deeper background see the [AI learning guide](" + AI_GUIDE + ").",
            [
                "**Token.** Models do not read letters or words; they read tokens, chunks of text from a fixed vocabulary of tens of thousands of pieces. An English word is about 1.3 tokens; Persian usually costs more tokens per word because tokenizers were trained on less Persian text (roughly 1.5–3 per word, (inferred) for Gemma's tokenizer). Everything is counted in tokens: prompt size, answer size, speed, limits. **In EX:** every number on [P4 metrics](steps/p-metrics.html) (`vllm:prompt_tokens_total`, `vllm:generation_tokens_total`) is tokens; the Kafka call summary carries token counts ([V13](steps/v-summary.html)).",
                "**Prompt vs completion.** The prompt is everything sent in (system instructions, history, retrieved knowledge, the employee's words); the completion is what comes back. Reading the prompt is called **prefill** and is done in parallel, fast per token; writing the completion is **decode**, one token at a time, and is what you hear as speaking speed. **In EX:** the ReAct prompt is large (system prompt + up to 50 history items + up to 10 Q&A contexts) and its answer is short, so prefill dominates time-to-first-token ([B10](steps/b-react.html)).",
                "**Context window vs deployed `--max-model-len`.** The context window is the most tokens a model can handle at once (prompt + completion). The model card states a native maximum (very large for Gemma-4, on the order of 128K–256K); the **deployment** sets the real limit with vLLM's `--max-model-len`, because every token of possible context reserves GPU memory. **In EX:** the 31B pools run at **15K** and the 26B-A4B pool at **23K** ([P1](steps/p-serving.html)). Since today the ReAct agent runs on 31B, its budget may have shrunk from 23K to 15K if the dedicated instance uses the same flags (unverified: its flags are not in git). A request over the limit is rejected with an HTTP 400 and the turn fails; it does not silently truncate.",
                "**Parameters and “B”.** Parameters are the learned numbers inside the model; “31B” means about 31 billion. More parameters usually means better reasoning and language quality, but also more GPU memory and slower decoding. Memory rule of thumb: in 16-bit precision each parameter takes 2 bytes, so 31B ≈ 62 GB of weights before any working memory. **In EX:** sizes per model are on [Models](models.html); they are public model facts, not read from code.",
                "**Dense vs Mixture-of-Experts (MoE); total vs active parameters.** A dense model uses all its parameters for every token. An MoE model has many “expert” sub-networks and a router that picks a few per token. `26B-A4B` means 26B total, about 4B **active** per token; `35B-A3B` (the Qwen3.5 code default for the KB summarizer, overridden in EX, see [K2](steps/k-summarize.html)) means 35B total, 3B active. **Why active params drive speed:** decoding one token means reading every weight that participates from GPU memory, and memory bandwidth is the bottleneck. A4B reads ~4B weights per token, the 31B dense reads all 31B, so the MoE decodes several times faster on the same GPU. But all 26B must still **fit** in memory, so MoE saves time, not memory. **In EX:** this is why the latency-critical small decisions ([V5](steps/v-turn.html), [B4](steps/b-intent.html), [B5](steps/b-clarify.html), [B8](steps/b-classify.html)) use 26B-A4B, and why moving the ReAct agent to 31B dense costs speed.",
                "**Per-layer embeddings and “effective” size (E2B).** Gemma-4 E2B stores a large share of its parameters in per-layer embedding tables, which are looked up rather than multiplied, so they can live in cheaper memory and add little compute. “E2B” = about 2B **effective** (compute-relevant) parameters, around 5B counting the embeddings. **In EX:** E2B is the relevance filter on every turn ([K7](steps/k-filter.html), [model](models/gemma-4-e2b.html)); it is the smallest and fastest LLM in the stack, and also the one whose mistakes decide what knowledge the answer agent sees.",
                "**Quantization and dtype.** Weights can be stored at lower precision: bf16 (2 bytes), fp8 (1 byte), int4 (half a byte). Lower precision means less memory and faster decode, with some quality loss, usually small at fp8 and more visible in non-English languages at 4-bit. **In EX:** no values file sets `--dtype` or `--quantization`, so the in-cluster pods use vLLM's default (bf16 for Gemma, (inferred)); the bare-metal instances' flags, including the new `:8318`, are not in git ([P1](steps/p-serving.html)). Ask SRE.",
                "**Temperature, max tokens, reasoning effort.** Temperature controls randomness: 0 = always the most likely token (repeatable), higher = more varied. Max tokens caps the completion length. Reasoning effort tells “thinking” models how much hidden reasoning to produce before answering; more thinking = better on hard questions but more latency. **In EX:** intent runs at temperature 0.1 (a decision must be stable) ([B4](steps/b-intent.html)); the ReAct agent and greeting run with reasoning effort `none` and no explicit temperature or max tokens, so server defaults apply ([B10](steps/b-react.html), [B2](steps/b-greeting.html)); the E2B filter allows up to 4096 output tokens for what is a short JSON list ([K7](steps/k-filter.html)).",
                "**Streaming, time-to-first-token (TTFT), tokens/sec.** With streaming, tokens are sent as soon as they are generated. For a phone call the number that matters is **TTFT** (queue wait + prefill) plus the time to produce the **first full sentence**, because TTS needs a sentence before it can speak. Tokens/sec (decode speed) then decides whether the rest of the answer keeps up with speech. **In EX:** the ReAct agent and clarifying agent stream; intent, classifier, guardrail and greeting do not, so their full completion time is on the critical path. TTS waits for `\". \"` before synthesising ([V8](steps/v-tts.html)), so a long first sentence delays audio.",
                "**Speculative decoding (MTP).** A small, fast draft predicts several next tokens; the big model checks them all in one step and keeps the ones it agrees with. When the draft is often right, you get 1.5–2.5× faster decoding with identical output quality. Gemma-4 uses an MTP (multi-token prediction) draft. **In EX:** the shared 31B pool runs MTP with 4 speculative tokens; it is **off** on the 26B-A4B pool because of a vLLM 0.25.1 bug ([P1](steps/p-serving.html)). Whether the new dedicated `:8318` instance runs MTP is a key latency question for today's change.",
            ],
        )),

        # ------------------------------------------------------------------ 5
        ("Concepts 2: how models are served", (
            [
                "**vLLM.** The open-source inference server that runs every in-house LLM and the Hakim embedder here. It exposes an OpenAI-compatible HTTP API (`/v1/chat/completions`, `/v1/responses`, `/v1/embeddings`), which is why aiva can talk to Gemma and to OpenAI with the same client. **In EX:** version 0.25.1 on the main pools ([P1](steps/p-serving.html)).",
                "**Continuous batching.** A GPU is most efficient when it processes many requests together. vLLM adds and removes requests from the running batch every step instead of waiting for a batch to finish, so a short request (an end-of-turn float) is not stuck behind a long one. The flip side: under heavy load every request slows down a bit, and queued requests wait. **In EX:** this is why the shared pools' load from other products shows up as EX latency; `vllm:num_requests_waiting` is the queue.",
                "**KV cache.** While processing a request, the model keeps intermediate results (keys and values) for every token so it does not recompute them. This cache lives in GPU memory and grows with context length × concurrent requests. When it is full, new requests wait or running ones are pre-empted. **Prefix caching** lets requests that share the same beginning (for example, the same system prompt) reuse it. **In EX:** aiva renders the ReAct system prompt from cache-stable fields only so the prefix can be reused ([B10](steps/b-react.html)); `vllm:gpu_cache_usage_perc` (or `kv_cache_usage_perc`) shows how full it is.",
                "**GPU memory utilization.** `--gpu-memory-utilization 0.95` lets vLLM take 95% of GPU memory: weights first, the rest for KV cache. With 31B in bf16 (~62 GB), what is left decides how many 15K-token conversations fit at once. This is the real reason context windows are set far below the native maximum: memory per concurrent call. **In EX:** all pools use 0.95 ([P1](steps/p-serving.html)).",
                "**Load balancers and bare-metal pools.** Each model “pool” is an Envoy load balancer (`*-llm-lb`) in Kubernetes that spreads requests over one in-cluster vLLM pod and several bare-metal GPU servers (`172.16.21.4`, `172.23.0.3/.4/.17` on various ports). Envoy retries on unhealthy upstreams and exports per-pool latency. **In EX:** the 26B-A4B pool is shared by 11 services and the 31B pool by 17; the new dedicated `172.23.0.17:8318` is a **single upstream with no load balancer in front** (as described in the change), so it has no failover and its metrics are not scraped unless SRE adds it to the exporter (inferred) ([P1](steps/p-serving.html), [P4](steps/p-metrics.html)).",
                "**Gateways (AxonHub).** A gateway maps aliases like `main-guardrail` to real models in a database. Useful for operators, opaque for reviewers. **In EX:** only one disabled step uses it ([P2](steps/p-gateway.html)).",
            ],
        )),

        # ------------------------------------------------------------------ 6
        ("Concepts 3: retrieval and grounding", (
            [
                "**Embedding / vector.** An embedding model turns a text into a list of numbers (a vector) so that texts with similar meaning get nearby vectors. **In EX:** [hakim-unsup](models/hakim-unsup.html), an in-house Persian encoder (~0.12B), produces 768-number vectors ([K4](steps/k-embed.html)).",
                "**Cosine similarity.** A score for how closely two vectors point the same way: 1 = same meaning, 0 = unrelated. It is a ranking signal, not a probability, and each embedding model has its own scale: 0.25 on Hakim is not comparable to 0.25 on another model.",
                "**Multivector and MAX_SIM.** Instead of one vector per answer, EX stores one vector per paraphrase question (an N×768 multivector per answer). At query time the answer's score is the **maximum** similarity between the query and any of its questions (Qdrant `MAX_SIM`). Effect: adding a new paraphrase can only help an answer be found; it never dilutes the others. **In EX:** [K5 collections](steps/k-collections.html).",
                "**Threshold and top-k.** Top-k = how many best matches to keep (10 here); threshold = minimum similarity (0.25 here, code default 0.5). Low threshold → high recall (rarely misses the right answer) but more noise; high threshold → precise but misses paraphrases. **In EX:** the low bar deliberately pushes precision onto the E2B filter ([K6](steps/k-search.html)).",
                "**RAG (retrieval-augmented generation).** Instead of trusting what the model memorised, you retrieve approved text and put it into the prompt, and instruct the model to answer only from it. **In EX:** retrieved `Question:/Answer:` pairs fill `{contexts}` in the ReAct user template ([K8](steps/k-carry.html)). Grounding is only as good as retrieval: if the right Q&A is not retrieved, the model either says it does not know or, worse, improvises.",
                "**Why only questions are embedded.** An employee's utterance looks like a question, not like a long policy answer. Matching question-to-question is more precise than question-to-answer, so EX embeds only the paraphrase questions ([K4](steps/k-embed.html)). The product consequence: **coverage = paraphrase coverage**. If HR writes one phrasing per answer, many real spoken phrasings will miss. Only the latest utterance is embedded, with no rewriting, so short follow-ups like «اون یکی چی؟» rely on carry-over ([K6](steps/k-search.html), [K8](steps/k-carry.html)).",
                "**LLM relevance filter vs reranker.** A **reranker** is a model (often a cross-encoder) that scores each (query, candidate) pair and re-orders them; it outputs scores. An **LLM filter** reads the whole conversation plus the candidate list and returns which items to keep. It understands context better but is slower, can produce invalid output and needs a failure policy. **In EX:** the filter is Gemma-4 E2B with prompt `ex_iva_contexts_filter_llm_template`, returning `{\"indexes\":[…]}`; on any error it **fails open** and passes all candidates unfiltered ([K7](steps/k-filter.html)).",
            ],
            {"note": "**Grounding in EX is prompt-only.** There is no code rule “no relevant context → refuse”. The chain threshold 0.25 → E2B filter (fails open) → 31B ReAct prompt instruction is what keeps answers inside the KB. Test it with questions the KB does not cover.", "kind": "warn"},
        )),

        # ------------------------------------------------------------------ 7
        ("Concepts 4: agents, guardrails and prompts", (
            [
                "**Guardrail.** A separate check that decides whether a request may be handled, before or alongside the answer. It can be a rule, a classifier or an LLM. **In EX:** the [B7 guardrail](steps/b-guardrail.html) is a Gemma-4 31B call that reads the conversation, the filtered contexts and retrieved allow/deny policies (from `chatbot-ex-aiva-guardrails`) and replies `1` (allow) or `0` (deny). A deny replaces the answer with a generated polite refusal ([B12](steps/b-guard-reply.html)).",
                "**Fail-open vs fail-closed.** When a safety component fails (timeout, error, garbage output), fail-open lets the request through; fail-closed blocks it. Fail-open protects availability, fail-closed protects safety. Neither is “right”; it is a product decision per component. **In EX:** the guardrail (empty or non-numeric reply = allowed), the relevance filter (error = all candidates pass) and intent (error = continue) all fail open; the end-of-turn detector fails to “finished” ([V5](steps/v-turn.html)). Write down which of these HR would accept.",
                "**ReAct and tool calling.** ReAct (Reason + Act) is an agent loop: the model either answers or asks to call a tool (a function with a name and JSON arguments); the system runs the tool and gives the result back; repeat until an answer. Tool calling is the model emitting a structured call instead of text. **In EX:** the [B10 ReAct agent](steps/b-react.html) may loop up to 10 times, but its only enabled tool is `send_sms`, without a token ([B11](steps/b-tools.html)); ending the call is a separate intent agent with `exit_tool`.",
                "**Intent detection and routing / classification.** Intent detection asks “what does the user want to do?” (here: hang up or continue). Routing picks which agent should answer (here: `main` or `clarifying_chitchat`). Both are classification tasks: short output, best done by a fast model at low temperature, with a safe default when the output is invalid. **In EX:** [B4 intent](steps/b-intent.html), [B8 classifier](steps/b-classify.html) (invalid → `main`). Note the classifier's few-shot examples come from a shared, non-EX collection.",
                "**Speculative branches and cancellation.** To hide latency, aiva starts several possible answers before it knows which one it needs, and cancels the losers. **In EX:** the clarifying reply streams privately on every turn; the orchestrator picks guardrail-deny > exit > clarifying > main and cancels the rest ([B9](steps/b-branch.html)). Cost: GPU work on every turn for output that is usually thrown away; benefit: short social replies feel instant.",
                "**Prompt registry and prompt versioning.** Prompts are product logic. A registry stores each prompt with versions and tags so you can change and roll back wording without a code release. **In EX:** aiva loads 13 `ex_iva_*` prompts from Phoenix with tag `production`, **once at pod start** ([B1](steps/b-prompts.html), [P3](steps/p-phoenix.html)). Editing in Phoenix is a production change without code review, and it takes effect only after a restart. The model shown next to a prompt in Phoenix is ignored; since today the main and guardrail prompts happen to match it (31B), the others still do not.",
            ],
            {"note": "**PRD link.** The PRD's decision order (listen first, one follow-up at most, KB-only answers, sensitive-topic handling, no promises about pay or promotion) is implemented **only** inside the Phoenix prompt text and the ReAct model's obedience to it. That is why the 31B upgrade matters and why prompt versions must be governed. See the [EX PRD](" + PRD + ").", "kind": ""},
        )),

        # ------------------------------------------------------------------ 8
        ("Concepts 5: voice", (
            [
                "**VAD (voice activity detection).** A tiny model that says, every few milliseconds, “speech” or “not speech”. It is the clock of the conversation: end of speech, barge-in and the silence timer all start from it. **In EX:** [Silero VAD](models/silero-vad.html) at threshold 0.3 and 0.2 s minimum speech: sensitive, to catch a short «بله» ([V3](steps/v-vad.html)).",
                "**STT / ASR (speech-to-text / automatic speech recognition).** Turns audio into text. **Streaming ASR** returns partial (interim) text while the person talks and a final text shortly after they stop; it must be fast and is usually slightly less accurate. **Offline ASR** gets the whole file and can use full context, so it is more accurate and can add labels (emotion, gender, speaker channel). **In EX:** live = [Soniox](models/soniox-stt.html), cloud, external ([V4](steps/v-stt.html)); after the call = in-house [k2 ASR](models/neurobox-asr.html) `coa_iva_prod_long` ([A3](steps/a-asr.html)). The two transcripts can differ, so the analysed text is not exactly what the bot heard.",
                "**WER (word error rate).** The standard ASR quality metric: (substituted + deleted + inserted words) ÷ words in the reference transcript. 10% WER means roughly one word in ten is wrong. For Persian, measure on your own audio (accents, phone line quality, HR vocabulary); vendor numbers rarely transfer. **In EX:** no WER measurement exists in the repos; a labelled sample of pilot calls is the only way to compare Soniox vs k2 fairly.",
                "**End-of-turn detection.** Deciding that the person has finished their thought, not just paused. Silence alone is a poor signal in Persian («که…» trails off mid-thought). **In EX:** after 0.5 s of silence a [Gemma-4 26B-A4B](models/gemma-4-26b-a4b.html) call reads the last 6 messages and returns a probability; below 0.5 the agent waits longer ([V5](steps/v-turn.html)).",
                "**Endpointing.** The extra wait between “probably finished” and committing the turn to the brain. Too short cuts people off; too long feels robotic. **In EX:** dynamic 0.1–0.5 s, about 5× tighter than the defaults ([V6](steps/v-endpoint.html)).",
                "**Barge-in.** Letting the caller interrupt the agent: playback stops when the caller speaks long enough. **In EX:** 0.4 s of VAD speech ([V9](steps/v-bargein.html)); with a sensitive VAD, line noise can cut the agent off.",
                "**TTS (text-to-speech).** Turns text into audio. Most TTS needs a full sentence for natural prosody, so the text stream is split into sentences first. **In EX:** neurobox `ex_prod`, speed 1.1; the splitter breaks only on `\". \"`, so a Persian question ending in `؟` is synthesised as one long chunk ([V8](steps/v-tts.html)).",
                "**Thinking sound and voice bridge.** Ways to mask the gap while the brain works: an ambient sound (on in EX) or a generated filler sentence (the voice bridge, off in EX) ([B13](steps/b-voicebridge.html)).",
            ],
        )),

        # ------------------------------------------------------------------ 9
        ("Concepts 6: data pipelines and observability", (
            [
                "**Kafka.** A durable message log. Producers append messages to a topic; consumers read at their own pace and record their position (offset). It decouples the live call from slow post-call work. **In EX:** the voice agent publishes to `chatbot-mci-ex-iva` ([V13](steps/v-summary.html)); grogu publishes to `anzu-coa-call-ex` for CCA ([A4](steps/a-publish.html)).",
                "**At-least-once delivery.** The consumer commits its offset only after the work is safely recorded, so after a crash a message may be processed twice but never lost. Consumers must therefore be idempotent (safe to repeat). **In EX:** grogu commits after the DB rows exist and skips calls already in progress or done ([A1](steps/a-ingest.html)). Note the producer side: a failed summary publish is logged, not re-queued, so a call can be missing from analytics entirely.",
                "**Dead letters.** Messages that failed processing are parked in a dead-letter store and retried later instead of blocking the stream. **In EX:** grogu's dead-letter table is retried every 5 min, up to 10 times ([A1](steps/a-ingest.html)). A call that never succeeds needs a human to notice it: ask who owns that alert.",
                "**ClickHouse vs Postgres.** Postgres is a transactional database: row-by-row reads and writes, constraints, good for the app's own state (sessions, messages, KB). ClickHouse is a columnar analytics database: very fast aggregation over millions of rows, append-oriented, poor at single-row updates. **In EX:** CCA writes results to ClickHouse `zaal.ex_call_analytics_dist`; sync daemons copy them into Postgres `coa_ex` for the panel ([A6](steps/a-store.html), [A7](steps/a-sync.html)).",
                "**Tracing (OpenTelemetry / OpenInference).** A trace is the tree of operations (spans) for one request, each with timing and attributes. OpenTelemetry is the general standard; OpenInference is its LLM flavour (spans for LLM calls, retrievers, tools, with prompts and outputs). **In EX:** aiva sends 100% of IVA traces to Phoenix project `chatbot-ex-iva`, kept 30 days ([P3](steps/p-phoenix.html)). Traces contain employee text and phone numbers, so they are also a privacy store ([M4](steps/m-stores.html)).",
                "**Metrics (Prometheus).** Numbers sampled over time (counters, gauges, histograms) scraped from `/metrics` endpoints and queried with PromQL in Grafana. Metrics tell you **how much and how fast** for a whole pool; traces tell you **why** for one request. **In EX:** vLLM and Envoy series per pool ([P4](steps/p-metrics.html)); they cannot separate EX from the other products on a shared pool. The dedicated `:8318` endpoint is the first EX-only LLM, so its metrics would be EX-only, if it is scraped.",
            ],
        )),

        # ------------------------------------------------------------------ 10
        ("How to reason about model choice for a step", (
            "Every LLM step is a trade-off between five forces. Ask them in this order, because on a phone call latency is a hard wall and privacy is a hard rule, while quality and cost are dials.",
            {"ol": [
                "**Privacy and data residency.** Does the input contain employee speech, identity or HR content? If yes, the default is in-cluster. EX has two exceptions today: Soniox (live audio) and OpenAI (greeting). Each needs explicit sign-off.",
                "**Latency budget.** Is the step on the critical path of a live turn, and is its output streamed? A non-streamed decision on the critical path must finish in a few hundred milliseconds; a streamed answer needs a low time-to-first-sentence. Offline steps (KB summarizer, CCA) can be slow.",
                "**Task difficulty and quality.** Classification and picking from a list are easy (small or MoE model); following a long rule-heavy Persian prompt with sensitive-topic rules is hard (largest model). Measure, do not guess: build a small labelled test set per step.",
                "**Cost and capacity.** Calls per turn × turns per call × concurrent calls. A call that runs on every turn and is often thrown away (clarifying) costs as much as one that is always used.",
                "**Failure behaviour.** What happens on timeout or bad output, and is the pool shared? A shared pool imports other products' load spikes into your latency; a dedicated endpoint removes that but adds a single point of failure.",
            ]},
            {"table": [
                ["Step", "Model", "Why it fits", "What it gives up"],
                ["[K7 relevance filter](steps/k-filter.html)", "[Gemma-4 E2B](models/gemma-4-e2b.html)", "Pick-from-list task, every turn, before the guardrail: must be the fastest", "Small model decides what knowledge the answer sees; fails open"],
                ["[V5 end-of-turn](steps/v-turn.html), [B4 intent](steps/b-intent.html), [B8 classify](steps/b-classify.html), [B5 clarify](steps/b-clarify.html)", "[Gemma-4 26B-A4B](models/gemma-4-26b-a4b.html)", "Needs real Persian understanding but tiny outputs; ~4B active keeps it fast", "Shared pool (11 services), spec-decode off, 8 s timeouts can stall a turn"],
                ["[B10 ReAct answer](steps/b-react.html)", "[Gemma-4 31B](models/gemma-4-31b.html) (since 2026-11-02)", "Hardest task: long Persian rule-heavy prompt, sensitive topics, no promises, KB-only", "Slower decode and prefill than A4B; 15K context if flags match the pool (unverified)"],
                ["[B7 guardrail](steps/b-guardrail.html) + [B12 refusal](steps/b-guard-reply.html)", "Gemma-4 31B (dedicated since 2026-11-02)", "Safety decision for HR: quality first", "Non-streamed and on the critical path of every turn"],
                ["[B2 greeting](steps/b-greeting.html)", "[OpenAI gpt-6-luna](models/openai-frontier.html)", "Probably wording quality of the first line (inferred)", "Leaves the cluster; no fallback except the MCI greeting"],
                ["[V4 live STT](steps/v-stt.html)", "[Soniox](models/soniox-stt.html)", "Persian streaming accuracy and latency (inferred)", "Live employee audio leaves the cluster; runs from an unmerged branch"],
                ["[K4 embeddings](steps/k-embed.html)", "[hakim-unsup](models/hakim-unsup.html)", "Small Persian encoder, cheap, 768-d", "Changing it needs a full manual re-embed"],
                ["[K2 KB summarizer](steps/k-summarize.html)", "Gemma-4 31B", "Offline admin tool, human reviews output", "Nothing important"],
            ]},
            "**Today's change, reasoned through.** Moving ReAct from 26B-A4B to 31B dense and putting both ReAct and the guardrail on a dedicated instance:",
            {"table": [
                ["Dimension", "Gain", "Cost / risk", "How to check"],
                ["Answer quality", "Better instruction-following on the long EX prompt (sensitive topics, no promises, one follow-up) (inferred)", "None, if the prompt was tuned on 31B (Phoenix lists 31B for these prompts)", "Re-run the PRD test scenarios; compare refusal and hallucination rates before/after"],
                ["Latency", "No noisy neighbours: the guardrail no longer queues behind 16 other services", "Dense 31B decodes several times slower than ~4B-active; prefill also heavier, so first-sentence time rises (inferred: a few hundred ms per turn)", "TTFT and e2e histograms on `:8318`; trace span durations for B7 and B10"],
                ["Context", "—", "If `--max-model-len` is 15K as on the pool, long calls (50 history items + 10 contexts + long system prompt) can hit HTTP 400 sooner than at 23K", "Ask SRE for the launch flags; grep logs for 400 / context length errors"],
                ["Availability", "Isolation from other products' incidents", "One upstream, no Envoy LB: if `:8318` is down, every EX turn fails (guardrail and answer together)", "Ask about health checks, restart policy and a fallback URL"],
                ["Capacity", "All GPU memory for EX", "Each turn now makes 2 calls (guardrail + answer) on one GPU server; 6 pods × 10 processes ≈ 60 concurrent calls (inferred) share it", "`vllm:num_requests_waiting` and KV-cache usage at peak hours"],
                ["Observability", "First LLM whose metrics are EX-only", "Not in the exporter target list yet (inferred), so it may be invisible in Grafana", "Look for `instance='172.23.0.17:8318'` in Prometheus"],
                ["Speed tricks", "MTP spec-decode would claw back speed", "Unknown whether `:8318` runs MTP", "`vllm:spec_decode_*` series on that instance"],
            ]},
        )),

        # ------------------------------------------------------------------ 11
        ("Worked example: one utterance, end to end", (
            "An employee has been on the line for a minute. They say: «راستش می‌خواستم بپرسم برای وام ضروری باید به کی درخواست بدم؟» (“Honestly, I wanted to ask who I should apply to for an emergency loan?”). Timings are from the end of their speech (t = 0). Configured values come from code; the model-call durations are estimates for a normally loaded system (inferred).",
            {"table": [
                ["t (s)", "Step", "Model call", "Input", "Output"],
                ["−3.0 → 0", "[V4 STT](steps/v-stt.html)", "Soniox (external), streaming", "caller audio frames via egress proxy", "interim then final Persian text"],
                ["0 → 0.5", "[V3 VAD](steps/v-vad.html)", "Silero (CPU)", "PCM frames", "end-of-speech after 0.5 s silence"],
                ["0.5 → ~0.8", "[V5 end-of-turn](steps/v-turn.html)", "Gemma-4 26B-A4B, non-streamed", "system “end-of-turn detector” + last 6 messages + latest text", "`0.94` (finished) (inferred)"],
                ["~0.8 → ~0.9", "[V6 endpointing](steps/v-endpoint.html)", "none", "turn probability", "commit near `min_delay` 0.1 s"],
                ["~0.9", "[V7 call aiva](steps/v-aiva.html)", "none", "`POST /chat/completions` stream, `session_id`", "thinking sound starts"],
                ["~0.9 → ~0.95", "[B3 setup](steps/b-setup.html)", "none", "session, ≤50 history items, memory `{}`, last turn's contexts", "one `UserInputEvent`, fan-out starts"],
                ["~0.95 → ~1.3", "[B4 intent](steps/b-intent.html)", "Gemma-4 26B-A4B, temp 0.1", "current utterance + `exit_tool` schema", "no tool call → CONTINUE"],
                ["~0.95 → …", "[B5 clarify](steps/b-clarify.html)", "Gemma-4 26B-A4B, streaming (private)", "full history + dates + memory", "a short reply, buffered; later cancelled"],
                ["~0.95 → ~1.05", "[K4/K6 embed + search](steps/k-search.html)", "hakim-unsup + Qdrant", "the utterance only", "768-d vector; up to 10 Q&A ≥ 0.25, plus guardrail policies and routing examples"],
                ["~1.05 → ~1.4", "[K7 filter](steps/k-filter.html)", "Gemma-4 E2B", "JSON: input, 15 history items, candidates (+ last turn's contexts)", "`{\"indexes\":[1,4]}`: the two loan Q&As"],
                ["~1.05 → ~1.35", "[B8 classify](steps/b-classify.html)", "Gemma-4 26B-A4B", "JSON: 10 history items, input, memory, examples", "`main`"],
                ["~1.4 → ~2.0", "[B7 guardrail](steps/b-guardrail.html)", "**Gemma-4 31B** at `:8318`, non-streamed", "conversation + 2 contexts + policies", "`1` (allowed)"],
                ["~2.0", "[B9 branch](steps/b-branch.html)", "none", "allow + CONTINUE + `main`", "clarifying stream cancelled; ReAct starts"],
                ["~2.0 → ~2.8", "[B10 ReAct](steps/b-react.html), prefill", "**Gemma-4 31B** at `:8318`, streaming", "system prompt + history + user template with `{contexts}`, dates, `{user_request}` (several thousand tokens, (inferred))", "first token"],
                ["~2.8 → ~3.4", "B10 decode", "same", "—", "first sentence ending in `\". \"`"],
                ["~3.4 → ~3.7", "[V8 TTS](steps/v-tts.html)", "neurobox `ex_prod`", "first sentence", "audio; the employee hears the answer"],
                ["after", "[K8 carry-over](steps/k-carry.html), [M1](steps/m-history.html)", "none", "filtered contexts, messages", "saved to session params and Postgres; trace in Phoenix"],
            ]},
            "**Reading the table.** About 3.5 s of silence (filled by the thinking sound) before the answer starts, of which ~0.9 s is the voice layer and the rest is the brain and TTS (inferred). The critical path is: VAD → end-of-turn → endpointing → embedding → Qdrant → E2B filter → **31B guardrail** → **31B ReAct prefill + first sentence** → TTS. Intent, classifier and clarifying run in parallel and only matter if they are slower than that chain. Before today, ReAct on 26B-A4B would likely have started speaking a few hundred milliseconds earlier (inferred); the guardrail, now on a quiet dedicated instance, may be faster than it was on the busy shared pool. Measure both in Phoenix traces.",
            {"note": "**Where it goes wrong.** If the answer has no `\". \"` in its first sentence (Persian often ends with `؟` or no period), TTS waits for the whole answer. If the E2B filter fails, all 10 candidates pass and the 31B must ignore the irrelevant ones. If `:8318` is slow, both guardrail and answer wait; the voice agent gives up after 10 s × 3 retries. If this were a goodbye, intent would emit `exit` and the call would end without the guardrail or ReAct being used.", "kind": "warn"},
            "**After hang-up** (lane 5): the agent publishes the session summary to Kafka `chatbot-mci-ex-iva` ([V13](steps/v-summary.html)); grogu merges the two `.ogg` tracks into stereo ([A2](steps/a-merge.html)), re-transcribes with k2 ASR plus emotion and gender ([A3](steps/a-asr.html)), publishes to `anzu-coa-call-ex` ([A4](steps/a-publish.html)); CCA writes tags, sentiment and a summary to ClickHouse ([A5](steps/a-cca.html)); sync daemons copy them to Postgres ([A7](steps/a-sync.html)), and HR sees the call in the EX panel minutes later (inferred) ([A9](steps/a-panel.html)).",
        )),

        # ------------------------------------------------------------------ 12
        ("Questions to ask each team", (
            "Prioritised: ask the first two per team in your first meeting. Each question points at the step where the gap is documented.",
            {"table": [
                ["Team", "Priority questions", "Why (step / risk)"],
                ["**Voice / LiveKit**", "1. When will `feat-soniox-lang` be merged into main, and who owns that? 2. Should human transfer exist in the pilot; if yes, what is `AGENT_SIP_REDIRECT_URL` and what does the employee hear if it fails? 3. Why is `AGENT_GREETING_MESSAGE` still the MCI greeting? 4. Can the TTS sentence splitter include `؟`, `!` and `،`? 5. Who tuned VAD 0.3 / endpointing 0.1–0.5 s, and on what calls? Have we measured cut-offs on emotional calls? 6. Where are LiveKit server, SIP trunk and dispatch rules managed?", "[V4](steps/v-stt.html), [V11](steps/v-end.html), [V2](steps/v-session.html), [V8](steps/v-tts.html), [V6](steps/v-endpoint.html), [V1](steps/v-ingress.html)"],
                ["**aiva (brain)**", "1. With ReAct and guardrail on `:8318`, what are the new timeouts, retries and fallback if that host is down? 2. Are the env fallback prompts fixed (the ReAct one would KeyError)? 3. What is the plan for prod 0.31.1 → main 0.33.3 and what changes for EX? 4. Is the clarifying branch worth its per-turn cost; any data on how often it wins? 5. Should `send_sms` be removed from EX? 6. What is in the shared `aiva-classification` collection?", "[B10](steps/b-react.html), [B1](steps/b-prompts.html), [B3](steps/b-setup.html), [B5](steps/b-clarify.html), [B11](steps/b-tools.html), [B8](steps/b-classify.html)"],
                ["**KB / content (HR)**", "1. Who writes and approves Q&A, and how many paraphrases per answer is the target? 2. Is there a staging KB, since edits go live within 60 s with no publish step? 3. Should the voice agent read `iva_text` (written but unused)? 4. Who maintains guardrail allow/deny examples, and which sensitive topics must they cover? 5. What should happen when no approved answer exists?", "[K1](steps/k-author.html), [K3](steps/k-sync.html), [K5](steps/k-collections.html), [B7](steps/b-guardrail.html), [K7](steps/k-filter.html)"],
                ["**COA / CCA (analytics)**", "1. Can we get the CCA repo: prompts, model, temperature, batching? 2. Is there, or will there be, an HR feedback taxonomy and a sensitive/emergency classifier with alerting? 3. Why do trends and failed-calls read MCI defaults (`cca-mci`, `unprocessed_calls_dist`)? 4. Which tables does AQA query for EX, and should EX use an external model there? 5. Who is alerted when a call stays `in_progress` or exhausts dead-letter retries?", "[A5](steps/a-cca.html), [A7](steps/a-sync.html), [A10](steps/a-aqa.html), [A1](steps/a-ingest.html)"],
                ["**SRE / platform**", "1. Launch flags of `172.23.0.17:8318`: `--max-model-len`, dtype, MTP, `max-num-seqs`, GPU type and count? 2. Is `:8318` scraped by Prometheus and behind any health check or LB? 3. Can missing exporter targets (31B `:8319`, `172.16.21.4:8315`) be fixed? 4. What is E2B's context length and where are its flags? 5. Capacity: how many concurrent EX calls can `:8318` hold at p95 TTFT < 1 s?", "[P1](steps/p-serving.html), [P4](steps/p-metrics.html)"],
                ["**Security / privacy**", "1. Is sending live employee audio to Soniox and greeting context to OpenAI approved, under what contract? 2. Retention and purge for Postgres messages, Phoenix traces (30 d, 100%), app logs with transcripts, MinIO recordings in the shared MCI bucket? 3. Should phone numbers be pseudonymised in logs and traces? 4. Can plaintext LiveKit and Redis secrets move to a secret store? 5. Who may listen to recordings, and is access logged?", "[M4](steps/m-stores.html), [V4](steps/v-stt.html), [V12](steps/v-record.html), [V1](steps/v-ingress.html)"],
                ["**HR product**", "1. Is the pilot a feedback channel, a Q&A helpdesk, or both? This sets KB scope and success metrics. 2. Should the agent remember employees across calls, given anonymity expectations? 3. What must happen with a sensitive or emergency report today, without a backend alert? 4. Is human transfer required for the pilot? 5. What AI disclosure must the greeting carry? 6. Which panel features must be hidden or rebranded from MCI?", "[M2](steps/m-longterm.html), [A5](steps/a-cca.html), [V11](steps/v-end.html), [B2](steps/b-greeting.html), [A9](steps/a-panel.html)"],
            ]},
        )),

        # ------------------------------------------------------------------ 13
        ("Hands-on exercises", (
            "Do these in order; each builds on the last. They are read-only unless stated. Anything that touches production data (recordings, traces, transcripts) needs the access you are entitled to and should be logged.",
            {"table": [
                ["#", "Exercise", "Where", "What you should learn"],
                ["1", "**Prompt inventory.** Open Prompts, filter `ex_iva_`. For each of the 13 used prompts note: latest version, tag `production` on which version, author, date. Open `ex_iva_react_agent_llm_template` and diff the last two versions.", "Phoenix UI `chatbot-phoenix.pr.mci.dev` → Prompts", "Who changes product behaviour, how often, and without code review ([B1](steps/b-prompts.html))"],
                ["2", "**Replay one call.** Tracing → project `chatbot-ex-iva` → pick one session → walk every span of one turn. Label them V7, B4, B5, K6, K7, B7, B8, B10. Read `retrieval.contexts` and the E2B output indexes. Check that the B7 and B10 spans show `gemma-4-31B` (post-change).", "Phoenix → Tracing", "What each model actually received and returned; which span is slowest ([P3](steps/p-phoenix.html))"],
                ["3", "**Find the turn budget.** In the same trace, sum the critical-path spans and compare with the worked example table. Do it for 5 turns, one before and one after 2026-11-02.", "Phoenix → Tracing", "Real numbers for the 31B trade-off"],
                ["4", "**Pool health.** Run the PromQL below in Grafana Explore for the 26B pool, the E2B pool and `:8318`.", "Grafana / Prometheus", "Queueing, TTFT, KV-cache pressure, spec-decode benefit ([P4](steps/p-metrics.html))"],
                ["5", "**Read the config.** In `chatbot-ops/prod/chatbot-ex/values.yaml`, find: `AGENT_LLM_BASE_URL` / `AGENT_LLM_MODEL` and `GUARDRAIL_LLM_BASE_URL` / `GUARDRAIL_LLM_MODEL` (now pointing at `:8318`, (inferred) variable names), `CONTEXT_RETRIEVE_THRESHOLD`, the `AGENT_VAD_*` block around line 3090–3110, `USE_PHOENIX_PROMPTS`, `OTEL_TRACES_SAMPLER_ARG`. Confirm `AGENT_SIP_REDIRECT_URL` is absent.", "git, `chatbot-ops` (prod branch)", "Map every setting on this site to its line; spot drift"],
                ["6", "**KB change and sync.** On a staging KB if one exists (otherwise an inactive or time-windowed test item agreed with HR): add a Q&A with 3 paraphrases. Watch `qdrant_last_sync` update within ~60 s, then ask the question on a test call and find the context in the trace. Then deactivate it and confirm it disappears.", "KB API / panel, Phoenix", "Edits are live in a minute; paraphrase coverage decides recall ([K3](steps/k-sync.html))"],
                ["7", "**Miss on purpose.** Ask 5 questions the KB does not cover and 5 paraphrases of covered ones. Record: retrieved count, E2B kept indexes, guardrail result, what the agent said.", "test call + Phoenix", "Whether grounding holds when retrieval is empty or noisy ([K7](steps/k-filter.html))"],
                ["8", "**Listen to a call.** Find the track paths in the Kafka summary or the coa call record: `s3://chatbot-mci-iva/chatbot-ex-iva-prod/<track_id>.ogg` (two tracks) and the merged WAV under `coa-analysis-prod/ex/prod/voices`. Listen to a test call; compare with the live transcript (Postgres messages) and the k2 transcript in the panel.", "MinIO (with approval), EX panel", "Live vs offline ASR differences; whether the greeting start is clipped ([V12](steps/v-record.html), [A3](steps/a-asr.html))"],
                ["9", "**Follow a call to the panel.** Note one call id; find it in `calls` / `call_ai_tags` (status), then in the panel. Time each hop.", "Postgres `coa_ex` (read-only), EX panel", "Where analytics can stall ([A1](steps/a-ingest.html), [A7](steps/a-sync.html))"],
                ["10", "**Run the PRD scenarios.** Pick 10 scenarios from the PRD test section (sensitive topic, angry employee, request for a promise about pay, goodbye) and score them with the PRD rubric.", "test calls + [PRD](" + PRD + ")", "Pilot readiness evidence"],
            ]},
            "**PromQL for exercise 4.** Replace the instance with the pool's upstreams; the dedicated endpoint is `172.23.0.17:8318` if SRE scrapes it. Metric names are vLLM's standard Prometheus series; label names can differ per scrape config (check with `{__name__=~'vllm:.*'}` first).",
            {"code": "# p95 time-to-first-token per vLLM instance (5-minute window)\n"
                     "histogram_quantile(0.95, sum by (le, instance) (rate(vllm:time_to_first_token_seconds_bucket[5m])))\n\n"
                     "# p95 end-to-end request latency on the new dedicated EX 31B endpoint\n"
                     "histogram_quantile(0.95, sum by (le) (rate(vllm:e2e_request_latency_seconds_bucket{instance='172.23.0.17:8318'}[5m])))\n\n"
                     "# decode speed: generated tokens per second, and mean time per output token\n"
                     "sum by (instance) (rate(vllm:generation_tokens_total[5m]))\n"
                     "rate(vllm:time_per_output_token_seconds_sum[5m]) / rate(vllm:time_per_output_token_seconds_count[5m])\n\n"
                     "# average prompt size (tokens per request): watch it approach --max-model-len\n"
                     "sum by (instance) (rate(vllm:prompt_tokens_total[5m])) / sum by (instance) (rate(vllm:request_success_total[5m]))\n\n"
                     "# answers cut by the token limit\n"
                     "sum by (instance) (rate(vllm:request_success_total{finished_reason='length'}[1h]))\n\n"
                     "# queueing and KV-cache pressure\n"
                     "max by (instance) (vllm:num_requests_waiting)\n"
                     "max by (instance) (vllm:gpu_cache_usage_perc)   # newer vLLM: vllm:kv_cache_usage_perc\n\n"
                     "# speculative decoding acceptance rate (MTP)\n"
                     "rate(vllm:spec_decode_num_accepted_tokens_total[5m]) / rate(vllm:spec_decode_num_draft_tokens_total[5m])\n\n"
                     "# Envoy: p95 upstream latency per LB pool, and 5xx rate\n"
                     "histogram_quantile(0.95, sum by (le, envoy_cluster_name) (rate(envoy_cluster_upstream_rq_time_bucket[5m])))\n"
                     "sum by (envoy_cluster_name) (rate(envoy_cluster_upstream_rq_xx{envoy_response_code_class='5'}[5m]))\n"
                     "# healthy upstreams per pool (bare-metal hosts dropping out)\n"
                     "min by (envoy_cluster_name) (envoy_cluster_membership_healthy)"},
            {"note": "Envoy's `envoy_cluster_upstream_rq_time` is in milliseconds; vLLM histograms are in seconds. On shared pools these numbers mix EX with other products; only `:8318` is EX-only. The aiva counter `guardrail_results_total{allowed}` would give the guardrail deny rate, if aiva's metrics are scraped (inferred).", "kind": ""},
        )),

        # ------------------------------------------------------------------ 14
        ("Decision checklist and red flags for the HR pilot", (
            "Use this as the agenda for the go/no-go review. A red flag is not automatically a blocker, but each one needs an explicit owner and decision in writing. Details and severity are on [Risks & gaps](risks.html).",
            {"table": [
                ["Area", "Check before pilot", "Red flag today", "Step"],
                ["Privacy: data leaving the cluster", "Written approval for Soniox (live audio) and OpenAI (greeting context), or an in-house replacement", "Both external with no recorded decision", "[V4](steps/v-stt.html), [B2](steps/b-greeting.html)"],
                ["Privacy: retention and access", "Retention, purge and access policy for Postgres messages, Phoenix traces, logs, recordings, analytics", "No retention job anywhere; transcripts in INFO logs; recordings in the shared MCI bucket", "[M4](steps/m-stores.html), [V12](steps/v-record.html)"],
                ["Privacy: identity", "Decision on pseudonymising phone numbers and on per-employee memory", "Phone + memory in every trace and log line; memory read path live, write path absent", "[M2](steps/m-longterm.html), [M3](steps/m-writer.html)"],
                ["Grounding", "Measured answer accuracy on in-KB and out-of-KB questions; a policy for “no approved answer”", "Threshold 0.25 + fail-open E2B filter; refusal is prompt-only", "[K6](steps/k-search.html), [K7](steps/k-filter.html)"],
                ["Sensitive topics", "A defined path for harassment, safety, self-harm or legal reports: what the bot says, who is alerted, how fast", "No sensitive classifier or alerting; the prompt assumes a backend that does not exist", "[A5](steps/a-cca.html), [B10](steps/b-react.html)"],
                ["Transfer", "Either a working human hand-off or a scripted alternative (call-back, number)", "Transfer always fails and drops the call", "[V11](steps/v-end.html)"],
                ["Branding", "Every caller-facing and panel string is EX, not MCI", "MCI greeting fallback; MCI trends and NL2SQL data may appear in the EX panel", "[V2](steps/v-session.html), [A7](steps/a-sync.html), [A10](steps/a-aqa.html)"],
                ["Change control", "Prompt edits in Phoenix go through review; deploys come from main", "Prompts change without review; voice agent from an unmerged branch; env fallback prompts broken", "[B1](steps/b-prompts.html), [P3](steps/p-phoenix.html)"],
                ["Reliability of today's change", "Known flags, health check, alerting and a fallback for `:8318`", "Single bare-metal host for both guardrail and answer", "[P1](steps/p-serving.html), [B7](steps/b-guardrail.html)"],
                ["Latency", "p95 first-audio time measured on real calls and accepted by HR", "No end-to-end latency metric; parts are estimates", "[V6](steps/v-endpoint.html), [P4](steps/p-metrics.html)"],
                ["Analytics trust", "CCA prompts/models reviewable; HR category tree agreed", "CCA is a black box with call-centre tags", "[A5](steps/a-cca.html)"],
            ]},
            {"note": "**Never claim** to HR that feedback is “recorded” or “escalated” unless a system event confirms it. The PRD forbids it, and aiva has no such event today. The same applies to anonymity: calls are keyed by phone number end to end.", "kind": "bad"},
        )),

        # ------------------------------------------------------------------ 15
        ("Glossary", (
            {"table": [
                ["Term", "One-line definition", "See"],
                ["Active parameters", "The parameters an MoE model actually uses per token; they set decode speed", "[Gemma-4 26B-A4B](models/gemma-4-26b-a4b.html)"],
                ["aiva", "The EX brain service (`iva-chatbot`) that orchestrates all per-turn agents", "[lane 2](index.html#lane-brain)"],
                ["At-least-once", "Delivery where messages may repeat but are never lost; consumers must be idempotent", "[A1](steps/a-ingest.html)"],
                ["AxonHub", "LLM gateway mapping aliases to models, routing kept in a database", "[P2](steps/p-gateway.html)"],
                ["Barge-in", "The caller interrupting the agent's speech", "[V9](steps/v-bargein.html)"],
                ["CCA", "External LLM engine that tags each call (sentiment, category, summary)", "[A5](steps/a-cca.html)"],
                ["ClickHouse", "Columnar analytics database holding CCA results", "[A6](steps/a-store.html)"],
                ["COA", "The call-analytics application and API behind the EX panel", "[A8](steps/a-api.html)"],
                ["Context window", "Maximum tokens per request; set in practice by `--max-model-len`", "[P1](steps/p-serving.html)"],
                ["Continuous batching", "vLLM's per-step batching of many requests on one GPU", "[P1](steps/p-serving.html)"],
                ["Cosine similarity", "Closeness of two vectors, 1 = same direction", "[K6](steps/k-search.html)"],
                ["Dead letter", "A failed message parked for later retry", "[A1](steps/a-ingest.html)"],
                ["Dense model", "A model that uses all its parameters for every token", "[Gemma-4 31B](models/gemma-4-31b.html)"],
                ["E2B (effective 2B)", "Gemma variant with ~2B compute parameters plus per-layer embeddings", "[Gemma-4 E2B](models/gemma-4-e2b.html)"],
                ["Embedding", "A vector representing a text's meaning", "[K4](steps/k-embed.html)"],
                ["End-of-turn detection", "Deciding the speaker has finished, not just paused", "[V5](steps/v-turn.html)"],
                ["Endpointing", "The wait before committing a turn", "[V6](steps/v-endpoint.html)"],
                ["Envoy", "The load balancer in front of each model pool", "[P1](steps/p-serving.html)"],
                ["EX", "Employee Experience / صدای کارکنان, the HR pilot", "[map](index.html)"],
                ["Fail-open / fail-closed", "On error, let the request through / block it", "[B7](steps/b-guardrail.html)"],
                ["grogu", "Go service that ingests finished calls, merges audio, re-transcribes and publishes", "[A1](steps/a-ingest.html)"],
                ["Guardrail", "A check that allows or denies a request", "[B7](steps/b-guardrail.html)"],
                ["Hakim", "MCI's in-house Persian embedding model family", "[hakim-unsup](models/hakim-unsup.html)"],
                ["Intent detection", "Classifying what the user wants to do (here: exit or continue)", "[B4](steps/b-intent.html)"],
                ["k2 ASR", "In-house offline speech recognition used for analytics", "[k2 ASR](models/neurobox-asr.html)"],
                ["Kafka", "Durable message log between the call and analytics", "[V13](steps/v-summary.html)"],
                ["KV cache", "GPU memory holding per-token state of running requests", "[P1](steps/p-serving.html)"],
                ["LiveKit", "The real-time audio platform that hosts each call", "[V1](steps/v-ingress.html)"],
                ["MAX_SIM", "Multivector score = best similarity over an answer's questions", "[K5](steps/k-collections.html)"],
                ["max-model-len", "vLLM flag fixing the deployed context window (15K / 23K here)", "[P1](steps/p-serving.html)"],
                ["MoE", "Mixture-of-Experts: only a few expert sub-networks run per token", "[models](models.html)"],
                ["MTP / speculative decoding", "A draft proposes tokens, the big model verifies several at once", "[P1](steps/p-serving.html)"],
                ["OpenInference", "LLM-specific tracing conventions on top of OpenTelemetry", "[P3](steps/p-phoenix.html)"],
                ["Phoenix (Arize)", "Prompt registry and tracing UI for EX", "[P3](steps/p-phoenix.html)"],
                ["Prefill / decode", "Reading the prompt (parallel) / writing tokens one by one", "[B10](steps/b-react.html)"],
                ["Prometheus / PromQL", "Metrics store and its query language", "[P4](steps/p-metrics.html)"],
                ["Qdrant", "The vector database holding KB, guardrail and routing vectors", "[K5](steps/k-collections.html)"],
                ["Quantization", "Storing weights at lower precision to save memory and time", "[models](models.html)"],
                ["RAG", "Retrieve approved text and answer only from it", "[lane 3](index.html#lane-kb)"],
                ["ReAct", "Agent loop of reasoning and tool calls until an answer", "[B10](steps/b-react.html)"],
                ["Relevance filter", "An LLM that keeps only relevant retrieved items", "[K7](steps/k-filter.html)"],
                ["Reranker", "A model that scores and re-orders retrieved items", "[K7](steps/k-filter.html)"],
                ["Silero VAD", "Tiny CPU model detecting speech vs silence", "[Silero VAD](models/silero-vad.html)"],
                ["Soniox", "External streaming speech-to-text service used live", "[Soniox](models/soniox-stt.html)"],
                ["Speculative branch", "An answer started early and cancelled if not chosen", "[B9](steps/b-branch.html)"],
                ["STT / ASR", "Speech-to-text / automatic speech recognition", "[V4](steps/v-stt.html)"],
                ["Temperature", "Randomness of generation; 0 = repeatable", "[B4](steps/b-intent.html)"],
                ["Threshold / top-k", "Minimum similarity / maximum number of retrieved items", "[K6](steps/k-search.html)"],
                ["Token", "The unit of text a model reads and writes", "[P4](steps/p-metrics.html)"],
                ["Tool calling", "The model emitting a structured function call instead of text", "[B11](steps/b-tools.html)"],
                ["TTFT", "Time to first token: queue + prefill", "[B10](steps/b-react.html)"],
                ["TTS", "Text-to-speech", "[neurobox TTS](models/neurobox-tts.html)"],
                ["vLLM", "The inference server running every in-house model", "[P1](steps/p-serving.html)"],
                ["Voice bridge", "A generated filler sentence while the answer is prepared (off in EX)", "[B13](steps/b-voicebridge.html)"],
                ["WER", "Word error rate of speech recognition", "[A3](steps/a-asr.html)"],
            ]},
        )),
    ],
}
