from tkinter import *
import boto3


global os_chosan
global window
global distro_chosan
global distro_choise
global ec2

global ami_transalate
ami_transalate = {
    "2019" : "ami-0b697c4ae566cad55",
    "2016" : "ami-0f3593d61e59c226b",
    "2012 R2" :  "ami-01f6e0054f2a60694" ,
    "Big Sur" : "ami-0ef98d91ff9126a43",
    "Catalina" : "ami-0e8dcb1f4e055d786",
    "Mojave" : "ami-007e277d769aa198c",
    "Amazon" : "ami-05d72852800cbf29e",
    "Ubuntu" : "ami-08962a4068733a2b6", 
    "redhat" : "ami-03d64741867e7bb94",
    "SUSE" : "ami-0f052119b3c7e61d1",
    "Fedora" : "ami-000f295fe8c032706",
    "Kali" : "ami-0d26b04c810f2beec",
    "mint" : "",
    "centOS" : "ami-000e7ce4dd68e7a11",


}

def finish():
    global distro_chosan
    global ami_transalate
    global distro_choise
    distro_choise = distro_chosan.get()
    window.destroy()
    actully_create()

def almost_there(a,b,c):
    global window
    OKbutton = Button(window,text="ok",command=finish)
    OKbutton.pack(pady=20)
    


def drop_versions(a,b,c):
    global os_chosan
    global window
    global distro_chosan
    os_choise = os_chosan.get()
    distros = []
    if os_choise == 'Windows':
        way_of_saying = 'Version'
        distros = [
            "2019",
            "2016",
            "2012 R2"
        ]
    elif os_choise == 'macOS':
        way_of_saying = 'Version'
        distros = [
            "Big Sur",
            "Catalina",
            "Mojave"
        ]
    elif os_choise == 'Linux':
        way_of_saying = 'Distro'
        distros = [
            "Amazon",
            "Ubuntu",
            "redhat",
            "SUSE",
            "Fedora",
            "Kali",
            "mint",
            "centOS"
        ]

    distro_chosan = StringVar()
    distro_chosan.set(way_of_saying)
    drop1 = OptionMenu(window,distro_chosan,*distros)
    drop1.pack(pady=20)
    distro_chosan.trace("w",almost_there)



def create_i_window(root,ec2_client):
    global os_chosan
    global window
    global ec2
    ec2 = ec2_client
    window = Toplevel(root,bg="#5c3b59")
    window.wm_attributes('-topmost',True)
    os_chosan = StringVar()
    os_chosan.set("os-type")

    os_types = [
        "Windows",
        "macOS",
        "Linux",
    ]

    drop = OptionMenu(window,os_chosan,*os_types)
    drop.pack(pady=20)
    os_chosan.trace("w",drop_versions)
    return window

def actully_create():
        global ec2
        global distro_choise
        ec2.create_instances(ImageId=ami_transalate[distro_choise], MinCount=1, MaxCount=1,InstanceType='t2.micro')
