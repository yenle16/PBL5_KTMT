import sqlite3
import datetime

def truy_xuat_lop_hoc_hien_tai():
    conn = sqlite3.connect('Database.db')  # Thay 'your_database.db' bằng tên cơ sở dữ liệu SQLite của bạn
    cursor = conn.cursor()
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.time().strftime("%H:%M:%S")  # Chuyển đổi thành chuỗi thời gian
    weekday = current_datetime.strftime('%A')
    query = """SELECT LopHocPhan.ten
               FROM LopHocPhan
               INNER JOIN TietHoc ON LopHocPhan.id_tiet = TietHoc.id
               WHERE TietHoc.giobatdau < ? AND LopHocPhan.Thu = ? """

    cursor.execute(query, (current_time,weekday))
    result = cursor.fetchall()

    if result:
        print("Các lớp học hiện tại:")
        for row in result:
            print(row)
    else:
        print("Không có lớp học nào có giờ bắt đầu nhỏ hơn thời gian hiện tại.")

    conn.close()

# Gọi hàm truy_xuat_lop_hoc_hien_tai để truy xuất các lớp học hiện tại
truy_xuat_lop_hoc_hien_tai()
