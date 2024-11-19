from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, IntegerField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class FormProduct(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    description = CKEditorField("description", validators=[DataRequired()])
    price = IntegerField("price", validators=[DataRequired()])
    amount = IntegerField("amount", validators=[DataRequired()])
    location = StringField("location", validators=[DataRequired()])
    category = SelectField("category", choices=[], validators=[DataRequired()])
    image = FileField("image", validators=[FileRequired()])
    submit = SubmitField("submit")

class FormProductForEdit(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    description = CKEditorField("description", validators=[DataRequired()])
    price = IntegerField("price", validators=[DataRequired()])
    amount = IntegerField("amount", validators=[DataRequired()])
    location = StringField("location", validators=[DataRequired()])
    category = SelectField("category", choices=[], validators=[DataRequired()])
    image = FileField("image")
    submit = SubmitField("submit")

class InputCategory(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    submit = SubmitField("submit")

class DeleteCategoryForm(FlaskForm):
    name = SelectField("name", validators=[DataRequired()])
    submit = SubmitField("submit")
