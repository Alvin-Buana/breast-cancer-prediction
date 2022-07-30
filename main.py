from unittest import result
from flask import Flask, redirect, render_template, request, send_from_directory,url_for
from flask_wtf import FlaskForm
from wtforms import  SubmitField,FileField
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import os
import glcm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'data'

class UploadFile(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Submit')


@app .route('/', methods=['GET', 'POST'])
def uploadfile():
    form = UploadFile()
    form2 = UploadFile()
    if form.validate_on_submit():
        file = form.file.data
        file_test = form2.file.data
        filename = secure_filename(file.filename)
        filename_test = secure_filename(file_test.filename)
        if filename[-3:] not in ['zip']:
            return 'File must be a zip file'
        else:
            with ZipFile(file, 'r') as zip:
                zip.extractall(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']))
            print(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']))
            glcm.create_dataset(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],'train'))

        if filename_test[-3:] not in ['zip']:
            return 'File must be a zip file'
        else:
            with ZipFile(file_test, 'r') as zip:
                zip.extractall(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']))
            print(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']))
            
        return redirect(url_for("predict"))
    return render_template('index.html', form=form)
@app.route('/predict')
def predict():
    result = glcm.evaluate(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],'valid'))
    form = UploadFile()
    if form.validate_on_submit():
        file = form.file.data
        file_test = form.file.data
        filename = secure_filename(file.filename)
        filename_test = secure_filename(file_test.filename)
    return render_template('predict.html',result = result)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host=)

