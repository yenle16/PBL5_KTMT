
from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk
import tkinter as tk
import tkinter
from tkinter import messagebox
# from tkcalendar import Calendar, DateEntry
# from datetime import datetime


import os
import numpy as np
import ActionDB


window = tk.Tk()
window.title("Dang ki hoc phan")
# window.geometry("1570x700")


def getDataGiangVien(event):
    khoa = cbb_khoa.get()

    maKhoa=ActionDB.getmaKhoabytenKhoa(khoa)[0]
    
    tenGiangVien=ActionDB.getGiangVienIDbyKhoa(maKhoa)


    cbb_gv['values'] = tenGiangVien
   


#khoa
lbl_khoa =  tk.Label(window, text="Khoa", foreground="#DA681D", font=("Arial", 13, "bold"))
# lbl_khoa.place(x=350,y=195)
lbl_khoa.grid(row=0, column=0, padx=10, pady=10)
cbb_khoa = Combobox(window, state="readonly")
cbb_khoa.grid(row=0, column=1, padx=10, pady=10)

cbb_khoa['values'] = ActionDB.getDataKhoa()
cbb_khoa.current(0)
cbb_khoa.bind("<<ComboboxSelected>>", getDataGiangVien)
# cbb_khoa.place(x = 350, y=220)

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
lbl_gv =  Label(window, text="Giảng viên", foreground="#DA681D", font=("Arial", 13, "bold"))
# lbl_gv.place(x=540,y=195)
lbl_gv.grid(row=1, column=0, padx=10, pady=10)

cbb_gv = Combobox(window, state="readonly")
cbb_gv.bind("<<ComboboxSelected>>", getDataHocKi)
# cbb_gv.place(x = 540, y=220)
cbb_gv.grid(row=1, column=1, padx=10, pady=10)


#hoc ki
lbl_hocki =  Label(window, text="Học kì", foreground="#DA681D", font=("Arial", 13, "bold"))
# lbl_hocki.place(x=730,y=195)
lbl_hocki.grid(row=2, column=0, padx=10, pady=10)

cbb_hocki = Combobox(window, state="readonly")
cbb_hocki.bind("<<ComboboxSelected>>", getDataMonHoc_GiangVien)
cbb_hocki.grid(row=2, column=1, padx=10, pady=10)

# cbb_hocki.place(x = 730, y=220)

def getDataLopHoc_Hocki(event):

    monhoc = cbb_mon.get()

    idMonhoc = ActionDB.getmaMonhocbytenMonhoc(monhoc)[0]

    cbb_hocki['values'] = ActionDB.gettenHockibymaMonhoc(idMonhoc)

    tenGV = cbb_gv.get()

    msgv = ActionDB.getmaGVbytenGV(tenGV)[0]

    hocki = cbb_hocki.get()

def getAllSinhvien(event ):
    print(ActionDB.getAllSV())
    result_ma_SV,result_ten_SV=ActionDB.getAllSV()[0]
    cbb_sv['values'] = result_ten_SV
    print(result_ten_SV)
    


def filter_combobox(event):
    typed_text = cbb_sv.get()
    filtered_values = [value for value in all_ten_sv if typed_text.lower() in value.lower()]
    cbb_sv['values'] = filtered_values
    cbb_sv.icursor(tk.END)

#Mon hoc
lbl_mon =  Label(window, text="Môn Học", foreground="#DA681D", font=("Arial", 13, "bold"))
# lbl_mon.place(x=920,y=195)
lbl_mon.grid(row=3, column=0, padx=10, pady=10)

cbb_mon = Combobox(window, state='disabled')
cbb_mon.bind("<<ComboboxSelected>>", getDataLopHoc_Hocki)
# cbb_mon.place(x = 920, y=220)
cbb_mon.grid(row=3, column=1, padx=10, pady=10)



#Sinh viên
lbl_sv =  Label(window, text="Sinh viên", foreground="#DA681D", font=("Arial", 13, "bold"))
# lbl_sv.place(x=920,y=195)
lbl_sv.grid(row=4, column=0, padx=10, pady=10)

cbb_sv = Combobox(window)
all_ma_sv,all_ten_sv = ActionDB.getAllSV()
cbb_sv['values'] = all_ten_sv
cbb_sv.bind('<Key>', filter_combobox)
cbb_sv.grid(row=4, column=1, padx=10, pady=10)

ma_sv = cbb_sv.get()
ActionDB.AddSinhVienHocPhan(ma_sv, id_monhoc_hocki)





window.mainloop()
