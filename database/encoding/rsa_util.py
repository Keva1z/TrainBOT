# coding: utf-8

# use module pycryptodome
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import MD5, SHA, SHA1, SHA256, SHA384, SHA512
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Util import number


class RSAHelper(object):
    ALG_MAP = {
        "SHA-256": SHA256,
        "SHA256": SHA256,
        "SHA-512": SHA512,
        "SHA512": SHA512,
        "SHA-384": SHA384,
        "SHA384": SHA384,
        "SHA-1": SHA1,
        "SHA1": SHA1,
        "SHA": SHA,
        "MD5": MD5,
    }

    @classmethod
    def new_keys(cls, key_size):
        random_generator = Random.new().read
        key = RSA.generate(key_size, random_generator)
        return key, key.publickey()

    @classmethod
    def import_key(cls, external_key):
        if isinstance(external_key, RSA.RsaKey):
            return external_key
        return RSA.importKey(external_key)

    @classmethod
    def get_public_key(cls, private_key):
        private_key = cls.import_key(private_key)
        return private_key.publickey()

    @classmethod
    def encrypt(cls, message, public_key):
        public_key = cls.import_key(public_key)
        cipher = PKCS1_OAEP.new(public_key)

        # to calculate the max message size the cipher can handle
        # it can be of variable length, but not longer than the RSA modulus (in bytes)
        # minus 2, minus twice the hash output size.
        modBits = number.size(cipher._key.n)
        k = number.ceil_div(modBits, 8)
        hLen = cipher._hashObj.digest_size
        length = k - 2 * hLen - 3

        res = []
        for i in range(0, len(message), length):
            res.append(cipher.encrypt(message[i : i + length]))
        #print(type(res), type(res[0]))
        return b"".join(res)

    @classmethod
    def decrypt(cls, cipher_text, private_key):
        private_key = cls.import_key(private_key)
        cipher = PKCS1_OAEP.new(private_key)

        length = private_key.size_in_bytes()
        res = []
        for i in range(0, len(cipher_text), length):
            decrypted_block = cipher.decrypt(cipher_text[i : i + length])
            res.append(decrypted_block)
        return b"".join(res)

    @classmethod
    def sign(cls, message, private_key, hash_alg="SHA-256"):
        private_key = cls.import_key(private_key)
        hash_alg = hash_alg.upper()
        if hash_alg not in cls.ALG_MAP:
            alg = cls.ALG_MAP["MD5"]
        else:
            alg = cls.ALG_MAP[hash_alg]

        signer = PKCS1_v1_5.new(private_key)
        digest = alg.new()
        digest.update(message)

        return signer.sign(digest)

    @classmethod
    def verify(cls, message, signature, public_key, hash_alg="SHA-256"):
        public_key = cls.import_key(public_key)
        hash_alg = hash_alg.upper()
        if hash_alg not in cls.ALG_MAP:
            alg = cls.ALG_MAP["MD5"]
        else:
            alg = cls.ALG_MAP[hash_alg]
        digest = alg.new()
        digest.update(message)
        signer = PKCS1_v1_5.new(public_key)
        signer.verify(digest, signature)


def main():
    from base64 import b64decode, b64encode

    msg1 = "Stay hungry," * 100
    msg2 = "Stay foolish." * 100

    msg1 = msg1.encode()
    msg2 = msg2.encode()

    key_size = 1024

    private_key, public_key = RSAHelper.new_keys(key_size)
    encrypted = b64encode(RSAHelper.encrypt(msg1, public_key))
    decrypted = RSAHelper.decrypt(b64decode(encrypted), private_key)

    print("------ encrypt and decrypt ------")
    print("msg1: %s" % msg1)
    print("encrypted: %s" % encrypted)
    print("decrypted: %s\n" % decrypted)

    print("------ sign and verify ------")
    signature = b64encode(RSAHelper.sign(msg2, private_key))
    print("msg2: %s" % msg2)
    print("signature: %s " % signature)
    RSAHelper.verify(msg2, b64decode(signature), public_key)
    print("verified!")


if __name__ == "__main__":
    main()
