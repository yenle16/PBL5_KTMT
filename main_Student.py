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
windown.title("Nhận Diện Khuôn Mặt Và Hỗ Trợ Điểm Danh Sinh Viên")
windown.geometry("1570x700")

# video = cv2.VideoCapture("http://10.10.53.128:81/stream")
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



photo = None
sampleNum = 0
count = 0

def update_frame():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    global canvas, photo
    #doc tu camera
    ret, frame = video.read()
    #resize
    frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
    #convert mau
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_cascade.detectMultiScale(gray)
    for (x, y, w, h) in faces:
        # vẽ 1 đường bao quanh khuôn mặt
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #convert thanh imgaetk
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(gray))
    #show
    canvas.create_image(0,0, image = photo, anchor=tkinter.NW)
    windown.after(15, update_frame)



def getDataCBB():
 
    tenGV=cbb_gv.get()
    maGV=ActionDB.getmaGVbytenGV(tenGV)[0]

    tenHocki=cbb_hocki.get()
    maHocki=ActionDB.getmaHockibytenHocki(tenHocki)[0]

    tenMonhoc=cbb_mon.get()
    maMonhoc=ActionDB.getmaMonhocbytenMonhoc(tenMonhoc)[0]

    return (maGV,maHocki,maMonhoc)

def show_svdiemdanh():
    result_data = getDataCBB()
    maGV,maHocki,maMonhoc=getDataCBB()

    print(result_data)

    now = datetime.now()
    ngay_diemdanh = now.strftime("%d-%m-%Y")
    kqua_sv_diemdanh=ActionDB.show_svdiemdanh(maGV,maHocki,maMonhoc,ngay_diemdanh)

    print (kqua_sv_diemdanh)
    # print(kqua_sv_diemdanh)
    mylist_sv_dihoc.delete(0,END)
    for item in kqua_sv_diemdanh:
        if item[4] == result_data[0]:
            mylist_sv_dihoc.insert(END, item[0] + "_" + item[1] + "/" + item[2]+ " " + item[3])


def diemdanh():
    current_monhoc = cbb_mon.get()
    count = 0
    for i in cbb_mon['values']:
        # print(i)
        if current_monhoc == i:
            count += 1
    if count == 0:
        messagebox.showinfo("Điểm Danh",
                            "Vui lòng chọn lớp học trước khi điểm danh!!!", icon='warning')
        return
    rec = recognizer.read("recognizer/training.yml")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # cap = cv2.VideoCapture(0)
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    global canvas, photo
    # doc tu camera
    ret, frame = video.read()
    # resize
    frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
    # convert mau
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    tile = False
    mssv_after = ""
    for (x, y, w, h) in faces:
        # vẽ 1 đường bao quanh khuôn mặt
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        mssv, confidence = recognizer.predict(roi_gray)
        if confidence < 100:
            tile = True
            mssv_after = mssv
            break
    if len(faces) == 0:
        messagebox.showinfo("Thêm sinh viên",
                            "Hệ thống tạm dừng vì không nhận diện được khuôn mặt bạn. Vui lòng thử lại!!!", icon='warning')
        lbl_name_result_after.configure(text="")
        lbl_mssv_result_after.configure(text="")
        lbl_lop_result_after.configure(text="")
        return
    if tile == True:
        result = ActionDB.getData(mssv_after)
        data_mssvs = mylist_mssv.get(0, END)
        count_exists = 0
        for data_mssv in data_mssvs:
            if result[0] == data_mssv:
                count_exists += 1
        if count_exists == 0:
            messagebox.showinfo("Điểm Danh",
                                "Bạn không có trong lớp học này. Vui lòng chọn đúng lớp học !!!", icon='info')
            lbl_name_result_after.configure(text="")
            lbl_mssv_result_after.configure(text="")
            lbl_lop_result_after.configure(text="")
            return
        if (result != None):
            lbl_name_result_after.configure(text=result[1])
            lbl_mssv_result_after.configure(text=result[0])
            lbl_lop_result_after.configure(text=result[2])


            result_data = getDataCBB()

            now = datetime.now()
            gio_diemdanh = now.strftime("%H:%M:%S")
            ngay_diemdanh = now.strftime("%d-%m-%Y")

            kqua_check_svdiemdanh=ActionDB.diemdanh()
            for item in kqua_check_svdiemdanh:
                if item[0] == result[0] and item[1] == result_data[0] and item[2] == result_data[1] and item[3] == result_data[2] and item[4] == ngay_diemdanh:
                    messagebox.showinfo("Điểm Danh", "Bạn đã điểm danh !!!", icon='info')
                    return
            ActionDB.insert_diemdanh(result[0], result_data[0], result_data[1], result_data[2], gio_diemdanh, ngay_diemdanh)
            show_svdiemdanh()
    else:
        lbl_name_result_after.configure(text="Unknow")
        lbl_mssv_result_after.configure(text="Unknow")
        lbl_lop_result_after.configure(text="Unknow")
    # convert thanh imgaetk
    lbl_hiendien2.configure(text=mylist_sv_dihoc.size())
    vang = mylist.size() - mylist_sv_dihoc.size()
    lbl_vang2.configure(text=vang)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(gray))
    # show
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)


button_diemdanh = tk.Button(windown, text="Điểm Danh", bg="yellow", width=13,  font=("Arial", 15, "bold"), borderwidth=2, relief="raised", height=6 ,command=diemdanh)
button_diemdanh.place(x=350,y=10)

#frame time
frame_time = tk.LabelFrame(windown, text="Thời Gian", font=("Arial", 15, "bold"))
frame_time.place(x=550,y=10)

def runTime():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    lbl_time2.configure(text=hour+ ":" + minute + ":" + second)
    lbl_time2.after(1000, runTime)
lbl_time1 = Label(frame_time, text=f"{datetime.now():%a, %b %d %Y}", foreground="#E20A0A", font=("Arial", 10, "bold"), width=30)
lbl_time1.grid(column=0, row=0)
lbl_time2 = Label(frame_time, foreground="#E20A0A", font=("Arial", 10, "bold"), width=30)
lbl_time2.grid(column=0, row=1, pady=5)



def getDataGiangVien(event):
    khoa = cbb_khoa.get()

    maKhoa=ActionDB.getmaKhoabytenKhoa(khoa)[0]
    
    tenGiangVien=ActionDB.getGiangVienIDbyKhoa(maKhoa)


    cbb_gv['values'] = tenGiangVien


lbl_khoa =  tk.Label(windown, text="Khoa", foreground="#DA681D", font=("Arial", 13, "bold"))
lbl_khoa.place(x=350,y=195)
cbb_khoa = Combobox(windown, state="readonly")
cbb_khoa['values'] = ActionDB.getDataKhoa()
cbb_khoa.current(0)
cbb_khoa.bind("<<ComboboxSelected>>", getDataGiangVien)
cbb_khoa.place(x = 350, y=220)


def getDataHocKi(event):
    # giangvien = cbb_gv.get()
    tenGV=cbb_gv.get()
    maGV=ActionDB.getmaGVbytenGV(tenGV)

    tenHocki=ActionDB.gettenHockibymaGV(maGV)

    cbb_hocki['values'] = tenHocki



def getDataMonHoc_GiangVien(event):
    count_hocki = 0
    for i in cbb_hocki['values']:
        if cbb_hocki.get() == i:
            count_hocki += 1
    if count_hocki == 0:
        cbb_mon['state'] = 'readonly'
    hocki = cbb_hocki.get()
    giangvien = cbb_gv.get()


    result_name_mh = []

    result_name_mh=ActionDB.getDataMonHoc_GiangVien(giangvien,hocki)
    cbb_mon['values'] = result_name_mh

#Giangvien
lbl_gv =  Label(windown, text="Giảng viên", foreground="#DA681D", font=("Arial", 13, "bold"))
lbl_gv.place(x=540,y=195)
cbb_gv = Combobox(windown, state="readonly")
cbb_gv.bind("<<ComboboxSelected>>", getDataHocKi)
cbb_gv.place(x = 540, y=220)

#hoc ki
lbl_hocki =  Label(windown, text="Học kì", foreground="#DA681D", font=("Arial", 13, "bold"))
lbl_hocki.place(x=730,y=195)
cbb_hocki = Combobox(windown, state="readonly")
cbb_hocki.bind("<<ComboboxSelected>>", getDataMonHoc_GiangVien)
cbb_hocki.place(x = 730, y=220)



def getDataLopHoc_Hocki(event):
    show_svdiemdanh()

    monhoc = cbb_mon.get()

    idMonhoc = ActionDB.getmaMonhocbytenMonhoc(monhoc)[0]

    


    cbb_hocki['values'] = ActionDB.gettenHockibymaMonhoc(idMonhoc)

    tenGV = cbb_gv.get()

    msgv = ActionDB.getmaGVbytenGV(tenGV)[0]

    hocki = cbb_hocki.get()


    result_name_sv,result_mssv=ActionDB.getSVbyMonhocGVHocki(idMonhoc, msgv, hocki)
    mylist.delete(0, END)
    mylist_mssv.delete(0, END)
    for line_name in result_name_sv:
        mylist.insert(END, str(line_name))

    for line_mssv in result_mssv:
        mylist_mssv.insert(END, str(line_mssv))

    
    lbl_tongso2.configure(text=mylist.size())
    lbl_hiendien2.configure(text=mylist_sv_dihoc.size())
    vang = mylist.size() - mylist_sv_dihoc.size()
    lbl_vang2.configure(text=vang)

def dangnhap():
    windown.destroy()
    import login

button_dangnhap = tk.Button(windown, text="Đăng nhập", background="#4BF6CE", font=("Arial", 13, "bold"), borderwidth=2, relief="raised", width=20, command=dangnhap)
button_dangnhap.place(x=1050,y=20)



#Mon hoc
lbl_mon =  Label(windown, text="Môn Học", foreground="#DA681D", font=("Arial", 13, "bold"))
lbl_mon.place(x=920,y=195)
cbb_mon = Combobox(windown, state='disabled')
cbb_mon.bind("<<ComboboxSelected>>", getDataLopHoc_Hocki)
cbb_mon.place(x = 920, y=220)

#Danh sach lop hoc
lbl_listclass =  Label(windown, text="Danh Sách Lớp Học", foreground="red", font=("Arial", 13, "bold"))
lbl_listclass.place(x=350,y=287)
list_class = Scrollbar(windown)
list_class.place(x=351,y=313)
mylist = Listbox(windown, width=40, bg="#EDFC8F", yscrollcommand=list_class.set)
mylist.place(x=350,y=313)

#Ma so sinh vien
lbl_listmssv =  Label(windown, text="Mã Số Sinh Viên", foreground="red", font=("Arial", 13, "bold"))
lbl_listmssv.place(x=680,y=287)
list_mssv = Scrollbar(windown)
list_mssv.place(x=681,y=313)
mylist_mssv = Listbox(windown, width=30, bg="#EDFC8F", yscrollcommand=list_mssv.set)
mylist_mssv.place(x=680,y=313)

#Sinh vien di hoc
lbl_sv_dihoc =  Label(windown, text="Sinh Viên Đi Học", foreground="red", font=("Arial", 13, "bold"))
lbl_sv_dihoc.place(x=950,y=287)
list_sv_dihoc = Scrollbar(windown)
list_sv_dihoc.place(x=951,y=313)
mylist_sv_dihoc = Listbox(windown, width=60, bg="#FFFFFF", yscrollcommand=list_sv_dihoc.set)
mylist_sv_dihoc.place(x=950,y=313)

#frame tong so
frame_tongso = tk.LabelFrame(windown, text="Tổng Số", font=("Arial", 13, "bold"))
frame_tongso.place(x=790,y=10)

lbl_tongso1 = Label(frame_tongso, text="Tổng Số: ", font=("Arial", 10, "bold"), width=15)
lbl_tongso1.grid(column=0, row=0)
lbl_tongso2 = Label(frame_tongso, text="00", foreground="#E20A0A", font=("Arial", 10, "bold"), width=15)
lbl_tongso2.grid(column=1, row=0)

lbl_hiendien1 = Label(frame_tongso, text="Hiện diện: ", font=("Arial", 10, "bold"), width=15)
lbl_hiendien1.grid(column=0, row=1)
lbl_hiendien2 = Label(frame_tongso, text="00", foreground="#E20A0A", font=("Arial", 10, "bold"), width=15)
lbl_hiendien2.grid(column=1, row=1)

lbl_vang1 = Label(frame_tongso, text="Vắng: ", font=("Arial", 10, "bold"), width=15)
lbl_vang1.grid(column=0, row=2)
lbl_vang2 = Label(frame_tongso, text="00", foreground="#E20A0A", font=("Arial", 10, "bold"), width=15)
lbl_vang2.grid(column=1, row=2)

update_frame()
getDataGiangVien(1)
getDataHocKi(1)
runTime()
windown.mainloop()