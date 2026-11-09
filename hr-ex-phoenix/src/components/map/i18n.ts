/** UI strings used only by the map, its toolbar, overview and tour (EN / FA). */
const EN = {
  overview: "Overview", detail: "Detail", mode: "Map level",
  pickInstance: "Instance", allInstances: "All instances", openInstance: "Open instance",
  highlightModel: "Highlight steps by model…", filterSteps: "Filter steps…",
  status: "Status", handoffs: "Hand-offs", handoffsTitle: "Show every cross-lane hand-off (otherwise only those of the open step's lane)",
  fit: "Fit everything", laneJump: "Jump to lane",
  tour: "Follow one turn", tourTitle: "Guided tour: the path of one employee utterance through the system",
  legend: "Legend", exportPng: "Export PNG", exportTitle: "Download the current view as a PNG image", exporting: "Exporting…",
  exportFailed: "Export failed", filters: "Filters", more: "More",
  steps: "steps", models: "models", risks: "risks", high: "high", openLane: "Open lane", handoffsOut: "Hands off to",
  legendStatus: "Step status", legendLanes: "Lanes", legendEdges: "Lines and marks",
  edgeLane: "Next step inside a lane", edgeCross: "Hand-off between lanes (dashed, animated); hover to highlight",
  dimmed: "Faded box: filtered out", glow: "Glowing box: matches the model or text filter",
  enTag: "EN tag: not translated yet, shown in English",
  tourStep: "Stop", tourOf: "of", prev: "Back", next: "Next", finish: "Finish", stop: "Exit tour",
  keys: "← → move along the lane · Esc close", tourKeys: "← → move · Esc exit",
  expand: "Expand", collapse: "Collapse", close: "Close",
};
type Strings = typeof EN;
const FA: Strings = {
  overview: "نمای کلی", detail: "جزئیات", mode: "سطح نقشه",
  pickInstance: "نمونه", allInstances: "همهٔ نمونه‌ها", openInstance: "باز کردن نمونه",
  highlightModel: "برجسته‌سازی بر اساس مدل…", filterSteps: "فیلتر گام‌ها…",
  status: "وضعیت", handoffs: "تحویل‌ها", handoffsTitle: "نمایش همهٔ تحویل‌های بین مسیرها (در غیر این صورت فقط مسیرِ گام باز)",
  fit: "نمای کامل", laneJump: "رفتن به مسیر",
  tour: "دنبال کردن یک نوبت", tourTitle: "تور راهنما: مسیر یک گفتهٔ کارمند در سامانه",
  legend: "راهنما", exportPng: "خروجی PNG", exportTitle: "دریافت نمای فعلی به‌صورت تصویر PNG", exporting: "در حال ساخت…",
  exportFailed: "ساخت تصویر ناموفق بود", filters: "فیلترها", more: "بیشتر",
  steps: "گام", models: "مدل", risks: "ریسک", high: "بالا", openLane: "باز کردن مسیر", handoffsOut: "تحویل به",
  legendStatus: "وضعیت گام", legendLanes: "مسیرها", legendEdges: "خط‌ها و نشانه‌ها",
  edgeLane: "گام بعدی درون یک مسیر", edgeCross: "تحویل بین مسیرها (خط‌چین متحرک)؛ با نگه داشتن نشانگر برجسته می‌شود",
  dimmed: "کادر کم‌رنگ: با فیلتر حذف شده", glow: "کادر درخشان: با مدل یا متن فیلتر منطبق است",
  enTag: "برچسب EN: هنوز ترجمه نشده و انگلیسی نمایش داده می‌شود",
  tourStep: "ایستگاه", tourOf: "از", prev: "قبلی", next: "بعدی", finish: "پایان", stop: "خروج از تور",
  keys: "← → حرکت در مسیر · Esc بستن", tourKeys: "← → حرکت · Esc خروج",
  expand: "بزرگ کردن", collapse: "کوچک کردن", close: "بستن",
};

export const T = (lang: "en" | "fa"): Strings => (lang === "fa" ? FA : EN);
