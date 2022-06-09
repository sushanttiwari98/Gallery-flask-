from posixpath import join
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import os
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey"
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg', '.gif']
app.config['UPLOAD_FOLDER'] = "static/Uploaded_files"

class Upload(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route("/", methods = ['GET', 'POST'])
@app.route("/home", methods = ['GET', 'POST'])
def home():
    form = Upload()
    if(form.validate_on_submit()):
        file = form.file.data    #First grab the file
        #Then save the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        flash("File has been uploaded.")
    return render_template('index.html', form=form)


@app.route('/templates/<filename>', methods = ['GET', 'POST'])
def display_image(filename):
    images = os.listdir('static/uploaded_files')
    images = ['uploaded_files/' + file for file in images]
    return render_template('pictures.html', images = images)


    #return redirect(url_for('static', filename='Uploaded_files/' + filename))
    #return render_template('pictures.html', filename = filename)

if __name__ == "__main__":
    app.run(debug=True, port=8000)