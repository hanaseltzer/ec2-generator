from tkinter import *
import boto3


def create_i_frame(root,logedin):
    new_i_frame = Frame(root,height=650,width=1050,bg="#1F1420")
    new_i_frame.grid(row=1, column=2)

    new_i_frame.pack_propagate(0)

    titleLabel = Label(new_i_frame,text="first",width=50).pack()
    if logedin:
        ec2 = boto3.resource('ec2')
        instances = get_instances(ec2)

        for instance in instances:
            print(instance.id, instance.instance_type)


    return new_i_frame

def get_instances(ec2):
    instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    return instances