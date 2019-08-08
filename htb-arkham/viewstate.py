import hmac
import base64
from Crypto.Cipher import DES
from hashlib import sha1

def pad(s):
        return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)

block_size = DES.block_size
key = "JsF9876-"

viewstate = "wHo0wmLu5ceItIi+I7XkEi1GAb4h12WZ894pA+Z4OH7bco2jXEy1RQxTqLYuokmO70KtDtngjDm0mNzA9qHjYerxo0jW7zu1mdKBXtxnT1RmnWUWTJyCuNcJuxE="
viewstate = base64.b64decode(viewstate)

obj = DES.new(key, DES.MODE_ECB)
decrypted_viewstate = obj.decrypt(pad(viewstate))
print(decrypted_viewstate)
