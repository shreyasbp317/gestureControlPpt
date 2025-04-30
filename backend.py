# backend.py
import cv2
import mediapipe as mp
import pyautogui
import time
import threading

class GestureBackend:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
        self.mp_drawing = mp.solutions.drawing_utils
        self.running = False
        self.cap = None
        self.stable_start = None
        self.last_action_time = 0
        self.cooldown = 1.0  # seconds

    def start_detection(self):
        if self.running:
            return
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop_detection(self):
        self.running = False
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()

    def _run(self):
        self.cap = cv2.VideoCapture(0)
        prev_gesture = None

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)

            feedback = "No gesture detected"
            gesture = None
            current_time = time.time()

            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                self.mp_drawing.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

                thumb_tip = hand.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
                index_tip = hand.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]

                dist = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5

                if dist < 0.03:
                    gesture = 'next'
                    feedback = "Pinch detected → NEXT slide"
                elif dist > 0.07:
                    gesture = 'prev'
                    feedback = "Fingers apart → PREVIOUS slide"

            # Gesture handling
            if gesture == prev_gesture:
                if self.stable_start and (current_time - self.stable_start > 0.5):
                    if gesture == 'next' and current_time - self.last_action_time > self.cooldown:
                        pyautogui.press('right')
                        feedback = "✅ NEXT SLIDE triggered"
                        self.last_action_time = current_time
                        self.stable_start = None
                    elif gesture == 'prev' and current_time - self.last_action_time > self.cooldown:
                        pyautogui.press('left')
                        feedback = "✅ PREVIOUS SLIDE triggered"
                        self.last_action_time = current_time
                        self.stable_start = None
            else:
                self.stable_start = current_time
                prev_gesture = gesture

            # Show feedback
            cv2.putText(frame, feedback, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            cv2.imshow("Gesture Presentation Controller", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.stop_detection()
