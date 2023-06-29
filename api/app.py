

# Imports for SMTP

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

 
# Imports for Flask
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import os,io


app = Flask(__name__)
cors = CORS(app)

FILE_NAME='image.jpeg'

@app.route('/', methods=['GET'])
def  home():
    return "Hello WOrld"    


@app.route('/test', methods=['POST','GET'])
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
        name=args.get('name')
        email=args.get('email')
        print('sending ',name,' to ',email)
        if name is None:
            return "Name is not provided"
        if email is None:
            return "Email is not provided"
        
        bytesOfImage = request.get_data()
        imageStream = io.BytesIO(bytesOfImage)

        # print('bytesOfImage',type(bytesOfImage),'imageStream',type(imageStream))

        response    = send_email(name,email,imageStream)
        if response:
            return "Email Sent"
        else:
            return "Email Failed"

@app.route('/send',methods=['GET'])
def send():
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, FILE_NAME),'rb') as binary_pdf:
        bytesOfImage=binary_pdf.read()
        return Response(bytesOfImage, mimetype='image/jpeg')

    




def send_email(receiver_name,receiver_email,binary_img):
    body = f'''
    Hello, {receiver_name}
    Welcome to SJCE 
    Yours Friendly
    Prakash Annanin Vizhudhugal
    '''
    # put your email here
    sender = 'yuvibro1211@gmail.com'
    password = 'tiecqtzjasbhectc'
    # put the email of the receiver here
    try:
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver_email
        message['Subject'] = 'This email has an attacment, a pdf file'
        print('attaching body to email')
        message.attach(MIMEText(body, 'plain'))

        payload = MIMEBase('application', 'octate-stream', Name=FILE_NAME)
        # payload = MIMEBase('application', 'pdf', Name=pdfname)
        payload.set_payload((binary_img).read())

        # enconding the binary into base64
        encoders.encode_base64(payload)

        # add header with file name
        print('attaching image to email')
        payload.add_header('Content-Decomposition', 'attachment', filename=FILE_NAME)
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
