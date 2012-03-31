#*-*coding: utf-8*-*
__author__='Xsoda'

from hashlib import md5, sha256
import string
import random

char_set = '8Ml*?!Yz(#:QSy{$|CbcaE,I>Fxi74j.Tu2h3`/v0-n+=o9;<B_HGf\\[)5D~P}s\'A@6OkmK%rpeVU^"&L1]JZdXWNtqgwR'

md5_email = lambda x: md5(x.encode(encoding='ascii').lower()).hexdigest() # md5加密，用于 Gravatar 的头像服务。

md5 = lambda x: md5(x.encode(encoding='ascii')).hexdigest() # md5 加密

sha256 = lambda x: sha256(x.encode()).hexdigest()

def salt_generator(size=24, chars=string.punctuation + string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def _encrypt_pwd(password, salt):
    pwd = ''
    for i in password:
        pwd += char_set[ord(x)%len(char_set)]
    return sha256(pwd + salt[-(len(salt) - len(pwd)):])

def encrypt(password):
    salt = salt_generator()
    if len(password) >=6 and len(password) <= 16:
        return _encrypt_pwd(password, salt), salt
    return 'error', salt

def check_password(pwd, enc_pwd, salt):
    return enc_pwd == _encrypt_pwd(pwd, salt)
