import cv2
import numpy as np
import tkinter as tk
import PIL
from PIL import ImageTk

#############################################
#   Plays video with button to select fram  #
#############################################

class VideoPlayer:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tk.Button(window, text="Select Color", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            ColorRange(frame)

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

        self.window.after(self.delay, self.update)

###############################
#   Selects frame from video  #
###############################
class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
             self.vid.release()

#################################################################
#   Allows user to pick color of whiteboard from fram in video  #
#################################################################
class ColorRange:
    hsvValue = [-1, -1]
    imgHSV = None
    def __init__(self, frame):
        self.img = frame

        global imgHSV

        imgHSV = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        scaled = cv2.resize(self.img, None, fx=1, fy=1)

        cv2.imshow('scaled', scaled)

        # Needs to match the name of the window showing image
        cv2.setMouseCallback('scaled', self.colorPicker)

    def colorPicker(self, event, x, y, flags, param):
        # Double click to get color values of pixel
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print('Left Double Clicked in image')
            hsvValue = imgHSV[y,x]
            #print('hsvValue: ' + str(hsvValue))
            print('Detected Color: ' + str(hsvValue[0]) + ', ' + str(hsvValue[1]) + ', ' + str(hsvValue[2]))

            return hsvValue


if __name__ == "__main__":
    # Create a window and pass it to the Application object
    VideoPlayer(tk.Tk(), "Tkinter and OpenCV", 'video.m4v')
    
