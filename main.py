#this is the mail file for CV as of now.
import time

import cv2
from ultralytics import YOLO
import random




#formating
#TODO make a log file
print("start of program")
print("______________________________________________")

# Use YOLOv8n (nano) instead of YOLOv8s (small) for ~2x faster inference.
# If you need the accuracy of yolov8s, switch back but expect slower speeds.
yolo = YOLO("yolov8n.pt")

# Each class (person, car, etc.) gets a unique RGB color.
# random.seed(cls_num): makes color consistent across frames.

# for testing run 
# ffmpeg -f v4l2 -video_size 640x480 -i /dev/video0 -vf "format=yuv420p" -f h264 "udp://127.0.0.1:1234" and then run the program
# this may need to be ran as root. It may be SE linux or some odd quirck of the Red Hat world for me but who knows.
# This is lagging on my end I do not think my loopback was made for this sort of work, and my IGPU sucks at video encoding. 
# also my I have a 12th gen 
        


#video_path = "rtsp://192.168.2.2:8554/video_stream__dev_video0"
video_path = "/dev/video0"
videoCap = cv2.VideoCapture(video_path)

# Set camera to lowest resolution for faster capture
videoCap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
videoCap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
videoCap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

frame_count = 0
# FPS tracking
fps_start = time.time()
frame_since_fps = 0
# Process every Nth frame to reduce inference load
PROCESS_EVERY = 5
frame_since_process = 0

def drawFrame(fr):
    results = yolo.predict(fr, stream=True, imgsz=320, verbose=False)
    for result in results:
        class_names = result.names
        for box in result.boxes:
            if box.conf[0] > 0.4:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cls = int(box.cls[0])
                class_name = class_names[cls]

                conf = float(box.conf[0])

                cv2.rectangle(fr, (x1, y1), (x2, y2), 2)

                cv2.putText(fr, f"{class_name} {conf:.2f}",
                            (x1, max(y1 - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, 2)


while True:
    ret, frame = videoCap.read()
    if not ret:
        video_path = "/dev/video0"
        videoCap = cv2.VideoCapture(video_path)
        continue

    frame_since_process += 1


    if frame_since_process >= PROCESS_EVERY:
        frame_since_process = 0
        drawFrame(frame)

    key = cv2.waitKey(1)
    cv2.imshow("test", frame)

    if key == 27 or cv2.getWindowProperty('test', cv2.WND_PROP_VISIBLE) < 1:
          break

    #todo add exit
    frame_count += 1


cv2.destroyAllWindows()
videoCap.release()





