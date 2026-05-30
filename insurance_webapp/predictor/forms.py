from django import forms
class InsurancePredictionForm(forms.Form):
    age = forms.IntegerField(min_value=18, max_value=64, label='Age')
    sex = forms.ChoiceField(choices=[('female', 'Female'), ('male', 'Male')], label='Sex')
    bmi = forms.FloatField(min_value=10, max_value=60, label='BMI')
    children = forms.IntegerField(min_value=0, max_value=5, label='Children')
    smoker = forms.ChoiceField(choices=[('no', 'No'), ('yes', 'Yes')], label='Smoker')
    region = forms.ChoiceField(choices=[('northeast', 'Northeast'),('northwest', 'Northwest'),('southeast', 'Southeast'),('southwest', 'Southwest')], label='Region')
