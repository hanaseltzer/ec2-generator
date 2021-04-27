from tkinter import *

root=Tk()

def button_command(x):
    print(x)


buttons=[]
for i in range(5):
    buttons.append(Button(root,command=lambda i=i : button_command(i)))
    buttons[i].pack()



root.mainloop()