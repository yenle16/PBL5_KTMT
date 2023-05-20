from builtins import print, property
from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import sqlite3
import numpy
import os
from time import sleep
from tkinter import messagebox
from threading import Thread
import shutil
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import time
from Trainning import recognizer
import pandas as pd
from openpyxl.workbook import Workbook
from facenet_pytorch import MTCNN
from mtcnn import MTCNN


import tensorflow as tf
import argparse
import os
import sys
import math
import pickle
import numpy as np
import cv2
import collections
from sklearn.svm import SVC
import ActionDB
windown = Tk()
windown.title("Nhận Diện Khuôn Mặt Và Hỗ Trợ Điểm Danh Sinh Viên Train")
windown.geometry("1570x700")

video = cv2.VideoCapture(0)

canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)


canvas = Canvas(windown, width = canvas_w, height = canvas_h)
canvas.pack(fill=BOTH)

#frame result

frame_result = tk.LabelFrame(windown, text="Kết Quả", font=("Arial", 15, "bold"))
frame_result.place(x=0,y=250)

lbl_name_result = Label(frame_result,text="Tên sinh viên: ", font=("Arial", 12))
lbl_name_result.grid(column=0, row=1)
lbl_name_result_after = Label(frame_result, foreground="#F72121", font=("Arial", 12))
lbl_name_result_after.grid(column=1, row=1, sticky=W, pady=4)
lbl_mssv_result = Label(frame_result,text="Mã số sinh viên: ", font=("Arial", 12))
lbl_mssv_result.grid(column=0, row=2)
lbl_mssv_result_after = Label(frame_result, foreground="#F72121", font=("Arial", 12))
lbl_mssv_result_after.grid(column=1, row=2, sticky=W, pady=4)
lbl_lop_result = Label(frame_result,text="Lớp: ", font=("Arial", 12))
lbl_lop_result.grid(column=0, row=3)
lbl_lop_result_after = Label(frame_result, foreground="#F72121", font=("Arial", 12))
lbl_lop_result_after.grid(column=1, row=3, sticky=W, pady=4)

#frame insert

frame_insert = tk.LabelFrame(windown, text="Thêm dữ liệu", font=("Arial", 15, "bold"))
frame_insert.place(x=0,y=383)

lbl_name = Label(frame_insert, text="Mã số sinh viên: ", foreground="#1A6991", font=("Arial", 13))
lbl_name.grid(column=0, row=2)
txt_name = Entry(frame_insert, width=23)
txt_name.grid(column=1, row=2, sticky=W, pady=4)
mtcnn = MTCNN()


def input_Image():
    mssv = txt_name.get()
    result=ActionDB.input_ImageDB(mssv)
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    global canvas, photo, sampleNum, count
    # doc tu camera
    ret, frame = video.read()
    faces = mtcnn.detect_faces(frame)

    # resize
    # frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
    # convert mau
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray)
    result_name = result[1].replace(" ", "")
    for face in faces:
        x, y, w, h = face['box']
        # Vẽ 1 đường bao quanh khuôn mặt
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Cắt và lưu ảnh khuôn mặt
        face_image = frame[y:y+h, x:x+w]
        cv2.imwrite("DataSetMTCNN/" + str(result_name) + "_" + str(result[0]) + '/Student_' + str(result[0]) + '_' + str(sampleNum) + '.jpg', face_image)

    # for (x, y, w, h) in faces:
    #     # vẽ 1 đường bao quanh khuôn mặt
    #     cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #     cv2.imwrite("DataSetMTCNN/" + str(result_name) + "_" + str(result[0]) + '/Student_' + str(result[0]) + '_' + str(sampleNum) + '.jpg', gray[y:y + h, x:x + w])
    
    if len(faces) == 0:
        messagebox.showinfo("Thêm sinh viên",
                            "Hệ thống tạm dừng vì không nhận diện được khuôn mặt bạn. Vui lòng thử lại!!!")
        sampleNum = 0
        count = 0
        if not os.path.exists('DataSetMTCNN/' + str(result_name) + "_" + str(mssv)):
            pass
        else:
            path = os.path.join(
                'DataSetMTCNN/' + str(result_name) + "_" + str(result[0]))
            shutil.rmtree(path)
        return
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    if not os.path.exists('DataSetMTCNN/' + str(result_name) + "_" + str(mssv)):
        os.makedirs('DataSetMTCNN/' + str(result_name) + "_" + str(mssv))
    sampleNum += 1
    count += 1
    if count == 5:
        messagebox.showinfo("Thêm sinh viên", "Thêm sinh viên thành công")
        windown.after(15, windown.destroy)
    print(count)
    windown.after(500, input_Image)


def nhandien():
    global mssv
    arr_mssv=ActionDB.nhandienDB()
    mssv = txt_name.get()
    exists = 0
    for item in arr_mssv:
        if mssv == item:
            exists = 1
    if exists == 0:
        messagebox.showinfo("Thêm sinh viên",
                            "Vui lòng nhập đúng mã số sinh viên !!!", icon='warning')
        return

    root = 'dataSetMTCNN'
    arr_path = os.listdir(root)
    check = False
    for path in arr_path:
        mssv_in_dataSet = path.split('_')[1]
        if mssv == mssv_in_dataSet:
            check = True
            break
    if check == True:
        check_update = messagebox.askquestion("Thêm Dữ Liệu", "Dữ Liệu Của Bạn Đã Tồn Tại. Ấn 'Yes' Nếu Bạn Muốn Update Dữ Liệu?", icon='question')
        if check_update == "no":
            return
        else:
            input_Image()
    input_Image()

button_insert = tk.Button(frame_insert, text="Submit", bg="#13CA38", command= nhandien, font=("Arial", 13, "bold"),  borderwidth=2, relief="groove")
button_insert.grid(column=1, row=8, pady=10, sticky=W)
# button.place(relx=0.0, rely=0.0, anchor=NW)

photo = None
sampleNum = 0
count = 0

def update_frame():
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    global canvas, photo
    #doc tu camera
    ret, frame = video.read()
    faces = mtcnn.detect_faces(frame)
    for face in faces:
        x, y, w, h = face['box']
        # Vẽ 1 đường bao quanh khuôn mặt
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Cắt và lưu ảnh khuôn mặt
        # face_image = frame[y:y+h, x:x+w]
        # cv2.imwrite("DataSetMTCNN/" + str(result_name) + "_" + str(result[0]) + '/Student_' + str(result[0]) + '_' + str(sampleNum) + '.jpg', face_image)


    #resize
    # frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
    #convert mau
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # # faces = face_cascade.detectMultiScale(gray)
    # for (x, y, w, h) in faces:
    #     # vẽ 1 đường bao quanh khuôn mặt
    #     cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #convert thanh imgaetk
    # Convert màu từ BGR sang RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Tạo đối tượng hình ảnh từ mảng numpy đã chuyển đổi màu
    image = PIL.Image.fromarray(rgb)

    # Tạo đối tượng PhotoImage từ hình ảnh để hiển thị trên canvas
    photo = PIL.ImageTk.PhotoImage(image=image)

    # photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    #show
    canvas.create_image(0,0, image = photo, anchor=tkinter.NW)
    windown.after(15, update_frame)

update_frame()


windown.mainloop()
