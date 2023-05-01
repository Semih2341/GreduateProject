import time
import cv2
import Metamotion as mm
import dlib
import imutils
import pyautogui
import numpy as np
from imutils import face_utils
from imutils.video import FileVideoStream, VideoStream
from scipy.spatial import distance as dist


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

LeftCounter = 0
RightCounter = 0

print("Loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


print("Starting video stream thread...")
vs = VideoStream(src=0).start()
time.sleep(1.0)

MetaMotion = mm.Metamotion()
MetaMotion.configure_device()
MetaMotion.start_acc_gyro()

while True:

    if not vs.read().any():
        break

    frame = vs.read()
    frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)

    for rect in rects:

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if leftEAR < EYE_AR_THRESH:
            LeftCounter += 1

        else:

            if LeftCounter >= EYE_AR_CONSEC_FRAMES:
                pyautogui.click()
            LeftCounter = 0


        if rightEAR < EYE_AR_THRESH:
            RightCounter += 1
        else:

            if RightCounter >= EYE_AR_CONSEC_FRAMES:
                pyautogui.rightClick()

            RightCounter = 0

        # cv2.putText(
        #     frame,
        #     "Blinks: {}".format(TOTAL),
        #     (10, 30),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.7,
        #     (255, 0, 255),
        #     2,
        # )

        print("EAR: {:.2f}".format(ear))


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


cv2.destroyAllWindows()

MetaMotion.disconnect_device()

vs.stop()