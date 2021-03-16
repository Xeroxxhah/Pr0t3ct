from typing import Text
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


def clearscr():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")


def secure_del(file):
    try:
        delfile = open(file,'wb')
        delfile.write(os.urandom(delfile.tell()))
        delfile.close()
        os.unlink(file)
    except Exception as err:
        print(err)


def keygen(password):
     return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt(key,path):
    fernet = Fernet(key)
    file = open(path,'rb')
    filedata = file.read()
    file.close()
    encrypted = fernet.encrypt(filedata)
    output_file = path.replace(os.path.basename(path),os.path.basename(path)+'.pr0t3ct')
    efile = open(output_file,'wb')
    efile.write(encrypted)
    efile.close()
    print(f"File encrypted sucessfully as {output_file}")


def decrypt(key,path):
    fernet = Fernet(key)
    file = open(path,'rb')
    filedata = file.read()
    file.close()
    decrypted = fernet.decrypt(filedata)
    output_file = path.replace(os.path.basename(path),os.path.basename(path).strip('.pr0t3ct'))
    efile = open(output_file,'wb')
    efile.write(decrypted)
    efile.close()
    print(f"File decrypted sucessfully as {output_file} ")


def file_handler(file_path,key):
    output_name = os.path.basename(file_path)
    if os.path.exists(file_path) and not file_path.endswith('.pr0t3ct'):
        encrypt(key,file_path)
    elif os.path.exists(file_path) and file_path.endswith('.pr0t3ct'):
        decrypt(key,file_path)
    else:
        print('File does not exist.')
        quit()


def hashpass(password):
    return hashlib.sha512(password.encode()).hexdigest()


def signup():
    username = input('Enter username: ')
    password = getpass.getpass(prompt="Enter Password: ")
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
    password = getpass.getpass(prompt="Enter Password: ")
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
    clearscr()
    print('*'*50)
    print('*'*50)
    print(f'Welcome :-: [{username}]')
    print('*'*50)
    print('*'*50)
    print('[1]-[Encrypt File]')
    print('[2]-[Decrypt File]')
    print('[3]-[Exit]')
    option = input('Selcet your option: ')
    clearscr()
    if option == '1':
        filepath = input('Enter path of file: ')
        op = input("Do you want to delete the orignal file? (y/n): ")
        if op.lower() == 'y':
            file_handler(filepath,key)
            secure_del(filepath)
        else:
            file_handler(filepath,key)
    elif option == '2':
        filepath = input('Enter path of file: ')
        op = input("Do you want to delete the encrypted file? (y/n): ")
        if op.lower() == 'y':
            file_handler(filepath,key)
            secure_del(filepath)
        else:
            file_handler(filepath,key)
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


