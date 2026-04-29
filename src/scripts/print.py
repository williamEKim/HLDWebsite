import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

# ========= SETTINGS =========
OUTPUT_FILE = "yugioh_grid_A4.pdf"
IMAGE_FOLDER = "images"

printer_scale_compensation = 1.1   # try 1.01–1.03 if needed

card_width_mm = 59 * printer_scale_compensation
card_height_mm = 86 * printer_scale_compensation

cols = 3
rows = 3
max_cards = cols * rows

spacing_mm = 3   # space between cards
# ============================


# Convert to points
card_w = card_width_mm * mm
card_h = card_height_mm * mm
spacing = spacing_mm * mm

page_w, page_h = A4

# Calculate centered grid
grid_w = cols * card_w + (cols - 1) * spacing
grid_h = rows * card_h + (rows - 1) * spacing

start_x = (page_w - grid_w) / 2
start_y = (page_h - grid_h) / 2

# Load images (sorted)
valid_ext = (".png", ".jpg", ".jpeg", ".webp")
image_files = sorted([
    f for f in os.listdir(IMAGE_FOLDER)
    if f.lower().endswith(valid_ext)
])[:max_cards]  # limit to 9

# Create PDF
c = canvas.Canvas(OUTPUT_FILE, pagesize=A4)
c.setPageCompression(0)

img_index = 0

for row in range(rows):
    for col in range(cols):
        x = start_x + col * (card_w + spacing)
        y = start_y + (rows - 1 - row) * (card_h + spacing)

        # Draw card border
        c.rect(x, y, card_w, card_h)

        # Place image if available
        if img_index < len(image_files):
            img_path = os.path.join(IMAGE_FOLDER, image_files[img_index])

            try:
                img = ImageReader(img_path)
                iw, ih = img.getSize()

                # Keep aspect ratio (fit inside card)
                scale = min(card_w / iw, card_h / ih)
                new_w = iw * scale
                new_h = ih * scale

                # Center image inside card
                img_x = x + (card_w - new_w) / 2
                img_y = y + (card_h - new_h) / 2

                c.drawImage(img, img_x, img_y, width=new_w, height=new_h)

            except Exception as e:
                print(f"Error loading {img_path}: {e}")

            img_index += 1

# Save
c.save()
print(f"PDF created: {OUTPUT_FILE}")
