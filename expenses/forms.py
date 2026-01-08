from django import forms
from .models import Expense, Category, Budget

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            "title",
            "amount",
            "category",
            "date",
            "payment_mode",
            "merchant_name",
            "location",
            "note",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Expense Title"}),
            "amount": forms.NumberInput(attrs={"placeholder": "Amount"}),
            "category": forms.Select(),
            "date": forms.DateInput(attrs={"type": "date"}),
            "payment_mode": forms.Select(),
            "merchant_name": forms.TextInput(attrs={"placeholder": "Merchant / Shop name"}),
            "location": forms.TextInput(attrs={"placeholder": "Location (optional)"}),
            "note": forms.Textarea(attrs={"placeholder": "Optional note...", "rows": 3}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Category name"}),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["amount", "month", "year"]
        widgets = {
            "amount": forms.NumberInput(attrs={"placeholder": "Enter monthly budget"}),
            "month": forms.NumberInput(attrs={"placeholder": "Month (1-12)"}),
            "year": forms.NumberInput(attrs={"placeholder": "Year (e.g. 2026)"}),
        }
