import qrcode
from PIL import Image, ImageDraw, ImageFont

# ============================================================
# CROPGUARD APK DOWNLOAD QR CODE
# ============================================================

DOWNLOAD_LINK = "https://drive.google.com/drive/folders/15FWWivNYowsUfwHl5PMzOKGBlN0cb5Fx?usp=sharing"
OUTPUT_FILE = "CropGuard_Download_QR.png"

# Generate QR
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=20,
    border=4
)

qr.add_data(DOWNLOAD_LINK)
qr.make(fit=True)

qr_image = qr.make_image(
    fill_color="black",
    back_color="white"
).convert("RGB")

# Canvas
padding = 60
label_height = 150

canvas = Image.new(
    "RGB",
    (
        qr_image.width + padding * 2,
        qr_image.height + padding * 2 + label_height
    ),
    "white"
)

# Put QR in center
canvas.paste(
    qr_image,
    (padding, padding)
)

# Draw text
draw = ImageDraw.Draw(canvas)

try:
    font_large = ImageFont.truetype("arial.ttf", 55)
    font_small = ImageFont.truetype("arial.ttf", 32)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

title = "CROPGUARD"
subtitle = "Scan to Download & Try"

# Center title
bbox = draw.textbbox((0, 0), title, font=font_large)
title_width = bbox[2] - bbox[0]

draw.text(
    (
        (canvas.width - title_width) // 2,
        qr_image.height + padding + 15
    ),
    title,
    fill="black",
    font=font_large
)

# Center subtitle
bbox = draw.textbbox((0, 0), subtitle, font=font_small)
subtitle_width = bbox[2] - bbox[0]

draw.text(
    (
        (canvas.width - subtitle_width) // 2,
        qr_image.height + padding + 80
    ),
    subtitle,
    fill="black",
    font=font_small
)

# Save
canvas.save(OUTPUT_FILE, "PNG")

print(f"QR code saved to: {OUTPUT_FILE}")
print(f"Encoded link: {DOWNLOAD_LINK}")