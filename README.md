# documents/ — map

Technical-PM workspace for two projects plus supporting material. The project registry is the entry point for
Claude and Codex: [`PROJECTS_REGISTRY.md`](PROJECTS_REGISTRY.md) (their global config points to this exact path, so it stays at the root).

| Folder | What | Start with |
|---|---|---|
| [`hr-ex-phoenix/`](hr-ex-phoenix/) | **HR / EX (Phoenix)**: product docs, technical docs, the clickable pipeline map, KB content, requirements, diagrams | [`hr-ex-phoenix/README.md`](hr-ex-phoenix/README.md) → folder map |
| [`chat-hub-product/`](chat-hub-product/) | **LLM Hub / Chat Hub** product docs (not the call-center chatbot) | [`CHAT_HUB_PROJECT_CONTEXT_FA.md`](chat-hub-product/CHAT_HUB_PROJECT_CONTEXT_FA.md) |
| [`project-proposals/`](project-proposals/) | Proposed projects, one Word file each | [`README.md`](project-proposals/README.md) |

Quick finds:

- **Understand the EX / Phoenix pipelines and every model** → `hr-ex-phoenix/technical/phoenix-pipelines/en/index.html` (Persian: `fa/`)
- **TPM learning guide** → `hr-ex-phoenix/technical/phoenix-pipelines/en/guide.html`
- **EX agent requirements (PRD)** → `hr-ex-phoenix/product-management/IVA_EX_PROMPT_REQUIREMENTS_FA.html`
- **Knowledge-base content and imports** → `hr-ex-phoenix/knowledge-base/`
- **Project context for an AI assistant** → `hr-ex-phoenix/HR_PROJECT_CONTEXT_FA.md`, `hr-ex-phoenix/COA_PROJECT_CONTEXT_FA.md`, `chat-hub-product/CHAT_HUB_PROJECT_CONTEXT_FA.md`

Conventions: folders `kebab-case`; one folder per project; each project folder has a `README.md` and its context file at its root;
generated documents are `UPPER_SNAKE` (`_FA` = Persian) and are rebuilt from `source/`, never edited by hand.
