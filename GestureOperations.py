import itertools
import mediapipe as mp
import cv2
import pyautogui
import Gestures

from scipy.spatial import distance as dist


class GestureOperations:

    def __init__(self, lefClickGesture, rightClickGesture, dragGesture, doubleClickGesture):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mpFaceMesh = mp.solutions.face_mesh
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.faceMesh = self.mpFaceMesh.FaceMesh()
        self.camera = cv2.VideoCapture(0)

        self.LEFT_EYE_INDEXES = list(set(itertools.chain(*self.mp_face_mesh.FACEMESH_LEFT_EYE)))
        self.RIGHT_EYE_INDEXES = list(set(itertools.chain(*self.mp_face_mesh.FACEMESH_RIGHT_EYE)))
        self.LIPS_INDEXES = list(set(itertools.chain(*self.mp_face_mesh.FACEMESH_LIPS)))

        self.eyeFrameThreshold = 8
        self.mouthFrameThreshold = 4

        self.leftFrameCounter = 0
        self.rightFrameCounter = 0
        self.mouthFrameCounter = 0
        self.bothEyeFrameCounter = 0

        self.leftEARThreshold = 0.70
        self.rightEARThreshold = 0.74
        self.mouthARThreshold = 1.10
        self.bothEARThreshold = 0.85

        self.double_click_gesture = doubleClickGesture
        self.left_click_gesture = lefClickGesture
        self.right_click_gesture = rightClickGesture
        self.drag_drop_gesture = dragGesture

        self.double_click_just_once = False
        self.left_click_just_once = False
        self.right_click_just_once = False
        self.drag_drop_just_once = False


    def calculateEAR(self, eyeIndexCoordinates):
        # RİGHT EYE
        rightEAR = (dist.euclidean(eyeIndexCoordinates[246], eyeIndexCoordinates[7]) +
                    dist.euclidean(eyeIndexCoordinates[161], eyeIndexCoordinates[163]) +
                    dist.euclidean(eyeIndexCoordinates[160], eyeIndexCoordinates[144]) +
                    dist.euclidean(eyeIndexCoordinates[159], eyeIndexCoordinates[145]) +
                    dist.euclidean(eyeIndexCoordinates[158], eyeIndexCoordinates[153]) +
                    dist.euclidean(eyeIndexCoordinates[157], eyeIndexCoordinates[154]) +
                    dist.euclidean(eyeIndexCoordinates[173], eyeIndexCoordinates[155])) / \
                   dist.euclidean(eyeIndexCoordinates[33], eyeIndexCoordinates[133])

        leftEAR = (dist.euclidean(eyeIndexCoordinates[398], eyeIndexCoordinates[382]) +
                   dist.euclidean(eyeIndexCoordinates[384], eyeIndexCoordinates[381]) +
                   dist.euclidean(eyeIndexCoordinates[385], eyeIndexCoordinates[380]) +
                   dist.euclidean(eyeIndexCoordinates[386], eyeIndexCoordinates[374]) +
                   dist.euclidean(eyeIndexCoordinates[387], eyeIndexCoordinates[373]) +
                   dist.euclidean(eyeIndexCoordinates[388], eyeIndexCoordinates[390]) +
                   dist.euclidean(eyeIndexCoordinates[466], eyeIndexCoordinates[249])) / \
                  dist.euclidean(eyeIndexCoordinates[362], eyeIndexCoordinates[263])

        return rightEAR, leftEAR, rightEAR+leftEAR

    def calculateMAR(self, mouthIndexCoordinates):
        mouthAR = (dist.euclidean(mouthIndexCoordinates[191], mouthIndexCoordinates[95]) +
                   dist.euclidean(mouthIndexCoordinates[80], mouthIndexCoordinates[88]) +
                   dist.euclidean(mouthIndexCoordinates[81], mouthIndexCoordinates[178]) +
                   dist.euclidean(mouthIndexCoordinates[82], mouthIndexCoordinates[87]) +
                   dist.euclidean(mouthIndexCoordinates[13], mouthIndexCoordinates[14]) +
                   dist.euclidean(mouthIndexCoordinates[312], mouthIndexCoordinates[317]) +
                   dist.euclidean(mouthIndexCoordinates[311], mouthIndexCoordinates[402]) +
                   dist.euclidean(mouthIndexCoordinates[310], mouthIndexCoordinates[318]) +
                   dist.euclidean(mouthIndexCoordinates[415], mouthIndexCoordinates[324])) / \
                  dist.euclidean(mouthIndexCoordinates[78], mouthIndexCoordinates[308])

        return mouthAR

    def start(self):
        with self.mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as face_mesh:
            while self.camera.isOpened():
                success, frame = self.camera.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_mesh_results = face_mesh.process(frame)
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if face_mesh_results.multi_face_landmarks:
                    # Draw the face mesh annotations on the image.

                    landmarks = face_mesh_results.multi_face_landmarks[0]

                    if landmarks:
                        coordinatesOfEyeIndexes = {}
                        coordinatesOfLipsIndexes = {}
                        for num, landmark in enumerate(landmarks.landmark):
                            # print(landmark)
                            x = landmark.x
                            y = landmark.y
                            relative_x = x * frame.shape[1]
                            relative_y = y * frame.shape[0]

                            if num in self.RIGHT_EYE_INDEXES:
                                # cv2.putText(frame, str(num), (int(relative_x), int(relative_y)), cv2.FONT_HERSHEY_SIMPLEX,0.18, (0, 255, 0), 0, cv2.LINE_AA)
                                coordinatesOfEyeIndexes[num] = (int(relative_x), int(relative_y))

                            if num in self.LEFT_EYE_INDEXES:
                                coordinatesOfEyeIndexes[num] = (int(relative_x), int(relative_y))

                            if num in self.LIPS_INDEXES:
                                coordinatesOfLipsIndexes[num] = (int(relative_x), int(relative_y))

                    self.rightEAR, self.leftEAR, self.bothEAR = self.calculateEAR(coordinatesOfEyeIndexes)
                    self.mouthAR = self.calculateMAR(coordinatesOfLipsIndexes)

                    # cv2.putText(frame, f"Left EAR: %.2f" % leftEAR, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    #             (180, 255, 255), 2)
                    # cv2.putText(frame, f"Right EAR: %.2f" % rightEAR, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    #             (180, 255, 255),
                    #             2)
                    # cv2.putText(frame, f"MAR: %.2f" % mouthAR, (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    #             (180, 255, 255), 2)
                    # cv2.putText(frame, f"BothEAR: %.2f" % bothEAR, (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    #             (180, 255, 255), 2)

                    if self.bothEAR < self.bothEARThreshold:
                        self.bothEyeFrameCounter += 1
                        # cv2.putText(frame, 'Both eye Closed', (20, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
                    else:
                        if self.leftEAR < self.leftEARThreshold:
                            self.leftFrameCounter += 1
                            # cv2.putText(frame, 'Left Eye Closed', (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255),1)

                        if self.rightEAR < self.rightEARThreshold:
                            self.rightFrameCounter += 1
                            # cv2.putText(frame, 'Right Eye Closed', (20, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0, 0, 255), 1)

                    if self.mouthAR > self.mouthARThreshold:
                        self.mouthFrameCounter += 1
                        # cv2.putText(frame, 'Mouth Open', (20, 2260), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

                    self.left_click()
                    self.right_click()
                    self.double_click()
                    self.drag_drop()

    def left_click(self):
        if self.left_click_gesture is Gestures.Gestures.LEFTBLINK:
            if self.leftFrameCounter > self.eyeFrameThreshold:
                if not self.left_click_just_once:
                    pyautogui.click(button='left')
                    self.left_click_just_once = True
                if not self.leftEAR < self.leftEARThreshold:
                    self.leftFrameCounter = 0
                    self.left_click_just_once = False

        if self.left_click_gesture is Gestures.Gestures.RIGHTBLINK:
            if self.rightFrameCounter > self.eyeFrameThreshold:
                if not self.left_click_just_once:
                    pyautogui.click(button='left')
                    self.left_click_just_once = True
                if not self.rightEAR < self.rightEARThreshold:
                    self.rightFrameCounter = 0
                    self.left_click_just_once = False

        if self.left_click_gesture is Gestures.Gestures.BOTHEYEBLINK:
            if self.bothEyeFrameCounter > self.eyeFrameThreshold:
                if not self.left_click_just_once:
                    pyautogui.click(button='left')
                    self.left_click_just_once = True
                if not self.bothEAR < self.bothEARThreshold:
                    self.bothEyeFrameCounter = 0
                    self.left_click_just_once = False

        if self.left_click_gesture is Gestures.Gestures.MOUTHOPEN:
            if self.mouthFrameCounter > self.mouthFrameThreshold:
                if not self.left_click_just_once:
                    pyautogui.click(button='left')
                    self.left_click_just_once = True
                if not self.mouthAR > self.mouthARThreshold:
                    self.mouthFrameCounter = 0
                    self.left_click_just_once = False

    def right_click(self):
        if self.right_click_gesture is Gestures.Gestures.RIGHTBLINK:
            if self.rightFrameCounter > self.eyeFrameThreshold:
                if not self.right_click_just_once:
                    pyautogui.click(button='right')
                    self.right_click_just_once = True
                if not self.rightEAR < self.rightEARThreshold:
                    self.rightFrameCounter = 0
                    self.right_click_just_once = False

        if self.right_click_gesture is Gestures.Gestures.LEFTBLINK:
            if self.leftFrameCounter > self.eyeFrameThreshold:
                if not self.right_click_just_once:
                    pyautogui.click(button='right')
                    self.right_click_just_once = True
                if not self.leftEAR < self.leftEARThreshold:
                    self.leftFrameCounter = 0
                    self.right_click_just_once = False

        if self.right_click_gesture is Gestures.Gestures.BOTHEYEBLINK:
            if self.bothEyeFrameCounter > self.eyeFrameThreshold:
                if not self.right_click_just_once:
                    pyautogui.click(button='right')
                    self.right_click_just_once = True
                if not self.bothEAR < self.bothEARThreshold:
                    self.bothEyeFrameCounter = 0
                    self.right_click_just_once = False

        if self.right_click_gesture is Gestures.Gestures.MOUTHOPEN:
            if self.mouthFrameCounter > self.mouthFrameThreshold:
                if not self.right_click_just_once:
                    pyautogui.click(button='right')
                    self.right_click_just_once = True
                if not self.mouthAR > self.mouthARThreshold:
                    self.mouthFrameCounter = 0
                    self.right_click_just_once = False

    def drag_drop(self):
        if self.drag_drop_gesture is Gestures.Gestures.MOUTHOPEN:
            if self.mouthFrameCounter > self.mouthFrameThreshold:
                if not self.drag_drop_just_once:
                    pyautogui.mouseDown(button='left')
                    self.drag_drop_just_once = True
                if not self.mouthAR > self.mouthARThreshold:
                    pyautogui.mouseUp(button='left')
                    self.mouthFrameCounter = 0
                    self.drag_drop_just_once = False

        if self.drag_drop_gesture is Gestures.Gestures.LEFTBLINK:
            if self.leftFrameCounter > self.eyeFrameThreshold:
                if not self.drag_drop_just_once:
                    pyautogui.mouseDown(button='left')
                    self.drag_drop_just_once = True
                if not self.leftEAR < self.leftEARThreshold:
                    pyautogui.mouseUp(button='left')
                    self.leftFrameCounter = 0
                    self.drag_drop_just_once = False

        if self.drag_drop_gesture is Gestures.Gestures.RIGHTBLINK:
            if self.rightFrameCounter > self.eyeFrameThreshold:
                if not self.drag_drop_just_once:
                    pyautogui.mouseDown(button='left')
                    self.drag_drop_just_once = True
                if not self.rightEAR < self.rightEARThreshold:
                    pyautogui.mouseUp(button='left')
                    self.rightFrameCounter = 0
                    self.drag_drop_just_once = False

    def double_click(self):
        if self.double_click_gesture is Gestures.Gestures.BOTHEYEBLINK:
            if self.bothEyeFrameCounter > self.eyeFrameThreshold:
                if not self.double_click_just_once:
                    pyautogui.doubleClick(button='left')
                    self.double_click_just_once = True
                if not self.bothEAR < self.bothEARThreshold:
                    self.bothEyeFrameCounter = 0
                    self.double_click_just_once = False

        if self.double_click_gesture is Gestures.Gestures.MOUTHOPEN:
            if self.mouthFrameCounter > self.mouthFrameThreshold:
                if not self.double_click_just_once:
                    pyautogui.doubleClick(button='left')
                    self.double_click_just_once = True
                if not self.mouthAR > self.mouthARThreshold:
                    self.mouthFrameCounter = 0
                    self.double_click_just_once = False

        if self.double_click_gesture is Gestures.Gestures.LEFTBLINK:
            if self.leftFrameCounter > self.eyeFrameThreshold:
                if not self.double_click_just_once:
                    pyautogui.doubleClick(button='left')
                    self.double_click_just_once = True
                if not self.leftEAR < self.leftEARThreshold:
                    self.leftFrameCounter = 0
                    self.double_click_just_once = False

        if self.double_click_gesture is Gestures.Gestures.RIGHTBLINK:
            if self.rightFrameCounter > self.eyeFrameThreshold:
                if not self.double_click_just_once:
                    pyautogui.doubleClick(button='left')
                    self.double_click_just_once = True
                if not self.rightEAR < self.rightEARThreshold:
                    self.rightFrameCounter = 0
                    self.double_click_just_once = False


    def stop(self):
        self.camera.release()

        # cv2.imshow('Gesture Detection', cv2.flip(frame, 1))
        # cv2.imshow('Gesture Detection', self.frame)
