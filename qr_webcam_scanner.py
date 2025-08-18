"""
QR Scanner (Webcam)
-------------------
- Opens your default camera and scans for QR codes in real time.
- Draws a box around detected codes and shows the decoded text on the frame.
- Press 'q' to quit.

Usage:
    python qr_webcam_scanner.py
"""
import sys
import time

# Try to use pyzbar first (fast, robust). Fall back to OpenCV's built-in detector if not available.
try:
    from pyzbar.pyzbar import decode
    _HAS_PYZBAR = True
except Exception:
    _HAS_PYZBAR = False

import cv2

def decode_with_pyzbar(frame):
    results = []
    try:
        from pyzbar.pyzbar import decode
        for obj in decode(frame):
            data = obj.data.decode('utf-8', errors='ignore')
            points = obj.polygon
            bbox = [(p.x, p.y) for p in points] if points else None
            results.append({'data': data, 'bbox': bbox})
    except Exception:
        pass
    return results

def decode_with_opencv(frame):
    # Fallback using OpenCV's built-in QRCodeDetector
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(frame)
    results = []
    if points is not None and data:
        bbox = [(int(x), int(y)) for x, y in points.reshape(-1, 2)]
        results.append({'data': data, 'bbox': bbox})
    return results

def draw_bbox(frame, bbox, label):
    if not bbox:
        return
    # Draw polygon
    for i in range(len(bbox)):
        pt1 = bbox[i]
        pt2 = bbox[(i + 1) % len(bbox)]
        cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
    # Put label above the first point
    x, y = bbox[0]
    cv2.putText(frame, label, (x, max(0, y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

def main():
    print("Starting camera... (press 'q' to quit)")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera. Try a different index (1 or 2).")
        print("Usage: python qr_webcam_scanner.py [camera_index]")
        # Try alternative index if provided
        if len(sys.argv) > 1:
            try:
                idx = int(sys.argv[1])
                cap = cv2.VideoCapture(idx)
            except ValueError:
                pass
        if not cap.isOpened():
            sys.exit(1)

    seen = set()
    last_print = time.time()
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Failed to grab frame.")
            break

        # Decode using pyzbar first, else fallback
        results = decode_with_pyzbar(frame) if _HAS_PYZBAR else []
        if not results:
            results = decode_with_opencv(frame)

        for r in results:
            data = r['data']
            bbox = r['bbox']
            draw_bbox(frame, bbox, data[:50] + ("..." if len(data) > 50 else ""))
            if data and data not in seen:
                seen.add(data)
                print(f"[QR] {data}")

        cv2.imshow('QR Scanner - press q to quit', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Occasionally re-print how to quit to keep console visible
        if time.time() - last_print > 15:
            print("Scanning... (press 'q' to quit)")
            last_print = time.time()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
