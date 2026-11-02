# knowledge-base/ — EX knowledge-base content and import files

Content for the EX (Employee Voice) agent's knowledge base. The KB is curated Q&A, loaded through the
KB API or a CSV import with the columns
`questions, questions_as_suggestion, answer_text, answer_iva_text, answer_type, start_time, end_time, is_active, tags`
(see lane 3, “Knowledge base”, of the pipeline map in the app: `npm run dev` in `hr-ex-phoenix/`, then `#/map/lane/kb`).

| Folder | What it holds |
|---|---|
| `MCINEXT_Employee_Voice_v2_Package/` | The customer package: `Employee_Voice_Agent_Instruction_v2` (csv + docx) and `Employee_Voice_Knowledge_Base_v2.docx` |
| `sensitive-emergency-v1/` | Our sensitive / emergency voice taxonomy: `taxonomy_v1.csv`, `detector_keywords_v1.csv`, `default_features_v1.csv`, `incident_config_v1.json`, `kb_import_v1.csv`, and `README_FA.md` explaining them |
| `tones/` | Behavior codes and tone material: tones (`T08` colloquial), question sets, tone samples |
| `imports/` | Ready-to-import KB CSVs: `ex_results_1405_kb.csv` (EX survey results 1405), `merged_revised_kb.csv` (merged and revised KB, 930 lines), `instruction_14-05.csv` (21,311 lines of telecom customer-service Q&A; origin not documented, so verify before using for EX) |
