from tkinter import *
from sidebar import sidebar
#from create_i_frame import create_i_frame
from user_box import UserBox
from instance import Instence,get_instances
from  create import create_i_window

root = Tk()

#display
backgroundcolor='black'


#mainFrame
mainFrame = Frame(root,bg=backgroundcolor,width=1200,height=650)
mainFrame.grid_propagate(0)
mainFrame.grid(row=0, column = 0)


def load_stuff():

    view_all_i_frame = Frame(mainFrame,height=650,width=1050,bg="#1F1420")
    view_all_i_frame.grid_propagate(0)
    view_all_i_frame.grid(row=1, column=2)



    #create_new_i_frame = create_i_frame(mainFrame,False)


    #third = Frame(mainFrame,height=650,width=1050,bg="#1F1420")
    #third.grid(row=1, column=2)

    #listt = {
    #    'option 1' : create_new_i_frame,
    #    'option 2' : view_all_i_frame,
    #    'option 3' : third
    #}


    #Sidebar = sidebar(mainFrame,listt,1,height=580,width=150)
    #Sidebar.grid(row=1,column=1)

    userbox = UserBox(mainFrame,height=70,width=150)
    userbox.grid(row=0,column=1)


    ec2_r = userbox.Db.athu_r()

    refresh_button = Button(mainFrame,text="refresh",width=5,height=2,bg="#473846",command=load_stuff)
    refresh_button.grid(row=0,column=2,sticky=W,padx=50)

    new_i_button = Button(view_all_i_frame,text="+",width=5,height=2,bg="#473846",command=lambda:create_i_window(root,ec2_r))
    new_i_button.grid(row=0,column=1,pady=30,padx=30)

    ec2 = userbox.Db.athunticate()
    if ec2:
        instences = get_instances(ec2)
        columns = [1,2,3,4]
        for i,instence_args in enumerate(instences):
            instence = Instence(view_all_i_frame,instence_args["instance_name"],instence_args["instance_status"],instence_args["public_ip"],instence_args["instance_image"],instence_args['instance_id'],ec2)
            instence.grid(row=1+(1+i)//5,column=columns[i%4],padx=25,pady=50)
            
        

    root.mainloop()

load_stuff()
