from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length
from plan_eligibility import PlanEligibilityChecker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-please-change')

class EligibilityForm(FlaskForm):
    plan_id = StringField('HIOS ID', validators=[DataRequired(), Length(min=4)])
    zipcode = StringField('ZIP Code', validators=[DataRequired(), Length(min=5, max=5)])
    year = IntegerField('Plan Year', validators=[DataRequired()])
    submit = SubmitField('Check Eligibility')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = EligibilityForm()
    result = None
    error = None

    if form.validate_on_submit():
        checker = PlanEligibilityChecker()
        try:
            result = checker.check_plan_eligibility(
                form.plan_id.data,
                form.zipcode.data,
                form.year.data
            )
            if not result['success']:
                error = result.get('error', 'An error occurred while checking eligibility')
        except Exception as e:
            error = str(e)

    return render_template('index.html', form=form, result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True) 