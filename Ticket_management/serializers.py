from rest_framework import serializers
from .models import Ticket, Assignment, Worklog, Ai_summarry
from Profiles.models import User


class AssignmentSerializer(serializers.ModelSerializer):

    technician_name = serializers.CharField(
        source="user.username",
        read_only=True
    )

    ticket_title = serializers.CharField(
        source="ticket.title",
        read_only=True
    )

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="T")
    )

    class Meta:
        model = Assignment
        fields = [
            "id",
            "ticket",
            "ticket_title",
            "user",
            "technician_name",
        ]

class WorklogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Worklog
        fields = ["id", "notes", "user"]

    def create(self,validated_data):
        ticket_id = self.context["ticket_id"]
        return Worklog.objects.create(ticket_id=ticket_id, **validated_data)


class Ai_SummarrySerializer(serializers.ModelSerializer):
    summarry = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    priority = serializers.CharField(read_only=True)
    suggestion = serializers.CharField(read_only=True)

    class Meta:
        model = Ai_summarry
        fields = ["id", "summarry", "category", "priority", "suggestion"]

    def create(self, validated_data):
        ticket_id = self.context["ticket_id"]
        return Ai_summarry.objects.create(ticket_id=ticket_id, **validated_data)

    def validate_ticket(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value


class TechnicianSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name"
        ]

class TicketSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

    ai_summarry = Ai_SummarrySerializer(
        read_only=True
    )

    ticket_worklogs = WorklogSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "location",
            "status",
            "user",
            "ai_summarry",
            "ticket_worklogs",
        ]
class UserTicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'location', 'user','status']

