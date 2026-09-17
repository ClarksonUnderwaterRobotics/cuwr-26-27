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
video_path = "/dev/video0"
videoCap = cv2.VideoCapture(0)

frame_count = 0

def getColours(cls_num):
    """Generate unique colors for each class ID"""
    random.seed(cls_num)
    return tuple(random.randint(0, 255) for _ in range(3))

while True:
    
    ret, frame = videoCap.read()
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
    key = cv2.waitKey(1)
    if(key < -1):
          cv2.destroyAllWindows()
          break
    
    #todo add exit
    frame_count += 1
   
videoCap.release()




