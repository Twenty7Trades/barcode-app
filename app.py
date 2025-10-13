import os
import tempfile
import json
import shutil
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
import pytz

from flask import (
    Flask, render_template, request, send_file, redirect, url_for, flash
)

from barcode_gen import generate_labels_bundle

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")  # set in prod

# Storage for generated files (temp). You can point this to EBS/S3 later.
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(tempfile.gettempdir(), "barcode_app"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Storage for saved labels
SAVED_LABELS_DIR = os.environ.get("SAVED_LABELS_DIR", os.path.join(tempfile.gettempdir(), "barcode_app_saved"))
os.makedirs(SAVED_LABELS_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/round21", methods=["GET"])
def round21():
    return render_template("round21.html")


@app.route("/hunter-harms", methods=["GET"])
def hunter_harms():
    return render_template("hunter_harms.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        flash("No file uploaded.")
        return redirect(request.referrer or url_for("index"))

    upload_file = request.files["file"]
    if upload_file.filename == "":
        flash("No selected file.")
        return redirect(request.referrer or url_for("index"))

    # Determine format based on referrer URL
    referrer = request.referrer or ""
    if "hunter-harms" in referrer:
        fmt = "hunter_harms"
    else:
        fmt = "round21"
    
    include_price = bool(request.form.get("include_price"))
    hot_market = bool(request.form.get("hot_market"))

    # Save upload to temp
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    session_dir = os.path.join(OUTPUT_DIR, f"job_{ts}")
    os.makedirs(session_dir, exist_ok=True)
    src_path = os.path.join(session_dir, upload_file.filename)
    upload_file.save(src_path)
    
    # Store original filename for later use
    original_filename = upload_file.filename

    try:
        # Generate labels (PNGs) + bundle PDF and ZIP
        results = generate_labels_bundle(
            xls_or_csv_path=src_path,
            format_choice=fmt,
            include_price=include_price,
            price_value=None,  # Individual prices now come from Column K
            out_dir=session_dir,
            hot_market=hot_market
        )
    except Exception as e:
        # Be explicit so debugging doesn't eat your life.
        flash(f"Error while generating labels: {e}")
        return redirect(request.referrer or url_for("index"))

    return render_template(
        "result.html",
        count=len(results["png_paths"]),
        pdf_path=url_for("download", kind="pdf", job=os.path.basename(session_dir)),
        zip_path=url_for("download", kind="zip", job=os.path.basename(session_dir)),
        sample_pngs=[url_for("preview", job=os.path.basename(session_dir), fname=os.path.basename(p)) for p in results["png_paths"][:4]],
        include_price=include_price,
        job=os.path.basename(session_dir),
        original_filename=original_filename
    )


@app.route("/download/<kind>/<job>", methods=["GET"])
def download(kind, job):
    session_dir = os.path.join(OUTPUT_DIR, job)
    if kind == "pdf":
        path = os.path.join(session_dir, "labels_bundle.pdf")
    elif kind == "zip":
        path = os.path.join(session_dir, "labels_png.zip")
        # zip lazily if not present
        if not os.path.exists(path):
            png_dir = os.path.join(session_dir, "png")
            with ZipFile(path, "w", ZIP_DEFLATED) as zf:
                for fname in sorted(os.listdir(png_dir)):
                    if fname.lower().endswith(".png"):
                        zf.write(os.path.join(png_dir, fname), arcname=fname)
    else:
        return "Unknown artifact", 400

    if not os.path.exists(path):
        return "Not found", 404

    as_name = f"{job}_{os.path.basename(path)}"
    return send_file(path, as_attachment=True, download_name=as_name)


@app.route("/preview/<job>/<fname>")
def preview(job, fname):
    # Serve generated PNGs for quick peek
    path = os.path.join(OUTPUT_DIR, job, "png", fname)
    if not os.path.exists(path):
        return "Not found", 404
    return send_file(path, mimetype="image/png")


@app.route("/save-labels/<job>")
def save_labels(job):
    """Save a label set to permanent storage"""
    session_dir = os.path.join(OUTPUT_DIR, job)
    if not os.path.exists(session_dir):
        flash("Label set not found.")
        return redirect(url_for("index"))
    
    # Get original filename from the uploaded file in the session directory
    original_filename = "Unknown"
    for file in os.listdir(session_dir):
        if file.endswith(('.xlsx', '.csv', '.xls')):
            original_filename = file
            break
    
    # Create saved label entry using original filename
    filename_base = os.path.splitext(original_filename)[0]
    saved_id = f"{filename_base}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"
    saved_dir = os.path.join(SAVED_LABELS_DIR, saved_id)
    os.makedirs(saved_dir, exist_ok=True)
    
    # Copy files to saved location
    shutil.copytree(session_dir, saved_dir, dirs_exist_ok=True)
    
    # Create metadata
    metadata = {
        "id": saved_id,
        "created": datetime.utcnow().isoformat(),
        "original_job": job,
        "original_filename": original_filename,
        "display_name": filename_base,
        "count": len([f for f in os.listdir(os.path.join(saved_dir, "png")) if f.endswith(".png")]),
        "has_pdf": os.path.exists(os.path.join(saved_dir, "labels_bundle.pdf"))
    }
    
    with open(os.path.join(saved_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f)
    
    flash(f"Labels saved successfully! ({metadata['count']} labels)")
    return redirect(url_for("all_labels"))


@app.route("/all-labels")
def all_labels():
    """Display all saved label sets"""
    saved_sets = []
    
    for item in os.listdir(SAVED_LABELS_DIR):
        item_path = os.path.join(SAVED_LABELS_DIR, item)
        if os.path.isdir(item_path):
            metadata_path = os.path.join(item_path, "metadata.json")
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                # Get first PNG for thumbnail
                png_dir = os.path.join(item_path, "png")
                if os.path.exists(png_dir):
                    png_files = [f for f in os.listdir(png_dir) if f.endswith(".png")]
                    if png_files:
                        metadata["thumbnail"] = url_for("saved_preview", saved_id=item, fname=png_files[0])
                
                # Handle missing display_name for older saved labels
                if "display_name" not in metadata:
                    metadata["display_name"] = metadata.get("original_filename", "Unknown")
                
                # Convert UTC timestamp to Pacific Time
                try:
                    utc_time = datetime.fromisoformat(metadata["created"].replace('Z', '+00:00'))
                    pacific_tz = pytz.timezone('America/Los_Angeles')
                    pacific_time = utc_time.astimezone(pacific_tz)
                    metadata["created_pacific"] = pacific_time.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    # Fallback to original format if conversion fails
                    metadata["created_pacific"] = metadata["created"][:19].replace('T', ' ')
                
                saved_sets.append(metadata)
    
    # Sort by creation date (newest first)
    saved_sets.sort(key=lambda x: x["created"], reverse=True)
    
    return render_template("all_labels.html", saved_sets=saved_sets)


@app.route("/saved-labels/<saved_id>")
def view_saved_labels(saved_id):
    """View a specific saved label set"""
    saved_dir = os.path.join(SAVED_LABELS_DIR, saved_id)
    if not os.path.exists(saved_dir):
        flash("Saved label set not found.")
        return redirect(url_for("all_labels"))
    
    metadata_path = os.path.join(saved_dir, "metadata.json")
    if not os.path.exists(metadata_path):
        flash("Invalid saved label set.")
        return redirect(url_for("all_labels"))
    
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    
    # Get PNG files for preview
    png_dir = os.path.join(saved_dir, "png")
    png_files = []
    if os.path.exists(png_dir):
        png_files = [f for f in os.listdir(png_dir) if f.endswith(".png")]
    
    sample_pngs = [url_for("saved_preview", saved_id=saved_id, fname=f) for f in png_files[:4]]
    
    # Convert UTC timestamp to Pacific Time
    try:
        utc_time = datetime.fromisoformat(metadata["created"].replace('Z', '+00:00'))
        pacific_tz = pytz.timezone('America/Los_Angeles')
        pacific_time = utc_time.astimezone(pacific_tz)
        created_pacific = pacific_time.strftime('%Y-%m-%d %H:%M:%S')
    except:
        # Fallback to original format if conversion fails
        created_pacific = metadata["created"][:19].replace('T', ' ')
    
    return render_template(
        "saved_result.html",
        saved_id=saved_id,
        count=metadata["count"],
        pdf_path=url_for("saved_download", kind="pdf", saved_id=saved_id) if metadata["has_pdf"] else None,
        zip_path=url_for("saved_download", kind="zip", saved_id=saved_id),
        sample_pngs=sample_pngs,
        created_pacific=created_pacific
    )


@app.route("/saved-download/<kind>/<saved_id>")
def saved_download(kind, saved_id):
    """Download files from saved label sets"""
    saved_dir = os.path.join(SAVED_LABELS_DIR, saved_id)
    if not os.path.exists(saved_dir):
        return "Not found", 404
    
    # Get original filename from metadata
    metadata_path = os.path.join(saved_dir, "metadata.json")
    display_name = saved_id
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            display_name = metadata.get("display_name", saved_id)
    
    if kind == "pdf":
        path = os.path.join(saved_dir, "labels_bundle.pdf")
        as_name = f"{display_name}_labels.pdf"
    elif kind == "zip":
        path = os.path.join(saved_dir, "labels_png.zip")
        # Create zip if it doesn't exist
        if not os.path.exists(path):
            png_dir = os.path.join(saved_dir, "png")
            with ZipFile(path, "w", ZIP_DEFLATED) as zf:
                for fname in sorted(os.listdir(png_dir)):
                    if fname.lower().endswith(".png"):
                        zf.write(os.path.join(png_dir, fname), arcname=fname)
        as_name = f"{display_name}_labels.zip"
    else:
        return "Unknown artifact", 400

    if not os.path.exists(path):
        return "Not found", 404

    return send_file(path, as_attachment=True, download_name=as_name)


@app.route("/saved-preview/<saved_id>/<fname>")
def saved_preview(saved_id, fname):
    """Serve saved PNGs for preview"""
    path = os.path.join(SAVED_LABELS_DIR, saved_id, "png", fname)
    if not os.path.exists(path):
        return "Not found", 404
    return send_file(path, mimetype="image/png")


@app.route("/delete-saved-labels/<saved_id>")
def delete_saved_labels(saved_id):
    """Delete a saved label set"""
    saved_dir = os.path.join(SAVED_LABELS_DIR, saved_id)
    if not os.path.exists(saved_dir):
        flash("Saved label set not found.")
        return redirect(url_for("all_labels"))
    
    # Get display name for confirmation message
    display_name = saved_id
    metadata_path = os.path.join(saved_dir, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            display_name = metadata.get("display_name", saved_id)
    
    # Delete the entire directory
    try:
        shutil.rmtree(saved_dir)
        flash(f"Label set '{display_name}' deleted successfully.")
    except Exception as e:
        flash(f"Error deleting label set: {e}")
    
    return redirect(url_for("all_labels"))


if __name__ == "__main__":
    # For local testing only
    app.run(host="0.0.0.0", port=5000, debug=True)

