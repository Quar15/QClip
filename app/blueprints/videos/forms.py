from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class VideoUploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)], render_kw={'placeholder': "Title"})
    file = FileField('Video', validators=[DataRequired()])
    submit = SubmitField('Upload')

    def __init__(self, *args, **kwargs):
        super(VideoUploadForm, self).__init__(*args, **kwargs)
        # Add FileAllowed validator dynamically now that we're in app context
        self.file.validators.append(FileAllowed(current_app.config['ALLOWED_EXTENSIONS']))
