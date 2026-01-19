import serial
import time

# =========================
# USER SETTINGS
# =========================
PORT = "COM15"          # ✅ Your SIM7600 COM port
BAUDRATE = 115200

PHONE_NUMBER = "+639929304214"   # replace with destination number
MESSAGE = "Hello from SIM7600 on COM10!"

# TNT / Globe SMS Center
SMSC_TNT = "+639180000371"


def send_at(ser, cmd, delay=1):
    ser.write((cmd + "\r").encode())
    time.sleep(delay)
    resp = ser.read_all().decode(errors="ignore")
    print(f">> {cmd}")
    print(resp)
    return resp


try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)

    # ---- Basic checks ----
    send_at(ser, "AT")
    send_at(ser, "AT+CPIN?")
    send_at(ser, "AT+CSQ")
    send_at(ser, "AT+CREG?")
    send_at(ser, "AT+CEREG?")

    # ---- SMS configuration ----
    send_at(ser, "AT+CMGF=1")                  # Text mode
    send_at(ser, f'AT+CSCA="{SMSC_TNT}"')       # TNT SMSC
    send_at(ser, "AT+CSMS=1")                   # Disable IMS SMS

    # ---- Send SMS ----
    ser.write(f'AT+CMGS="{PHONE_NUMBER}"\r'.encode())
    time.sleep(1)
    ser.write(MESSAGE.encode())
    ser.write(b"\x1A")  # CTRL+Z
    time.sleep(5)

    print(ser.read_all().decode(errors="ignore"))
    ser.close()

except Exception as e:
    print("ERROR:", e)
