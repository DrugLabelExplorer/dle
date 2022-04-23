from django.db import IntegrityError
from django.test import TestCase
from django.test import Client
from django.contrib.auth import authenticate, login
from .models import MyLabel, User
from data.models import DrugLabel


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


class MyLabelModelTests(TestCase):

    def setUp(self):
        username = "test"
        email = "test@druglabelexplorer.org"
        password = "12345"
        self.user = User.objects.create_user(username, email, password)
        self.client = Client()
        self.logged_in = self.client.login(username=username, password=password)

    def logout_user(self):
        self.client.logout()

    def test_can_insert_my_label(self):
        num_entries = MyLabel.objects.count()
        dl = DrugLabel(
            source="EMA",
            product_name="Diffusia",
            generic_name="lorem ipsem",
            version_date="2022-03-15",
            source_product_number="ABC-123-DO-RE-ME",
            raw_text="Fake raw label text",
            marketer="Landau Pharma",
        )
        dl.save()
        
        ml = MyLabel(
            user=self.user,
            drug_label=dl,
        )
        ml.save()

        num_new_entries = MyLabel.objects.count()
        self.assertEqual(num_entries + 1, num_new_entries)

    def test_can_load_my_labels_html(self):
        response = self.client.get("/users/my_labels/", {"user": self.user})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/my_labels.html")

    def test_null_user_cannot_access_my_labels(self):
        self.logout_user()
        response = self.client.get("/users/my_labels/")
        self.assertEqual(response.status_code, 302)
