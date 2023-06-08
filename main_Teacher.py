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
from Training import recognizer
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
window = Tk()
window.title("Nhận Diện Khuôn Mặt Và Hỗ Trợ Điểm Danh Sinh Viên")
window.geometry("1570x700")

video = cv2.VideoCapture(0)
# video = cv2.VideoCapture('http://192.168.1.12:81/stream')


canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)


canvas = Canvas(window, width = canvas_w, height = canvas_h)
canvas.pack(fill=BOTH)

#frame result

frame_result = tk.LabelFrame(window, text="Kết Quả", font=("Arial", 15, "bold"))
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

frame_insert = tk.LabelFrame(window, text="Thêm dữ liệu", font=("Arial", 15, "bold"))
frame_insert.place(x=0,y=383)

lbl_name = Label(frame_insert, text="Mã số sinh viên: ", foreground="#1A6991", font=("Arial", 13))
lbl_name.grid(column=0, row=2)
txt_name = Entry(frame_insert, width=23)
txt_name.grid(column=1, row=2, sticky=W, pady=4)


def input_Image():
    mssv = txt_name.get()
    result=ActionDB.input_ImageDB(mssv)
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
    if count == 60:
        messagebox.showinfo("Thêm sinh viên", "Thêm sinh viên thành công")
        window.after(15, window.destroy)
    print(count)
    window.after(500, input_Image)
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
    window.after(15, update_frame)



def show_svdiemdanhHP():
    now = datetime.now()
    tenLopHocPhan=lbl_tenlophocphan["text"]
    idLopHocPhan=ActionDB.getidLopHocPhanbyten(tenLopHocPhan)[0]
    ngay_diemdanh = now.strftime("%d-%m-%Y")
    kqua_sv_diemdanh=ActionDB.show_svdiemdanhHP(idLopHocPhan,ngay_diemdanh)

    # print (kqua_sv_diemdanh)
    # print(kqua_sv_diemdanh)
    mylist_sv_dihoc.delete(0,END)
    for item in kqua_sv_diemdanh:
        print (item)
        if item[3] == ngay_diemdanh:
            mylist_sv_dihoc.insert(END, item[0] + "_" + item[1] + "/" + item[2]+ " " + item[3])


def diemdanh():
    mylist=Listbox()
    mylist_mssv=Listbox()
    tenLopHocPhan=lbl_tenlophocphan["text"]
    print (tenLopHocPhan)
    idLopHocPhan=ActionDB.getidLopHocPhanbyten(tenLopHocPhan)[0]
    result_name_sv,result_mssv=ActionDB.getSVbyLopHocPhan(tenLopHocPhan)
    for line_name in result_name_sv:
        # print (line_name)
        mylist.insert(END, str(line_name))


    for line_mssv in result_mssv:
        mylist_mssv.insert(END, str(line_mssv))

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
        # mssv, confidence,dist = recognizer.predict(roi_gray)
        # mssv, confidence = recognizer.predict(roi_gray)
        mssv, dist= recognizer.predict(roi_gray)
        print (dist)
        print (mssv)
        if (dist < 90):
            
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


            # result_data = getDataCBB()

            now = datetime.now()
            gio_diemdanh = now.strftime("%H:%M:%S")
            ngay_diemdanh = now.strftime("%d-%m-%Y")

            kqua_check_svdiemdanh=ActionDB.diemdanhHP()
            for item in kqua_check_svdiemdanh:
                if item[0] == result[0] and item[1] == idLopHocPhan and  item[2] == ngay_diemdanh:
                    messagebox.showinfo("Điểm Danh", "Bạn đã điểm danh !!!", icon='info')
                    return
            ActionDB.insert_diemdanhHP(mssv, idLopHocPhan, gio_diemdanh, ngay_diemdanh)
            show_svdiemdanhHP()
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

button_diemdanh = tk.Button(window, text="Điểm Danh", bg="yellow", width=13,  font=("Arial", 15, "bold"), borderwidth=2, relief="raised", height=6 ,command=diemdanh)
button_diemdanh.place(x=350,y=10)

#frame time
frame_time = tk.LabelFrame(window, text="Thời Gian", font=("Arial", 15, "bold"))
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
    tenLopHocPhan=lbl_tenlophocphan["text"]
    print (tenLopHocPhan)
    if tenLopHocPhan == '':
        messagebox.showinfo("Điểm Danh",
                            "Hiện tại không có lớp học để thống kê!!!", icon='warning')
        return
    else:
        idLopHocPhan=ActionDB.getidLopHocPhanbyten(tenLopHocPhan)[0]

    # conn = sqlite3.connect('Database.db')
    # now = datetime.now()
    ngay_diemdanh = date_thongke.get()
    result_ngay_diemdanh = ngay_diemdanh.replace("/", "-")

    kqua_sv_diemdanh=ActionDB.thongketheongay(idLopHocPhan,result_ngay_diemdanh)

    hocphan_excel = tenLopHocPhan.replace(" ", "")
    df = pd.DataFrame(kqua_sv_diemdanh, columns=['Tên', 'MSSV', 'Giờ Điểm Danh', 'Ngày Điểm Danh'])
    with pd.ExcelWriter("ExportExcel/"+hocphan_excel+"_"+result_ngay_diemdanh+".xlsx") as writer:
        df.to_excel(writer)
    messagebox.showinfo("Thống Kê Theo Ngày", "Thống Kê Xong", icon='info')

def thongkeHetMon():
    tenLopHocPhan=lbl_tenlophocphan["text"]
    print (tenLopHocPhan)
    if tenLopHocPhan == '':
        messagebox.showinfo("Điểm Danh",
                            "Hiện tại không có lớp học nào!!!", icon='warning')
        return
    else:
        idLopHocPhan=ActionDB.getidLopHocPhanbyten(tenLopHocPhan)[0]

        kqua_all_sv,kqua_sv_diemdanh_kthucmon=ActionDB.thongkeHetMon(idLopHocPhan)

        for sv in kqua_all_sv:
            is_exists = False
            for sv_diemdanh in kqua_sv_diemdanh_kthucmon:
                if sv[1] == sv_diemdanh[1]:
                    is_exists = True
                    break
            if is_exists == False:
                kqua_sv_diemdanh_kthucmon.append((sv[0], sv[1], 0))
        hocphan_excel = tenLopHocPhan.replace(" ", "")
        df = pd.DataFrame(kqua_sv_diemdanh_kthucmon, columns=['Tên', 'MSSV', 'Số Buổi Đi Học'])
        with pd.ExcelWriter("ExportExcel/"+hocphan_excel+".xlsx") as writer:
        # with pd.ExcelWriter("ExportExcel/"+hocphan_excel+"xlsx") as writer:
            df.to_excel(writer)
        messagebox.showinfo("Thống Kê Kết Thúc Môn", "Thống Kê Xong", icon='info')

button_thongke_ngay = tk.Button(window, text="Thống Kê Theo Ngày", background="#4BF6CE", font=("Arial", 13, "bold"), borderwidth=2, relief="raised", width=20, command=thongketheongay)
button_thongke_ngay.place(x=1050,y=20)


def AddSinhVien():
    import AddSV

def AddSinhVienHocPhan():
    import AddSV_LopHocPhan


class CustomDateEntry(DateEntry):

    def _select(self, event=None):
        date = self._calendar.selection_get()
        if date is not None:
            self._set_text(date.strftime('%d/%m/%Y'))
            self.event_generate('<<DateEntrySelected>>')
        self._top_cal.withdraw()
        if 'readonly' not in self.state():
            self.focus_set()

date_thongke = CustomDateEntry(window, width= 15)
date_thongke._set_text(date_thongke._date.strftime('%d/%m/%Y'))
date_thongke.place(x=1300,y=22)
button_thongke_hetmon = tk.Button(window, text="Thống Kê Kết Thúc Môn", background="#4BF6CE", width=20, borderwidth=2, relief="raised", font=("Arial", 13, "bold"), command=thongkeHetMon)
button_thongke_hetmon.place(x=1050,y=65)

button_thongke_hetmon = tk.Button(window, text="Thêm dữ liệu sinh viên", background="#4BF6CE", width=20, borderwidth=2, relief="raised", font=("Arial", 13, "bold"), command=AddSinhVien)
button_thongke_hetmon.place(x=1050,y=108)

button_thongke_hetmon = tk.Button(window, text="Thêm SV vào lớp học phần", background="#4BF6CE", width=20, borderwidth=2, relief="raised", font=("Arial", 13, "bold"), command=AddSinhVienHocPhan)
button_thongke_hetmon.place(x=1050,y=155)





def dangxuat():
    window.destroy()
    import main_Student

button_dangxuat = tk.Button(window, text="Đăng xuất", background="#4BF6CE", width=10, borderwidth=2, relief="raised", font=("Arial", 13, "bold"), command=dangxuat)
button_dangxuat.place(x=1300,y=65)


def truy_xuat_thoi_gian_lop_hoc_phan(ten_lop_hoc_phan):
    conn = sqlite3.connect('Database.db')  # Thay 'your_database.db' bằng tên cơ sở dữ liệu SQLite của bạn
    cursor = conn.cursor()

    query = """SELECT Tiet.giobatdau, Tiet.gioketthuc
               FROM LopHocPhan
               INNER JOIN Tiet ON LopHocPhan.id_tiet = Tiet.id
               WHERE LopHocPhan.ten = ?"""

    cursor.execute(query, (ten_lop_hoc_phan,))
    result = cursor.fetchone()

    if result:
        giobatdau, gioketthuc = result
        print(f"Thời gian của lớp học phần '{ten_lop_hoc_phan}': Giờ bắt đầu: {giobatdau}, Giờ kết thúc: {gioketthuc}")
    else:
        print(f"Không tìm thấy lớp học phần có tên '{ten_lop_hoc_phan}'")

    conn.close()


def truy_xuat_lop_hoc_hien_tai():
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.time().strftime("%H:%M:%S")  # Chuyển đổi thành chuỗi thời gian
    weekday = current_datetime.strftime('%A')
    ActionDB.truy_xuat_lop_hoc_hien_tai(current_time,weekday)
# Gọi hàm truy_xuat_lop_hoc_hien_tai để truy xuất các lớp học hiện tại

def getSVbyLopHocPhan(tenLopHocPhan):
    # tenLopHocPhan=cbb_lophocphan.get()
    scrollbar = Scrollbar(window)
    scrollbar.pack(side=RIGHT, fill=Y)
    mylist = Listbox(window, width=40, bg="#EDFC8F",yscrollcommand=scrollbar.set)
    mylist.place(x=350,y=313)   
    # mylist.pack(side=RIGHT, fill=BOTH)

    # scrollbar.config(command=mylist.yview)
    mylist_mssv = Listbox(window, width=30, bg="#EDFC8F",yscrollcommand=scrollbar.set)
    mylist_mssv.place(x=680,y=313)
    # mylist = Listbox()
    # mylist_mssv = Listbox()
    mylist_sv_dihoc=Listbox()
    # tenLopHocPhan=cbb_lophocphan.current(0)
    result_name_sv,result_mssv=ActionDB.getSVbyLopHocPhan(tenLopHocPhan)
    # print(result_name_sv)
    mylist.delete(0, END)
    mylist_mssv.delete(0, END)
    for line_name in result_name_sv:
        # print (line_name)
        mylist.insert(END, str(line_name))


    for line_mssv in result_mssv:
        mylist_mssv.insert(END, str(line_mssv))

    # conn.close()
    # show_svdiemdanh()
    lbl_tongso2 = Label()
    lbl_hiendien2=Label()
    lbl_vang2=Label()
    lbl_tongso2.configure(text=mylist.size())
    lbl_hiendien2.configure(text=mylist_sv_dihoc.size())
    vang = mylist.size() - mylist_sv_dihoc.size()
    lbl_vang2.configure(text=vang)




#Lophocphan
lbl_lophocphan =  Label(window, text="Lớp học phần", foreground="#DA681D", font=("Arial", 13, "bold"))
# lbl_lophocphan.place(x=1110,y=195)
lbl_lophocphan.place(x=650,y=125)
cbb_lophocphan = Combobox(window, state="readonly")
cbb_lophocphan.bind("<<ComboboxFocusOut>>",getSVbyLopHocPhan)
cbb_lophocphan.bind("<<ComboboxSelected>>", getSVbyLopHocPhan)
# cbb_lophocphan.place(x = 1110, y=220)

# truy_xuat_lop_hoc_hien_tai()
values = []

current_datetime = datetime.now()
current_time = current_datetime.time().strftime("%H:%M:%S")  # Chuyển đổi thành chuỗi thời gian
weekday = current_datetime.strftime('%A')
values=ActionDB.truy_xuat_lop_hoc_hien_tai(current_time,weekday)
lbl_tenlophocphan=Label(window,text='', foreground="#DA681D", font=("Arial", 13, "bold"))
# lbl_tenlophocphan.place(x = 1110, y=220)
lbl_tenlophocphan.place(x = 600, y=150)

if values:
    tenLopHocPhan=values[0]
    lbl_tenlophocphan.configure(text=values[0])

    print (tenLopHocPhan)
    getSVbyLopHocPhan(tenLopHocPhan)
else:
    messagebox.showinfo("Điểm Danh",
                         "Hiện tại không có lớp học nào!!!", icon='warning')


#Danh sach lop hoc
lbl_listclass =  Label(window, text="Danh Sách Lớp Học", foreground="red", font=("Arial", 13, "bold"))
lbl_listclass.place(x=350,y=287)
list_class = Scrollbar(window)
list_class.place(x=351,y=313)


#Ma so sinh vien
lbl_listmssv =  Label(window, text="Mã Số Sinh Viên", foreground="red", font=("Arial", 13, "bold"))
lbl_listmssv.place(x=680,y=287)
list_mssv = Scrollbar(window)
list_mssv.place(x=681,y=313)


#Sinh vien di hoc
lbl_sv_dihoc =  Label(window, text="Sinh Viên Đi Học", foreground="red", font=("Arial", 13, "bold"))
lbl_sv_dihoc.place(x=950,y=287)
list_sv_dihoc = Scrollbar(window)
list_sv_dihoc.place(x=951,y=313)
mylist_sv_dihoc = Listbox(window, width=60, bg="#FFFFFF", yscrollcommand=list_sv_dihoc.set)
mylist_sv_dihoc.place(x=950,y=313)

#frame tong so
frame_tongso = tk.LabelFrame(window, text="Tổng Số", font=("Arial", 13, "bold"))
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

runTime()
window.mainloop()