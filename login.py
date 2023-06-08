from tkinter import *
from tkinter import messagebox
import ActionDB

root=Tk()
root.title('Đăng nhập')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False,False)

def signin():
    username=user.get()
    password=code.get()
    teacher=FALSE
    # if username=='admin' and password=='1234':
    #     root.destroy()
    #     import main_Teacher

    # elif username!='admin' and password!='1234':

    #     messagebox.showerror("Invaid","Invaid username and password")
    teacher=ActionDB.CheckLogin(username,password)
    if teacher:
        root.destroy()
        import main_Teacher

    else:
        messagebox.showerror("Invaid","Invaid username and password")


def diemdanh():

    root.destroy()
    import main_Student
    

img=PhotoImage(file='static\img\login.png')
Label(root,image=img,bg='white').place(x=50,y=50)

frame=Frame(root,width=350,height=350,bg="white")
frame.place(x=480,y=70)

heading=Label(frame,text='Đăng nhập',fg='#57a1f8',bg='white',font=("Time New Roman",23,'bold'))
heading.place(x=100,y=5)


#########################---------------------------------
def user_on_enter(e):
    user.delete(0,'end')

def user_on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')

user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Time New Roman',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>', user_on_enter)
user.bind('<FocusOut>', user_on_leave)


Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

#########################---------------------------------

def code_on_enter(e):
    code.delete(0,'end')

def code_on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')


code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Time New Roman',11))
code.place(x=30,y=150)
code.insert(0,"Password")
code.bind('<FocusIn>', code_on_enter)
code.bind('<FocusOut>', code_on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

#########################---------------------------------
Button(frame,width=39,pady=7,text='Đăng nhập',bg='#57a1f8',fg='white',border=0,command=signin).place(x=35,y=204)
label=Label(frame,text="Bạn không phải là giáo viên?",fg='black',bg='white',font=('Time New Roman',9))
label.place(x=40,y=270)


sign_up=Button(frame,width=15,text='Đến điểm danh',border=0,bg='white',cursor='hand1',fg='#57a1f8',command=diemdanh)
sign_up.place(x=215,y=270)



root.mainloop()