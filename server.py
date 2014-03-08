#!/usr/bin/python           

import socket  
import json
import pickle
import os
from threading import Thread
from Crypto.Cipher import AES

def writeToJsonFile(usersFile, users_data, user, password, index):
  data = {'entry' + str(index): {'user': user, 'password': password}}
  users_data.update(data)
  json.dump(data, usersFile)
  usersFile.write('\n')

def readFromJsonFile(users_data):
  try:
    if os.stat('users.json').st_size == 0: #empty
      return False
    with open('users.json', 'r') as usersFile:
      for line in usersFile:
        users_data.update(json.loads(line))
  except IOError:
    return False
  except OSError:
    return False

  return True

def returnOption(option):
  if option.lower() == 'n':
    return False
  elif option.lower() != 'y':
    print 'Invalid option.'
    return False
  return True

def addMoreUsers(user_data):
  option = raw_input('Do you wish to add some users?[y/n]: ')
  stillAddUsers = returnOption(option)
  index = 0

  if readFromJsonFile(user_data) and stillAddUsers:
    index = len(user_data)
    with open('users.json', 'ab+') as usersFile:
      while (stillAddUsers):
        print 'Add another user andd his password...'
        user = raw_input('user: ')
        password = raw_input('password: ')
        writeToJsonFile(usersFile, user_data, user, password, index)
        index += 1
        option = raw_input('continue?[y/n]: ')
        stillAddUsers = returnOption(option)

  return index == 0 # user file still empty

def checkData(data):
  if 'user' in data:
    if data['user'] is None:
      return False
  else: 
    return False

  if 'key' in data:
    if data['key'] is None:
      return False
  else:
    return False

  if 'password' in data:
    if data['password'] is None:
      return False
  else:
    return False

  return True

def findUserData(users_data, user, password):
  userFound = False
  passwordFound = False
  for entry in users_data.values():
    for key, value in entry.items():
      if key == 'user' and value == user:
        userFound = True  
      if key == 'password' and value == password:
        passwordFound = True
  
  return userFound and passwordFound

def recvData(c, size):
  rawData = c.recv(size) 
  return pickle.loads(rawData) 

def sendData(c, data):
  c.send(pickle.dumps(data))
  
def resolveJobForClient(c, users_data):
  data = recvData(c, 1024)
  print 'Received: ' + repr(data)

  if not checkData(data): # invalid data received
    c.close()
    return
  
  ciphertext = "0000000000000000000000000000000000000000000000000000000000000000"
  iv = ciphertext[:16]
  chypher = AES.new(data['key'], AES.MODE_CFB, iv)
  password = chypher.decrypt(data['password'])
  
  if findUserData(users_data, data['user'], password):
    print 'User found!'
    sendData(c, False)
    c.close()  
  else:
    print 'User not found!'
    sendData(c, True)
    tryAgain = recvData(c, 1024)
    if tryAgain:
      resolveJobForClient(c, users_data) 

def printUsers(users_data):
  for key, value in users_data.items():
    print key
    print value 
       
def runServer(): 
  users_data = {}
  addMoreUsers(users_data)
  printUsers(users_data)
  
  # start the server
  s = socket.socket()         
  host = socket.gethostname() 
  port = 13333
  s.bind((host, port))        

  s.listen(5)                 
  while True:
     c, addr = s.accept()     
     print 'New user connected: ' + repr(addr)
     thread = Thread(target = resolveJobForClient, args=(c, users_data))
     thread.start()

if __name__ == '__main__':
  runServer()
                  
