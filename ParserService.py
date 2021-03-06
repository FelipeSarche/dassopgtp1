

#!/usr/bin/python3
import signal 
from threading import Thread
from time import sleep
import socket
import json


UDP_IP = "127.0.0.1"
UDP_PORT = 10000
TIEMPOLECTURA=30



def handler(sig, frame):  # define the handler  
    print("Signal Number:", sig, " Frame: ", frame) 
    exit(0)
 

   

class Divisas:
    def __init__(self,dir):
        self.dirDivisas=dir

    def get_lista(self): #obtine una lista a partir del csv
        try:
            with open(self.dirDivisas, "r") as f:
                path=f.read()
                texto=path.split('\n')
        except:
            print("Error lectura "+self.dirDivisas)

        try:
            with open(texto[0], "r") as f:
                archivo=f.read()
        except:
            print("Error lectura "+archivo)
        lista=archivo.split('\n')
        return lista
    
    def get_json(self): #apartir de la lista construye una trama con formato json
        lista=self.get_lista()
        #print(lista)
        item=[]
        try:
            for i in range(len(lista)):
                if i==0:
                    llave=lista[0].split(',')
                else:
                    dic=dict()
                    r=lista[i].split(',')
                    dic[llave[0]]=int(r[0])
                    dic["value1"]=float(r[2])
                    dic["value2"]=float(r[3])
                    dic["name"]=r[1]
                    item.append(dic)
            return json.dumps(item)
        except:
            print("Error jason process")
            return " "
        
       
        





signal.signal(signal.SIGINT, handler) 
ob=Divisas("config.txt")
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
try:
    while True:#en este lazo envia la trama cada cierto tiempo
  
        print(ob.get_json())
        sock.sendto(bytes(ob.get_json(), "utf-8"), (UDP_IP, UDP_PORT))
        sleep(TIEMPOLECTURA)

 
finally:
    sock.close()#cierro el puerto
    print("socket cerrado")



    
