from flask import Flask, Response, request, jsonify
from io import BytesIO
import base64
from flask_cors import CORS, cross_origin
import os
import sys

from send_email import send_email
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
        with open('image.jpeg', 'wb') as out:
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
    
    
if __name__ == '__main__':
    app.run(host="localhost", port=5000,debug=True)
