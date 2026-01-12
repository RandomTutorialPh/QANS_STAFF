import os, sys
import ctypes

# 🔇 Suppress ZBar (C-level) warnings by redirecting stderr
sys.stderr = open(os.devnull, 'w')

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import qrcode
import cv2
from threading import Thread
import time
import requests
import winsound

from pyzbar.pyzbar import decode
from openpyxl import Workbook, load_workbook
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================================
# 🔐 ANDROID SMS GATEWAY CONFIG (STATIC TOKEN)
# ==========================================================
ANDROID_IP = None
ANDROID_TOKEN = "YOUR_STATIC_SECRET_TOKEN_HERE"  # 🔐 STATIC TOKEN

# ==========================================================
# UI HELPERS
# ==========================================================
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# ==========================================================
# HOME SCREEN
# ==========================================================
def show_home():
    clear_content()

    home_frame = ttk.Frame(content_frame)
    home_frame.place(relx=0.5, rely=0.5, anchor="center")

    title = ttk.Label(
        home_frame,
        text="QR ATTENDANCE SYSTEM",
        font=("Arial", 20, "bold")
    )
    title.pack(pady=20)

    ttk.Button(
        home_frame,
        text="QR Generator",
        command=show_form
    ).pack(pady=10, ipadx=20, ipady=10)

    ttk.Button(
        home_frame,
        text="QR Scanner",
        command=open_qr_scanner
    ).pack(pady=10, ipadx=20, ipady=10)

# ==========================================================
# QR GENERATOR
# ==========================================================
def show_form():
    clear_content()

    form_frame = ttk.Frame(content_frame)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    entries = {}

    fields = [
        "First Name", "Middle Name", "Last Name",
        "Gender", "Address", "Department", "Position",
        "Emergency Contact Name", "Emergency Contact Number"
    ]

    for i, field in enumerate(fields):
        ttk.Label(form_frame, text=f"{field}:").grid(row=i, column=0, sticky="w", padx=5, pady=5)
        entries[field] = ttk.Entry(form_frame, width=40)
        entries[field].grid(row=i, column=1, padx=5, pady=5)

    def submit_form():
        data = {k: v.get().strip().upper() for k, v in entries.items()}
        if any(not v for v in data.values()):
            messagebox.showwarning("Missing", "Please fill all fields")
            return

        qr_text = "\n".join([f"{k}: {v}" for k, v in data.items()])
        qr = qrcode.make(qr_text)

        base = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(base, "qrcodes")
        os.makedirs(out_dir, exist_ok=True)

        filename = f"{data['First Name']}_{data['Last Name']}.png"
        path = os.path.join(out_dir, filename)
        qr.save(path)

        messagebox.showinfo("Success", f"QR saved to:\n{path}")
        show_form()

    ttk.Button(form_frame, text="Generate QR", command=submit_form).grid(
        row=len(fields), column=0, columnspan=2, pady=15
    )

    ttk.Button(form_frame, text="🏠 Home", command=show_home).grid(
        row=len(fields) + 1, column=0, columnspan=2
    )

# ==========================================================
# SMS FUNCTION (STATIC TOKEN)
# ==========================================================
def send_sms(number, message):
    if not ANDROID_IP:
        print("❌ Android IP not set")
        return False

    data = {
        "token": ANDROID_TOKEN,
        "number": number,
        "message": message
    }

    try:
        r = requests.post(f"http://{ANDROID_IP}:5000/send_sms", data=data, timeout=10)
        print("📨 SMS:", r.status_code, r.text)
        return r.status_code == 200
    except Exception as e:
        print("❌ SMS error:", e)
        return False

# ==========================================================
# QR SCANNER
# ==========================================================
def open_qr_scanner():
    clear_content()

    frame = ttk.Frame(content_frame)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(
        frame,
        text="📱 Enter Android SMS Gateway IP",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    ip_entry = ttk.Entry(frame, width=30)
    ip_entry.pack(pady=5)

    def proceed():
        global ANDROID_IP
        ANDROID_IP = ip_entry.get().strip()
        if not ANDROID_IP:
            messagebox.showwarning("Missing", "Please enter Android IP")
            return
        start_scanner()

    ttk.Button(frame, text="Proceed to Scanner", command=proceed).pack(pady=10)
    ttk.Button(frame, text="🏠 Home", command=show_home).pack()

# ==========================================================
# CAMERA SCANNER LOOP
# ==========================================================
def start_scanner():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Cannot open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for obj in decode(frame):
            qr_data = obj.data.decode("utf-8")
            print("QR:", qr_data)
            winsound.Beep(1000, 200)

            cap.release()
            cv2.destroyAllWindows()

            send_sms("09187705134", "Attendance recorded successfully")
            messagebox.showinfo("Success", "Attendance recorded!")
            show_home()
            return

        cv2.imshow("QR Scanner (Press Q to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    show_home()

# ==========================================================
# MAIN
# ==========================================================
root = tk.Tk()
root.title("QR Attendance Notification System")
root.geometry("600x700")

content_frame = ttk.Frame(root)
content_frame.pack(fill="both", expand=True)

show_home()
root.mainloop()
