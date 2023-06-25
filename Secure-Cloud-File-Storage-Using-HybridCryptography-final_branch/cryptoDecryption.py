from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
import os
import boto3
import shutil
import genFunc as gen


def decrypt_fernet(k):
    if not os.path.exists("data_storage/fileStore.enc"):
        print("File not found")
        return ""

    with open("data_storage/fileStore.enc", "rb") as fi1:
        encrptData = fi1.read()

    p_fernet = Fernet(k)
    decrptData = p_fernet.decrypt(encrptData)
    return decrptData


def decrypt_multi_fernet(f1, k1, k2):
    srcPath = os.path.join("filesDownloadFromCloud", f1)
    trgtPath = os.path.join("files", f1)

    if not os.path.exists(srcPath):
        print("No file found")
        return

    with open(srcPath, "rb") as sf1, open(trgtPath, "wb") as tf2:
        encrptData = sf1.read()
        f = MultiFernet([Fernet(k1), Fernet(k2)])
        decrptData = f.decrypt(encrptData)
        tf2.write(decrptData)


def decrypt_chacha20poly(f1, k, n):
    srcPath = os.path.join("filesDownloadFromCloud", f1)
    trgtPath = os.path.join("files", f1)

    if not os.path.exists(srcPath):
        print("File not found")
        return

    with open(srcPath, "rb") as srcFile, open(trgtPath, "wb") as trgtFile:
        encrptData = srcFile.read()
        d = b"authenticated but unencrypted data"
        chacha = ChaCha20Poly1305(k)
        decrypted_data = chacha.decrypt(n, encrptData, d)
        trgtFile.write(decrypted_data)


def decrypt_aesgcm(f1, k, n):
    srcPath = os.path.join("filesDownloadFromCloud", f1)
    trgtPath = os.path.join("files", f1)

    if not os.path.exists(srcPath):
        print("File not found")
        return

    with open(srcPath, "rb") as src_file, open(trgtPath, "wb") as tgt_file:
        encrptData = src_file.read()
        g = b"authenticated but unencrypted data"
        aesfunc = AESGCM(k)
        decrptData = aesfunc.decrypt(n, encrptData, g)
        tgt_file.write(decrptData)


def decrypt_aesccm(f1, k, n):
    b = b"authenticated but unencrypted data"
    ccmfunc = AESCCM(k)
    source_filename = 'filesDownloadFromCloud/' + f1
    target_filename = 'files/' + f1
    with open(source_filename, 'rb') as fl:
        fr = fl.read()
    data = ccmfunc.decrypt(n, fr, b)
    with open(target_filename, 'wb') as tgtf1:
        tgtf1.write(data)


def decrypter(pvtKey, access_key, secret_key, bucket_name):
    gen.empFolder('files')

    # Read public key from file
    key1 = ""
    lstFolder = os.listdir('secret_key')
    f1 = './secret_key/' + lstFolder[0]
    with open(f1, "rb") as key:
        for row in key:
            key1 += row

    print('PRINTING INSIDE DECRYPTER')
    print(type(pvtKey))
    pvtKey = pvtKey.encode('ascii')
    print(pvtKey)
    # pvtKey = serialization.load_pem_private_key(pvtKey, password=None, backend=default_backend())
    print('NEXT STEP')

    # Decrypt the secret information from the public key
    # decrypted_key_1 = pvtKey.decrypt(
    #     key1,
    #     padding.OAEP(
    #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
    #         algorithm=hashes.SHA256(),
    #         label=None
    #     )
    # )

    decrptKey = decrypt_fernet(key1)
    keypart1, keypart2, keypart3, keypart4, keypart5, nonce, nonce1 = decrptKey.split(':::::')

    # Set up the S3 client with server-side encryption
    s3 = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4', s3={'use_accelerate_endpoint': True}),
                      region_name='us-east-1',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)

    # Set the path to the local directory to download the files
    local_directory_path = './filesDownloadFromCloud/'

    if os.path.exists(local_directory_path):
        shutil.rmtree(local_directory_path)
    os.makedirs(local_directory_path)

    # Retrieve a list of all the files in the S3 directory
    objects = s3.list_objects_v2(Bucket=bucket_name)

    # Download each file in the bucket to the local directory
    for obj in objects['Contents']:
        object_key = obj['Key']
        local_filename = local_directory_path + object_key
        s3.download_file(bucket_name, object_key, local_filename)

    files = os.listdir(local_directory_path)
    print(files)

    for j, file in enumerate(files):
        if j % 4 == 0:
            decrypt_multi_fernet(file, keypart1, keypart2)
        elif j % 4 == 1:
            decrypt_chacha20poly(file, keypart3, nonce)
        elif j % 4 == 2:
            decrypt_aesgcm(file, keypart4, nonce)
        else:
            decrypt_aesccm(file, keypart5, nonce1)
