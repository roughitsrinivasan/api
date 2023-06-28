from flask import Flask, Response, request, jsonify
from io import BytesIO
import base64
from flask_cors import CORS, cross_origin
import os
import sys

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['GET'])
def  home():
    return "Hello WOrld"    


@app.route('/search', methods=['POST'])
def index():
    if request.method == 'POST':
        args = request.args
        print(args)
        return jsonify(args)
    else:
        return "Hello World"
@app.route("/image", methods=['GET', 'POST'])
def image():
    if(request.method == "POST"):
        args = request.args
        name=args['name']
        email=args['email']
        bytesOfImage = request.get_data()
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'image.jpeg'),'wb') as out:
            out.write(bytesOfImage)
        send_email('image.jpeg',name,email)
        return "Image read"


@app.route("/video", methods=['GET', 'POST'])
def video():
    if(request.method == "POST"):
        bytesOfVideo = request.get_data()
        with open('video.mp4', 'wb') as out:
            out.write(bytesOfVideo)
        return "Video read"
    
    


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email(pdfname,receiver_name,receiver_email):
    body = f'''
    Hello, {receiver_name}
    This is the body of the email
    sicerely yours
    G.G.
    '''
    # put your email here
    sender = 'yuvibro1211@gmail.com'
    # get the password in the gmail (manage your google account, click on the avatar on the right)
    # then go to security (right) and app password (center)
    # insert the password and then choose mail and this computer and then generate
    # copy the password generated here
    password = 'tiecqtzjasbhectc'
    # put the email of the receiver here
    try:
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver_email
        message['Subject'] = 'This email has an attacment, a pdf file'

        message.attach(MIMEText(body, 'plain'))



        # open the file in bynary
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'image.jpeg'),'rb') as binary_pdf:

            payload = MIMEBase('application', 'octate-stream', Name=pdfname)
            # payload = MIMEBase('application', 'pdf', Name=pdfname)
            payload.set_payload((binary_pdf).read())

            # enconding the binary into base64
            encoders.encode_base64(payload)

            # add header with pdf name
            payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
            message.attach(payload)

            #use gmail with port
            session = smtplib.SMTP('smtp.gmail.com', 587)

            #enable security
            session.starttls()

            #login with mail_id and password
            session.login(sender, password)

            text = message.as_string()
            session.sendmail(sender, receiver_email, text)
            session.quit()
            print('Mail Sent')
            return True
    except:
        print("Mail failed")
        return False
    
if __name__ == '__main__':
    app.run(host="localhost", port=5000,debug=True)
