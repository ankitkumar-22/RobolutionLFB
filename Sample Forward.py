import cv2
from serial import Serial

cap = cv2.VideoCapture(0)

cap.set(3, 160)
cap.set(4, 120)
ser = Serial('COM3', 9600) # For serial communication with the arduino


# The function below pre-process the image to make sure that contour detection is as perfect as possible and eliminating background noise 
def preprocess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgThresh = cv2.threshold(imgBlur, 40, 255, cv2.THRESH_BINARY_INV)[1]
    return imgThresh


# Helps detecting the contours and finding out whether the bot is moving on the track 
def compute(img):
    contours, h = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Following line of code gives the largest contour in the pre-processed frames
    # This is done so that only the path of the bot is detected and the noise would be refrained
    if contours:
        biggestcnt = max(contours, key=cv2.contourArea)
        cv2.drawContours(imgcontour, [biggestcnt], -1, (255, 0, 255), 3)

        # Method of moments to find the centroid of the contour and the drawing an indicating point
        mo = cv2.moments(biggestcnt)
        cx = int(mo["m10"] / (mo["m00"] + 1e-5))
        cy = int(mo["m01"] / (mo["m00"] + 1e-5))
        cv2.circle(imgcontour, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        # Calculating the error based on segmentation of frames into 3 parts
        # Error is 0 when indicating point is between 260 and 380
        # Error is negative when the indicating point is beyond 380
        # Error is positive when the indicating point is below 260
        error = 0
        if cx > 380:
            print("left")
            error = frame_width / 2 - cx
            ser.write(bytes(str('L'), 'utf-8'))
        elif 260 <= cx <= 380:
            print("on track")
            ser.write(bytes(str('F'), 'utf-8'))
        elif cx < 260:
            print("right")
            error = frame_width / 2 - cx
            ser.write(bytes(str('R'), 'utf-8'))

        print(error)

while True:
    ret, img = cap.read()
    frame_height, frame_width, channels = img.shape
    print(frame_width, frame_height)

    imgcontour = img.copy()
    imgpreproc = preprocess(img)
    compute(imgpreproc)
    cv2.line(imgcontour, (260, 480), (260, 0), (0, 255, 0), thickness=5)
    cv2.line(imgcontour, (380, 480), (380, 0), (0, 255, 0), thickness=5)  # Two Lines for Visual Reference
    cv2.imshow("Path", imgcontour)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # use 'q' button to quit
        break

cap.release()
cv2.destroyAllWindows()
