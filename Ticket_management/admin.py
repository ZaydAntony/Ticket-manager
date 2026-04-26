from django.contrib import admin
from .models import Ticket, Assignment, Worklog, Ai_summarry

# 🔹 TICKET ADMIN
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'user', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    ordering = ['-created_at']
    autocomplete_fields = ['user']  # ⚡ better performance


# 🔹 ASSIGNMENT ADMIN
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'assigned_at']
    list_filter = ['assigned_at']
    search_fields = ['ticket__title', 'user__username']
    ordering = ['-assigned_at']
    autocomplete_fields = ['ticket', 'user']

    def save_model(self, request, obj, form, change):
        # 🔥 AUTO UPDATE TICKET STATUS → ASSIGNED
        obj.save()
        ticket = obj.ticket
        if ticket.status == Ticket.STATUS_PENDING:
            ticket.status = Ticket.STATUS_ASSIGNED
            ticket.save()


# 🔹 WORKLOG ADMIN
@admin.register(Worklog)
class WorklogAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['notes', 'ticket__title', 'user__username']
    ordering = ['-created_at']
    autocomplete_fields = ['ticket', 'user']

    # ⚠️ THIS FIXES YOUR ISSUE (no fields/exclude override)

    def save_model(self, request, obj, form, change):
        # Prevent notes from being wiped accidentally
        if change:
            old_obj = Worklog.objects.get(pk=obj.pk)
            if not obj.notes:
                obj.notes = old_obj.notes

        obj.save()

        # 🔥 AUTO STATUS LOGIC
        ticket = obj.ticket

        if ticket.status in [Ticket.STATUS_PENDING, Ticket.STATUS_ASSIGNED]:
            ticket.status = Ticket.STATUS_INPROGRESS

        # Optional: if you later add is_completion_log
        if hasattr(obj, 'is_completion_log') and obj.is_completion_log:
            ticket.status = Ticket.STATUS_COMPLETED

        ticket.save()


# 🔹 AI SUMMARY ADMIN
@admin.register(Ai_summarry)
class AiSummarryAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'priority', 'category', 'created_at']
    list_filter = ['priority', 'category', 'created_at']
    search_fields = ['summarry', 'suggestion', 'ticket__title']
    ordering = ['-created_at']
    autocomplete_fields = ['ticket']