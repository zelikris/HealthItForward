from binascii import hexlify, unhexlify

import hashlib
import hmac
import os


def gen(password, salt=os.urandom(32), digestalgo='sha256', iters=131072, keylen=32):
    """Generate a PBKDF2 hash.

    Keyword arguments:
    password -- the password to hash
    salt -- the salt (default 32 random bytes)
    digestalgo -- the digest algorithm to use (default 'sha256')
    iters -- the number of PBKDF2 iterations (default 131072)
    keylen -- the length of the resulting hash in bytes (default 32)
    """
    password = password.encode('utf-8')
    digest = hashlib.pbkdf2_hmac(digestalgo, password, salt, iters, keylen)
    return 'pbkdf2${0}${1}${2}${3}'.format(digestalgo, iters,
                                           hexlify(salt).decode('utf-8'),
                                           hexlify(digest).decode('utf-8'))


def verify(password, password_hash):
    """Verify a PBKDF2 hash.
    This function is constant-time, regardless of the validity of the password.

    Keyword arguments:
    password -- the password to verify
    password_hash -- previously computed hash generated by gen
    """
    parts = password_hash.split('$')
    return hmac.compare_digest(password_hash, gen(password,
                                                  unhexlify(parts[3]),
                                                  parts[1],
                                                  int(parts[2]),
                                                  len(unhexlify(parts[4]))))


def fake_digest():
    """Return a fake digest.
    This fake digest will always fail verification when verified with verify.
    This is useful in cases where no password hash is available to pass to
    verify, but one must be tested anyway to avoid timing attacks.
    """
    return '=fake=$sha256$131072$00000000000000000000000000000000000000000000' \
           '00000000000000000000$00000000000000000000000000000000000000000000' \
           '00000000000000000000'
