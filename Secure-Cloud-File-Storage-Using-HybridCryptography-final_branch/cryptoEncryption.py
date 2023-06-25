import os
from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
import genFunc as gen
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def encrypt_fernet(data_to_encrypt, key_to_encrypt_with):
    fernet_encrypt = Fernet(key_to_encrypt_with)
    file_obj = open("data_storage/fileStore.enc", "wb")
    encrypted_data = fernet_encrypt.encrypt(data_to_encrypt)
    file_obj.write(encrypted_data)
    file_obj.close()


def encrypt_multi_fernet(file_to_encrypt, key1_to_encrypt_with, key2_to_encrypt_with):
    multi_fernet_encrypt = MultiFernet([Fernet(key1_to_encrypt_with), Fernet(key2_to_encrypt_with)])
    src_filename = 'files/' + file_to_encrypt
    trgt_filename = 'encrypted/' + file_to_encrypt
    file_obj = open(src_filename, 'rb')
    write_file_obj = open(trgt_filename, 'wb')
    raw = ""
    for line in file_obj:
        raw = raw + line
    encrypted_data = multi_fernet_encrypt.encrypt(raw)
    write_file_obj.write(encrypted_data)
    file_obj.close()
    write_file_obj.close()


def chacha20_encryption(file_to_encrypt, key_to_encrypt_with, random_str):
    aad = "authenticated but unencrypted data"
    chacha_encrypt = ChaCha20Poly1305(key_to_encrypt_with)
    src_filename = 'files/' + file_to_encrypt
    trgt_filename = 'encrypted/' + file_to_encrypt
    file_obj = open(src_filename, 'rb')
    write_file_obj = open(trgt_filename, 'wb')
    raw = ""
    for line in file_obj:
        raw = raw + line
    encrypted_data = chacha_encrypt.encrypt(random_str, raw, aad)
    write_file_obj.write(encrypted_data)
    file_obj.close()
    write_file_obj.close()


def aesgcm_encryption(file_to_encrypt, key_to_encrypt_with, random_str):
    aad = "authenticated but unencrypted data"
    aesgcm_encrypt = AESGCM(key_to_encrypt_with)
    src_filename = 'files/' + file_to_encrypt
    trgt_filename = 'encrypted/' + file_to_encrypt
    file_obj = open(src_filename, 'rb')
    write_file_obj = open(trgt_filename, 'wb')
    raw = ""
    for line in file_obj:
        raw = raw + line
    encrypted_data = aesgcm_encrypt.encrypt(random_str, raw, aad)
    write_file_obj.write(encrypted_data)
    file_obj.close()
    write_file_obj.close()


def aesccm_encryption(file_to_encrypt, key_to_encrypt_with, random_str):
    aad = "authenticated but unencrypted data"
    aesccm_encrypt = AESCCM(key_to_encrypt_with)
    src_filename = 'files/' + file_to_encrypt
    trgt_filename = 'encrypted/' + file_to_encrypt
    file_obj = open(src_filename, 'rb')
    write_file_obj = open(trgt_filename, 'wb')
    raw = ""
    for line in file_obj:
        raw = raw + line
    encrypted_data = aesccm_encrypt.encrypt(random_str, raw, aad)
    write_file_obj.write(encrypted_data)
    file_obj.close()
    write_file_obj.close()


def encrypter():
    gen.empFolder('secret_key')
    gen.empFolder('encrypted')
    pblc_key = Fernet.generate_key()
    multi_fernet_key_1 = Fernet.generate_key()
    multi_fernet_key_2 = Fernet.generate_key()
    chacha20_key = ChaCha20Poly1305.generate_key()
    aesgcm_key = AESGCM.generate_key(bit_length=128)
    aesccm_key = AESCCM.generate_key(bit_length=128)
    random_str1 = os.urandom(13)
    random_str2 = os.urandom(12)
    sorted_files = sorted(os.listdir('files'))
    for file_indx in range(0, len(sorted_files)):
        if file_indx % 4 == 0:
            encrypt_multi_fernet(sorted_files[file_indx], multi_fernet_key_1, multi_fernet_key_2)
        elif file_indx % 4 == 1:
            chacha20_encryption(sorted_files[file_indx], chacha20_key, random_str2)
        elif file_indx % 4 == 2:
            aesgcm_encryption(sorted_files[file_indx], aesgcm_key, random_str2)
        else:
            aesccm_encryption(sorted_files[file_indx], aesccm_key, random_str1)

    secret = (multi_fernet_key_1) + ":::::" + (multi_fernet_key_2) + ":::::" + (chacha20_key) + ":::::" + (
        aesgcm_key) + ":::::" + (aesccm_key) + ":::::" + (random_str2) + ":::::" + (random_str1)
    encrypt_fernet(secret, pblc_key)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    readable_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    encrypted_key_1 = public_key.encrypt(
        pblc_key.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return_key = open("./secret_key/keyfile.pem", "wb")
    return_key.write(pblc_key)
    return_key.close()
    gen.empFolder('files')
    print("\\n".join(readable_private_key.split("\n")))
    return readable_private_key
