
from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk
import tkinter as tk
import tkinter
from tkinter import messagebox


import os
import numpy as np
import ActionDB


window = tk.Tk()
window.title("Dang ki hoc phan")


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

def AddSinhVienHocPhan():
    ten_sv=cbb_sv.get()
    ma_sv = ActionDB.getmaSVbytenSV(ten_sv)
    print (ma_sv)
    # id_monhoc,id_hocki=getMaHocKi()
    lophocphan = cbb_lophocphan.get()
    print(lophocphan)
    idLophocphan = ActionDB.getidLopHocPhanbyten(lophocphan)[0]
    print (idLophocphan)
    ActionDB.AddSinhVienHocPhan(ma_sv, idLophocphan)

    

def get_selected_value(combobox):
    selected_value = combobox.get()
    print("Selected value:", selected_value)
    return selected_value



#LopHocPhan
lbl_lophocphan =  tk.Label(window, text="Lớp học phần", foreground="#DA681D", font=("Arial", 13, "bold"))
# lbl_lophocphan.place(x=350,y=195)
lbl_lophocphan.grid(row=0, column=0, padx=10, pady=10)
cbb_lophocphan = Combobox(window, state="readonly")
all_ma_lophocphan,all_ten_lophocphan=ActionDB.getAllLopHocPhan()
cbb_lophocphan['values'] = all_ten_lophocphan
cbb_lophocphan.grid(row=0, column=1, padx=10, pady=10)


#Sinh viên
lbl_sv =  Label(window, text="Sinh viên", foreground="#DA681D", font=("Arial", 13, "bold"))
# lbl_sv.place(x=920,y=195)
lbl_sv.grid(row=3, column=0, padx=10, pady=10)

cbb_sv = Combobox(window)
all_ma_sv,all_ten_sv = ActionDB.getAllSV()
cbb_sv['values'] = all_ten_sv
cbb_sv.bind('<Key>', filter_combobox)
cbb_sv.grid(row=3, column=1, padx=10, pady=10)


btn_add = tk.Button(window, text="Thêm sinh viên vào lớp", command=AddSinhVienHocPhan)
btn_add.grid(row=5, column=1, padx=10, pady=10)

window.mainloop()
