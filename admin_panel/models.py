from django.db import models
from members.models import Member

class ActivityLog(models.Model):
    EVENT_TYPES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('payment', 'Payment'),
        ('pending', 'Pending'),
    ]

    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.description}"
