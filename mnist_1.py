
import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image

import numpy as np


classes = ["0","1","2","3","4","5","6","7","8","9"]
image_size = 28

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = load_model('./model.h5', compile=False)#�w�K�ς݃��f�������[�h


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('�t�@�C��������܂���')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('�t�@�C��������܂���')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            #�󂯎�����摜��ǂݍ��݁Anp�`���ɕϊ�
            img = image.load_img(filepath, grayscale=True, target_size=(image_size,image_size))
            img = image.img_to_array(img)
            data = np.array([img])
            #�ϊ������f�[�^�����f���ɓn���ė\������
            result = model.predict(data)[0]
            predicted = result.argmax()
            pred_answer = "����� " + classes[predicted] + " �ł�"

            return render_template("index.html",answer=pred_answer)

    return render_template("index.html",answer="")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)