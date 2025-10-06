from flask.views import MethodView
from flask import Flask, render_template, request
from wtforms import Form, StringField, SubmitField, SelectField

from dotenv import load_dotenv
import os

from temperatures import get_temperature, get_lattitude_longitude
from calories import calculate_calories

load_dotenv()
weather_api_key = os.getenv('API_KEY')

app = Flask(__name__)

class HomePage(MethodView):
    def get(self):
        return render_template('homepage.html')


class CaloriePage(MethodView):
    def get(self):
        user_info = UserCalorieForm()

        return render_template(
            'caloriepage.html',
            user_info=user_info
            )
class ResultsPage(MethodView):
    def post(self):
        user_info = UserCalorieForm(request.form)
        weight = int(user_info.weight.data)
        height = int(user_info.height.data)
        age = int(user_info.age.data)
        activity_level = int(user_info.activity_level.data)
        city = user_info.city.data
        country = user_info.country.data
        gender = user_info.gender.data

        coordinates = get_lattitude_longitude(city, country, weather_api_key)
        temperture = get_temperature(coordinates['lattitude'], coordinates['longitude'], weather_api_key)
        calories = calculate_calories(age, gender, height, weight, activity_level, temperture)
        return render_template(
            'resultspage.html',
            weight=weight,
            height=height,
            age=age,
            city=city,
            country=country,
            gender=gender,
            temperture=temperture,
            calories=calories
            )
class UserCalorieForm(Form):
    weight = StringField('Weight (kg):')
    height = StringField('Height (cm):')
    age = StringField('Age:')
    gender = SelectField('Gender',
                         choices=[('male','male'), ('female','female')])
    activity_level = StringField('How active are you? (1-5)')

    city = StringField('City:')
    country = StringField('Country:')
    submit_button = SubmitField('Calculate')

app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/calories', view_func=CaloriePage.as_view('calorie_page'))
app.add_url_rule('/results', view_func=ResultsPage.as_view('results_page'))

app.run(debug=True)