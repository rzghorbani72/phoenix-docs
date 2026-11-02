# documents/ — map

Technical-PM workspace for two projects plus supporting material. The project registry is the entry point for
Claude and Codex: [`PROJECTS_REGISTRY.md`](PROJECTS_REGISTRY.md) (their global config points to this exact path, so it stays at the root).

| Folder | What | Start with |
|---|---|---|
| [`hr-ex-phoenix/`](hr-ex-phoenix/) | **HR / EX (Phoenix)** as a React app: interactive pipeline map, models, guide, risks, plus all product/technical docs, KB content, requirements and diagrams under `public/docs/` | [`hr-ex-phoenix/README.md`](hr-ex-phoenix/README.md) → folder map |
| [`chat-hub-product/`](chat-hub-product/) | **LLM Hub / Chat Hub** product docs (not the call-center chatbot) | [`CHAT_HUB_PROJECT_CONTEXT_FA.md`](chat-hub-product/CHAT_HUB_PROJECT_CONTEXT_FA.md) |
| [`project-proposals/`](project-proposals/) | Proposed projects, one Word file each | [`README.md`](project-proposals/README.md) |

Quick finds:

- **Interactive app: pipelines, every model, TPM guide, risks, all documents (start here)** → `cd hr-ex-phoenix && npm install && npm run dev` (EN/FA toggle inside)
- **EX agent requirements (PRD)** → `hr-ex-phoenix/public/docs/product-management/IVA_EX_PROMPT_REQUIREMENTS_FA.html`
- **Knowledge-base content and imports** → `hr-ex-phoenix/public/docs/knowledge-base/`
- **Project context for an AI assistant** → `hr-ex-phoenix/HR_PROJECT_CONTEXT_FA.md`, `hr-ex-phoenix/COA_PROJECT_CONTEXT_FA.md`, `chat-hub-product/CHAT_HUB_PROJECT_CONTEXT_FA.md`

Conventions: folders `kebab-case`; one folder per project; each project folder has a `README.md` and its context file at its root;
generated documents are `UPPER_SNAKE` (`_FA` = Persian) and are rebuilt from their sources (`hr-ex-phoenix/scripts/docs/`, `hr-ex-phoenix/content/`), never edited by hand.
