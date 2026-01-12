import qrcode
import os

# ==============================
# DATA TO ENCODE (PLAIN TEXT)
# ==============================
qr_data = (
    "NAME: Jerhome T. Reantaso\n"
    "ULI: 45345345654\n"
    "ADDRESS: Samang\n"
    "GUARDIAN: Rios\n"
    "GUARDIAN_NO: 09384747545"
)

# ==============================
# GENERATE QR
# ==============================
qr = qrcode.QRCode(
    version=2,                 # QR size (2 is enough for text)
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)

qr.add_data(qr_data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

# ==============================
# SAVE FILE
# ==============================
output_dir = "qrcodes"
os.makedirs(output_dir, exist_ok=True)

file_path = os.path.join(output_dir, "jerhome_reantaso_qr.png")
img.save(file_path)

print("✅ QR code generated:", file_path)
