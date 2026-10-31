#!/usr/bin/env bash
# Rebuild every document in product/ from the sources in this folder.
# Each document is published twice: a dark-themed standalone HTML page and its PDF.
set -euo pipefail
cd "$(dirname "$0")"
pdf() { google-chrome --headless=new --no-sandbox --no-pdf-header-footer \
  --print-to-pdf="$2" "file://$PWD/$1" 2>/dev/null; }

python3 build_xlsx.py        # product-management/FIT_GAP_TRACKER.xlsx + fit_gap_tracker_fa.html
python3 build_feature_catalog.py  # FEATURE_CATALOG(.md|_FA.md) -> feature_catalog(_fa).html (the .md files stay the source)
python3 apply_theme.py       # inline theme/phoenix_fa.{css,js} into every HTML source

PM=../product-management
TECH=../technical
publish() {  # source.html  dest-dir  NAME  [pdf]
  cp "$1" "$2/$3.html"
  if [ "${4:-}" = pdf ]; then pdf "$1" "$2/$3.pdf"; fi
}
publish product_dossier_fa.html   "$PM"   PRODUCT_DOSSIER_FA   pdf
publish roadmap_fa.html           "$PM"   ROADMAP_FA           pdf
publish answer_pack_fa.html       "$PM"   ANSWER_PACK_FA       pdf
publish fit_gap_tracker_fa.html   "$PM"   FIT_GAP_TRACKER_FA
publish inspiration_playbook_fa.html "$PM" INSPIRATION_PLAYBOOK_FA pdf
publish market_alignment_fa.html  "$PM"   MARKET_ALIGNMENT_FA  pdf
publish ai_learning_guide_fa.html "$PM"   AI_LEARNING_GUIDE_FA pdf
publish iva_ex_prompt_requirements_fa.html "$PM" IVA_EX_PROMPT_REQUIREMENTS_FA pdf
publish feature_catalog.html      "$PM"   FEATURE_CATALOG
publish feature_catalog_fa.html   "$PM"   FEATURE_CATALOG_FA
publish technical_dossier_fa.html "$TECH" TECHNICAL_DOSSIER_FA pdf
echo "done"
