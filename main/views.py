# Create your views here.
from main.models import Experience, Achievement, Project
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from main.forms import ProjectForm, ExperienceForm
import datetime
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Enzo Susilo",
        "npm": "2506584382",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Halo, saya Enzo Susilo, mahasiswa S1 Ilmu Komputer di Fasilkom Universitas Indonesia angkatan 2025 dengan minat mendalam pada kecerdasan buatan, cybersecurity, dan data science. "
            "Berbekal fondasi matematis yang kuat dan hobi memecahkan tantangan yang ada."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)




def show_achievements(request):
    context = {
        "name": "Enzo Susilo",
        "achievements_list": Achievement.objects.all(),
    }
    return render(request, "achievements.html", context)

@login_required(login_url="/login/")
def create_project(request):
    if not (request.user.is_superuser or (request.user.is_authenticated and request.user.groups.filter(name="Editor").exists())):
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Enzo Susilo",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()
    is_admin = request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name="Editor").exists())
    context = {
        "name": "Enzo Susilo",
        "project_list": projects,
        "title_query": title_query,
        "is_admin": is_admin,
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not (request.user.is_superuser or (request.user.is_authenticated and request.user.groups.filter(name="Editor").exists())):
        raise PermissionDenied
        
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

#untuk experience 

def show_experience(request):
    json_response = get_experience_json(request)
    
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()
    is_admin = request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name="Editor").exists())

    context = {
        "name": "Enzo Susilo",
        "experience_list": experiences,
        "title_query": title_query,
        "is_admin": is_admin,
    }
    return render(request, "experience.html", context)

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    return HttpResponse(experiences_json, content_type="application/json")

@login_required(login_url="/login/")
def create_experience(request):
    if not (request.user.is_superuser or (request.user.is_authenticated and request.user.groups.filter(name="Editor").exists())):
        raise PermissionDenied
    
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Enzo Susilo",
        "form": form,
    }
    return render(request, "experiences_form.html", context)

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not (request.user.is_superuser or (request.user.is_authenticated and request.user.groups.filter(name="Editor").exists())):
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not (request.user.is_superuser or (request.user.is_authenticated and request.user.groups.filter(name="Editor").exists())):
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)
    # instance=experience memastikan form terisi dengan data yang sudah ada
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Enzo Susilo",
        "form": form,
    }
    # Kita bisa menggunakan template form yang sama dengan fungsi create
    return render(request, "experiences_form.html", context)

#tutorial 4
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Enzo Susilo",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Enzo Susilo",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)
    return redirect("main:show_experience")