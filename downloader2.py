# -*- coding: UTF-8 -*-
import os
import socketUtil
import Tkinter
import tkFileDialog

import time
import threading
import traceback

remoteIP="123.206.195.156"
port=17650
workingType="host_send" #host_send host_recv client_send client_recv 
blocksize=1024
sendfile=""
recvfile=""

linecounting=0.0



def setWorkingType(str):
    global workingType
    workingType=str

def setWorkingType2():
    global workingType
    global radioSet
    workingType=radioSet.get()

def test():
    global workingType
    global sendfile
    global recvfile
    print workingType,sendfile, recvfile

def openFileDialog():
    global workingType
    mode=workingType.split("_")[1]
    if mode=="send":
        openFileSelect()
    else:
        openFileSave()

def openFileSelect():
    global sendfile
    sendfile=tkFileDialog.askopenfilename(title="选择发送的文件")
    entry2.delete(0, "end")
    entry2.insert(0,sendfile)

def openFileSave():
    global recvfile
    recvfile=tkFileDialog.asksaveasfilename(title="选择接收的位置")
    entry2.delete(0, "end")
    entry2.insert(0,recvfile)

def startTransfer():
    global remoteIP
    global port
    global workingType
    global blocksize
    global sendfile
    global recvfile

    port=entry1.get()
    remoteIP=entry0.get()

    with open("conf.ini","w") as fp:
        fp.write(str(port)+"|"+str(remoteIP))

    # print remoteIP,port,workingType,blocksize,sendfile,recvfile
    bgworking=bgWorking(remoteIP,port,workingType,blocksize,sendfile,recvfile)
    bgworking.start()
    



#############################


class bgWorking(threading.Thread):
    def __init__(self,remoteIP,port,workingType,blocksize,sendfile,recvfile):
        threading.Thread.__init__(self)
        self.remoteIP=remoteIP
        self.port=port
        self.workingType=workingType
        self.blocksize=blocksize
        self.sendfile=sendfile
        self.recvfile=recvfile

    def run(self):
        try:
            if self.workingType=="host_send":
                self.run_host_send(self.port,self.blocksize,self.sendfile)
            elif self.workingType=="host_recv":
                self.run_host_recv(self.port,self.blocksize,self.recvfile)
            elif self.workingType=="client_send":
                self.run_client_send(self.port,self.blocksize,self.remoteIP,self.sendfile)
            elif self.workingType=="client_recv":
                self.run_client_recv(self.port,self.blocksize,self.remoteIP,self.recvfile)
        except Exception,e:
            print e
            # self.LogTolog("sys error")
            self.LogTolog(traceback.format_exc())

    def run_host_send(self,port, blocksize, sendfile):
        counting=0
        self.LogTolog("start")
        socketServer, conn, addr = socketUtil.startServer(port)
        self.LogTolog("host "+str(addr))

        fp=open(sendfile, "rb")
        while 1:
            data=fp.read(blocksize)
            if data != "":
                counting=counting+blocksize
                socketUtil.sendData(data, socketServer, conn, "server")
            else:
                socketUtil.sendData(data, socketServer, conn, "server")
                break
            # self.LogTolog(str(round(counting/1024.0/1024.0,2))+"MB")
            self.LogToSameline(str(round(counting/1024.0/1024.0,2))+"MB")
        fp.close()
        socketUtil.endServer(socketServer, conn)
        self.LogTolog("send done")


    def run_host_recv(self,port,blocksize,recvfile):
        counting=0
        self.LogTolog("start")
        socketServer, conn, addr = socketUtil.startServer(port)
        self.LogTolog("host "+str(addr))

        fp=open(recvfile,"ab")
        while 1:
            data = socketUtil.receiveData(blocksize, socketServer, conn, "server")
            fp.flush()
            if data != "":
                counting=counting+blocksize
                fp.write(data)
            else:
                fp.write("")
                break
            # self.LogTolog(str(round(counting/1024.0/1024.0,2))+"MB")
            self.LogToSameline(str(round(counting/1024.0/1024.0,2))+"MB")
        fp.close()
        socketUtil.endServer(socketServer, conn)
        self.LogTolog("receive done")


    def run_client_send(self,port,blocksize,remoteIP,sendfile):
        counting=0
        self.LogTolog("start")
        socketClient = socketUtil.startClient(remoteIP,port)
        self.LogTolog("connected to "+remoteIP)

        fp=open(sendfile, "rb")
        while 1:
            data=fp.read(blocksize)
            if data != "":
                counting=counting+blocksize
                socketUtil.sendData(data,socketClient, None, "client")
            else:
                socketUtil.sendData(data,socketClient, None, "client")
                break
            # self.LogTolog(str(round(counting/1024.0/1024.0,2))+"MB")
            self.LogToSameline(str(round(counting/1024.0/1024.0,2))+"MB")

        fp.close()
        socketUtil.endClient(socketClient)
        self.LogTolog("send done")


    def run_client_recv(self,port,blocksize,remoteIP,recvfile):
        counting=0
        self.LogTolog("start")
        socketClient = socketUtil.startClient(remoteIP,port)
        self.LogTolog("connected to "+remoteIP)

        fp=open(recvfile,"ab")
        while 1:
            data = socketUtil.receiveData(blocksize, socketClient, None, "client")
            fp.flush()
            if data != "":
                counting=counting+blocksize
                fp.write(data)
            else:
                fp.write("")
                break
            # self.LogTolog(str(round(counting/1024.0/1024.0,2))+"MB")
            self.LogToSameline(str(round(counting/1024.0/1024.0,2))+"MB")
        fp.close()
        socketUtil.endClient(socketClient)
        self.LogTolog("receive done")

    def LogTolog(self,s):
        global linecounting
        listLog.insert("end",str(s)+"\n")
        linecounting=linecounting+1
        # print str(s)  

    def LogToSameline(self,s):
        global linecounting
        listLog.delete(linecounting,linecounting+1)
        linecounting=linecounting-1
        self.LogTolog(s)

    




############################# UI start
fp=open("conf.ini","a")
fp.close()
with open("conf.ini","r") as fp:
    line=fp.readline()
    print line
    if line != None and line != "":
        port=line.split("|")[0]
        remoteIP=line.split("|")[1]
print port,remoteIP

UI=Tkinter.Tk()
# UI.configure(background='black')
UI.title("socket下载")
# UI.geometry("355x180")
UI.geometry("355x500")
# UI.minsize(400,400)
# UI.maxsize(400,400)
UI.resizable(width=False, height=False)

Tkinter.Label(UI,text="远程地址").grid(row=0, column=0)
entry0=Tkinter.Entry(UI)
entry0.grid(row=0, column=1, columnspan=3, sticky="w" + "e")
entry0.insert(0,remoteIP)

Tkinter.Label(UI,text="端口").grid(row=1, column=0)
entry1=Tkinter.Entry(UI)
entry1.grid(row=1, column=1, columnspan=3, sticky="w" + "e")
entry1.insert(0,port)

radioSet=Tkinter.StringVar()
radioSet.set("host_send")
Tkinter.Radiobutton(UI,text="服务端发送",value="host_send", variable=radioSet, command=setWorkingType2).grid(row=2, column=0)
Tkinter.Radiobutton(UI,text="服务端接收",value="host_recv", variable=radioSet, command=setWorkingType2).grid(row=2, column=1)
Tkinter.Radiobutton(UI,text="客户端发送",value="client_send", variable=radioSet, command=setWorkingType2).grid(row=2, column=2)
Tkinter.Radiobutton(UI,text="客户端接收",value="client_recv", variable=radioSet, command=setWorkingType2).grid(row=2, column=3)
   
# Tkinter.Button(UI,text="服务端发送", command=lambda :setWorkingType("host_send")).grid(row=1, column=0)
# Tkinter.Button(UI,text="服务端接收", command=lambda :setWorkingType("host_recv")).grid(row=1, column=1)
# Tkinter.Button(UI,text="客户端发送", command=lambda :setWorkingType("client_send")).grid(row=1, column=2)
# Tkinter.Button(UI,text="客户端接收", command=lambda :setWorkingType("client_recv")).grid(row=1, column=3)
#Tkinter.Button(UI,text="test", command=test).grid(row=3, column=0)

Tkinter.Button(UI,text="选择文件",command=openFileDialog).grid(row=3,column=0)
# Tkinter.Button(UI,text="选择接收的位置",command=openFileSave).grid(row=3,column=2,columnspan=2)

# Tkinter.Label(UI,text="发送的文件").grid(row=4, column=0, sticky="w")
entry2=Tkinter.Entry(UI)
entry2.grid(row=3, column=1, columnspan=3, sticky="w" + "e")

# Tkinter.Label(UI,text="接收的文件").grid(row=5, column=0, sticky="w")
# entry3=Tkinter.Entry(UI)
# entry3.grid(row=5, column=1, columnspan=3, sticky="w" + "e")

Tkinter.Button(UI,text="开始",command=startTransfer).grid(row=6,columnspan=4)

Tkinter.Label(UI,text="Log").grid(row=7,columnspan=4, sticky="w")
listLog=Tkinter.Text(UI)
listLog.grid(row=8,columnspan=512)

UI.mainloop()
