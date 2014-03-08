#!/usr/bin/python           

import socket  
import random  
import string
import pickle 
import getpass
from Crypto.Cipher import AES

def keyGenerator(size):
  return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for number in range(size))

def encryptPassword(password):
  key = keyGenerator(16)  
  ciphertext = "0000000000000000000000000000000000000000000000000000000000000000"
  iv = ciphertext[:16]
  cypher = AES.new(key, AES.MODE_CFB, iv)
 
  return key, cypher.encrypt(password)

def readUserData():
  user = raw_input('user: ')
  password = getpass.getpass('password: ')
  return user, password

def returnOption(option):
  if option.lower() == 'n':
    return False
  elif option.lower() != 'y':
    print 'Invalid option.'
    return False
  return True

def recvData(c, size):
  rawData = c.recv(size) 
  return pickle.loads(rawData) 

def sendData(c, data):
  c.send(pickle.dumps(data))

def sendUserData(c):
  user, password = readUserData()
  key, encryptedPassword = encryptPassword(password)
  data = {'user': user, 'key': key, 'password': encryptedPassword}
  
  sendData(c, data)
  tryAgain = recvData(c, 1024)

  if not tryAgain:
    print 'Logged in!'
    c.close()  
  else:
    option = raw_input('Incorrect user or password.Try again?[y/n]: ')
    if returnOption(option):
      sendData(c, True) 
      sendUserData(c) 
    else:
      sendData(c, False)
       

def connectToServer():
  s = socket.socket()         
  host = socket.gethostname() 
  port = 13333
  s.connect((host, port))
  sendUserData(s)
  
if __name__ == '__main__':
  connectToServer()
               
