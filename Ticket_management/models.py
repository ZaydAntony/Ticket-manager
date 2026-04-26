from django.db import models
from django.conf import settings

class Ticket(models.Model):
    STATUS_PENDING = 'P'
    STATUS_ASSIGNED= 'A'
    STATUS_INPROGRESS = 'I'
    STATUS_COMPLETED = 'C'

    STATUS_UPDATES =[
        (STATUS_PENDING, 'Pending'),
        (STATUS_ASSIGNED, 'Assigned'),
        (STATUS_INPROGRESS, 'In-Progress'),
        (STATUS_COMPLETED, 'Completed'),

    ]
    title = models.CharField(max_length=40, null=False)
    location = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_UPDATES, default=STATUS_PENDING, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return f"{self.title}, {self.get_status_display()}, {self.user.username}"


class Assignment(models.Model):
    assigned_at = models.DateTimeField(auto_now_add =True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='assignment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignments')

    def __str__(self):
        return f"{self.ticket.title}, Assigned to: {self.user.username}"


class Worklog(models.Model):
    notes = models.TextField()
    is_completed_worklog = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_worklogs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='worklogs')

    def __str__(self):
        return f"{self.ticket.title}, {self.user.username}"



class Ai_summarry(models.Model):
    CATEGORY_BILLING = 'B'
    CATEGORY_COMPLAINT = 'C'
    CATEGORY_TECHNICAL ='T'
    CATEGORY_CONNECTIVITY = 'N'

    CATEGORY_STATES= [
    (CATEGORY_BILLING, 'Billing'),
    (CATEGORY_COMPLAINT,'Complaint'),
    (CATEGORY_TECHNICAL, 'Technical'),
    (CATEGORY_CONNECTIVITY, 'Connectivity'),
    ]

    PRIORITY_HIGH = 'H'
    PRIORITY_LOW = 'L'

    PRIORITY_STATES =[
        (PRIORITY_HIGH,'High'),
        (PRIORITY_LOW , 'Low')
    ]
    summarry = models.TextField()
    suggestion = models.TextField()
    category = models.CharField(max_length=1, choices=CATEGORY_STATES, db_index=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_STATES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='ai_summarry')

    def __str__ (self):
        return f"{self.ticket.title}, {self.get_priority_display()}, {self.get_category_display()}"
