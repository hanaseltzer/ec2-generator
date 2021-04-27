from tkinter import * 
from PIL import ImageTk,Image
import sqlite3
import os

root=Tk()
root.title("database")
#root.iconbitmap(".\\img\\chill.ico")
root.geometry("400x400")

conn = sqlite3.connect('user.db')

c = conn.cursor()


    
c.execute(""" CREATE TABLE IF NOT EXISTS creds (
    firstName text,
    lastName text,
    AWS_Access_Key_ID text,
    AWS_Secret_Access_Key text,
    region_name text
    )""")


fields = [
    "firstName",
    "lastName",
    "AWS_Access_Key_ID",
    "AWS_Secret_Access_Key",
    "region_name"
]
fields_labels=[]
fields_entrys=[]
def query_fields(array):
    query=""
    for i in range(len(array)-1):
        query += ":" + array[i] + ","
    query+=":"+array[-1]
    return query

def get_dictionary(array_f,array_E):
    dick={}
    for i in range(len(array_f)):
        dick.update({str(array_f[i]) : str(array_E[i])})
    return dick

def update(record_list):
    Label(root,text=record_list).grid()

def search():
    global fields,fields_entrys
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    array_input = []
    emtey_entrys=0
    for i in range(len(fields_entrys)):
        array_input.append(fields_entrys[i].get())
        if (fields_entrys[i].get() == ''):
            emtey_entrys+=1
    if (emtey_entrys == len(fields)):
        c.execute("SELECT * FROM creds")
    else:
        search_details=get_dictionary(fields,array_input)
        keys=[]
        values=[]
        for key,value in search_details.items():
            if (value !=''):
                keys.append(key)
                values.append(value)
        search_dict=get_dictionary(keys,values)
        search_query=""
        i=1
        for key,value in search_dict.items():
            if (i == (len(search_dict))):
                search_query+= str(key) + " LIKE '" + str(value) + "'"
            else:
                search_query += str(key) + " LIKE '" + str(value) + "' AND " 
            i+=1
        c.execute("SELECT * FROM creds WHERE "+search_query)
    records = c.fetchall()
    searchWindow=Toplevel(root)
    edit_buttons=[]
    for record_l in records:
        i=0
        for record in record_l:
            Label(searchWindow,text=str(fields[i])+": "+str(record)).grid(sticky = W,padx=40,pady=2)
            i+=1
        edit_buttons.append(Button(searchWindow,text="edit",command=lambda: update(record_l)).grid(column=0,columnspan=2,pady=(2,20)))
    conn.commit()
    conn.close()

def submit():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    array_input=[]
    for i in range(len(fields_entrys)):
        array_input.append(fields_entrys[i].get())
    c.execute("INSERT INTO creds VALUES("+query_fields(fields)+")",get_dictionary(fields,array_input))
    conn.commit()
    conn.close()
    for entry in fields_entrys:
        entry.delete(0,END)
for i in range(len(fields)):
    fields_labels.append(Label(root,text=fields[i] + " :"))
    fields_entrys.append(Entry(root,width=20))
    fields_labels[i].grid(row=i,column=0,sticky=E,padx=10)
    fields_entrys[i].grid(row=i,column=1)

def delete_after_select(array,boolarray):
    conn = sqlite3.connect('user.db')
    c = conn.cursor() 
    membersToDelete=[]
    for i in range(len(array)):
        if (boolarray[i].get() == 1):
            membersToDelete.append(array[i])
    delete_query=""
    count=1
    for member in membersToDelete:
        deletedict = get_dictionary(fields,member)
        i=1
        for key,value in deletedict.items():
            if (i == (len(deletedict))):
                delete_query+= str(key) + " LIKE '" + str(value) + "'"
            else:
                delete_query += str(key) + " LIKE '" + str(value) + "' AND " 
            i+=1
        c.execute("DELETE FROM creds WHERE "+ delete_query )
        Label(root,text="option "+ str(count) + "has been deleted").grid()
        delete_query=""
        count+=1
    
    conn.commit()
    conn.close()

def delete():
    global fields,fields_entrys
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    array_input = []
    for i in range(len(fields_entrys)):
        array_input.append(fields_entrys[i].get())
    search_details=get_dictionary(fields,array_input)
    keys=[]
    values=[]
    for key,value in search_details.items():
        if (value !=''):
            keys.append(key)
            values.append(value)
    search_dict=get_dictionary(keys,values)
    search_query=""
    i=1
    for key,value in search_dict.items():
        if (i == (len(search_dict))):
            search_query+= str(key) + " LIKE '" + str(value) + "'"
        else:
            search_query += str(key) + " LIKE '" + str(value) + "' AND " 
        i+=1
    c.execute("SELECT * FROM creds WHERE "+search_query)
    records = c.fetchall()
    deleteWindow=Toplevel(root)
    deleteWindow.iconbitmap(".\\img\\chill.ico")
    deleteOrNot = []
    for i in range(len(records)):
        deleteOrNot.append(IntVar())
        deleteOrNot[i].set(0)
    i=0
    for record_l in records:
        j=0
        for record in record_l:
            if (j == 0):
                Checkbutton(deleteWindow,text=str(fields[j])+": "+str(record),variable=deleteOrNot[i],onvalue=1,offvalue=0).grid(sticky = W,padx=21)
            else:
                Label(deleteWindow,text=str(fields[j])+": "+str(record)).grid(sticky = W,padx=40)
            j+=1 
        i+=1
    delete_button_in_window=Button(deleteWindow,text="delete",command=lambda:delete_after_select(records,deleteOrNot)).grid(pady=20)
    conn.commit()
    conn.close()


submit_button=Button(root,text="SUBMIT",command=submit)
submit_button.grid(row=len(fields),column=0,columnspan=3,pady=10)

search_button=Button(root,text="search",command=search)
search_button.grid(row=len(fields)+2,column=0,columnspan=3,pady=5)

delete_button=Button(root,text="delete",command=delete)
delete_button.grid(row=len(fields)+3,column=0,columnspan=3,pady=5)



conn.commit()



conn.close()



root.mainloop()