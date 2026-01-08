from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse

import openpyxl
from datetime import date

from .models import Expense, Category, Budget
from .forms import ExpenseForm, CategoryForm, BudgetForm


def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully!")
        login(request, user)
        return redirect("home")
    return render(request, "expenses/register.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "expenses/login.html")

@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    today = date.today()
    month = today.month
    year = today.year

    budget = Budget.objects.filter(user=request.user, month=month, year=year).first()
    total = sum(exp.amount for exp in expenses if exp.date.month == month and exp.date.year == year)
    crossed = budget and total > budget.amount

    context = {"expenses": expenses, "budget": budget, "total": total, "crossed": crossed}
    return render(request, "expenses/home.html", context)

@login_required
def add_expense(request):
    form = ExpenseForm()
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.created_by = request.user
            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect("home")
    return render(request, "expenses/add_expense.html", {"form": form})


@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    form = ExpenseForm(instance=expense)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated!")
            return redirect("home")
    return render(request, "expenses/edit_expense.html", {"form": form})


@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    messages.success(request, "Expense deleted!")
    return redirect("home")

@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "Category added!")
            return redirect("add_expense")
    return render(request, "expenses/add_category.html", {"form": form})

@login_required
def set_budget(request):
    today = date.today()
    month = today.month
    year = today.year
    budget = Budget.objects.filter(user=request.user, month=month, year=year).first()
    form = BudgetForm(instance=budget)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            new_budget = form.save(commit=False)
            new_budget.user = request.user
            new_budget.month = month
            new_budget.year = year
            new_budget.save()
            messages.success(request, "Budget set!")
            return redirect("home")
    return render(request, "expenses/set_budget.html", {"form": form})


@login_required
def budget_report(request):
    budgets = Budget.objects.filter(user=request.user).order_by("-year", "-month")
    return render(request, "expenses/budget_report.html", {"budgets": budgets})


@login_required
def export_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Expenses"

    
    ws.append(["ID", "Date", "Category", "Title", "Amount",
               "Payment Mode", "Merchant", "Location", "Notes", "Created By"])

    expenses = Expense.objects.filter(user=request.user).order_by("date")
    for exp in expenses:
        ws.append([
            exp.id,
            exp.date.strftime("%Y-%m-%d"),
            exp.category.name,
            exp.title,
            float(exp.amount),
            exp.payment_mode,
            exp.merchant_name,
            exp.location,
            exp.note,
            exp.created_by.username if exp.created_by else ""
        ])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename=expenses.xlsx'
    wb.save(response)
    return response
