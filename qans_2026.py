import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import qrcode
from tkinter import messagebox
from datetime import datetime

# ================= FUNCTIONS =================
def show_home():
    home_frame.tkraise()

def show_generate_qr():
    generate_qr_frame.tkraise()

def scan_qr():
    scan_frame.tkraise()
    scanned_data_label.config(text="Waiting for scan...")
    scan_entry.delete(0, tk.END)
    scan_entry.focus()

def process_scan():
    scanned_data = scan_entry.get().strip()
    if not scanned_data:
        return

    # Split the scanned data by |
    try:
        fullname, id_no, address, guardian_name, guardian_contact = scanned_data.split("|")
    except ValueError:
        scanned_data_label.config(text="Invalid QR data!")
        scan_entry.delete(0, tk.END)
        scan_entry.focus()
        return

    # Create a human-readable formatted string
    formatted_text = (
        "📋 Personal Data\n"
        f"Name: {fullname}\n"
        f"ULI: {id_no}\n"
        f"Address: {address}\n\n"
        "🚨 In case of Emergency\n"
        f"Name: {guardian_name}\n"
        f"Contact: {guardian_contact}\n\n"
        "💬 Sending SMS: Pending..."
    )

    scanned_data_label.config(text=formatted_text)

    # Clear the hidden entry
    scan_entry.delete(0, tk.END)

    # Automatically reset after 5 seconds
    scan_frame.after(5000, lambda: scanned_data_label.config(text="Waiting for scan..."))
    scan_frame.after(5000, lambda: scan_entry.focus())


def open_folder():
    folder_path = os.path.join(BASE_DIR, "attendance")
    os.makedirs(folder_path, exist_ok=True)

    if sys.platform.startswith("win"):
        os.startfile(folder_path)
    elif sys.platform == "darwin":
        os.system(f"open '{folder_path}'")
    else:
        os.system(f"xdg-open '{folder_path}'")

def only_numbers(new_value):
    return new_value.isdigit() or new_value == ""

def contact_number_validation(new_value):
    return (new_value.isdigit() and len(new_value) <= 11) or new_value == ""

def generate_qr():
    fullname = entry_fullname.get().strip().upper()
    id_no = entry_idno.get().strip()
    address = entry_address.get().strip()
    guardian_name = entry_guardian_name.get().strip().upper()
    guardian_contact = entry_guardian_contact.get().strip()

    if not fullname or not id_no or not address or not guardian_name or not guardian_contact:
        messagebox.showerror("Validation Error", "All fields are required.")
        return
    if not guardian_contact.isdigit() or len(guardian_contact) != 11:
        messagebox.showerror("Validation Error", "Guardian contact number must be EXACTLY 11 digits.")
        return

    qr_data = f"{fullname}|{id_no}|{address}|{guardian_name}|{guardian_contact}"

    attendance_folder = os.path.join(BASE_DIR, "attendance")
    qr_folder = os.path.join(attendance_folder, "QR Code")
    os.makedirs(qr_folder, exist_ok=True)

    safe_name = "_".join(fullname.split())
    filename = f"{safe_name}.png"
    qr_path = os.path.join(qr_folder, filename)

    try:
        qr = qrcode.make(qr_data)
        qr.save(qr_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate QR Code.\n{e}")
        return

    messagebox.showinfo("Success", f"QR Code generated successfully!\n\nSaved to:\n{qr_path}")

    entry_fullname.delete(0, tk.END)
    entry_idno.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_guardian_name.delete(0, tk.END)
    entry_guardian_contact.delete(0, tk.END)

def exit_app():
    root.destroy()

# ================= BASE PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "src", "img", "logo.png")
ICON_PATH = os.path.join(BASE_DIR, "src", "img", "logo.ico")

# ================= MAIN WINDOW =================
root = tk.Tk()

vcmd_numbers = root.register(only_numbers)
vcmd_contact = root.register(contact_number_validation)

root.overrideredirect(True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.bind("<Escape>", lambda e: None)

try:
    if os.path.exists(ICON_PATH):
        root.iconbitmap(default=ICON_PATH)
except:
    pass

root.configure(bg="#f4f6f9")
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# ================= HEADER =================
header = tk.Frame(root, bg="#1e293b", height=100)
header.grid(row=0, column=0, sticky="nsew")
header.columnconfigure(1, weight=1)

logo = None
try:
    if os.path.exists(LOGO_PATH):
        logo_img = Image.open(LOGO_PATH).resize((70, 70))
        logo = ImageTk.PhotoImage(logo_img)
except:
    pass

if logo:
    lbl_logo = tk.Label(header, image=logo, bg="#1e293b")
    lbl_logo.image = logo
else:
    lbl_logo = tk.Label(header, bg="#1e293b", width=10)

lbl_logo.grid(row=0, column=0, padx=20, pady=10)

tk.Label(
    header,
    text="QR ATTENDANCE NOTIFICATION SYSTEM",
    font=("Arial", 26, "bold"),
    bg="#1e293b",
    fg="white"
).grid(row=0, column=1, sticky="w")

# ================= CONTENT =================
content = tk.Frame(root, bg="#f4f6f9")
content.grid(row=1, column=0, sticky="nsew")
content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=1)

# ================= HOME FRAME =================
home_frame = tk.Frame(content, bg="#f4f6f9")
home_frame.grid(row=0, column=0, sticky="nsew")

center_frame = tk.Frame(home_frame, bg="#f4f6f9")
center_frame.place(relx=0.5, rely=0.5, anchor="center")

row1 = tk.Frame(center_frame, bg="#f4f6f9")
row1.pack(pady=25)

tk.Button(
    row1, text="Generate QR Code",
    command=show_generate_qr,
    bg="#2563EB", fg="white",
    activebackground="#1D4ED8",
    font=("Arial", 16, "bold"),
    width=22, height=2, bd=0
).pack(side="left", padx=30)

tk.Button(
    row1, text="Scan QR Code",
    command=scan_qr,
    bg="#0EA5E9", fg="white",
    activebackground="#0284C7",
    font=("Arial", 16, "bold"),
    width=22, height=2, bd=0
).pack(side="left", padx=30)

row2 = tk.Frame(center_frame, bg="#f4f6f9")
row2.pack(pady=25)

tk.Button(
    row2, text="Open Folder",
    command=open_folder,
    bg="#16A34A", fg="white",
    activebackground="#15803D",
    font=("Arial", 16, "bold"),
    width=22, height=2, bd=0
).pack(side="left", padx=30)

tk.Button(
    row2, text="Exit",
    command=exit_app,
    bg="#DC2626", fg="white",
    activebackground="#991B1B",
    font=("Arial", 16, "bold"),
    width=22, height=2, bd=0
).pack(side="left", padx=30)

# ================= GENERATE QR FRAME =================
generate_qr_frame = tk.Frame(content, bg="#f4f6f9")
generate_qr_frame.grid(row=0, column=0, sticky="nsew")

# ================= SCAN QR FRAME =================
scan_frame = tk.Frame(content, bg="#f4f6f9")
scan_frame.grid(row=0, column=0, sticky="nsew")

scan_label = tk.Label(
    scan_frame,
    text="Scan QR Code",
    font=("Arial", 22, "bold"),
    bg="#f4f6f9"
)
scan_label.pack(pady=(50, 20))

# Display scanned data
scanned_data_label = tk.Label(
    scan_frame,
    text="Waiting for scan...",
    font=("Arial", 18),
    bg="#f4f6f9",
    fg="#1e293b",
    wraplength=600,
    justify="center"
)
scanned_data_label.pack(pady=20)

# Hidden entry to capture scanner input
scan_entry = tk.Entry(scan_frame)
scan_entry.pack()
scan_entry.place(x=-100, y=-100)  # keep it hidden
scan_entry.bind("<Return>", lambda e: process_scan())

# Home button for Scan screen
home_btn = tk.Button(
    scan_frame,
    text="HOME",
    command=show_home,
    bg="#6B7280",
    fg="white",
    font=("Arial", 14, "bold"),
    width=18,
    height=2,
    bd=0
)
home_btn.pack(pady=20)

# ================= GENERATE QR FORM =================
form = tk.Frame(generate_qr_frame, bg="#f4f6f9")
form.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(
    form,
    text="Generate QR Code",
    font=("Arial", 22, "bold"),
    bg="#f4f6f9"
).pack(pady=(0, 30))

user_info = tk.LabelFrame(
    form,
    text=" USER INFORMATION ",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#1e293b",
    padx=30,
    pady=20
)
user_info.pack(fill="x", pady=(0, 25))

tk.Label(user_info, text="FULL NAME:", bg="white", font=("Arial", 13))\
    .grid(row=0, column=0, sticky="w", padx=(0, 20), pady=10)
entry_fullname = tk.Entry(user_info, font=("Arial", 13), width=35)
entry_fullname.grid(row=0, column=1, pady=10)

tk.Label(user_info, text="ID NO:", bg="white", font=("Arial", 13))\
    .grid(row=1, column=0, sticky="w", padx=(0, 20), pady=10)
entry_idno = tk.Entry(
    user_info, font=("Arial", 13), width=35,
    validate="key", validatecommand=(vcmd_numbers, "%P")
)
entry_idno.grid(row=1, column=1, pady=10)

tk.Label(user_info, text="ADDRESS:", bg="white", font=("Arial", 13))\
    .grid(row=2, column=0, sticky="w", padx=(0, 20), pady=10)
entry_address = tk.Entry(user_info, font=("Arial", 13), width=35)
entry_address.grid(row=2, column=1, pady=10)

guardian_info = tk.LabelFrame(
    form,
    text=" SMS GUARDIAN INFORMATION ",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#1e293b",
    padx=30,
    pady=20
)
guardian_info.pack(fill="x", pady=(0, 30))

tk.Label(guardian_info, text="NAME:", bg="white", font=("Arial", 13))\
    .grid(row=0, column=0, sticky="w", padx=(0, 20), pady=10)
entry_guardian_name = tk.Entry(guardian_info, font=("Arial", 13), width=35)
entry_guardian_name.grid(row=0, column=1, pady=10)

tk.Label(guardian_info, text="CONTACT NO:", bg="white", font=("Arial", 13))\
    .grid(row=1, column=0, sticky="w", padx=(0, 20), pady=10)
entry_guardian_contact = tk.Entry(
    guardian_info, font=("Arial", 13), width=35,
    validate="key", validatecommand=(vcmd_contact, "%P")
)
entry_guardian_contact.grid(row=1, column=1, pady=10)

btn_frame = tk.Frame(form, bg="#f4f6f9")
btn_frame.pack(pady=10)

tk.Button(
    btn_frame,
    text="GENERATE QR",
    command=generate_qr,
    bg="#2563EB",
    fg="white",
    font=("Arial", 14, "bold"),
    width=18,
    height=2,
    bd=0
).pack(side="left", padx=20)

tk.Button(
    btn_frame,
    text="HOME",
    command=show_home,
    bg="#6B7280",
    fg="white",
    font=("Arial", 14, "bold"),
    width=18,
    height=2,
    bd=0
).pack(side="left", padx=20)

# ================= START =================
show_home()
root.mainloop()
