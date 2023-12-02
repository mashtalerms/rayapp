from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(APITestCase):
    def test_authorization_user(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")

        data = {"email": "test@example.com", "password": "testpassword"}
        response = self.client.post("/accounts/auth/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("token", response.data)

    def test_registration(self):
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "testpassword",
            "repeat_password": "testpassword",
            "name": "New User",
            "phone_number": "1234567890",
        }
        response = self.client.post("/accounts/registration/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("token", response.data)

    def test_invalid_registration(self):
        data = {"email": "", "password": "", "repeat_password": "", "name": "", "username": "", "phone_number": ""}
        response = self.client.post("/accounts/registration/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
        self.assertIn("repeat_password", response.data)
        self.assertIn("name", response.data)
        self.assertIn("username", response.data)
        self.assertIn("phone_number", response.data)


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            name="Test User",
            phone_number="1234567890",
        )
        self.client.force_authenticate(user=self.user)

    def test_info(self):
        response = self.client.get("/accounts/profile/info/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("name", response.data)
        self.assertIn("email", response.data)
        self.assertIn("phone_number", response.data)

    def test_change_profile(self):
        data = {"name": "Updated User", "email": "updated@example.com", "phone_number": "9876543210"}
        response = self.client.put("/accounts/profile/change_profile/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Updated User")
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertEqual(self.user.phone_number, "9876543210")

    def test_change_password(self):
        data = {"new_password": "newpassword"}
        response = self.client.put("/accounts/profile/change_password/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword"))
