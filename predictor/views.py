from pathlib import Path
import joblib
import pandas as pd
from django.shortcuts import render
from .forms import InsurancePredictionForm
from .models import PredictionRecord

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'model' / 'insurance_cost_model.joblib'
model = joblib.load(MODEL_PATH)

def classify_bmi_value(bmi):
    if bmi < 18.5: return 'Underweight'
    if bmi < 25: return 'Healthy Weight'
    if bmi < 30: return 'Overweight'
    if bmi < 35: return 'Obesity Class 1'
    if bmi < 40: return 'Obesity Class 2'
    return 'Obesity Class 3'

def region_weather(region):
    weather_map = {'northeast': ('New York', 15.6, 78, 9.4), 'northwest': ('Seattle', 10.5, 85, 13.8), 'southeast': ('Miami', 27.5, 74, 13.7), 'southwest': ('Phoenix', 26.6, 17, 9.4)}
    return weather_map[region]

def dashboard(request):
    recent_predictions = PredictionRecord.objects.order_by('-created_at')[:5]
    return render(request, 'predictor/dashboard.html', {'recent_predictions': recent_predictions})

def predict(request):
    prediction = None
    form = InsurancePredictionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        city, temp, humidity, wind = region_weather(data['region'])
        high_bmi_flag = 1 if data['bmi'] >= 30 else 0
        smoker_flag = 1 if data['smoker'] == 'yes' else 0
        age_risk_flag = 1 if data['age'] >= 50 else 0
        risk_score = high_bmi_flag * 2 + smoker_flag * 3 + age_risk_flag
        risk_category = 'Low Risk' if risk_score <= 1 else ('Medium Risk' if risk_score <= 3 else 'High Risk')
        input_df = pd.DataFrame([{'age': data['age'], 'sex': data['sex'], 'bmi': data['bmi'], 'children': data['children'], 'smoker': data['smoker'], 'region': data['region'], 'high_bmi_flag': high_bmi_flag, 'smoker_flag': smoker_flag, 'age_risk_flag': age_risk_flag, 'risk_score': risk_score, 'risk_category': risk_category, 'bmi_category': classify_bmi_value(data['bmi']), 'region_temperature_c': temp, 'region_humidity_percent': humidity, 'region_wind_speed': wind}])
        prediction = round(float(model.predict(input_df)[0]), 2)
        PredictionRecord.objects.create(age=data['age'], sex=data['sex'], bmi=data['bmi'], children=data['children'], smoker=data['smoker'], region=data['region'], predicted_charge=prediction)
    return render(request, 'predictor/predict.html', {'form': form, 'prediction': prediction})
