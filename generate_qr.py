import qrcode
import qrcode.image.svg
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
import os

BASE_URL = "https://llyllo972.github.io/gratitude/"
FICHES   = list("ABCDEFGHIJKLMNOP")
OUT_DIR  = "assets/qrcodes"
COLOR    = "#1a2e1a"
SIZE_PX  = 472   # 4cm @ 300 dpi

os.makedirs(OUT_DIR, exist_ok=True)

for lettre in FICHES:
    url = f"{BASE_URL}fiche-{lettre}.html"

    # ── PNG ──
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=COLOR, back_color="white").convert("RGB")
    img = img.resize((SIZE_PX, SIZE_PX), Image.NEAREST)
    png_path = f"{OUT_DIR}/qr-fiche-{lettre}.png"
    img.save(png_path)

    # ── SVG ──
    qr2 = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=4,
                         image_factory=qrcode.image.svg.SvgPathFillImage)
    qr2.add_data(url)
    qr2.make(fit=True)
    svg_img = qr2.make_image(fill_color=COLOR, back_color="white")
    svg_path = f"{OUT_DIR}/qr-fiche-{lettre}.svg"
    with open(svg_path, "wb") as f:
        svg_img.save(f)

    # Injecter width/height 4cm dans le SVG
    with open(svg_path, encoding="utf-8") as f:
        svg = f.read()
    svg = svg.replace('<svg ', '<svg width="4cm" height="4cm" ', 1)
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"✓ fiche-{lettre}  PNG {SIZE_PX}×{SIZE_PX}px  SVG 4cm×4cm  — {url}")

print(f"\n{len(FICHES)*2} fichiers générés dans {OUT_DIR}/")
