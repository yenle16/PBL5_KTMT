import tkinter as tk
import sqlite3
from tkcalendar import Calendar, DateEntry
import tkinter.ttk as ttk
import ActionDB
class CustomDateEntry(DateEntry):

    def _select(self, event=None):
        date = self._calendar.selection_get()
        if date is not None:
            self._set_text(date.strftime('%d/%m/%Y'))
            self.event_generate('<<DateEntrySelected>>')
        self._top_cal.withdraw()
        if 'readonly' not in self.state():
            self.focus_set()

gioitinh_values = ["Nam", "Nữ"]

# Function to insert student into the database
def add_student():
    mssv = entry_mssv.get()
    ten = entry_ten.get()
    gioitinh = combobox_gioitinh.get()
    if (gioitinh)=='Nữ':
        gioi_tinh=0
    else:
        gioi_tinh=1
    cmnd = entry_cmnd.get()
    ngay_sinh = date_entry_ngay_sinh.get_date().strftime('%Y-%m-%d') # Lấy giá trị ngày sinh từ widget DateEntry
    tenLop=entry_tenlop.get()
    id_lop=int((ActionDB.getmaLopbytenLop(tenLop)[0]))
    ActionDB.AddSV(mssv,ten,gioi_tinh,cmnd,ngay_sinh,id_lop)
    

    # Clear the entry fields
    entry_mssv.delete(0, tk.END)
    entry_ten.delete(0, tk.END)
    combobox_gioitinh.set('')
    entry_cmnd.delete(0, tk.END)
    entry_tenlop.delete(0, tk.END)

    # Show a success message
    label_status.config(text="Sinh viên đã được thêm vào cơ sở dữ liệu")

# Create the main window
window = tk.Tk()
window.title("Thêm Sinh viên")

# Create and place the labels
label_mssv = tk.Label(window, text="Mã sinh viên:")
label_mssv.grid(row=0, column=0, padx=10, pady=10)
label_ten = tk.Label(window, text="Tên sinh viên:")
label_ten.grid(row=1, column=0, padx=10, pady=10)
label_gioitinh = tk.Label(window, text="Giới tính:")
label_gioitinh.grid(row=2, column=0, padx=10, pady=10)
label_cmnd = tk.Label(window, text="CMND:")
label_cmnd.grid(row=3, column=0, padx=10, pady=10)
label_ngaysinh = tk.Label(window, text="Ngày sinh:")
label_ngaysinh.grid(row=4, column=0, padx=10, pady=10)
label_tenlop = tk.Label(window, text="Tên lớp:")
label_tenlop.grid(row=5, column=0, padx=10, pady=10)
label_status = tk.Label(window, text="")
label_status.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Create and place the entry fields
entry_mssv = tk.Entry(window)
entry_mssv.grid(row=0, column=1, padx=10, pady=10)
entry_ten = tk.Entry(window)
entry_ten.grid(row=1, column=1, padx=10, pady=10)
combobox_gioitinh = ttk.Combobox(window, values=gioitinh_values,width =17)
combobox_gioitinh.grid(row=2, column=1, padx=10, pady=10)
entry_cmnd = tk.Entry(window)
entry_cmnd.grid(row=3, column=1, padx=10, pady=10)
date_entry_ngay_sinh = CustomDateEntry(window, width= 17)

date_entry_ngay_sinh.grid(row=4, column=1, padx=10, pady=10)
entry_tenlop = tk.Entry(window)
entry_tenlop.grid(row=5, column=1, padx=10, pady=10)

# Create and place the "Add Student" button
btn_add = tk.Button(window, text="Thêm sinh viên", command=add_student)
btn_add.grid(row=6, column=1, padx=10, pady=10)


window.mainloop()

