from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Food, Consume, HealthGoal
from .forms import FoodForm, HealthGoalForm
from django.contrib.auth.forms import UserCreationForm

def index(request):
    if request.method =="POST":
        food_consumed = request.POST['food_consumed']
        c = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=c)
        consume.save()
        foods = Food.objects.all()
    else:
        foods = Food.objects.all()
        user = request.user
    consumed_food = Consume.objects.filter(user=user)
    health_goal = HealthGoal.objects.filter(user=user).first()

    context = {
        'foods': foods,
        'consumed_food': consumed_food,
        'health_goal': health_goal,
    }

    return render(request, 'app/index.html', context)

def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method=="POST":
        consumed_food.delete()
        return redirect('/')
    return render(request, 'app/delete.html')

def create_goal(request):
    health_goal, created = HealthGoal.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = HealthGoalForm(request.POST, instance=health_goal)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('/')
    else:
        form = HealthGoalForm(instance=health_goal)

    return render(request, 'app/create_goal.html', {'form': form})

def chart_data(request):
    consumed = Consume.objects.filter(user=request.user)
    health_goal = HealthGoal.objects.filter(user=request.user).first()

    goal_data = {
        "goal_carbs": health_goal.carb_goal if health_goal else 0,
        "goal_proteins": health_goal.protein_goal if health_goal else 0,
        "goal_fats": health_goal.fat_goal if health_goal else 0,
        "goal_calories": health_goal.daily_calorie_goal if health_goal else 0,
    }

    data = {
        "labels": [c.food_consumed.name for c in consumed],
        "carbs": [c.food_consumed.carbs for c in consumed],
        "proteins": [c.food_consumed.proteins for c in consumed],
        "fats": [c.food_consumed.fats for c in consumed],
        "calories": [c.food_consumed.calorie for c in consumed],

        "goal_carbs": health_goal.carb_goal if health_goal else 0,
        "goal_proteins": health_goal.protein_goal if health_goal else 0,
        "goal_fats": health_goal.fat_goal if health_goal else 0,
        "goal_calories": health_goal.daily_calorie_goal if health_goal else 0,
    }
    return JsonResponse(data)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "app/register.html", {"form": form})


def add_food(request):
    if request.method == "POST":
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect("index") 
    else:
        form = FoodForm()
    return render(request, "app/add_food.html", {"form": form})


