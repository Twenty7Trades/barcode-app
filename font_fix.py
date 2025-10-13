def _load_font(size):
    # Try Amazon Linux fonts first
    font_paths = [
        # Amazon Linux fonts
        "/usr/share/fonts/urw-base35/C059-Roman.otf",
        "/usr/share/fonts/urw-base35/URWGothic-Book.otf",
        "/usr/share/fonts/urw-base35/URWBookman-Light.otf",
        # Fallback Linux fonts
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size=size)
            except (OSError, IOError):
                continue
    
    # Fallback to default font with explicit size
    try:
        return ImageFont.load_default()
    except:
        # Last resort - create a basic font
        return ImageFont.load_default()


