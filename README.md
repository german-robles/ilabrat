# Ilabrat

... Ilabrat in Assyrian, Babylonian and Akkadian mythology is the attendant and minister of state of the chief sky god Anu, and part of his entourage. (Wiki)...


Ilabrat is a web service that provides encryption for your texts and files, using gpg algorithm and python. The main goal of ilabrat it to get one place to encrypt your documents, so that you can forget  generate code on your apps to achieve this purpose.





### Version
1.0.0

### Tech

Ilabrat uses a number of open source projects to work properly:

* [Python Flask]
* [Python gnupg]
* [Python YAML]

### Installation

You need Python 2.7 , Python Flask, Python GNUPG, Python YAML installed:

```sh
$ sudo pip install flask
$ sudo pip install python-gnupg
$ sudo pip install pyyaml
```

```sh
$ git clone https://github.com/german-robles/ilabrat
```

You need to create your GPG key to encrypt and Decrypt inside ilabrat, if you are not familiar you may visit this page [GPGKEY] 


### Configuration File

Inside de ilabrat directory you will find a config file called ilabrat.conf you must fill it with your configuration

```yaml
home: '/home/user/.gnupg'
passphrase: 'your gpg passphrase'
emailKey: 'emailkey@emailkey.com'
sslkey: '/opt/ilabrat/ssl/ilabrat.key' #(Example of ilabrat path)
sslcrt: '/opt/ilabrat/ssl/ilabrat.crt' #(Example of ilabrat path)
accesslog: '/opt/ilabrat/log/ilabrat_access.log' #(Example of ilabrat path)
logfile: '/opt/ilabrat/log/ilabrat.log' #(Example of ilabrat path)
bind: '127.0.0.1'
port: 9000
debug: False
uploadFolder: '/home/user/ilabrat/uploads' #(Example of ilabrat path)
```

# Usage:

You have 4 services to use in ilabrat encrypt , decrypt, fileEncrypt, fileDecrypt :

##### To encrypt body:
Send your text in the body using POST to "https://ilabratserver:9000/encrypt" You will recieve a GPG sign as a response of your request.

##### To decrypt body:

Send your GPG sign in the body using POST to "https://ilabratserver:9000/decrypt" You will recieve decrypted text as a response of your request

##### To encrypt files:

Send your file in the body using POST to "https://ilabratserver:9000/fileEncrypt" You will recieve a GPG sign as a response of your request.

Python example:

```python
import requests

url = "https://ilabratServer:9000/fileEncrypt"
fin = open('yourfile.ext', 'rb')
files = {'file': fin}
try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url, files=files, verify=False, stream=True)
        with open('yourfile.ext.gpg', 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                                f.write(chunk)

finally:
                fin.close()
```


##### To decrypt files:

Send your GPG file signature in the body using POST to "https://ilabratserver:9000/fileDecrypt" You will recieve a file as a response of your request.
Python example:

```python
import requests

url = "https://ilabratServer:9000/fileDecrypt"
fin = open('yourfile.ext.gpg', 'rb')
files = {'file': fin}
try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url, files=files, verify=False, stream=True)
        with open('yourfile.ext', 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                                f.write(chunk)

finally:
                fin.close()
```



   [Python Flask]: <https://pypi.python.org/pypi/Flask>
   [Python gnupg]: <https://pypi.python.org/pypi/gnupg>
   [Python YAML]: <https://pypi.python.org/pypi/PyYAML>
   [GPGKEY]: <https://fedoraproject.org/wiki/Creating_GPG_Keys>