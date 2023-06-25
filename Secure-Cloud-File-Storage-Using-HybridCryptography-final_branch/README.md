# Cloud file storage using Asymmetric Key Encryption
The project mainly focuses on storing the files securely in cloud by encrypting the files, and decrypting the files while cloning from cloud.
Secure File Storage in Cloud

Used: AWS, Python
# Working of the Application

## Storage Step
1. Spin up the server and provide the necessary AWS credentials of the account used for storage</br>
2. Choose the upload option and uploda a file</br>
3. The file is stored as smaller chunks of data each of which is encrypted </br>
4. The chunks of data are encrypted by one of four encryption algorithm that is chosen in a round-robn fashion</br>
5. These individual keys are concatenated together into one key and then further encrypted using an asymmetric private/public key pair </br>
6. This encrypted combination key is written into a file and is provided to the user once the files have been encrypted.</br>
7. Furthermore, the public kry from the asymmetric pair used to encrypt the combined is also displayed for the user to note down, to provide during the restore step along with the downloaded combination key pem file</br>
8. In the meantime, the system would have uploaded the chunks to the cloud.

## Restore Step</br>
1. Upload the public key and type in the private key in the restore page of the server</br>
2. The server then uses the private key to decrypt the public key provided and use it to separately decrypt each individual chunk </br>
3. Once decrypted, the chunks are pooled together to the original file </br>
4. The server cleans up the data from the server and provides the restored final file as a downloadable.</br>

# Deployment Steps

1. Install Requirements</br>
`pip install -r requirements.txt`</br>

2. Run the application</br>
`python app.py`</br>

3. Open server on browser</br>
