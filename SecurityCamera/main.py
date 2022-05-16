import cv2
import time
import datetime

cap = cv2.VideoCapture(0)

# Use cascade provided by OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detect_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

# cap.get(3) gives width as float
# cap.get(4) gives height as float
frame_size = (int(cap.get(3)), int(cap.get(4)))

# Format to save video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

while True:
    # Underscore is a placeholder variable
    # Only care about the frame that is returned
    _, frame = cap.read()

    # Convert to grayscale because CV requires grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Image, Scale Factor, Minimum number of neighbors
    # Scale factor is a number that determines accuracy and speed of algorithm
    # Scale factor must be at least 1
    # Lower scale factor is more accurate but slower
    # Minimum number of neighbors tells you how many overlapping boxes must be detected
    # for something to be considered a face
    # Raise number if it is detecting non-face objects as faces
    # Lower number if it has difficulties detecting faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            # Video name, four character code, frame rate, frame size
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20.0, frame_size)
            print("Started recording")
    elif detection:
        if timer_started:
            if time.time() - detect_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print("Stopped recording")
        else:
            timer_started = True
            detect_stopped_time = time.time()

    if detection:
        out.write(frame)

    # # Draw rectangle on image to indicate faces
    # # frame is the image that you want to draw on
    # # (x,y) is the top left corner of the image
    # # (x + width, y + height) is the bottom right corner of the image
    # # (255, 0, 0) is BGR and gives the rectangle a blue color
    # # 3 is the line thickness in px
    # for (x, y, width, height) in faces:
    #     cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 5)

    # for (x, y, width, height) in bodies:
    #     cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 5)

    cv2.imshow("Camera", frame)

    # hit q key to end the while loop
    if cv2.waitKey(1) == ord('q'):
        break

# Save video and release resources
out.release()
cap.release()
cv2.destroyAllWindows()
