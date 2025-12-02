# portal/urls.py
from django.shortcuts import render
from django.urls import path
from . import views
from .models import DesignRequest

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_request, name='create_request'),
    path('delete/<int:pk>/', views.delete_request, name='delete_request'),

    # Админка
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/status/<int:pk>/', views.update_status, name='update_status'),
    path('admin/categories/', views.manage_categories, name='manage_categories'),
]

def home(request):
    completed_requests = DesignRequest.objects.filter(status='done').order_by('-created_at')[:4]
    in_progress_count = DesignRequest.objects.filter(status='in_progress').count()
    return render(request, 'portal/home.html', {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count,
    })