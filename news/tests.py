from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

from news.models import News

User = get_user_model()


class NewsViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            name="Test User",
            phone_number="1234567890",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_news(self):
        data = {"title": "Test News", "url": "http://example.com"}
        response = self.client.post(reverse("news-list"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        news = News.objects.get(title="Test News")
        self.assertEqual(news.user, self.user)

    def test_destroy_own_news(self):
        news = News.objects.create(title="Test News", url="http://example.com", user=self.user)

        response = self.client.delete(reverse("news-detail", args=[news.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(News.DoesNotExist):
            News.objects.get(id=news.id)

    def test_destroy_other_user_news(self):
        other_user = User.objects.create_user(username="otheruser", email="other@example.com", password="testpassword")
        news = News.objects.create(title="Test News", url="http://example.com", user=other_user)

        response = self.client.delete(reverse("news-detail", args=[news.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(News.objects.filter(id=news.id).exists(), True)

    def test_tech_download_news_from_api(self):
        response = self.client.post(reverse("news-tech-download-news-from-api"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OK", response.data["detail"])
