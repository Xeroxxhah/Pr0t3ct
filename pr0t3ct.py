from cryptography import fernet
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import hashlib
import getpass
import os
from art import *

salt = b'K\x8d\xb9\x86\xf7\x11\\\x14\xe8\x84\x16l\x8d+X\xe3'

kdf = PBKDF2HMAC(
     algorithm=hashes.SHA256(),
     length=32,
     salt=salt,
     iterations=100000,
 )





def keygen(password):
     return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt(filedata,key,output_name,extention):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(filedata)
    efile = open('Output/'+output_name+'.'+extention+'.pr0t3ct','wb')
    efile.write(encrypted)
    efile.close()
    print(f"File encrypted sucessfully as {output_name+'.'+extention+'.pr0t3ct'} in Output")


def decrypt(filedata,key,output_name,extention):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(filedata)
    efile = open('Output/'+output_name+'.pr0t3ct'+'.'+extention,'wb')
    efile.write(decrypted)
    efile.close()
    print(f"File decrypted sucessfully as {output_name+'.'+extention+'.pr0t3ct'} in Output")


def file_handler(file_path,key,output_name):
    if os.path.exists(file_path) and not file_path.endswith('.pr0t3ct'):
        filex = file_path.split('.')
        try:
            extention = filex[1]
        except IndexError:
            extention = ''
        file = open(file_path,'rb')
        filedata = file.read()
        file.close()
        encrypt(filedata,key,output_name,extention)
    elif os.path.exists(file_path) and file_path.endswith('.pr0t3ct'):
        filex = file_path.split('.')
        try:
            extention = filex[1]
        except IndexError:
            extention=''
        file = open(file_path,'rb')
        filedata = file.read()
        file.close()
        decrypt(filedata,key,output_name,extention)
    else:
        print('File does not exist.')
        quit()


def hashpass(password):
    return hashlib.sha512(password.encode()).hexdigest()


def signup():
    username = input('Enter username: ')
    password = getpass.getpass()
    hashedpass = hashpass(password)
    try:
        os.mkdir('dep/'+username)
        pfile = open('dep/'+username+'/'+'shadow','w')
        pfile.write(hashedpass)
        print('Profile created sucessfully')
    except FileExistsError:
        print('user already exists')


def signin():
    username = input('Enter username: ')
    password = getpass.getpass()
    hashedpass = hashpass(password)
    key = keygen(password.encode())
    if os.path.exists('dep/'+username):
        hashfile = open('dep/'+username+'/shadow','rb')
        stored_hash = hashfile.read()
        hashfile.close()
        if str(hashedpass) != str(stored_hash.decode()):
            print('access denied')
            quit()
        else:
            menu(key=key,username=username)
    else:
        print('user does not exist\nSignup first')
        quit()

def menu(key,username):
    print('*'*50)
    print(f'Welcome :: {username}')
    print('*'*50)
    print('1:Encrypt File')
    print('2:Decrypt File')
    print('3:Exit')
    option = input('Selcet your option: ')
    if option == '1':
        filepath = input('Enter path of file: ')
        filename = input('Enter output file name: ')
        file_handler(filepath,key,filename)
    elif option == '2':
        filepath = input('Enter path of file: ')
        filename = input('Enter output file name: ')
        file_handler(filepath,key,filename)
    elif option == '3':
        quit()
    else:
        print('Wrong option')
        quit()
    

tprint("Pr0t3ct","random")
print('1:Signup\n2:Signin\n3:exit')
option = input('Choose your option: ')
if option == '1':
    signup()
elif option == '2':
    signin()
elif option == '3':
    quit()
else:
    print('Wrong option')
    quit()


