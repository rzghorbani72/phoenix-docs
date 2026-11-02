"""Persian model catalog: card list and overview sections plus the 22 model pages (split across part files)."""

from content_fa_models_a import PAGES as _PAGES_A
from content_fa_models_b import PAGES as _PAGES_B
from content_fa_models_meta import MODELS_META

MODELS = dict(MODELS_META, pages={**_PAGES_A, **_PAGES_B})
