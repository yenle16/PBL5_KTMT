import sqlite3

# def getAllSV():
#     conn = sqlite3.connect('Database.db')

#     query = "Select SinhVien.ten from SinhVien "

#     cursor = conn.execute(query)

#     result = []

#     for row in cursor:
#         result.append(row[0])

#     conn.close()
#     return  result
def getAllSV():
    conn = sqlite3.connect('Database.db')
    query = "Select SinhVien.mssv , SinhVien.ten from SinhVien"
    cursor = conn.execute(query)
    result_ma_SV = []
    result_ten_SV = []
    for row in cursor:
        result_ma_SV.append(row[0])
        result_ten_SV.append(row[1])
    conn.close()
    return  (result_ma_SV,result_ten_SV)

def AddSV(mssv,ten,gioi_tinh,cmnd,ngay_sinh,id_lop):
    # Connect to the database
    conn = sqlite3.connect('Database.db')
    cursor = conn.cursor()

    # Insert student into the database
    cursor.execute("INSERT INTO SinhVien (mssv, ten, gioitinh, cmnd, ngaysinh, id_lop) VALUES (?, ?, ?, ?, ?, ?)",
                   (mssv, ten, gioi_tinh, cmnd, ngay_sinh, id_lop))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def AddSinhVienHocPhan(mssv, id_monhoc_hocki):
    conn =sqlite3.connect('Database.db')
    cursor = conn.cursor()

    # Insert student into the database
    cursor.execute("INSERT INTO MonHoc_SinhVien (mssv,id_monhoc_hocki) VALUES (?, ?)",
                   (mssv,id_monhoc_hocki ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def getmaLopbytenLop(tenLop):
    conn = sqlite3.connect('Database.db')

    query = "Select Lop.id_lop from Lop Where Lop.ten='%s'" % tenLop

    cursor = conn.execute(query)

    result = None

    for row in cursor:
        result = row

    conn.close()

    conn.close()

    return  result


def getDataLop():
    conn = sqlite3.connect('Database.db')

    query = "Select Lop.ten from Lop "

    cursor = conn.execute(query)

    result = []

    for row in cursor:
        result.append(row)

    conn.close()
    return  result

def input_ImageDB(mssv):
    conn = sqlite3.connect('Database.db')
    query = "Select * from SinhVien Where mssv = " + str(mssv)
    cursor2 = conn.execute(query)

    result = None

    for row in cursor2:
        result = row
    conn.close()
    return result

def nhandienDB():
    conn = sqlite3.connect('Database.db')
    query_arr_mssv = "Select SinhVien.mssv from SinhVien"
    cursor = conn.execute(query_arr_mssv)

    arr_mssv = []

    for row in cursor:
        arr_mssv.append(row[0])
    
    return arr_mssv

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

def getDataCBB(masogv,hocki,monhoc):
    conn = sqlite3.connect('Database.db')

    # get msgv
    query_msgv = "Select GiangVien.msgv from GiangVien " \
                 "INNER JOIN Khoa ON Khoa.id_khoa = GiangVien.id_khoa " \
                 "Where GiangVien.ten = '%s'" % masogv
    cursor_msgv = conn.execute(query_msgv)
    kqua_msgv = None
    for row in cursor_msgv:
        kqua_msgv = row
    id_msgv = kqua_msgv[0]

    # get id_hocki
    query_id_hocki = "Select HocKi.id_hocki from HocKi  Where HocKi.ten = '%s'" % hocki
    cursor_id_hocki = conn.execute(query_id_hocki)
    kqua_id_hocki = None
    for row in cursor_id_hocki:
        kqua_id_hocki = row
    id_hocki = kqua_id_hocki[0]

    # get id_monhoc
    query_id_monhoc = "Select MonHoc.id_monhoc from MonHoc  Where MonHoc.ten = '%s'" % monhoc
    cursor_id_monhoc = conn.execute(query_id_monhoc)
    kqua_id_monhoc = None
    for row in cursor_id_monhoc:
        kqua_id_monhoc = row
    id_monhoc = kqua_id_monhoc[0]
    return (id_msgv, id_hocki, id_monhoc)

def show_svdiemdanh(result_data,ngay_diemdanh):
    conn = sqlite3.connect('Database.db')

    # now = datetime.now()
    # ngay_diemdanh = now.strftime("%d-%m-%Y")

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
    conn.close()
    return kqua_sv_diemdanh
def show_svdiemdanh(maGV,maHocki,maMonhoc,ngay_diemdanh):
    conn = sqlite3.connect('Database.db')

    # now = datetime.now()
    # ngay_diemdanh = now.strftime("%d-%m-%Y")

    query_svdiemdanh = "Select SinhVien.ten, SinhVien.mssv, SinhVienDiemDanh.gio_diemdanh, SinhVienDiemDanh.ngay_diemdanh, SinhVienDiemDanh.msgv from SinhVienDiemDanh " \
                       "INNER JOIN SinhVien ON SinhVien.mssv = SinhVienDiemDanh.mssv " \
                       "Where SinhVienDiemDanh.msgv = '%s' " \
                       "And SinhVienDiemDanh.id_hocki = '%s' " \
                       "And SinhVienDiemDanh.id_monhoc = '%s' " \
                       "And SinhVienDiemDanh.ngay_diemdanh = '%s'" % (
                       maGV, maHocki, maMonhoc, ngay_diemdanh)
    cursor_svdiemdanh = conn.execute(query_svdiemdanh)
    kqua_sv_diemdanh = []
    for row in cursor_svdiemdanh:
        kqua_sv_diemdanh.append(row)
    conn.close()
    return kqua_sv_diemdanh

def diemdanh():
    conn = sqlite3.connect('Database.db')
    query_check_svdiemdanh = "Select SinhVienDiemDanh.mssv, SinhVienDiemDanh.msgv, SinhVienDiemDanh.id_hocki, SinhVienDiemDanh.id_monhoc, SinhVienDiemDanh.ngay_diemdanh from SinhVienDiemDanh " \
                                     "INNER JOIN SinhVien ON SinhVien.mssv = SinhVienDiemDanh.mssv "
    cursor_check_svdiemdanh = conn.execute(query_check_svdiemdanh)
    kqua_check_svdiemdanh = []
    for row in cursor_check_svdiemdanh:
        kqua_check_svdiemdanh.append(row)
    return kqua_check_svdiemdanh

def thongketheongay(result_data,result_ngay_diemdanh):
    conn = sqlite3.connect('Database.db')
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

    conn.close()
    return kqua_sv_diemdanh


def thongkeHetMon(result_data,hocki):
    conn = sqlite3.connect('Database.db')
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

    return (kqua_all_sv,kqua_sv_diemdanh_kthucmon)

def getDataKhoa():
    conn = sqlite3.connect('Database.db')

    query = "Select Khoa.ten from Khoa "

    cursor = conn.execute(query)

    result = []

    for row in cursor:
        result.append(row[0])

    conn.close()
    return  result

def getmaKhoabytenKhoa(khoa):
    conn = sqlite3.connect('Database.db')
    query1 = "Select Khoa.id_khoa from Khoa  Where Khoa.ten = '%s'" % khoa
    cursor = conn.execute(query1)
    kqua = None
    for row in cursor:
        kqua = row

    conn.close()
    return kqua


# def getGiangVienIDbyKhoa(maKhoa):
#     conn = sqlite3.connect('Database.db')
#     query = "Select GiangVien.ten from GiangVien INNER JOIN Khoa ON GiangVien.id_khoa = Khoa.id_khoa Where Khoa.id_khoa = " + str(maKhoa)
#     cursor = conn.execute(query)
#     result = []
#     for row in cursor:
#         result.append(row[0])
#     conn.close()
#     return result
def getGiangVienIDbyKhoa(maKhoa):
    conn = sqlite3.connect('Database.db')
    query = "SELECT GiangVien.ten FROM GiangVien INNER JOIN Khoa ON GiangVien.id_khoa = Khoa.id_khoa WHERE Khoa.id_khoa = ?"
    cursor = conn.execute(query, (str(maKhoa),))
    result = [row[0] for row in cursor]
    conn.close()
    return result



def getmaGVbytenGV(tenGiangVien):
    conn = sqlite3.connect('Database.db')
    query = "Select GiangVien.msgv from GiangVien  Where GiangVien.ten = '%s'" % tenGiangVien
    cursor = conn.execute(query)
    result = []
    for row in cursor:
        result.append(row[0])
    conn.close()
    return result

def tenMonhoc_HockibymaGV(msgv):
    conn = sqlite3.connect('Database.db')
    query = "SELECT DISTINCT MonHoc.ten, HocKi.ten FROM MonHoc " \
            "INNER JOIN MonHoc_GiangVien ON MonHoc_GiangVien.id_monhoc = MonHoc.id_monhoc " \
            "INNER JOIN GiangVien ON GiangVien.msgv = MonHoc_GiangVien.msgv " \
            "INNER JOIN MonHoc_HocKi ON MonHoc.id_monhoc = MonHoc_HocKi.id_monhoc " \
            "INNER JOIN HocKi ON HocKi.id_hocki = MonHoc_HocKi.id_hocki " \
            "Where GiangVien.msgv = '%s' " % (msgv)

    cursor = conn.execute(query)
    result_ten_mh = []
    result_hocki = []
    for row in cursor:
        result_ten_mh.append(row[0])
        result_hocki.append(row[1])
    conn.close()
    return (result_ten_mh,result_hocki)



def getDataGiangVien(khoa,name_gv):
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
    result = []
    for row in cursor4:
        result_ten_mh.append(row[0])
        result.append(row[1])
    conn.close()
    return result


def getDataHocKi(giangvien):
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
    result = []

    for row in cursor3:
        result.append(row)
    conn.close()

    return result

def getDataMonHoc_GiangVien(giangvien,hocki):
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
    conn.close()
    return result_name_mh

def getmaMonhocbytenMonhoc(monhoc):
    conn = sqlite3.connect('Database.db')
    query_id_mh = "Select MonHoc.id_monhoc from MonHoc Where MonHoc.ten = '%s'" % monhoc
    cursor = conn.execute(query_id_mh)
    kqua = None
    for row in cursor:
        kqua = row
    conn.close()
    return kqua

def getmaHockibytenHocki(tenHocki):
    conn = sqlite3.connect('Database.db')
    query = "Select HocKi.id_hocki from HocKi  Where HocKi.ten = '%s'" % tenHocki
    cursor = conn.execute(query)
    result = None
    for row in cursor:
        result = row
    conn.close()
    return result

def gettenHockibymaGV(maGV):
    conn = sqlite3.connect('Database.db')
    query = "SELECT HocKi.ten FROM HocKi " \
            "INNER JOIN MonHoc_HocKi ON MonHoc_HocKi.id_hocki = HocKi.id_hocki " \
            "INNER JOIN MonHoc_GiangVien ON MonHoc_GiangVien.id_monhoc = MonHoc_HocKi.id_monhoc " \
            "INNER JOIN GiangVien ON GiangVien.msgv = MonHoc_GiangVien.msgv " \
            "Where GiangVien.msgv = '%s'" % (maGV)
    cursor = conn.execute(query)
    result = []

    for row in cursor:
        result.append(row)
    conn.close()
    return result


def gettenHockibymaMonhoc(idMonhoc):
    conn = sqlite3.connect('Database.db')
    query = "Select HocKi.ten from HocKi " \
                  "INNER JOIN MonHoc_HocKi ON HocKi.id_hocki = MonHoc_HocKi.id_hocki " \
                  "INNER JOIN MonHoc ON MonHoc.id_monhoc = MonHoc_HocKi.id_monhoc  " \
                  "Where MonHoc.id_monhoc = '%s'" % idMonhoc
    cursor = conn.execute(query)
    result = []
    for row in cursor:
        result.append(row)
    conn.close()
    return result

def getmaGVbytenGV(tenGV):
    conn = sqlite3.connect('Database.db')
    query = "Select GiangVien.msgv from GiangVien  Where GiangVien.ten = '%s'" % tenGV
    cursor = conn.execute(query)
    msgv = None
    for row in cursor:
        msgv = row
    conn.close()
    return msgv    

def getSVbyMonhocGVHocki(idMonhoc, maGV, tenHocki):
    conn = sqlite3.connect('Database.db')
    query = "Select SinhVien.ten, SinhVien.mssv from SinhVien " \
            "INNER JOIN MonHoc_SinhVien ON MonHoc_SinhVien.mssv = SinhVien.mssv " \
            "INNER JOIN MonHoc_HocKi ON MonHoc_HocKi.id = MonHoc_SinhVien.id_monhoc_hocki " \
            "INNER JOIN MonHoc ON MonHoc.id_monhoc = MonHoc_HocKi.id_monhoc " \
            "INNER JOIN MonHoc_GiangVien ON MonHoc_GiangVien.id_monhoc = MonHoc.id_monhoc " \
            "INNER JOIN GiangVien ON GiangVien.msgv = MonHoc_GiangVien.msgv " \
            "INNER JOIN HocKi ON HocKi.id_hocki = MonHoc_HocKi.id_hocki " \
            "Where MonHoc.id_monhoc = '%s' And GiangVien.msgv = '%s' And HocKi.ten = '%s'"  % (idMonhoc, maGV, tenHocki)

    cursor = conn.execute(query)

    result_name_sv = []
    result_mssv = []

    for row in cursor:
        result_name_sv.append(row[0])
        result_mssv.append(row[1])
    conn.close()
    return (result_name_sv,result_mssv)


def getDataLopHoc_Hocki(monhoc,hocki,giangvien):
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
    result_hocki

    query_msgv = "Select GiangVien.msgv from GiangVien  Where GiangVien.ten = '%s'" % giangvien
    cursor3 = conn.execute(query_msgv)
    msgv = None
    for row in cursor3:
        msgv = row
    msgv_result = msgv[0]


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

    conn.close()
    return (result_name_sv,result_mssv)



