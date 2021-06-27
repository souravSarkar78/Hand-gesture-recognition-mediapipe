import cv2

import mediapipe as mp

mpHands = mp.solutions.hands

hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)

mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


thumb_tip = 4

tips = [8, 12, 16, 20]

rock = [1, 0, 0, 1]
victory = [1, 1, 0, 0]
closed = [0, 0, 0, 0]
opened = [1, 1, 1, 1]

def gesture(landmarks):
    if landmarks:
        tip_state = []
        for i in (tips):
            if landmarks[i][1] < landmarks [i-2][1]:
                tip_state.append(1)
            else:
                tip_state.append(0)

        if tip_state == rock:
            print("rock")
        elif tip_state == victory:
            print("victory")
        
        elif tip_state == closed:
            if landmarks[thumb_tip][1] < landmarks[tips[0]][1]:
                print("ok")
            elif landmarks[thumb_tip][1] > landmarks[tips[3]][1]:
                print("Not Ok")
            else:
                print("closed")

        else:
            print("nothing matched")

while True:
    _, frame = cap.read()

    x, y, c = frame.shape

    frame = cv2.flip(frame, 1)

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(framergb)

    # print(result)
    
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)


            # print(landmarks)
        # g = gesture(landmarks)
        

    # print(landmarks)
    cv2.imshow("Output", frame) 

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()