# Barcode Generator (Round21 format)

Upload an XLSX/CSV and get:
- Individual PNG labels (SKU-based filenames)
- One combined multi-page PDF

## Format options
- **Round21**:
  - Start at row 12 (1-indexed)
  - Stop when Column A equals "Customer PO"
  - Skip empty rows
  - Columns:
    - A: SKU
    - C: Title (falls back to B if C is blank)
    - I: Garment Color
    - J: UPC

## Price line
- If "Include Price" is checked **and** a value is supplied, the same price is printed on all labels.
- If unchecked, no price line is added (no placeholders).

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export FLASK_SECRET_KEY="change-me"
python app.py
# open http://localhost:5000
```

## Server Connection

For connecting to the production server, see **[SERVER_CONNECTION.md](SERVER_CONNECTION.md)**

Quick connect:
```bash
./connect_server.sh
```

Or manually:
```bash
ssh -i ~/.ssh/lambda-layer-key.pem ec2-user@18.220.30.5
```

