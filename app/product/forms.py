from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField,DecimalField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
    Optional,
    NumberRange,
)

class ProductForm(FlaskForm):
    name = StringField("ProductName:", validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField("category:",choices=[("Food", "Food"), ("Pills", "Pills"), ("Clothes", "Clothes"), ("Other", "Other")],validators=[DataRequired()],)
    image = FileField('Product Image',validators=[DataRequired()])
    submit = SubmitField('Add Product')

# update product form
class Update_ProductForm(FlaskForm):
    name = StringField("ProductName:", validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField("category:",choices=[("Food", "Food"), ("Pills", "Pills"), ("Clothes", "Clothes"), ("Other", "Other")],validators=[DataRequired()],)
    image = FileField('Product Image')
    submit = SubmitField('Update Product')
