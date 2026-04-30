from rest_framework import serializers
from .models import Ticket, Assignment, Worklog, Ai_summarry


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    ai_summarry = serializers.StringRelatedField(read_only=True)
    ticket_worklogs = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "title", "location", "user", "ai_summarry", "ticket_worklogs"]


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ["id", "user", "ticket"]


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
