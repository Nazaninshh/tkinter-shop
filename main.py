import sqlite3
import tkinter

try:
    cnt=sqlite3.connect('shop.db')
    # print("opened database succesfully")
except:
    print("an error occured in db connection")
#######------------- creat  users table-----------------
# query='''CREATE TABLE users
#     (ID INTEGER PRIMARY KEY,
#     user CHAR(25) NOT NULL,
#     pass CHAR(25) NOT NULL,
#     addr CHAR(25) NOT NULL,
#     comment CHAR(20)
# )'''
# cnt.execute(query)
# print("Table created successfully")
# cnt.close()

def product_table():
    pass

######------------- creat product table-----------------
# query='''CREATE TABLE product
#     (ID INTEGER PRIMARY KEY,
#     pname CHAR(25) NOT NULL,
#     price int NOT NULL,
#     qnt int NOT NULL,
#     comment CHAR(20)
# )'''
# cnt.execute(query)
# print("Table created successfully")


######--------------creat finalShop---------######uid,pid کلید خارجی هست چون در یه جدول دیگه کلید اصلی است####
# query='''CREATE TABLE finalShop
#     (ID INTEGER PRIMARY KEY,
#     uid int NOT NULL,
#     pid int NOT NULL,
#     qnt int NOT NULL
#     )'''
# cnt.execute(query)
# print("Table created successfully")
# cnt.close()


######--------------------- insert initial record in users table-------
# query=''' INSERT INTO users (user,pass,addr)
# VALUES ("admin","123456789","rasht")'''
# cnt.execute(query)
# cnt.commit()
# cnt.close()

######--------------------- insert initial record in product table-------
# query=''' INSERT INTO product (pname,price,qnt)
# VALUES ("nokia n95","100","20")'''
# cnt.execute(query)
# cnt.commit()
# cnt.close()

############----------functions---------------
def login():
    global userID,user
    user=user_text.get()
    pas=pass_text.get()
    query='''SELECT id FROM users WHERE user==? AND pass==? '''
    result=cnt.execute(query,(user,pas))
    rows=result.fetchall()
    #print(rows)
    if len(rows)<1 :
        msg_lbl.configure(text="wrong username or password!", fg="red")
        return
    userID=rows[0][0]
    if(user=="admin"):
        btn_Apannel.configure(state="active")

    #print(rows)
    msg_lbl.configure(text="welcome to your account", fg="green")
    btn_login.configure(state="disabled")
    btn_logout.configure(state="active")
    btn_submit.configure(state="disabled")
    btn_shop.configure(state="active")
    btn_myShop.configure(state="active")


    user_text.delete(0,"end")
    pass_text.delete(0, "end")

    user_text.configure(state="disabled")
    pass_text.configure(state="disabled")



def logout():
    msg_lbl.configure(text="you are logged out now", fg="green")
    btn_login.configure(state="active")
    btn_logout.configure(state="disabled")
    btn_shop.configure(state="disabled")
    user_text.configure(state="normal")
    pass_text.configure(state="normal")
    btn_submit.configure(state="active")
    btn_Apannel.configure(state="disabled")

def submit_win():
    global txt_user,txt_pass,txt_pc,txt_addr,lbl_submsg
    sub_win=tkinter.Toplevel(win)
    sub_win.title("submit panel")
    sub_win.geometry("300x300")
    sub_win.resizable(False,False)
    # -------------submit widget-----------------

    lbl_user=tkinter.Label(sub_win,text="Username")
    lbl_user.pack()
    txt_user=tkinter.Entry(sub_win,width=20)
    txt_user.pack()
    lbl_pass=tkinter.Label(sub_win, text="Password")
    lbl_pass.pack()
    txt_pass=tkinter.Entry(sub_win, width=20)
    txt_pass.pack()
    lbl_pc=tkinter.Label(sub_win,text="Password Confirmation")
    lbl_pc.pack()
    txt_pc =tkinter.Entry(sub_win, width=20)
    txt_pc.pack()
    lbl_addr=tkinter.Label(sub_win,text="Address")
    lbl_addr.pack()
    txt_addr =tkinter.Entry(sub_win, width=40)
    txt_addr.pack()
    lbl_submsg=tkinter.Label(sub_win,text="")
    lbl_submsg.pack()
    btn_finalSubmit=tkinter.Button(sub_win,text="Submit Now",command=submit)
    btn_finalSubmit.pack(pady=25)

    sub_win.mainloop()

def submit():
    user_id=txt_user.get()
    pass_id=txt_pass.get()
    cc_id=txt_pc.get()
    addr_id=txt_addr.get()
    #------- validation-------

    if(user_id=="" or pass_id=="" or cc_id=="" or addr_id==""):
        lbl_submsg.configure(text="Please fill All the Blanks", fg="red")
        return
    if(pass_id!=cc_id):
        lbl_submsg.configure(text="ERROR:  password and confirmation mismatch!! ", fg="red")
        return
    if(len(pass_id)<8):
        lbl_submsg.configure(text="ERROR: password must be least 8 chars!! ", fg="red")
        return

    #----------- submit username--------

    query='''SELECT user FROM users '''
    result=cnt.execute(query)
    rows=result.fetchall()
    # print(rows)

    count = 0
    for item in rows:
        if (user_id in item):
            count += 1

    if(count>0):
        lbl_submsg.configure(text="ERROR: username already exist", fg="red")

    else:
        query = ''' INSERT INTO users (user,pass,addr)
            values(?,?,?)'''
        cnt.execute(query,(user_id,pass_id,addr_id))
        cnt.commit()
        lbl_submsg.configure(text="SUCCESS: submit done!!", fg="green")


        txt_user.delete(0, "end")
        txt_pass.delete(0, "end")
        txt_pc.delete(0, "end")
        txt_addr.delete(0, "end")


def change_qnt():
    final_shop()

    #######------------ update product table---------
    new_qnt=real_pqnt-int(pqnt)
    query='''UPDATE product SET qnt=? WHERE id=?'''
    cnt.execute(query,(new_qnt,pId))
    cnt.commit()
    query = '''SELECT * FROM product'''
    result = cnt.execute(query)
    rows = result.fetchall()
    for i in rows:
        # msg= str(i[0]) + "----" + i[1] + "----Price:" + str(i[2]) + "----QNT:" + str(i[3]) #or
        msg = f"{i[0]}----{i[1]}----Price:{i[2]}----QNT:{i[3]}"
        lstbox.insert("end", msg)



    lbl_msg2.configure(text="successfully added to cart", fg="green")
    txt_id.delete(0,"end")
    txt_qnt.delete(0, "end")



def shop_win():
    global txt_id
    global txt_qnt
    global lbl_msg2,lstbox
    sh_win=tkinter.Toplevel(win)
    sh_win.title("shopping panel")
    sh_win.geometry("500x500")
    sh_win.resizable(False,False)

    #------- fetch all products---------

    query='''SELECT * FROM product'''
    result=cnt.execute(query)
    rows=result.fetchall()
    # print(rows)

    #------- Listbox-------------

    lstbox=tkinter.Listbox(sh_win, width=100)
    lstbox.pack(pady=10)
    for i in rows:
        #msg= str(i[0]) + "----" + i[1] + "----Price:" + str(i[2]) + "----QNT:" + str(i[3]) #or
        msg=f"{i[0]}----{i[1]}----Price:{i[2]}----QNT:{i[3]}"
        lstbox.insert("end",msg)



    #-------------shop widget-----------------
    lbl_id=tkinter.Label(sh_win,text="Product ID")
    lbl_id.pack()
    txt_id=tkinter.Entry(sh_win,width=20)
    txt_id.pack()
    lbl_qnt = tkinter.Label(sh_win, text="Product QNT")
    lbl_qnt.pack()
    txt_qnt = tkinter.Entry(sh_win, width=20)
    txt_qnt.pack()
    lbl_msg2=tkinter.Label(sh_win,text="")
    lbl_msg2.pack()
    btn_final_shop=tkinter.Button(sh_win,text="SHOP NOW",command=change_qnt)
    btn_final_shop.pack(pady=10)
    sh_win.mainloop()



def final_shop():
    global new_qnt,pId,real_pqnt,pqnt
    pId=txt_id.get()
    pqnt=txt_qnt.get()
    if(pId=="" or pqnt==""):
        lbl_msg2.configure(text="Please fill All the Blanks", fg="red")
        return
    query='''SELECT * FROM product WHERE id=?'''
    result=cnt.execute(query,(pId,))
    rows=result.fetchall()
    if len(rows)==0:
        lbl_msg2.configure(text="Wrong Product id",fg="red")
        return
    real_pqnt=rows[0][3]#داخل rows یک list است که میشه خونه 0 لیست و داخلش تاپل هست
    if(int(pqnt)>real_pqnt):
        lbl_msg2.configure(text="Not Enough Product Quantity ", fg="red")

    #######------------- insert to finalshop table--------
    query='''INSERT INTO finalShop(uid,pid,qnt)
        VALUES(?,?,?)'''
    cnt.execute(query,(userID,pId,pqnt))
    cnt.commit()


def my_shop():
    sh_win=tkinter.Toplevel(win)
    sh_win.title("my shop")
    sh_win.geometry("300x300")
    sh_win.resizable(False,False)
    #------- get id from username----------
    query='''SELECT id from users where user=?'''
    result=cnt.execute(query,(user,))
    row=result.fetchone()
    # print(row)
    #------- get pid,qnt from user------------
    query='''SELECT pid,qnt from finalShop where uid=?'''
    final_result=cnt.execute(query,(row[0],))
    rows=final_result.fetchall()
    #print(rows)
    #---------
    for i in rows:
        #print(i)

        query='''SELECT pname,price from product where id=?'''
        final_result=cnt.execute(query,(i[0],))
        row1=final_result.fetchall()
        #print(row1)
    lstbox=tkinter.Listbox(sh_win, width=100)
    lstbox.pack(pady=10)
    for i in row1:
        msg=f"Name:{i[0]}----Price:{i[1]}"
        lstbox.insert("end",msg)



def Apannel():
    global txt_Pname,txt_price,txt_quantity,lbl_insert
    admin_win=tkinter.Toplevel(win)
    admin_win.title("Admin panel")
    admin_win.geometry("300x300")
    admin_win.resizable(False,False)

    lbl_Pname = tkinter.Label(admin_win, text="Product Name")
    lbl_Pname.pack()
    txt_Pname = tkinter.Entry(admin_win, width=20)
    txt_Pname.pack(pady=3)

    lbl_price = tkinter.Label(admin_win, text="Price")
    lbl_price.pack()
    txt_price = tkinter.Entry(admin_win, width=20)
    txt_price.pack(pady=3)

    lbl_quantity = tkinter.Label(admin_win, text="Quantity")
    lbl_quantity.pack()
    txt_quantity = tkinter.Entry(admin_win, width=20)
    txt_quantity.pack(pady=3)
    btn_Pinsert=tkinter.Button(admin_win,text="Insert Product",command=insert_pro)
    lbl_insert=tkinter.Label(admin_win,text="")
    btn_Pinsert.pack(pady=10)

def insert_pro():

    p_name=txt_Pname.get()
    p_price=txt_price.get()
    p_quantity=txt_quantity.get()
    if(p_name!="" and p_price!="" and p_quantity!=""):
        query='''INSERT into product(pname,price,qnt)
        values(?,?,?)'''
        cnt.execute(query,(p_name,p_price,p_quantity))
        cnt.commit()
        txt_Pname.delete(0, "end")
        txt_price.delete(0, "end")
        txt_quantity.delete(0, "end")
        lbl_insert.configure(text="The products have been updated", fg='green')
    else:
        lbl_insert.configure(text="Please fill All the Blanks", fg="red")

##########----------------- TKinter()--------------
win=tkinter.Tk()
win.geometry("400x300")
win.title("login")

from tkinter import *
lab = Label(win,text=":) لطفا با دست باز نگاه کنید ",bg="crimson").pack()
user_lbl=tkinter.Label(win,text="Username: ")
user_lbl.pack()

user_text=tkinter.Entry(win,width=25)
user_text.pack()

pass_lbl=tkinter.Label(win,text="Password: ")
pass_lbl.pack()

pass_text=tkinter.Entry(win,width=25)
pass_text.pack()

msg_lbl=tkinter.Label(win,text="")
msg_lbl.pack()


btn_login=tkinter.Button(win,text="login",command=login)
btn_login.pack(pady="2")

btn_submit=tkinter.Button(win,text="submit",command=submit_win)
btn_submit.pack(pady="2")

btn_logout=tkinter.Button(win,text="logout",state="disabled",command=logout)
btn_logout.pack(pady="2")

btn_shop=tkinter.Button(win,text="shop",state="disabled",command=shop_win)
btn_shop.pack(pady="2")

btn_myShop=tkinter.Button(win,text="my shop",state="disabled",command=my_shop)
btn_myShop.pack(pady="2")

btn_Apannel=tkinter.Button(win,text="Admin Pannel",state="disabled",command=Apannel)
btn_Apannel.pack(pady="2")


win.mainloop()