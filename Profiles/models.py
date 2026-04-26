from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_ADMIN = 'A'
    USER_CLIENT = 'U'
    USER_TECHNICIAN ='T'

    USER_ROLES = [
        (USER_ADMIN, 'Admin'),
        (USER_CLIENT, 'User'),
        (USER_TECHNICIAN, 'Technician'),
    ]

    email = models.EmailField(unique=True, null=False)
    role = models.CharField(max_length=1, choices=USER_ROLES, default=USER_CLIENT, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    

    def __str__(self):
        return f"{self.username}, {self.get_role_display()}"