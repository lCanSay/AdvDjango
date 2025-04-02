from django.contrib import admin
from .models import Category, Expense, ExpenseFilter, GroupExpense

# Register your models here.
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(GroupExpense)

