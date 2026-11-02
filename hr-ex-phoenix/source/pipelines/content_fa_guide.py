"""Persian learning guide for the Phoenix EX pipeline site (translation of content_en_guide.py).

Split in three part files to keep each file small; this module assembles GUIDE.
State reflects prod on 2026-11-02.
"""

from content_fa_guide_p1 import SECTIONS1, AI_GUIDE, PRD  # noqa: F401
from content_fa_guide_p2 import SECTIONS2
from content_fa_guide_p3 import SECTIONS3

GUIDE = {
    "title": "راهنمای یادگیری: تسلط بر Phoenix EX",
    "lede": "مسیر مطالعه برای یک مدیر محصول فنی (TPM) که باید مالک عامل صوتی صدای کارکنان (Employee Voice) باشد و با همهٔ تیم‌های پشت آن با اطمینان صحبت کند. هر مفهوم از صفر توضیح داده می‌شود و سپس به همان گام، مدل و تنظیمی گره می‌خورد که در EX ظاهر می‌شود. آن را کنار [نقشهٔ خط لوله](index.html) بخوانید؛ دورهٔ عمومی هوش مصنوعی را که در [راهنمای یادگیری هوش مصنوعی (فارسی)](" + AI_GUIDE + ") آمده تکرار نمی‌کند.",
    "sections": SECTIONS1 + SECTIONS2 + SECTIONS3,
}
