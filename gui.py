# gui.py
import tkinter as tk
from backend import GestureBackend

class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Presentation Controller")
        self.root.geometry("400x250")
        self.backend = GestureBackend()

        self.label = tk.Label(root, text="Control Presentations with Gestures!", font=("Arial", 14))
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start Gesture Control", command=self.start_gesture)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Gesture Control", command=self.stop_gesture)
        self.stop_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=10)

    def start_gesture(self):
        self.backend.start_detection()
        self.label.config(text="Gesture Detection Running...")

    def stop_gesture(self):
        self.backend.stop_detection()
        self.label.config(text="Detection Stopped.")

    def exit_app(self):
        self.backend.stop_detection()
        self.root.destroy()
