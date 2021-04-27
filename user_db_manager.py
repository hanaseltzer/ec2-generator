from tkinter import * 
from tkinter import messagebox
import sqlite3
import boto3



class db():
    def __init__(self,root):
        #username
        self.name = None
        #sqlite cursor
        self.c = None
        #sqlite connection
        self.conn = None
        #tkinter master
        self.root = root
        #the boto 3 resource
        self.ec2 = None
        self.ec2_r = None
        # the fields the user gives and the database stores
        self.user_fields = [
                            "username",
                            "AWS_Access_Key_ID",
                            "AWS_Secret_Access_Key",
                        ]
        self.connect()
        self.loginW = None
    def connect(self):
        self.conn = sqlite3.connect("user.db")
        self.c = self.conn.cursor()

    def create_table(self):
        longstring = """ CREATE TABLE IF NOT EXISTS creds ( """
        for column in self.user_fields:
            longstring += column + """ text,"""
        longstring = longstring[:len(longstring)-1] + """)"""
        self.c.execute(longstring)

    def delete_table(self):
        self.c.execute(""" DROP TABLE IF EXISTS creds """)

    #reads the information from the database for athenticating to aws
    def get_user(self):
        self.c.execute("""SELECT * FROM creds """)
        listt = self.c.fetchall()
        result = {}
        i=0
        for field in listt:
            result[self.user_fields[i]]=field
            i+=1
        return result
    #the login function that the button in the login window activates
    def login(self,dic):
        self.connect()
        self.logged = True
        # making sure user entered all of the input fields
        for key,value in dic.items():
            if (value.get() == ""):
                messagebox.showinfo(title="login error",message="invalid input \nmust enter "+ key)
                return None
        # making sure that the creds table is created and emtey
        self.delete_table()
        self.create_table()
        # getting the values prepard for inserting to the table
        keys="("
        values="('"
        for key,value in dic.items():
            keys+=key + ","
            values+=value.get() + "','"
        keys=keys[:len(keys)-1] + ")"
        values=values[:len(values)-2] + ")"
        #inserting the preperd values to the table
        self.c.execute("""INSERT INTO creds """ + keys + """VALUES""" + values + ";")
        self.athunticate()
        self.close()

        self.root.logedin = self.root.Db.user_logedin()
        self.loginW.destroy()
        self.root.user_boxing()


    def athunticate(self):
        try:
            self.c.execute("""SELECT * FROM creds ;""")
        
        except:
            return False
        results=self.c.fetchall()
        #need to run aws configure with these parameters
        self.username = results[0][0]
        self.ec2 = boto3.client(
                            service_name='ec2',
                            region_name='us-east-2',
                            aws_access_key_id=results[0][1],
                            aws_secret_access_key=results[0][2]
                        )
        return self.ec2

    def athu_r(self):
        try:
            self.c.execute("""SELECT * FROM creds ;""")
        
        except:
            return False
        results=self.c.fetchall()
        #need to run aws configure with these parameters
        self.username = results[0][0]
        self.ec2_r = boto3.resource(
                            'ec2',
                            region_name='us-east-2',
                            aws_access_key_id=results[0][1],
                            aws_secret_access_key=results[0][2]
                        )
        return self.ec2_r

        
        #for status in self.ec2.meta.client.describe_instance_status()['InstanceStatuses']:
        #    print(status)
        
        
     
        
 
    #login popup window
    def login_window(self):
        self.logged = True
        self.loginW=Toplevel(self.root,bg="#1F1420")
        self.loginW.wm_attributes('-topmost',True)
        entrys = {}
        self.loginW.title('Login')
        for i in range(len(self.user_fields)):
            label = Label(self.loginW,text=self.user_fields[i],bg="#1F1420",fg="#d6a2e0")
            entrys[self.user_fields[i]]=Entry(self.loginW,width=20,bg="#3f3a40",fg="#d6a2e0")
            label.grid(row=i+1,column=1,padx=15,pady=10)
            entrys[self.user_fields[i]].grid(row=i+1,column=2,padx=15,pady=10)
        login_btn=Button(self.loginW,text='Login',bg="#1F1420",fg="#d6a2e0",command= lambda dic=entrys : self.login(dic))
        login_btn.grid(row=len(entrys)+1,column=1,columnspan=2,padx=15,pady=20)
        self.loginW.mainloop()
        
    def user_logedin(self):
        cred_exists = True
        try:
            self.c.execute("""SELECT * from creds;""")
        except:
            cred_exists = False
        if (cred_exists):
            name = self.c.fetchall()
            self.name = name[0][0]
            #check if to remove next line
            self.athunticate()
        return cred_exists

        
    def get_username(self):
        if (self.user_logedin()):
            return self.name
    def close(self):
        self.conn.commit()
        self.conn.close()
      

    