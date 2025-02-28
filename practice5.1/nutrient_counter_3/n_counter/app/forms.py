from django import forms
from .models import Food, HealthGoal

class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = HealthGoal
        fields = '__all__'

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name", "carbs", "proteins", "fats", "calorie"]
