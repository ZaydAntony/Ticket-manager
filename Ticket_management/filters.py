from django_filters.rest_framework import FilterSet
from . models import Ticket, Assignment, Worklog, Ai_summarry

class TicketFilter(FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'status': ['exact'],
            'created_at':['exact', 'gte', 'lte'],
            'location': ['exact', 'icontains']
        }

class AssignmentFilter(FilterSet):
    class Meta:
        model = Assignment 
        fields ={
            'user': ['exact'],
            'assigned_at': ['exact','gte', 'lte']
        }

class WorklogFilter(FilterSet):
    class Meta:
        model = Worklog
        fields = {
            'user': ['exact'],
            'created_at': ['exact', 'gte', 'lte']
        }

class Ai_summarryFilter(FilterSet):
    class Meta:
        model = Ai_summarry
        fields = {
            'category': ['exact'],
            'priority': ['exact'],
            'created_at': ['exact', 'gte', 'lte']
        }