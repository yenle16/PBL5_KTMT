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
windown = Tk()
windown.title("Nhận Diện Khuôn Mặt Và Hỗ Trợ Điểm Danh Sinh Viên")
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

def getDataLop():
    conn = sqlite3.connect('Database.db')

    query = "Select Lop.ten from Lop "

    cursor = conn.execute(query)

    result = []

    for row in cursor:
        result.append(row)

    conn.close()
    return  result

def input_Image():
    conn = sqlite3.connect('Database.db')
    mssv = txt_name.get()
    query = "Select * from SinhVien Where mssv = " + str(mssv)
    cursor2 = conn.execute(query)

    result = None

    for row in cursor2:
        result = row
    conn.close()

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    global canvas, photo, sampleNum, count
    # doc tu camera
    ret, frame = video.read()
    # resize
    frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
    # convert mau
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    result_name = result[1].replace(" ", "")
    for (x, y, w, h) in faces:
        # vẽ 1 đường bao quanh khuôn mặt
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite("dataSet/" + str(result_name) + "_" + str(result[0]) + '/Student_' + str(result[0]) + '_' + str(sampleNum) + '.jpg', gray[y:y + h, x:x + w])
    if len(faces) == 0:
        messagebox.showinfo("Thêm sinh viên",
                            "Hệ thống tạm dừng vì không nhận diện được khuôn mặt bạn. Vui lòng thử lại!!!")
        sampleNum = 0
        count = 0
        if not os.path.exists('dataSet/' + str(result_name) + "_" + str(mssv)):
            pass
        else:
            path = os.path.join(
                # '/home/thangnt/PycharmProjects/DoAnTN/dataSet/' + str(result_name) + "_" + str(result[0]))
                'dataSet/' + str(result_name) + "_" + str(result[0]))
            shutil.rmtree(path)
        return
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(gray))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    if not os.path.exists('dataSet/' + str(result_name) + "_" + str(mssv)):
        os.makedirs('dataSet/' + str(result_name) + "_" + str(mssv))
    sampleNum += 1
    count += 1
    if count == 20:
        messagebox.showinfo("Thêm sinh viên", "Thêm sinh viên thành công")
        windown.after(15, windown.destroy)
    print(count)
    windown.after(500, input_Image)
def nhandien():
    global mssv
    conn = sqlite3.connect('Database.db')
    query_arr_mssv = "Select SinhVien.mssv from SinhVien"
    cursor = conn.execute(query_arr_mssv)

    arr_mssv = []

    for row in cursor:
        arr_mssv.append(row[0])

    mssv = txt_name.get()
    exists = 0
    for item in arr_mssv:
        if mssv == item:
            exists = 1
    if exists == 0:
        messagebox.showinfo("Thêm sinh viên",
                            "Vui lòng nhập đúng mã số sinh viên !!!", icon='warning')
        return

    root = 'dataSet'
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

def getData(mssv):
    conn = sqlite3.connect('Database.db')

    query2 = "Select SinhVien.mssv, SinhVien.ten, Lop.ten from SinhVien INNER JOIN Lop ON SinhVien.id_lop = Lop.id_lop Where mssv = " + str(mssv)
    cursor2 = conn.execute(query2)

    result = None

    for row in cursor2:
        result = row

    conn.close()
    return  result


def insert_diemdanh(mssv, msgv, id_hocki, id_monhoc, gio_diemdanh, ngay_diemdanh):
    conn = sqlite3.connect('Database.db')

    query = "INSERT INTO SinhVienDiemDanh(mssv, msgv, id_hocki, id_monhoc, gio_diemdanh, ngay_diemdanh) VALUES ("+str(mssv)+", '"+str(msgv)+"', '"+str(id_hocki)+"', '"+str(id_monhoc)+"', '"+str(gio_diemdanh)+"', '"+str(ngay_diemdanh)+"')"

    conn.execute(query)

    conn.commit()

    conn.close()


def getDataCBB():
    conn = sqlite3.connect('Database.db')

    # get msgv
    masogv = cbb_gv.get()
    query_msgv = "Select GiangVien.msgv from GiangVien " \
                 "INNER JOIN Khoa ON Khoa.id_khoa = GiangVien.id_khoa " \
                 "Where GiangVien.ten = '%s'" % masogv
    cursor_msgv = conn.execute(query_msgv)
    kqua_msgv = None
    for row in cursor_msgv:
        kqua_msgv = row
    id_msgv = kqua_msgv[0]

    # get id_hocki
    hocki = cbb_hocki.get()
    query_id_hocki = "Select HocKi.id_hocki from HocKi  Where HocKi.ten = '%s'" % hocki
    cursor_id_hocki = conn.execute(query_id_hocki)
    kqua_id_hocki = None
    for row in cursor_id_hocki:
        kqua_id_hocki = row
    id_hocki = kqua_id_hocki[0]

    # get id_monhoc
    monhoc = cbb_mon.get()
    query_id_monhoc = "Select MonHoc.id_monhoc from MonHoc  Where MonHoc.ten = '%s'" % monhoc
    cursor_id_monhoc = conn.execute(query_id_monhoc)
    kqua_id_monhoc = None
    for row in cursor_id_monhoc:
        kqua_id_monhoc = row
    id_monhoc = kqua_id_monhoc[0]
    return (id_msgv, id_hocki, id_monhoc)

def show_svdiemdanh():
    result_data = getDataCBB()
    conn = sqlite3.connect('Database.db')

    now = datetime.now()
    ngay_diemdanh = now.strftime("%d-%m-%Y")

    query_svdiemdanh = "Select SinhVien.ten, SinhVien.mssv, SinhVienDiemDanh.gio_diemdanh, SinhVienDiemDanh.ngay_diemdanh, SinhVienDiemDanh.msgv from SinhVienDiemDanh " \
                       "INNER JOIN SinhVien ON SinhVien.mssv = SinhVienDiemDanh.mssv " \
                       "Where SinhVienDiemDanh.msgv = '%s' " \
                       "And SinhVienDiemDanh.id_hocki = '%s' " \
                       "And SinhVienDiemDanh.id_monhoc = '%s' " \
                       "And SinhVienDiemDanh.ngay_diemdanh = '%s'" % (
                       result_data[0], result_data[1], result_data[2], ngay_diemdanh)
    cursor_svdiemdanh = conn.execute(query_svdiemdanh)
    kqua_sv_diemdanh = []
    for row in cursor_svdiemdanh:
        kqua_sv_diemdanh.append(row)
    print(kqua_sv_diemdanh)
    mylist_sv_dihoc.delete(0,END)
    for item in kqua_sv_diemdanh:
        if item[4] == result_data[0]:
            mylist_sv_dihoc.insert(END, item[0] + "_" + item[1] + "/" + item[2]+ " " + item[3])

def diemdanh():
    current_monhoc = cbb_mon.get()
    count = 0
    for i in cbb_mon['values']:
        print(i)
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
        result = getData(mssv_after)
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

            conn = sqlite3.connect('Database.db')

            result_data = getDataCBB()

            now = datetime.now()
            gio_diemdanh = now.strftime("%H:%M:%S")
            ngay_diemdanh = now.strftime("%d-%m-%Y")

            query_check_svdiemdanh = "Select SinhVienDiemDanh.mssv, SinhVienDiemDanh.msgv, SinhVienDiemDanh.id_hocki, SinhVienDiemDanh.id_monhoc, SinhVienDiemDanh.ngay_diemdanh from SinhVienDiemDanh " \
                                     "INNER JOIN SinhVien ON SinhVien.mssv = SinhVienDiemDanh.mssv "
            cursor_check_svdiemdanh = conn.execute(query_check_svdiemdanh)
            kqua_check_svdiemdanh = []
            for row in cursor_check_svdiemdanh:
                kqua_check_svdiemdanh.append(row)

            for item in kqua_check_svdiemdanh:
                if item[0] == result[0] and item[1] == result_data[0] and item[2] == result_data[1] and item[3] == result_data[2] and item[4] == ngay_diemdanh:
                    messagebox.showinfo("Điểm Danh", "Bạn đã điểm danh !!!", icon='info')
                    return
            insert_diemdanh(result[0], result_data[0], result_data[1], result_data[2], gio_diemdanh, ngay_diemdanh)
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

def thongketheongay():
    khoa = cbb_khoa.get()
    masogv = cbb_gv.get()
    hocki = cbb_hocki.get()
    monhoc = cbb_mon.get()
    count = 0
    for i in cbb_mon['values']:
        if monhoc == i:
            count += 1
    if count == 0:
        messagebox.showinfo("Điểm Danh",
                            "Vui lòng chọn lớp học trước khi thống kê!!!", icon='warning')
        return
    conn = sqlite3.connect('Database.db')
    result_data = getDataCBB()

    # now = datetime.now()
    ngay_diemdanh = date_thongke.get()
    result_ngay_diemdanh = ngay_diemdanh.replace("/", "-")

    query_svdiemdanh = "Select SinhVien.ten, SinhVien.mssv, SinhVienDiemDanh.gio_diemdanh, SinhVienDiemDanh.ngay_diemdanh from SinhVienDiemDanh " \
                       "INNER JOIN SinhVien ON SinhVien.mssv = SinhVienDiemDanh.mssv " \
                       "Where SinhVienDiemDanh.msgv = '%s' " \
                       "And SinhVienDiemDanh.id_hocki = '%s' " \
                       "And SinhVienDiemDanh.id_monhoc = '%s' " \
                       "And SinhVienDiemDanh.ngay_diemdanh = '%s'" % (result_data[0], result_data[1], result_data[2], result_ngay_diemdanh)
    cursor_svdiemdanh = conn.execute(query_svdiemdanh)
    kqua_sv_diemdanh = []
    for row in cursor_svdiemdanh:
        kqua_sv_diemdanh.append(row)

    monhoc_excel = monhoc.replace(" ", "")
    df = pd.DataFrame(kqua_sv_diemdanh, columns=['Tên', 'MSSV', 'Giờ Điểm Danh', 'Ngày Điểm Danh'])
    with pd.ExcelWriter("ExportExcel/"+monhoc_excel+"_"+result_data[0]+"_"+result_ngay_diemdanh+".xlsx") as writer:
        df.to_excel(writer)
    messagebox.showinfo("Thống Kê Theo Ngày", "Thống Kê Xong", icon='info')

def thongkeHetMon():
    khoa = cbb_khoa.get()
    masogv = cbb_gv.get()
    hocki = cbb_hocki.get()
    monhoc = cbb_mon.get()
    count = 0
    for i in cbb_mon['values']:
        if monhoc == i:
            count += 1
    if count == 0:
        messagebox.showinfo("Điểm Danh",
                            "Vui lòng chọn lớp học trước khi thống kê!!!", icon='warning')
        return
    conn = sqlite3.connect('Database.db')
    result_data = getDataCBB()

    query = "Select SinhVien.ten, SinhVien.mssv from SinhVien " \
            "INNER JOIN MonHoc_SinhVien ON MonHoc_SinhVien.mssv = SinhVien.mssv " \
            "INNER JOIN MonHoc_HocKi ON MonHoc_HocKi.id = MonHoc_SinhVien.id_monhoc_hocki " \
            "INNER JOIN MonHoc ON MonHoc.id_monhoc = MonHoc_HocKi.id_monhoc " \
            "INNER JOIN MonHoc_GiangVien ON MonHoc_GiangVien.id_monhoc = MonHoc.id_monhoc " \
            "INNER JOIN GiangVien ON GiangVien.msgv = MonHoc_GiangVien.msgv " \
            "INNER JOIN HocKi ON HocKi.id_hocki = MonHoc_HocKi.id_hocki " \
            "Where MonHoc.id_monhoc = '%s' And GiangVien.msgv = '%s' And HocKi.ten = '%s'" % (result_data[2], result_data[0], hocki)
    cursor_all_sv = conn.execute(query)
    kqua_all_sv = []
    for row in cursor_all_sv:
        kqua_all_sv.append(row)

    query_svdiemdanh_kthucmon = "Select SinhVien.ten, SinhVien.mssv, count(SinhVien.mssv) as solandiemdanh from SinhVien " \
                       "INNER JOIN SinhVienDiemDanh ON SinhVien.mssv = SinhVienDiemDanh.mssv " \
                       "Where SinhVienDiemDanh.msgv = '%s' " \
                       "And SinhVienDiemDanh.id_hocki = '%s' " \
                       "And SinhVienDiemDanh.id_monhoc = '%s' " \
                       "GROUP BY SinhVien.mssv " % (result_data[0], result_data[1], result_data[2])
    cursor_svdiemdanh_kthucmon = conn.execute(query_svdiemdanh_kthucmon)
    kqua_sv_diemdanh_kthucmon = []
    for row in cursor_svdiemdanh_kthucmon:
        kqua_sv_diemdanh_kthucmon.append(row)

    for sv in kqua_all_sv:
        is_exists = False
        for sv_diemdanh in kqua_sv_diemdanh_kthucmon:
            if sv[1] == sv_diemdanh[1]:
                is_exists = True
                break
        if is_exists == False:
            kqua_sv_diemdanh_kthucmon.append((sv[0], sv[1], 0))
    monhoc_excel = monhoc.replace(" ", "")
    df = pd.DataFrame(kqua_sv_diemdanh_kthucmon, columns=['Tên', 'MSSV', 'Số Buổi Đi Học'])
    with pd.ExcelWriter("ExportExcel/"+monhoc_excel+"_"+result_data[0]+"_"+hocki+".xlsx") as writer:
        df.to_excel(writer)
    messagebox.showinfo("Thống Kê Kết Thúc Môn", "Thống Kê Xong", icon='info')

button_thongke_ngay = tk.Button(windown, text="Thống Kê Theo Ngày", background="#4BF6CE", font=("Arial", 13, "bold"), borderwidth=2, relief="raised", width=20, command=thongketheongay)
button_thongke_ngay.place(x=1050,y=20)
class CustomDateEntry(DateEntry):

    def _select(self, event=None):
        date = self._calendar.selection_get()
        if date is not None:
            self._set_text(date.strftime('%d/%m/%Y'))
            self.event_generate('<<DateEntrySelected>>')
        self._top_cal.withdraw()
        if 'readonly' not in self.state():
            self.focus_set()

date_thongke = CustomDateEntry(windown, width= 15)
date_thongke._set_text(date_thongke._date.strftime('%d/%m/%Y'))
date_thongke.place(x=1300,y=22)
button_thongke_hetmon = tk.Button(windown, text="Thống Kê Kết Thúc Môn", background="#4BF6CE", width=20, borderwidth=2, relief="raised", font=("Arial", 13, "bold"), command=thongkeHetMon)
button_thongke_hetmon.place(x=1050,y=65)

def getDataKhoa():
    conn = sqlite3.connect('Database.db')

    query = "Select Khoa.ten from Khoa "

    cursor = conn.execute(query)

    result = []

    for row in cursor:
        result.append(row[0])

    conn.close()
    return  result

def getDataGiangVien(event):
    khoa = cbb_khoa.get()
    conn = sqlite3.connect('Database.db')
    query1 = "Select Khoa.id_khoa from Khoa  Where Khoa.ten = '%s'" % khoa
    cursor = conn.execute(query1)
    kqua = None
    for row in cursor:
        kqua = row

    id = kqua[0]

    query = "Select GiangVien.ten from GiangVien INNER JOIN Khoa ON GiangVien.id_khoa = Khoa.id_khoa Where Khoa.id_khoa = " + str(id)
    cursor2 = conn.execute(query)

    result = []

    for row in cursor2:
        result.append(row[0])

    cbb_gv['values'] = result
    cbb_gv.current(0)

    name_gv = cbb_gv.get()
    query3 = "Select GiangVien.msgv from GiangVien  Where GiangVien.ten = '%s'" % name_gv
    cursor3 = conn.execute(query3)
    result_msgv = None
    for row in cursor3:
        result_msgv = row

    msgv = result_msgv[0]

    query2 = "SELECT DISTINCT MonHoc.ten, HocKi.ten FROM MonHoc " \
            "INNER JOIN MonHoc_GiangVien ON MonHoc_GiangVien.id_monhoc = MonHoc.id_monhoc " \
            "INNER JOIN GiangVien ON GiangVien.msgv = MonHoc_GiangVien.msgv " \
            "INNER JOIN MonHoc_HocKi ON MonHoc.id_monhoc = MonHoc_HocKi.id_monhoc " \
            "INNER JOIN HocKi ON HocKi.id_hocki = MonHoc_HocKi.id_hocki " \
            "Where GiangVien.msgv = '%s' " % (msgv)

    cursor4 = conn.execute(query2)
    result_ten_mh = []
    result_hocki = []
    for row in cursor4:
        result_ten_mh.append(row[0])
        result_hocki.append(row[1])
    conn.close()
    cbb_hocki['values'] = result_hocki

#khoa
lbl_khoa =  tk.Label(windown, text="Khoa", foreground="#DA681D", font=("Arial", 13, "bold"))
lbl_khoa.place(x=350,y=195)
cbb_khoa = Combobox(windown, state="readonly")
cbb_khoa['values'] = getDataKhoa()
cbb_khoa.current(0)
cbb_khoa.bind("<<ComboboxSelected>>", getDataGiangVien)
cbb_khoa.place(x = 350, y=220)

def getDataHocKi(event):
    giangvien = cbb_gv.get()
    conn = sqlite3.connect('Database.db')

    query1 = "Select GiangVien.msgv from GiangVien  Where GiangVien.ten = '%s'" % giangvien
    cursor = conn.execute(query1)

    kqua = None

    for row in cursor:
        kqua = row

    id = kqua[0]

    query_hocki = "SELECT HocKi.ten FROM HocKi " \
            "INNER JOIN MonHoc_HocKi ON MonHoc_HocKi.id_hocki = HocKi.id_hocki " \
            "INNER JOIN MonHoc_GiangVien ON MonHoc_GiangVien.id_monhoc = MonHoc_HocKi.id_monhoc " \
            "INNER JOIN GiangVien ON GiangVien.msgv = MonHoc_GiangVien.msgv " \
            "Where GiangVien.msgv = '%s'" % (id)
    cursor3 = conn.execute(query_hocki)
    result_hocki = []

    for row in cursor3:
        result_hocki.append(row)
    conn.close()

    cbb_hocki['values'] = result_hocki

def getDataMonHoc_GiangVien(event):
    count_hocki = 0
    for i in cbb_hocki['values']:
        if cbb_hocki.get() == i:
            count_hocki += 1
    if count_hocki == 0:
        cbb_mon['state'] = 'readonly'
    hocki = cbb_hocki.get()
    giangvien = cbb_gv.get()
    conn = sqlite3.connect('Database.db')
    query1 = "Select GiangVien.msgv from GiangVien  Where GiangVien.ten = '%s'" % giangvien
    cursor = conn.execute(query1)
    kqua = None
    for row in cursor:
        kqua = row

    id = kqua[0]

    query = "SELECT MonHoc.ten FROM MonHoc " \
            "INNER JOIN MonHoc_GiangVien ON MonHoc_GiangVien.id_monhoc = MonHoc.id_monhoc " \
            "INNER JOIN GiangVien ON GiangVien.msgv = MonHoc_GiangVien.msgv " \
            "INNER JOIN MonHoc_HocKi ON MonHoc_HocKi.id_monhoc = MonHoc.id_monhoc " \
            "INNER JOIN HocKi ON HocKi.id_hocki = MonHoc_HocKi.id_hocki " \
            "Where HocKi.ten = '%s' And GiangVien.msgv = '%s'" % (hocki, id)

    cursor2 = conn.execute(query)

    result_name_mh = []

    for row in cursor2:
        result_name_mh.append(row[0])
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
    conn = sqlite3.connect('Database.db')
    query_id_mh = "Select MonHoc.id_monhoc from MonHoc Where MonHoc.ten = '%s'" % monhoc
    cursor = conn.execute(query_id_mh)
    kqua = None
    for row in cursor:
        kqua = row
    id = kqua[0]

    query_hocki = "Select HocKi.ten from HocKi " \
                  "INNER JOIN MonHoc_HocKi ON HocKi.id_hocki = MonHoc_HocKi.id_hocki " \
                  "INNER JOIN MonHoc ON MonHoc.id_monhoc = MonHoc_HocKi.id_monhoc  " \
                  "Where MonHoc.id_monhoc = '%s'" % id
    cursor2 = conn.execute(query_hocki)
    result_hocki = []
    for row in cursor2:
        result_hocki.append(row)
    cbb_hocki['values'] = result_hocki

    giangvien = cbb_gv.get()
    query_msgv = "Select GiangVien.msgv from GiangVien  Where GiangVien.ten = '%s'" % giangvien
    cursor3 = conn.execute(query_msgv)
    msgv = None
    for row in cursor3:
        msgv = row
    msgv_result = msgv[0]

    hocki = cbb_hocki.get()

    query = "Select SinhVien.ten, SinhVien.mssv from SinhVien " \
            "INNER JOIN MonHoc_SinhVien ON MonHoc_SinhVien.mssv = SinhVien.mssv " \
            "INNER JOIN MonHoc_HocKi ON MonHoc_HocKi.id = MonHoc_SinhVien.id_monhoc_hocki " \
            "INNER JOIN MonHoc ON MonHoc.id_monhoc = MonHoc_HocKi.id_monhoc " \
            "INNER JOIN MonHoc_GiangVien ON MonHoc_GiangVien.id_monhoc = MonHoc.id_monhoc " \
            "INNER JOIN GiangVien ON GiangVien.msgv = MonHoc_GiangVien.msgv " \
            "INNER JOIN HocKi ON HocKi.id_hocki = MonHoc_HocKi.id_hocki " \
            "Where MonHoc.id_monhoc = '%s' And GiangVien.msgv = '%s' And HocKi.ten = '%s'"  % (id, msgv_result, hocki)

    cursor4 = conn.execute(query)

    result_name_sv = []
    result_mssv = []

    for row in cursor4:
        result_name_sv.append(row[0])
        result_mssv.append(row[1])
    mylist.delete(0, END)
    mylist_mssv.delete(0, END)
    for line_name in result_name_sv:
        mylist.insert(END, str(line_name))

    for line_mssv in result_mssv:
        mylist_mssv.insert(END, str(line_mssv))

    conn.close()

    lbl_tongso2.configure(text=mylist.size())
    lbl_hiendien2.configure(text=mylist_sv_dihoc.size())
    vang = mylist.size() - mylist_sv_dihoc.size()
    lbl_vang2.configure(text=vang)

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