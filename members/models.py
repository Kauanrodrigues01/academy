from django.db import models
from django.utils import timezone

class Member(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    start_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=False)  # Atualizado dinamicamente
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Campos de pagamento
    payment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def update_activity_status(self):
        """Atualiza o status de atividade do membro com base na data de pagamento."""
        now = timezone.now().date()
        # Verifica se o pagamento foi realizado nos últimos 30 dias
        if self.payment_date >= now - timezone.timedelta(days=30):
            self.is_active = True
        else:
            self.is_active = False
        self.save()

    def last_payment_date(self):
        """Retorna a última data de pagamento do membro."""
        return self.payment_date
