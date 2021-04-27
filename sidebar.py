from tkinter import *
class sidebar(Frame):
    def __init__(self,_master,OL,chsO,**kywrds):
        super().__init__(_master,bg='#533657',**kywrds)
        self.OL=OL
        self.chsO=chsO
        self.buttonlist=[]
        self.grid_propagate(0)
        
        i = 0
        for O,L in self.OL.items():
            kywrdz={
            "width" : 150,
            "height" : 3,
            "text" : O,
            "fg" : 'white',
            "command" : lambda O=O, L=L, n=i : self.view(L,O,n),
            "activebackground" : 'gray'
            }
            self.buttonlist.append(Button(self,bg="#5f4866",**kywrdz))
            self.buttonlist[i].grid(row=2+i ,column= 2)
            
            if i==chsO-1:
                self.buttonlist[i].configure(bg="#1F1420")
            i+=1
    def view(self,frame,o,n):
        for framee in self.OL.values():
            framee.grid_forget()
        frame.grid(row=1, column=2)
        j=0
        for button in self.buttonlist:
            if (n==j):
                self.buttonlist[j].configure(bg="#1F1420")
            else: 
                self.buttonlist[j].configure(bg="#5f4866")
            j+=1
        
            

    

