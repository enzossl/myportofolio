from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada experience yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

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