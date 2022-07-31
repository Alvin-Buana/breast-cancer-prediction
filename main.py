from unittest import result
from flask import Flask, redirect, render_template, request, send_from_directory,url_for
from flask_wtf import FlaskForm
from numpy import result_type
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
    
    if form.validate_on_submit():
        file = form.file.data
        
        filename = secure_filename(file.filename)
        
        if filename[-3:] not in ['zip']:
            return 'File must be a zip file'
        else:
            with ZipFile(file, 'r') as zip:
                zip.extractall(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']))
            print(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']))
            glcm.create_dataset(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],'train'))

        
            
        return redirect(url_for("output"))
    return render_template('index.html', form=form)
@app.route('/predict', methods=['GET', 'POST'])
def predict():
   
    form = UploadFile()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        if filename[-3:] not in ['png','jpg','jpeg']:
            return 'File must be an image file'
        else:
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),'static',filename))
            x, pred = glcm.svm_predict(os.path.join(os.path.abspath(os.path.dirname(__file__)),'static',filename))
            return render_template('predict.html', pred=pred, x=x,form=form,img = filename)
    return render_template('predict.html',form=form)
@app.route('/output')
def output():
    return render_template('output.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    form = UploadFile()
    if form.validate_on_submit():
        print("test")
        file_test = form.file.data
        filename_test = secure_filename(file_test.filename)
        if filename_test[-3:] not in ['zip']:
            return 'File must be a zip file'
        else:
            with ZipFile(file_test, 'r') as zip:
                zip.extractall(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']))
            print(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']))
            result = glcm.evaluate(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],'test'))
            print(result)
            return render_template('test.html', result=result,form=form)
    return render_template('test.html',form=form)



if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host=)

