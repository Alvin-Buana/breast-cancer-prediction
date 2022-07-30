from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import  SubmitField,FileField
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = './data'

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
            
            return 'file uploaded successfully'
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host=)

