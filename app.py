from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange
from models import db, Person
import os

# Initialize the Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Path to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
app.config['SECRET_KEY'] = 'mysecretkey'  # Secret key for CSRF protection

# Initialize the database
db.init_app(app)

# WTForm for adding a new person
class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    vyska = FloatField('Vyska (m)', validators=[DataRequired(), NumberRange(min=0, max=2.99, message="Vyska must be a valid number up to 2.99")])
    vaha = FloatField('Vaha (kg)', validators=[DataRequired(), NumberRange(min=0, max=199, message="Vaha must be a valid number up to 199")])
    submit = SubmitField('Add Person')

# Create the tables and populate initial data if not already present
with app.app_context():
    db.create_all()
    if not Person.query.first():
        db.session.add_all([
            Person(name='Honza', vyska=1.65, vaha=80),
            Person(name='Dan', vyska=1.95, vaha=90),
            Person(name='Zuzka', vyska=1.55, vaha=45),
            Person(name='Josef', vyska=1.70, vaha=65),
            Person(name='Anicka', vyska=1.50, vaha=50)
        ])
        db.session.commit()

@app.route('/')
def index():
    persons = Person.query.all()
    return render_template('index.html', persons=persons)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PersonForm()
    if form.validate_on_submit():
        new_person = Person(name=form.name.data, vyska=form.vyska.data, vaha=form.vaha.data)
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

