from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout_user'), 
    path('add-expense/', views.add_expense, name='add_expense'),
    path('edit-expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('set-budget/', views.set_budget, name='set_budget'),
    path('budget-report/', views.budget_report, name='budget_report'),
    path('export-excel/', views.export_excel, name='export_excel'), 
]
