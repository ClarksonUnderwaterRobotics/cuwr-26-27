#this is the mail file for CV as of now.
import cv2 
from ultralytics import YOLO
import random
import threading


#formating
#TODO make a log file
print("start of program")
print("______________________________________________")
yolo = YOLO("yolov8s.pt")
# Each class (person, car, etc.) gets a unique RGB color.
# random.seed(cls_num): makes color consistent across frames.

# for testing run 
# ffmpeg -f v4l2 -video_size 640x480 -i /dev/video0 -vf "format=yuv420p" -f h264 "udp://127.0.0.1:1234"^C and then run the program
# This is lagging on my end I do not think my loopback was made for this sort of work. and my IGPU sucks at video encoding
video_path = "udp://127.0.0.1:1234"
videoCap = cv2.VideoCapture(video_path)

frame_count = 0

def getColours(cls_num):
    """Generate unique colors for each class ID"""
    random.seed(cls_num)
    return (255, 0, 0)

while True:
    
    ret, frame = videoCap.read()
    print(ret)
    if not ret:
        break
    results = yolo.track(frame, stream=True) 
    for result in results:
        class_names = result.names
        for box in result.boxes:
            if box.conf[0] > 0.4:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cls = int(box.cls[0])
                class_name = class_names[cls]

                conf = float(box.conf[0])

                colour = getColours(cls)

                cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)

                cv2.putText(frame, f"{class_name} {conf:.2f}",
                            (x1, max(y1 - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, colour, 2)
                  
    cv2.imshow("test",frame)
    #no idea what this dose
    key = cv2.waitKey(10)

    if key ==27 or cv2.getWindowProperty('test', cv2.WND_PROP_VISIBLE) < 1:
          break
    
    #todo add exit
    frame_count += 1

cv2.destroyAllWindows()
videoCap.release()




