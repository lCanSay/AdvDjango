from django.forms import ModelForm
from .models import Category, Expense

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['name','amount', 'category', 'description', 'date']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']  