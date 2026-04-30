# Always test behaviour rather than implementation
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from Ticket_management.models import Ticket

User = get_user_model()


@pytest.mark.django_db
class TestWorklogApi:

    def test_if_user_is_anonymous_return_401(self):
        admin = User.objects.create_user(
            username='admin',
            password='pass',
            is_staff=True
        )

        client = APIClient()
        ticket=baker.make(Ticket)
        response = client.post(f'/api/v1/tickets/{ticket.id}/worklogs/',{
            "notes":"test note",
            "user":admin.id
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
        ticket = baker.make(Ticket)

        response = client.post(f'/api/v1/tickets/{ticket.id}/worklogs/')

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

        ticket = baker.make(Ticket)

        response = client.post(f'/api/v1/tickets/{ticket.id}/worklogs/',{
            "notes":"test note",
            "user":admin.id
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0