from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
from urllib import parse
from public import config

try:
    with open(config.RSA_PRIKEY_FILE_PATH, "rb") as file:
        privkey_b = file.read()
    privkey = RSA.importKey(privkey_b)
    cipher_rsa = PKCS1_v1_5.new(privkey)
except Exception as e:
    print(e)


def encrypt(context):
    return cipher_rsa.encrypt(context.encode('utf8')).decode('utf8')


def decrypt(context):
    context = parse.unquote(context)
    context = base64.b64decode(context)
    decontext = cipher_rsa.decrypt(context, None)
    if decontext is None:
        return None
    return decontext
