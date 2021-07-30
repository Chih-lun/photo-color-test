from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import NumberRange
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
import colorgram
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ae39sGR5Z4bzASaYKk7zC294wTD7rK5e'
Bootstrap(app)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'

class Color():
    def __init__(self,color,percentage):
        self.color = color
        self.percentage = percentage

class RecieveForm(FlaskForm):
    photo = FileField(label="File to upload:", validators=[FileAllowed(['jpg','jpeg','png'])])
    number = IntegerField(label='Number of Color:', validators=[NumberRange(min=1,max=99)])
    run = SubmitField(label='Run')

@app.route('/',methods=['GET','POST'])
def home():
    form = RecieveForm()
    url = 'static/uploads/demo.jpg'
    num = 10
    result = []
    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename)
        full_fillename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(full_fillename)
        url = full_fillename
        num = form.number.data
    colors = colorgram.extract(url,num)
    for i in colors:
        new_color = Color(color=f"rgb{(i.rgb.r,i.rgb.g,i.rgb.b)}",percentage=f"{'{:.2f}'.format(i.proportion * 100)}%")
        result.append(new_color)
    return render_template('index.html',url=url,result=result,form=form)

if __name__ == '__main__':
    app.run(threaded=True)