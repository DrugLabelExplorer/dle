from datetime import date
from urllib import response
from django.test import TestCase
#from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from .models import MyQueries, User


# Create your tests here.
class User_tests(TestCase):
    def test_dummy(self):
        self.assertEqual(1, 1)

    def test_register_users(self):
        client = Client()
        response = client.post(
            "/users/register/",
            {
                "username": "testuser",
                "email": "testuser@gmail.com",
                "password": "testuser",
                "confirmation": "testuser",
            },
        )
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    #    def test_register_page(self):
    #        self.assertEqual(response.status_code,200)
    #        self.assertTemplateUsed(response,'dle/users/templates/users/register.html')

    def test_login_users(self):
        client = Client()
        response = client.post(
            "/users/login/",
            {
                "username": "testuser",
                #  "email": 'testuser@gmail.com',
                "password": "testuser"
                #   "confirmation": 'testuser'
            },
        )
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_logout_users(self):
        client = Client()
        response = client.post(
            "/users/login/",
            {
                "username": "testuser",
                #  "email": 'testuser@gmail.com',
                "password": "testuser"
                #   "confirmation": 'testuser'
            },
        )
        print(response.status_code)
        response = client.get("/users/logout/")
        self.assertEqual(response.status_code, 302)

        #  user= User.objects.filter(email=self.user['email']).first()
        #  user.is_active=True
        #  user.save()
        #  self.assertEqual(response.status_code,302)

    # def test_login_page(self):
    #     response = self.login_url
    #     self.assertEqual(response.status_code,200)
    #     self.assertTemplateUsed(response,'dle/users/templates/users/login.html')
    def test_insert_myLabel(self):
        user = User.objects.create_user(
            username="testuser", email="testuser@gmail.com")

        num_entries = MyQueries.objects.count()

        dl = MyQueries(
            user=user,
            #date= date.today(),
            query="test query",
            results="[]"
        )
        dl.save()

        new_num_entries = MyQueries.objects.count()
        self.assertEqual(num_entries + 1, new_num_entries)