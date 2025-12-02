# sitecustomize.py — auto-imported if on sys.path
# Force Pillow to use a real TTF (not the tiny bitmap) and upsize small requests.
import os
from PIL import ImageFont as _ImageFont

# Env knobs (safe defaults)
_FALLBACK = os.getenv("BARCODE_FONT_PATH", "/usr/share/fonts/liberation/LiberationSans-Regular.ttf")
_SCALE    = float(os.getenv("BARCODE_FONT_SCALE", "1.6"))            # multiply requested sizes
_DEFAULT_PX = max(10, int(float(os.getenv("BARCODE_LOAD_DEFAULT_PX", "28"))))  # size when code calls load_default()

# Keep originals
_orig_truetype = _ImageFont.truetype
_orig_load_default = _ImageFont.load_default

def _try(path, size, *a, **k):
    try:
        return _orig_truetype(path, size, *a, **k)
    except Exception:
        return None

def _select(size):
    # pick a usable font at a readable size
    size = max(10, int(round(size * _SCALE)))
    ft = _try(_FALLBACK, size)
    if ft:
        return ft
    base, ext = os.path.splitext(_FALLBACK)
    ft = _try(f"{base}-Bold{ext}", size)
    return ft or _orig_load_default()

def _truetype_with_fallback(font, size, *a, **k):
    # honor the requested face if available; otherwise use our fallback
    size = max(10, int(round(size * _SCALE)))
    try:
        return _orig_truetype(font, size, *a, **k)
    except Exception:
        return _select(size)

def _load_default_override(*a, **k):
    # when code calls load_default(), return a real TTF at a sane size
    return _select(_DEFAULT_PX)

# Patch Pillow globally
_ImageFont.truetype = _truetype_with_fallback
_ImageFont.load_default = _load_default_override
