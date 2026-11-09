import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ExperienceAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser(
            username="experience-owner", password="test-password",
            email="owner@example.com",
        )
        cls.reader = User.objects.create_user(
            username="experience-reader", password="test-password",
        )
        cls.editor = User.objects.create_user(
            username="experience-editor", password="test-password",
        )
        cls.editor.groups.add(Group.objects.create(name="Editor"))
        cls.experience = Experience.objects.create(
            title="Original experience", description="Original description",
            category="volunteer",
        )

    def setUp(self):
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "New experience", "description": "A useful experience",
            "category": "research", "thumbnail": "",
        }

    def data_snapshot(self):
        return list(Experience.objects.order_by("id").values(
            "id", "title", "description", "category", "thumbnail",
        ))

    def test_guest_and_reader_are_read_only(self):
        original = self.data_snapshot()
        for user in (None, self.reader):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.get(self.list_url).status_code, 200)
            self.assertEqual(self.client.get(self.detail_url).status_code, 200)
            for method, url, payload in (
                ("post", self.list_url, self.payload),
                ("patch", self.detail_url, {"title": "Forbidden"}),
                ("put", self.detail_url, self.payload),
                ("delete", self.detail_url, None),
            ):
                with self.subTest(user=user, method=method):
                    response = getattr(self.client, method)(url, payload, format="json")
                    self.assertEqual(response.status_code, 403)
                    self.assertEqual(self.data_snapshot(), original)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        original = self.data_snapshot()
        for url in (self.list_url, self.detail_url):
            for method in ("get", "head", "options"):
                self.assertEqual(getattr(self.client, method)(url).status_code, 200)
                self.assertEqual(self.data_snapshot(), original)

        response = self.client.patch(
            self.detail_url, {"title": "Edited by Editor"}, format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited by Editor")
        self.assertEqual(self.experience.description, "Original description")

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, self.payload["title"])
        self.assertEqual(self.experience.description, self.payload["description"])

        original = self.data_snapshot()
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code, 403,
        )
        self.assertEqual(self.data_snapshot(), original)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(self.data_snapshot(), original)

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        created_id = response.data["id"]
        self.assertTrue(Experience.objects.filter(pk=created_id).exists())
        detail_url = reverse("api:experience-detail", args=[created_id])

        response = self.client.patch(detail_url, {"title": "Owner update"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Experience.objects.get(pk=created_id).title, "Owner update")
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=created_id).exists())
        self.assertEqual(self.client.get(detail_url).status_code, 404)

    def test_search_is_case_insensitive_and_supports_empty_results(self):
        Experience.objects.create(
            title="Different role", description="Another item", category="research",
        )
        response = self.client.get(self.list_url, {"title": " ORIGINAL "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data], [str(self.experience.id)])
        self.assertEqual(self.client.get(self.list_url, {"title": "not-found"}).data, [])
        self.assertEqual(len(self.client.get(self.list_url, {"title": "   "}).data), 2)

    def test_serializer_preserves_labels_status_and_current_user_star(self):
        self.experience.starred_by.add(self.reader)
        self.client.force_authenticate(user=self.reader)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["category"], "volunteer")
        self.assertEqual(response.data["category_display"], "Volunteer")
        self.assertTrue(response.data["is_ongoing"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], self.reader.username)
        self.assertNotIn("starred_by", response.data)
        self.assertNotIn(self.reader.password, response.content.decode())
        self.assertNotIn(self.owner.email, response.content.decode())

        self.experience.ended_at = timezone.now()
        self.experience.save(update_fields=["ended_at"])
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertFalse(response.data["is_ongoing"])
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

    def test_star_requires_login_toggles_and_uses_current_user(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertEqual(self.experience.starred_by.count(), 0)
        for user in (self.reader, self.editor, self.owner):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.post(
                    self.star_url, {"user_id": self.owner.pk}, format="json",
                )
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.data["is_starred"])
                self.assertEqual(response.data["star_count"], 1)
                self.assertEqual(
                    list(self.experience.starred_by.values_list("pk", flat=True)), [user.pk],
                )
                response = self.client.post(self.star_url)
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.data["is_starred"])
                self.assertEqual(self.experience.starred_by.count(), 0)

    def test_invalid_input_is_rejected_and_text_is_cleaned(self):
        self.client.force_authenticate(user=self.owner)
        original = self.data_snapshot()
        for changes, field in (
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"description": "<b></b>"}, "description"),
            ({"category": "not-a-category"}, "category"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
        ):
            with self.subTest(changes=changes):
                response = self.client.post(
                    self.list_url, {**self.payload, **changes}, format="json",
                )
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
                self.assertEqual(self.data_snapshot(), original)
        response = self.client.post(self.list_url, {
            **self.payload, "title": "<b>Clean title</b>",
            "description": "<b>Clean description</b>",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        saved = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(saved.title, "Clean title")
        self.assertEqual(saved.description, "Clean description")

    def test_computed_fields_and_id_cannot_be_forged(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = str(uuid.uuid4())
        response = self.client.post(self.list_url, {
            **self.payload, "id": forged_id, "star_count": 99,
            "is_starred": True, "starred_by_names": "forged",
            "starred_by": [self.reader.pk], "is_ongoing": False,
            "ended_at": "2000-01-01T00:00:00Z", "category_display": "forged",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], forged_id)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")
        self.assertEqual(response.data["category_display"], "Research")
        saved = Experience.objects.get(pk=response.data["id"])
        self.assertIsNone(saved.ended_at)
        self.assertEqual(saved.starred_by.count(), 0)

    def test_missing_objects_and_wrong_methods(self):
        self.assertEqual(self.client.get(reverse(
            "api:experience-detail", args=[uuid.uuid4()],
        )).status_code, 404)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)

    def test_session_writes_without_csrf_are_rejected(self):
        original = self.data_snapshot()
        for user, method, url, payload in (
            (self.owner, "post", self.list_url, self.payload),
            (self.editor, "patch", self.detail_url, {"title": "Forbidden without CSRF"}),
            (self.reader, "post", self.star_url, {}),
            (self.owner, "delete", self.detail_url, None),
        ):
            with self.subTest(user=user, method=method):
                client = APIClient(enforce_csrf_checks=True)
                self.assertTrue(client.login(username=user.username, password="test-password"))
                response = getattr(client, method)(url, payload, format="json")
                self.assertEqual(response.status_code, 403)
                self.assertIn("CSRF", str(response.data["detail"]))
                self.assertEqual(self.data_snapshot(), original)
                self.assertEqual(self.experience.starred_by.count(), 0)

    def test_session_writes_with_csrf_succeed_for_allowed_roles(self):
        def session_client(user):
            client = APIClient(enforce_csrf_checks=True)
            self.assertTrue(client.login(username=user.username, password="test-password"))
            self.assertEqual(client.get(reverse("main:show_experience")).status_code, 200)
            return client, client.cookies["csrftoken"].value

        owner, owner_token = session_client(self.owner)
        response = owner.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=owner_token,
        )
        self.assertEqual(response.status_code, 201)
        created_id = response.data["id"]
        editor, editor_token = session_client(self.editor)
        response = editor.patch(self.detail_url, {"title": "Editor session update"},
                                format="json", HTTP_X_CSRFTOKEN=editor_token)
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Editor session update")
        reader, reader_token = session_client(self.reader)
        response = reader.post(self.star_url, format="json", HTTP_X_CSRFTOKEN=reader_token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.experience.starred_by.filter(pk=self.reader.pk).exists())
        response = owner.delete(reverse("api:experience-detail", args=[created_id]),
                                HTTP_X_CSRFTOKEN=owner_token)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Experience.objects.filter(pk=created_id).exists())
