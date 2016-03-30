from binascii import hexlify, unhexlify

import hashlib
import hmac
import os


def gen(password, salt=os.urandom(32), digestalgo='sha256', iters=131072, keylen=32):
    password = password.encode('utf-8')
    digest = hashlib.pbkdf2_hmac(digestalgo, password, salt, iters, keylen)
    return 'pbkdf2${0}${1}${2}${3}'.format(digestalgo, iters, hexlify(salt).decode('utf-8'),
                                           hexlify(digest).decode('utf-8'))


def verify(password, password_hash):
    parts = password_hash.split('$')
    return hmac.compare_digest(password_hash,
                               gen(password, unhexlify(parts[3]), parts[1], int(parts[2]), len(unhexlify(parts[4]))))


def fake_digest():
    return 'failed$sha256$4096$0000000000000000000000000000000000000000000000000000000000000000' \
           '$0000000000000000000000000000000000000000000000000000000000000000'
