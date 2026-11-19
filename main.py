# this is the mail file for CV as of now.
import cv2
from ultralytics import YOLO


# formating
# TODO make a log file
print("start of program")
print("______________________________________________")

yolo = YOLO("yolov8n.pt")


try:
    video_path = "rtsp://192.168.2.2:8554/video_stream__dev_video0"
    videoCap = cv2.VideoCapture(video_path)
except:
    pass  # this is handled later by a guard case

# Set camera to lowest resolution for faster capture.
# This is the part that makes it go fast
videoCap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
videoCap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
videoCap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


def drawFrame(fr):
    # this seems to be the fastest way to do this
    # that being said I cannot find documtation
    results = yolo.predict(fr, stream=True, imgsz=320, verbose=False)

    for result in results:
        for box in result.boxes:
            if box.conf[0] > 0.4:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cls = int(box.cls[0])
                class_name = result.names[cls]

                conf = float(box.conf[0])

                cv2.rectangle(fr, (x1, y1), (x2, y2), 2)

                cv2.putText(
                    fr,
                    f"{class_name} {conf:.2f}",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    2,
                )


while True:
    ret, frame = videoCap.read()
    if not ret:
        video_path = "/dev/video0"
        videoCap = cv2.VideoCapture(video_path)
        print("falling back to vidoe0")
        continue

    drawFrame(frame)
    key = cv2.waitKey(1)
    cv2.imshow("test", frame)

    if key == 27 or cv2.getWindowProperty("test", cv2.WND_PROP_VISIBLE) < 1:
        break


cv2.destroyAllWindows()
videoCap.release()
