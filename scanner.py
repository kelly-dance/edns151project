"""
Issues here:
Seems like it has a long startup time before it starts scanning
for qr codes. idk if thats just my computer, I haven't tested
this code on my laptop yet.
Also I don't have a great understanding of multithreading in
python. There may be issues with this blocking threads.
We need to plan out how / when this script will get activated.
A button or something? Idk whats possible with the hardware

ps part of the issue with threading is that control + c
doesnt seem to be killing the process right away
I have been having to kill this from task manager
"""

from datetime import datetime
import threading
from typing import Iterable, Tuple
import cv2 # !!! opencv-python
from pyzbar import pyzbar # !!!
from data import add_item

# this code 100% expects the data is formed as we are expecting it to be.
# might be fine? but if we were making a real product we would want detection for
# unsupported qrcodes
def parse_qrdata(data: str) -> Iterable[Tuple[str, int]]:
    lines = data.split('\n')
    return map(lambda t: (t[0], int(t[1])), zip(lines[::2], lines[1::2]))

def process_recognition(data: str):
    today = int(datetime.now().timestamp()/86400) # days since jan 1 1970
    for item, days in parse_qrdata(data):
        add_item((today + days)*86400, item)


# yoinked this code from:
# https://towardsdatascience.com/building-a-barcode-qr-code-reader-using-python-360e22dfb6e5
def read_qrs(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        process_recognition(barcode.data.decode('utf-8'))
    return frame

def read_loop():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        frame = read_qrs(frame)
    #3
    camera.release()
    cv2.destroyAllWindows()


thread = threading.Thread(target=read_loop)
thread.start()

