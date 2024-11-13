from django.db import models
from django.utils import timezone
from users.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    phone = models.CharField(max_length=15)
    start_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({self.user.cpf})"
    

class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"{self.member.user.full_name} - {'Paid' if self.is_paid else 'Not Paid'}"
    
    def check_payment_status(self):
        """Check if the member's payment is up-to-date."""
        if self.payment_date >= timezone.now() - timezone.timedelta(days=30):
            self.is_paid = True
        else:
            self.is_paid = False
        self.save()

