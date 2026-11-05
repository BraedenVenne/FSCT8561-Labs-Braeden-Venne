from pathlib import Path
from PIL import Image, ExifTags
import base64
import csv

# Set up the target image directory and initialize results container
image_dir = Path("Images")
results = []

# List of cybersecurity-related keywords to flag in metadata
suspicious_names = [
    "recon",
    "vuln",
    "exploit",
    "lateral",
    "persist",
    "exfil",
    "cve",
    "waf"
]

# Dynamically scan all PNG files in the directory
for image_path in sorted(image_dir.glob("*.png")):
    filename = image_path.name
    with Image.open(image_path) as img:
        # Initialize result dictionary structure for the current image
        result = {
            "filename": filename,
            "format": img.format,
            "metadata_fields": ", ".join(img.info.keys()),
            "suspected_field": "",
            "encoding": "",
            "risk_score": 0,
            "reason": "",
        }
        
        suspected_field = ""
        encoding = ""
        risk_score = 0
        reason = ""

        # Inspect EXIF metadata
        exif = img.getexif()
        for tag_id, value in exif.items():
            tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
            if value is not None:
                val_str = str(value).strip()
                # Verify value contains readable text words
                matched_keyword = False
                for keyword in suspicious_names:
                    if keyword in val_str.lower():
                        matched_keyword = True
                        break
                if matched_keyword:
                    suspected_field = f"EXIF:{tag_name}"
                    encoding = "Plain text"
                    risk_score += 10
                    reason = f"EXIF covert message ({tag_name})."
                    break

        # Inspect PNG text metadata and raw bytes
        if not suspected_field:
            for key, value in img.info.items():
                if key.lower() in ["icc_profile"]:
                    continue
                
                val_str = ""
                is_binary = False
                # Safely decode raw bytes chunks
                if isinstance(value, bytes):
                    is_binary = True
                    try:
                        val_str = value.decode("utf-8", errors="ignore").strip()
                    except Exception:
                        continue
                elif isinstance(value, str):
                    val_str = value.strip()

                if val_str:
                    # Check and decode Base64 strings
                    try:
                        if len(val_str) % 4 == 0 and all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in val_str):
                            decoded_bytes = base64.b64decode(val_str.encode("utf-8"))
                            decoded_str = decoded_bytes.decode("utf-8")
                            matched_keyword = False
                            for keyword in suspicious_names:
                                if keyword in decoded_str.lower():
                                    matched_keyword = True
                                    break
                            if matched_keyword or any(c.isalnum() for c in decoded_str):
                                suspected_field = f"PNG:{key}"
                                encoding = "Base64"
                                risk_score += 5  # +5 for suspicious encoded value requiring investigation
                                reason = f"Suspicious Base64 encoding ({key})."
                                break
                    except Exception:
                        pass

                    # Flag unexpected binary data blocks or unusual descriptive text blocks
                    matched_keyword = False
                    for keyword in suspicious_names:
                        if keyword in val_str.lower():
                            matched_keyword = True
                            break

                    if matched_keyword:
                        suspected_field = f"PNG:{key}"
                        encoding = "Plain text"
                        risk_score += 10  # +10 for confirmed covert-message field
                        reason = f"PNG covert message ({key})."
                        break
                    elif is_binary and len(val_str) > 10 and any(c.isalpha() for c in val_str):
                        suspected_field = f"PNG:{key}"
                        encoding = "Plain text (Decoded Bytes)"
                        risk_score += 10  # +10 for confirmed covert-message field
                        reason = f"Anomalous binary chunk ({key})."
                        break

        # Inspect XMP metadata blocks
        xmp = img.info.get("XML:com.adobe.xmp") or img.info.get("xmp")
        if isinstance(xmp, bytes):
            xmp = xmp.decode("utf-8", errors="replace")
        if xmp and "No XMP found" not in str(xmp) and not suspected_field:
            suspected_field = "XMP:XML:com.adobe.xmp"
            encoding = "Plain text (XML)"
            risk_score += 10  # +10 for confirmed covert-message field
            reason = "Confirmed XMP covert message."

        # Assign default status if no risk indicators were triggered
        if risk_score == 0:
            reason = "No anomalous metadata detected."

        # Populate final row data and append to results list
        result["suspected_field"] = suspected_field if suspected_field else "None"
        result["encoding"] = encoding if encoding else "None"
        result["risk_score"] = risk_score
        result["reason"] = reason
        results.append(result)

        # Print results to the terminal console
        print(f"filename: {result['filename']} | format: {result['format']} | suspected: {result['suspected_field']} | encoding: {result['encoding']} | risk: {result['risk_score']} | reason: {result['reason']}")

# Export all scan results to metadata_report.csv
with open("metadata_report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\nSaved", len(results), "rows to metadata_report.csv")