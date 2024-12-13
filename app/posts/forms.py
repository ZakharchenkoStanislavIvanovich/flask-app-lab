from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

# Список категорій
CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])

    is_active = BooleanField("Active Post")

    publish_date = DateField("Publish Date", format='%Y-%m-%d', validators=[DataRequired()]) 
    category = SelectField("Category", choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField("Add Post")
