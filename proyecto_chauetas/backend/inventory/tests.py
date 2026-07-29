from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Category, Location, Item


class InventoryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_credentials = {'username': 'admin2', 'password': 'testpass'}
        User = get_user_model()
        User.objects.create_user(username=self.user_credentials['username'], password=self.user_credentials['password'])
        Category.objects.all().delete()
        Location.objects.all().delete()
        Item.objects.all().delete()

    def authenticate(self):
        resp = self.client.post('/api/token/', self.user_credentials, format='json')
        self.assertEqual(resp.status_code, 200)
        access = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_token_and_auth_required(self):
        resp = self.client.post('/api/token/', self.user_credentials, format='json')
        self.assertEqual(resp.status_code, 200)
        access = resp.data.get('access')
        unauth = self.client.get('/api/items/')
        self.assertEqual(unauth.status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        resp2 = self.client.get('/api/items/')
        self.assertEqual(resp2.status_code, 200)

    def test_create_category_location_and_item(self):
        self.authenticate()

        resp_cat = self.client.post('/api/categories/', {'name': 'Útiles'}, format='json')
        self.assertEqual(resp_cat.status_code, 201)
        category_id = resp_cat.data['id']

        resp_loc = self.client.post('/api/locations/', {'name': 'Bodega'}, format='json')
        self.assertEqual(resp_loc.status_code, 201)
        location_id = resp_loc.data['id']

        resp_item = self.client.post(
            '/api/items/',
            {
                'name': 'Cuaderno',
                'description': 'Cuaderno de 100 hojas',
                'quantity': 12,
                'category_id': category_id,
                'location_id': location_id,
            },
            format='json'
        )
        self.assertEqual(resp_item.status_code, 201)
        self.assertEqual(resp_item.data['name'], 'Cuaderno')
        self.assertEqual(resp_item.data['quantity'], 12)
        self.assertEqual(str(resp_item.data['category']['id']), category_id)
        self.assertEqual(str(resp_item.data['location']['id']), location_id)
