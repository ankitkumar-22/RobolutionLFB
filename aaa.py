import cv2
import numpy as np
from serial import Serial

ser = Serial(port='COM5', baudrate=9600, timeout=1)

#PID parameters
kp = 0.5
ki = .1
kd = 0.2

prev_error = 0
integral =0


cap = cv2.VideoCapture(0)
cap.set(3, 160)
w = 160
cap.set(4, 120)
while True:
    ret, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(imgGray, (5, 5), 0)

    high_b = np.uint8([5])
    low_b = np.uint8([0])
    mask = cv2.inRange(imgGray, low_b, high_b)
    contours, hierarchy = cv2.findContours(image=mask, mode=1, method=cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print("CX : " + str(cx) + "CY" + str(cy))


            error = w - cx
            integral += error
            derivative = error - prev_error

            control = int(kp * error + ki * integral + kd * derivative)
            ser.write(f"{cx}\n".encode())
            prev_error = error


            """ 
            Previous code
            if cx >= 120:
                print("Turn Left")
                ser.write(bytes(str('l'), 'utf-8'))
            if cx < 120 and cx > 40:
                print("On track")
                ser.write(bytes(str('f'), 'utf-8'))
            if cx < 40:
                print("Turn Right")
                ser.write(bytes(str('r'), 'utf-8'))
             """
            cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)

    cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                     lineType=cv2.LINE_AA)
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()