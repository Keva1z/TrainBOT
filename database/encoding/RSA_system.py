import os
import pickle
from database.encoding.rsa_util import RSAHelper
from Crypto.PublicKey import RSA
from dotenv import load_dotenv
RSA_Helper = RSAHelper()

load_dotenv("misc/.env")

KEYS_FOLDER = os.getenv('KEYS_FOLDER')
RSA_Helper = RSAHelper()

def generate_keys() -> str:
    
    # генерация ключей
    key = RSA.generate(2048)

    # создание папки, если ее нет
    if not os.path.exists(KEYS_FOLDER):
        os.makedirs(KEYS_FOLDER)

    # сохранение ключей
    if not os.path.exists(KEYS_FOLDER + '/private_key.pem') or not os.path.exists(KEYS_FOLDER + '/public_key.pem'):
        with open(os.path.join(KEYS_FOLDER, 'private_key.pem'), 'wb') as f:
            f.write(key.export_key())
        with open(os.path.join(KEYS_FOLDER, 'public_key.pem'), 'wb') as f:
            f.write(key.publickey().export_key())
        return "Keys created!"
    else:
        return "Keys already exist!"

async def load_keys(TYPE = None):
    # загрузка ключей
    with open(os.path.join(KEYS_FOLDER, 'private_key.pem'), 'rb') as f:
        private_key = RSA.import_key(f.read())
    with open(os.path.join(KEYS_FOLDER, 'public_key.pem'), 'rb') as f:
        public_key = RSA.import_key(f.read())

    if TYPE == 'Public':
        return public_key
    elif TYPE == 'Private':
        return private_key
    else:
        return private_key, public_key

async def encrypt(data):
    pickled_data = pickle.dumps(data)

    encrypted_data = RSA_Helper.encrypt(pickled_data, await load_keys('Public'))

    return encrypted_data

async def decrypt(data):
    decrypted_data = pickle.loads(RSA_Helper.decrypt(data, await load_keys('Private')))

    return decrypted_data

generate_keys()
