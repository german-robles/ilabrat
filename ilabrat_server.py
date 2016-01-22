#!/usr/bin/python
# -*- coding: utf-8 *-*
from flask import Flask, request
from encrypt import Encrypter
from logging.handlers import RotatingFileHandler
import logging
import ssl
import glob, os
from flask import Flask, request, redirect, url_for, send_from_directory, send_file
from werkzeug import secure_filename
import io
from flask import g

# Initialize the Flask application
encrypter = Encrypter()
(home, passphrase, emailKey, bind, port, debug, sslcrt, sslkey, accesslog, logfile,
 upload_folder) = encrypter.getConfig()

app = Flask(__name__, static_url_path='%s' % (upload_folder))
UPLOAD_FOLDER = '%s' % (upload_folder)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'sql', 'gz', 'gpg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'sql', 'gz', 'gpg'])


@app.route('/encrypt', methods=['POST'])
def api_encrypt_data():
    data = request.data
    response = encrypter.encrypt(home, emailKey, data)
    return response


@app.route('/decrypt', methods=['POST'])
def api_decrypt_data():
    data = request.data
    response = encrypter.decrypt(home, passphrase, data)
    return response


def allowed_file(filename):
    # this has changed from the original example because the original did not work for me
    return filename[-3:].lower() in ALLOWED_EXTENSIONS


def after_this_request(func):
    if not hasattr(g, 'call_after_request'):
        g.call_after_request = []
    g.call_after_request.append(func)
    return func


@app.after_request
def per_request_callbacks(response):
    for func in getattr(g, 'call_after_request', ()):
        response = func(response)
    return response


@app.route('/fileEncrypt', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print '**found file', file.filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            encrypter.encrypt_file(home, emailKey, filename, upload_folder)
            encrypted_file = '%s/%s.gpg' % (upload_folder, filename)

            # return send_file(io.BytesIO(encrypted_file))

            @after_this_request
            def delete_uploaded_files(response):
                filelist = glob.glob('%s/*' % (upload_folder))
                for f in filelist:
                    os.remove(f)
                return response

            return send_file(encrypted_file)

@app.route('/fileDecrypt', methods=['GET', 'POST'])
def decrypt_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print '**found file', file.filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            encrypter.decrypt_file(home, filename, upload_folder, passphrase)
            filenamed = filename.replace('.gpg', '')
            decrypted_file = '%s/%s' % (upload_folder, filenamed)

            @after_this_request
            def delete_uploaded_files(response):
                filelist = glob.glob('%s/*' % (upload_folder))
                for f in filelist:
                    os.remove(f)
                return response

            return send_file(decrypted_file)


if __name__ == '__main__':
    handler = RotatingFileHandler(logfile, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    logger = logging.getLogger('werkzeug')
    handler = logging.FileHandler(accesslog)
    logger.addHandler(handler)
    app.logger.addHandler(handler)

    app.run(host=bind, port=port, debug=debug, ssl_context=(sslcrt, sslkey, ssl.PROTOCOL_TLSv1))
