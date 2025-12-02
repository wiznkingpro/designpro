# views.py (частичный фрагмент — см. ниже полный список всех view)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomUserCreationForm, DesignRequestForm, StatusUpdateForm
from .models import DesignRequest, Category
from django.db.models import Q

# Главная страница
def home(request):
    completed_requests = DesignRequest.objects.filter(status='done').order_by('-created_at')[:4]
    in_progress_count = DesignRequest.objects.filter(status='in_progress').count()
    return render(request, 'portal/home.html', {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count,
    })

# Регистрация
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'portal/register.html', {'form': form})

# Авторизация
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Неверный логин или пароль.")
    return render(request, 'portal/login.html')

# Выход
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    user_requests = DesignRequest.objects.filter(user=request.user).order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        user_requests = user_requests.filter(status=status_filter)
    return render(request, 'portal/dashboard.html', {
        'requests': user_requests,
        'status_choices': DesignRequest.STATUS_CHOICES,
    })

@login_required
def create_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_req = form.save(commit=False)
            design_req.user = request.user
            design_req.save()
            messages.success(request, "Заявка успешно создана!")
            return redirect('dashboard')
        else:
            messages.error(request, "Исправьте ошибки в форме.")
    else:
        form = DesignRequestForm()
    return render(request, 'portal/create_request.html', {'form': form})


@login_required
def delete_request(request, pk):
    req = get_object_or_404(DesignRequest, pk=pk, user=request.user)
    if req.status != 'new':
        messages.error(request, "Можно удалять только заявки со статусом 'Новая'.")
        return redirect('dashboard')
    if request.method == 'POST':
        req.delete()
        messages.success(request, "Заявка удалена.")
        return redirect('dashboard')
    return render(request, 'portal/confirm_delete.html', {'request_obj': req})

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def update_status(request, pk):
    req = get_object_or_404(DesignRequest, pk=pk)
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, request.FILES, instance=req)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно обновлён.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Ошибка при обновлении статуса.")
    else:
        form = StatusUpdateForm(instance=req)
    return render(request, 'portal/update_status.html', {'form': form, 'request_obj': req})

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    requests = DesignRequest.objects.all().order_by('-created_at')
    return render(request, 'portal/admin_dashboard.html', {'requests': requests})







@login_required
@user_passes_test(is_admin)
def manage_categories(request):
    if request.method == 'POST':
        if 'add' in request.POST:
            name = request.POST.get('name')
            if name:
                Category.objects.get_or_create(name=name)
        elif 'delete' in request.POST:
            cat_id = request.POST.get('category_id')
            Category.objects.filter(id=cat_id).delete()
    categories = Category.objects.all()
    return render(request, 'portal/manage_categories.html', {'categories': categories})











