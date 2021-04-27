import boto3
from tkinter import *
import json

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
def get_os(ami):
    keys = ami_transalate.keys()
    values = ami_transalate.values()
    if ami in values:
        answer = ""
        i = 0
        x=0
        distro = ""
        for key,value in ami_transalate.items():
            if value == ami:
                distro = key
                x = i
                break
            i += 1
        if x < 3:
            answer += "Windows - "
        elif x < 6:
            answer += "macOS - "
        else:
            answer += "Linux - "
        answer += distro
        return answer
    else:
        return ami

class Instence(Frame):

    def __init__(self,_master,name,status,ip,operating_system,id,ec2):
        self.id = id
        self.ec2 = ec2
        if status == "running" :
            self.backgroud = "#41c445"
        else:
            self.backgroud = "#bd5a3e"
        super().__init__(_master,bg=self.backgroud,width=250,height=550)
        Label(self,text="VM")
        self.name = name
        self.name_l = Label(self,text="name: "+ name,bg=self.backgroud).grid(sticky=W,row=2)
        self.status_l = Label(self,text="status: "+ status,bg=self.backgroud).grid(sticky=W,row=3)
        self.ip_l = Label(self,text="ip: "+ ip,bg=self.backgroud).grid(sticky=W,row=4)
        self.ami_l = Label(self,text="image: "+ get_os(operating_system),bg=self.backgroud).grid(sticky=W,row=5)
        self.menu = Menu(_master,tearoff=False)
        if status == 'running':
            state = 'normal'
        else: 
            state = 'disable'
        self.menu.add_command(label="Shut down",state=state,command=self.shutdown_vm)
        if status == 'stopped':
            state = 'normal'
        else: 
            state = 'disable'
        self.menu.add_command(label="Start",state=state,command=self.start_vm)
        if status != 'terminated' and status != 'terminating' :
            state = 'normal'
        else: 
            state = 'disable'
        self.menu.add_command(label="Terminate",state=state,command=self.term_vm)
        self.bind("<Button-3>",self.popup)
    def popup(self,e):
            self.menu.tk_popup(e.x_root,e.y_root)
    def shutdown_vm(self):
        self.ec2.stop_instances(InstanceIds=[self.id])
    def start_vm(self):
        self.ec2.start_instances(InstanceIds=[self.id])

    def term_vm(self):
        self.ec2.terminate_instances(InstanceIds=[self.id])


def get_instances(ec2_client):
        reservations = ec2_client.describe_instances()
        instances = []
        for i,reservation in enumerate(reservations["Reservations"]):
            instances.append({})
            for instance in reservation["Instances"]:
                instances[i]["instance_name"] = instance["PublicDnsName"].split('.')[0]
                instances[i]["instance_type"] = instance["InstanceType"]
                instances[i]["instance_image"] = instance["ImageId"]
                instances[i]["instance_id"] = instance["InstanceId"]
                instances[i]["instance_status"] = instance["State"]["Name"]
                if instances[i]["instance_status"] == 'running':
                    instances[i]["public_ip"] = instance["PublicIpAddress"]
                else: 
                    instances[i]["public_ip"] = ""
                if instances[i]["instance_status"] != 'terminated':
                    instances[i]["private_ip"] = instance["PrivateIpAddress"]
                else: 
                    instances[i]["private_ip"] = ""
                
        return instances

