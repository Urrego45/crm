from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework.test import APITestCase

class TestSetUp(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.url = reverse('vulnerabilidad-api')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        return super().setUp()

