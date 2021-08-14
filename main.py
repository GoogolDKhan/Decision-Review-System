'''
Author  : Sarfaraz
Date    : 17/05/2021
Purpose : Third Project
pip install opencv-python
pip install pillow
pip install imutils
'''

import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
from functools import partial
import threading
import imutils
import time

stream = cv2.VideoCapture("video/match.mp4")
flag = True


def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")

    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    if flag:
        canvas.create_text(134, 26, fill="red",
                           font="Times 26 bold", text="Decision Pending")
    flag = not flag


def pending(decision):

    # 1.Display decision pending image
    frame = cv2.cvtColor(cv2.imread("images/pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)

    # 2.Wait for 2 second
    time.sleep(2)

    # 3.Display sponsor image
    frame = cv2.cvtColor(cv2.imread("images/sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)

    # 4.Wait for 2 second
    time.sleep(2)

    # 5.Display Out/NotOut image
    if decision == 'out':
        decisionImg = "images/out.png"
    else:
        decisionImg = "images/not_out.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)


def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("player is out")


def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("player is not out")


# Width and height of main screen
SET_WIDTH = 650
SET_HEIGHT = 400

# Tkinter GUI starts here
window = tkinter.Tk()
window.title("Sarfaraz's Decision Review Kit")
cv_img = cv2.cvtColor(cv2.imread("images/welcome.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()


# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous (fast)",
                     width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)",
                     width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (slow) >>",
                     width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast) >>",
                     width=50, command=partial(play, +25))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()

window.mainloop()
