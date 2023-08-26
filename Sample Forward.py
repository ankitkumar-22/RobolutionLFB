import cv2
import numpy as np
from serial import Serial

# Initialize the serial connection
ser = Serial('COM5', 9600)

cap = cv2.VideoCapture(0)
cap.set(3,160)
cap.set(4,120)

while True:
    ret, img = cap.read()
    imgGray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(imgGray,(5,5),0)

    high_b = np.uint8([5])
    low_b = np.uint8([0])
    mask = cv2.inRange(imgGray , low_b , high_b)
    contours , hierarchy = cv2.findContours(image= mask, mode = 1,method = cv2.CHAIN_APPROX_NONE)
    if len(contours)>0:
        c= max(contours,key= cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"]!=0:
            cX = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            #print("CX : "+str(cX)+ "CY" + str(cy))
            if cX < 75:
                ser.write(bytes(str('L'), 'utf-8')) # Command to turn left
                print("CX : L " + str(cX) + "CY" + str(cy))
            elif cX >85:
                ser.write(bytes(str('R'), 'utf-8'))  # Command to turn right
                print("CX : R " + str(cX) + "CY" + str(cy))
            else:
                ser.write(bytes(str('F'), 'utf-8'))  # Command to move forward
                print("CX : F " + str(cX) + "CY" + str(cy))
            cv2.circle(img=frame, center=(cX,cy), radius=5, color=(255,255,255),thickness=-1)
    cv2.drawContours(image =frame,contours= contours , contourIdx =-1, color = (0,255,0),thickness =2,lineType=cv2.LINE_AA)
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cap.release()
ser.close()
cv2.destroyAllWindows()



