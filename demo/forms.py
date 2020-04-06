from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField


class UploadForm(FlaskForm):
    image = FileField("Choose an image")
    predict = SubmitField("Predict")