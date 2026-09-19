# Create your views here.
from main.models import Experience, Achievement, Project
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ProjectForm, ExperienceForm

def show_main(request):
    context = {
        "name": "Enzo Susilo",
        "npm": "2506584382",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Halo, saya Enzo Susilo, mahasiswa S1 Ilmu Komputer di Fasilkom Universitas Indonesia angkatan 2025 dengan minat mendalam pada kecerdasan buatan, cybersecurity, dan data science. "
            "Berbekal fondasi matematis yang kuat dan hobi memecahkan tantangan yang ada."
        ),
    }
    return render(request, "index.html", context)




def show_achievements(request):
    context = {
        "name": "Enzo Susilo",
        "achievements_list": Achievement.objects.all(),
    }
    return render(request, "achievements.html", context)

def create_project(request):
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

    context = {
        "name": "Enzo Susilo",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
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

    context = {
        "name": "Enzo Susilo",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def create_experience(request):
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

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def update_experience(request, experience_id):
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