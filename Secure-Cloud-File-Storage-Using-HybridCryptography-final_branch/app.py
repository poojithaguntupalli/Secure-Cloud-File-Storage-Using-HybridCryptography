import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file, flash
import cryptoEncryption as enc
import cryptoDecryption as dec
import upload as up
import delete as dl
import genFunc as gen

UPLOAD_FOLDER = './uploads/'
UPLOAD_KEY = './secret_key/'
ALLOWED_EXTENSIONS = set(['pem'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_KEY'] = UPLOAD_KEY


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def start_encryption():
    gen.filesDivide()
    gen.empFolder('uploads')
    private_key = enc.encrypter()
    up.uploadfileToCloud(access_key, secret_key, bucket_name)
    return render_template('downloadKeyPage.html', key = private_key)


def start_decryption(pvtKey):
    dec.decrypter(pvtKey, access_key, secret_key, bucket_name)
    gen.empFolder('secret_key')
    gen.restoreFiles()
    dl.deleteobjects(access_key, secret_key, bucket_name)
    return render_template('filesDownloadPage.html')


@app.route('/return-key/My_Key.pem')
def return_key():
    list_directory = os.listdir('secret_key')
    filename = './secret_key/' + list_directory[0]
    return send_file(filename, attachment_filename='My_Key.pem')


@app.route('/return-file/')
def return_file():
    list_directory = os.listdir('restored_file')
    filename = './restored_file/' + list_directory[0]
    print("Restored file")
    print(list_directory[0])
    return send_file(filename, attachment_filename=list_directory[0], as_attachment=True)


@app.route('/download/')
def downloads():
    return render_template('getKeyPage.html')


@app.route('/upload')
def call_page_upload():
    return render_template('uploadPage.html')


@app.route('/home')
def back_home():
    gen.empFolder('secret_key')
    gen.empFolder('restored_file')
    return render_template('homePage.html')


@app.route('/')
def index():
    return render_template('homePage.html')


@app.route('/data', methods=['GET', 'POST'])
def upload_file():
    gen.empFolder('uploads')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash(gen.NO_PART)
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash(gen.NO_FILE)
            return gen.NO_FILE
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return start_encryption()
        return gen.INVALID_FILE


@app.route('/download_data', methods=['GET', 'POST'])
def upload_key():
    private_key = request.form.get("pvtKey")
    gen.empFolder('secret_key')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash(gen.NO_PART)
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash(gen.NO_FILE)
            return gen.NO_FILE
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_KEY'], file.filename))
            return start_decryption(private_key)
        return gen.INVALID_FILE


if __name__ == '__main__':
    access_key = input("Enter aws access key")
    secret_key = input("Enter aws secret key")
    bucket_name = input("Enter bucket name")

    app.run(host='127.0.0.1', port=8000, debug=True, use_reloader=False)
