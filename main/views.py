from django.shortcuts import render

# Create your views here.

from main.models import Experience


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


def show_experience(request):
    context = {
        "name": "Enzo Susilo",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)