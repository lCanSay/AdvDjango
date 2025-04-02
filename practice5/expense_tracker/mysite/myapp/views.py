from django.shortcuts import render, redirect
from .forms import CategoryForm, ExpenseForm
from .models import Category, Expense, ExpenseFilter, GroupExpense
from django.db.models import Sum
import datetime
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expense_list.html', {'expenses': expenses})


def index(request):
    if request.method =="POST":
        form = ExpenseForm(request.POST)
        form2 = CategoryForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user 
            expense.save()
            return redirect('index')
        if form2.is_valid():
            category = form2.save(commit=False)
            category.user = request.user 
            category.save()
            return redirect('index')
    
    expenses = Expense.objects.all()
    
    total_expenses = expenses.aggregate(Sum('amount'))
    
    last_year = datetime.date.today()-datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))


    last_month = datetime.date.today()-datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))
    
    
    last_week = datetime.date.today()-datetime.timedelta(days=7)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))    
    
    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    
    categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    
    expense_form = ExpenseForm()

    category_form = CategoryForm()
    
    return render(request, 'myapp/index.html', {'expense_form':expense_form, 'category_form':category_form, 'expenses':expenses, 'total_expenses':total_expenses, 'yearly_sum':yearly_sum, 'monthly_sum':monthly_sum, 'weekly_sum':weekly_sum, 'daily_sums':daily_sums, 'categorical_sums':categorical_sums})

def edit(request, id): 
    expense = Expense.objects.get(id=id, user=request.user)
    expense_form = ExpenseForm(instance=expense)
    
    if request.method =="POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'myapp/edit.html', {'expense_form':expense_form})

def delete(request, id):
    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id, user=request.user)
        expense.delete()
    return redirect('index') 


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    expense_filter = ExpenseFilter(request.GET, queryset=expenses, user=request.user)
    return render(request, 'expense_list.html', {'filter': expense_filter})

@login_required
def add_group_expense(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        users = request.POST.getlist('users')
        group_expense = GroupExpense.objects.create(name=name, amount=amount, date=now())
        group_expense.users.set(users)
    return redirect('group_expense_list')

@login_required
def group_expense_list(request):
    expenses = GroupExpense.objects.all()
    return render(request, 'group_expense_list.html', {'expenses': expenses})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index') 
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})