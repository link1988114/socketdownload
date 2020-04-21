# -*- coding=UTF-8 -*-
#coding=utf-8

import socket

def startServer(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", int(port)))
    s.listen(1)
    print "listening..."
    conn, addr = s.accept()
    print str(addr) + "connected"
    return s, conn, addr

def startClient(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    return s

def endServer(socket, conn):
    conn.close()
    socket.close()

def endClient(socket):
    socket.close()

def sendData(data, socket, conn, type):
    if not data:
        return "failed"
    else:
        if type=="server":
            conn.send(data)
        else:
            socket.send(data)
    return "done"

def receiveData(blocksize, socket, conn, type):
    data=""
    if type=="server":
        data=conn.recv(blocksize)
    else:
        data=socket.recv(blocksize)
    return data

