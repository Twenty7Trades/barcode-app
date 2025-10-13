import math
import os
import pandas as pd
import pdfplumber
from PIL import Image, ImageDraw, ImageFont
from barcode import Code128
from barcode.writer import ImageWriter
from typing import Union


# ---------------- UPC-A encoding ----------------

L_CODES = {
    '0': '0001101','1': '0011001','2': '0010011','3': '0111101','4': '0100011',
    '5': '0110001','6': '0101111','7': '0111011','8': '0110111','9': '0001011',
}
R_CODES = {
    '0': '1110010','1': '1100110','2': '1101100','3': '1000010','4': '1011100',
    '5': '1001110','6': '1010000','7': '1000100','8': '1001000','9': '1110100',
}


def upc_check_digit(upc11: str) -> str:
    digits = [int(d) for d in upc11]
    odd_sum = sum(digits[0::2])
    even_sum = sum(digits[1::2])
    total = odd_sum * 3 + even_sum
    return str((10 - total % 10) % 10)


def encode_upc(upc12: str) -> str:
    start_guard = '101'
    center_guard = '01010'
    end_guard = '101'
    left = upc12[:6]
    right = upc12[6:]
    left_encoded = ''.join(L_CODES[d] for d in left)
    right_encoded = ''.join(R_CODES[d] for d in right)
    return start_guard + left_encoded + center_guard + right_encoded + end_guard


def _load_font(size):
    # Prioritize Amazon Linux fonts first
    font_paths = [
        # Amazon Linux fonts (prioritized)
        "/usr/share/fonts/google-droid-sans-fonts/DroidSans.ttf",
        "/usr/share/fonts/google-droid-sans-fonts/DroidSans-Regular.ttf",
        "/usr/share/fonts/google-noto-vf/NotoSans-VF.ttf",
        "/usr/share/fonts/google-noto-vf/NotoSans-Regular.ttf",
        "/usr/share/fonts/nimbus-sans/NimbusSans-Regular.ttf",
        # Other Linux fonts
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        # macOS system fonts (fallback)
        "/System/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SF-Pro-Text-Regular.otf",
        "/System/Library/Fonts/SF-Pro-Display-Regular.otf",
        "/Library/Fonts/Arial.ttf",
        "/Library/Fonts/Helvetica.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size=size)
            except (OSError, IOError):
                continue
    
    # Fallback to default font - but this should never happen on AWS
    try:
        return ImageFont.load_default()
    except:
        # Last resort - create a basic font
        return ImageFont.load_default()


def render_label(
    title: str,
    sku: str,
    color: str,
    upc_input: str,
    out_path: str,
    include_price: bool = False,
    price_value: Union[str, None] = None,
    canvas_w: int = 1400,
    canvas_h: int = 900,
    margin: int = 80
):
    # Build UPC-12 robustly from 11 or 12 digits
    digits = ''.join(c for c in str(upc_input) if c.isdigit())
    if len(digits) == 11:
        upc12 = digits + upc_check_digit(digits)
    elif len(digits) == 12:
        upc12 = digits
    else:
        raise ValueError(f"UPC must have 11 or 12 digits, got '{upc_input}'")
    pattern = encode_upc(upc12)

    # Canvas
    img = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(img)

    # Fonts - balanced sizes for readability and fit
    title_font = _load_font(100)
    line2_font = _load_font(85)
    digits_font = _load_font(75)

    # Line 1: Title centered
    title_txt = (title or "").strip().upper()
    title_w = draw.textbbox((0, 0), title_txt, font=title_font)[2]
    draw.text(((canvas_w - title_w) // 2, margin), title_txt, font=title_font, fill="black")

    # Line 2: SKU left, color right
    sku_txt = (sku or "").strip()
    color_txt = (color or "").strip().upper()
    line2_y = margin + 110  # Reduced from 130
    draw.text((margin, line2_y), sku_txt, font=line2_font, fill="black")
    color_w = draw.textbbox((0, 0), color_txt, font=line2_font)[2]
    draw.text((canvas_w - margin - color_w, line2_y), color_txt, font=line2_font, fill="black")

    # Barcode area - adjusted for price space
    bar_top = line2_y + 100  # Reduced from 120
    bar_bottom = canvas_h - 220  # Increased bottom margin from 180 to 220
    bar_height = bar_bottom - bar_top

    modules = len(pattern)  # 95
    module_w = int(max(1, math.floor((canvas_w - 2 * margin) / modules)))
    total_w = module_w * modules
    x0 = (canvas_w - total_w) // 2

    guard_extra = int(bar_height * 0.12)

    for i, bit in enumerate(pattern):
        if bit == '1':
            is_guard = (i < 3) or (45 <= i < 50) or (modules - 3 <= i < modules)
            top = bar_top
            bottom = bar_bottom + (guard_extra if is_guard else 0)
            draw.rectangle([x0 + i * module_w, top, x0 + (i + 1) * module_w - 1, bottom], fill="black")

    # Human-readable digits centered
    hr = f"{upc12[0]}  {upc12[1:6]}  {upc12[6:11]}  {upc12[11]}"
    hr_w = draw.textbbox((0, 0), hr, font=digits_font)[2]
    digits_y = bar_bottom + guard_extra + 10
    draw.text(((canvas_w - hr_w) // 2, digits_y), hr, font=digits_font, fill="black")

    # Optional price line: only if explicitly requested and provided
    if include_price and price_value:
        price_txt = str(price_value).strip()
        pv_w = draw.textbbox((0, 0), price_txt, font=digits_font)[2]
        price_y = digits_y + 80  # Reduced from 90 to fit better
        draw.text(((canvas_w - pv_w) // 2, price_y), price_txt, font=digits_font, fill="black")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    return upc12, out_path


def render_hot_market_label(
    col_j: str,
    col_c: str,
    col_b: str,
    col_a: str,
    col_e: str,
    upc_input: str,
    out_path: str,
    canvas_w: int = 1400,
    canvas_h: int = 900,
    margin: int = 40
):
    """
    Render Hot Market format label:
    - Row 1: Left (Column J) + Right (Column C)
    - Row 2: Column B
    - Row 3: Column A - Column E
    - UPC-A barcode at bottom (no price)
    """
    # Build UPC-12 robustly from 11 or 12 digits
    digits = ''.join(c for c in str(upc_input) if c.isdigit())
    if len(digits) == 11:
        upc12 = digits + upc_check_digit(digits)
    elif len(digits) == 12:
        upc12 = digits
    else:
        raise ValueError(f"UPC must have 11 or 12 digits, got '{upc_input}'")
    pattern = encode_upc(upc12)

    # Canvas
    img = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(img)

    # Fonts - similar to Round21 but adjusted for 3 rows
    row1_font = _load_font(100)
    row2_font = _load_font(60)  # Much smaller font for Row 2
    row3_font = _load_font(90)
    digits_font = _load_font(80)

    # Row 1: Column J (left) + Column C (right)
    col_j_txt = (col_j or "").strip().upper()
    col_c_txt = (col_c or "").strip().upper()
    row1_y = margin
    
    draw.text((margin, row1_y), col_j_txt, font=row1_font, fill="black")
    col_c_w = draw.textbbox((0, 0), col_c_txt, font=row1_font)[2]
    draw.text((canvas_w - margin - col_c_w, row1_y), col_c_txt, font=row1_font, fill="black")

    # Row 2: Column B (centered, with text wrapping up to 3 lines using full width)
    col_b_txt = (col_b or "").strip().upper()
    row2_y = row1_y + 120
    
    # Use full width for text wrapping (with small margins)
    text_margin = 20  # Small margin for text
    max_width = canvas_w - 2 * text_margin  # Full width available for text
    
    # Check if text fits on one line
    col_b_w = draw.textbbox((0, 0), col_b_txt, font=row2_font)[2]
    
    if col_b_w <= max_width:
        # Text fits on one line - center it
        draw.text(((canvas_w - col_b_w) // 2, row2_y), col_b_txt, font=row2_font, fill="black")
        row2_actual_height = 60  # Single line height
    else:
        # Text too long - split into multiple lines
        words = col_b_txt.split()
        if len(words) <= 1:
            # Single word too long - truncate
            truncated = col_b_txt[:40] + "..." if len(col_b_txt) > 40 else col_b_txt
            truncated_w = draw.textbbox((0, 0), truncated, font=row2_font)[2]
            draw.text(((canvas_w - truncated_w) // 2, row2_y), truncated, font=row2_font, fill="black")
            row2_actual_height = 60
        else:
            # Try to fit text into 2 or 3 lines
            lines = []
            current_line = []
            current_width = 0
            
            for word in words:
                test_line = " ".join(current_line + [word])
                test_width = draw.textbbox((0, 0), test_line, font=row2_font)[2]
                
                if test_width <= max_width and len(lines) < 2:  # Allow up to 3 lines total
                    current_line.append(word)
                    current_width = test_width
                else:
                    if current_line:
                        lines.append(" ".join(current_line))
                    current_line = [word]
                    current_width = draw.textbbox((0, 0), word, font=row2_font)[2]
            
            # Add the last line
            if current_line:
                lines.append(" ".join(current_line))
            
            # If we still have too many lines, force into 3 lines
            if len(lines) > 3:
                # Redistribute words more evenly across 3 lines
                words_per_line = len(words) // 3
                remainder = len(words) % 3
                
                lines = []
                start_idx = 0
                for i in range(3):
                    if i < remainder:
                        end_idx = start_idx + words_per_line + 1
                    else:
                        end_idx = start_idx + words_per_line
                    lines.append(" ".join(words[start_idx:end_idx]))
                    start_idx = end_idx
            
            # Draw the lines (centered)
            for i, line in enumerate(lines):
                line_w = draw.textbbox((0, 0), line, font=row2_font)[2]
                draw.text(((canvas_w - line_w) // 2, row2_y + i * 60), line, font=row2_font, fill="black")
            
            row2_actual_height = len(lines) * 60  # Dynamic height based on number of lines

    # Row 3: Column A - Column E (centered)
    col_a_txt = (col_a or "").strip().upper()
    col_e_txt = (col_e or "").strip().upper()
    row3_text = f"{col_a_txt}-{col_e_txt}" if col_a_txt and col_e_txt else (col_a_txt or col_e_txt)
    row3_y = row2_y + row2_actual_height + 20  # Dynamic spacing based on Row 2 height
    row3_w = draw.textbbox((0, 0), row3_text, font=row3_font)[2]
    draw.text(((canvas_w - row3_w) // 2, row3_y), row3_text, font=row3_font, fill="black")

    # Barcode area - positioned below row 3
    bar_top = row3_y + 120
    bar_bottom = canvas_h - 150  # No price, so less bottom margin needed
    bar_height = bar_bottom - bar_top

    modules = len(pattern)  # 95
    module_w = int(max(1, math.floor((canvas_w - 2 * margin) / modules)))
    total_w = module_w * modules
    x0 = (canvas_w - total_w) // 2

    guard_extra = int(bar_height * 0.12)

    for i, bit in enumerate(pattern):
        if bit == '1':
            is_guard = (i < 3) or (45 <= i < 50) or (modules - 3 <= i < modules)
            top = bar_top
            bottom = bar_bottom + (guard_extra if is_guard else 0)
            draw.rectangle([x0 + i * module_w, top, x0 + (i + 1) * module_w - 1, bottom], fill="black")

    # Human-readable digits centered
    hr = f"{upc12[0]}  {upc12[1:6]}  {upc12[6:11]}  {upc12[11]}"
    hr_w = draw.textbbox((0, 0), hr, font=digits_font)[2]
    digits_y = bar_bottom + guard_extra + 10
    draw.text(((canvas_w - hr_w) // 2, digits_y), hr, font=digits_font, fill="black")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    return upc12, out_path


# ---------------- Spreadsheet parsing for formats ----------------

def _parse_round21(path: str) -> list[dict]:
    """
    Rules:
    1) Values start at ROW 12 (1-indexed) => index 11
    2) Stop when Column A equals 'Customer PO'
    3) Skip empty rows

    Columns:
    A: SKU
    C: Title
    I: Garment Color
    J: UPC
    K: Price (optional)
    """
    # Support CSV or XLSX
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path, header=None)
    else:
        df = pd.read_excel(path, header=None)

    start_row = 11
    records = []
    nrows, ncols = df.shape

    for r in range(start_row, nrows):
        a_val = df.iloc[r, 0] if 0 < ncols else None
        if isinstance(a_val, str) and a_val.strip().upper() == "CUSTOMER PO":
            break

        # pull fields
        sku = "" if pd.isna(df.iloc[r, 0]) else str(df.iloc[r, 0]).strip()
        # Prefer Column C; fall back to Column B if C is blank in their sheet
        title_val = df.iloc[r, 2] if ncols > 2 else None
        if pd.isna(title_val) or str(title_val).strip() == "":
            title_val = df.iloc[r, 1] if ncols > 1 else None
        title = "" if title_val is None or pd.isna(title_val) else str(title_val).strip()
        color = "" if (ncols <= 8 or pd.isna(df.iloc[r, 8])) else str(df.iloc[r, 8]).strip()
        upc_val = df.iloc[r, 8] if ncols > 8 else None
        upc = "" if upc_val is None or pd.isna(upc_val) else str(upc_val).strip()
        price_val = df.iloc[r, 10] if ncols > 10 else None
        price = "" if price_val is None or pd.isna(price_val) else str(price_val).strip()
        
        # Hot Market additional fields
        hot_market_col_c = "" if (ncols <= 2 or pd.isna(df.iloc[r, 2])) else str(df.iloc[r, 2]).strip()
        hot_market_col_j = "" if (ncols <= 9 or pd.isna(df.iloc[r, 9])) else str(df.iloc[r, 9]).strip()
        hot_market_col_b = "" if (ncols <= 1 or pd.isna(df.iloc[r, 1])) else str(df.iloc[r, 1]).strip()
        hot_market_col_a = "" if (ncols <= 0 or pd.isna(df.iloc[r, 0])) else str(df.iloc[r, 0]).strip()
        hot_market_col_e = "" if (ncols <= 4 or pd.isna(df.iloc[r, 4])) else str(df.iloc[r, 4]).strip()

        # Skip empty or missing-upc rows
        if not upc or not sku:
            continue

        if not title:
            # synthesize from SKU if needed
            title = " ".join(str(sku).split("-")[:3]).upper()

        records.append({
            "row": r + 1,
            "SKU": sku,
            "Title": title,
            "Color": color,
            "UPC": upc,
            "Price": price,
            "HotMarketColC": hot_market_col_c,
            "HotMarketColJ": hot_market_col_j,
            "HotMarketColB": hot_market_col_b,
            "HotMarketColA": hot_market_col_a,
            "HotMarketColE": hot_market_col_e
        })
    return records


def _parse_hunter_harms(pdf_path: str) -> list[dict]:
    """
    Parse Hunter Harms PDF format:
    - Column 1: Title
    - Column 4: SKUs (separated by newlines)
    - Column 6: Color
    - Columns 7-12: Size quantities (S, M, L, XL, 2XL, 3XL)
    """
    records = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract table from PDF
            tables = page.extract_tables()
            if not tables:
                continue
                
            table = tables[0]  # Use first table
            
            # Skip header row, process data rows
            for row_idx, row in enumerate(table[1:], start=2):
                if len(row) < 13:  # Need at least 13 columns
                    continue
                    
                # Extract data from columns
                title = str(row[0]).strip() if row[0] else ""
                skus_text = str(row[3]).strip() if row[3] else ""  # Column 4 (0-indexed)
                color = str(row[5]).strip() if row[5] else ""  # Column 6 (0-indexed)
                
                # Stop parsing if Column 1 is empty (end of data)
                if not title:
                    break
                
                # Skip if no SKUs
                if not skus_text:
                    continue
                
                # Split SKUs by newlines
                skus = [sku.strip() for sku in skus_text.split('\n') if sku.strip()]
                
                # Extract size quantities from columns 7-12
                size_columns = row[6:12]  # Columns 7-12 (0-indexed)
                size_names = ['S', 'M', 'L', 'XL', '2XL', '3XL']
                
                # Create one record per SKU (SKU already contains size info)
                for sku in skus:
                    # Extract size from SKU (last part before the final number)
                    sku_parts = sku.split('-')
                    if len(sku_parts) >= 4:
                        size_from_sku = sku_parts[-2]  # e.g., "S" from "CLUB-TS-BN-S-11"
                    else:
                        size_from_sku = "UNKNOWN"
                    
                    records.append({
                        "row": row_idx,
                        "Title": f"{title} - {color}",
                        "SKU": sku,
                        "Size": size_from_sku,
                        "Quantity": 1  # Each SKU represents 1 item
                    })
    
    return records


def generate_code128_barcode(sku: str, width: int = 400, height: int = 100) -> Image.Image:
    """Generate Code 128 barcode image from SKU"""
    try:
        code128 = Code128(sku, writer=ImageWriter())
        barcode_img = code128.render({
            'module_width': 1,  # Fixed module width
            'module_height': height,  # Use full height
            'quiet_zone': 2.5,
            'font_size': 8,
            'text_distance': 2.0,
            'background': 'white',
            'foreground': 'black',
            'write_text': False,  # Don't include text - we position it manually
        })
        
        # Resize to desired width while maintaining aspect ratio
        if barcode_img.width != width:
            aspect_ratio = barcode_img.height / barcode_img.width
            new_height = int(width * aspect_ratio)
            barcode_img = barcode_img.resize((width, new_height), Image.Resampling.LANCZOS)
        
        return barcode_img
    except Exception as e:
        # Fallback: create a simple placeholder
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        draw.text((10, height//2 - 10), f"Error: {str(e)[:50]}", fill="red")
        return img


def render_hunter_harms_label(
    title: str,
    sku: str,
    size: str,
    out_path: str,
    canvas_w: int = 1400,
    canvas_h: int = 900,
    margin: int = 80
):
    """Render label for Hunter Harms format with Code 128 barcode"""
    # Canvas
    img = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = _load_font(100)
    sku_font = _load_font(85)
    size_font = _load_font(95)  # Larger size font

    # Title centered at top
    title_txt = title.strip().upper()
    title_w = draw.textbbox((0, 0), title_txt, font=title_font)[2]
    draw.text(((canvas_w - title_w) // 2, margin), title_txt, font=title_font, fill="black")

    # Generate Code 128 barcode (use more width, reduced height)
    barcode_img = generate_code128_barcode(sku, width=1200, height=80)
    
    # Position barcode below title (with more space)
    barcode_y = margin + 120
    barcode_x = (canvas_w - barcode_img.width) // 2
    img.paste(barcode_img, (barcode_x, barcode_y))

    # SKU centered below barcode
    sku_txt = sku.strip()
    sku_y = barcode_y + barcode_img.height + 15
    sku_w = draw.textbbox((0, 0), sku_txt, font=sku_font)[2]
    draw.text(((canvas_w - sku_w) // 2, sku_y), sku_txt, font=sku_font, fill="black")

    # Size below SKU (more spacing above)
    size_txt = size.strip()
    size_y = sku_y + 90  # Increased spacing above size
    size_w = draw.textbbox((0, 0), size_txt, font=size_font)[2]
    draw.text(((canvas_w - size_w) // 2, size_y), size_txt, font=size_font, fill="black")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    return sku, out_path


def generate_labels_bundle(
    xls_or_csv_path: str,
    format_choice: str,
    include_price: bool,
    price_value: Union[str, None],
    out_dir: str,
    hot_market: bool = False
) -> dict:
    """
    Returns dict with:
      png_paths: list[str]
      pdf_path: str
      zip_path: str (created lazily by app.py if missing)
    """
    format_choice = (format_choice or "").lower()
    if format_choice not in ("round21", "hunter_harms"):
        raise ValueError(f"Unsupported format: {format_choice}")

    if format_choice == "round21":
        records = _parse_round21(xls_or_csv_path)
    elif format_choice == "hunter_harms":
        records = _parse_hunter_harms(xls_or_csv_path)

    # Render all
    png_dir = os.path.join(out_dir, "png")
    os.makedirs(png_dir, exist_ok=True)
    png_paths = []

    for rec in records:
        if format_choice == "round21":
            fname = f"{rec['SKU']}".replace("/", "-").replace("\\", "-").replace(" ", "_")
            out_png = os.path.join(png_dir, f"{fname}.png")
            
            if hot_market:
                # Use Hot Market format
                render_hot_market_label(
                    col_j=rec["HotMarketColJ"],
                    col_c=rec["HotMarketColC"],
                    col_b=rec["HotMarketColB"],
                    col_a=rec["HotMarketColA"],
                    col_e=rec["HotMarketColE"],
                    upc_input=rec["UPC"],
                    out_path=out_png
                )
            else:
                # Use standard Round21 format
                render_label(
                    title=rec["Title"],
                    sku=rec["SKU"],
                    color=rec["Color"],
                    upc_input=rec["UPC"],
                    out_path=out_png,
                    include_price=include_price,
                    price_value=rec["Price"] if include_price else None
                )
        elif format_choice == "hunter_harms":
            fname = f"{rec['SKU']}_{rec['Size']}".replace("/", "-").replace("\\", "-").replace(" ", "_")
            out_png = os.path.join(png_dir, f"{fname}.png")
            render_hunter_harms_label(
                title=rec["Title"],
                sku=rec["SKU"],
                size=rec["Size"],
                out_path=out_png
            )
        png_paths.append(out_png)

    # Bundle PDF using Pillow
    pdf_path = os.path.join(out_dir, "labels_bundle.pdf")
    if png_paths:
        imgs = [Image.open(p).convert("RGB") for p in png_paths]
        imgs[0].save(pdf_path, save_all=True, append_images=imgs[1:])
    else:
        # Create an empty stub if nothing parsed (helps with predictable output)
        img = Image.new("RGB", (1000, 300), "white")
        d = ImageDraw.Draw(img)
        d.text((20, 120), "No labels generated from input.", font=_load_font(36), fill="black")
        img.save(pdf_path, "PDF")

    return {
        "png_paths": png_paths,
        "pdf_path": pdf_path,
        "zip_path": os.path.join(out_dir, "labels_png.zip"),
    }

