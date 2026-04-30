import json
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Ticket, Ai_summarry, Assignment, Worklog
from .serializers import (
    TicketSerializer,
    Ai_SummarrySerializer,
    AssignmentSerializer,
    WorklogSerializer,
)
from .services import ai_services
from .filters import TicketFilter, WorklogFilter, AssignmentFilter, Ai_summarryFilter
from .pagination import defaultPagination


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TicketFilter
    search_fields = ["ticket__title", "user__username"]
    ordering_fields = ["created_at"]
    pagination_class = defaultPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.select_related(
            "user", "ai_summarry"
        ).prefetch_related("ticket_worklogs")

        if user.is_staff:
            return queryset
        return queryset.filter(user=user)

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "DELETE"]:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        ticket = serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if (
            self.request.user != self.get_object().user
            and not self.request.user.is_staff
        ):
            raise PermissionDenied("You can only edit your own tickets")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only delete your own tickets")
        instance.delete()


class AiSummarry(ListCreateAPIView):
    http_method_names = ["post", "get"]
    queryset = Ai_summarry.objects.select_related("ticket").all()
    serializer_class = Ai_SummarrySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = Ai_summarryFilter
    ordering_fields = ["created_at"]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_context(self):
        return {"ticket_id": self.kwargs["Ticket_pk"]}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = get_object_or_404(Ticket,id=self.kwargs["Ticket_id"])

        ai_output = ai_services.generate_ai_summarry(ticket.description)

        try:
            ai_data = json.loads(ai_output)
        except:
            return Response(
                {"error": "AI response format invalid"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer.save(
            summarry=ai_data.get("summary") or "No summary provided",
            priority=ai_data.get("priority") or "Low",
            category=ai_data.get("category") or "Technical",
            suggestion=ai_data.get("suggestion") or "No suggestion provided",
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.select_related("ticket", "user").all()
    serializer_class = AssignmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AssignmentFilter
    search_fields = ["user__username", "ticket__title"]
    ordering_fields = ["created_at"]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_context(self):
        return {"request": self.request}


class WorklogViewSet(ModelViewSet):
    serializer_class = WorklogSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WorklogFilter
    ordering_fields = ["created_at"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Worklog.objects.select_related("ticket", "user").all()
        if user.is_staff:
            return queryset
        return queryset.filter(user=user)

    def get_serializer_context(self):
        return {"ticket_id": self.kwargs["tickets_pk"]}

    def perform_create(self, serializer):
        worklog = serializer.save(user=self.request.user)
        ticket = Ticket.objects.get(id=self.kwargs["tickets_pk"])

        if ticket.status == Ticket.STATUS_COMPLETED:
            raise ValidationError("Ticket already completed")

        if ticket.status in [Ticket.STATUS_PENDING, Ticket.STATUS_ASSIGNED]:
            ticket.status = Ticket.STATUS_INPROGRESS

        if hasattr(worklog, "is_completion_log") and worklog.is_completion_log:
            ticket.status = Ticket.STATUS_COMPLETED
            ticket.completed_at = timezone.now()

        ticket.save()
        

    def perform_update(self, serializer):
        worklog = self.get_object()

        if self.request.user != worklog.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only edit your own worklogs")

        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only delete your own worklogs")

        instance.delete()
