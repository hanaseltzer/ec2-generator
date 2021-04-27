from tkinter import *
from user_db_manager import db

class UserBox(Frame):
    def __init__(self,_master,**kywrds):
        super().__init__(_master,bg="#3f3a40",**kywrds)
        self.parent = _master
        self.Db=db(self)
        self.username = self.Db.get_username()
        self.logedin = self.Db.user_logedin()
        self.grid_propagate(0)
        self.label = None
        self.Db.connect()
        self.user_boxing()
    
        
        
    def user_boxing(self):
        slaves = self.winfo_children()
        for slave in slaves:
            if isinstance(slave,Button) or isinstance(slave,Label):
                slave.destroy()
        self.Db.connect()
        if self.logedin:
            self.label = Label(self,bg="#3f3a40",fg="#d6a2e0",text="Hi, "+self.username)
            self.label.grid()
            self.outbutton = Button(self,text="Logout",bg="#3f3a40",fg="#d6a2e0",command=self.logout)
            self.outbutton.grid()
        else:
            self.Db.close()
            self.loginbutton = Button(self,text="Login",bg="#3f3a40",fg="#d6a2e0",command=self.login_happen)
            self.loginbutton.grid()
    def login_happen(self):
        self.Db.connect()
        self.Db.login_window()
        self.wait_window(self.Db.loginW)
        self.logedin = self.Db.user_logedin()
        self.user_boxing()
        
        
        
    def logout(self):
        self.Db.connect()
        self.Db.delete_table()
        self.Db.close()
        self.logedin = self.Db.user_logedin()
    
        self.user_boxing()
