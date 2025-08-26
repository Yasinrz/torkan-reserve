from django.db import models
from accounts.models import User

class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.receiver.name} - {self.message}"
