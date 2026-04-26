# Always test behaviour rather than implementation
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestTicketApi:

    def test_if_user_is_anonymous_return_401(self):
        client = APIClient()

        response = client.post('/ticket/', {
            "title": "Test",
            "location": "Nairobi",
            "description": "Test issue",
            "status": "P"
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_return_400(self):
        admin = User.objects.create_user(
            username='admin',
            password='pass',
            is_staff=True
        )

        client = APIClient()
        client.force_authenticate(user=admin)

        response = client.post('/ticket/', {
            "title": "",
            "location": "",
            "description": "",
            "status": ""
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None


    def test_if_data_is_valid_return_201(self):
        admin = User.objects.create_user(
            username='admin2',
            password='pass',
            is_staff=True
        )

        client = APIClient()
        client.force_authenticate(user=admin)

        response = client.post('/ticket/', {
            "title": "Test title",
            "location": "Nairobi",
            "description": "Test issue",
            "status": "P"
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0