from customtkinter import *
import cv2
from PIL import Image, ImageTk
import os
import numpy as np
import mediapipe as mp

class SignLanguageTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Translator")

        # Variables
        self.recording = False
        self.recorded_data = ""

        # Webcam variables
        self.cap = None
        self.panel = None

        # Interface 1
        self.interface1()

    def interface1(self):
        self.frame1 = CTkFrame(self.root)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.add_padding(self.frame1, 20)

        # Get the path to the image file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "kmutnb.jpg")

        # Load and resize the image
        image = Image.open(image_path)
        image = image.resize((300, 200), Image.ANTIALIAS)  # Resize image to fit within (300, 200)
        img_tk = ImageTk.PhotoImage(image)

        # Create and display the image
        label_image = CTkLabel(self.frame1, image=img_tk)
        label_image.image = img_tk
        label_image.pack(pady=10)

        label = CTkLabel(self.frame1, text="Welcome to the Sign Language Translator")
        label.pack(pady=10)

        translate_button = CTkButton(self.frame1, text="Click for Translate", command=self.translate_and_record)
        translate_button.pack()

    def interface2(self):
        # Destroy previous frames
        if hasattr(self, 'frame1'):
            self.frame1.destroy()

        self.frame2 = CTkFrame(self.root)
        self.frame2.grid(row=0, column=0, sticky="nsew")
        self.add_padding(self.frame2, 20)

        # Initialize mediapipe holistic model
        self.holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Webcam feed
        self.cap = cv2.VideoCapture(0)
        self.panel = CTkLabel(self.frame2)
        self.panel.pack()

        recording_label = CTkLabel(self.frame2, text="Recording, please do the pose")
        recording_label.pack(pady=10)

        back_to_main_button = CTkButton(self.frame2, text="Back to First Page", command=self.back_to_interface1)
        back_to_main_button.pack()

        # Start capturing video
        self.capture_video()

    def translate_and_record(self):
        # Simulating translation result
        self.recorded_data = "Kwai"
        self.interface2()

    def start_recording(self):
        self.recording = True
        self.recorded_data = ""

    def stop_recording(self):
        self.recording = False
        if self.cap:
            self.cap.release()

    def capture_video(self):
        if self.frame2 is None:
            # If not in interface2, return without capturing video
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process frame with mediapipe
            frame, results = self.mediapipe_detection(frame)

            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(img)
            self.panel.configure(image=img_tk)
            self.panel.image = img_tk

            if self.recording:
                # Process the frame data (you need to implement pose detection logic here)
                # For now, let's assume it's being recorded as text
                self.recorded_data += "Dummy Text "

            # Repeat the process
            self.root.after(10, self.capture_video)
        else:
            if self.cap:
                self.cap.release()

    def mediapipe_detection(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
        image.flags.writeable = False                  # Image is no longer writeable
        results = self.holistic.process(image)         # Make prediction
        image.flags.writeable = True                   # Image is now writeable 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
        self.draw_landmarks(image, results)            # Draw landmarks on image
        return image, results

    def draw_landmarks(self, image, results):
        mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks, mp.solutions.holistic.POSE_CONNECTIONS)
        mp.solutions.drawing_utils.draw_landmarks(image, results.left_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)
        mp.solutions.drawing_utils.draw_landmarks(image, results.right_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)

    def add_padding(self, widget, amount):
        # Adds padding around the specified widget
        for side in ("top", "bottom", "left", "right"):
            widget.grid_configure(padx=amount, pady=amount)
            # Configure padding on all sides of the widget

    def back_to_interface1(self):
        # Command for the "Back to First Page" button in interface2
        self.stop_recording()  # Stop recording and release webcam
        self.interface1()      # Go back to interface1

if __name__ == "__main__":
    root = CTk()
    app = SignLanguageTranslator(root)
    root.mainloop()
