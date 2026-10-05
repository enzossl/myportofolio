from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.forms import ExperienceForm
from main.models import Experience, Achievement


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami dasar pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="experience-search-form"')
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="error"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="grid"')
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_experience_json_contains_data_and_star_information(self):
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["pk"], str(self.experience.id))
        self.assertEqual(data[0]["fields"]["title"], self.experience.title)
        self.assertEqual(data[0]["fields"]["category"], "Part-Time")
        self.assertEqual(data[0]["fields"]["star_count"], 0)
        self.assertFalse(data[0]["fields"]["is_starred"])
        self.assertTrue(data[0]["fields"]["is_ongoing"])

    def test_experience_json_search_filters_by_title(self):
        Experience.objects.create(
            title="Relawan Acara",
            description="Membantu pelaksanaan acara.",
            category="volunteer",
        )

        response = self.client.get(
            reverse("main:get_experience_json"),
            {"title": "Asisten"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["title"], self.experience.title)

    def test_experience_json_marks_star_for_logged_in_user(self):
        user = User.objects.create_user(username="reader", password="password123")
        self.experience.starred_by.add(user)
        self.client.force_login(user)

        response = self.client.get(reverse("main:get_experience_json"))

        fields = response.json()[0]["fields"]
        self.assertEqual(fields["star_count"], 1)
        self.assertTrue(fields["is_starred"])
        self.assertEqual(fields["starred_by_names"], user.username)

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(
            response,
            "Belum ada experience yang ditambahkan atau ditemukan.",
        )

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertFalse(response.json()[0]["fields"]["is_ongoing"])

    def test_experience_form_rejects_title_containing_only_html(self):
        form = ExperienceForm(data={
            "title": '<img src="x" onerror="alert(1)">',
            "description": "Deskripsi aman",
            "category": "part-time",
            "thumbnail": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_experience_form_strips_html_from_description(self):
        form = ExperienceForm(data={
            "title": "Asisten Praktikum",
            "description": "Membantu <b>mahasiswa</b>",
            "category": "part-time",
            "thumbnail": "",
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["description"], "Membantu mahasiswa")

    def test_create_experience_ajax_rejects_unauthorized_user(self):
        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {
                "title": "Pengalaman Baru",
                "description": "Deskripsi pengalaman.",
                "category": "volunteer",
                "thumbnail": "",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_create_experience_ajax_creates_data_for_superuser(self):
        owner = User.objects.create_superuser(
            username="owner",
            email="owner@example.com",
            password="password123",
        )
        self.client.force_login(owner)

        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {
                "title": "Pengalaman Baru",
                "description": "Deskripsi pengalaman.",
                "category": "volunteer",
                "thumbnail": "",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Experience.objects.count(), 2)
        self.assertTrue(Experience.objects.filter(title="Pengalaman Baru").exists())

    def test_create_experience_ajax_returns_validation_errors(self):
        owner = User.objects.create_superuser(
            username="owner",
            email="owner@example.com",
            password="password123",
        )
        self.client.force_login(owner)

        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {
                "title": '<img src="x" onerror="alert(1)">',
                "description": "Deskripsi pengalaman.",
                "category": "volunteer",
                "thumbnail": "",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])

    def test_achievements_url_is_accessible(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievements.html")

    def test_achievements_page_shows_data_and_structure(self):
        Achievement.objects.create(
            title="IELTS Band 7",
            description="Validasi kemahiran berbahasa Inggris.",
            category="certification",
            year="Januari 2025"
        )
        response = self.client.get(reverse("main:show_achievements"))
        self.assertEqual(response.status_code, 200)
        
        # mengecek apakah data model berhasil muncul 
        self.assertContains(response, "IELTS Band 7")
        self.assertContains(response, "Validasi kemahiran berbahasa")
        self.assertContains(response, "Januari 2025")

    def test_empty_achievements_page(self):
        # memastikan pesan kosong muncul saat data tidak ada
        Achievement.objects.all().delete()
        response = self.client.get(reverse("main:show_achievements"))
        self.assertContains(response, "Belum ada pencapaian akademik yang ditambahkan.")
