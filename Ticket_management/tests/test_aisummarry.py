# Always test behaviour rather than implementation
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from  Ticket_management.models import Ticket

User = get_user_model()


@pytest.mark.django_db
class TestAisummarryApi:

    def test_if_user_is_anonymous_return_401(self):
        client = APIClient()
        ticket = baker.make(Ticket)

        response = client.post( f'/api/v1/tickets/{ticket.id}/ai-summary/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_not_admin_return_403(self):
        user = User.objects.create_user(
            username='normal_user',
            password='pass',
            is_staff=False
        )

        client = APIClient()
        client.force_authenticate(user=user)
        ticket = baker.make(Ticket)

        response = client.post(f'/api/v1/tickets/{ticket.id}/ai-summary/')

        assert response.status_code == status.HTTP_403_FORBIDDEN


    